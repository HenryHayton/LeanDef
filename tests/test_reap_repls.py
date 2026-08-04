"""Tests for `scripts/reap_repls.py` -- the orphaned-REPL reaper.

The safety property is the whole point: this will run on a box hosting several legitimate
concurrent scoring workers, and killing a live worker's server would destroy hours of work. So
the tests that matter most are the NEGATIVE ones -- every way a process can look REPL-ish
without being a reapable orphan.

Both predicates are tested against fake process objects rather than real processes. Spawning a
genuine orphaned Mathlib server to test against would cost ~2.5 GB and a minute, and getting it
genuinely orphaned means deliberately doing the thing that caused the incident this script
exists to clean up after.
"""

import importlib.util
from pathlib import Path

import psutil
import pytest

_spec = importlib.util.spec_from_file_location(
    "reap_repls", Path(__file__).resolve().parent.parent / "scripts" / "reap_repls.py"
)
reap = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(reap)

# A real lean_interact launch line, as `subprocess.Popen` receives it (lean_interact/server.py).
REAL_REPL_CMD = (
    "/Users/x/.elan/bin/lake env /Users/x/proj/.venv/lib/python3.12/site-packages/lean_interact/"
    "cache/augustepoiroux/repl/repl_v1.3.18_lean-toolchain-v4.32.0/.lake/build/bin/repl"
)


class _FakeProc:
    def __init__(self, cmdline, ppid=1, pid=4242):
        self._cmdline = cmdline.split()
        self._ppid = ppid
        self.pid = pid

    def cmdline(self):
        return self._cmdline

    def ppid(self):
        return self._ppid


# --- condition 1: is it actually a lean_interact REPL? ------------------------------------------


def test_a_real_repl_launch_line_is_recognised():
    assert reap._is_lean_repl(_FakeProc(REAL_REPL_CMD))


@pytest.mark.parametrize(
    "cmdline,why",
    [
        ("/usr/libexec/replayd", "macOS `replayd` contains 'repl' and runs on every Mac"),
        ("/bin/zsh -c cd /Users/x/lean_interact/cache && ls", "mentions the cache path but is a shell"),
        ("python -m pytest tests/test_ladder_tier2.py", "a test file about the repl is not the repl"),
        ("/Users/x/replication/bin/replay --repl-mode", "'repl' as a substring of other words"),
        ("vim /Users/x/site-packages/lean_interact/cache/notes.txt", "editing a file under the cache"),
    ],
)
def test_processes_that_merely_look_repl_ish_are_not_matched(cmdline, why):
    assert not reap._is_lean_repl(_FakeProc(cmdline)), why


def test_the_binary_must_be_a_path_component_not_a_substring():
    """`.../build/bin/repl` qualifies; `.../build/bin/replay` must not."""
    almost = REAL_REPL_CMD.replace("/bin/repl", "/bin/replay")
    assert not reap._is_lean_repl(_FakeProc(almost))


def test_cache_marker_alone_is_insufficient():
    assert not reap._is_lean_repl(_FakeProc("/bin/cat /Users/x/lean_interact/cache/README"))


# --- condition 2: is it orphaned? ---------------------------------------------------------------


def test_reparented_to_init_is_an_orphan():
    assert reap._is_orphan(_FakeProc(REAL_REPL_CMD, ppid=1))


def test_a_live_workers_server_is_never_an_orphan(monkeypatch):
    """THE safety test. A scoring worker's server has that worker's live Python process as its
    parent, so it must never be reapable no matter how long it has been running."""
    monkeypatch.setattr(psutil, "pid_exists", lambda pid: True)
    assert not reap._is_orphan(_FakeProc(REAL_REPL_CMD, ppid=99999))


def test_a_process_whose_parent_has_vanished_is_an_orphan(monkeypatch):
    monkeypatch.setattr(psutil, "pid_exists", lambda pid: False)
    assert reap._is_orphan(_FakeProc(REAL_REPL_CMD, ppid=99999))


def test_unreadable_parent_is_not_treated_as_an_orphan():
    """Failing closed: if we cannot establish orphan status we must not kill."""

    class _Opaque(_FakeProc):
        def ppid(self):
            raise psutil.AccessDenied(self.pid)

    assert not reap._is_orphan(_Opaque(REAL_REPL_CMD))


def test_unreadable_cmdline_is_not_matched():
    class _Opaque(_FakeProc):
        def cmdline(self):
            raise psutil.AccessDenied(self.pid)

    assert not reap._is_lean_repl(_Opaque(REAL_REPL_CMD))


# --- the two conditions are conjunctive ---------------------------------------------------------


def test_both_conditions_are_required(monkeypatch):
    """A live REPL and an orphaned non-REPL must each be spared; only the conjunction reaps."""
    monkeypatch.setattr(psutil, "pid_exists", lambda pid: True)
    live_repl = _FakeProc(REAL_REPL_CMD, ppid=500)
    assert reap._is_lean_repl(live_repl) and not reap._is_orphan(live_repl)

    orphan_other = _FakeProc("/usr/libexec/replayd", ppid=1)
    assert reap._is_orphan(orphan_other) and not reap._is_lean_repl(orphan_other)


def test_find_orphans_on_a_clean_machine_returns_a_list():
    """Smoke: the real scan runs without raising on whatever is actually on this machine."""
    assert isinstance(reap.find_orphans(), list)
