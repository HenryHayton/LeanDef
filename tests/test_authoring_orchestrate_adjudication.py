"""Tests for `authoring.orchestrate.adjudicate_proposed_facts` -- contract §6 rows 4-5. Needs
a real warm Mathlib environment (the mechanical verdict comes from `authoring.validate`, which
this module wraps). Kept out of `tests/test_authoring_orchestrate.py` for the same reason
`test_authoring_validate_hardening.py` is its own module: the second test here deliberately
triggers a genuine REPL timeout, which kills the underlying Lean server -- `AutoLeanServer`
self-heals on the next call but every environment id from before the restart is gone
(`harness.repl.run_checked`'s own documented caveat). This module's own `mathlib_env` fixture
instance is never shared with the fast, no-REPL orchestration tests, so a timeout here cannot
poison them.
"""

import pytest

from authoring.facts import ConventionPoint, DomainSpec, ProposedFact
from authoring.orchestrate import adjudicate_proposed_facts
from authoring.validate import ReasonCode
from harness.repl import get_warm_environment
from harness.results import CheckStatus

TRUE_DOMAIN = DomainSpec(
    constraint="True", variables=[], conventions=[ConventionPoint(point=None, statement=None, note="NONE_DECLARED: x")]
)


@pytest.fixture(scope="module")
def mathlib_env():
    server, import_result = get_warm_environment()
    assert import_result.status is CheckStatus.PASSED, import_result.detail
    yield server, import_result.env
    server.kill()


def test_adjudicate_accepts_true_facts_and_drops_false_ones_with_no_retry(mathlib_env):
    server, env = mathlib_env
    true_fact = ProposedFact(
        id="true1", type="casework", mechanism="decide",
        statement="example : (1 : Nat) + 1 = 2 := by decide", domain_inputs={},
    )
    false_fact = ProposedFact(
        id="false1", type="casework", mechanism="decide",
        statement="example : (1 : Nat) + 1 = 3 := by decide", domain_inputs={},
    )
    result = adjudicate_proposed_facts(server, env, [true_fact, false_fact], TRUE_DOMAIN, "irrelevant")
    assert [f.id for f in result.accepted] == ["true1"]
    assert len(result.dropped) == 1
    assert result.dropped[0].fact_id == "false1"
    assert result.dropped[0].reason_code == ReasonCode.FALSE_OF_GROUND_TRUTH
    assert result.task_errored == []


def test_adjudicate_provisionally_validated_global_fact_is_accepted(mathlib_env):
    server, env = mathlib_env
    global_fact = ProposedFact(
        id="g1", type="global", mechanism="proof",
        statement="Monotone (Nat.clog 2)", anchors=["Nat.clog_monotone"],
    )
    result = adjudicate_proposed_facts(server, env, [global_fact], TRUE_DOMAIN, "Nat.clog")
    assert [f.id for f in result.accepted] == ["g1"]
    assert result.dropped == []


def test_adjudicate_errored_fact_is_revalidated_once_then_flags_the_task(mathlib_env):
    """Deliberately triggers a genuine REPL timeout (same confirmed-slow expression
    `test_authoring_validate_hardening.py` uses) under a short timeout -- the first
    `validate_fact` call ERRORs for real; the mandated one-more-time re-run then hits a server
    that has self-healed but lost the old environment id, which also ERRORs -- exactly the
    "persistent ERRORED" case row 5 describes. Must run LAST in this module: the timeout kills
    the shared server, invalidating `env` for anything sharing this fixture afterward."""
    server, env = mathlib_env
    slow_fact = ProposedFact(
        id="slow1", type="casework", mechanism="decide",
        statement="set_option maxRecDepth 4000000 in example : ∀ n < 500000, n + 0 = n := by decide",
        domain_inputs={},
    )
    result = adjudicate_proposed_facts(server, env, [slow_fact], TRUE_DOMAIN, "irrelevant", timeout=2.0)
    assert result.accepted == []
    assert result.dropped == []
    assert len(result.task_errored) == 1
    assert result.task_errored[0].fact_id == "slow1"
    assert result.task_errored[0].reason_code == ReasonCode.ERRORED
