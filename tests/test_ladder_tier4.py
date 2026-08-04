"""Tests for ladder.tier4 -- equivalence transfer. Box-only (`docs/ec2_runbook.md` Phase G.4):
the "genuinely different candidate" case exhausts tier 2 and falls through to tier 3 (real
hammer), which needs the box's Hammer-enabled environment, same as `test_ladder_tier3.py`.
"""

import os
from pathlib import Path

import pytest
from lean_interact import AutoLeanServer, Command, LeanREPLConfig, LocalProject

from ladder.budgets import DEFAULT_LADDER_BUDGETS
from ladder.statuses import AdjudicationStatus
from ladder.tier4 import adjudicate_tier4_equivalence

pytestmark = pytest.mark.box_only

VERIFIER_LEAN_DIR = Path.home() / "verifier-lean"
PATCHED_REPL_DIR = Path.home() / "patched-repl"
DYNLIB_PATH = VERIFIER_LEAN_DIR / ".lake" / "packages" / "cvc5" / ".lake" / "build" / "lib" / "libcvc5_cvc5.so"


@pytest.fixture(scope="module")
def hammer_env():
    os.environ["LEAN_INTERACT_LOAD_DYNLIB"] = str(DYNLIB_PATH)
    config = LeanREPLConfig(
        project=LocalProject(directory=str(VERIFIER_LEAN_DIR)),
        local_repl_path=str(PATCHED_REPL_DIR),
        build_repl=False,
        verbose=False,
    )
    server = AutoLeanServer(config, max_total_memory=0.95)
    resp = server.run(Command(cmd="import Hammer\nimport Mathlib"))
    yield server, resp.env
    server.kill()


def _declare(server: AutoLeanServer, env: int, cmd: str) -> int:
    check = server.run(Command(cmd=cmd, env=env))
    assert not check.has_errors(), check.get_errors()
    return check.env


def test_eta_expanded_alias_proves_equal_via_tier2(hammer_env):
    server, env = hammer_env
    truth_env = _declare(server, env, "def VTask_truth_double (n : Nat) : Nat := n + n")
    # eta/beta-expanded alias -- definitionally equal, the common case tier 4 exists for.
    candidate_env = _declare(server, truth_env, "def VTask_alias_double (n : Nat) : Nat := (fun m => m + m) n")

    result = adjudicate_tier4_equivalence(
        server, candidate_env, truth_env, "VTask_alias_double", "VTask_truth_double", DEFAULT_LADDER_BUDGETS,
    )

    assert result.winning is not None
    assert result.winning.status is AdjudicationStatus.CERTIFIED
    assert result.winning.tier in (2, 3)  # tier 2's rfl is expected to win; tier is whichever actually did


def test_genuinely_different_candidate_does_not_prove_equal(hammer_env):
    server, env = hammer_env
    truth_env = _declare(server, env, "def VTask_truth_double2 (n : Nat) : Nat := n + n")
    candidate_env = _declare(server, truth_env, "def VTask_wrong_double2 (n : Nat) : Nat := n + n + 1")

    result = adjudicate_tier4_equivalence(
        server, candidate_env, truth_env, "VTask_wrong_double2", "VTask_truth_double2", DEFAULT_LADDER_BUDGETS,
    )

    assert result.winning is None
    assert result.attempts  # both tiers were genuinely tried, not skipped
    assert all(a.status is not AdjudicationStatus.ENV_DEATH for a in result.attempts)
