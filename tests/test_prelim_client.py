"""Tests for `prelim.client` against `prelim.stubserver` -- no real endpoint, no GPU.

The stub is a real loopback HTTP server rather than a mocked `requests.post`: the behaviour under
test is almost entirely about what happens on timeouts, dropped connections and error statuses,
and a mock that returns whatever it was told to return cannot demonstrate that the client
survives a genuinely misbehaving socket. Same reasoning `tests/fixtures/bedrock_stub.py` records
for the bedrock client.

Backoff sleeping is injected (`sleep_fn`) so the retry tests finish in milliseconds.
"""

import json

import pytest

from prelim import config as cfg
from prelim.client import (
    EndpointMalformedResponseError,
    EndpointRequestError,
    EndpointUnavailable,
    PrelimClientError,
    generate,
)
from prelim.stubserver import (
    DROP_CONNECTION,
    ScriptedResponse,
    StubEndpointServer,
    chat_completion_body,
    error_body,
)

MESSAGES = [{"role": "user", "content": "State the definition."}]


@pytest.fixture
def stub():
    servers = []

    def _make(script=None):
        s = StubEndpointServer(script)
        servers.append(s)
        return s

    yield _make
    for s in servers:
        s.stop()


@pytest.fixture
def no_sleep():
    """Collects the backoff delays instead of sleeping them, so tests can assert the schedule."""
    slept = []
    yield slept, slept.append


def _generate(server, tmp_path, **kw):
    kw.setdefault("temperature", 0.7)
    kw.setdefault("max_tokens", 256)
    kw.setdefault("model_name", "stub/model")
    kw.setdefault("log_path", tmp_path / "call_log.jsonl")
    return generate(MESSAGES, endpoint_url=server.url, **kw)


def _log_lines(tmp_path):
    path = tmp_path / "call_log.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


# --- success path -------------------------------------------------------------------------------


def test_success_returns_text_finish_reason_and_token_counts(stub, tmp_path):
    server = stub([ScriptedResponse(200, chat_completion_body("the answer", prompt_tokens=31, completion_tokens=9))])
    result = _generate(server, tmp_path)

    assert result.text == "the answer"
    assert result.finish_reason == "stop"
    assert result.prompt_tokens == 31
    assert result.completion_tokens == 9
    assert result.attempts == 1
    assert result.wall_time_s > 0
    assert result.raw_response["object"] == "chat.completion"  # raw kept for provenance


def test_request_body_carries_the_sampling_params_and_messages(stub, tmp_path):
    server = stub()
    _generate(server, tmp_path, temperature=0.95, max_tokens=4096, model_name="Goedel-LM/Goedel-Prover-V2-8B")

    sent = server.requests_received[0]
    assert sent["messages"] == MESSAGES
    assert sent["temperature"] == 0.95
    assert sent["max_tokens"] == 4096
    assert sent["model"] == "Goedel-LM/Goedel-Prover-V2-8B"


def test_missing_usage_object_reports_none_token_counts_not_zero(stub, tmp_path):
    """Absence recorded honestly: a server that reports no usage must not be indistinguishable
    from one reporting a genuine zero."""
    body = chat_completion_body("x")
    del body["usage"]
    server = stub([ScriptedResponse(200, body)])
    result = _generate(server, tmp_path)

    assert result.prompt_tokens is None
    assert result.completion_tokens is None


def test_null_content_is_read_as_empty_text(stub, tmp_path):
    """Some servers return null content with a `length` finish_reason when a generation is cut
    off before emitting anything -- readable, not a malformed body."""
    body = chat_completion_body("ignored", finish_reason="length")
    body["choices"][0]["message"]["content"] = None
    server = stub([ScriptedResponse(200, body)])
    result = _generate(server, tmp_path)

    assert result.text == ""
    assert result.finish_reason == "length"


# --- auth -----------------------------------------------------------------------------------


def test_keyless_operation_sends_no_authorization_header(stub, tmp_path, monkeypatch):
    monkeypatch.delenv(cfg.ENV_API_KEY, raising=False)
    server = stub()
    _generate(server, tmp_path)

    assert "Authorization" not in server.headers_received[0]


def test_api_key_when_present_is_sent_as_bearer(stub, tmp_path):
    server = stub()
    _generate(server, tmp_path, api_key="sk-test-123")

    assert server.headers_received[0]["Authorization"] == "Bearer sk-test-123"


def test_api_key_is_never_written_to_the_call_log(stub, tmp_path):
    server = stub()
    _generate(server, tmp_path, api_key="sk-secret-do-not-log")

    assert "sk-secret-do-not-log" not in (tmp_path / "call_log.jsonl").read_text(encoding="utf-8")


# --- retry ----------------------------------------------------------------------------------


def test_retries_then_succeeds_on_5xx(stub, tmp_path, no_sleep):
    slept, sleep_fn = no_sleep
    server = stub([
        ScriptedResponse(500, error_body("internal", err_type="InternalError", code=500)),
        ScriptedResponse(503, error_body("loading model", err_type="ServiceUnavailable", code=503)),
        ScriptedResponse(200, chat_completion_body("recovered")),
    ])
    result = _generate(server, tmp_path, sleep_fn=sleep_fn)

    assert result.text == "recovered"
    assert result.attempts == 3
    assert server.call_count == 3
    assert slept == [1.0, 2.0]  # exponential backoff


def test_retries_then_succeeds_on_429(stub, tmp_path, no_sleep):
    slept, sleep_fn = no_sleep
    server = stub([
        ScriptedResponse(429, error_body("rate limited", err_type="RateLimit", code=429)),
        ScriptedResponse(200, chat_completion_body("ok now")),
    ])
    result = _generate(server, tmp_path, sleep_fn=sleep_fn)

    assert result.text == "ok now"
    assert result.attempts == 2


def test_retries_then_succeeds_on_timeout(stub, tmp_path, no_sleep):
    """First reply is delayed past the (deliberately tiny) client timeout; second is prompt."""
    slept, sleep_fn = no_sleep
    server = stub([
        ScriptedResponse(200, chat_completion_body("too late"), delay_s=0.6),
        ScriptedResponse(200, chat_completion_body("in time")),
    ])
    result = _generate(server, tmp_path, timeout_s=0.2, sleep_fn=sleep_fn)

    assert result.text == "in time"
    assert result.attempts == 2


def test_retries_then_succeeds_on_dropped_connection(stub, tmp_path, no_sleep):
    slept, sleep_fn = no_sleep
    server = stub([
        ScriptedResponse(200, DROP_CONNECTION),
        ScriptedResponse(200, chat_completion_body("second time lucky")),
    ])
    result = _generate(server, tmp_path, sleep_fn=sleep_fn)

    assert result.text == "second time lucky"
    assert result.attempts == 2


# --- hard failures ----------------------------------------------------------------------------


def test_400_fails_immediately_without_retrying(stub, tmp_path, no_sleep):
    """A 400 means OUR request is malformed -- looping on it would burn the whole night making
    the same mistake."""
    slept, sleep_fn = no_sleep
    server = stub([ScriptedResponse(400, error_body("unknown model 'nope'"))])

    with pytest.raises(EndpointRequestError) as exc:
        _generate(server, tmp_path, sleep_fn=sleep_fn)

    assert exc.value.http_status == 400
    assert "unknown model" in exc.value.message
    assert server.call_count == 1  # no retry
    assert slept == []


@pytest.mark.parametrize("status", [401, 403, 404, 422])
def test_other_4xx_also_fail_immediately(stub, tmp_path, status):
    server = stub([ScriptedResponse(status, error_body("nope", code=status))])
    with pytest.raises(EndpointRequestError):
        _generate(server, tmp_path, sleep_fn=lambda s: None)
    assert server.call_count == 1


def test_endpoint_unavailable_after_retries_exhausted(stub, tmp_path, no_sleep):
    slept, sleep_fn = no_sleep
    server = stub([ScriptedResponse(500, error_body("still broken", code=500))])

    with pytest.raises(EndpointUnavailable) as exc:
        _generate(server, tmp_path, sleep_fn=sleep_fn)

    assert exc.value.attempts == cfg.MAX_ATTEMPTS
    assert "500" in exc.value.last_error
    assert server.call_count == cfg.MAX_ATTEMPTS


def test_endpoint_unavailable_on_permanent_connection_failure(tmp_path, no_sleep):
    """A dead pod: nothing listening at all. Must raise, never return empty text."""
    slept, sleep_fn = no_sleep
    dead = StubEndpointServer()
    url = dead.url
    dead.stop()  # port now closed -> connection refused

    with pytest.raises(EndpointUnavailable):
        generate(
            MESSAGES, temperature=0.7, max_tokens=64, model_name="m", endpoint_url=url,
            log_path=tmp_path / "call_log.jsonl", sleep_fn=sleep_fn,
        )


def test_malformed_2xx_body_raises_and_is_not_retried(stub, tmp_path):
    server = stub([ScriptedResponse(200, b"this is not json at all")])
    with pytest.raises(EndpointMalformedResponseError):
        _generate(server, tmp_path, sleep_fn=lambda s: None)
    assert server.call_count == 1


def test_missing_endpoint_configuration_raises_before_any_request(tmp_path, monkeypatch):
    monkeypatch.delenv(cfg.ENV_ENDPOINT_URL, raising=False)
    with pytest.raises(PrelimClientError, match=cfg.ENV_ENDPOINT_URL):
        generate(MESSAGES, temperature=0.7, max_tokens=64, model_name="m", log_path=tmp_path / "l.jsonl")


def test_endpoint_url_read_from_environment_when_not_passed(stub, tmp_path, monkeypatch):
    server = stub()
    monkeypatch.setenv(cfg.ENV_ENDPOINT_URL, server.url)
    result = generate(
        MESSAGES, temperature=0.1, max_tokens=8, model_name="m", log_path=tmp_path / "call_log.jsonl"
    )
    assert result.text == "stub completion"


# --- call log ---------------------------------------------------------------------------------


def test_call_log_line_written_on_success(stub, tmp_path):
    server = stub([ScriptedResponse(200, chat_completion_body("logged"))])
    _generate(server, tmp_path, model_name="some/model")

    lines = _log_lines(tmp_path)
    assert len(lines) == 1
    rec = lines[0]
    assert rec["outcome"] == "success"
    assert rec["http_status"] == 200
    assert rec["attempt"] == 1
    assert rec["model_name"] == "some/model"
    assert rec["request"]["messages"] == MESSAGES
    assert rec["response"]["choices"][0]["message"]["content"] == "logged"
    assert rec["timestamp"] and rec["latency_s"] >= 0


def test_call_log_records_every_attempt_including_the_final_failure(stub, tmp_path, no_sleep):
    slept, sleep_fn = no_sleep
    server = stub([ScriptedResponse(500, error_body("boom", code=500))])

    with pytest.raises(EndpointUnavailable):
        _generate(server, tmp_path, sleep_fn=sleep_fn)

    lines = _log_lines(tmp_path)
    assert len(lines) == cfg.MAX_ATTEMPTS  # every attempt logged, not just the last
    assert [r["attempt"] for r in lines] == [1, 2, 3]
    assert all(r["outcome"] == "retryable_error" for r in lines)


def test_call_log_records_a_non_retryable_failure(stub, tmp_path):
    server = stub([ScriptedResponse(400, error_body("bad params"))])
    with pytest.raises(EndpointRequestError):
        _generate(server, tmp_path, sleep_fn=lambda s: None)

    lines = _log_lines(tmp_path)
    assert len(lines) == 1
    assert lines[0]["outcome"] == "request_error"
    assert lines[0]["http_status"] == 400


# --- /v1/completions support (Stage 2, Item 3) ---------------------------------------------------
#
# No model in the current table selects this path -- the 2026-08-03 card sweep found all six use
# chat templates, including DeepSeek-Prover-V2, correcting Stage 1's assumption. It exists so a
# model that turns out to need raw completions can be switched with a table edit, not a code
# change, mid-run.


def completion_body(text, *, finish_reason="stop", prompt_tokens=11, completion_tokens=4):
    """The legacy OpenAI `/v1/completions` shape: text at choices[0].text, no message object."""
    return {
        "id": "cmpl-stub",
        "object": "text_completion",
        "created": 1754200000,
        "model": "stub-model",
        "choices": [{"index": 0, "text": text, "finish_reason": finish_reason, "logprobs": None}],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
        },
    }


def test_completion_style_sends_a_prompt_string_not_messages(stub, tmp_path):
    server = stub([ScriptedResponse(200, completion_body("def f := 0"))])
    result = generate(
        "raw prompt text", temperature=0.5, max_tokens=32, model_name="m",
        endpoint_style="completion", endpoint_url=server.url, log_path=tmp_path / "call_log.jsonl",
    )

    sent = server.requests_received[0]
    assert sent["prompt"] == "raw prompt text"
    assert "messages" not in sent
    assert result.text == "def f := 0"
    assert result.finish_reason == "stop"
    assert result.prompt_tokens == 11


def test_completion_style_shares_the_retry_path(stub, tmp_path, no_sleep):
    """One retry/logging path for both shapes -- the style flag selects only the wire format."""
    slept, sleep_fn = no_sleep
    server = stub([
        ScriptedResponse(503, error_body("loading", code=503)),
        ScriptedResponse(200, completion_body("recovered")),
    ])
    result = generate(
        "p", temperature=0.5, max_tokens=32, model_name="m", endpoint_style="completion",
        endpoint_url=server.url, log_path=tmp_path / "call_log.jsonl", sleep_fn=sleep_fn,
    )
    assert result.text == "recovered"
    assert result.attempts == 2


def test_chat_style_still_sends_messages(stub, tmp_path):
    server = stub()
    _generate(server, tmp_path)
    assert "messages" in server.requests_received[0]
    assert "prompt" not in server.requests_received[0]


def test_mismatched_prompt_type_is_rejected_before_any_request(stub, tmp_path):
    server = stub()
    with pytest.raises(PrelimClientError, match="requires a messages list"):
        generate("a string", temperature=0.5, max_tokens=8, model_name="m",
                 endpoint_style="chat", endpoint_url=server.url, log_path=tmp_path / "l.jsonl")
    with pytest.raises(PrelimClientError, match="requires a prompt string"):
        generate([{"role": "user", "content": "x"}], temperature=0.5, max_tokens=8, model_name="m",
                 endpoint_style="completion", endpoint_url=server.url, log_path=tmp_path / "l.jsonl")
    assert server.call_count == 0


def test_unknown_endpoint_style_is_rejected(tmp_path):
    with pytest.raises(PrelimClientError, match="endpoint_style"):
        generate([], temperature=0.5, max_tokens=8, model_name="m", endpoint_style="grpc",
                 endpoint_url="http://x", log_path=tmp_path / "l.jsonl")


# --- streaming (added 2026-08-03, live-forced) ----------------------------------------------------
#
# Streaming is not a nicety here: RunPod's proxy returns HTTP 524 on any non-streaming request
# that takes too long to produce its first byte, which at 8192 max_tokens (~246s on the run's
# A40) is every long generation. These tests pin the accumulation so the sample format and
# provenance stay byte-compatible with the non-streaming path.

from prelim.stubserver import sse_stream


def test_streaming_accumulates_deltas_into_one_completion(stub, tmp_path):
    server = stub([ScriptedResponse(200, sse_stream("def VTask.clog := 0", prompt_tokens=41, completion_tokens=9))])
    result = generate(MESSAGES, temperature=0.7, max_tokens=64, model_name="m", stream=True,
                      endpoint_url=server.url, log_path=tmp_path / "call_log.jsonl")

    assert result.text == "def VTask.clog := 0"   # reassembled from 8-char chunks
    assert result.finish_reason == "stop"
    assert result.prompt_tokens == 41
    assert result.completion_tokens == 9


def test_streaming_request_sets_stream_and_usage_options(stub, tmp_path):
    server = stub([ScriptedResponse(200, sse_stream("x"))])
    generate(MESSAGES, temperature=0.7, max_tokens=64, model_name="m", stream=True,
             endpoint_url=server.url, log_path=tmp_path / "call_log.jsonl")

    sent = server.requests_received[0]
    assert sent["stream"] is True
    assert sent["stream_options"] == {"include_usage": True}


def test_streaming_and_non_streaming_produce_the_same_result_shape(stub, tmp_path):
    """The whole point: nothing downstream may be able to tell which path ran."""
    a = stub([ScriptedResponse(200, sse_stream("def f := 1", prompt_tokens=7, completion_tokens=3))])
    b = stub([ScriptedResponse(200, chat_completion_body("def f := 1", prompt_tokens=7, completion_tokens=3))])
    r1 = generate(MESSAGES, temperature=0.7, max_tokens=64, model_name="m", stream=True,
                  endpoint_url=a.url, log_path=tmp_path / "l1.jsonl")
    r2 = generate(MESSAGES, temperature=0.7, max_tokens=64, model_name="m", stream=False,
                  endpoint_url=b.url, log_path=tmp_path / "l2.jsonl")

    assert (r1.text, r1.finish_reason, r1.prompt_tokens, r1.completion_tokens) == \
           (r2.text, r2.finish_reason, r2.prompt_tokens, r2.completion_tokens)
    # raw_response stays completion-shaped so stored provenance is comparable across paths
    assert r1.raw_response["choices"][0]["message"]["content"] == "def f := 1"


def test_streaming_length_finish_reason_survives(stub, tmp_path):
    server = stub([ScriptedResponse(200, sse_stream("truncated", finish_reason="length"))])
    r = generate(MESSAGES, temperature=0.7, max_tokens=8, model_name="m", stream=True,
                 endpoint_url=server.url, log_path=tmp_path / "call_log.jsonl")
    assert r.finish_reason == "length"


def test_streaming_skips_a_malformed_chunk_rather_than_failing(stub, tmp_path):
    """Losing one delta degrades a sample; raising would discard an otherwise complete one."""
    good = sse_stream("abcdefgh", chunk_size=4).decode()
    broken = good.replace('data: {"id": "chatcmpl-stub", "object": "chat.completion.chunk"', 'data: {NOT JSON', 1)
    server = stub([ScriptedResponse(200, broken.encode())])
    r = generate(MESSAGES, temperature=0.7, max_tokens=64, model_name="m", stream=True,
                 endpoint_url=server.url, log_path=tmp_path / "call_log.jsonl")
    assert "efgh" in r.text  # the surviving chunk still arrived


def test_streaming_errors_still_raise_normally(stub, tmp_path):
    server = stub([ScriptedResponse(400, error_body("bad params"))])
    with pytest.raises(EndpointRequestError):
        generate(MESSAGES, temperature=0.7, max_tokens=64, model_name="m", stream=True,
                 endpoint_url=server.url, log_path=tmp_path / "l.jsonl", sleep_fn=lambda s: None)
