"""Run selection-time preflight over the batch-2500 pool, in resumable chunks.

    uv run python scripts/preflight_batch2500.py --limit 400

Preflight is mechanical -- `#check`, print-then-reparse the pinned type, splice the REAL body,
probe decidability for Prop-valued names. No Bedrock calls, so this costs REPL time only and is
safe to re-run.

**Resumable by name.** Results merge into the existing `batch2500_preflight.json`, and names
already recorded there are skipped. The pool is 2368 names and a full sweep is hours of REPL
time; authoring does not need to wait for all of it, so this is designed to be run a chunk at a
time while authoring works through the names already passing.

Emits `batch2500_passing.txt` -- the PASSing subset in pool order -- which is what the authoring
runner consumes as its name list.
"""

import argparse
import json
import sys
import time
from pathlib import Path

POOL = Path("authoring/batches/batch2500_2026-08-16.txt")
PREFLIGHT = Path("authoring/batches/batch2500_preflight.json")
PASSING = Path("authoring/batches/batch2500_passing.txt")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=400, help="names to preflight this run")
    args = ap.parse_args()

    from authoring.preflight import run_preflight, write_preflight_json, load_preflight_json
    from harness.repl import get_warm_environment
    from harness.results import CheckStatus

    pool = [n.strip() for n in POOL.read_text(encoding="utf-8").splitlines() if n.strip()]
    done = load_preflight_json(PREFLIGHT) if PREFLIGHT.exists() else {}
    todo = [n for n in pool if n not in done][: args.limit]
    print(f"pool {len(pool)}, already preflighted {len(done)}, this run {len(todo)}", flush=True)
    if not todo:
        print("nothing to do")
        return 0

    def _warm():
        srv, base = get_warm_environment()
        if base.status is not CheckStatus.PASSED:
            raise RuntimeError(base.detail)
        return srv, base.env

    server, base_env = _warm()

    def _stale(results: list) -> bool:
        """The AutoLeanServer restarted and `base_env` no longer names a live environment.

        Every subsequent name then fails instantly with `LeanError: Unknown environment.`
        WITHOUT BEING CHECKED. The first run of this script recorded 242 such entries as
        genuine preflight failures -- a 60% "fail" rate that was pure artefact. `run_batch`
        recovers from this through its `repl_warmup` hook; `run_preflight` has no equivalent,
        so the recovery has to live here.
        """
        return any(r.status != "pass" and "Unknown environment" in (r.detail or "")
                   for r in results)

    t0 = time.perf_counter()
    results = []
    # Chunked so a crash mid-sweep keeps everything already checked.
    for i in range(0, len(todo), 25):
        chunk = todo[i:i + 25]
        out = run_preflight(chunk, server, base_env)
        for attempt in range(3):
            if not _stale(out):
                break
            print(f"    REPL environment lost -- re-warming and redoing chunk "
                  f"(attempt {attempt + 1})", flush=True)
            try:
                server.kill()
            except Exception:  # noqa: BLE001 -- already dead is the common case
                pass
            server, base_env = _warm()
            out = run_preflight(chunk, server, base_env)
        if _stale(out):
            # Do not persist unchecked names as failures; leave them absent so a later run
            # picks them up.
            out = [r for r in out if not (r.status != "pass"
                                          and "Unknown environment" in (r.detail or ""))]
        results.extend(out)
        write_preflight_json(list(done.values()) + results, PREFLIGHT)
        rate = (i + len(chunk)) / max(time.perf_counter() - t0, 1e-6)
        n_pass = sum(1 for r in results if r.status == "pass")
        print(f"  {i + len(chunk)}/{len(todo)}  pass={n_pass}/{len(results)}  "
              f"{rate * 60:.0f}/min  eta {(len(todo) - i - len(chunk)) / rate / 60:.0f} min",
              flush=True)
    server.kill()

    all_res = load_preflight_json(PREFLIGHT)
    passing = [n for n in pool if n in all_res and all_res[n].status == "pass"]
    PASSING.write_text("\n".join(passing) + "\n", encoding="utf-8")

    cats = {}
    for r in all_res.values():
        if r.status != "pass":
            cats[r.category] = cats.get(r.category, 0) + 1
    print(f"\npreflighted {len(all_res)} total: {len(passing)} pass, {len(all_res) - len(passing)} fail")
    print(f"fail categories: {cats}")
    print(f"-> {PASSING}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
