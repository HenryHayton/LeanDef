"""Tests for ladder.tier3 -- the real hammer tier. Box-only (`docs/ec2_runbook.md` Phase G.4):
needs the EC2 box's Hammer-enabled Lean project (`~/verifier-lean`) and the patched local REPL
checkout (`~/patched-repl`, `lean/repl_main.ec2.lean`'s `--load-dynlib` fix) -- neither exists
on the Mac. Statements are the runbook's own smoke-test goals (`~/verifier-lean/smoke_goals/`),
converted to bare-Prop canonical form (schema v1.1 §3.1's proof-mechanism statement shape).

The cache write-on-box / replay-on-Mac test is split across two functions in this file: the
box-side half writes the cache entry to the synced repo's cache path; a companion check in
`tests/test_ladder_tier3_replay_on_mac.py` (Mac-only, run manually after syncing the cache
file back) replays it there -- see that file's own docstring for why this can't be one
end-to-end test given the two environments never share a live process.
"""

import os
from pathlib import Path

import pytest
from lean_interact import AutoLeanServer, Command, LeanREPLConfig, LocalProject

from harness.results import CheckStatus
from ladder.axiom_audit import audit_proof_axioms
from ladder.budgets import DEFAULT_LADDER_BUDGETS
from ladder.cache import CacheEntry, ProofScriptCache, statement_hash, toolchain_pin
from ladder.statuses import AdjudicationStatus
from ladder.tier3 import adjudicate_tier3_hammer

pytestmark = pytest.mark.box_only

VERIFIER_LEAN_DIR = Path.home() / "verifier-lean"
PATCHED_REPL_DIR = Path.home() / "patched-repl"
DYNLIB_PATH = VERIFIER_LEAN_DIR / ".lake" / "packages" / "cvc5" / ".lake" / "build" / "lib" / "libcvc5_cvc5.so"
BOX_CACHE_PATH = Path.home() / "definition-verifier" / "ladder" / "output" / "tier3_test_cache.jsonl"


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


def test_goal1_add_comm_discharges(hammer_env):
    server, env = hammer_env
    result = adjudicate_tier3_hammer(server, env, "g1", "∀ (a b : Nat), a + b = b + a", [], DEFAULT_LADDER_BUDGETS)
    assert result.winning is not None
    assert result.winning.status is AdjudicationStatus.CERTIFIED


def test_goal2_list_length_append_discharges(hammer_env):
    server, env = hammer_env
    result = adjudicate_tier3_hammer(
        server, env, "g2", "∀ (l1 l2 : List Nat), (l1 ++ l2).length = l1.length + l2.length", [],
        DEFAULT_LADDER_BUDGETS,
    )
    assert result.winning is not None


def test_goal3_monotone_succ_discharges_crash_free(hammer_env):
    """The exact goal that historically SIGABRTed without the --load-dynlib fix
    (`docs/ec2_runbook.md` Phase C.7) -- reaching this assertion at all (not a hard process
    crash mid-test-run) is itself part of what this test verifies."""
    server, env = hammer_env
    result = adjudicate_tier3_hammer(server, env, "g3", "Monotone (fun n : Nat => n + 1)", [], DEFAULT_LADDER_BUDGETS)
    assert result.winning is not None
    assert result.winning.status is AdjudicationStatus.CERTIFIED


def test_goal5_eventually_constant_fails_gracefully(hammer_env):
    """A genuinely hard fact (runbook changelog: "1/7 failed gracefully... not a defect") --
    UNKNOWN, not a crash and not ENV_DEATH."""
    server, env = hammer_env
    statement = (
        "∀ {f : Nat → Nat}, Monotone f → ∀ {c : Nat}, (∀ n, f n ≤ c) → ∃ b N, ∀ n ≥ N, f n = b"
    )
    result = adjudicate_tier3_hammer(server, env, "g5", statement, [], DEFAULT_LADDER_BUDGETS)
    assert result.winning is None
    assert result.attempts[0].status in (AdjudicationStatus.UNKNOWN, AdjudicationStatus.ERRORED)
    assert result.attempts[0].status is not AdjudicationStatus.ENV_DEATH


def test_goal7_linear_arithmetic_discharges_via_cvc5(hammer_env):
    server, env = hammer_env
    result = adjudicate_tier3_hammer(
        server, env, "g7", "∀ (x y : Int), x + y ≤ 10 → y ≥ 0 → x ≤ 10", [], DEFAULT_LADDER_BUDGETS,
    )
    assert result.winning is not None


def test_cache_round_trip_of_a_hammer_found_script(hammer_env):
    """Writes a real tier-3-discharged proof script into the cache, at the SAME toolchain pin
    the Mac computes by default (both read the identical, rsync'd `lean/lean-toolchain` +
    `lean/lake-manifest.json` content) -- this is the entry
    `tests/test_ladder_tier3_replay_on_mac.py` replays after a sync-back, proving "search
    happens once, on the box; replay runs anywhere" for real, not just for tier 2."""
    server, env = hammer_env
    statement = "∀ (a b : Nat), a + b = b + a"
    result = adjudicate_tier3_hammer(server, env, "cache_rt", statement, [], DEFAULT_LADDER_BUDGETS)
    assert result.winning is not None

    audit = audit_proof_axioms(server, result.env, result.winning_theorem_name)
    assert audit.passed

    cache = ProofScriptCache(path=BOX_CACHE_PATH)
    entry = CacheEntry(
        statement_hash=statement_hash(statement), toolchain_pin=toolchain_pin(), tier=3,
        script=result.winning_script, axiom_closure=sorted(audit.axioms), wall_clock_s=result.winning.elapsed_s,
        canonical_statement=statement,
    )
    cache.put(entry)

    reloaded = ProofScriptCache(path=BOX_CACHE_PATH)
    got = reloaded.get(statement, toolchain_pin())
    assert got == entry
