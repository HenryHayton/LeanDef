"""Unit tests for `harness.results`' fidelity formula and EXCESSIVE_UNKNOWN flag.

Pure Python logic, no REPL involved -- uses synthetic `FactResult`s to exercise the
UNKNOWN/ERRORED paths, since nothing in this codebase produces a real UNKNOWN yet (the
prover scaffold doesn't exist). See `docs/design/task_schema_v1.md` "Scoring semantics" for
the formula and flag this tests against.
"""

from harness.results import CandidateScore, CheckResult, CheckStatus, ExcessiveUnknownFlag, FactResult, ProofStatus

SPLICE_OK = CheckResult(status=CheckStatus.PASSED, elapsed_s=0.01)


def _decide(fact_id: str, status: CheckStatus) -> FactResult:
    return FactResult(fact_id=fact_id, status=status, elapsed_s=0.01)


def _proof(fact_id: str, status: ProofStatus) -> FactResult:
    return FactResult(fact_id=fact_id, status=status, elapsed_s=1.0)


def _score(fact_results: list[FactResult], admissible: bool = True) -> CandidateScore:
    return CandidateScore(
        label="synthetic",
        splice=SPLICE_OK,
        admissible=admissible,
        admissibility_detail="",
        fact_results=fact_results,
    )


# --- fidelity ---


def test_fidelity_all_passed_is_one():
    score = _score([_decide("a", CheckStatus.PASSED), _decide("b", CheckStatus.PASSED)])
    assert score.fidelity == 1.0


def test_fidelity_all_failed_is_zero():
    score = _score([_decide("a", CheckStatus.FAILED), _decide("b", CheckStatus.FAILED)])
    assert score.fidelity == 0.0


def test_fidelity_mixed_passed_failed():
    score = _score([_decide("a", CheckStatus.PASSED), _decide("b", CheckStatus.FAILED)])
    assert score.fidelity == 0.5


def test_fidelity_true_counts_as_certified_for_proof_mechanism():
    score = _score([_proof("a", ProofStatus.TRUE), _proof("b", ProofStatus.FALSE)])
    assert score.fidelity == 0.5


def test_fidelity_excludes_unknown_from_denominator():
    """3 facts, 1 UNKNOWN: fidelity is 1/2 (the UNKNOWN is dropped from both numerator and
    denominator), not 1/3."""
    score = _score(
        [_decide("a", CheckStatus.PASSED), _decide("b", CheckStatus.FAILED), _proof("c", ProofStatus.UNKNOWN)]
    )
    assert score.fidelity == 0.5


def test_fidelity_excludes_errored_from_denominator():
    score = _score(
        [_decide("a", CheckStatus.PASSED), _decide("b", CheckStatus.FAILED), _decide("c", CheckStatus.ERRORED)]
    )
    assert score.fidelity == 0.5


def test_fidelity_excludes_both_unknown_and_errored():
    score = _score(
        [
            _decide("a", CheckStatus.PASSED),
            _proof("b", ProofStatus.UNKNOWN),
            _decide("c", CheckStatus.ERRORED),
        ]
    )
    assert score.fidelity == 1.0  # 1 certified / (3 - 1 unknown - 1 errored) = 1/1


def test_fidelity_none_when_everything_unresolved():
    score = _score([_proof("a", ProofStatus.UNKNOWN), _decide("b", CheckStatus.ERRORED)])
    assert score.fidelity is None


def test_fidelity_none_when_not_admissible():
    score = _score([_decide("a", CheckStatus.PASSED)], admissible=False)
    assert score.fidelity is None


def test_fidelity_none_when_no_facts():
    score = _score([])
    assert score.fidelity is None


# --- EXCESSIVE_UNKNOWN ---


def test_excessive_unknown_none_below_threshold():
    # 1/10 proof facts UNKNOWN == 10%, at the default threshold (not exceeding it).
    facts = [_proof(f"p{i}", ProofStatus.TRUE) for i in range(9)] + [_proof("p9", ProofStatus.UNKNOWN)]
    score = _score(facts)
    assert score.excessive_unknown() is None


def test_excessive_unknown_flags_above_threshold():
    # 2/10 proof facts UNKNOWN == 20% > default 10%.
    facts = [_proof(f"p{i}", ProofStatus.TRUE) for i in range(8)] + [
        _proof("p8", ProofStatus.UNKNOWN),
        _proof("p9", ProofStatus.UNKNOWN),
    ]
    score = _score(facts)
    flag = score.excessive_unknown()
    assert isinstance(flag, ExcessiveUnknownFlag)
    assert flag.unknown_count == 2
    assert flag.proof_fact_count == 10
    assert set(flag.affected_fact_ids) == {"p8", "p9"}
    assert "2/10" in flag.reason
    assert "UNKNOWN" in flag.reason


def test_excessive_unknown_ignores_decide_mechanism_facts_in_denominator():
    """A pile of decide-mechanism facts must not dilute the proof-mechanism UNKNOWN rate --
    the alarm is scoped to proof-mechanism facts specifically (task_schema_v1.md)."""
    facts = [_decide(f"d{i}", CheckStatus.PASSED) for i in range(100)] + [
        _proof("p0", ProofStatus.UNKNOWN),
        _proof("p1", ProofStatus.TRUE),
    ]
    score = _score(facts)
    flag = score.excessive_unknown()
    assert isinstance(flag, ExcessiveUnknownFlag)
    assert flag.proof_fact_count == 2  # not 102
    assert flag.unknown_count == 1


def test_excessive_unknown_none_when_no_proof_facts():
    score = _score([_decide("a", CheckStatus.PASSED), _decide("b", CheckStatus.FAILED)])
    assert score.excessive_unknown() is None


def test_excessive_unknown_custom_threshold():
    # 1/4 proof facts UNKNOWN == 25%: flagged at the default 10% threshold, not at 50%.
    facts = [_proof("p0", ProofStatus.TRUE), _proof("p1", ProofStatus.TRUE), _proof("p2", ProofStatus.FALSE)]
    facts.append(_proof("p3", ProofStatus.UNKNOWN))
    score = _score(facts)
    assert score.excessive_unknown(threshold=0.10) is not None
    assert score.excessive_unknown(threshold=0.50) is None
