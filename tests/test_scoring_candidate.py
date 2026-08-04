"""End-to-end scoring of one candidate against live Mathlib (Stage B).

The vehicle is `Nat.clog`, whose real suite carries both mechanisms (21 decide, 8 proof), so the
dispatch, the verdict mapping and the tier-1 semantics fix are all exercised on real data rather
than on statements invented for the test.

**The load-bearing test in this file is the adversarial one.** The equivalence fast path requires
the truth definition to be co-resident with the candidate in one environment. If a fact could
resolve against the truth instead of the candidate, every candidate would score perfectly and
the entire measurement would be worthless -- and it would look like success, which is the
dangerous kind of wrong. `test_wrong_candidate_still_fails_its_facts_with_truth_co_resident`
scores a deliberately wrong candidate with the truth present and requires the facts to fail.
"""

import pytest

from harness.facts import Fact
from harness.signature import PinnedSignature
from ladder.budgets import DEFAULT_LADDER_BUDGETS, LadderBudgets, TacticBudget
from scoring.candidate import (
    CERTIFIED_VIA_EQUIVALENCE,
    CERTIFIED_VIA_FACT,
    is_prop_valued,
    score_candidate_body,
    truth_signature_for,
)
from scoring.verdicts import DECIDE, PROOF, Verdict, check_mechanism_invariant

CLOG = PinnedSignature(name="VTask.clog", type_sig="(b n : ℕ) -> ℕ")
TRUTH = "Nat.clog"

# The real definition as a candidate would express it. Eta-expanded, NOT the bare alias
# `_root_.Nat.clog`: a bare alias deliberately trips the admissibility shadowing check, which is
# how this repo currently declines to score a verbatim copy as a definition (docs/deferred.md,
# "bare-alias candidate bodies ... rather than being scored as memorization", trigger: mini-trial
# design). Eta-expanded is still definitionally equal to the truth, so the equivalence fast path
# closes it by `rfl` exactly as a genuine near-verbatim candidate would.
VERBATIM = "fun b n => Nat.clog b n"
# Off by one: agrees nowhere interesting. `clog 2 8 = 3` becomes 4.
WRONG = "fun b n => Nat.log b n + 1"

# Real decide facts from prelim_testing/tasks/Nat.clog/task.json.
FACT_TRUE = Fact(
    id="clog_casework_2_8", type="casework", mechanism="decide",
    statement="example : VTask.clog 2 8 = 3 := by decide",
    domain_inputs={"b": ["2"], "n": ["8"]}, anchors=[],
)
FACT_TRUE_2 = Fact(
    id="clog_casework_1_1", type="casework", mechanism="decide",
    statement="example : VTask.clog 2 1 = 0 := by decide",
    domain_inputs={"b": ["2"], "n": ["1"]}, anchors=[],
)
# A fact the WRONG candidate happens to satisfy: floor+1 and ceiling agree off the powers of
# the base, so this is what makes a PARTIAL score testable rather than an all-or-nothing one.
FACT_WRONG_AGREES = Fact(
    id="clog_casework_2_5", type="casework", mechanism="decide",
    statement="example : VTask.clog 2 5 = 3 := by decide",
    domain_inputs={"b": ["2"], "n": ["5"]}, anchors=[],
)
# Undecidable as stated -- no `Decidable` instance for an unbounded forall.
FACT_NO_INSTANCE = Fact(
    id="clog_undecidable", type="casework", mechanism="decide",
    statement="example : ∀ n : ℕ, VTask.clog 2 n = VTask.clog 2 n := by decide",
    domain_inputs={"n": ["0"]}, anchors=[],
)
# Names a symbol that does not exist -- a broken splice, not a refutation.
FACT_BROKEN = Fact(
    id="clog_broken_ref", type="casework", mechanism="decide",
    statement="example : VTask.noSuchThing 2 8 = 3 := by decide",
    domain_inputs={"b": ["2"]}, anchors=[],
)
FACT_PROOF = Fact(
    id="clog_global_monotone", type="global", mechanism="proof",
    statement="∀ b : ℕ, Monotone (VTask.clog b)",
    domain_inputs={}, anchors=["Nat.clog_monotone"],
)

# Keep proof search short: these tests are about dispatch and mapping, not about how clever the
# tactic ladder is. The real budgets are what the pilot measures.
FAST = LadderBudgets(tier2_tactics=(TacticBudget("rfl", 3.0), TacticBudget("simp", 5.0)))


# --- pure helpers ------------------------------------------------------------------------------


def test_truth_symbol_differs_from_the_task_symbol():
    """The whole inertness argument rests on this."""
    truth = truth_signature_for(CLOG)
    assert truth.name == "VTruth.clog"
    assert truth.name != CLOG.name
    assert truth.type_sig == CLOG.type_sig


def test_prop_valued_detection():
    assert not is_prop_valued(CLOG)
    assert is_prop_valued(PinnedSignature(name="VTask.Monotone", type_sig="(f : ℕ → ℕ) -> Prop"))


# --- the equivalence fast path ------------------------------------------------------------------


def test_verbatim_candidate_is_certified_by_equivalence(mathlib_env):
    """One `rfl` certifies the whole suite. This is the case the 12 RECALLED_TARGET tasks make
    common, and the reason the fast path is worth its complexity."""
    server, env = mathlib_env
    record = score_candidate_body(
        server, env, CLOG, VERBATIM, [FACT_TRUE, FACT_PROOF], truth_real_name=TRUTH, budgets=FAST
    )

    assert record["admissible"], record["admissibility_detail"]
    assert record["equivalence_attempted"]
    assert record["equivalence_certified"], record.get("equivalence_attempts")
    assert record["fidelity"] == 1.0
    assert {fv["certified_via"] for fv in record["fact_verdicts"]} == {CERTIFIED_VIA_EQUIVALENCE}
    assert all(fv["verdict"] == "pass" for fv in record["fact_verdicts"])
    # It certified the PROOF fact too, without ever running the ladder -- that is the payoff.
    assert any(fv["mechanism"] == PROOF for fv in record["fact_verdicts"])


def test_wrong_candidate_does_not_get_certified_by_equivalence(mathlib_env):
    server, env = mathlib_env
    record = score_candidate_body(
        server, env, CLOG, WRONG, [FACT_TRUE], truth_real_name=TRUTH, budgets=FAST
    )
    assert record["equivalence_attempted"]
    assert not record["equivalence_certified"]


# --- THE adversarial test ------------------------------------------------------------------------


def test_wrong_candidate_still_fails_its_facts_with_truth_co_resident(mathlib_env):
    """Inertness. The truth is present in the same environment; the facts name `VTask.clog` and
    must resolve to the CANDIDATE, so a wrong candidate must still be refuted.

    If this ever fails, the equivalence fast path is unsound and must be removed: every
    candidate would score perfectly and the whole measurement would be worthless.
    """
    server, env = mathlib_env
    record = score_candidate_body(
        server, env, CLOG, WRONG, [FACT_TRUE], truth_real_name=TRUTH, budgets=FAST
    )

    assert record["admissible"], record["admissibility_detail"]
    assert not record["equivalence_certified"]
    verdicts = [fv["verdict"] for fv in record["fact_verdicts"]]
    assert verdicts == ["fail"], record["fact_verdicts"]
    assert record["fidelity"] == 0.0


def test_the_same_wrong_candidate_fails_identically_without_truth_present(mathlib_env):
    """Control for the test above: co-residence must not change the verdict either way."""
    server, env = mathlib_env
    with_truth = score_candidate_body(
        server, env, CLOG, WRONG, [FACT_TRUE], truth_real_name=TRUTH, budgets=FAST
    )
    without = score_candidate_body(server, env, CLOG, WRONG, [FACT_TRUE], budgets=FAST)

    assert [fv["verdict"] for fv in with_truth["fact_verdicts"]] == [
        fv["verdict"] for fv in without["fact_verdicts"]
    ]
    assert not without["equivalence_attempted"]


def test_correct_candidate_passes_its_facts_on_the_per_fact_path(mathlib_env):
    """Equivalence disabled, so the facts are genuinely evaluated against the candidate."""
    server, env = mathlib_env
    record = score_candidate_body(server, env, CLOG, VERBATIM, [FACT_TRUE, FACT_TRUE_2], budgets=FAST)

    assert [fv["verdict"] for fv in record["fact_verdicts"]] == ["pass", "pass"]
    assert {fv["certified_via"] for fv in record["fact_verdicts"]} == {CERTIFIED_VIA_FACT}
    assert record["fidelity"] == 1.0


# --- tier-1 semantics reaching the verdict layer ---------------------------------------------------


def test_undecidable_fact_is_unknown_and_leaves_fidelity_unscored(mathlib_env):
    """The tier-1 fix, end to end. Before it, this was a refutation -- and with only this fact
    the candidate would have scored 0.0 fidelity instead of being correctly unscored."""
    server, env = mathlib_env
    record = score_candidate_body(server, env, CLOG, VERBATIM, [FACT_NO_INSTANCE], budgets=FAST)

    assert [fv["verdict"] for fv in record["fact_verdicts"]] == ["unknown"]
    assert record["fidelity"] is None


def test_broken_fact_reference_is_error_not_refutation(mathlib_env):
    server, env = mathlib_env
    record = score_candidate_body(server, env, CLOG, VERBATIM, [FACT_BROKEN], budgets=FAST)

    assert [fv["verdict"] for fv in record["fact_verdicts"]] == ["error"]
    assert record["fidelity"] is None


def test_mixed_suite_computes_fidelity_over_resolved_facts_only(mathlib_env):
    """A partial score with an UNKNOWN and an ERROR present: both must vanish from the
    denominator rather than counting either way.

    `WRONG` is `Nat.log b n + 1`, i.e. floor+1 where the truth is ceiling. Those differ exactly
    on the powers of the base and agree elsewhere -- so `clog 2 8 = 3` fails (it yields 4) while
    `clog 2 5 = 3` passes (floor 2, +1 = 3; ceiling is also 3). One of two resolved facts passes.
    """
    server, env = mathlib_env
    record = score_candidate_body(
        server, env, CLOG, WRONG, [FACT_TRUE, FACT_WRONG_AGREES, FACT_NO_INSTANCE, FACT_BROKEN], budgets=FAST
    )
    verdicts = [fv["verdict"] for fv in record["fact_verdicts"]]

    assert verdicts.count("unknown") == 1
    assert verdicts.count("error") == 1
    assert verdicts.count("fail") == 1
    assert verdicts.count("pass") == 1
    assert record["fidelity"] == pytest.approx(0.5)


# --- proof facts through the real ladder ------------------------------------------------------------


def test_proof_fact_goes_through_the_ladder_and_never_reaches_fail(mathlib_env):
    """`run_facts` raises `NotImplementedError` here; this path is what replaces it. Whatever the
    tactics manage, the invariant holds: a proof fact is PASS, UNKNOWN or ERROR, never FAIL."""
    server, env = mathlib_env
    record = score_candidate_body(server, env, CLOG, VERBATIM, [FACT_PROOF], budgets=FAST)

    fv = record["fact_verdicts"][0]
    assert fv["mechanism"] == PROOF
    assert fv["verdict"] in {"pass", "unknown", "error"}
    assert fv["verdict"] != "fail"
    check_mechanism_invariant(PROOF, Verdict(fv["verdict"]))


def test_tier_attempts_are_persisted_for_timing_calibration(mathlib_env):
    """The pilot's per-tactic timing data has to collect itself, so losing attempts are kept."""
    server, env = mathlib_env
    record = score_candidate_body(server, env, CLOG, VERBATIM, [FACT_PROOF], budgets=FAST)

    attempts = record["fact_verdicts"][0]["attempts"]
    assert isinstance(attempts, list)
    for attempt in attempts:
        assert {"tier", "status", "elapsed_s"} <= set(attempt)


# --- candidates that never get scored are still recorded ---------------------------------------------


def test_a_non_compiling_candidate_yields_a_record_not_an_exception(mathlib_env):
    server, env = mathlib_env
    record = score_candidate_body(server, env, CLOG, "this is not lean at all", [FACT_TRUE], budgets=FAST)

    assert not record["admissible"]
    assert record["admissibility_failure"] == "compile_error"
    assert record["admissibility_detail"]
    assert record["fact_verdicts"] == []
    assert record["fidelity"] is None


def test_splice_path_is_recorded_for_a_plain_candidate(mathlib_env):
    server, env = mathlib_env
    record = score_candidate_body(server, env, CLOG, VERBATIM, [FACT_TRUE], budgets=FAST)
    assert record["splice_path"] == "plain"
    assert record["splice_retries"] == 0


def test_every_fact_verdict_satisfies_the_mechanism_invariant_on_real_data(mathlib_env):
    """Belt and braces over a mixed real suite -- the invariant is enforced in the scorer, so
    this asserts the scorer actually ran it rather than trusting that it did."""
    server, env = mathlib_env
    record = score_candidate_body(
        server, env, CLOG, WRONG, [FACT_TRUE, FACT_NO_INSTANCE, FACT_PROOF], budgets=DEFAULT_LADDER_BUDGETS
        if False else FAST,
    )
    for fv in record["fact_verdicts"]:
        check_mechanism_invariant(fv["mechanism"], Verdict(fv["verdict"]))
        assert fv["mechanism"] in (DECIDE, PROOF)
