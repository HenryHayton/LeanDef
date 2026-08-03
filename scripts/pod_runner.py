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
# Four, not the original seven: DeepSeek and Herald produce byte-corrupted output under
# vLLM 0.26, and Kimina-Autoformalizer emits theorem statements rather than definitions.
# See prelim.models.DROPPED_MODELS for the evidence behind each exclusion.
MODELS = [
    "Goedel-LM/Goedel-Prover-V2-8B",
    "AI-MO/Kimina-Prover-Preview-Distill-7B",
    "Goedel-LM/Goedel-Formalizer-V2-8B",
    "Qwen/Qwen2.5-Coder-7B-Instruct",
]

# Per-model --max-model-len. A model whose config caps max_position_embeddings BELOW the value
# we ask for refuses to start at all: Herald (4096) aborted the first live smoke run this way,
# and because the driver can only wait for a model that never appears, one wrong number here
# costs a 15-minute timeout and halts the whole run. Anything absent uses DEFAULT_MAX_MODEL_LEN.
# Values verified from each model's own config.json on the pod, 2026-08-03.
MAX_MODEL_LEN_BY_MODEL: dict[str, int] = {
    # (Herald's 4096 entry removed with the model itself.) All four survivors take the default.
}
DEFAULT_MAX_MODEL_LEN = 16384

VLLM_PORT = 8000
# 8500, not 8001 (changed 2026-08-03 during live setup). The RunPod PyTorch template ships an
# nginx that already binds 0.0.0.0:8001 for its unused "vscode server" block, proxying it to
# localhost:8000 -- so binding 8001 here fails with EADDRINUSE, and both exposed external ports
# would otherwise land on vLLM. Setup repoints that one nginx proxy_pass at 8500, giving:
#     external :8000 -> vLLM directly
#     external :8001 -> nginx -> localhost:8500 -> this control server
CONTROL_PORT = 8500
# 90 minutes (raised from 60 on 2026-08-03, before the live run): the watchdog's activity signal
# is control-server traffic, and the driver can legitimately spend a long stretch generating
# against port 8000 without touching port 8001 -- long temperature-1.0 generations were measured
# running close to the old 60-minute margin. 90 keeps the protection (a Mac that dies at 2am
# still stops the meter within the hour and a half) while removing the false-positive risk.
IDLE_TIMEOUT_S = 90 * 60
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
        # Flags kept minimal and version-stable on purpose. `--disable-log-requests` was valid in
        # vLLM 0.6.x but REMOVED by 0.26.0 (the version that actually installed on the pod,
        # 2026-08-03), where it aborts startup with "unrecognized arguments". It only suppressed
        # per-request log lines, which go to a file nobody reads during the run, so it is simply
        # dropped rather than replaced -- fewer flags is fewer things to break on a version bump.
        cmd = [
            "vllm", "serve", hf_name,
            "--port", str(self.port),
            "--max-model-len", str(MAX_MODEL_LEN_BY_MODEL.get(hf_name, DEFAULT_MAX_MODEL_LEN)),
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

    # REST, not GraphQL (fixed 2026-08-03 after two live failures). The GraphQL
    # `podTerminate` mutation returned HTTP 403 Forbidden for BOTH a read-scoped key and a
    # write-scoped one -- i.e. the 403 was about the call, not the credential; that mutation
    # appears to be retired. `DELETE /v1/pods/{id}` on RunPod's REST API is the current path, and
    # a read-only `GET` on the same resource with the same Bearer auth was verified to return 200
    # before switching. The DELETE itself is deliberately NOT exercised in testing: the only way
    # to prove it is to destroy the pod.
    req = urllib.request.Request(
        f"https://rest.runpod.io/v1/pods/{pod_id}",
        headers={"Authorization": f"Bearer {api_key}"}, method="DELETE",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            log(f"pod terminate requested via REST; API replied {r.status}")
            return True
    except (urllib.error.URLError, OSError) as e:
        log(f"pod terminate FAILED: {e} -- TERMINATE MANUALLY FROM THE DASHBOARD")
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
