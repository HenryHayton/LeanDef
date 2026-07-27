"""Tests for ladder.adjudicate -- the per-fact adjudication loop.

Real Mathlib environment: exercises the decide path, the proof path through tier 2 (cache miss
-> fresh search -> axiom audit -> cache write), the cache-hit replay path, and budget
exhaustion on a genuinely hard fact returning UNKNOWN with partial attempt records.
"""

import pytest

from harness.facts import Fact
from harness.repl import get_warm_environment
from harness.results import CheckStatus
from ladder.adjudicate import adjudicate_fact
from ladder.budgets import DEFAULT_LADDER_BUDGETS
from ladder.cache import ProofScriptCache, toolchain_pin
from ladder.statuses import AdjudicationStatus, ElaborationStatus


@pytest.fixture(scope="module")
def mathlib_env():
    server, import_result = get_warm_environment()
    assert import_result.status is CheckStatus.PASSED, import_result.detail
    yield server, import_result.env
    server.kill()


def _decide_fact(fact_id: str, statement: str) -> Fact:
    return Fact(id=fact_id, type="casework", mechanism="decide", statement=statement)


def _proof_fact(fact_id: str, statement: str) -> Fact:
    return Fact(id=fact_id, type="global", mechanism="proof", statement=statement, anchors=[])


def test_decide_mechanism_true_statement_certifies_at_tier1(mathlib_env):
    server, env = mathlib_env
    fact = _decide_fact("d1", "example : Nat.clog 2 37 = 6 := by decide")
    adjudication, returned_env = adjudicate_fact(fact, env, server, DEFAULT_LADDER_BUDGETS)
    assert adjudication.status is AdjudicationStatus.CERTIFIED
    assert adjudication.tier == 1
    assert adjudication.elaboration is ElaborationStatus.ELABORATES
    assert adjudication.axiom_closure is None  # tier 1 is kernel computation, no audit applies
    assert returned_env == env  # decide mechanism never mutates the environment


def test_decide_mechanism_false_statement_is_failed(mathlib_env):
    server, env = mathlib_env
    fact = _decide_fact("d2", "example : Nat.clog 2 37 = 5 := by decide")
    adjudication, _ = adjudicate_fact(fact, env, server, DEFAULT_LADDER_BUDGETS)
    assert adjudication.status is AdjudicationStatus.FAILED


def test_proof_mechanism_fact_discharged_by_tier2_certifies_and_caches(mathlib_env, tmp_path):
    server, env = mathlib_env
    cache = ProofScriptCache(path=tmp_path / "cache.jsonl")
    fact = _proof_fact("p1", "∀ (n : ℕ), n + 0 = n")

    adjudication, env = adjudicate_fact(fact, env, server, DEFAULT_LADDER_BUDGETS, cache)

    assert adjudication.status is AdjudicationStatus.CERTIFIED
    assert adjudication.tier == 2
    assert adjudication.elaboration is ElaborationStatus.ELABORATES
    assert adjudication.axiom_closure is not None
    assert adjudication.script is not None
    assert not adjudication.from_cache

    # the cache now holds an entry for this exact statement.
    entry = cache.get(fact.statement, toolchain_pin())
    assert entry is not None
    assert entry.tier == 2


def test_proof_mechanism_fact_cache_hit_replays_without_a_fresh_search(mathlib_env, tmp_path):
    server, env = mathlib_env
    cache = ProofScriptCache(path=tmp_path / "cache.jsonl")
    fact = _proof_fact("p2", "∀ (n : ℕ), n + 0 = n")

    first, env = adjudicate_fact(fact, env, server, DEFAULT_LADDER_BUDGETS, cache)
    assert first.status is AdjudicationStatus.CERTIFIED
    assert not first.from_cache

    second, env = adjudicate_fact(fact, env, server, DEFAULT_LADDER_BUDGETS, cache)
    assert second.status is AdjudicationStatus.CERTIFIED
    assert second.from_cache
    assert second.script == first.script
    assert len(second.attempts) == 0  # no tier attempted -- pure replay


def test_genuinely_hard_proof_fact_returns_unknown_with_partial_attempt_records(mathlib_env):
    server, env = mathlib_env
    fact = _proof_fact("p3", "∀ (n : ℕ), 1 < n → Nat.clog 2 (2 * n) = Nat.clog 2 n + 1")

    adjudication, _ = adjudicate_fact(fact, env, server, DEFAULT_LADDER_BUDGETS)

    assert adjudication.status is AdjudicationStatus.UNKNOWN
    assert adjudication.elaboration is ElaborationStatus.ELABORATES
    assert adjudication.tier is None
    assert adjudication.script is None
    assert len(adjudication.attempts) == len(DEFAULT_LADDER_BUDGETS.tier2_tactics)  # partial records survive


def test_non_elaborating_statement_short_circuits_with_no_tier_attempted(mathlib_env):
    server, env = mathlib_env
    fact = _proof_fact("p4", "Nat.this_identifier_does_not_exist_anywhere = 0")

    adjudication, _ = adjudicate_fact(fact, env, server, DEFAULT_LADDER_BUDGETS)

    assert adjudication.elaboration is ElaborationStatus.DOES_NOT_ELABORATE
    assert adjudication.status is AdjudicationStatus.UNKNOWN
    assert adjudication.attempts == []
