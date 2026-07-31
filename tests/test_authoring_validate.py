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
from harness.facts import FactProvenance
from harness.repl import get_warm_environment
from harness.results import CheckStatus
from tests.fixtures.authoring_facts import (
    CLOG_DOMAIN,
    CLOG_NAME,
    MONOTONE_DOMAIN,
    MONOTONE_NAME,
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
    verdict, _ = check_domain_containment(server, env, CLOG_DOMAIN, {"b": ["2"], "n": ["37"]})
    assert verdict == "IN_DOMAIN"


def test_domain_containment_out_of_domain(mathlib_env):
    server, env = mathlib_env
    verdict, _ = check_domain_containment(server, env, CLOG_DOMAIN, {"b": ["100"], "n": ["37"]})
    assert verdict == "OUT_OF_DOMAIN"


def test_domain_containment_via_convention_point(mathlib_env):
    server, env = mathlib_env
    verdict, evidence = check_domain_containment(server, env, CLOG_DOMAIN, {"b": ["5"], "n": ["1"]})
    assert verdict == "IN_DOMAIN_VIA_CONVENTION"
    assert evidence["matched_convention_point"] == "n ≤ 1"


def test_domain_containment_undecided_when_predicate_is_not_decidable(mathlib_env):
    server, env = mathlib_env
    domain = DomainSpec(
        constraint="Continuous f",
        conventions=[ConventionPoint(point=None, statement=None, note="NONE_DECLARED: not this test's concern")],
    )
    verdict, _ = check_domain_containment(server, env, domain, {"f": ["(fun x : ℝ => x)"]})
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


# --- Global-fact ERRORED/FAILED split (2026-07-31 fix) ------------------------------------------
#
# A bogus `env` id against a real warm server reproduces Lean's own dead-server error text
# ("LeanError: Unknown environment.") exactly, and is the established way this suite simulates
# REPL death without killing a shared fixture (same technique as tests/test_authoring_batch.py).
# Before this fix, `validate_global_fact` collapsed that infra failure into
# PROPOSITION_DOES_NOT_ELABORATE, so `adjudicate_proposed_facts`' row-5 retry/flag machinery --
# gated on ReasonCode.ERRORED -- could never fire for a global fact, and the fact was silently
# dropped as if the model had proposed something invalid.

BOGUS_ENV = 999_999

_GLOBAL_FACT = ProposedFact(
    id="g_infra", type="global", mechanism="proof",
    statement="∀ b n : ℕ, Nat.clog b n ≥ 0", anchors=["Nat.clog_pow"],
)


def test_global_fact_repl_death_is_errored_not_rejected_as_non_elaborating(mathlib_env):
    server, _env = mathlib_env
    outcome = validate_global_fact(server, BOGUS_ENV, _GLOBAL_FACT, CLOG_DOMAIN, CLOG_NAME, timeout=30.0)
    assert outcome.reason_code == ReasonCode.ERRORED, outcome.detail
    assert "Unknown environment" in outcome.detail


def test_global_fact_genuinely_non_elaborating_still_rejects(mathlib_env):
    """The other direction: a real (live) environment plus a statement that genuinely does not
    elaborate must still reject as PROPOSITION_DOES_NOT_ELABORATE -- the fix must not have
    turned every rejection into an infra excuse."""
    server, env = mathlib_env
    fact = ProposedFact(
        id="g_bad", type="global", mechanism="proof",
        statement="∀ b n : ℕ, Nat.clog b n ≥ thisIdentifierDoesNotExist", anchors=["Nat.clog_pow"],
    )
    outcome = validate_global_fact(server, env, fact, CLOG_DOMAIN, CLOG_NAME, timeout=30.0)
    assert outcome.verdict is Verdict.REJECTED
    assert outcome.reason_code == ReasonCode.PROPOSITION_DOES_NOT_ELABORATE, outcome.detail


def test_global_fact_anchor_repl_death_is_errored_not_anchor_not_found(mathlib_env):
    """The anchor loop carried the same conflation: a REPL that dies while resolving an anchor
    says nothing about whether that anchor exists, so it must not report ANCHOR_NOT_FOUND. The
    proxy lets the proposition `#check` through to the real server, then kills every later call
    -- the only way to reach the anchor loop with a dead server but a passing prop check."""
    server, env = mathlib_env

    class _DiesAfterFirstCall:
        def __init__(self, real):
            self._real = real
            self._calls = 0

        def run(self, request, timeout=None):
            from lean_interact.interface import LeanError

            self._calls += 1
            if self._calls == 1:
                return self._real.run(request, timeout=timeout)
            return LeanError(message="Unknown environment.")

        def __getattr__(self, item):
            return getattr(self._real, item)

    outcome = validate_global_fact(
        _DiesAfterFirstCall(server), env, _GLOBAL_FACT, CLOG_DOMAIN, CLOG_NAME, timeout=30.0
    )
    assert outcome.reason_code == ReasonCode.ERRORED, outcome.detail
    assert outcome.reason_code != ReasonCode.ANCHOR_NOT_FOUND


def test_global_fact_repl_death_reaches_task_errored_not_dropped(mathlib_env):
    """The payoff, end to end: with the reason code fixed, a REPL-dead global fact now flows
    into `adjudicate_proposed_facts`' `task_errored` (row 5: flag the whole task) instead of
    being silently dropped as a bad fact. This is the behaviour the fix exists to restore."""
    from authoring.orchestrate import adjudicate_proposed_facts

    server, _env = mathlib_env
    result = adjudicate_proposed_facts(
        server, BOGUS_ENV, [_GLOBAL_FACT], CLOG_DOMAIN, CLOG_NAME, timeout=30.0
    )
    assert result.task_errored, "REPL-death global fact must reach task_errored, not be dropped"
    assert not result.dropped
    assert result.task_errored[0].fact_id == "g_infra"


def test_unknown_fact_type_rejected_without_repl():
    fact = ProposedFact(id="w", type="bogus", mechanism="decide", statement="whatever")
    outcome = validate_fact(None, None, fact, CLOG_DOMAIN, CLOG_NAME)
    assert outcome.verdict is Verdict.REJECTED
    assert outcome.reason_code == ReasonCode.MALFORMED_UNKNOWN_TYPE


# --- ProposedFact projection and ValidationRun reporting --------------------------------------


def test_to_fact_carries_domain_inputs_and_anchors_but_drops_expected_type():
    """Schema v1.1: domain_inputs and anchors now ship in task.json, so to_fact() carries them
    through; expected_type remains the one authoring-only field (see authoring/facts.py's
    module docstring and docs/design/task_schema_v1_1.md's Open points)."""
    pf = ProposedFact(
        id="x", type="global", mechanism="proof", statement="s",
        domain_inputs={"n": ["1"]}, anchors=["A"], expected_type="Nat",
    )
    f = pf.to_fact(validation_status="PROVISIONALLY_VALIDATED")
    assert (f.id, f.type, f.mechanism, f.statement) == ("x", "global", "proof", "s")
    assert f.instance is None
    assert f.polarity is None
    assert f.violated_property is None
    assert f.domain_inputs == {"n": ["1"]}
    assert f.anchors == ["A"]
    assert f.validation_status == "PROVISIONALLY_VALIDATED"
    assert f.discharge is None
    assert f.cached_script is None
    assert f.axiom_closure is None
    assert not hasattr(f, "expected_type")


def test_to_fact_carries_discharge_evidence_when_certified():
    pf = ProposedFact(id="y", type="casework", mechanism="decide", statement="s", domain_inputs={"n": ["1"]})
    f = pf.to_fact(
        validation_status="CERTIFIED",
        provenance=FactProvenance(validation_run_id="run-1", note="ran fine"),
        discharge={"tier": 1, "wall_clock_s": 0.01, "at": "authoring"},
        cached_script="by decide",
        axiom_closure=["propext"],
    )
    assert f.validation_status == "CERTIFIED"
    assert f.provenance == FactProvenance(validation_run_id="run-1", note="ran fine")
    assert f.discharge == {"tier": 1, "wall_clock_s": 0.01, "at": "authoring"}
    assert f.cached_script == "by decide"
    assert f.axiom_closure == ["propext"]


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


def test_membership_fact_with_no_expected_type_still_gets_accepted(mathlib_env):
    """2026-07-28: `expected_type` is optional (not a schema requirement). A real membership
    fact with it entirely absent must still reach a real verdict via the plain `#check
    (instance)` elaboration-probe fallback, not bounce off `MALFORMED_MISSING_FIELD` the way it
    did before this session's fix (the real 2026-07-28 gate incident's root cause)."""
    server, env = mathlib_env
    fact = ProposedFact(
        id="monotone_no_expected_type",
        type="membership",
        mechanism="decide",
        statement="example : Monotone (fun n : Fin 3 => n) := by decide",
        instance="(fun n : Fin 3 => n)",
        polarity="accept",
        expected_type=None,
    )
    outcome = validate_membership_fact(server, env, fact, MONOTONE_DOMAIN)
    assert outcome.verdict is Verdict.ACCEPTED
    assert outcome.reason_code != ReasonCode.MALFORMED_MISSING_FIELD
    # plain `#check (instance)`, not the type-ascribed `#check ((instance) : (expected_type))`
    assert outcome.evidence["elaboration"]["command"] == "#check ((fun n : Fin 3 => n))"
