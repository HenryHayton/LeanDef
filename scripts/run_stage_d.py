"""Stage D — the decide-mechanism pass over every extractable candidate.

Full pipeline per candidate (`scoring.candidate.score_candidate_body`): re-extract from the
stored completion → declaration-verbatim splice with the Stage A retry ladder → admissibility
including WRONG_TYPE → tier-4 equivalence fast path → decide facts via tier 1. Proof-mechanism
facts are marked `NOT_ATTEMPTED_THIS_PASS`, distinct from UNKNOWN, and the resume logic records
that the record covers `decide` only so Stage E can fill them in without rescoring.

Sequential, single worker. Decide facts are kernel computation measured at ~13 ms each, so
parallelism buys little and costs the coordination risk that produced this project's one real
outage.

`--limit-candidates` implements the priority rule: run a bounded prefix, inspect the funnel, and
only then commit to the full pass. A systematic surprise at scale is much cheaper to find in the
first 50 candidates than in the last 50.
"""

import argparse
import collections
import json
import time
from pathlib import Path

from ladder.budgets import DEFAULT_LADDER_BUDGETS
from scoring import config as cfg
from scoring import store
from scoring.runner import ServerHandle, score_task
from scoring.samples import available_models, available_tasks




def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit-candidates", type=int, default=None,
                    help="stop after roughly this many candidates have been SCORED (priority rule)")
    ap.add_argument("--models", nargs="*", default=None)
    ap.add_argument("--out", default="scoring_output/stage_d_summary.json")
    ap.add_argument("--mechanisms", default="decide",
                    help="comma-separated: 'decide' for Stage D, 'proof' for Stage E")
    args = ap.parse_args()

    mechanisms = tuple(m.strip() for m in args.mechanisms.split(',') if m.strip())
    models = args.models or [m for m in available_models() if not m.startswith("kimina")]
    print(f"pass mechanisms={mechanisms}  models={models}\n", flush=True)

    handle = ServerHandle()
    started = time.perf_counter()
    per_model: dict[str, dict] = {}
    scored_total = 0
    stopped_early = False

    try:
        for model in models:
            tasks = available_tasks(model)
            agg = {"scored": 0, "fanned_out": 0, "skipped": 0, "unextractable": 0,
                   "equivalence_hits": 0, "noncomputable": 0,
                   "admissibility": collections.Counter(), "errors": [], "tasks": 0}
            for task_name in tasks:
                if args.limit_candidates is not None and scored_total >= args.limit_candidates:
                    stopped_early = True
                    break
                out = score_task(model, task_name, handle, budgets=DEFAULT_LADDER_BUDGETS,
                                 mechanisms=mechanisms)
                agg["tasks"] += 1
                for k in ("scored", "fanned_out", "skipped", "unextractable",
                          "equivalence_hits", "noncomputable"):
                    agg[k] += getattr(out, k)
                agg["admissibility"].update(out.admissibility)
                agg["errors"].extend(out.errors)
                scored_total += out.scored
            agg["admissibility"] = dict(agg["admissibility"])
            per_model[model] = agg
            print(f"  == {model}: scored={agg['scored']} fanned={agg['fanned_out']} "
                  f"equiv={agg['equivalence_hits']} noncomputable={agg['noncomputable']} "
                  f"adm={agg['admissibility']}", flush=True)
            if stopped_early:
                break
    finally:
        handle.close()

    wall = time.perf_counter() - started
    summary = {
        "generated_at_unix": int(time.time()),
        "mechanisms": list(mechanisms),
        "models": per_model,
        "scored_total": scored_total,
        "stopped_early": stopped_early,
        "limit_candidates": args.limit_candidates,
        "env_probe_fires": handle.env_probe_fires,
        "server_recycles": handle.recycles,
        "wall_clock_s": round(wall, 1),
        "per_candidate_s": round(wall / scored_total, 3) if scored_total else None,
        "scores_dir": str(cfg.scores_dir()),
        "verdict_files": sum(1 for _ in store.iter_verdicts()),
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"\n{'=' * 70}")
    print(f"scored {scored_total} candidates in {wall / 60:.1f} min "
          f"({summary['per_candidate_s']}s each)")
    print(f"env_probe_fires={handle.env_probe_fires} recycles={handle.recycles} "
          f"verdict_files={summary['verdict_files']}")
    if stopped_early:
        print("STOPPED EARLY at the requested limit -- inspect the funnel before continuing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
