"""Tests for ladder.tier1 -- the thin wrapper over harness's existing decide machinery."""

import pytest

from harness.repl import get_warm_environment
from harness.results import CheckStatus
from ladder.budgets import DEFAULT_LADDER_BUDGETS
from ladder.statuses import AdjudicationStatus
from ladder.tier1 import adjudicate_tier1


@pytest.fixture(scope="module")
def mathlib_env():
    server, import_result = get_warm_environment()
    assert import_result.status is CheckStatus.PASSED, import_result.detail
    yield server, import_result.env
    server.kill()


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
