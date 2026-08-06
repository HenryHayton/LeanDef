"""Calibration: re-run the prelim's known names-the-target survivors through SELF_DELEGATION.

These 22 candidates are the population the gate was built for -- prelim survivors whose extracted
body names the mined Mathlib target outright (`def VTask.choose := Nat.choose`). They were scored
ADMITTED and counted as survivors, because at the time nothing distinguished "constructed the
object" from "invoked the object". Every one of them must now trip.

This is a free, fully-labelled calibration set: the expected verdict is known for all 22 without
anyone hand-labelling anything, and a gate that misses any of them is under-matching while a gate
that trips on a non-member is over-matching. Both directions are reported.

    uv run python scripts/self_delegation_calibration.py

**Historical verdicts are NOT rewritten.** The check applies to this smoke and everything after;
the prelim's survivor counts predate it and stay as recorded. This script only re-splices and
re-asks, writing its own report.
"""

import argparse
import collections
import json
import sys
from pathlib import Path

from authoring.namematch import name_occurs
from harness.admissibility import AdmissibilityFailure, check_admissibility
from harness.scoring import splice_candidate_declaration
from harness.results import CheckStatus
from scoring.runner import ServerHandle
from scoring.samples import load_task


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scores", default="scoring_output/scores")
    ap.add_argument("--out", default="scoring_output/self_delegation_calibration.json")
    args = ap.parse_args()

    # The labelled set: admissible prelim candidates whose own source names the mined target.
    # Source-text matching is the right selector HERE (it is how the population was originally
    # characterised); the gate itself then re-derives the answer from the elaborated closure,
    # which is the independent check.
    named, other_admissible = [], []
    for path in sorted(Path(args.scores).rglob("sample_*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        if not rec.get("admissible"):
            continue
        task = rec["task_name"]
        code = rec.get("extracted_code") or ""
        real = load_task(task).get("truth_real_name")
        if not real or not code:
            continue
        (named if name_occurs(code, real) else other_admissible).append(
            {"task": task, "model": rec.get("model_slug"), "idx": rec.get("sample_index"),
             "code": code, "real": real, "equiv": rec.get("equivalence_certified")}
        )

    print(f"labelled set: {len(named)} admissible candidates name their target "
          f"({len(other_admissible)} admissible candidates do not)\n")

    handle = ServerHandle()
    # `closure_only` is NOT an over-match bucket. The labelled set is selected by SOURCE TEXT,
    # which cannot see dot notation: `n.divisors` elaborates to `Nat.divisors` while containing
    # no such substring. A closure-only catch is therefore the gate finding a delegation the
    # labelling missed -- the case that motivated checking the closure instead of the source.
    # Each entry still needs eyeballing; genuine over-matching would show up here too.
    results = {"tripped": [], "missed": [], "unspliceable": [], "closure_only": []}
    try:
        for group, expect_trip in ((named, True), (other_admissible, False)):
            for c in group:
                t = load_task(c["task"])
                server, env = handle.get()
                outcome = splice_candidate_declaration(server, env, t["signature"], c["code"])
                if outcome.result.status is not CheckStatus.PASSED:
                    if expect_trip:
                        results["unspliceable"].append(
                            {**c, "why": (outcome.result.detail or "")[:200]})
                    continue
                verdict = check_admissibility(
                    server, outcome.result.env, t["signature"], splice_response=None,
                    target_real_name=c["real"],
                )
                tripped = verdict.failure is AdmissibilityFailure.SELF_DELEGATION
                entry = {k: c[k] for k in ("task", "model", "idx", "real", "equiv")}
                entry["detail"] = verdict.detail[:200]
                if expect_trip and tripped:
                    results["tripped"].append(entry)
                elif expect_trip and not tripped:
                    results["missed"].append(entry)
                elif not expect_trip and tripped:
                    entry["code"] = c["code"]
                    results["closure_only"].append(entry)
    finally:
        handle.close()

    n_named = len(named)
    print(f"{'=' * 78}\nCALIBRATION\n{'=' * 78}")
    print(f"  tripped        {len(results['tripped'])}/{n_named}")
    print(f"  missed         {len(results['missed'])}   <- under-matching")
    print(f"  unspliceable   {len(results['unspliceable'])}   (could not re-splice; not a verdict)")
    print(f"  closure-only   {len(results['closure_only'])}/{len(other_admissible)}"
          f"   <- caught via the elaborated closure; source text did not name the target")
    for m in results["missed"]:
        print(f"    MISSED {m['model']}/{m['task']}#{m['idx']} target={m['real']}")
    for f in results["closure_only"]:
        print(f"    CLOSURE-ONLY {f['model']}/{f['task']}#{f['idx']} target={f['real']}")
        print(f"      code: {' '.join(f['code'].split())[:120]}")

    by_task = collections.Counter(t["task"] for t in results["tripped"])
    print(f"\n  tripped by task: {dict(by_task.most_common())}")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(
        {"n_named": n_named, "n_other_admissible": len(other_admissible),
         **{k: v for k, v in results.items()}}, indent=1), encoding="utf-8")
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
