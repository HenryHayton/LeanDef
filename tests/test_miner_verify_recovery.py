"""Unit test for miner.verify's environment-death recovery, using a fake server that
returns scripted `lean_interact` response objects -- no real REPL involved.

This exercises a real bug found during this stage's own first full-corpus harvest run: one
slow check triggered a server restart, which invalidated the shared base environment, and
every subsequent candidate then failed with a misleading "Unknown environment" error rather
than a genuine "does not elaborate." See miner.verify.verify_all_with_recovery's docstring.
"""

from lean_interact.interface import CommandResponse, LeanError, Message, Pos

from miner.scan import ScanHit
from miner.verify import _looks_like_env_death, verify_all_with_recovery


def _error_message(data: str) -> Message:
    return Message(start_pos=Pos(line=1, column=1), end_pos=None, severity="error", data=data)


class _FakeServer:
    """Returns one scripted response per `.run()` call, in order, and records
    `(cmd, env)` for each call so the test can inspect exactly what was sent."""

    def __init__(self, script: list):
        self.script = list(script)
        self.calls: list[tuple[str, object]] = []

    def run(self, request, timeout=None):
        self.calls.append((request.cmd, request.env))
        if not self.script:
            raise AssertionError(f"fake server ran out of scripted responses at call: {request.cmd!r}")
        return self.script.pop(0)


def test_looks_like_env_death():
    assert _looks_like_env_death("does not elaborate: LeanError: Unknown environment.")
    assert not _looks_like_env_death("does not elaborate: unknown identifier 'foo'")


def test_recovery_reimports_and_continues_with_new_env():
    hit1 = ScanHit(name="Foo.bar", module_path="Foo.lean", source_text="def bar := 1")
    hit2 = ScanHit(name="Baz.qux", module_path="Baz.lean", source_text="def qux := 2")

    script = [
        # hit1, `#check Foo.bar` against the original (dead) env: fails twice (run_checked
        # retries once on a LeanError before giving up), triggering recovery.
        LeanError(message="Unknown environment."),
        LeanError(message="Unknown environment."),
        # recovery: warm_import's `import Mathlib` succeeds against a NEW environment id.
        CommandResponse(env=99, messages=[]),
        # hit1 retried against the new env -- fails for an ordinary (non-death) reason, so
        # no second recovery attempt is triggered.
        CommandResponse(env=99, messages=[_error_message("unknown identifier 'bar'")]),
        # hit2 -- must be checked against the recovered env (99), not the original dead one.
        CommandResponse(env=99, messages=[_error_message("unknown identifier 'qux'")]),
    ]
    server = _FakeServer(script)

    results = verify_all_with_recovery(server, initial_base_env=1, hits=[hit1, hit2], timeout=5.0)

    assert len(results) == 2
    assert all(not r.included for r in results)
    # not misreported as environment death after recovery
    assert "Unknown environment" not in results[0].exclusion_reason

    # `import Mathlib` was actually sent once, to recover.
    import_calls = [c for c in server.calls if c[0] == "import Mathlib"]
    assert len(import_calls) == 1

    # hit2's #check must have used the recovered env (99), not the original dead one (1).
    hit2_calls = [c for c in server.calls if c[0] == "#check Baz.qux"]
    assert hit2_calls == [("#check Baz.qux", 99)]
