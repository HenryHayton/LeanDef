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

# Candidates are full DECLARATIONS, matching what the prelim prompt asks models for and what
# 1040 of 1040 extractable field candidates actually are.
VERBATIM = "def VTask.clog (b n : ℕ) : ℕ := Nat.clog b n"
# Floor+1 where the truth is ceiling: differs exactly on the powers of the base.
WRONG = "def VTask.clog (b n : ℕ) : ℕ := Nat.log b n + 1"
# Compiles as Lean, but is not the pinned type -- the WRONG_TYPE population.
WRONG_ARITY = "def VTask.clog (b : ℕ) : ℕ := b"
WRONG_RESULT = "def VTask.clog (b n : ℕ) : Prop := b = n"
# A bare alias: `full_name` reports the TARGET, which used to read as a phantom second
# declaration. Scored, not rejected, since 2026-08-05 (deferred.md trigger fired).
BARE_ALIAS = "def VTask.clog : (b n : ℕ) -> ℕ := Nat.clog"
NONCOMPUTABLE = "noncomputable def VTask.clog (b n : ℕ) : ℕ := Nat.log b n + 1"
WITH_ATTRIBUTE = "@[simp] def VTask.clog (b n : ℕ) : ℕ := Nat.clog b n"

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
    record = score_candidate_body(server, env, CLOG, "def VTask.clog := this is not lean", [FACT_TRUE], budgets=FAST)

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


# --- declaration-verbatim splicing (2026-08-05) ---------------------------------------------------


def test_wrong_arity_is_wrong_type_not_compile_error(mathlib_env):
    """`WRONG_TYPE` is its own failure kind: Stage F's funnel needs "valid Lean, wrong type"
    separated from "broken Lean". Under construction-based splicing this case was impossible --
    the harness wrote the signature -- so the check only became necessary once the candidate
    started supplying its own."""
    server, env = mathlib_env
    record = score_candidate_body(server, env, CLOG, WRONG_ARITY, [FACT_TRUE], budgets=FAST)

    assert not record["admissible"]
    assert record["admissibility_failure"] == "wrong_type"
    assert "pinned type" in record["admissibility_detail"]
    assert record["fact_verdicts"] == []


def test_wrong_result_type_is_also_wrong_type(mathlib_env):
    server, env = mathlib_env
    record = score_candidate_body(server, env, CLOG, WRONG_RESULT, [FACT_TRUE], budgets=FAST)
    assert record["admissibility_failure"] == "wrong_type"


def test_broken_lean_is_still_compile_error_not_wrong_type(mathlib_env):
    """The two failure kinds must stay distinguishable in the funnel."""
    server, env = mathlib_env
    record = score_candidate_body(server, env, CLOG, "def VTask.clog := ???", [FACT_TRUE], budgets=FAST)
    assert record["admissibility_failure"] == "compile_error"


def test_a_noncomputable_candidate_is_admissible_and_scores(mathlib_env):
    """`noncomputable` is load-bearing and must survive verbatim splicing.

    This is also the regression guarding the type probe's form: `example : T := VTask.clog`
    COMPILES the definition and so fails every noncomputable candidate with "consider marking it
    as 'noncomputable'". `#check (VTask.clog : T)` only elaborates. Had the probe used the
    `example` form, every classical-construction candidate would have been recorded WRONG_TYPE.
    """
    server, env = mathlib_env
    record = score_candidate_body(server, env, CLOG, NONCOMPUTABLE, [FACT_TRUE], budgets=FAST)

    assert record["admissible"], record["admissibility_detail"]
    assert record["fact_verdicts"], "a noncomputable candidate must still be scored"


def test_reducible_takes_effect_through_the_declaration_path(mathlib_env):
    """`@[reducible]` is why a `Decidable` instance resolves THROUGH the splice (the `Nat.ModEq`
    case that motivated it). Verbatim splicing must not lose it: a Prop-valued candidate whose
    decidability comes from unfolding the definition has to remain decide-able."""
    modeq = PinnedSignature(name="VTask.ModEq", type_sig="(n a b : ℕ) -> Prop")
    fact = Fact(
        id="modeq_1_4_mod_3", type="casework", mechanism="decide",
        statement="example : VTask.ModEq 3 1 4 := by decide",
        domain_inputs={"n": ["3"]}, anchors=[],
    )
    server, env = mathlib_env
    record = score_candidate_body(
        server, env, modeq, "def VTask.ModEq (n a b : ℕ) : Prop := a % n = b % n", [fact], budgets=FAST
    )

    assert record["admissible"], record["admissibility_detail"]
    # If `@[reducible]` were lost, this would be UNKNOWN (no Decidable instance through the splice).
    assert [fv["verdict"] for fv in record["fact_verdicts"]] == ["pass"], record["fact_verdicts"]


def test_a_model_supplied_attribute_is_preserved_by_merging(mathlib_env):
    """`@[reducible] @[simp] def` is a Lean syntax error; `@[reducible, simp] def` is not. The
    model's own attributes are merged, not stacked."""
    server, env = mathlib_env
    record = score_candidate_body(server, env, CLOG, WITH_ATTRIBUTE, [FACT_TRUE], budgets=FAST)
    assert record["admissible"], record["admissibility_detail"]


def test_a_bare_alias_candidate_is_scored_not_rejected(mathlib_env):
    """The deferred-trigger decision (2026-08-05): verbatim recall is the memorization population
    we measure, not tampering. Rejecting it as NAME_SHADOWED would misclassify a correct answer
    as inadmissible, and it lands precisely on the RECALLED_TARGET slice."""
    server, env = mathlib_env
    record = score_candidate_body(server, env, CLOG, BARE_ALIAS, [FACT_TRUE], budgets=FAST)

    assert record["admissible"], record["admissibility_detail"]
    assert [fv["verdict"] for fv in record["fact_verdicts"]] == ["pass"]


def test_a_second_declaration_is_still_rejected(mathlib_env):
    """Name enforcement carries more weight now that construction no longer guarantees it."""
    server, env = mathlib_env
    smuggled = f"{VERBATIM}\n\ntheorem VTask.sneaky : 1 = 1 := rfl"
    record = score_candidate_body(server, env, CLOG, smuggled, [FACT_TRUE], budgets=FAST)
    assert not record["admissible"]
    assert record["admissibility_failure"] == "name_shadowed"


def test_a_declaration_of_the_wrong_name_is_rejected(mathlib_env):
    server, env = mathlib_env
    record = score_candidate_body(
        server, env, CLOG, "def VTask.somethingElse (b n : ℕ) : ℕ := 0", [FACT_TRUE], budgets=FAST
    )
    assert not record["admissible"]
    assert record["admissibility_failure"] == "name_shadowed"


# --- universe-variable type probe (2026-08-06 regression) ------------------------------------------


def test_universe_names_are_extracted_but_not_the_wildcard():
    from harness.admissibility import universe_names

    assert universe_names("{α : Type u} -> {β : Type v} -> Prop") == ["u", "v"]
    assert universe_names("{α : Sort u_1} -> {β : Type u_1} -> Prop") == ["u_1"]  # deduped, ordered
    assert universe_names("(b n : ℕ) -> ℕ") == []
    assert universe_names("{α : Type*} -> Prop") == []  # a wildcard, not a named universe


def test_a_universe_polymorphic_candidate_is_admissible(mathlib_env):
    """THE regression. A bare `#check (name : type)` does not bind the universe variables a
    `def` auto-binds, so the probe failed with "unknown universe level `u`" and rejected
    perfectly correct candidates as WRONG_TYPE.

    Measured before the fix: 7 of 7 `Monotone` candidates rejected, and 32 of the 41 tasks carry
    universe variables -- so this would have manufactured false WRONG_TYPE across 78% of the
    corpus and read as a model failure rather than a harness one.
    """
    server, env = mathlib_env
    sig = PinnedSignature(
        name="VTask.Monotone",
        type_sig="{α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> Prop",
    )
    decl = ("def VTask.Monotone {α : Type*} {β : Type*} [Preorder α] [Preorder β] (f : α → β) : Prop := "
            "∀ a b : α, a ≤ b → f a ≤ f b")
    record = score_candidate_body(server, env, sig, decl, [], budgets=FAST)

    assert record["admissible"], record["admissibility_detail"]
    assert record["admissibility_failure"] is None


def test_a_genuinely_wrong_type_is_still_rejected_under_universe_binding(mathlib_env):
    """The fix must not blunt the check: binding the universes cannot make a mismatch pass."""
    server, env = mathlib_env
    sig = PinnedSignature(
        name="VTask.Monotone",
        type_sig="{α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> Prop",
    )
    record = score_candidate_body(
        server, env, sig, "def VTask.Monotone (n : ℕ) : ℕ := n", [], budgets=FAST
    )
    assert not record["admissible"]
    assert record["admissibility_failure"] == "wrong_type"


def test_iff_is_only_for_a_bare_prop_not_a_predicate_with_arguments():
    """`↔` relates propositions. A predicate taking arguments is a FUNCTION returning Prop, so the
    `↔` form is ill-typed and Lean rejects it before any tactic runs -- which silently disabled
    tier-4 equivalence for most of the predicate corpus."""
    from harness.signature import PinnedSignature
    from scoring.candidate import equivalence_uses_iff, is_prop_valued

    predicate = PinnedSignature(name="VTask.ModEq", type_sig="(n a b : ℕ) -> Prop")
    bare = PinnedSignature(name="VTask.P", type_sig="Prop")
    data = PinnedSignature(name="VTask.clog", type_sig="(b n : ℕ) -> ℕ")

    assert is_prop_valued(predicate) and not equivalence_uses_iff(predicate)
    assert is_prop_valued(bare) and equivalence_uses_iff(bare)
    assert not is_prop_valued(data) and not equivalence_uses_iff(data)
