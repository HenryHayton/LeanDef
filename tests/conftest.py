"""Shared test fixtures.

**The Mathlib environment is shared across the whole session** (2026-08-04). It used to be a
module-scoped fixture copy-pasted, byte-identical, into 12 test files -- so a full run started
and killed a dozen independent ~2.5 GB Mathlib servers in sequence. That cost ~1 minute of cold
import each (most of the suite's runtime) and, more seriously, gave a dozen separate
opportunities to strand a 2.5 GB process if a run was interrupted. Stranded servers reparent to
launchd and are NOT reaped by `harness.repl._kill_stray_children` (which only reaps children of
the *current* process); six of them reached 15.8 GB of a 16 GB machine and forced a hard
restart. See `scripts/reap_repls.py` for the cleanup side of that story.

`mathlib_env` is deliberately **function-scoped over a session-scoped manager** rather than
simply session-scoped. A plain session-scoped fixture computes once and hands the same
`(server, env)` pair to every test forever, which makes recycling impossible: a test holding an
`env` id from before a recycle would be holding an id the new server has never heard of. The
manager instead resolves `(server, env)` at each test's setup, so it hands back the existing
warm server in the overwhelmingly common case and can transparently replace it when it must.
"""

import os
import sys

import psutil
import pytest
from lean_interact import AutoLeanServer, Command, LeanREPLConfig, LocalProject

from harness import config as cfg
from harness.repl import get_warm_environment, is_unknown_environment_error, run_checked
from harness.results import CheckStatus

# Recycling thresholds for the shared server. A session-scoped server lives far longer than any
# module-scoped one did, and 2026-08-04 showed a single server ballooning, so long life needs a
# ceiling that per-module churn used to supply for free.
#
# **Keyed on GROWTH FROM BASELINE, not an absolute number** -- measured the hard way. A first
# attempt used a flat 5 GB cap on the reasoning that a warm Mathlib import "measures ~2.5 GB"
# (CLAUDE.md). It does not: a healthy warm server on this machine reads **5.7 GB RSS**, because
# Mathlib mmaps gigabytes of `.olean` files and RSS counts those mapped pages. The flat cap
# therefore sat BELOW the normal working set and fired on literally every test, so every test
# paid a fresh ~60 s cold import -- the exact opposite of what sharing a server is for.
#
# Growth-relative is also the more honest test of the thing we actually fear: "ballooning" means
# growing well past where a healthy server sits, and that is machine-independent in a way a flat
# GB number never is (the EC2 box has the same oleans and far more RAM).
MATHLIB_SERVER_GROWTH_FACTOR = 1.5   # recycle at 1.5x the post-warm baseline
MATHLIB_SERVER_ABSOLUTE_CAP_GB = 10.0  # backstop, in case the baseline measurement is itself bad


@pytest.fixture(scope="session")
def lean_server():
    config = LeanREPLConfig(project=LocalProject(directory=str(cfg.LEAN_PROJECT_DIR)), verbose=False)
    # Dev machines are often near AutoLeanServer's default 80% system-memory guard from
    # unrelated apps; these tests don't import Mathlib, so actual usage stays low regardless.
    server = AutoLeanServer(config, max_total_memory=cfg.MAX_TOTAL_MEMORY)
    yield server
    server.kill()


class _MathlibEnvManager:
    """Owns the one shared warm Mathlib server for the session.

    Recycles on any of three conditions, checked at each test's setup:

    1. **Nothing started yet** -- the first test to ask pays the cold import.
    2. **The server is not alive** -- something killed it (a genuine REPL timeout, an OOM). The
       next test must not be handed a corpse; without this check one dying test would cascade
       into every subsequent Mathlib test failing with "Unknown environment."
    3. **RSS over `MATHLIB_SERVER_RSS_CAP_GB`** -- the ceiling described in the module docstring.
    """

    def __init__(self):
        self._server = None
        self._env = None
        self._baseline_gb = None  # RSS measured just after the warm import, per server

    @staticmethod
    def _rss_gb() -> float:
        """Best-effort RSS of our subprocess tree (the REPL is a child). Returns 0.0 if it
        can't be read -- an unreadable measurement must not be treated as "over the cap" and
        trigger an endless recycle loop."""
        try:
            proc = psutil.Process(os.getpid())
            return sum(c.memory_info().rss for c in proc.children(recursive=True)) / (1024**3)
        except (psutil.Error, OSError):
            return 0.0

    def _needs_recycle(self) -> str | None:
        if self._server is None:
            return "first use"
        try:
            if not self._server.is_alive():
                return "server died"
        except Exception:  # noqa: BLE001 -- a server too broken to answer is a dead server
            return "server unresponsive"

        # Liveness is NOT enough, and assuming it was cost 70 test failures on 2026-08-05.
        # `AutoLeanServer` self-heals: when the REPL dies it silently restarts on the next call,
        # so `is_alive()` reports True again -- but every environment id from before the restart
        # is gone, and requests against them fail with "Unknown environment". A stale env handed
        # to the next test poisons it, and with ONE session-scoped server that poisons every
        # remaining test rather than (as module scope used to bound it) one file's worth.
        #
        # So probe the env itself, not just the process. A trivial command against a warm server
        # is sub-millisecond, which is nothing next to the ~40 s cold import it protects against
        # paying unnecessarily -- or the whole-session cascade it prevents.
        probe = run_checked(
            self._server, Command(cmd="example : True := trivial", env=self._env), timeout=30.0
        )
        if is_unknown_environment_error(probe.detail or ""):
            return "environment was invalidated by a server restart"
        rss = self._rss_gb()
        if rss > MATHLIB_SERVER_ABSOLUTE_CAP_GB:
            return f"RSS {rss:.1f}GB over the {MATHLIB_SERVER_ABSOLUTE_CAP_GB}GB backstop"
        if self._baseline_gb and rss > self._baseline_gb * MATHLIB_SERVER_GROWTH_FACTOR:
            return f"RSS {rss:.1f}GB is {rss / self._baseline_gb:.1f}x the {self._baseline_gb:.1f}GB baseline"
        return None

    def get(self):
        reason = self._needs_recycle()
        if reason is not None:
            # Announced on stderr, not silent: a recycle costs ~60 s of cold import, so a run
            # that is unexpectedly slow should say why rather than leave it to be guessed at.
            print(f"[mathlib_env] starting fresh server ({reason})", file=sys.stderr, flush=True)
            self.close()
            server, import_result = get_warm_environment()
            assert import_result.status is CheckStatus.PASSED, import_result.detail
            self._server, self._env = server, import_result.env
            self._baseline_gb = self._rss_gb()
        return self._server, self._env

    def close(self):
        self._baseline_gb = None
        if self._server is not None:
            try:
                self._server.kill()
            except Exception:  # noqa: BLE001 -- teardown must not mask a test failure
                pass
        self._server, self._env = None, None


@pytest.fixture(scope="session")
def _mathlib_manager():
    manager = _MathlibEnvManager()
    yield manager
    manager.close()


@pytest.fixture
def mathlib_env(_mathlib_manager):
    """`(server, env)` for a warm Mathlib environment, shared across the session.

    A test module that must poison or kill its server -- `test_authoring_validate_hardening.py`
    deliberately induces a REPL timeout to exercise a real failure path -- defines its OWN
    module-scoped `mathlib_env`, which shadows this one for that module. That is the supported
    escape hatch, and it is why the manager also checks liveness rather than trusting callers.
    """
    return _mathlib_manager.get()


def pytest_collection_modifyitems(items):
    """Mark every test that requests `mathlib_env` with the `mathlib` marker.

    Applied by fixture use rather than written into each module, for two reasons. It is
    PRECISE: several modules mix a handful of Mathlib-backed tests with dozens of fast
    fake-server ones (`test_candidate_splice_parity.py` is 4 slow and 17 fast), and a
    module-level `pytestmark` would deselect the fast majority along with the slow few. And it
    is SELF-MAINTAINING: a new Mathlib-backed test is marked the moment it asks for the
    fixture, so the default fast suite cannot silently acquire a 1-minute cold import because
    someone forgot a decorator.
    """
    for item in items:
        if "mathlib_env" in getattr(item, "fixturenames", ()):
            item.add_marker("mathlib")
