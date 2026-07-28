"""Shared local-HTTP Bedrock stub, factored out of `tests/test_bedrock_client.py`'s original
in-file `_StubBedrockServer`/`_ScriptedResponse` pair so `tests/test_authoring_orchestrate.py`
can script canned responses for the new authoring-call shapes without duplicating the server
machinery. `test_bedrock_client.py` itself is left untouched (its own copy still works exactly
as before) -- this is a new shared copy, not a refactor of an existing file, per the task's
"no real Bedrock calls anywhere ... extend the stub's canned responses" instruction: extending
means a new shared fixture reusable by more tests, not editing bedrock.client's own test file
for an unrelated task.
"""

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class ScriptedResponse:
    def __init__(self, status: int, body):
        self.status = status
        # `body`: a dict (JSON-encoded automatically) or raw bytes (sent as-is, e.g. garbage).
        self.body = body


def success_body(text: str, *, stop_reason: str = "end_turn") -> dict:
    """The Bedrock-Anthropic wire-format success body `bedrock.client._extract_text` reads.
    `stop_reason` defaults to `"end_turn"` (a normal completion); pass `"max_tokens"` to script
    a truncated response for testing the truncation-as-malformed-response path."""
    return {
        "id": "msg_stub",
        "type": "message",
        "role": "assistant",
        "content": [{"type": "text", "text": text}],
        "model": "stub-model",
        "stop_reason": stop_reason,
        "stop_sequence": None,
        "usage": {"input_tokens": 12, "output_tokens": 5},
    }


class StubBedrockServer:
    """A real (loopback-only) HTTP server returning one scripted response per POST, in order.
    Records every request body received so tests can assert on what was sent."""

    def __init__(self, script: list[ScriptedResponse]):
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
