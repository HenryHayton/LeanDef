"""The prelim-testing endpoint client: one public function (`generate`), structured provenance
logging, and bounded retry against an OpenAI-compatible chat-completions endpoint (what vLLM
serves).

**No provider-specific code.** Configuration is `PRELIM_ENDPOINT_URL` + optional
`PRELIM_API_KEY`, read from the environment (see `prelim.config`). A URL is a URL: RunPod today,
anything speaking the same shape tomorrow, with nothing here to change.

**No prompt logic.** `generate` takes already-built messages. Per-model templates and output
extractors are Stage 2's job and deliberately absent -- this module must not acquire any notion
of which model it is talking to beyond passing `model_name` through.

**Failure behaviour, which is the point of this module.** Prelim testing runs unattended
overnight against a rented GPU pod, so the interesting engineering is entirely in what happens
when things go wrong:

- Retryable (up to `MAX_ATTEMPTS` total, exponential backoff): read timeouts, transport/
  connection errors, 5xx, and 429. These are all "the server or the network is briefly unwell".
- NOT retryable: any other 4xx. A 400 means we built a malformed request (bad sampling params, a
  model name the server doesn't host); looping on it would burn the whole night making the same
  mistake, so it raises immediately and loudly.
- Exhaustion raises `EndpointUnavailable` carrying the last error. The client NEVER returns
  empty text to paper over a failure -- a silent empty completion would land in the sample store
  as though the model had genuinely produced nothing, corrupting the very measurement this
  effort exists to make. Policy (skip the sample? abandon the model? pause the run?) belongs to
  Stage 3's driver, which can only make that decision if the failure reaches it.

Every attempt -- success or final failure -- appends one record to
`prelim_testing/output/call_log.jsonl`, mirroring `bedrock.client`'s provenance discipline and
field style (`timestamp`/`attempt`/`max_attempts`/`http_status`/`outcome`/`latency_s`/`request`/
`response`/`error`). That module is not touched or imported; this is a parallel implementation
of the same convention for a different wire format.
"""

import json
import time
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

import requests

from prelim import config as cfg

# Transient, server-side, worth retrying -- alongside genuine transport failures (connection
# refused, DNS failure, read timeout), which are not HTTP statuses at all. 429 is the standard
# rate-limit/overloaded signal; vLLM returns 503 while a model is still loading, which is
# exactly the case retrying is for. Everything else non-2xx is a well-formed error response
# about OUR request and fails immediately.
_RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, 504})


class PrelimClientError(Exception):
    """Base class for every exception this client raises."""


class EndpointRequestError(PrelimClientError):
    """A well-formed non-retryable error response (4xx other than 429) -- our request is wrong.
    Raised immediately, never retried."""

    def __init__(self, http_status: int, message: str):
        self.http_status = http_status
        self.message = message
        super().__init__(f"endpoint rejected the request (HTTP {http_status}): {message}")


class EndpointMalformedResponseError(PrelimClientError):
    """A 2xx whose body isn't a well-formed chat completion. Not retried: a garbled body from a
    successful call is a contract problem, not a transient one (same reasoning as
    `bedrock.client.BedrockMalformedResponseError`)."""


class EndpointUnavailable(PrelimClientError):
    """Retries exhausted against a retryable failure. Carries the last error so the driver can
    log/decide; `attempts` is how many were made."""

    def __init__(self, attempts: int, last_error: str):
        self.attempts = attempts
        self.last_error = last_error
        super().__init__(f"endpoint unavailable after {attempts} attempt(s); last error: {last_error}")


@dataclass(frozen=True)
class GenerationResult:
    """One successful generation. `prompt_tokens`/`completion_tokens` are `None` when the server
    reports no `usage` object -- absence is recorded honestly rather than defaulted to 0, which
    would be indistinguishable from a genuine zero downstream."""

    text: str
    finish_reason: str | None
    prompt_tokens: int | None
    completion_tokens: int | None
    wall_time_s: float
    model_name: str
    attempts: int  # total attempts made, including the successful one (1 == no retry needed)
    raw_response: dict = field(default_factory=dict)


def _extract_completion(parsed: dict) -> tuple[str, str | None, int | None, int | None]:
    """Same as `_extract`, for the legacy `/v1/completions` shape: the text lives at
    `choices[0].text` rather than `choices[0].message.content`. Everything else (finish_reason,
    optional usage) is identical, so only the one field differs.

    Kept for models whose card documents raw-completion usage. As of the 2026-08-03 card sweep
    all six candidates use chat templates -- including DeepSeek-Prover-V2, which corrects an
    earlier assumption -- so nothing in the current table selects this path. It exists because
    the cost of having it and not needing it is one small function, while the cost of needing it
    mid-run is a dead night.
    """
    choice = parsed["choices"][0]
    text = choice.get("text")
    if text is None:
        text = ""
    if not isinstance(text, str):
        raise TypeError(f"choices[0].text must be a string or null, got {type(text).__name__}")
    usage = parsed.get("usage") or {}
    return text, choice.get("finish_reason"), usage.get("prompt_tokens"), usage.get("completion_tokens")


def _extract(parsed: dict) -> tuple[str, str | None, int | None, int | None]:
    """Pull (text, finish_reason, prompt_tokens, completion_tokens) out of an OpenAI-shaped
    chat-completion body. Raises KeyError/IndexError/TypeError on anything unexpected; the caller
    turns that into `EndpointMalformedResponseError`.

    ASSUMPTION (Stage 2's live smoke test verifies): vLLM's OpenAI-compatible server returns
    `choices[0].message.content` and `choices[0].finish_reason`, with an optional top-level
    `usage`. Two tolerances are built in deliberately rather than assumed away: `usage` may be
    absent entirely (token counts become None), and a `content` of `null` is read as empty text
    rather than crashing -- some servers return null content alongside a `length` finish_reason
    when a generation is cut off before emitting anything.
    """
    choice = parsed["choices"][0]
    message = choice.get("message") or {}
    text = message.get("content")
    if text is None:
        text = ""
    if not isinstance(text, str):
        raise TypeError(f"choices[0].message.content must be a string or null, got {type(text).__name__}")
    finish_reason = choice.get("finish_reason")
    usage = parsed.get("usage") or {}
    return text, finish_reason, usage.get("prompt_tokens"), usage.get("completion_tokens")


def _consume_sse(resp, endpoint_style: str) -> dict:
    """Accumulate an SSE stream into the same dict shape the non-streaming path returns.

    vLLM emits `data: {...}` lines carrying incremental deltas, then `data: [DONE]`. Deltas are
    concatenated; `finish_reason` arrives on the chunk that has it; token counts arrive in a
    final usage-only chunk (requested via `stream_options.include_usage`). The assembled dict
    carries both the accumulated values under `_`-prefixed keys AND a reconstructed `choices`
    array, so the raw_response stored for provenance still looks like a normal completion.

    A malformed individual chunk is skipped rather than fatal: losing one delta degrades a
    sample, whereas raising would discard a generation that is otherwise complete.
    """
    parts: list[str] = []
    finish_reason = None
    prompt_tokens = completion_tokens = None
    model = ""

    for raw in resp.iter_lines(decode_unicode=True):
        if not raw or not raw.startswith("data:"):
            continue
        payload = raw[len("data:"):].strip()
        if payload == "[DONE]":
            break
        try:
            chunk = json.loads(payload)
        except json.JSONDecodeError:
            continue
        model = chunk.get("model") or model
        usage = chunk.get("usage")
        if usage:
            prompt_tokens = usage.get("prompt_tokens", prompt_tokens)
            completion_tokens = usage.get("completion_tokens", completion_tokens)
        for choice in chunk.get("choices") or []:
            if choice.get("finish_reason"):
                finish_reason = choice["finish_reason"]
            piece = (choice.get("delta") or {}).get("content") if endpoint_style == "chat" else choice.get("text")
            if piece:
                parts.append(piece)

    text = "".join(parts)
    return {
        "_text": text,
        "_finish_reason": finish_reason,
        "_prompt_tokens": prompt_tokens,
        "_completion_tokens": completion_tokens,
        "object": "chat.completion" if endpoint_style == "chat" else "text_completion",
        "model": model,
        "streamed": True,
        "choices": [{
            "index": 0,
            "finish_reason": finish_reason,
            **({"message": {"role": "assistant", "content": text}} if endpoint_style == "chat"
               else {"text": text}),
        }],
        "usage": {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens},
    }


def _error_message(body_bytes: bytes) -> str:
    """Best-effort human-readable message from an error body. Falls back to the raw text, so a
    non-JSON error body still produces a readable exception rather than a second, confusing
    JSONDecodeError (same approach as `bedrock.client._parse_error_body`)."""
    try:
        parsed = json.loads(body_bytes)
    except json.JSONDecodeError:
        return body_bytes.decode("utf-8", errors="replace")[:500]
    err = parsed.get("error")
    if isinstance(err, dict):
        return str(err.get("message") or err)
    return str(err or parsed)[:500]


def _log_attempt(
    log_path: Path,
    *,
    attempt: int,
    max_attempts: int,
    model_name: str,
    endpoint_url: str,
    request: dict,
    latency_s: float,
    http_status: int | None,
    outcome: str,
    response: dict | None,
    error: dict | None,
) -> None:
    """Append one structured provenance record. Every attempt is logged, not just the one that
    ultimately succeeds or raises -- so a night's run can be reconstructed exactly, including how
    much of it was spent retrying.

    The request is logged in full (it contains the prompt, which is the thing we most need for
    provenance). The API key is never part of the request body and never logged; the endpoint URL
    is, since it identifies which pod produced a sample.
    """
    record = {
        "timestamp": datetime.now(UTC).isoformat(),
        "model_name": model_name,
        "endpoint_url": endpoint_url,
        "attempt": attempt,
        "max_attempts": max_attempts,
        "http_status": http_status,
        "outcome": outcome,
        "latency_s": latency_s,
        "request": request,
        "response": response,
        "error": error,
    }
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def generate(
    prompt: list[dict] | str,
    *,
    temperature: float,
    max_tokens: int,
    model_name: str,
    endpoint_style: str = "chat",
    # Off by default: streaming is a DEPLOYMENT concern, not a property of the wire format,
    # and this client should stay honest about talking plain OpenAI. `prelim.driver` turns it
    # on because it knows it is going through RunPod's proxy, which 524s long non-streaming
    # requests. Keeping the default off also keeps every non-streaming test meaningful.
    stream: bool = False,
    timeout_s: float | None = None,
    endpoint_url: str | None = None,
    api_key: str | None = None,
    max_attempts: int = cfg.MAX_ATTEMPTS,
    retry_base_delay_s: float = cfg.RETRY_BASE_DELAY_S,
    log_path: Path | None = None,
    sleep_fn=time.sleep,
) -> GenerationResult:
    """Send one generation request and return the result.

    `prompt` is either the OpenAI messages list (`endpoint_style="chat"`, the default) or a
    single prompt string (`endpoint_style="completion"`) -- already built; this module has no
    prompt logic. `endpoint_url`/`api_key` default to the environment (`prelim.config`); passing
    them explicitly is for tests. `sleep_fn` is injectable so retry tests don't wait out backoff.

    `endpoint_url` is expected to name the matching route (`/v1/chat/completions` vs
    `/v1/completions`); the style flag selects the request/response SHAPE, and does not rewrite
    the URL -- guessing a caller's routing would be a surprising thing for a client to do.

    Raises `EndpointRequestError` (4xx, immediate), `EndpointMalformedResponseError` (2xx with an
    unreadable body, immediate), or `EndpointUnavailable` (retryable failures exhausted).
    """
    if endpoint_style not in ("chat", "completion"):
        raise PrelimClientError(f"endpoint_style must be 'chat' or 'completion', got {endpoint_style!r}")
    url = endpoint_url if endpoint_url is not None else cfg.endpoint_url()
    if not url:
        raise PrelimClientError(
            f"no endpoint configured: set ${cfg.ENV_ENDPOINT_URL} or pass endpoint_url= explicitly"
        )
    key = api_key if api_key is not None else cfg.api_key()
    timeout_s = timeout_s if timeout_s is not None else cfg.DEFAULT_TIMEOUT_S
    log_path = log_path if log_path is not None else cfg.CALL_LOG_PATH

    request_body = {
        "model": model_name,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if endpoint_style == "chat":
        if not isinstance(prompt, list):
            raise PrelimClientError("chat endpoint_style requires a messages list")
        request_body["messages"] = prompt
        extract_fn = _extract
    else:
        if not isinstance(prompt, str):
            raise PrelimClientError("completion endpoint_style requires a prompt string")
        request_body["prompt"] = prompt
        extract_fn = _extract_completion

    if stream:
        # Server-Sent Events. REQUIRED for long generations through RunPod's Cloudflare-backed
        # proxy: a non-streaming request sends nothing until the whole completion is ready, and
        # the proxy kills any connection that stays silent too long -- measured live as HTTP 524
        # on an 8192-token request (~246s at the 33 tok/s this A40 sustains). Streaming keeps
        # bytes flowing, so the proxy never sees an idle socket, at any cap or concurrency.
        # `include_usage` asks vLLM for a final chunk carrying token counts, which the
        # non-streaming path gets for free and provenance depends on.
        request_body["stream"] = True
        request_body["stream_options"] = {"include_usage": True}
    headers = {"Content-Type": "application/json"}
    if key:
        # Absent/empty key => no header at all, not an empty one: vLLM is commonly keyless, and
        # some servers reject a malformed `Authorization: Bearer ` outright.
        headers["Authorization"] = f"Bearer {key}"

    last_error_summary = ""
    for attempt in range(1, max_attempts + 1):
        start = time.perf_counter()
        streamed: dict | None = None
        try:
            if stream:
                resp = requests.post(url, json=request_body, headers=headers,
                                     timeout=timeout_s, stream=True)
                http_status = resp.status_code
                if http_status == 200:
                    streamed = _consume_sse(resp, endpoint_style)
                    body_bytes = b""
                else:
                    body_bytes = resp.content
                transport_error = None
            else:
                resp = requests.post(url, json=request_body, headers=headers, timeout=timeout_s)
                http_status, body_bytes, transport_error = resp.status_code, resp.content, None
        except requests.RequestException as e:
            # Covers read/connect timeouts, connection refused, DNS failures, chunked-encoding
            # errors from a dropped connection -- all transient by nature, all retryable.
            http_status, body_bytes, transport_error = None, b"", e
        latency_s = time.perf_counter() - start

        if transport_error is not None:
            last_error_summary = f"{type(transport_error).__name__}: {transport_error}"
            _log_attempt(
                log_path, attempt=attempt, max_attempts=max_attempts, model_name=model_name,
                endpoint_url=url, request=request_body, latency_s=latency_s, http_status=None,
                outcome="transport_error", response=None,
                error={"type": type(transport_error).__name__, "message": str(transport_error)},
            )
            if attempt < max_attempts:
                sleep_fn(retry_base_delay_s * (2 ** (attempt - 1)))
                continue
            raise EndpointUnavailable(attempts=attempt, last_error=last_error_summary)

        if http_status == 200:
            try:
                if streamed is not None:
                    # Already assembled into the SAME shape the non-streaming path produces, so
                    # everything downstream (GenerationResult, the sample file, provenance) is
                    # byte-compatible and nothing else in the pipeline knows streaming happened.
                    parsed = streamed
                    text = parsed["_text"]
                    finish_reason = parsed["_finish_reason"]
                    prompt_tokens = parsed["_prompt_tokens"]
                    completion_tokens = parsed["_completion_tokens"]
                else:
                    parsed = json.loads(body_bytes)
                    text, finish_reason, prompt_tokens, completion_tokens = extract_fn(parsed)
            except (json.JSONDecodeError, KeyError, IndexError, TypeError) as e:
                _log_attempt(
                    log_path, attempt=attempt, max_attempts=max_attempts, model_name=model_name,
                    endpoint_url=url, request=request_body, latency_s=latency_s,
                    http_status=http_status, outcome="malformed_response", response=None,
                    error={
                        "type": type(e).__name__, "message": str(e),
                        "raw_body": body_bytes.decode("utf-8", errors="replace")[:2000],
                    },
                )
                raise EndpointMalformedResponseError(
                    f"endpoint response was not a well-formed chat completion: {type(e).__name__}: {e}"
                ) from e

            _log_attempt(
                log_path, attempt=attempt, max_attempts=max_attempts, model_name=model_name,
                endpoint_url=url, request=request_body, latency_s=latency_s,
                http_status=http_status, outcome="success", response=parsed, error=None,
            )
            return GenerationResult(
                text=text, finish_reason=finish_reason, prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens, wall_time_s=latency_s,
                model_name=model_name, attempts=attempt, raw_response=parsed,
            )

        message = _error_message(body_bytes)
        last_error_summary = f"HTTP {http_status}: {message}"
        retryable = http_status in _RETRYABLE_STATUS_CODES
        _log_attempt(
            log_path, attempt=attempt, max_attempts=max_attempts, model_name=model_name,
            endpoint_url=url, request=request_body, latency_s=latency_s, http_status=http_status,
            outcome="retryable_error" if retryable else "request_error", response=None,
            error={"type": "HTTPError", "message": message},
        )
        if not retryable:
            raise EndpointRequestError(http_status, message)
        if attempt < max_attempts:
            sleep_fn(retry_base_delay_s * (2 ** (attempt - 1)))
            continue
        raise EndpointUnavailable(attempts=attempt, last_error=last_error_summary)

    raise EndpointUnavailable(attempts=max_attempts, last_error=last_error_summary)  # pragma: no cover
