"""Tests for ladder.tier1 -- the thin wrapper over harness's existing decide machinery."""


from ladder.budgets import DEFAULT_LADDER_BUDGETS
from ladder.statuses import AdjudicationStatus
from ladder.tier1 import adjudicate_tier1



def test_true_decide_statement_certifies(mathlib_env):
    server, env = mathlib_env
    attempt = adjudicate_tier1(server, env, "example : Nat.clog 2 37 = 6 := by decide", DEFAULT_LADDER_BUDGETS)
    assert attempt.status is AdjudicationStatus.CERTIFIED
    assert attempt.tier == 1
    assert attempt.tactic is None


def test_false_decide_statement_is_a_genuine_failure(mathlib_env):
    server, env = mathlib_env
    attempt = adjudicate_tier1(server, env, "example : Nat.clog 2 37 = 5 := by decide", DEFAULT_LADDER_BUDGETS)
    assert attempt.status is AdjudicationStatus.FAILED
