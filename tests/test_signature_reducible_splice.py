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
from harness.repl import get_warm_environment, run_checked
from harness.results import CheckStatus

CLOG_SIG = PinnedSignature(name=task_symbol_for("Nat.clog"), type_sig="Nat -> Nat -> Nat")
CLOG_TRUE_BODY = "fun b n => if b ≤ 1 ∨ n ≤ 1 then 0 else Nat.log b (n - 1) + 1"
CLOG_FACTS = [
    Fact(id="c1", type="casework", mechanism="decide", statement=f"example : {CLOG_SIG.name} 2 8 = 3 := by decide"),
    Fact(id="c2", type="casework", mechanism="decide", statement=f"example : {CLOG_SIG.name} 2 9 = 4 := by decide"),
]

MODEQ_SIG = PinnedSignature(name=task_symbol_for("Nat.ModEq"), type_sig="(n a b : ℕ) -> Prop")


@pytest.fixture(scope="module")
def mathlib_env():
    server, import_result = get_warm_environment()
    assert import_result.status is CheckStatus.PASSED, import_result.detail
    yield server, import_result.env
    server.kill()


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


def test_bare_alias_candidate_still_trips_shadowing_after_reducible_splice(mathlib_env):
    """The one regression this change could plausibly have caused silently (docs/deferred.md's
    "bare-alias candidate bodies... trip the admissibility shadowing check" note): a candidate
    body that is just the real name, unapplied (`body = "Nat.clog"`, not `"Nat.clog b n"`),
    makes LeanInteract's declaration report list the real name alongside the pinned one -- this
    is what currently keeps a verbatim-copy candidate from silently passing admissibility.
    Confirmed this still fires under the new `@[reducible]` splice, not just the old plain one."""
    server, env = mathlib_env
    cmd = CLOG_SIG.splice("Nat.clog")  # bare, point-free -- NOT "Nat.clog b n"
    splice = run_checked(server, Command(cmd=cmd, env=env, declarations=True), timeout=30.0)
    assert splice.status is CheckStatus.PASSED, splice.detail

    verdict = check_admissibility(server, splice.env, CLOG_SIG, splice_response=splice.raw_response, timeout=30.0)
    assert not verdict.passed
    assert verdict.failure is AdmissibilityFailure.NAME_SHADOWED, verdict.detail


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
