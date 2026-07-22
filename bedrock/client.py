"""A minimal Bedrock (Claude) client: one public method (`BedrockClient.send`), structured
provenance logging, and bounded retry -- built against a local stub server while the company
AWS Bedrock account's access problem is resolved by an admin (see the task that introduced
this module). No prompt templates, structured-output parsing, or pipeline integration here --
that's the next stage-2 task.

**What changes when real AWS access arrives:** fill in real values for
`bedrock.config.REGION`/`AUTHORING_MODEL_ID`/`FLAGSHIP_MODEL_ID`, leave `ENDPOINT_URL` at its
default `None`, and run `bedrock/real_roundtrip.py` once by hand to confirm a genuine
round-trip (see that script's own docstring for why it's manual, never part of the automated
suite). Nothing else needs to change: this module already routes every call through boto3's
own default AWS credential chain and region-based endpoint resolution whenever
`ENDPOINT_URL` is `None` -- that path is untested here (AWS access is unavailable for this
task) but is not new code introduced later, it already exists below.

**Two transports, one shared retry/logging/classification path.** `ENDPOINT_URL is None`
(real Bedrock): `_invoke_real` calls `boto3`'s `bedrock-runtime` client, which handles AWS
SigV4 signing and endpoint resolution via the standard SDK default credential chain --
nothing here reads, writes, or stores credentials itself. `ENDPOINT_URL` set (tests):
`_invoke_stub` sends a plain, unauthenticated HTTP POST via `requests` straight to that URL,
skipping boto3 and AWS auth entirely -- there is no local way to make boto3 itself complete a
round trip against a hand-rolled stub server without also reimplementing large parts of its
retry/connection-pool internals (confirmed empirically while building this: even
`Config(retries={"max_attempts": 1})` does not stop `urllib3`'s own connection-pool-level
retries from firing underneath boto3's service-level retry handler, which would make "log
every attempt, max 3 total" impossible to keep accurate). Both transports return the same
`(http_status, body_bytes, transport_error)` shape; everything above that -- success/
throttling/error/malformed classification, retry, backoff, and the provenance log -- is one
code path shared by both, so switching transports is the *only* thing `ENDPOINT_URL` changes.
"""

import json
import time
import urllib.parse
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

import requests

from bedrock import config as cfg

# HTTP status codes treated as transient / retryable, alongside genuine transport failures
# (connection refused, DNS failure, read timeout). 429 covers Bedrock's `ThrottlingException`
# and `ModelNotReadyException` (both 429 per the service's own error shapes); the 5xx codes
# cover `InternalServerException` (500) and `ServiceUnavailableException` (503) -- all
# transient, server-side, and worth retrying the same way a throttling response is. Everything
# else non-2xx (400 validation, 403 access-denied, 404 not-found, 424 model-error) is treated
# as a well-formed error response: fail immediately, per the task's explicit instruction.
_RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, 504})


class BedrockClientError(Exception):
    """Base class for every exception this client raises."""


class BedrockRequestError(BedrockClientError):
    """A well-formed error response came back (e.g. a validation error) -- not retried, per
    the task's explicit instruction to fail immediately on this shape of error."""

    def __init__(self, http_status: int, error_type: str | None, message: str):
        self.http_status = http_status
        self.error_type = error_type
        self.message = message
        super().__init__(f"Bedrock request error (HTTP {http_status}, {error_type}): {message}")


class BedrockMalformedResponseError(BedrockClientError):
    """A response came back with a 2xx status but a body that isn't valid JSON, or is valid
    JSON missing the fields this client expects. Not retried: a garbled response from a
    successful call is a parsing/contract problem, not a transient one."""


class BedrockRetriesExhaustedError(BedrockClientError):
    """Raised once `config.MAX_ATTEMPTS` attempts have all failed with a transport error or a
    retryable (throttling-shaped) response. `attempts` is every attempt's outcome, in order,
    for a caller that wants detail beyond the message; the same information is also in the
    provenance log."""

    def __init__(self, attempts: int, last_error: str):
        self.attempts = attempts
        self.last_error = last_error
        super().__init__(f"Bedrock call did not succeed after {attempts} attempt(s); last error: {last_error}")


@dataclass(frozen=True)
class LLMResponse:
    """The outcome of one successful `BedrockClient.send()` call."""

    text: str
    model_id: str
    region: str
    attempt: int  # which attempt (1-based) succeeded
    latency_s: float  # of the successful attempt only, not the whole retry sequence
    stop_reason: str | None
    usage: dict | None
    raw_response: dict = field(repr=False)  # the full parsed response body, for provenance


def _build_request_body(system: str, user_message: str, max_tokens: int, temperature: float) -> dict:
    """The Bedrock-Anthropic wire format for Claude models' `invoke_model` body -- stable,
    documented, unrelated to whether this call is going to the real service or the stub."""
    return {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "system": system,
        "messages": [{"role": "user", "content": user_message}],
    }


def _extract_text(parsed: dict) -> str:
    content = parsed["content"]
    return "".join(block["text"] for block in content if block.get("type") == "text")


def _parse_error_body(body_bytes: bytes) -> tuple[str | None, str]:
    """Best-effort (type, message) extraction from a non-2xx response body. Falls back to the
    raw text if the body isn't JSON -- a malformed *error* body still needs to produce a
    readable exception, not a second, confusing `JSONDecodeError`."""
    try:
        parsed = json.loads(body_bytes)
    except json.JSONDecodeError:
        return None, body_bytes.decode("utf-8", errors="replace")
    error_type = parsed.get("__type") or parsed.get("code")
    message = parsed.get("message") or parsed.get("Message") or str(parsed)
    return error_type, message


class BedrockClient:
    def __init__(
        self,
        region: str | None = None,
        endpoint_url: str | None = None,
        log_path: Path | None = None,
        max_attempts: int | None = None,
        retry_base_delay_s: float | None = None,
        connect_timeout_s: float | None = None,
        read_timeout_s: float | None = None,
        sleep_fn=time.sleep,
    ):
        """All parameters default to `bedrock.config`'s module-level values, same pattern as
        `harness.repl.get_warm_environment`'s optional overrides. `sleep_fn` is overridable so
        tests exercising the retry path don't have to wait out real backoff delays."""
        self.region = region if region is not None else cfg.REGION
        self.endpoint_url = endpoint_url if endpoint_url is not None else cfg.ENDPOINT_URL
        self.log_path = log_path if log_path is not None else cfg.CALL_LOG_PATH
        self.max_attempts = max_attempts if max_attempts is not None else cfg.MAX_ATTEMPTS
        self.retry_base_delay_s = retry_base_delay_s if retry_base_delay_s is not None else cfg.RETRY_BASE_DELAY_S
        self.connect_timeout_s = connect_timeout_s if connect_timeout_s is not None else cfg.CONNECT_TIMEOUT_S
        self.read_timeout_s = read_timeout_s if read_timeout_s is not None else cfg.READ_TIMEOUT_S
        self._sleep = sleep_fn

        self._boto_client = None
        if self.endpoint_url is None:
            import boto3  # imported lazily: never needed on the stub path, so a stub-only

            # test run never has to satisfy boto3's own import-time requirements.
            self._boto_client = boto3.client("bedrock-runtime", region_name=self.region)

    def send(
        self,
        system: str,
        user_message: str,
        *,
        model_id: str,
        max_tokens: int = 1024,
        temperature: float = 1.0,
    ) -> LLMResponse:
        """Send one prompt (system + user message) and return the response text plus
        metadata. `model_id` is required and not defaulted here -- callers pass
        `bedrock.config.AUTHORING_MODEL_ID` or `.FLAGSHIP_MODEL_ID` explicitly, so the pinned
        model actually used is visible at the call site as well as in the provenance log (the
        reproducibility rule this client exists to support -- see this module's own
        docstring)."""
        request_body = _build_request_body(system, user_message, max_tokens, temperature)
        last_error_summary = ""

        for attempt in range(1, self.max_attempts + 1):
            start = time.perf_counter()
            http_status, body_bytes, transport_error = self._invoke(model_id, request_body)
            latency_s = time.perf_counter() - start

            if transport_error is not None:
                last_error_summary = f"transport error: {transport_error}"
                self._log_attempt(
                    attempt=attempt,
                    model_id=model_id,
                    request=request_body,
                    latency_s=latency_s,
                    http_status=None,
                    outcome="transport_error",
                    response=None,
                    error={"type": type(transport_error).__name__, "message": str(transport_error)},
                )
                if attempt < self.max_attempts:
                    self._sleep(self.retry_base_delay_s * (2 ** (attempt - 1)))
                    continue
                raise BedrockRetriesExhaustedError(attempts=attempt, last_error=last_error_summary)

            if http_status == 200:
                try:
                    parsed = json.loads(body_bytes)
                    text = _extract_text(parsed)
                except (json.JSONDecodeError, KeyError, TypeError) as e:
                    self._log_attempt(
                        attempt=attempt,
                        model_id=model_id,
                        request=request_body,
                        latency_s=latency_s,
                        http_status=http_status,
                        outcome="malformed_response",
                        response=None,
                        error={
                            "type": type(e).__name__,
                            "message": str(e),
                            "raw_body": body_bytes.decode("utf-8", errors="replace"),
                        },
                    )
                    raise BedrockMalformedResponseError(
                        f"Bedrock response body was not a well-formed completion: {type(e).__name__}: {e}"
                    ) from e

                self._log_attempt(
                    attempt=attempt,
                    model_id=model_id,
                    request=request_body,
                    latency_s=latency_s,
                    http_status=http_status,
                    outcome="success",
                    response=parsed,
                    error=None,
                )
                return LLMResponse(
                    text=text,
                    model_id=model_id,
                    region=self.region,
                    attempt=attempt,
                    latency_s=latency_s,
                    stop_reason=parsed.get("stop_reason"),
                    usage=parsed.get("usage"),
                    raw_response=parsed,
                )

            # Non-transport, non-200: classify by status code.
            error_type, message = _parse_error_body(body_bytes)
            last_error_summary = f"HTTP {http_status} {error_type}: {message}"
            if http_status in _RETRYABLE_STATUS_CODES:
                self._log_attempt(
                    attempt=attempt,
                    model_id=model_id,
                    request=request_body,
                    latency_s=latency_s,
                    http_status=http_status,
                    outcome="throttled",
                    response=None,
                    error={"type": error_type, "message": message},
                )
                if attempt < self.max_attempts:
                    self._sleep(self.retry_base_delay_s * (2 ** (attempt - 1)))
                    continue
                raise BedrockRetriesExhaustedError(attempts=attempt, last_error=last_error_summary)

            self._log_attempt(
                attempt=attempt,
                model_id=model_id,
                request=request_body,
                latency_s=latency_s,
                http_status=http_status,
                outcome="error",
                response=None,
                error={"type": error_type, "message": message},
            )
            raise BedrockRequestError(http_status=http_status, error_type=error_type, message=message)

        raise BedrockRetriesExhaustedError(  # pragma: no cover -- loop always returns or raises above
            attempts=self.max_attempts, last_error=last_error_summary
        )

    def _invoke(self, model_id: str, request_body: dict) -> tuple[int | None, bytes | None, Exception | None]:
        """Returns `(http_status, body_bytes, transport_error)` -- exactly one of
        `transport_error` or `(http_status, body_bytes)` is meaningful per call. Never raises:
        every failure mode is reported back through this triple so `send`'s retry/logging
        logic has one shape to classify, regardless of which transport handled the call."""
        if self._boto_client is not None:
            return self._invoke_real(model_id, request_body)
        return self._invoke_stub(model_id, request_body)

    def _invoke_real(self, model_id: str, request_body: dict) -> tuple[int | None, bytes | None, Exception | None]:
        from botocore.exceptions import ClientError

        try:
            response = self._boto_client.invoke_model(
                modelId=model_id,
                body=json.dumps(request_body),
                contentType="application/json",
                accept="application/json",
            )
        except ClientError as e:
            http_status = e.response.get("ResponseMetadata", {}).get("HTTPStatusCode", 500)
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            error_message = e.response.get("Error", {}).get("Message", str(e))
            body = json.dumps({"__type": error_code, "message": error_message}).encode()
            return http_status, body, None
        except Exception as e:  # noqa: BLE001 -- deliberately broad: any transport-level failure
            # (EndpointConnectionError, ConnectionClosedError, ReadTimeoutError, ...) is
            # reported back uniformly as a transport error, not re-raised here.
            return None, None, e

        return 200, response["body"].read(), None

    def _invoke_stub(self, model_id: str, request_body: dict) -> tuple[int | None, bytes | None, Exception | None]:
        url = urllib.parse.urljoin(self.endpoint_url.rstrip("/") + "/", f"model/{model_id}/invoke")
        try:
            response = requests.post(
                url,
                json=request_body,
                timeout=(self.connect_timeout_s, self.read_timeout_s),
            )
        except requests.exceptions.RequestException as e:
            return None, None, e
        return response.status_code, response.content, None

    def _log_attempt(
        self,
        *,
        attempt: int,
        model_id: str,
        request: dict,
        latency_s: float,
        http_status: int | None,
        outcome: str,
        response: dict | None,
        error: dict | None,
    ) -> None:
        """Append one structured provenance record. Load-bearing downstream (task
        instructions): every LLM-populated value in a stage-2 task must be traceable to a
        logged call, so every attempt is logged here, not just the one that ultimately
        succeeds or the one that ultimately raises."""
        record = {
            "timestamp": datetime.now(UTC).isoformat(),
            "model_id": model_id,
            "region": self.region,
            "attempt": attempt,
            "max_attempts": self.max_attempts,
            "http_status": http_status,
            "outcome": outcome,
            "latency_s": latency_s,
            "request": request,
            "response": response,
            "error": error,
        }
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
