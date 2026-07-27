"""Tests for ladder.cache -- the proof-script cache (reward doc §3.2).

`statement_hash`/`toolchain_pin` are pure. `ProofScriptCache.put`/`.get` are pure (no REPL --
they just index/persist `CacheEntry` records). `replay` needs a real warm environment, since
it runs the cached script as a genuine kernel check.
"""

import pytest

from harness.repl import get_warm_environment
from harness.results import CheckStatus
from ladder.cache import CacheEntry, ProofScriptCache, replay, statement_hash, toolchain_pin


@pytest.fixture(scope="module")
def mathlib_env():
    server, import_result = get_warm_environment()
    assert import_result.status is CheckStatus.PASSED, import_result.detail
    yield server, import_result.env
    server.kill()


def test_statement_hash_is_stable_and_whitespace_insensitive():
    a = statement_hash("Nat.clog 2 37 = 6")
    b = statement_hash("  Nat.clog 2 37 = 6  ")
    c = statement_hash("Nat.clog 2 37 = 7")
    assert a == b
    assert a != c


def test_toolchain_pin_reads_real_repo_files():
    pin = toolchain_pin()
    assert pin.startswith("leanprover/lean4:")
    assert "@" in pin
    lean_part, mathlib_rev = pin.split("@", 1)
    assert mathlib_rev != "unknown"


def test_cache_put_then_get_round_trips(tmp_path):
    cache = ProofScriptCache(path=tmp_path / "cache.jsonl")
    entry = CacheEntry(
        statement_hash=statement_hash("(1:Nat) + 1 = 2"),
        toolchain_pin="pin-a",
        tier=2,
        script="by omega",
        axiom_closure=["propext"],
        wall_clock_s=0.5,
        canonical_statement="(1:Nat) + 1 = 2",
    )
    cache.put(entry)
    got = cache.get("(1:Nat) + 1 = 2", "pin-a")
    assert got == entry
    assert cache.get("(1:Nat) + 1 = 2", "pin-b") is None  # different toolchain pin -> miss


def test_cache_reloads_from_disk(tmp_path):
    path = tmp_path / "cache.jsonl"
    cache = ProofScriptCache(path=path)
    entry = CacheEntry(
        statement_hash=statement_hash("True"),
        toolchain_pin="pin-a",
        tier=2,
        script="by trivial",
        axiom_closure=[],
        wall_clock_s=0.1,
        canonical_statement="True",
    )
    cache.put(entry)

    reloaded = ProofScriptCache(path=path)
    assert reloaded.get("True", "pin-a") == entry


def test_flag_for_research_appends_and_newest_wins_on_reload(tmp_path):
    path = tmp_path / "cache.jsonl"
    cache = ProofScriptCache(path=path)
    entry = CacheEntry(
        statement_hash=statement_hash("True"),
        toolchain_pin="pin-a",
        tier=2,
        script="by trivial",
        axiom_closure=[],
        wall_clock_s=0.1,
        canonical_statement="True",
    )
    cache.put(entry)
    cache.flag_for_research(entry)

    assert cache.get("True", "pin-a").flagged_for_research

    # append-only on disk: two lines for the same key, newest wins on reload.
    lines = path.read_text().strip().splitlines()
    assert len(lines) == 2
    reloaded = ProofScriptCache(path=path)
    assert reloaded.get("True", "pin-a").flagged_for_research


def test_replay_a_valid_cached_script_passes(mathlib_env):
    server, env = mathlib_env
    entry = CacheEntry(
        statement_hash=statement_hash("(1:Nat) + 1 = 2"),
        toolchain_pin="pin-a",
        tier=2,
        script="by omega",
        axiom_closure=["propext"],
        wall_clock_s=0.5,
        canonical_statement="(1:Nat) + 1 = 2",
    )
    check = replay(entry, server, env)
    assert check.status is CheckStatus.PASSED


def test_replay_a_poisoned_script_fails(mathlib_env):
    server, env = mathlib_env
    entry = CacheEntry(
        statement_hash=statement_hash("(1:Nat) + 1 = 2"),
        toolchain_pin="pin-a",
        tier=2,
        script="by nonexistent_tactic_xyz",  # deliberately broken/poisoned script
        axiom_closure=["propext"],
        wall_clock_s=0.5,
        canonical_statement="(1:Nat) + 1 = 2",
    )
    check = replay(entry, server, env)
    assert check.status is not CheckStatus.PASSED
