"""A minimal local HTTP server speaking the vLLM/OpenAI chat-completions response shape.

Lives in the package rather than under `tests/` on purpose: Stage 4's dry-run rehearsal needs to
run the whole driver end-to-end with no GPU, pointing `PRELIM_ENDPOINT_URL` at this server. Run
it standalone with `python -m prelim.stubserver` (see `main()` for flags).

**Scriptable failure sequences** are the reason this exists rather than a canned mock: the
client's whole value is its retry behaviour, and that can only be tested against something that
actually fails in a specified order (two 500s then a success; a hang long enough to trip the
read timeout; a permanent refusal). `ScriptedResponse` is one entry in that sequence.

Modelled on `tests/fixtures/bedrock_stub.py` (same loopback ThreadingHTTPServer approach,
`requests_received` for assertions) but speaking a different wire format and adding the delay /
connection-drop injections the bedrock stub never needed.
"""

import argparse
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from prelim import config

# Sentinel body: instead of replying, drop the connection without sending anything. Produces a
# genuine transport-level error client-side, which is what a dead pod actually looks like --
# distinct from any HTTP status, and not reproducible with one.
DROP_CONNECTION = "__DROP_CONNECTION__"


class ScriptedResponse:
    """One scripted reply. `status` is the HTTP status; `body` is a dict (JSON-encoded), raw
    bytes (sent as-is, e.g. to simulate a truncated/garbage body), or `DROP_CONNECTION`.
    `delay_s` sleeps before replying -- set it above the client's timeout to trip a read
    timeout."""

    def __init__(self, status: int = 200, body=None, *, delay_s: float = 0.0):
        self.status = status
        self.body = body
        self.delay_s = delay_s


def chat_completion_body(
    text: str,
    *,
    finish_reason: str = "stop",
    prompt_tokens: int = 17,
    completion_tokens: int = 5,
    model: str = "stub-model",
) -> dict:
    """The OpenAI/vLLM `chat.completion` success body `prelim.client` reads.

    ASSUMPTION (flagged for Stage 2's live smoke test): vLLM's OpenAI-compatible server returns
    the standard OpenAI shape -- `choices[0].message.content` for the text,
    `choices[0].finish_reason` in {"stop", "length", ...}, and a `usage` object with
    `prompt_tokens`/`completion_tokens`. This matches vLLM's documented OpenAI compatibility,
    but it is reproduced here from the spec, not from a captured real response.
    """
    return {
        "id": "chatcmpl-stub",
        "object": "chat.completion",
        "created": 1754200000,
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": text},
                "finish_reason": finish_reason,
                "logprobs": None,
            }
        ],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
        },
    }


def error_body(message: str, *, err_type: str = "BadRequestError", code: int = 400) -> dict:
    """vLLM's error shape (an OpenAI-style `error` object)."""
    return {"error": {"message": message, "type": err_type, "param": None, "code": code}}


class StubEndpointServer:
    """A real (loopback-only) HTTP server replying from a scripted sequence, in order.

    Once the script is exhausted the LAST entry repeats indefinitely, rather than erroring the
    way the bedrock stub does. That difference is deliberate: this server doubles as Stage 4's
    dry-run backend, where the driver will make hundreds of calls that no test enumerated, and
    "keep answering" is the useful behaviour there. Tests that care about exact call counts
    assert on `len(server.requests_received)`.
    """

    def __init__(self, script: list[ScriptedResponse] | None = None, *, port: int = 0):
        # `port=0` lets the OS pick a free ephemeral port -- what tests want, so parallel test
        # runs never collide. `main()` passes a fixed port so a human can point an env var at it.
        self.script = list(script) if script else [ScriptedResponse(200, chat_completion_body("stub completion"))]
        self.requests_received: list[dict] = []
        self.headers_received: list[dict] = []
        self._call_index = 0
        server = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def do_POST(self):
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length)
                try:
                    server.requests_received.append(json.loads(raw))
                except json.JSONDecodeError:
                    server.requests_received.append({"__unparseable__": raw.decode("utf-8", errors="replace")})
                server.headers_received.append(dict(self.headers))

                idx = min(server._call_index, len(server.script) - 1)
                server._call_index += 1
                scripted = server.script[idx]

                if scripted.delay_s:
                    time.sleep(scripted.delay_s)

                if scripted.body is DROP_CONNECTION or scripted.body == DROP_CONNECTION:
                    # Close without replying: a genuine transport error client-side.
                    self.close_connection = True
                    try:
                        self.wfile.close()
                    except Exception:
                        pass
                    return

                body = scripted.body if scripted.body is not None else chat_completion_body("stub completion")
                body_bytes = body if isinstance(body, bytes) else json.dumps(body).encode()
                self.send_response(scripted.status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body_bytes)))
                self.end_headers()
                self.wfile.write(body_bytes)

            def log_message(self, format, *args):  # noqa: A002 -- matches BaseHTTPRequestHandler
                pass  # silence per-request access logging during test runs

        self._httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
        self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)
        self._thread.start()

    @property
    def url(self) -> str:
        host, port = self._httpd.server_address
        return f"http://{host}:{port}/v1/chat/completions"

    @property
    def call_count(self) -> int:
        return len(self.requests_received)

    def stop(self):
        self._httpd.shutdown()
        self._httpd.server_close()
        self._thread.join(timeout=2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the prelim-testing stub endpoint standalone.")
    parser.add_argument("--port", type=int, default=8000, help="port to bind (default 8000)")
    parser.add_argument("--text", default="stub completion", help="completion text to return")
    parser.add_argument("--delay-s", type=float, default=0.0, help="artificial per-call delay")
    args = parser.parse_args()

    server = StubEndpointServer(
        [ScriptedResponse(200, chat_completion_body(args.text), delay_s=args.delay_s)],
        port=args.port,
    )
    print(f"prelim stub endpoint listening on {server.url}", flush=True)
    print(f"  export {config.ENV_ENDPOINT_URL}={server.url}", flush=True)
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop()
        print("\nstopped", flush=True)


if __name__ == "__main__":
    main()
