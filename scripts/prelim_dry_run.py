#!/usr/bin/env python3
"""Full local rehearsal of the overnight run, against the stub endpoint. No GPU, no cost.

Exercises everything the real night will exercise except vLLM itself: all 7 models' prompt
assembly, the validity gate on both paths, bounded-concurrency generation, a mid-run kill and
relaunch proving resume, and the pod advance/status handshake against a stub control server.

    uv run python scripts/prelim_dry_run.py

Prints a transcript and exits non-zero if any rehearsal expectation fails, so it can be run as a
pre-flight check before touching a real pod.
"""

import json
import shutil
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from prelim import config as cfg
from prelim import store
from prelim.driver import RunLog, run_model, run_prelim
from prelim.models import MODEL_SLUGS, get_model
from prelim.prompts import assemble_prompt, prompt_text
from prelim.stubserver import ScriptedResponse, StubEndpointServer, chat_completion_body

GOOD = (
    "Let me plan first.\n\n```lean\ndef VTask.clog (b n : ℕ) : ℕ :=\n"
    "  if 1 < b ∧ 1 < n then VTask.clog b ((n + b - 1) / b) + 1 else 0\n```\n"
)
GARBAGE = "I'm sorry, I don't have enough information to answer that."

failures: list[str] = []


def check(label: str, condition: bool, detail: str = "") -> None:
    print(f"  {'PASS' if condition else 'FAIL'}  {label}{(' -- ' + detail) if detail else ''}")
    if not condition:
        failures.append(label)


class StubControl:
    """Stands in for scripts/pod_runner.py's control server."""

    def __init__(self, models: list[str]):
        self.models = models
        self.index = 0
        self.advances = 0
        outer = self

        class H(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def _reply(self, code, body):
                data = json.dumps(body).encode()
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self):
                if self.path.startswith("/v1/models"):
                    cur = outer.models[outer.index] if outer.index < len(outer.models) else None
                    self._reply(200, {"data": [{"id": cur}] if cur else []})
                else:
                    self._reply(200, {"model": outer.models[outer.index] if outer.index < len(outer.models) else None})

            def do_POST(self):
                outer.advances += 1
                outer.index += 1
                done = outer.index >= len(outer.models)
                self._reply(200, {
                    "model": None if done else outer.models[outer.index],
                    "terminating": done,
                })

            def log_message(self, *a):
                pass

        self._srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=self._srv.serve_forever, daemon=True).start()
        host, port = self._srv.server_address
        self.base = f"http://{host}:{port}"

    def stop(self):
        self._srv.shutdown()
        self._srv.server_close()


def main() -> int:
    work = Path(tempfile.mkdtemp(prefix="prelim_dry_"))
    samples_dir = work / "samples"
    print("=" * 78)
    print("PRELIM DRY RUN -- full rehearsal against the stub endpoint (no GPU, no cost)")
    print(f"scratch: {work}")
    print("=" * 78)

    # --- 1. prompt assembly for all 7 models ----------------------------------------------
    print("\n[1] Prompt assembly, all 7 models x 2 tasks")
    for slug in MODEL_SLUGS:
        for task in ("Nat.clog", "Nat.ModEq"):
            p = assemble_prompt(slug, task)
            text = prompt_text(p)
            ok = "Mathlib is already imported" in text and f"VTask.{task.split('.')[-1]}" in text
            if not ok:
                check(f"{slug}/{task} assembles", False)
                break
        else:
            spec = get_model(slug)
            n = len(prompt_text(assemble_prompt(slug, "Nat.clog")))
            check(f"{slug:28s} assembles ({spec.endpoint_style}, {n} chars)", True)

    # --- 2. happy path: 2 tasks x 2 samples ------------------------------------------------
    print("\n[2] Generation: 2 tasks x 2 samples, gate + concurrency")
    server = StubEndpointServer([ScriptedResponse(200, chat_completion_body(GOOD))])
    run_log = RunLog(work / "run_log.txt", echo=False)
    outcome = run_model(
        "goedel-prover-v2-8b", ["Nat.clog", "Nat.ModEq"], samples_per_task=2,
        samples_dir=samples_dir, endpoint_url=server.url, call_log_path=work / "calls.jsonl",
        run_log=run_log, concurrency=4,
    )
    check("gate passed and all 4 samples stored", outcome.status == "completed" and outcome.completed == 4,
          f"status={outcome.status} completed={outcome.completed}")
    check("no extraction failures on good output", outcome.extraction_failures == 0)

    # --- 3. gate failure path ----------------------------------------------------------------
    print("\n[3] Gate failure: a model returning garbage")
    bad_server = StubEndpointServer([ScriptedResponse(200, chat_completion_body(GARBAGE))])
    bad = run_model(
        "herald-7b", ["Nat.clog"], samples_per_task=10, samples_dir=samples_dir,
        endpoint_url=bad_server.url, run_log=run_log, concurrency=4,
    )
    check("gate halted the model", bad.status == "gate_failed")
    check("cost exactly 3 samples, not 10", bad_server.call_count == 3, f"calls={bad_server.call_count}")
    bad_server.stop()

    # --- 4. resume after a mid-run kill --------------------------------------------------------
    print("\n[4] Resume: delete 2 samples, relaunch, only those are regenerated")
    before = server.call_count
    for f in sorted((samples_dir / "goedel-prover-v2-8b" / "Nat.ModEq").glob("sample_*.json")):
        f.unlink()
    resumed = run_model(
        "goedel-prover-v2-8b", ["Nat.clog", "Nat.ModEq"], samples_per_task=2,
        samples_dir=samples_dir, endpoint_url=server.url, run_log=run_log, concurrency=4,
    )
    regenerated = server.call_count - before
    check("relaunch completed the set", resumed.completed == 4)
    check("regenerated only the 2 missing", regenerated == 2, f"regenerated={regenerated}")

    # --- 5. pod handshake ------------------------------------------------------------------------
    print("\n[5] Pod handshake: wait-for-model, advance, terminate")
    from prelim.podcontrol import PodControl

    models = ["goedel-prover-v2-8b", "qwen2.5-coder-7b-instruct"]
    ctrl = StubControl([get_model(m).hf_name for m in models])
    pod = PodControl(control_url=ctrl.base, models_url=f"{ctrl.base}/v1/models")
    fresh = work / "samples2"
    result = run_prelim(
        models, ["Nat.clog"], samples_per_task=1, samples_dir=fresh,
        endpoint_url=server.url, pod=pod, run_log_path=work / "run2.txt",
        summary_path=work / "summary.json", echo=False,
    )
    check("both models ran", [o.status for o in result.outcomes] == ["completed", "completed"])
    check("advanced once per model incl. final", ctrl.advances == 2, f"advances={ctrl.advances}")
    check("run not halted", result.stopped_reason is None)
    summary = json.loads((work / "summary.json").read_text())
    check("summary written with totals", bool(summary["totals"]), json.dumps(summary["totals"]))
    check("ALL DONE logged", "ALL DONE" in (work / "run2.txt").read_text())
    ctrl.stop()

    # --- 6. store summary --------------------------------------------------------------------------
    print("\n[6] Store summary")
    counts = store.summarize(samples_dir=samples_dir)
    print(f"      {json.dumps(counts, indent=6)}")
    check("summarize counts only complete samples", counts.get("goedel-prover-v2-8b", {}).get("Nat.clog") == 2)

    server.stop()
    print("\n" + "=" * 78)
    if failures:
        print(f"DRY RUN FAILED: {len(failures)} check(s) failed: {failures}")
    else:
        print("DRY RUN PASSED -- every rehearsed path behaved as designed")
    print(f"scratch retained at {work}")
    print("=" * 78)
    shutil.rmtree(work, ignore_errors=True)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
