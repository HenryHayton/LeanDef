"""Tests for ladder.axiom_audit -- the fact-proof axiom rule (reward doc §3.3).

Needs a real, Mathlib-imported warm environment (`#print axioms` inspects a real kernel
declaration) -- same `mathlib_env` fixture pattern `tests/test_miner_discharge.py` established.
"""

from lean_interact import Command

from harness.repl import run_checked
from harness.results import CheckStatus
from ladder.axiom_audit import PERMITTED_FACT_PROOF_AXIOMS, _parse_axioms, audit_proof_axioms



def _declare(server, env, cmd: str) -> int:
    check = run_checked(server, Command(cmd=cmd, env=env), timeout=30.0)
    assert check.status is CheckStatus.PASSED, check.detail
    assert check.env is not None
    return check.env


def test_clean_proof_within_permitted_set_passes(mathlib_env):
    server, env = mathlib_env
    env = _declare(server, env, "theorem __audit_omega : (1 : Nat) + 1 = 2 := by omega")
    result = audit_proof_axioms(server, env, "__audit_omega")
    assert result.passed
    assert not result.has_sorry
    assert not result.excess_axioms
    assert result.axioms <= PERMITTED_FACT_PROOF_AXIOMS


def test_clean_decide_proof_with_no_axioms_passes(mathlib_env):
    server, env = mathlib_env
    env = _declare(server, env, "theorem __audit_decide : Nat.clog 2 37 = 6 := by decide")
    result = audit_proof_axioms(server, env, "__audit_decide")
    assert result.passed
    assert result.axioms == frozenset()


def test_planted_sorry_is_rejected(mathlib_env):
    server, env = mathlib_env
    env = _declare(server, env, "theorem __audit_sorry : (1 : Nat) + 1 = 3 := by sorry")
    result = audit_proof_axioms(server, env, "__audit_sorry")
    assert not result.passed
    assert result.has_sorry
    assert "sorryAx" in result.axioms
    assert "sorry" in result.detail


def test_unknown_declaration_fails_closed(mathlib_env):
    server, env = mathlib_env
    result = audit_proof_axioms(server, env, "__no_such_declaration_exists")
    assert not result.passed
    assert not result.has_sorry


def test_excess_axiom_beyond_permitted_set_is_rejected(mathlib_env):
    server, env = mathlib_env
    env = _declare(server, env, "theorem __audit_narrow : (1 : Nat) + 1 = 2 := by omega")
    result = audit_proof_axioms(server, env, "__audit_narrow", permitted=frozenset())
    assert not result.passed
    assert result.excess_axioms
    assert "excess axioms" in result.detail


def test_parse_axioms_handles_a_pretty_printer_line_wrap():
    """Regression test: Lean's `#print axioms` pretty-printer wraps the axiom list onto
    multiple lines once it's long enough (a long declaration name plus 3 axioms is enough --
    confirmed empirically, tier-cascade measurement, 2026-07-27). `_parse_axioms` must not
    silently fail to parse a wrapped list -- that bug demoted genuinely CERTIFIED facts to
    UNKNOWN with no other symptom."""
    wrapped = "'__some_long_declaration_name' depends on axioms: [propext,\n Classical.choice,\n Quot.sound]"
    assert _parse_axioms(wrapped) == frozenset({"propext", "Classical.choice", "Quot.sound"})


def test_parse_axioms_still_handles_a_single_line_list():
    single_line = "'__t_omega' depends on axioms: [propext, Quot.sound]"
    assert _parse_axioms(single_line) == frozenset({"propext", "Quot.sound"})
