"""Which "genuine theorem" facts can actually DISCRIMINATE, and which merely restate the definition?

    SCORING_SCORES_DIR=scoring_output/smoke32b_scores \
    uv run python scripts/audit_fact_discrimination.py

**Why.** Stage-2 validation asks "is this fact TRUE of the ground truth?". Every fact here passes
that. It never asks "could this fact ever be FALSE of a plausible misreading?" -- and a fact with
no possible counterexample cannot measure faithfulness however true it is.

The clearest such class is the DEFINITIONAL RESTATEMENT: `Relation.Map r f g c d ↔ ∃ a b, r a b ∧
f a = c ∧ g b = d` is Mathlib's `Relation.map_apply`, a real named lemma -- proved there by
`Iff.rfl`, because it just unfolds the definition. Any candidate written in that shape satisfies
it for free; a correct candidate written differently may fail it. It rewards syntactic conformity,
not correctness. `Relation.Map/map_apply_unfold` is the same statement again, anchored to the
DEFINITION rather than to any theorem.

**The test.** State the fact about the REAL Mathlib object and try `rfl` / `Iff.rfl` alone. If it
closes, the fact is definitionally true of the truth, and its discriminating power is at best
weak. Deliberately conservative: `rfl`-closure is sufficient evidence of restatement, not
necessary, so this UNDER-counts. Facts needing genuine work are reported as SUBSTANTIVE.

Nothing here changes a verdict. It reclassifies facts so a resolution figure can be reported over
the discriminating subset instead of over everything.
"""

import argparse
import collections
import dataclasses
import json
import sys
import time
from pathlib import Path

from harness.repl import get_warm_environment, run_checked
from harness.results import CheckStatus
from harness.signature import root_qualify
from lean_interact import Command
from scoring import config as cfg
from scoring.samples import load_task

RFL_PROOFS = ("by intros; rfl", "by intros; exact Iff.rfl", "by rfl", "Iff.rfl")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", default="scoring_output/fact_discrimination_audit.json")
    args = ap.parse_args()

    items = []
    for tdir in sorted(Path("prelim_testing/tasks").glob("*/task.json")):
        task = tdir.parent.name
        d = json.loads(tdir.read_text())
        real = (d.get("provenance") or {}).get("mathlib_name")
        for f in d["facts"]:
            if f.get("mechanism") == "proof":
                items.append((task, f["id"], f["statement"], f.get("type"), real,
                              (f.get("anchors") or [])))
    if args.limit:
        items = items[: args.limit]
    print(f"auditing {len(items)} proof-mechanism facts for definitional restatement", flush=True)

    server, base = get_warm_environment()
    if base.status is not CheckStatus.PASSED:
        raise RuntimeError(base.detail)

    results, counts = [], collections.Counter()
    t0 = time.perf_counter()
    for i, (task, fid, stmt, ftype, real, anchors) in enumerate(items, 1):
        if not real:
            counts["NO_TRUTH"] += 1
            continue
        sym = load_task(task)["signature"].name
        truth_stmt = stmt.replace(sym, root_qualify(real))
        verdict = "SUBSTANTIVE"
        for pf in RFL_PROOFS:
            out = run_checked(server, Command(cmd=f"example : {truth_stmt} := {pf}", env=base.env),
                              timeout=30.0)
            if out.status is CheckStatus.PASSED:
                verdict = "RESTATEMENT"
                break
        # A fact anchored to the DEFINITION rather than to a theorem about it is a restatement
        # by construction, whether or not rfl happens to close it in this formulation.
        anchored_to_def = any(a == real or a.endswith(f".{real.rsplit('.', 1)[-1]}")
                              for a in anchors)
        if verdict == "SUBSTANTIVE" and anchored_to_def and not any(
                a != real and "." in a for a in anchors):
            verdict = "ANCHORED_TO_DEFINITION"
        counts[verdict] += 1
        results.append({"task": task, "fact_id": fid, "type": ftype, "verdict": verdict,
                        "anchors": anchors, "statement": stmt[:220]})
        if i % 25 == 0:
            rate = i / max(time.perf_counter() - t0, 1e-6)
            print(f"  {i}/{len(items)}  {dict(counts)}  eta {(len(items)-i)/rate/60:.0f} min",
                  flush=True)
    server.kill()

    print("\n" + "=" * 70)
    tot = sum(counts.values())
    for k, v in counts.most_common():
        print(f"  {k:<24}{v:>5}  ({100*v/tot:.1f}%)")
    print("\nRESTATEMENTS by task:")
    per = collections.Counter(r["task"] for r in results if r["verdict"] != "SUBSTANTIVE")
    for t, n in per.most_common(15):
        print(f"  {n:>3}  {t}")
    Path(args.out).write_text(json.dumps({"counts": dict(counts), "results": results}, indent=1),
                              encoding="utf-8")
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
