"""Audit every unresolved fact against the REAL Mathlib object it was mined from.

    SCORING_SCORES_DIR=scoring_output/smoke32b_scores uv run python scripts/audit_fact_truth.py

A fact left UNKNOWN against a candidate conflates three very different situations, and the
verifier currently cannot tell them apart:

  TRUE_OF_TRUTH      the fact provably holds of the genuine Mathlib definition -- so it is a
                     sound fact, and the UNKNOWN is a statement about proof difficulty
  FALSE_OF_TRUTH     its NEGATION proves against the genuine definition -- the fact is DEFECTIVE
                     (this is what Nat.log/log_lt_of_lt_pow and Nat.divisors/divisors_mem_iff
                     turned out to be, each missing an `n ≠ 0` side condition)
  UNDECIDED          neither direction closed in budget -- says nothing either way

Only the middle class indicts the task suite, and only the first justifies treating an UNKNOWN
as "the model could not do the maths". Guessing between them from the shape of a statement is
exactly the pattern-matching this script exists to replace.

The truth statement is the fact with the task symbol rewritten to the real name, which is the
same rewrite `_refutes_truth_too` performs -- one substitution, no re-elaboration of the task.
"""

import argparse
import collections
import dataclasses
import json
import sys
import time
from pathlib import Path

from harness.repl import get_warm_environment
from harness.results import CheckStatus
from harness.signature import root_qualify
from ladder.budgets import DEFAULT_LADDER_BUDGETS, TacticBudget
from ladder.tier2 import adjudicate_tier2
from scoring import config as cfg
from scoring import store
from scoring.samples import load_task
from scoring.verdicts import Verdict

FORWARD_TACTICS = (
    TacticBudget("rfl", 5.0),
    TacticBudget("decide", 10.0),
    TacticBudget("simp", 10.0),
    TacticBudget("omega", 5.0),
    TacticBudget("norm_num", 10.0),
    TacticBudget("aesop", 25.0, heavy=True),
    TacticBudget("intros <;> simp_all", 15.0),
)
NEGATION_TACTICS = (
    TacticBudget("decide", 10.0),
    TacticBudget("push_neg <;> simp_all", 15.0),
    TacticBudget("push_neg <;> omega", 10.0),
    TacticBudget("push_neg <;> aesop", 25.0, heavy=True),
)


def budgets(tactics):
    return dataclasses.replace(DEFAULT_LADDER_BUDGETS, tier2_tactics=tactics, tier3_enabled=False)


def unresolved_pairs(scores_dir):
    """(task, fact_id) -> how many admissible candidates left it UNKNOWN."""
    pairs = collections.Counter()
    for record in store.iter_verdicts(scores_dir=scores_dir):
        if not record.get("admissible"):
            continue
        for fv in (record.get("fact_verdicts") or []):
            if fv.get("verdict") == Verdict.UNKNOWN.value:
                pairs[(record["task_name"], fv["fact_id"])] += 1
    return pairs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", default="scoring_output/fact_truth_audit.json")
    args = ap.parse_args()

    pairs = unresolved_pairs(cfg.scores_dir())
    items = sorted(pairs.items(), key=lambda kv: -kv[1])
    if args.limit:
        items = items[: args.limit]
    print(f"auditing {len(items)} distinct unresolved facts against their real Mathlib objects",
          flush=True)

    server, base = get_warm_environment()
    if base.status is not CheckStatus.PASSED:
        raise RuntimeError(base.detail)

    results, counts = [], collections.Counter()
    t0 = time.perf_counter()
    for i, ((task, fid), n_cands) in enumerate(items, 1):
        t = load_task(task)
        real = t.get("truth_real_name")
        stmt = next((f.statement for f in t["facts"] if f.id == fid), None)
        if stmt is None or not real:
            counts["NO_TRUTH_NAME"] += 1
            continue
        # `example : ... := by decide`-shaped facts carry their own proof wrapper; audit the
        # proposition itself, not the wrapper.
        prop = stmt.strip()
        if prop.startswith("example"):
            prop = prop.split(":", 1)[1].rsplit(":=", 1)[0].strip()
        truth_prop = prop.replace(t["signature"].name, root_qualify(real))
        imports = cfg.imports_for(t.get("imports"))

        fwd = adjudicate_tier2(server, base.env, f"aud_{i}", truth_prop,
                               budgets(FORWARD_TACTICS), imports=imports)
        if fwd.winning is not None:
            verdict = "TRUE_OF_TRUTH"
        else:
            neg = adjudicate_tier2(server, base.env, f"audn_{i}", f"¬ ({truth_prop})",
                                   budgets(NEGATION_TACTICS), imports=imports)
            verdict = "FALSE_OF_TRUTH" if neg.winning is not None else "UNDECIDED"
        counts[verdict] += 1
        results.append({"task": task, "fact_id": fid, "candidates_unknown": n_cands,
                        "verdict": verdict, "statement": prop[:300]})
        if verdict == "FALSE_OF_TRUTH":
            print(f"  DEFECTIVE  {task}/{fid}  (unknown against {n_cands} candidates)", flush=True)
        if i % 10 == 0:
            rate = i / max(time.perf_counter() - t0, 1e-6)
            print(f"  {i}/{len(items)}  {dict(counts)}  eta {(len(items)-i)/rate/60:.0f} min",
                  flush=True)
    server.kill()

    print("\n" + "=" * 78)
    total = sum(counts.values())
    for k, v in counts.most_common():
        print(f"  {k:<18}{v:>5}  ({100*v/total:.1f}%)")
    weighted = collections.Counter()
    for r in results:
        weighted[r["verdict"]] += r["candidates_unknown"]
    print("\n weighted by candidates affected:")
    for k, v in weighted.most_common():
        print(f"  {k:<18}{v:>5}")
    Path(args.out).write_text(json.dumps(
        {"counts": dict(counts), "weighted": dict(weighted), "results": results}, indent=1),
        encoding="utf-8")
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
