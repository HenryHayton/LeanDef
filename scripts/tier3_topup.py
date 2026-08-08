"""Tier-3 top-up: re-adjudicate ONLY the facts tiers 1-2 left UNKNOWN, hammer enabled.

    # on the box:
    export PATH="$HOME/.elan/bin:$PATH"
    VERIFIER_LEAN_PROJECT_DIR=$HOME/verifier-lean \
    LEAN_INTERACT_LOAD_DYNLIB=$HOME/verifier-lean/.lake/packages/cvc5/.lake/build/lib/libcvc5_cvc5.so \
    SCORING_EXTRA_IMPORTS=Hammer \
    SCORING_SCORES_DIR=scoring_output/smoke32b_scores \
    .venv/bin/python scripts/tier3_topup.py

Why a dedicated pass rather than re-running `run_stage_d` with tier 3 on: the smoke records are
COMPLETE for both mechanisms, so the runner's resume would skip every one of them -- and stripping
completeness to force a full re-score would burn hours re-proving the 934 facts tiers 1-2 already
closed. `score_candidate_body` takes the fact list as an argument, so this pass hands it exactly
the unresolved facts and nothing else.

Selection: admissible records with >=1 UNKNOWN fact verdict. ERROR facts are excluded -- ERROR is
infrastructure, not adjudication, and this corpus has zero anyway. The candidate is re-spliced
from `extracted_code` (the record carries it; raw samples not needed), which also re-runs the
tier-4 equivalence probe WITH the hammer for candidates not yet certified -- the pilot's
residual tier-4 weakness (Monotone/DependsOn/Pi.Lex defeq pairs that rfl/simp missed) gets its
hammer shot in the same splice for free.

Merging reuses `scoring.runner._merge_with_existing` -- the same function every multi-pass write
goes through. A real verdict from this pass overwrites the stored UNKNOWN; everything else
carries forward untouched. `tier3_topup: true` is stamped on the record so a reader can tell
which pass resolved what.
"""

import argparse
import collections
import json
import sys
import time
from pathlib import Path

from ladder.budgets import DEFAULT_LADDER_BUDGETS
from scoring import config as cfg
from scoring import store
from scoring.candidate import score_candidate_body
from scoring.runner import ServerHandle, _merge_with_existing
from scoring.samples import load_task
from scoring.verdicts import Verdict, fidelity, resolution_rate


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None, help="smoke-test bound on candidates")
    args = ap.parse_args()
    scores_dir = cfg.scores_dir()
    assert DEFAULT_LADDER_BUDGETS.tier3_enabled, "top-up with tier 3 disabled is a no-op"
    extra = cfg.extra_imports()
    if "Hammer" not in extra:
        print("REFUSING: $SCORING_EXTRA_IMPORTS does not include Hammer -- the tactic would be "
              "unknown and every attempt would fail in ~0ms while looking like a real loss.")
        return 1

    todo = []
    for record in store.iter_verdicts(scores_dir=scores_dir):
        if not record.get("admissible") or not record.get("extracted_code"):
            continue
        unresolved = [fv["fact_id"] for fv in (record.get("fact_verdicts") or [])
                      if fv.get("verdict") == Verdict.UNKNOWN.value]
        if unresolved and not record.get("tier3_topup"):
            # The stamp is the resume marker: a topped-up record whose facts are STILL unknown
            # after the hammer has had its shot must not be re-attempted on every restart.
            todo.append((record, unresolved))

    if args.limit:
        todo = todo[: args.limit]
    n_facts = sum(len(u) for _, u in todo)
    by_model = collections.Counter(r["model_slug"] for r, _ in todo)
    print(f"{len(todo)} candidates carry {n_facts} unresolved facts  {dict(by_model)}", flush=True)

    handle = ServerHandle()
    done = resolved_now = certified_now = 0
    t0 = time.perf_counter()
    try:
        for record, unresolved in todo:
            model, task, idx = record["model_slug"], record["task_name"], record["sample_index"]
            t = load_task(task)
            facts = [f for f in t["facts"] if f.id in set(unresolved)]
            server, env = handle.get()
            fresh = score_candidate_body(
                server, env, t["signature"], record["extracted_code"], facts,
                truth_real_name=t.get("truth_real_name"),
                try_equivalence=not record.get("equivalence_certified"),
                imports=t.get("imports"),
            )
            fresh.update(model_slug=model, task_name=task, sample_index=idx)
            merged = _merge_with_existing(fresh, model, task, idx, scores_dir)
            merged["tier3_topup"] = True
            verdicts = [Verdict(fv["verdict"]) for fv in merged["fact_verdicts"]]
            merged["fidelity"] = fidelity(verdicts)
            merged["resolution_rate"] = resolution_rate(verdicts)
            store.write_verdict(merged, scores_dir=scores_dir)

            done += 1
            gained = sum(1 for fv in fresh.get("fact_verdicts", [])
                         if fv["fact_id"] in set(unresolved)
                         and fv["verdict"] in (Verdict.PASS.value, Verdict.FAIL.value))
            resolved_now += gained
            certified_now += bool(fresh.get("equivalence_certified")
                                  and not record.get("equivalence_certified"))
            if done % 10 == 0:
                rate = done / max(time.perf_counter() - t0, 1e-6)
                print(f"{done}/{len(todo)}  newly-resolved={resolved_now}/{n_facts}  "
                      f"newly-equiv={certified_now}  eta {((len(todo)-done)/rate)/60:.0f} min",
                      flush=True)
    finally:
        handle.close()

    print(f"\nDONE {done} candidates, {resolved_now}/{n_facts} facts newly resolved, "
          f"{certified_now} newly equivalence-certified, "
          f"{(time.perf_counter()-t0)/60:.1f} min "
          f"(recycles={handle.recycles} env_probe_fires={handle.env_probe_fires})")
    Path("scoring_output/tier3_topup_summary.json").write_text(json.dumps({
        "candidates": done, "facts_attempted": n_facts, "facts_newly_resolved": resolved_now,
        "newly_equivalence_certified": certified_now,
        "by_model": dict(by_model),
    }, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
