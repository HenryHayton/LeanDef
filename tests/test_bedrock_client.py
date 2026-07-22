"""Unit tests for bedrock.client, using a scripted local HTTP server -- no real AWS call
anywhere in this file. This is the network-level analogue of
tests/test_miner_verify_recovery.py's in-process `_FakeServer`: same "scripted responses,
popped in order, AssertionError if exhausted" philosophy, but a genuine `http.server` is
required here because `bedrock.config.ENDPOINT_URL` override semantics are themselves about
where an HTTP request actually goes -- there's no boto3 call to substitute a plain Python
object for (see bedrock.client's module docstring for why boto3 itself can't be the stub
transport).
"""

import json
import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from bedrock.client import (
    BedrockClient,
    BedrockMalformedResponseError,
    BedrockRequestError,
    BedrockRetriesExhaustedError,
)


class _ScriptedResponse:
    def __init__(self, status: int, body):
        self.status = status
        # `body`: a dict (JSON-encoded automatically) or raw bytes (sent as-is, e.g. garbage).
        self.body = body


class _StubBedrockServer:
    """A real (loopback-only) HTTP server returning one scripted response per POST, in order.
    Records every request body received so tests can assert on what was sent."""

    def __init__(self, script: list[_ScriptedResponse]):
        self.script = list(script)
        self.requests_received: list[dict] = []
        server = self

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length)
                server.requests_received.append(json.loads(raw))

                if not server.script:
                    raise AssertionError(f"stub server ran out of scripted responses at path: {self.path!r}")
                scripted = server.script.pop(0)
                body_bytes = scripted.body if isinstance(scripted.body, bytes) else json.dumps(scripted.body).encode()

                self.send_response(scripted.status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body_bytes)))
                self.end_headers()
                self.wfile.write(body_bytes)

            def log_message(self, format, *args):  # noqa: A002 -- matches BaseHTTPRequestHandler's signature
                pass  # silence default access-log lines to stderr during test runs

        self._httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)
        self._thread.start()

    @property
    def url(self) -> str:
        host, port = self._httpd.server_address
        return f"http://{host}:{port}"

    def stop(self):
        self._httpd.shutdown()
        self._httpd.server_close()
        self._thread.join(timeout=2)


@pytest.fixture
def stub_server():
    server = None

    def _make(script):
        nonlocal server
        server = _StubBedrockServer(script)
        return server

    yield _make
    if server is not None:
        server.stop()


def _success_body(text: str = "hello from the stub") -> dict:
    return {
        "id": "msg_stub",
        "type": "message",
        "role": "assistant",
        "content": [{"type": "text", "text": text}],
        "model": "stub-model",
        "stop_reason": "end_turn",
        "stop_sequence": None,
        "usage": {"input_tokens": 12, "output_tokens": 5},
    }


def _closed_port_url() -> str:
    """A loopback URL nothing is listening on -- binds a socket to a free port then closes it
    immediately, so connection attempts fail deterministically and immediately rather than
    timing out."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    _host, port = sock.getsockname()
    sock.close()
    return f"http://127.0.0.1:{port}"


def _read_log(log_path) -> list[dict]:
    with log_path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def test_successful_round_trip_returns_text_and_logs_one_record(stub_server, tmp_path):
    server = stub_server([_ScriptedResponse(200, _success_body("the answer is 42"))])
    log_path = tmp_path / "log.jsonl"
    client = BedrockClient(endpoint_url=server.url, log_path=log_path, sleep_fn=lambda s: None)

    response = client.send(system="be terse", user_message="what is the answer?", model_id="test-model-id")

    assert response.text == "the answer is 42"
    assert response.model_id == "test-model-id"
    assert response.attempt == 1
    assert response.stop_reason == "end_turn"
    assert response.usage == {"input_tokens": 12, "output_tokens": 5}

    records = _read_log(log_path)
    assert len(records) == 1
    record = records[0]
    assert record["outcome"] == "success"
    assert record["model_id"] == "test-model-id"
    assert record["region"] == client.region
    assert record["attempt"] == 1
    assert record["http_status"] == 200
    assert record["request"]["system"] == "be terse"
    assert record["request"]["messages"] == [{"role": "user", "content": "what is the answer?"}]
    assert record["response"]["content"][0]["text"] == "the answer is 42"
    assert record["latency_s"] >= 0
    assert "timestamp" in record


def test_retry_succeeds_on_second_attempt_and_logs_both(stub_server, tmp_path):
    server = stub_server(
        [
            _ScriptedResponse(429, {"__type": "ThrottlingException", "message": "slow down"}),
            _ScriptedResponse(200, _success_body("succeeded on retry")),
        ]
    )
    log_path = tmp_path / "log.jsonl"
    client = BedrockClient(endpoint_url=server.url, log_path=log_path, sleep_fn=lambda s: None)

    response = client.send(system="s", user_message="u", model_id="test-model-id")

    assert response.text == "succeeded on retry"
    assert response.attempt == 2

    records = _read_log(log_path)
    assert len(records) == 2
    assert records[0]["attempt"] == 1
    assert records[0]["outcome"] == "throttled"
    assert records[0]["http_status"] == 429
    assert records[1]["attempt"] == 2
    assert records[1]["outcome"] == "success"


def test_exhaustion_raises_typed_exception_with_all_attempts_logged(tmp_path):
    dead_url = _closed_port_url()
    log_path = tmp_path / "log.jsonl"
    client = BedrockClient(endpoint_url=dead_url, log_path=log_path, max_attempts=3, sleep_fn=lambda s: None)

    with pytest.raises(BedrockRetriesExhaustedError) as exc_info:
        client.send(system="s", user_message="u", model_id="test-model-id")

    assert exc_info.value.attempts == 3

    records = _read_log(log_path)
    assert len(records) == 3
    assert [r["attempt"] for r in records] == [1, 2, 3]
    assert all(r["outcome"] == "transport_error" for r in records)
    assert all(r["http_status"] is None for r in records)


def test_malformed_response_body_raises_and_is_logged(stub_server, tmp_path):
    server = stub_server([_ScriptedResponse(200, b"this is not json{{{")])
    log_path = tmp_path / "log.jsonl"
    client = BedrockClient(endpoint_url=server.url, log_path=log_path, sleep_fn=lambda s: None)

    with pytest.raises(BedrockMalformedResponseError):
        client.send(system="s", user_message="u", model_id="test-model-id")

    records = _read_log(log_path)
    assert len(records) == 1
    assert records[0]["outcome"] == "malformed_response"
    assert records[0]["http_status"] == 200
    assert "this is not json" in records[0]["error"]["raw_body"]


def test_validation_error_fails_immediately_without_retry(stub_server, tmp_path):
    server = stub_server(
        [_ScriptedResponse(400, {"__type": "ValidationException", "message": "max_tokens too large"})]
    )
    log_path = tmp_path / "log.jsonl"
    client = BedrockClient(endpoint_url=server.url, log_path=log_path, max_attempts=3, sleep_fn=lambda s: None)

    with pytest.raises(BedrockRequestError) as exc_info:
        client.send(system="s", user_message="u", model_id="test-model-id")

    assert exc_info.value.http_status == 400
    assert exc_info.value.error_type == "ValidationException"

    records = _read_log(log_path)
    assert len(records) == 1  # no retry attempted
    assert records[0]["outcome"] == "error"


def test_endpoint_override_is_respected_and_no_boto_client_constructed(stub_server, tmp_path):
    server = stub_server([_ScriptedResponse(200, _success_body())])
    log_path = tmp_path / "log.jsonl"
    client = BedrockClient(endpoint_url=server.url, log_path=log_path, sleep_fn=lambda s: None)

    assert client._boto_client is None  # stub path never touches boto3 / AWS credentials

    client.send(system="s", user_message="u", model_id="test-model-id")

    assert len(server.requests_received) == 1
    assert server.requests_received[0]["messages"] == [{"role": "user", "content": "u"}]


def test_request_body_is_the_bedrock_anthropic_wire_format(stub_server, tmp_path):
    server = stub_server([_ScriptedResponse(200, _success_body())])
    log_path = tmp_path / "log.jsonl"
    client = BedrockClient(endpoint_url=server.url, log_path=log_path, sleep_fn=lambda s: None)

    client.send(system="be terse", user_message="hi", model_id="test-model-id", max_tokens=50, temperature=0.5)

    sent = server.requests_received[0]
    assert sent["anthropic_version"] == "bedrock-2023-05-31"
    assert sent["max_tokens"] == 50
    assert sent["temperature"] == 0.5
    assert sent["system"] == "be terse"
    assert sent["messages"] == [{"role": "user", "content": "hi"}]


def test_backoff_sleep_called_with_increasing_delay(stub_server, tmp_path):
    server = stub_server(
        [
            _ScriptedResponse(429, {"__type": "ThrottlingException", "message": "slow down"}),
            _ScriptedResponse(429, {"__type": "ThrottlingException", "message": "slow down"}),
            _ScriptedResponse(200, _success_body()),
        ]
    )
    log_path = tmp_path / "log.jsonl"
    sleeps = []
    client = BedrockClient(
        endpoint_url=server.url, log_path=log_path, max_attempts=3, retry_base_delay_s=1.0, sleep_fn=sleeps.append
    )

    client.send(system="s", user_message="u", model_id="test-model-id")

    assert sleeps == [1.0, 2.0]
