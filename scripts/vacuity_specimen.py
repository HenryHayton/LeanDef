"""Score deliberately VACUOUS candidates through the standard pipeline.

    SCORING_SCORES_DIR=scoring_output/vacuity_specimens \
    uv run python scripts/vacuity_specimen.py

`def VTask.P ... : Prop := True` is the failure mode the reward doc names first: it denotes
nothing, yet every positively-phrased fact about it holds trivially. The corpus currently has
17 of 41 tasks with no reject-polarity fact at all, including the Prop-valued `Monotone` and
`DependsOn` -- so the prediction is fidelity 1.000 with full resolution.

This runs the REAL scorer (`scoring.candidate.score_candidate_body`), not a bespoke path, so the
result is directly comparable to every other verdict in the corpus. Whatever comes back is the
calibration point for the near-miss gate: if a fact does catch a vacuous candidate, knowing WHICH
one and WHY is more valuable than the headline.
"""

import json
import sys
from pathlib import Path

from harness.repl import get_warm_environment
from harness.results import CheckStatus
from scoring import config as cfg
from scoring.candidate import score_candidate_body
from scoring.samples import load_task
from scoring.verdicts import Verdict, fidelity, resolution_rate

# Binders are supplied so the body typechecks against the pinned signature; the point is that the
# BODY ignores every one of them.
SPECIMENS = {
    "Monotone": "def VTask.Monotone {α : Type u} {β : Type v} [Preorder α] [Preorder β] "
                "(_f : α → β) : Prop := True",
    "DependsOn": "def VTask.DependsOn {ι : Type u_1} {α : ι → Type u_2} {β : Type u_3} "
                 "(_f : ((i : ι) → α i) → β) (_s : Set ι) : Prop := True",
}


def main() -> int:
    out_dir = Path("scoring_output/vacuity_specimens")
    out_dir.mkdir(parents=True, exist_ok=True)
    server, base = get_warm_environment()
    if base.status is not CheckStatus.PASSED:
        raise RuntimeError(base.detail)

    summary = {}
    for task_name, body in SPECIMENS.items():
        t = load_task(task_name)
        print("=" * 96)
        print(f"TASK {task_name}   (truth = {t.get('truth_real_name')})")
        print(body)
        rec = score_candidate_body(
            server, base.env, t["signature"], body, t["facts"],
            truth_real_name=t.get("truth_real_name"),
            try_equivalence=True, imports=t.get("imports"),
        )
        rec.update(model_slug="VACUOUS_SPECIMEN", task_name=task_name, sample_index=0,
                   extracted_code=body)
        verdicts = [Verdict((f.get("verdict") or "unknown").lower())
                    for f in (rec.get("fact_verdicts") or [])]
        fid = fidelity(verdicts) if verdicts else None
        res = resolution_rate(verdicts) if verdicts else None
        rec["fidelity"], rec["resolution_rate"] = fid, res

        print(f"\n  admissible = {rec.get('admissible')}"
              f"   failure = {rec.get('admissibility_failure')}"
              f"   equivalence_certified = {rec.get('equivalence_certified')}")
        print(f"  {'fact_id':<44}{'verdict':<10}{'tier':<6}mechanism")
        for fv in (rec.get("fact_verdicts") or []):
            print(f"  {fv['fact_id']:<44}{(fv.get('verdict') or ''):<10}"
                  f"{str(fv.get('tier') or ''):<6}{fv.get('mechanism') or ''}")
        print(f"\n  FIDELITY = {fid}   RESOLUTION = {res}")
        (out_dir / f"{task_name}.json").write_text(
            json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        summary[task_name] = {
            "admissible": rec.get("admissible"), "fidelity": fid, "resolution_rate": res,
            "n_facts": len(rec.get("fact_verdicts") or []),
            "passed": sum(1 for v in verdicts if v is Verdict.PASS),
            "failed": sum(1 for v in verdicts if v is Verdict.FAIL),
            "unknown": sum(1 for v in verdicts if v is Verdict.UNKNOWN),
        }
    server.kill()
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print("\n" + json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
