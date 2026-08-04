"""Coverage hardening for `authoring/validate.py`'s untested failure paths (repo-audit
follow-up, 2026-07-24): reason code `ERRORED` (validation infrastructure failure, as opposed
to the fact being wrong), reason code `MALFORMED_MISSING_FIELD` (structurally broken
proposals), the `DOMAIN_UNDECIDED` path end-to-end (proposal → containment check → flagged
bucket), and an adversarial-input minisuite reproducing the kind of malformed content real LLM
output actually produces. These are the garbage-input routes real LLM output hits first --
untested error paths are exactly where a validator can silently misclassify.

**Deliberately its own module, not added to `test_authoring_validate.py`.** Two of the tests
here (the `ERRORED` cases) must genuinely trigger a REPL timeout to exercise the real failure
path, and per `harness.repl.run_checked`'s own documented caveat, a timeout that kills the
underlying Lean server invalidates every environment id from before the restart -- "recovering
full context... after a mid-run crash is not implemented." `test_authoring_validate.py`'s
`mathlib_env` fixture is module-scoped and reused across many tests that all assume a live,
Mathlib-imported environment; adding a timeout-inducing test into that module would risk
poisoning every test that runs after it. This module gets its own `mathlib_env` (same pattern,
separate instance) and keeps the two timeout-inducing tests at the very end of the file, after
everything else that needs the environment to stay healthy.

Coverage hardening surfaced three confirmed bugs (documented as `xfail` when this module was
first written); a follow-up fix session closed all three in `authoring/validate.py` --
`validate_membership_fact`'s instance-elaboration check now distinguishes `ERRORED` from
`INSTANCE_DOES_NOT_ELABORATE`, `_run_statement` guards against an empty/missing statement
before `Command` construction, and a decide-mechanism parse error is now reported under its own
`MALFORMED_UNPARSEABLE_STATEMENT` reason code rather than folded into `FALSE_OF_GROUND_TRUTH`.
No `xfail`s remain in this module.
"""

import pytest

from authoring.facts import ConventionPoint, DomainSpec, ProposedFact
from authoring.validate import (
    ReasonCode,
    Verdict,
    validate_casework_fact,
    validate_facts,
    validate_global_fact,
    validate_membership_fact,
)
from harness.repl import get_warm_environment
from harness.results import CheckStatus


CLOG_DOMAIN = DomainSpec(
    constraint="1 < b ∧ b ≤ 12 ∧ 1 < n",
    variables=["b", "n"],
    conventions=[
        ConventionPoint(point="b ≤ 1", statement="Nat.clog b n = 0 for b ≤ 1", note="junk value", predicate="b ≤ 1"),
    ],
)
CLOG_NAME = "Nat.clog"

TRUE_DOMAIN = DomainSpec(
    constraint="True", variables=[], conventions=[ConventionPoint(point=None, statement=None, note="NONE_DECLARED: x")]
)

# A domain constraint that is well-formed Lean but has no `Decidable` instance in general --
# the same shape `test_authoring_validate.py`'s own isolated-unit test already uses for
# `check_domain_containment`, reused here to drive the SAME undecidable predicate through the
# full per-type validators end-to-end (the untested half of that gap).
UNDECIDABLE_DOMAIN = DomainSpec(
    constraint="Continuous f", variables=["f"], conventions=[ConventionPoint(point=None, statement=None, note="NONE_DECLARED: x")]
)


@pytest.fixture(scope="module")
def mathlib_env():
    server, import_result = get_warm_environment()
    assert import_result.status is CheckStatus.PASSED, import_result.detail
    yield server, import_result.env
    server.kill()


# === Gap 2: MALFORMED_MISSING_FIELD (and siblings) -- none of these touch the REPL, matching
# === the existing "malformed facts rejected without repl" convention in test_authoring_validate.py.


def test_membership_missing_instance_is_malformed_missing_field():
    """The one case that genuinely produces `MALFORMED_MISSING_FIELD` today: `instance` absent
    on a membership fact. `expected_type` absence is NOT this (2026-07-28: made optional --
    `validate_membership_fact` falls back to a plain elaboration probe instead of rejecting)."""
    fact = ProposedFact(
        id="no_instance", type="membership", mechanism="decide", statement="whatever",
        instance=None, polarity="accept", expected_type="Nat",
    )
    outcome = validate_membership_fact(None, None, fact, CLOG_DOMAIN)
    assert outcome.verdict is Verdict.REJECTED
    assert outcome.reason_code == ReasonCode.MALFORMED_MISSING_FIELD


def test_membership_missing_polarity_is_malformed_bad_polarity():
    """Distinct from `test_membership_bad_polarity_rejected_without_repl` (a WRONG polarity
    string) -- this is polarity simply absent (`ProposedFact`'s own default). Same reason code
    either way (`fact.polarity not in ("accept", "reject")` catches both `None` and a typo
    identically), which is why this is filed under `MALFORMED_MISSING_FIELD`'s sibling
    `MALFORMED_BAD_POLARITY`, not a dedicated missing-polarity code -- there isn't one."""
    fact = ProposedFact(id="no_polarity", type="membership", mechanism="decide", statement="whatever", instance="(0)", expected_type="Nat")
    assert fact.polarity is None
    outcome = validate_membership_fact(None, None, fact, CLOG_DOMAIN)
    assert outcome.verdict is Verdict.REJECTED
    assert outcome.reason_code == ReasonCode.MALFORMED_BAD_POLARITY


def test_casework_missing_domain_inputs_binding_is_domain_undecided_not_missing_field():
    """`domain_inputs` absent (empty) for a casework fact does NOT produce
    `MALFORMED_MISSING_FIELD` -- `check_domain_containment`'s own documented design is `if not
    inputs: return "DOMAIN_UNDECIDED"` (verified by reading, not assumed), so this lands in
    the SAME flagged bucket as gap 3's genuinely-undecidable-predicate case. No REPL round-trip
    happens either way: the empty-inputs short circuit fires before any command is sent."""
    fact = ProposedFact(id="no_domain_inputs", type="casework", mechanism="decide", statement="example : Nat.clog 2 37 = 6 := by decide")
    assert fact.domain_inputs == {}
    outcome = validate_casework_fact(None, None, fact, CLOG_DOMAIN)
    assert outcome.verdict is Verdict.FLAGGED
    assert outcome.reason_code == ReasonCode.DOMAIN_UNDECIDED


# NOTE on the other two "missing field" cases the audit named:
# - missing `violated_property` on a reject-polarity fact: already covered by
#   `test_membership_missing_violated_property_rejected_without_repl` in
#   `test_authoring_validate.py` (MALFORMED_MISSING_VIOLATED_PROPERTY). Not duplicated here.
# - empty `anchors` on a global fact: already covered by
#   `test_global_missing_anchors_rejected_without_repl` in `test_authoring_validate.py`
#   (MALFORMED_MISSING_ANCHORS). Not duplicated here.


def test_casework_missing_statement_returns_malformed_missing_field():
    """An empty (missing) `statement` on a casework fact is guarded at the top of
    `_run_statement`, before `Command(cmd=fact.statement, ...)` is ever constructed --
    `lean_interact`'s `Command` model requires a non-empty string, so without the guard this
    would raise an uncaught `pydantic.ValidationError` instead of returning a
    `ValidationOutcome`. No REPL round-trip is needed to trigger the guard, since it fires
    before any request is sent -- hence `server=None` here (a `"True"` domain constraint
    short-circuits containment without touching it, matching `check_domain_containment`'s own
    documented fast path, so this test reaches the guard rather than failing earlier on
    `None.run(...)`)."""
    fact = ProposedFact(id="empty_statement", type="casework", mechanism="decide", statement="", domain_inputs={})
    outcome = validate_casework_fact(None, None, fact, TRUE_DOMAIN)
    assert outcome.verdict is Verdict.REJECTED
    assert outcome.reason_code == ReasonCode.MALFORMED_MISSING_FIELD


# === Gap 3: DOMAIN_UNDECIDED end-to-end (proposal -> containment check -> flagged bucket) =====


def test_domain_undecided_end_to_end_casework_lands_in_flagged_bucket(mathlib_env):
    server, env = mathlib_env
    fact = ProposedFact(
        id="undecided_casework", type="casework", mechanism="decide",
        statement="example : True := trivial", domain_inputs={"f": ["(fun x : ℝ => x)"]},
    )
    run = validate_facts(server, env, [fact], UNDECIDABLE_DOMAIN, "irrelevant")
    outcome = run.outcomes[0]
    assert outcome.verdict is Verdict.FLAGGED
    assert outcome.reason_code == ReasonCode.DOMAIN_UNDECIDED
    assert outcome in run.flagged()
    assert outcome not in run.rejections()
    assert run.counts_by_verdict() == {"flagged": 1}


def test_domain_undecided_end_to_end_membership_lands_in_flagged_bucket(mathlib_env):
    server, env = mathlib_env
    fact = ProposedFact(
        id="undecided_membership", type="membership", mechanism="decide",
        statement="example : True := trivial", instance="(fun x : ℝ => x)", polarity="accept",
        expected_type="ℝ → ℝ", domain_inputs={"f": ["(fun x : ℝ => x)"]},
    )
    run = validate_facts(server, env, [fact], UNDECIDABLE_DOMAIN, "irrelevant")
    outcome = run.outcomes[0]
    assert outcome.verdict is Verdict.FLAGGED
    assert outcome.reason_code == ReasonCode.DOMAIN_UNDECIDED
    assert outcome in run.flagged()
    assert outcome not in run.rejections()


# === Adversarial-input minisuite: the kind of malformed content real LLM output produces =====


def test_adversarial_decide_mechanism_with_bare_prop_statement(mathlib_env):
    """`decide` mechanism, statement is a bare Prop (no `:=`, no `#`-command) -- schema v1.1's
    statement-format rule (`docs/design/task_schema_v1_1.md`) would catch this, but that rule
    lives in `harness.task_schema` (structural), not here (mechanical/semantic) -- see that
    doc's own "status of structural vs. semantic validation" split. What actually happens:
    submitted as-is, the bare Prop is not a valid top-level Lean COMMAND, so the REPL reports a
    parse error (`response.has_errors()` -- a normal FAILED, not a timeout/ERRORED), which
    `_run_statement` recognizes via the "expected command" substring and reports under
    `MALFORMED_UNPARSEABLE_STATEMENT`, distinct from a genuinely-false well-formed statement."""
    server, env = mathlib_env
    fact = ProposedFact(id="bare_prop", type="casework", mechanism="decide", statement="Nat.clog 2 37 = 6", domain_inputs={"b": ["2"], "n": ["37"]})
    outcome = validate_casework_fact(server, env, fact, CLOG_DOMAIN)
    assert outcome.verdict is Verdict.REJECTED
    assert outcome.reason_code == ReasonCode.MALFORMED_UNPARSEABLE_STATEMENT
    assert "expected command" in outcome.evidence["execution"]["detail"]


def test_adversarial_proof_mechanism_with_decide_shaped_statement(mathlib_env):
    """The reverse shape mismatch: `proof` mechanism (global fact), statement is a full
    `example ... := by decide` command instead of a bare Prop. `validate_global_fact` wraps
    the statement as `#check (STATEMENT : Prop)`; a command embedded inside a term-mode type
    ascription is a parse error, correctly surfaced as `PROPOSITION_DOES_NOT_ELABORATE` -- an
    honest, accurate description of what happened, not a misclassification."""
    server, env = mathlib_env
    fact = ProposedFact(
        id="wrong_shape_global", type="global", mechanism="proof",
        statement="example : Nat.clog 2 37 = 6 := by decide", anchors=["Nat.clog_pow"],
    )
    outcome = validate_global_fact(server, env, fact, CLOG_DOMAIN, CLOG_NAME)
    assert outcome.verdict is Verdict.REJECTED
    assert outcome.reason_code == ReasonCode.PROPOSITION_DOES_NOT_ELABORATE


def test_adversarial_statement_with_markdown_fence(mathlib_env):
    """LLM output routinely wraps code in ```lean fences -- if that text leaks into a proposed
    fact's statement verbatim, it must not crash the validator. It doesn't: the backtick lines
    are parse errors like any other malformed command, reported under
    `MALFORMED_UNPARSEABLE_STATEMENT` (same finding as the bare-Prop case above)."""
    server, env = mathlib_env
    fact = ProposedFact(
        id="markdown_fenced", type="casework", mechanism="decide",
        statement="```lean\nexample : Nat.clog 2 37 = 6 := by decide\n```",
        domain_inputs={"b": ["2"], "n": ["37"]},
    )
    outcome = validate_casework_fact(server, env, fact, CLOG_DOMAIN)
    assert outcome.verdict is Verdict.REJECTED
    assert outcome.reason_code == ReasonCode.MALFORMED_UNPARSEABLE_STATEMENT


def test_adversarial_domain_inputs_references_undeclared_domain_variable(mathlib_env):
    """A `domain_inputs` key that isn't one of `domain.variables` (schema v1.1 would reject
    this structurally) -- mechanically, the containment checker builds a lambda binding a
    variable the constraint never uses; the constraint's own free variables (`b`, `n`) are
    then unbound in that lambda body, which Lean reports as an error (not a crash), read by
    `_decide_bool` as "not decidable" -> DOMAIN_UNDECIDED. A safe, honest "can't tell" outcome
    for malformed input, not a false IN_DOMAIN/OUT_OF_DOMAIN claim."""
    server, env = mathlib_env
    fact = ProposedFact(
        id="undeclared_domain_var", type="casework", mechanism="decide",
        statement="example : Nat.clog 2 37 = 6 := by decide", domain_inputs={"z": ["5"]},
    )
    outcome = validate_casework_fact(server, env, fact, CLOG_DOMAIN)
    assert outcome.verdict is Verdict.FLAGGED
    assert outcome.reason_code == ReasonCode.DOMAIN_UNDECIDED


def test_adversarial_duplicate_fact_ids_validated_independently_no_crash_no_silent_drop(mathlib_env):
    """Duplicate `id`s across a proposed batch: uniqueness is a structural concern owned by
    `harness.task_schema` (confirmed: it has an explicit duplicate-id check; this module does
    not). `validate_facts` has no special handling either -- each fact is validated
    independently in order, so `ValidationRun.outcomes` legitimately contains two entries
    sharing one `fact_id`. Confirms this is safe (no crash, no cross-contamination between the
    two) rather than asserting this module ought to catch it -- it correctly doesn't."""
    server, env = mathlib_env
    true_fact = ProposedFact(id="dup", type="casework", mechanism="decide", statement="example : Nat.clog 2 37 = 6 := by decide", domain_inputs={"b": ["2"], "n": ["37"]})
    false_fact = ProposedFact(id="dup", type="casework", mechanism="decide", statement="example : Nat.clog 2 37 = 5 := by decide", domain_inputs={"b": ["2"], "n": ["37"]})
    run = validate_facts(server, env, [true_fact, false_fact], CLOG_DOMAIN, CLOG_NAME)
    assert len(run.outcomes) == 2
    assert run.outcomes[0].fact_id == run.outcomes[1].fact_id == "dup"
    assert run.outcomes[0].verdict is Verdict.ACCEPTED
    assert run.outcomes[0].reason_code == ReasonCode.CERTIFIED_TRUE_OF_GROUND_TRUTH
    assert run.outcomes[1].verdict is Verdict.REJECTED
    assert run.outcomes[1].reason_code == ReasonCode.FALSE_OF_GROUND_TRUTH


# === Gap 1: ERRORED (validation infrastructure failure, not the fact being wrong) ============
#
# These two tests genuinely trigger a REPL timeout and must run LAST in this module -- see the
# module docstring for why (a timeout-induced server restart invalidates `env` for anything
# that runs after it in the same shared `mathlib_env`).


def test_casework_execution_error_is_errored_not_false(mathlib_env):
    """A statement that genuinely errors during validation (REPL timeout, here) must come back
    ERRORED, never `FALSE_OF_GROUND_TRUTH` -- confusing the two would report a candidate-side
    infrastructure failure as "the fact is mathematically wrong," poisoning authoring
    statistics. Reuses `test_admissibility.py`'s own confirmed-slow expression (`∀ n < 500000`
    with `maxRecDepth` raised) rather than inventing a new one, since that shape was already
    verified empirically to run long rather than fast-failing."""
    server, env = mathlib_env
    fact = ProposedFact(
        id="errored_casework", type="casework", mechanism="decide",
        statement="set_option maxRecDepth 4000000 in example : ∀ n < 500000, n + 0 = n := by decide",
        domain_inputs={"b": ["2"], "n": ["2"]},
    )
    outcome = validate_casework_fact(server, env, fact, CLOG_DOMAIN, timeout=2.0)
    assert outcome.verdict is Verdict.REJECTED
    assert outcome.reason_code == ReasonCode.ERRORED


def test_membership_instance_elaboration_error_is_errored_not_does_not_elaborate(mathlib_env):
    """Same concern as the casework case above, for the membership instance-elaboration check
    specifically -- a timeout there must be reported as validation infrastructure failing
    (`ERRORED`), not as the instance being malformed (`INSTANCE_DOES_NOT_ELABORATE`). Uses a
    deliberately expensive `expected_type` (nested `Nat.rec` unfolding) to force a slow
    elaboration under a short timeout; confirmed empirically to reproduce the timeout reliably
    before writing this test."""
    server, env = mathlib_env
    fact = ProposedFact(
        id="errored_membership", type="membership", mechanism="decide",
        statement="example : True := trivial", instance="(2:Nat)", polarity="accept",
        expected_type="Fin (Nat.rec (motive := fun _ => Nat) 1 (fun _ ih => ih * 2) 400000)",
    )
    outcome = validate_membership_fact(server, env, fact, TRUE_DOMAIN, timeout=2.0)
    assert outcome.verdict is Verdict.REJECTED
    assert outcome.reason_code == ReasonCode.ERRORED
