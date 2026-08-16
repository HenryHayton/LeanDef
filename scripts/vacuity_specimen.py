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
#
# `expect_fail` is the KNOWN ANSWER, and it is what makes this a test of the instrument rather than
# an observation about a definition. Facts are named explicitly rather than counted, so a suite that
# is edited later fails loudly here instead of quietly changing what was proved.
SPECIMENS = {
    # The original two. Both are Prop tasks with NO reject-polarity fact at all, so nothing in
    # either suite can refute a vacuous body: fidelity 1.000 is the correct, uninformative answer.
    # Kept as the negative control -- they show the probe does not manufacture failures.
    # NOTE: these live in a different task batch and are absent from `tasks_batch200`; the runner
    # skips specimens whose task is not present rather than aborting the whole probe.
    "monotone_vacuous": ("Monotone", [],
                         "def VTask.Monotone {α : Type u} {β : Type v} [Preorder α] [Preorder β] "
                         "(_f : α → β) : Prop := True"),
    "dependson_vacuous": ("DependsOn", [],
                          "def VTask.DependsOn {ι : Type u_1} {α : ι → Type u_2} {β : Type u_3} "
                          "(_f : ((i : ι) → α i) → β) (_s : Set ι) : Prop := True"),

    # The CONTRAST specimens. Both carry many certified reject facts, but every one is adjudicated
    # by the `proof` mechanism -- which `scoring.verdicts` forbids from returning FAIL, on the
    # grounds that a tactic failing to prove something is not a refutation of it. A vacuous body
    # should therefore come back UNKNOWN here, not FAIL, no matter how wrong it is. These make the
    # ceiling visible: reject facts alone do not buy refutation, decidable reject facts do.
    "xor_vacuous": ("Xor", [], "def VTask.Xor (_a _b : Prop) : Prop := True"),
    "set_nontrivial_vacuous": ("Set.Nontrivial", [],
                               "def VTask.Nontrivial {α : Type u} (_s : Set α) : Prop := True"),

    # THE DECISIVE ONE. `Nat.FermatPsp` carries four CERTIFIED reject facts adjudicated by tier-1
    # `decide` -- and tier-1 decide is the only mechanism `scoring.verdicts` permits to return FAIL.
    # With the body `True`, each reject fact `example : ¬VTask.FermatPsp n b := by decide` becomes
    # `¬True`, which the kernel evaluates to false. If these four do not come back FAIL, the
    # instrument cannot produce a FAIL at all and every zero-FAIL result elsewhere is an artifact.
    "fermatpsp_vacuous": ("Nat.FermatPsp",
                          ["fermatpsp_7_2_reject_prime", "fermatpsp_4_2_reject_probable_prime",
                           "fermatpsp_1_1_reject_lower_bound", "fermatpsp_0_0_reject_lower_bound"],
                          "def VTask.FermatPsp (_n _b : ℕ) : Prop := True"),

    # The opposite pole, on the same suite. An EMPTY definition refutes every mutant and fails the
    # positive facts -- the mirror image of the vacuous one. Running both against one suite is what
    # shows the two-sided design works in both directions rather than just being hard to satisfy.
    #
    # The expected failures are the two DECIDE-mechanism accept facts. An earlier version of this
    # entry expected `fermatpsp_base_one_all_composites` instead, which is a `proof` fact -- and
    # proof facts are forbidden from returning FAIL by `scoring.verdicts`, so that expectation could
    # never have been met by a working instrument. The probe duly reported INSTRUMENT BROKEN, which
    # was a bad prediction rather than a bad scorer. Expectations here must name decidable facts.
    "fermatpsp_empty": ("Nat.FermatPsp", ["fermatpsp_4_1_accept", "fermatpsp_9_1_accept"],
                        "def VTask.FermatPsp (_n _b : ℕ) : Prop := False"),
}


def main() -> int:
    out_dir = Path("scoring_output/vacuity_specimens")
    out_dir.mkdir(parents=True, exist_ok=True)
    server, base = get_warm_environment()
    if base.status is not CheckStatus.PASSED:
        raise RuntimeError(base.detail)

    summary = {}
    for specimen_id, (task_name, expect_fail, body) in SPECIMENS.items():
        try:
            t = load_task(task_name)
        except FileNotFoundError:
            # Task batches differ between machines. Skipping is right for a probe whose specimens
            # are independent; aborting would lose the decisive ones to an absent control.
            print(f"SKIP {specimen_id}: task {task_name} not in this task root")
            summary[specimen_id] = {"task": task_name, "instrument": "SKIPPED_TASK_ABSENT"}
            continue
        print("=" * 96)
        print(f"SPECIMEN {specimen_id}   TASK {task_name}   (truth = {t.get('truth_real_name')})")
        print(body)
        if expect_fail:
            print(f"  KNOWN ANSWER: these must come back FAIL -> {', '.join(expect_fail)}")
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

        # Adjudicate the INSTRUMENT against the known answer, not the definition against the facts.
        got = {fv["fact_id"]: (fv.get("verdict") or "").lower()
               for fv in (rec.get("fact_verdicts") or [])}
        missed = [f for f in expect_fail if got.get(f) != "fail"]
        verdict_on_instrument = "INCONCLUSIVE" if not expect_fail else (
            "INSTRUMENT OK" if not missed else "INSTRUMENT BROKEN")
        if expect_fail:
            print(f"  KNOWN-ANSWER CHECK: {verdict_on_instrument}")
            for f in expect_fail:
                print(f"     {f:<44}expected fail, got {got.get(f, '<absent>')}")

        (out_dir / f"{specimen_id}.json").write_text(
            json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        summary[specimen_id] = {
            "task": task_name,
            "admissible": rec.get("admissible"), "fidelity": fid, "resolution_rate": res,
            "n_facts": len(rec.get("fact_verdicts") or []),
            "passed": sum(1 for v in verdicts if v is Verdict.PASS),
            "failed": sum(1 for v in verdicts if v is Verdict.FAIL),
            "unknown": sum(1 for v in verdicts if v is Verdict.UNKNOWN),
            "expected_fail": expect_fail,
            "expected_fail_not_delivered": missed,
            "instrument": verdict_on_instrument,
        }
    server.kill()
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print("\n" + json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
