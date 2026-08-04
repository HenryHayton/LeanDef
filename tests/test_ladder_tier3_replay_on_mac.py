"""Replays, on the Mac's plain (Hammer-free) Mathlib environment, a cache entry that
`tests/test_ladder_tier3.py` wrote on the EC2 box -- proving "search happens once, on the box;
replay runs anywhere" (reward doc §3.2) for tier 3 specifically, not just tier 2.

This is deliberately two separate test files rather than one end-to-end test: the box and the
Mac never share a live process (or even a live SSH session) within a single pytest run, so the
"write on box, sync, read on Mac" step is a real filesystem/network hop between them, not
something a single test function can express. Run `test_ladder_tier3.py` on the box, `rsync`
`ladder/output/tier3_test_cache.jsonl` back to the Mac (`docs/ec2_runbook.md` Phase G), then run
this file here.

Not marked `box_only` -- this is the Mac half specifically, and needs no box. Skips cleanly
(rather than failing) if the cache file hasn't been synced back yet, so a routine `uv run
pytest` on the Mac (no ladder Session B box work done recently) doesn't spuriously fail.
"""

from pathlib import Path

import pytest

from harness.results import CheckStatus
from ladder.cache import ProofScriptCache, replay, toolchain_pin


CACHE_PATH = Path(__file__).resolve().parent.parent / "ladder" / "output" / "tier3_test_cache.jsonl"


def test_tier3_cache_entry_replays_on_the_mac_without_hammer(mathlib_env):
    if not CACHE_PATH.exists():
        pytest.skip(f"{CACHE_PATH} not synced from the box yet -- see this file's docstring")

    server, env = mathlib_env
    cache = ProofScriptCache(path=CACHE_PATH)
    pin = toolchain_pin()  # same pin the box computed by default -- identical lean/ metadata

    entries = list(cache._entries.values())
    assert entries, f"{CACHE_PATH} exists but is empty"

    tier3_entries = [e for e in entries if e.tier == 3]
    assert tier3_entries, "expected at least one tier-3 cache entry from the box run"

    for entry in tier3_entries:
        assert entry.toolchain_pin == pin, "box and Mac disagree on the toolchain pin -- re-pin drift?"
        assert "hammer" not in entry.script.lower(), (
            f"cached script still re-invokes hammer ({entry.script!r}) -- not Mac-replayable by design; "
            "this cache entry should have used the reconstructed portable script"
        )
        check = replay(entry, server, env)
        assert check.status is CheckStatus.PASSED, f"replay failed on the Mac: {check.detail}"
