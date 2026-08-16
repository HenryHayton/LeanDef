"""Re-adjudicate ONLY the UNKNOWN facts, with the 11 Aug 2026 ladder fixes in place.

    SCORING_SCORES_DIR=scoring_output/smoke32b_scores \
    uv run python scripts/rescore_unknowns.py

Existing PASS/certification verdicts are sound and are NOT re-run: `score_candidate_body` takes
the fact list as an argument, so this hands it exactly the unresolved facts and nothing else.
Anything already certified carries forward untouched via `_merge_with_existing`.

What changed under it, and why a rescore is expected to move:
  - tier 2 now unfolds the candidate's own definition on GLOBAL facts (579 of 731 unknowns)
  - tier 4 now attempts funext + induction, which certifies recursive candidates and transfers
    the WHOLE suite (Nat.choose: 16 admissible candidates, 0 certified, 128 unknowns)
  - winning tactics are recorded, so the newly-resolved population can be attributed

`tier3_enabled` follows the environment as usual: on the laptop there is no Hammer build, and a
tier-3 attempt would fail in ~0ms while looking like a real loss.
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

STAMP = "unfold_rescore"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--task", default=None, help="restrict to one task (smoke)")
    ap.add_argument("--include-errors", action="store_true",
                    help="also re-adjudicate ERROR facts. An ERROR is usually a genuine outcome, "
                         "but `LeanError: Unknown environment` is not -- it means a server restart "
                         "invalidated the env mid-candidate and the fact was never actually tried. "
                         "`scoring.runner` warns that a restart contaminates the ERROR population; "
                         "this recovers it. In the 2026-08-16 pilot ALL 112 errors were of that "
                         "kind, 72 of them on Nat.FermatPsp -- the one task whose decide-mechanism "
                         "reject facts are able to produce a FAIL at all.")
    args = ap.parse_args()
    # Only the environment-loss errors are recoverable; a real elaboration failure is a result and
    # re-running it just burns time to reach the same answer.
    RECOVERABLE_ERROR = "Unknown environment"
    scores_dir = cfg.scores_dir()

    todo = []
    for record in store.iter_verdicts(scores_dir=scores_dir):
        if not record.get("admissible") or not record.get("extracted_code"):
            continue
        if record.get(STAMP):
            continue
        if args.task and record["task_name"] != args.task:
            continue
        def wanted(fv) -> bool:
            v = fv.get("verdict")
            if v == Verdict.UNKNOWN.value:
                return True
            return (args.include_errors and v == Verdict.ERROR.value
                    and RECOVERABLE_ERROR in (fv.get("detail") or ""))

        unresolved = [fv["fact_id"] for fv in (record.get("fact_verdicts") or []) if wanted(fv)]
        if unresolved:
            todo.append((record, unresolved))
    if args.limit:
        todo = todo[: args.limit]

    n_facts = sum(len(u) for _, u in todo)
    print(f"{len(todo)} candidates carry {n_facts} unresolved facts"
          f"{' (UNKNOWN + recoverable ERROR)' if args.include_errors else ' (UNKNOWN)'}  "
          f"{dict(collections.Counter(r['model_slug'] for r, _ in todo))}", flush=True)

    handle = ServerHandle()
    done = gained = newly_equiv = 0
    by_tactic = collections.Counter()
    by_model = collections.Counter()
    by_class = collections.Counter()
    t0 = time.perf_counter()
    try:
        for record, unresolved in todo:
            model, task, idx = record["model_slug"], record["task_name"], record["sample_index"]
            t = load_task(task)
            wanted = set(unresolved)
            facts = [f for f in t["facts"] if f.id in wanted]
            kinds = {f.id: (f.type, f.mechanism) for f in facts}
            server, env = handle.get()
            fresh = score_candidate_body(
                server, env, t["signature"], record["extracted_code"], facts,
                truth_real_name=t.get("truth_real_name"),
                try_equivalence=not record.get("equivalence_certified"),
                imports=t.get("imports"),
            )
            fresh.update(model_slug=model, task_name=task, sample_index=idx)
            merged = _merge_with_existing(fresh, model, task, idx, scores_dir)
            for k, v in (record or {}).items():
                merged.setdefault(k, v)
            merged[STAMP] = True
            verdicts = [Verdict(fv["verdict"]) for fv in merged["fact_verdicts"]]
            merged["fidelity"] = fidelity(verdicts)
            merged["resolution_rate"] = resolution_rate(verdicts)
            store.write_verdict(merged, scores_dir=scores_dir)

            if fresh.get("equivalence_certified") and not record.get("equivalence_certified"):
                newly_equiv += 1
            for fv in fresh.get("fact_verdicts", []):
                if fv["fact_id"] in wanted and fv["verdict"] in (Verdict.PASS.value,
                                                                 Verdict.FAIL.value):
                    gained += 1
                    by_model[model] += 1
                    ftype, mech = kinds.get(fv["fact_id"], ("?", "?"))
                    by_class[f"{ftype}/{mech}"] += 1
                    by_tactic[(fv.get("script") or "(unrecorded)")[:60]] += 1
            done += 1
            if done % 10 == 0:
                rate = done / max(time.perf_counter() - t0, 1e-6)
                print(f"{done}/{len(todo)}  resolved={gained}/{n_facts}  "
                      f"newly-equiv={newly_equiv}  eta {((len(todo)-done)/rate)/60:.0f} min",
                      flush=True)
    finally:
        handle.close()

    mins = (time.perf_counter() - t0) / 60
    print(f"\nDONE {done} candidates: {gained}/{n_facts} previously-UNKNOWN facts resolved, "
          f"{newly_equiv} newly equivalence-certified, {mins:.1f} min")
    print("\nby model:", dict(by_model))
    print("by fact class:", dict(by_class))
    print("\nwinning tactic on newly-resolved facts:")
    for tac, n in by_tactic.most_common(25):
        print(f"  {n:>4}x  {tac}")
    Path("scoring_output/unfold_rescore_summary.json").write_text(json.dumps({
        "candidates": done, "facts_attempted": n_facts, "facts_resolved": gained,
        "newly_equivalence_certified": newly_equiv, "minutes": round(mins, 1),
        "by_model": dict(by_model), "by_class": dict(by_class),
        "by_tactic": {k: v for k, v in by_tactic.most_common()},
    }, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
