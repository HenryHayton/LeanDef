"""Author + validate a slice of the 200-task batch, and price it.

    # 3-task calibration, then the 50 checkpoint:
    uv run python scripts/run_batch200.py --limit 3
    uv run python scripts/run_batch200.py --limit 50

Wraps `authoring.batch.run_batch` (preflight gate, credential checks, chunking, rotation queue,
REPL-death recovery -- all already built) and adds the two things this batch specifically needs:

  * COST, as a first-class output. The 200 exists to price an eventual full-721 session, so
    per-task Bedrock spend is measured from the call log rather than estimated.
  * COMPOSITION COMPLIANCE against the new prompt rules -- the <=6 decide cap and >=2 reject
    floor are only real if something counts them. Reported per task, not just in aggregate,
    because a systematic miss at 3 tasks is a prompt fix and at 50 it is a rerun.

Resume is by file existence, implemented HERE: `authoring.batch.run_batch` has no existence
check of its own. That was assumed rather than verified once, and the 12 Aug resume re-authored
21 tasks that were already on disk -- paying twice and reaching none of the unattempted ones.
"""

import argparse
import collections
import json
import sys
import time
from pathlib import Path

NAMES_FILE = Path("authoring/batches/batch200_passing.txt")
PREFLIGHT = Path("authoring/batches/batch200_preflight.json")
OUT_DIR = Path("prelim_testing/tasks_batch200")


def _call_log_totals(path: Path, since_line: int) -> dict:
    """(calls, input_tokens, output_tokens) appended to the Bedrock call log since `since_line`."""
    if not path.exists():
        return {"calls": 0, "input_tokens": 0, "output_tokens": 0}
    lines = path.read_text(encoding="utf-8").splitlines()[since_line:]
    calls = inp = out = 0
    for line in lines:
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        calls += 1
        usage = (r.get("response") or {}).get("usage") or {}
        inp += usage.get("input_tokens") or 0
        out += usage.get("output_tokens") or 0
    return {"calls": calls, "input_tokens": inp, "output_tokens": out}


def composition(task_json: Path) -> dict:
    """The rules the new prompt states, counted from what actually shipped."""
    d = json.loads(task_json.read_text(encoding="utf-8"))
    facts = d.get("facts") or []
    decide = [f for f in facts if f.get("mechanism") == "decide"]
    reject = [f for f in facts if (f.get("polarity") == "reject")
              or any(t in (f.get("statement") or "") for t in ("¬", "∉", "≠"))]
    return {
        "n_facts": len(facts),
        "n_decide": len(decide),
        "n_reject": len(reject),
        "n_near_miss": sum(1 for f in facts if f.get("near_miss_clause")),
        "n_self_restatement": sum(1 for f in facts if f.get("self_restatement")),
        "decide_cap_ok": len(decide) <= 6,
        "reject_floor_ok": len(reject) >= 2,
        "suite_floor_ok": len(facts) >= 8,
        "boundary_labelled": sum(1 for f in decide if f.get("boundary_vs_interior")),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=3)
    ap.add_argument("--out", default=str(OUT_DIR))
    ap.add_argument("--redo", action="store_true",
                    help="re-author tasks that already have a task.json (default: skip them)")
    # Batch 2500 (16 Aug) reuses this runner unchanged apart from where it reads names and
    # preflight from -- deliberately the same code path, so the larger run is comparable to the
    # 200 rather than being a second implementation of it.
    ap.add_argument("--names", default=str(NAMES_FILE))
    ap.add_argument("--preflight", default=str(PREFLIGHT))
    args = ap.parse_args()
    names_file, preflight_path = Path(args.names), Path(args.preflight)

    from bedrock import config as bcfg
    from bedrock.client import BedrockClient
    from authoring.batch import run_batch
    from authoring.pipeline import PipelineConfig
    from harness.repl import get_warm_environment
    from harness.results import CheckStatus
    from authoring.resolve import make_resolver


    names = [n for n in names_file.read_text(encoding="utf-8").splitlines()
             if n.strip() and not n.startswith("#")][: args.limit]
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    if not args.redo:
        already = [n for n in names if (out_dir / n / "task.json").exists()]
        names = [n for n in names if n not in set(already)]
        if already:
            print(f"resume: skipping {len(already)} task(s) already on disk", flush=True)
    if not names:
        print("nothing to do -- every task in this slice is already authored")
        return 0
    slice_file = out_dir / f"_slice_{len(names)}.txt"
    slice_file.write_text("\n".join(names) + "\n", encoding="utf-8")
    print(f"{len(names)} tasks -> {out_dir}", flush=True)

    log_path = bcfg.CALL_LOG_PATH
    start_line = len(log_path.read_text(encoding="utf-8").splitlines()) if log_path.exists() else 0

    def _warm():
        # `run_batch`'s docstring suggests `lambda: get_warm_environment(...)`, but that returns
        # (server, CheckResult) while the batch wants (server, base_env:int) -- the CheckResult
        # reaches lean_interact as `Command(env=...)` and fails pydantic validation, rotating
        # every task with zero LLM calls made.
        srv, res = get_warm_environment()
        if res.status is not CheckStatus.PASSED:
            raise RuntimeError(res.detail)
        return srv, res.env

    server, base_env = _warm()

    config = PipelineConfig(
        client=BedrockClient(read_timeout_s=900.0),
        authoring_model_id=bcfg.AUTHORING_MODEL_ID,
        flagship_model_id=bcfg.FLAGSHIP_MODEL_ID,
        server=server, base_env=base_env,
        resolve_definition=make_resolver(preflight_path),
        output_dir=out_dir, batch_review_dir=out_dir,
    )
    t0 = time.perf_counter()
    result = run_batch(slice_file, config, preflight_path=preflight_path,
                       curation_yaml_path=Path("miner/curation.yaml"),
                       repl_warmup=_warm)
    elapsed = time.perf_counter() - t0
    cost = _call_log_totals(log_path, start_line)

    outcomes = collections.Counter(r.outcome for r in result.results)
    print(f"\n{'=' * 78}\nOUTCOMES {dict(outcomes)}   status={result.status}   "
          f"{elapsed / 60:.1f} min")

    comp, rows = {}, []
    for name in names:
        tj = out_dir / name / "task.json"
        if tj.exists():
            comp[name] = composition(tj)
            rows.append((name, comp[name]))
    print(f"\n{'task':<44}{'facts':>6}{'dec':>5}{'rej':>5}{'nm':>4}{'cap':>5}{'floor':>7}")
    for name, c in rows:
        print(f"{name:<44}{c['n_facts']:>6}{c['n_decide']:>5}{c['n_reject']:>5}"
              f"{c['n_near_miss']:>4}{'ok' if c['decide_cap_ok'] else 'OVER':>5}"
              f"{'ok' if c['reject_floor_ok'] else 'UNDER':>7}")

    per_task = (cost["input_tokens"] * 3.0 + cost["output_tokens"] * 15.0) / 1e6
    n_done = max(len(rows), 1)
    summary = {
        "tasks_attempted": len(names), "tasks_emitted": len(rows),
        "outcomes": dict(outcomes), "status": result.status,
        "wall_clock_min": round(elapsed / 60, 1),
        "bedrock": cost,
        "usd_total_at_sonnet_rates": round(per_task, 2),
        "usd_per_task": round(per_task / n_done, 3),
        "projected_50": round(per_task / n_done * 50, 2),
        "projected_200": round(per_task / n_done * 200, 2),
        "projected_721": round(per_task / n_done * 721, 2),
        "composition": comp,
    }
    (out_dir / "_calibration_summary.json").write_text(json.dumps(summary, indent=1),
                                                       encoding="utf-8")
    print(f"\nBedrock: {cost['calls']} calls, {cost['input_tokens']:,} in / "
          f"{cost['output_tokens']:,} out  ~= ${per_task:.2f}")
    print(f"per task ${per_task / n_done:.3f}   ->  50: ${summary['projected_50']}   "
          f"200: ${summary['projected_200']}   721: ${summary['projected_721']}")
    server.kill()
    return 0


if __name__ == "__main__":
    sys.exit(main())
