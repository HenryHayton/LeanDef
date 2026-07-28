"""Tests for ladder.adjudicate -- the per-fact adjudication loop.

Real Mathlib environment: exercises the decide path, the proof path through tier 2 (cache miss
-> fresh search -> axiom audit -> cache write), the cache-hit replay path, and budget
exhaustion on a genuinely hard fact returning UNKNOWN with partial attempt records.
"""

import time

import pytest

from harness.facts import Fact
from harness.repl import get_warm_environment
from harness.results import CheckStatus
from ladder.adjudicate import BUDGET_EXHAUSTED_MARKER, adjudicate_fact
from ladder.budgets import DEFAULT_LADDER_BUDGETS, LadderBudgets
from ladder.cache import ProofScriptCache, toolchain_pin
from ladder.statuses import AdjudicationStatus, ElaborationStatus, TierAttempt
from ladder.tier2 import Tier2Result


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
    # tier 2's full ladder, then tier 3 (real as of Session B) -- on the Mac, with no Hammer
    # project available, `hammer` isn't even a real tactic, so tier 3 comes back UNKNOWN too
    # ("unknown tactic", not a crash and not ENV_DEATH) -- exactly the graceful degradation
    # tier 3 is supposed to have when Hammer genuinely isn't available. Tier 4 is skipped (no
    # truth_env/candidate_name/truth_name supplied), tier 5 is still a stub.
    assert len(adjudication.attempts) == len(DEFAULT_LADDER_BUDGETS.tier2_tactics) + 1  # partial records survive
    assert adjudication.attempts[-1].tier == 3
    assert adjudication.attempts[-1].status is AdjudicationStatus.UNKNOWN


def test_per_fact_ceiling_stops_tier2_from_reaching_tier3(mathlib_env, monkeypatch):
    server, env = mathlib_env
    # Real tactic search timing is not a reliable clock to race against: `exact?`'s discrimination
    # tree gets built once per environment and reused, so a statement that's genuinely slow to
    # discharge on a cold environment can come back near-instant on a warm one (observed directly
    # while developing this test -- two consecutive real runs on the same "hard" statement came
    # back 0.02s and 1.8s respectively, a ~90x spread with no other change). Racing a fixed or
    # even a measured-then-halved ceiling against that is inherently flaky. Instead, keep the
    # elaboration probe real (a single, reliably-fast `#check`) and replace tier 2 itself with a
    # stand-in that sleeps a fixed, controlled duration -- this tests the LOOP's ceiling
    # enforcement, not tier 2's own timing, which `test_ladder_tier2.py` already covers for real.
    def _slow_fake_tier2(server, env, fact_id, canonical_statement, budgets, *, imports=None):
        time.sleep(1.0)
        dummy = TierAttempt(
            tier=2, tactic="omega", status=AdjudicationStatus.UNKNOWN, elapsed_s=1.0, detail="fake, for ceiling test"
        )
        return Tier2Result(attempts=[dummy], winning=None, winning_theorem_name=None, winning_script=None, env=env)

    monkeypatch.setattr("ladder.adjudicate.adjudicate_tier2", _slow_fake_tier2)

    fact = _proof_fact("p5", "(2:ℕ) + 2 = 4")  # elaborates trivially and fast; tier 2 itself never runs for real
    tight_budgets = LadderBudgets(per_fact_total_wall_clock_s=0.2)  # < the fake tier 2's 1.0s sleep

    adjudication, _ = adjudicate_fact(fact, env, server, tight_budgets)

    assert adjudication.status is AdjudicationStatus.UNKNOWN
    assert adjudication.tier is None
    assert BUDGET_EXHAUSTED_MARKER in adjudication.detail
    assert len(adjudication.attempts) == 1  # the fake tier 2's one dummy attempt -- it DID run
    assert adjudication.wall_clock_s >= tight_budgets.per_fact_total_wall_clock_s


def test_non_elaborating_statement_short_circuits_with_no_tier_attempted(mathlib_env):
    server, env = mathlib_env
    fact = _proof_fact("p4", "Nat.this_identifier_does_not_exist_anywhere = 0")

    adjudication, _ = adjudicate_fact(fact, env, server, DEFAULT_LADDER_BUDGETS)

    assert adjudication.elaboration is ElaborationStatus.DOES_NOT_ELABORATE
    assert adjudication.status is AdjudicationStatus.UNKNOWN
    assert adjudication.attempts == []
