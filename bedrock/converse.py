"""Provider-agnostic Bedrock client, via the Converse API.

`bedrock.client.BedrockClient` speaks the Bedrock-**Anthropic** `invoke_model` wire format:
`anthropic_version`, a top-level `system` string, `thinking`, and a response parsed as
`content: [{type: "text", ...}]`. None of that is portable -- DeepSeek and Qwen accept an
OpenAI-shaped body and answer in an OpenAI-shaped envelope, so pointing the existing client at
them fails at `_build_request_body` and again at `_extract_text`.

Rather than grow a second wire format per vendor, this uses **Converse**, which is Bedrock's own
normalisation layer: one request shape, one response shape, every text model that supports it.
Both models this was written for support it (checked against their model cards, 11 Aug 2026):

    deepseek.v3.2                   164K context,  8K max output
    qwen.qwen3-coder-480b-a35b-v1:0 262K context, 66K max output

**Region is a per-call concern here, not a global.** Neither model is offered in `eu-west-1`,
the region `bedrock.config.REGION` pins for Claude. Both are offered in `eu-west-2` (London) and
`eu-north-1` (Stockholm), so a run mixing Claude with either of these is necessarily a
multi-region run and the region has to travel with the model id.

Kept deliberately small: retry-with-backoff on throttling and transient 5xx, and nothing else.
The provenance log, pricing table, and stub transport of `bedrock.client` are not duplicated --
if this grows past a few hundred lines it should be merged into that module instead.
"""

import random
import time
from dataclasses import dataclass

# Model ids, pinned here for the same reproducibility reason `bedrock.config` pins Claude's:
# a run's model must be recoverable from the repo, not from shell history.
DEEPSEEK_V32 = "deepseek.v3.2"
DEEPSEEK_V31 = "deepseek.v3.1"  # documented fallback if V3.2 is unavailable in the account
QWEN3_CODER_480B = "qwen.qwen3-coder-480b-a35b-v1:0"

# Neither model is available in eu-west-1. Both are in eu-west-2 (London) and eu-north-1.
DEFAULT_REGION = "eu-west-2"

# Per-model output ceilings, from the model cards. DeepSeek's 8K is a HARD cap -- asking for more
# is an API error, not a silent clamp, and the batch-5 truncation post-mortem is the reason this
# is recorded rather than left to a caller's guess.
MAX_OUTPUT_TOKENS = {
    DEEPSEEK_V32: 8192,
    DEEPSEEK_V31: 8192,
    QWEN3_CODER_480B: 32768,
}

_THROTTLE_CODES = {"ThrottlingException", "TooManyRequestsException",
                   "ServiceUnavailableException", "ModelNotReadyException",
                   "InternalServerException"}


@dataclass
class ConverseResult:
    text: str
    input_tokens: int | None
    output_tokens: int | None
    stop_reason: str | None
    model_id: str
    region: str


class ConverseError(RuntimeError):
    pass


class ConverseClient:
    """One boto3 `bedrock-runtime` client per (region), calling `converse`."""

    def __init__(self, region: str = DEFAULT_REGION, *, max_attempts: int = 4,
                 read_timeout_s: float = 900.0, sleep=time.sleep):
        self.region = region
        self.max_attempts = max_attempts
        self._sleep = sleep
        import boto3
        from botocore.config import Config

        self._client = boto3.client(
            "bedrock-runtime", region_name=region,
            config=Config(read_timeout=read_timeout_s, connect_timeout=30,
                          retries={"max_attempts": 0}),  # retry policy lives here, not in botocore
        )

    def send(self, system: str, user_message: str, *, model_id: str,
             max_tokens: int, temperature: float = 1.0) -> ConverseResult:
        cap = MAX_OUTPUT_TOKENS.get(model_id)
        if cap is not None and max_tokens > cap:
            max_tokens = cap  # clamp rather than let the API reject the whole call

        kwargs = {
            "modelId": model_id,
            "messages": [{"role": "user", "content": [{"text": user_message}]}],
            "inferenceConfig": {"maxTokens": max_tokens, "temperature": temperature},
        }
        if system:
            kwargs["system"] = [{"text": system}]

        last = ""
        for attempt in range(1, self.max_attempts + 1):
            try:
                response = self._client.converse(**kwargs)
            except Exception as e:  # noqa: BLE001 -- classified below, never swallowed
                name = type(e).__name__
                code = getattr(e, "response", {}).get("Error", {}).get("Code", name)
                last = f"{code}: {str(e)[:200]}"
                if code in _THROTTLE_CODES and attempt < self.max_attempts:
                    # Jittered backoff: a fleet of workers hitting one quota must not retry in
                    # lockstep, which is what turned the Sonnet arm's quota wall into a stampede.
                    self._sleep(min(60.0, 2.0 ** attempt) * (0.5 + random.random()))
                    continue
                raise ConverseError(f"converse failed ({model_id} @ {self.region}): {last}") from e

            message = (response.get("output") or {}).get("message") or {}
            text = "".join(b.get("text", "") for b in (message.get("content") or []))
            usage = response.get("usage") or {}
            return ConverseResult(
                text=text,
                input_tokens=usage.get("inputTokens"),
                output_tokens=usage.get("outputTokens"),
                stop_reason=response.get("stopReason"),
                model_id=model_id,
                region=self.region,
            )
        raise ConverseError(f"converse exhausted {self.max_attempts} attempts: {last}")


class ConverseAuthoringClient:
    """`BedrockClient`-shaped adapter over Converse, so the authoring pipeline can run on
    DeepSeek/Qwen without knowing anything about wire formats.

    Written when Sonnet hit its daily token quota mid-batch for the fourth time in this project.
    The pipeline only ever reads `.text`, `.stop_reason` and `.usage` off a response
    (`authoring.orchestrate`), so matching `LLMResponse` on those three is sufficient.

    **One real caveat, not a detail.** DeepSeek V3.2 caps output at 8,192 tokens, while the
    fact-proposal call is configured for 16,384 -- `ConverseClient.send` clamps rather than
    erroring, so a large fact suite can come back truncated. `stop_reason == "max_tokens"` is
    exactly what `_parse_llm_json_response` treats as a truncation failure, so this degrades
    into an honest per-task rotation rather than silent corruption; but on tasks with big suites
    it will rotate more often than Sonnet would.
    """

    def __init__(self, region: str = DEFAULT_REGION, *, model_id: str = DEEPSEEK_V32,
                 log_path=None, read_timeout_s: float = 900.0):
        self._client = ConverseClient(region=region, read_timeout_s=read_timeout_s)
        self._default_model = model_id
        self.log_path = log_path
        self.region = region

    def send(self, system: str, user_message: str, *, model_id: str | None = None,
             max_tokens: int = 1024, temperature: float = 1.0, thinking=None):
        import json as _json
        import time as _time
        from dataclasses import dataclass as _dc

        # `thinking` is Anthropic-only and is accepted-and-ignored rather than rejected, so the
        # pipeline needs no per-provider branching.
        t0 = _time.perf_counter()
        res = self._client.send(system, user_message,
                                model_id=self._default_model,
                                max_tokens=max_tokens, temperature=temperature)
        latency = _time.perf_counter() - t0

        @_dc(frozen=True)
        class _Resp:
            text: str
            model_id: str
            region: str
            attempt: int
            latency_s: float
            stop_reason: str | None
            usage: dict | None
            raw_response: dict

        usage = {"input_tokens": res.input_tokens, "output_tokens": res.output_tokens}
        if self.log_path is not None:
            # Same shape the cost accounting in scripts/run_batch200.py reads.
            rec = {"timestamp": _time.strftime("%Y-%m-%dT%H:%M:%S"), "model_id": res.model_id,
                   "outcome": "success", "latency_s": round(latency, 2),
                   "request": {"max_tokens": max_tokens},
                   "response": {"usage": usage, "stop_reason": res.stop_reason}}
            with open(self.log_path, "a", encoding="utf-8") as fh:
                fh.write(_json.dumps(rec) + "\n")
        return _Resp(text=res.text, model_id=res.model_id, region=res.region, attempt=1,
                     latency_s=latency, stop_reason=res.stop_reason, usage=usage,
                     raw_response={})
