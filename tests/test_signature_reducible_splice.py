"""Regression coverage for the 2026-07-30 `@[reducible]` splice fix
(`harness.signature.PinnedSignature.splice`, `docs/design/llm_io_contract_v1.md` §4.4).

Real Mathlib REPL throughout (module-scoped `mathlib_env`, same pattern as
`tests/test_authoring_pipeline.py`) -- the whole point of this fix is instance-search behavior
that only exists against the real environment; nothing here can be faked with a stub.

Covers, in order: (1) the emitted command text itself; (2) the bug this fix targets, confirmed
fixed (`Nat.ModEq` decidability); (3)+(4) the admissibility shadowing check's declared-name
comparison is unaffected by the new attribute, in BOTH directions -- a normal candidate still
passes, and a bare-alias candidate (`body = Nat.clog` verbatim, no application) still trips it,
which is the one regression this change could plausibly have caused silently; (5)+(6) the
value-typed path (`Nat.clog`) is byte-identical: admissibility, decide facts, and the real
RECALLED_TARGET incident's own failure mode (unbound `b`/`n`) all behave exactly as before.
"""

import pytest
from lean_interact import Command

from authoring.task_symbol import task_symbol_for
from harness import Fact, PinnedSignature, score_candidate
from harness.admissibility import AdmissibilityFailure, check_admissibility
from harness.repl import run_checked
from harness.results import CheckStatus
from harness.scoring import splice_real_name


CLOG_SIG = PinnedSignature(name=task_symbol_for("Nat.clog"), type_sig="Nat -> Nat -> Nat")
CLOG_TRUE_BODY = "fun b n => if b ≤ 1 ∨ n ≤ 1 then 0 else Nat.log b (n - 1) + 1"
CLOG_FACTS = [
    Fact(id="c1", type="casework", mechanism="decide", statement=f"example : {CLOG_SIG.name} 2 8 = 3 := by decide"),
    Fact(id="c2", type="casework", mechanism="decide", statement=f"example : {CLOG_SIG.name} 2 9 = 4 := by decide"),
]

MODEQ_SIG = PinnedSignature(name=task_symbol_for("Nat.ModEq"), type_sig="(n a b : ℕ) -> Prop")


def test_splice_emits_reducible_attribute():
    sig = PinnedSignature(name="X", type_sig="Nat -> Nat")
    assert sig.splice("body") == "@[reducible] def X : Nat -> Nat := body"


def test_modeq_decidable_true_and_false_instances_after_reducible_splice(mathlib_env):
    """The bug this fix targets: `Nat.ModEq`'s `Decidable` instance is keyed to its own head
    symbol (`Mathlib/Data/Nat/ModEq.lean`), invisible to instance search through a plain-`def`
    splice. Confirmed here directly with a true and a false instance, exactly the check the
    real Gate 2 rotation needed and didn't have."""
    server, env = mathlib_env
    splice = run_checked(server, Command(cmd=MODEQ_SIG.splice("Nat.ModEq"), env=env), timeout=30.0)
    assert splice.status is CheckStatus.PASSED, splice.detail

    true_check = run_checked(
        server, Command(cmd=f"example : {MODEQ_SIG.name} 4 7 15 := by decide", env=splice.env), timeout=30.0
    )
    assert true_check.status is CheckStatus.PASSED, true_check.detail

    false_check = run_checked(
        server, Command(cmd=f"example : ¬ {MODEQ_SIG.name} 4 7 12 := by decide", env=splice.env), timeout=30.0
    )
    assert false_check.status is CheckStatus.PASSED, false_check.detail


def test_shadowing_check_unaffected_by_reducible_attribute_normal_candidate(mathlib_env):
    """A normal, well-formed candidate still declares exactly the pinned name -- the
    `@[reducible]` attribute itself must not appear as (or introduce) an extra declaration."""
    server, env = mathlib_env
    cmd = CLOG_SIG.splice(CLOG_TRUE_BODY)
    splice = run_checked(server, Command(cmd=cmd, env=env, declarations=True), timeout=30.0)
    assert splice.status is CheckStatus.PASSED, splice.detail

    verdict = check_admissibility(server, splice.env, CLOG_SIG, splice_response=splice.raw_response, timeout=30.0)
    assert verdict.failure is not AdmissibilityFailure.NAME_SHADOWED, verdict.detail


def test_bare_alias_candidate_is_now_SCORED_not_rejected(mathlib_env):
    """Reversed deliberately on 2026-08-05 (`docs/deferred.md`, trigger "mini-trial design"
    fired at Stage B).

    This test previously asserted the opposite, on the reasoning that a bare-alias body
    (`body = "Nat.clog"`, unapplied) is a verbatim copy and should not silently pass
    admissibility. The mechanism was `full_name` resolving to the alias TARGET, which made the
    declaration look like two declarations. The decision is now to SCORE such candidates:
    verbatim recall is the memorization population the run exists to MEASURE, and recording it
    as inadmissible misclassifies a correct answer as tampering. Measured incidence: 5 of 1040
    extractable prelim candidates, four of them verbatim-correct `Nat.choose` -- concentrated on
    exactly the `RECALLED_TARGET` slice the results table reports on.

    A second declaration, or a declaration of some other name, still fails -- see
    `tests/test_admissibility.py` and `tests/test_scoring_candidate.py`.
    """
    server, env = mathlib_env
    cmd = CLOG_SIG.splice("Nat.clog")  # bare, point-free -- NOT "Nat.clog b n"
    splice = run_checked(server, Command(cmd=cmd, env=env, declarations=True), timeout=30.0)
    assert splice.status is CheckStatus.PASSED, splice.detail

    verdict = check_admissibility(server, splice.env, CLOG_SIG, splice_response=splice.raw_response, timeout=30.0)
    assert verdict.failure is not AdmissibilityFailure.NAME_SHADOWED, verdict.detail


def test_nat_clog_admissibility_and_facts_byte_identical_under_reducible_splice(mathlib_env):
    """The value-typed path (`Nat.clog`) must behave identically to before this fix: a
    decidable-equality fact on the definition's ℕ-valued OUTPUT resolves via a generic instance
    on ℕ (`Nat.decEq`), never needing to unfold the definition's own name -- reducibility was
    never the blocker here, so nothing should change."""
    server, env = mathlib_env
    score = score_candidate(
        server, env, CLOG_SIG, CLOG_TRUE_BODY, CLOG_FACTS, label="clog_true", baseline_axioms=frozenset(
            {"propext", "Classical.choice", "Quot.sound"}
        ),
    )
    assert score.admissible, score.admissibility_detail
    assert score.fidelity == 1.0


def test_nat_clog_recalled_target_body_fails_the_same_way(mathlib_env):
    """The real 2026-07-29 RECALLED_TARGET incident's failure mode (`Nat.clog b n` as a
    round-trip body -- unbound `b`/`n`, since the pinned type is an anonymous arrow, not a
    named-binder Pi type) is a SCOPING problem, unrelated to instance-search reducibility --
    confirmed it still fails the exact same way, not silently fixed as a side effect."""
    server, env = mathlib_env
    cmd = CLOG_SIG.splice("Nat.clog b n")
    splice = run_checked(server, Command(cmd=cmd, env=env, declarations=True), timeout=30.0)
    assert splice.status is CheckStatus.FAILED
    assert "Unknown identifier" in (splice.detail or "")


# === splice_real_name (2026-07-31, the "Harness Fixes" session) ================
#
# Root cause, confirmed by a real 4-name x 3-attribute-variant repro matrix (this session's
# report has the full verbatim output): `Monotone`/`DependsOn` fail truth_splice under EVERY
# attribute variant (plain def, @[reducible] def, abbrev) -- proving @[reducible] was never the
# cause. The real cause: `def VTask.Monotone := Monotone` (bare, unqualified real name) resolves
# the body's `Monotone` to the currently-being-elaborated `VTask.Monotone` itself, since both
# end in `.Monotone` -- a bogus self-reference that fails the termination checker with a
# misleading "well-founded recursion" error. `Function.extend` fails separately: it's
# noncomputable at the alias site even though its own source line has no `noncomputable`
# keyword (confirmed: it uses `open scoped Classical in` internally).


def test_splice_real_name_root_qualifies():
    sig = PinnedSignature(name="VTask.Monotone", type_sig="Nat -> Prop")
    assert sig.splice_real_name("Monotone") == "@[reducible] def VTask.Monotone : Nat -> Prop := _root_.Monotone"


def test_splice_real_name_noncomputable_modifier_ordering():
    """Confirmed empirically (2026-07-31): `@[reducible] noncomputable def` is the only order
    Lean accepts -- `noncomputable @[reducible] def` is a syntax error (attributes must precede
    modifiers)."""
    sig = PinnedSignature(name="VTask.extend", type_sig="Nat -> Nat")
    cmd = sig.splice_real_name("Function.extend", noncomputable=True)
    assert cmd == "@[reducible] noncomputable def VTask.extend : Nat -> Nat := _root_.Function.extend"


@pytest.mark.parametrize(
    "real_name,symbol,pinned_type",
    [
        ("Monotone", "VTask.Monotone", "{α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> Prop"),
        ("DependsOn", "VTask.DependsOn", "{ι : Type u_1} -> {α : ι → Type u_2} -> {β : Type u_3} -> (f : ((i : ι) → α i) → β) -> (s : Set ι) -> Prop"),
    ],
)
def test_root_qualified_truth_splice_fixes_the_self_reference_collision(mathlib_env, real_name, symbol, pinned_type):
    server, env = mathlib_env
    sig = PinnedSignature(name=symbol, type_sig=pinned_type)
    # The OLD (bug-reproducing) shape: bare unqualified real name.
    bare_cmd = sig.splice(real_name)
    bare = run_checked(server, Command(cmd=bare_cmd, env=env), timeout=30.0)
    assert bare.status is CheckStatus.FAILED
    assert "well-founded recursion" in (bare.detail or "")

    # The FIX: root-qualified via splice_real_name.
    fixed = run_checked(server, Command(cmd=sig.splice_real_name(real_name), env=env), timeout=30.0)
    assert fixed.status is CheckStatus.PASSED, fixed.detail


def test_splice_real_name_retries_with_noncomputable_on_the_specific_compiler_error(mathlib_env):
    server, env = mathlib_env
    sig = PinnedSignature(
        name="VTask.extend",
        type_sig="{α : Sort u_1} -> {β : Sort u_2} -> {γ : Sort u_3} -> (f : α → β) -> (g : α → γ) -> (j : β → γ) -> β → γ",
    )
    result = splice_real_name(server, env, sig, "Function.extend", timeout=30.0)
    assert result.status is CheckStatus.PASSED, result.detail


def test_splice_real_name_does_not_retry_on_an_unrelated_error(mathlib_env):
    """The retry is specific to the noncomputable compiler error -- a genuinely different
    failure (here: a deliberately wrong pinned type, an ordinary type mismatch) must come back
    as ITSELF, not silently swapped for a noncomputable-retry's own (different, confusing)
    error."""
    server, env = mathlib_env
    sig = PinnedSignature(name="VTask.badClog", type_sig="Bool -> Bool -> Bool")  # wrong type for Nat.clog
    result = splice_real_name(server, env, sig, "Nat.clog", timeout=30.0)
    assert result.status is not CheckStatus.PASSED
    assert "noncomputable" not in (result.detail or "").lower()


def test_splice_real_name_byte_identical_for_already_working_names(mathlib_env):
    """Nat.clog and Nat.ModEq (both dotted, both already working) must behave identically under
    the new root-qualified splice -- `_root_.` is always safe to prepend, never a behavior
    change for a name that was never ambiguous."""
    server, env = mathlib_env
    clog_result = run_checked(server, Command(cmd=CLOG_SIG.splice_real_name("Nat.clog"), env=env), timeout=30.0)
    assert clog_result.status is CheckStatus.PASSED, clog_result.detail
    modeq_result = run_checked(server, Command(cmd=MODEQ_SIG.splice_real_name("Nat.ModEq"), env=env), timeout=30.0)
    assert modeq_result.status is CheckStatus.PASSED, modeq_result.detail
