#!/usr/bin/env python3
"""Pod-side model sequencer for prelim testing. Single file, stdlib only, deliberately boring.

Runs on the rented GPU pod. Serves one model at a time with `vllm serve`, and exposes a tiny
control server so the Mac-side driver can advance to the next model when it is finished with the
current one.

    port 8000 : vLLM's own OpenAI-compatible API (this script does not touch it)
    port 8001 : this script's control server
                POST /advance  -> kill current vLLM, start next model (or terminate the pod)
                GET  /status   -> {model, index, uptime_s, ...}

**The pod is dumb on purpose.** It knows only its ordered model list and how to move one step
along it. Every judgement -- is this output usable, is this model finished, should we stop --
lives on the Mac, where the state is durable. A pod that decided things for itself would be a
second source of truth to reconcile after a crash.

**Two independent ways this pod stops billing**, because the failure that actually costs money is
the Mac dying at 2am and nobody noticing until morning:
  1. The driver advances past the last model -> self-terminate.
  2. The idle watchdog: no vLLM request for IDLE_TIMEOUT_S -> self-terminate regardless.
The watchdog is the one that matters. It assumes nothing about the Mac being alive.

Termination needs `RUNPOD_API_KEY` and `RUNPOD_POD_ID`. If either is unset the script prints a
large banner instead of failing -- an un-terminated pod costing money is bad, but a script that
crashes on startup because a variable was missing is worse, since then nothing runs at all.

This file cannot be honestly integration-tested from a Mac with no GPU. It is therefore written
to be verifiable by reading, and its real verification is the runbook's smoke test.
"""

import json
import os
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# The seven models, in serving order. MUST match `prelim.models.MODELS` order -- the driver waits
# for a specific hf_name before generating, so a mismatch stalls rather than corrupts, but a
# stall at 2am still costs the night.
MODELS = [
    "Goedel-LM/Goedel-Prover-V2-8B",
    "deepseek-ai/DeepSeek-Prover-V2-7B",
    "AI-MO/Kimina-Prover-Preview-Distill-7B",
    "AI-MO/Kimina-Autoformalizer-7B",
    "FrenzyMath/Herald_translator",
    "Goedel-LM/Goedel-Formalizer-V2-8B",
    "Qwen/Qwen2.5-Coder-7B-Instruct",
]

VLLM_PORT = 8000
CONTROL_PORT = 8001
MAX_MODEL_LEN = 8192
IDLE_TIMEOUT_S = 60 * 60  # 60 minutes with no vLLM traffic -> assume the Mac died, stop billing
WATCHDOG_POLL_S = 60


def log(msg: str) -> None:
    print(f"[pod_runner] {time.strftime('%Y-%m-%dT%H:%M:%S')} {msg}", flush=True)


class Sequencer:
    """Owns the current vLLM subprocess and the position in the model list."""

    def __init__(self, models: list[str], *, spawn=None, port: int = VLLM_PORT):
        self.models = list(models)
        self.index = -1
        self.proc: subprocess.Popen | None = None
        self.started_at: float | None = None
        self.terminating = False
        self.port = port
        # Injectable so the sequencing logic is testable without a GPU or a real vLLM binary.
        self._spawn = spawn if spawn is not None else self._spawn_vllm
        self._lock = threading.Lock()

    def _spawn_vllm(self, hf_name: str) -> subprocess.Popen:
        cmd = [
            "vllm", "serve", hf_name,
            "--port", str(self.port),
            "--max-model-len", str(MAX_MODEL_LEN),
            "--disable-log-requests",
        ]
        log(f"launching: {' '.join(cmd)}")
        return subprocess.Popen(cmd)

    @property
    def current_model(self) -> str | None:
        return self.models[self.index] if 0 <= self.index < len(self.models) else None

    def start_next(self) -> str | None:
        """Kill the current server (if any) and start the next model. Returns the new model name,
        or None when the list is exhausted."""
        with self._lock:
            self._kill_current()
            self.index += 1
            if self.index >= len(self.models):
                log("model list exhausted")
                return None
            hf_name = self.models[self.index]
            log(f"starting model {self.index + 1}/{len(self.models)}: {hf_name}")
            self.proc = self._spawn(hf_name)
            self.started_at = time.time()
            return hf_name

    def _kill_current(self) -> None:
        if self.proc is None:
            return
        log(f"stopping vLLM for {self.current_model}")
        try:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=120)
            except subprocess.TimeoutExpired:
                # A model mid-load can ignore SIGTERM; a stuck old process holding VRAM would
                # make the NEXT model fail to load, so escalate rather than hope.
                log("vLLM did not exit in 120s; killing")
                self.proc.kill()
                self.proc.wait(timeout=30)
        except Exception as e:  # noqa: BLE001 - never let teardown block the next model
            log(f"error stopping vLLM (continuing): {e}")
        self.proc = None
        self.started_at = None

    def status(self) -> dict:
        return {
            "model": self.current_model,
            "index": self.index,
            "total": len(self.models),
            "uptime_s": round(time.time() - self.started_at, 1) if self.started_at else None,
            "terminating": self.terminating,
            "vllm_running": self.proc is not None and self.proc.poll() is None,
        }


def terminate_pod() -> bool:
    """Ask RunPod to terminate this pod. Returns True if the API accepted the request.

    Prints a loud banner and returns False when the credentials are absent, rather than raising:
    the caller has already finished its work by this point, and crashing here would only replace
    a billing problem with a confusing traceback.
    """
    api_key, pod_id = os.environ.get("RUNPOD_API_KEY"), os.environ.get("RUNPOD_POD_ID")
    if not api_key or not pod_id:
        banner = "!" * 74
        print(f"\n{banner}\n!!! RUNPOD_API_KEY / RUNPOD_POD_ID NOT SET -- CANNOT SELF-TERMINATE\n"
              f"!!! PLEASE TERMINATE THIS POD MANUALLY FROM THE RUNPOD DASHBOARD NOW\n{banner}\n",
              flush=True)
        return False

    payload = json.dumps({"query": f'mutation {{ podTerminate(input: {{podId: "{pod_id}"}}) }}'}).encode()
    req = urllib.request.Request(
        f"https://api.runpod.io/graphql?api_key={api_key}",
        data=payload, headers={"Content-Type": "application/json"}, method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            log(f"pod terminate requested; API replied {r.status}")
            return True
    except (urllib.error.URLError, OSError) as e:
        log(f"pod terminate FAILED: {e} -- TERMINATE MANUALLY")
        return False


class IdleWatchdog(threading.Thread):
    """Terminates the pod if vLLM sees no traffic for `timeout_s`.

    Liveness is probed by hitting vLLM's own `/v1/models`, and 'activity' is defined as the
    driver having advanced or the control server having been touched -- see `touch()`. The point
    is not precision; it is that a Mac which crashed at 2am cannot leave an A100 billing until
    morning.
    """

    daemon = True

    def __init__(self, sequencer: Sequencer, *, timeout_s: float = IDLE_TIMEOUT_S,
                 poll_s: float = WATCHDOG_POLL_S, on_idle=terminate_pod, clock=time.monotonic,
                 sleep_fn=time.sleep):
        super().__init__(name="idle-watchdog")
        self.sequencer = sequencer
        self.timeout_s = timeout_s
        self.poll_s = poll_s
        self.on_idle = on_idle
        self._clock = clock
        self._sleep = sleep_fn
        self._last_activity = clock()
        self._stop = threading.Event()

    def touch(self) -> None:
        self._last_activity = self._clock()

    def idle_for(self) -> float:
        return self._clock() - self._last_activity

    def stop(self) -> None:
        self._stop.set()

    def run(self) -> None:
        while not self._stop.is_set():
            self._sleep(self.poll_s)
            if self._stop.is_set():
                return
            if self.idle_for() >= self.timeout_s:
                log(f"IDLE WATCHDOG: no activity for {self.idle_for() / 60:.0f} min -- terminating pod")
                self.sequencer.terminating = True
                self.on_idle()
                return


def make_control_server(sequencer: Sequencer, watchdog: IdleWatchdog | None, *,
                        port: int = CONTROL_PORT, on_finished=terminate_pod) -> ThreadingHTTPServer:
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def _reply(self, code: int, body: dict) -> None:
            data = json.dumps(body).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if watchdog:
                watchdog.touch()
            if self.path.rstrip("/") == "/status":
                self._reply(200, sequencer.status())
            else:
                self._reply(404, {"error": "not found"})

        def do_POST(self):
            if watchdog:
                watchdog.touch()
            if self.path.rstrip("/") != "/advance":
                self._reply(404, {"error": "not found"})
                return
            nxt = sequencer.start_next()
            if nxt is None:
                sequencer.terminating = True
                self._reply(200, {"model": None, "terminating": True, "message": "all models served"})
                log("all models served -- terminating pod")
                # Reply first, then terminate: the driver's advance call must not hang on a pod
                # that is busy killing itself.
                threading.Thread(target=on_finished, daemon=True).start()
            else:
                self._reply(200, {"model": nxt, "index": sequencer.index, "terminating": False})

        def log_message(self, format, *args):  # noqa: A002
            pass

    return ThreadingHTTPServer(("0.0.0.0", port), Handler)


def main() -> int:
    log(f"starting; {len(MODELS)} models to serve")
    sequencer = Sequencer(MODELS)
    watchdog = IdleWatchdog(sequencer)
    server = make_control_server(sequencer, watchdog)

    first = sequencer.start_next()
    log(f"first model: {first}")
    watchdog.start()
    threading.Thread(target=server.serve_forever, daemon=True).start()
    log(f"control server on port {CONTROL_PORT} (POST /advance, GET /status)")

    try:
        while not sequencer.terminating:
            time.sleep(5)
            # If vLLM died on its own (OOM, bad model id), say so loudly rather than sitting
            # there serving nothing -- the driver's own wait_for_model will time out, but this
            # makes the pod log say why.
            if sequencer.proc is not None and sequencer.proc.poll() is not None:
                log(f"WARNING: vLLM for {sequencer.current_model} exited with {sequencer.proc.returncode}")
                sequencer.proc = None
    except KeyboardInterrupt:
        log("interrupted")
    finally:
        watchdog.stop()
        sequencer._kill_current()
    log("exiting")
    return 0


if __name__ == "__main__":
    sys.exit(main())
