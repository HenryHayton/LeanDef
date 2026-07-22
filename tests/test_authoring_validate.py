"""Tests for `authoring.validate` against the two hand-written fixture fact sets in
`tests/fixtures/authoring_facts.py` (`Nat.clog`, `Monotone`), plus focused unit tests for the
domain-containment checker and the malformed-fact fast paths that never touch the REPL.

Uses a real, Mathlib-imported warm environment (`mathlib_env`, module-scoped) rather than a
scripted fake server: unlike `miner.verify` or `harness.scoring`, this validator's whole job is
checking facts against the *true* Mathlib definitions, so there is no ground truth to fake --
`Nat.clog` and `Monotone` must be the real Mathlib declarations. This is the first test module
in the suite to pay Mathlib's cold-import cost; see the task that introduced this module for
why (and the suite's reported runtime for the actual cost).
"""

import pytest

from authoring.facts import ConventionPoint, DomainSpec, ProposedFact
from authoring.validate import (
    ReasonCode,
    ValidationOutcome,
    ValidationRun,
    Verdict,
    check_domain_containment,
    validate_casework_fact,
    validate_fact,
    validate_facts,
    validate_global_fact,
    validate_membership_fact,
)
from harness.repl import get_warm_environment
from harness.results import CheckStatus
from tests.fixtures.authoring_facts import (
    CLOG_DOMAIN,
    CLOG_NAME,
    MONOTONE_DOMAIN,
    clog_fixture_set,
    monotone_fixture_set,
)


@pytest.fixture(scope="module")
def mathlib_env():
    server, import_result = get_warm_environment()
    assert import_result.status is CheckStatus.PASSED, import_result.detail
    yield server, import_result.env
    server.kill()


def _assert_matches_expected(run: ValidationRun, expected: dict[str, tuple[Verdict, str]]) -> None:
    outcomes = {o.fact_id: o for o in run.outcomes}
    for fact_id, (verdict, reason) in expected.items():
        outcome = outcomes[fact_id]
        assert outcome.verdict is verdict, (
            f"{fact_id}: expected verdict {verdict}, got {outcome.verdict} "
            f"({outcome.reason_code}: {outcome.detail})"
        )
        assert outcome.reason_code == reason, (
            f"{fact_id}: expected reason {reason}, got {outcome.reason_code}: {outcome.detail}"
        )


def test_clog_fixture_set_matches_expected_verdicts(mathlib_env):
    server, env = mathlib_env
    domain, name, facts, expected = clog_fixture_set()
    run = validate_facts(server, env, facts, domain, name)
    assert set(o.fact_id for o in run.outcomes) == set(expected)
    _assert_matches_expected(run, expected)


def test_monotone_fixture_set_matches_expected_verdicts(mathlib_env):
    server, env = mathlib_env
    domain, name, facts, expected = monotone_fixture_set()
    run = validate_facts(server, env, facts, domain, name)
    assert set(o.fact_id for o in run.outcomes) == set(expected)
    _assert_matches_expected(run, expected)


# --- domain-containment checker, in isolation ------------------------------------------------


def test_domain_containment_in_domain(mathlib_env):
    server, env = mathlib_env
    verdict, _ = check_domain_containment(server, env, CLOG_DOMAIN, {"b": "2", "n": "37"})
    assert verdict == "IN_DOMAIN"


def test_domain_containment_out_of_domain(mathlib_env):
    server, env = mathlib_env
    verdict, _ = check_domain_containment(server, env, CLOG_DOMAIN, {"b": "100", "n": "37"})
    assert verdict == "OUT_OF_DOMAIN"


def test_domain_containment_via_convention_point(mathlib_env):
    server, env = mathlib_env
    verdict, evidence = check_domain_containment(server, env, CLOG_DOMAIN, {"b": "5", "n": "1"})
    assert verdict == "IN_DOMAIN_VIA_CONVENTION"
    assert evidence["matched_convention_point"] == "n ≤ 1"


def test_domain_containment_undecided_when_predicate_is_not_decidable(mathlib_env):
    server, env = mathlib_env
    domain = DomainSpec(constraint="Continuous f", conventions=[])
    verdict, _ = check_domain_containment(server, env, domain, {"f": "(fun x : ℝ => x)"})
    assert verdict == "DOMAIN_UNDECIDED"


def test_domain_containment_undecided_when_no_inputs_supplied():
    """No REPL call needed: a non-trivial constraint with no domain_inputs is undecidable by
    construction, so this must not touch `server`/`env` at all."""
    verdict, evidence = check_domain_containment(None, None, CLOG_DOMAIN, {})
    assert verdict == "DOMAIN_UNDECIDED"
    assert "no domain_inputs" in evidence["note"]


def test_domain_containment_true_sentinel_is_always_in_domain_without_repl():
    verdict, evidence = check_domain_containment(None, None, MONOTONE_DOMAIN, {})
    assert verdict == "IN_DOMAIN"


# --- malformed facts are rejected before any REPL round-trip ---------------------------------


def test_casework_wrong_mechanism_rejected_without_repl():
    fact = ProposedFact(id="x", type="casework", mechanism="proof", statement="whatever")
    outcome = validate_casework_fact(None, None, fact, CLOG_DOMAIN)
    assert outcome.verdict is Verdict.REJECTED
    assert outcome.reason_code == ReasonCode.MALFORMED_BAD_MECHANISM


def test_membership_bad_polarity_rejected_without_repl():
    fact = ProposedFact(
        id="y", type="membership", mechanism="decide", statement="whatever", instance="(0)",
        polarity="maybe", expected_type="Nat",
    )
    outcome = validate_membership_fact(None, None, fact, CLOG_DOMAIN)
    assert outcome.verdict is Verdict.REJECTED
    assert outcome.reason_code == ReasonCode.MALFORMED_BAD_POLARITY


def test_membership_missing_violated_property_rejected_without_repl():
    fact = ProposedFact(
        id="y2", type="membership", mechanism="decide", statement="whatever", instance="(0)",
        polarity="reject", violated_property=None, expected_type="Nat",
    )
    outcome = validate_membership_fact(None, None, fact, CLOG_DOMAIN)
    assert outcome.verdict is Verdict.REJECTED
    assert outcome.reason_code == ReasonCode.MALFORMED_MISSING_VIOLATED_PROPERTY


def test_global_missing_anchors_rejected_without_repl():
    fact = ProposedFact(id="z", type="global", mechanism="proof", statement="Nat.clog 1 1 = 1", anchors=[])
    outcome = validate_global_fact(None, None, fact, CLOG_DOMAIN, CLOG_NAME)
    assert outcome.verdict is Verdict.REJECTED
    assert outcome.reason_code == ReasonCode.MALFORMED_MISSING_ANCHORS


def test_global_bad_mechanism_rejected_without_repl():
    fact = ProposedFact(id="z2", type="global", mechanism="decide", statement="Nat.clog 1 1 = 1", anchors=["Nat.clog_pow"])
    outcome = validate_global_fact(None, None, fact, CLOG_DOMAIN, CLOG_NAME)
    assert outcome.verdict is Verdict.REJECTED
    assert outcome.reason_code == ReasonCode.MALFORMED_BAD_MECHANISM


def test_global_missing_pinned_name_rejected_without_repl():
    fact = ProposedFact(
        id="z3", type="global", mechanism="proof", statement="∀ n : ℕ, n = n", anchors=["Nat.clog_pow"]
    )
    outcome = validate_global_fact(None, None, fact, CLOG_DOMAIN, CLOG_NAME)
    assert outcome.verdict is Verdict.REJECTED
    assert outcome.reason_code == ReasonCode.DOES_NOT_MENTION_PINNED_NAME


def test_unknown_fact_type_rejected_without_repl():
    fact = ProposedFact(id="w", type="bogus", mechanism="decide", statement="whatever")
    outcome = validate_fact(None, None, fact, CLOG_DOMAIN, CLOG_NAME)
    assert outcome.verdict is Verdict.REJECTED
    assert outcome.reason_code == ReasonCode.MALFORMED_UNKNOWN_TYPE


# --- ProposedFact projection and ValidationRun reporting --------------------------------------


def test_to_fact_drops_authoring_only_fields():
    pf = ProposedFact(
        id="x", type="casework", mechanism="decide", statement="s",
        domain_inputs={"n": "1"}, anchors=["A"], expected_type="Nat",
    )
    f = pf.to_fact()
    assert (f.id, f.type, f.mechanism, f.statement) == ("x", "casework", "decide", "s")
    assert f.instance is None
    assert f.polarity is None
    assert f.violated_property is None


def test_validation_run_counts_and_summary():
    outcomes = [
        ValidationOutcome("a", Verdict.ACCEPTED, ReasonCode.CERTIFIED_TRUE_OF_GROUND_TRUTH),
        ValidationOutcome("b", Verdict.REJECTED, ReasonCode.FALSE_OF_GROUND_TRUTH, detail="nope"),
        ValidationOutcome("c", Verdict.FLAGGED, ReasonCode.DOMAIN_UNDECIDED, detail="dunno"),
    ]
    run = ValidationRun(outcomes)
    assert run.counts_by_verdict() == {"accepted": 1, "rejected": 1, "flagged": 1}
    assert run.counts_by_reason() == {
        ReasonCode.CERTIFIED_TRUE_OF_GROUND_TRUTH: 1,
        ReasonCode.FALSE_OF_GROUND_TRUTH: 1,
        ReasonCode.DOMAIN_UNDECIDED: 1,
    }
    summary = run.render_summary()
    assert f"b: {ReasonCode.FALSE_OF_GROUND_TRUTH} -- nope" in summary
    assert f"c: {ReasonCode.DOMAIN_UNDECIDED} -- dunno" in summary


def test_convention_point_dataclass_defaults_to_no_predicate():
    cp = ConventionPoint(point="0", statement="tau 0 = 0", note="junk value")
    assert cp.predicate is None
