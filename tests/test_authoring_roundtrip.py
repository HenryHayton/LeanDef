"""Tests for `authoring.roundtrip.score_round_trip_first_cut` -- the suite-partitioning round-
trip scorer (contract §5, §8 item 5). Real warm Mathlib environment, same pattern as
`tests/test_authoring_validate.py`: this module's whole point is exercising real splice/
admissibility/fact-adjudication machinery, so there's no ground truth to fake.

The central behavior under test: a fact suite containing a `proof`-mechanism (global) fact
must NOT reach `harness.scoring.run_facts` (which raises `NotImplementedError` for that
mechanism by design) -- every test here includes at least one global fact precisely to prove
that partitioning holds.
"""


from harness.facts import Fact
from harness.signature import PinnedSignature
from authoring.roundtrip import score_round_trip_first_cut


SIGNATURE = PinnedSignature(name="rtDouble", type_sig="Nat -> Nat")


def _decide_fact(fact_id: str, statement: str) -> Fact:
    return Fact(id=fact_id, type="casework", mechanism="decide", statement=statement, domain_inputs={"n": ["3"]})


def _global_fact(fact_id: str, statement: str, anchors=None) -> Fact:
    return Fact(id=fact_id, type="global", mechanism="proof", statement=statement, anchors=anchors or [])


def test_correct_candidate_passes_decide_and_global_facts(mathlib_env):
    server, env = mathlib_env
    facts = [
        _decide_fact("d_true", "example : rtDouble 3 = 6 := by decide"),
        _global_fact("g_shape", "∀ n : ℕ, rtDouble n = n + n"),
    ]
    score = score_round_trip_first_cut(server, env, SIGNATURE, "fun n => n + n", facts)
    assert score.admissible
    assert score.passed
    assert score.failing_decide_fact_ids == []
    assert score.failing_global_fact_ids == []


def test_global_fact_never_reaches_run_facts_no_crash(mathlib_env):
    """The core partitioning guarantee: even a suite containing ONLY a global fact must not
    raise NotImplementedError -- it must be checked structurally instead."""
    server, env = mathlib_env
    facts = [_global_fact("g_only", "∀ n : ℕ, rtDouble n = n + n")]
    score = score_round_trip_first_cut(server, env, SIGNATURE, "fun n => n + n", facts)
    assert score.admissible
    assert score.passed
    assert score.decide_fact_results == []
    assert len(score.global_elaboration_results) == 1


def test_wrong_candidate_fails_a_decide_fact(mathlib_env):
    server, env = mathlib_env
    facts = [_decide_fact("d_false", "example : rtDouble 3 = 7 := by decide")]
    score = score_round_trip_first_cut(server, env, SIGNATURE, "fun n => n + n", facts)
    assert score.admissible
    assert not score.passed
    assert score.failing_decide_fact_ids == ["d_false"]


def test_global_fact_that_does_not_elaborate_fails_structurally(mathlib_env):
    server, env = mathlib_env
    facts = [_global_fact("g_bad", "∀ n : ℕ, rtDouble n +++ 1 = n")]
    score = score_round_trip_first_cut(server, env, SIGNATURE, "fun n => n + n", facts)
    assert score.admissible
    assert not score.passed
    assert score.failing_global_fact_ids == ["g_bad"]


def test_inadmissible_candidate_short_circuits_before_any_fact_check(mathlib_env):
    server, env = mathlib_env
    facts = [
        _decide_fact("d_true", "example : rtDouble 3 = 6 := by decide"),
        _global_fact("g_shape", "∀ n : ℕ, rtDouble n = n + n"),
    ]
    score = score_round_trip_first_cut(server, env, SIGNATURE, "sorry", facts)
    assert not score.admissible
    assert not score.passed
    assert score.decide_fact_results == []
    assert score.global_elaboration_results == []


def test_criterion_is_always_first_cut(mathlib_env):
    server, env = mathlib_env
    facts = [_decide_fact("d_true", "example : rtDouble 3 = 6 := by decide")]
    score = score_round_trip_first_cut(server, env, SIGNATURE, "fun n => n + n", facts)
    assert score.criterion == "first_cut"
