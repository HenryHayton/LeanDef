"""Tests for miner.discharge -- the tier-2 discharge measurement (batch-4 "wide mine" task).

The pure matching/serialization logic (`find_mentioning_statements`, `write_discharge_manifest`)
is tested with synthetic data, no REPL. The tactic-ladder behavior
(`attempt_statement`/`measure_discharge_for_definition`) needs a real, Mathlib-imported warm
environment -- there's no ground truth to fake for "does this tactic actually discharge this
goal" -- so those tests share the same module-scoped `mathlib_env` fixture pattern
`tests/test_authoring_validate.py` established.
"""

import json

import pytest
from lean_interact.interface import CommandResponse, LeanError, Message, Pos

from harness.repl import get_warm_environment
from harness.results import CheckStatus
from miner import config as miner_cfg
from miner.discharge import (
    DefinitionDischarge,
    StatementDischarge,
    TacticAttempt,
    _as_example,
    _attempt_statement_with_recovery,
    _looks_like_env_death,
    attempt_statement,
    find_mentioning_statements,
    measure_discharge,
    measure_discharge_for_definition,
    write_discharge_manifest,
)
from miner.rank import ManifestRecord
from miner.verify import VerifiedDef


def _error_message(data: str) -> Message:
    return Message(start_pos=Pos(line=1, column=1), end_pos=None, severity="error", data=data)


class _FakeServer:
    """Same scripted-fake-server pattern as `tests/test_miner_verify_recovery.py`'s
    `_FakeServer`: one scripted response per `.run()` call, in order, `AssertionError` if
    exhausted. Used here to force a deterministic "Unknown environment" death partway through
    a measurement -- not practical to trigger reliably against a real Lean REPL."""

    def __init__(self, script: list):
        self.script = list(script)
        self.calls: list[tuple[str, object]] = []

    def run(self, request, timeout=None):
        self.calls.append((request.cmd, request.env))
        if not self.script:
            raise AssertionError(f"fake server ran out of scripted responses at call: {request.cmd!r}")
        return self.script.pop(0)


@pytest.fixture(scope="module")
def mathlib_env():
    server, import_result = get_warm_environment()
    assert import_result.status is CheckStatus.PASSED, import_result.detail
    yield server, import_result.env
    server.kill()


# --- find_mentioning_statements: pure, no REPL ------------------------------------------------


def test_find_mentioning_statements_qualified_match():
    records = [("theorem foo : Nat.clog 2 3 = 2", ""), ("theorem qux : True", "")]
    assert find_mentioning_statements("Nat.clog", records) == ["theorem foo : Nat.clog 2 3 = 2"]


def test_find_mentioning_statements_namespace_scoped_bare_match():
    records = [
        ("theorem bar : clog 2 3 = 2", "Nat"),  # bare, matching namespace -- counts
        ("theorem baz : clog 2 3 = 2", "Int"),  # bare, wrong namespace -- must not count
    ]
    assert find_mentioning_statements("Nat.clog", records) == ["theorem bar : clog 2 3 = 2"]


def test_find_mentioning_statements_preserves_scan_order():
    records = [(f"theorem t{i} : Nat.clog 2 {i} = 0", "") for i in range(5)]
    assert find_mentioning_statements("Nat.clog", records) == [r[0] for r in records]


# --- _as_example: pure, no REPL ---------------------------------------------------------------


def test_as_example_rewrites_a_real_theorem_header():
    statement = "theorem clog_pow (b x : ℕ) (hb : 1 < b) :\n    Nat.clog b (b ^ x) = x"
    assert _as_example(statement) == "example (b x : ℕ) (hb : 1 < b) :\n    Nat.clog b (b ^ x) = x"


def test_as_example_rewrites_a_lemma_header():
    assert _as_example("lemma foo (n : ℕ) : n = n") == "example (n : ℕ) : n = n"


def test_as_example_wraps_a_bare_proposition():
    assert _as_example("Nat.clog 2 (2 ^ 3) = 3") == "example : Nat.clog 2 (2 ^ 3) = 3"


# --- attempt_statement / measure_discharge_for_definition: live REPL --------------------------


def test_attempt_statement_discharged_by_first_tactic_stops_ladder(mathlib_env):
    server, env = mathlib_env
    result = attempt_statement(server, env, "Nat.clog 2 (2 ^ 3) = 3")
    assert result.discharged
    assert result.winning_tactic == "rfl"
    assert len(result.attempts) == 1  # ladder stopped -- omega/simp/... never attempted


def test_attempt_statement_falls_through_to_a_later_tactic(mathlib_env):
    server, env = mathlib_env
    result = attempt_statement(server, env, "∀ (l : List ℕ), l ++ [] = l")
    assert result.discharged
    assert result.attempts[0].tactic == "rfl"
    assert result.attempts[0].status == "not_discharged"
    assert result.winning_tactic in ("simp", "exact?", "aesop")


def test_attempt_statement_not_discharged_tries_every_tactic(mathlib_env):
    server, env = mathlib_env
    result = attempt_statement(server, env, "∀ n : ℕ, n = n + 1")
    assert not result.discharged
    assert result.winning_tactic is None
    assert [a.tactic for a in result.attempts] == miner_cfg.TACTIC_LADDER
    assert all(a.status in ("not_discharged", "errored") for a in result.attempts)


def test_measure_discharge_for_definition_samples_up_to_limit(mathlib_env):
    server, env = mathlib_env
    records = [(f"theorem t{i} : Nat.clog 2 (2 ^ {i}) = {i}", "") for i in range(5)]
    result, returned_env = measure_discharge_for_definition(server, env, "Nat.clog", 5, records, sample_size=3)
    assert result.name == "Nat.clog"
    assert result.theorem_mention_count == 5
    assert result.statements_sampled == 3
    assert result.attempted == 3
    assert result.discharged == 3
    assert result.winning_tactic_counts == {"rfl": 3}
    assert len(result.per_statement) == 3
    assert returned_env == env  # no recovery needed -- environment never died


# --- environment-death recovery: scripted fake server, no real REPL ---------------------------


def test_looks_like_env_death():
    assert _looks_like_env_death("LeanError: Unknown environment.")
    assert not _looks_like_env_death("Tactic `rfl` failed: ...")


def test_attempt_statement_recovery_reimports_and_retries_after_env_death():
    dead = LeanError(message="Unknown environment.")
    script = (
        [dead, dead] * 5  # every tactic in the ladder errors twice (run_checked's own retry) against the dead env
        + [CommandResponse(env=99, messages=[])]  # warm_import's reimport succeeds, fresh env 99
        + [CommandResponse(env=99, messages=[])]  # statement retried against env 99 -- rfl succeeds this time
    )
    server = _FakeServer(script)

    outcome, new_env = _attempt_statement_with_recovery(
        server, 1, "Nat.clog 2 (2 ^ 3) = 3",
        tactics=miner_cfg.TACTIC_LADDER, timeout=5.0, imports=None, warmup_timeout=5.0,
    )

    assert new_env == 99
    assert outcome.discharged
    assert outcome.winning_tactic == "rfl"

    import_calls = [c for c in server.calls if c[0] == "import Mathlib"]
    assert len(import_calls) == 1  # reimport actually happened

    retry_calls = [c for c in server.calls if c[1] == 99 and "Nat.clog" in c[0]]
    assert len(retry_calls) == 1  # retried statement checked against the NEW env, not the dead one


def test_attempt_statement_no_recovery_when_env_is_alive():
    """A genuine tactic failure (not an env death) must not trigger a reimport at all."""
    ordinary_failure = CommandResponse(env=1, messages=[_error_message("some ordinary tactic failure")])
    script = [ordinary_failure] * len(miner_cfg.TACTIC_LADDER)
    server = _FakeServer(script)

    outcome, new_env = _attempt_statement_with_recovery(
        server, 1, "Nat.clog 2 (2 ^ 3) = 3",
        tactics=miner_cfg.TACTIC_LADDER, timeout=5.0, imports=None, warmup_timeout=5.0,
    )

    assert new_env == 1  # unchanged -- no recovery triggered
    assert not outcome.discharged
    assert not any(c[0] == "import Mathlib" for c in server.calls)


# --- measure_discharge: skip behavior needs no REPL at all ------------------------------------


def _stub_verified(name: str) -> VerifiedDef:
    return VerifiedDef(name=name, module_path="Stub.lean", source_text="def stub := 0", docstring=None, mention_count=0, included=True)


def _stub_record(name: str) -> ManifestRecord:
    return ManifestRecord(
        name=name, module_path="Stub.lean", eligible=True, exclusion_reason="", gates_failed=[],
        rank=1, return_shape="value", verified=_stub_verified(name), proxies=None, richness=None,
        docstring_substance=None, score=None,
    )


def test_measure_discharge_skips_zero_mention_records_without_touching_repl():
    record = _stub_record("Foo.bar")
    results = measure_discharge(None, None, [record], theorem_mention_counts={}, statement_records=[])
    assert results == []


def test_measure_discharge_stops_at_wall_clock_cutoff():
    """A `max_wall_clock_s` of 0 must still let the definition already in progress finish
    (the deadline is only checked *after* each definition completes), but must not start a
    second one -- guarantees an overnight run terminates instead of running unboundedly."""
    records = [_stub_record(f"Foo.bar{i}") for i in range(3)]
    counts = {r.name: 1 for r in records}
    statement_records = [(f"theorem t{i} : Foo.bar{i} = 1", "") for i in range(3)]
    script = [CommandResponse(env=1, messages=[]) for _ in range(3)]  # each rfl succeeds immediately
    server = _FakeServer(script)

    results = measure_discharge(server, 1, records, counts, statement_records, max_wall_clock_s=0.0)

    assert len(results) == 1
    assert results[0].name == "Foo.bar0"


def test_measure_discharge_calls_on_progress_for_each_definition():
    records = [_stub_record(f"Foo.bar{i}") for i in range(2)]
    counts = {r.name: 1 for r in records}
    statement_records = [(f"theorem t{i} : Foo.bar{i} = 1", "") for i in range(2)]
    script = [CommandResponse(env=1, messages=[]) for _ in range(2)]
    server = _FakeServer(script)

    seen = []
    measure_discharge(
        server, 1, records, counts, statement_records,
        on_progress=lambda i, total, result: seen.append((i, total, result.name)),
    )

    assert seen == [(1, 2, "Foo.bar0"), (2, 2, "Foo.bar1")]


# --- write_discharge_manifest: pure JSONL round trip ------------------------------------------


def test_write_discharge_manifest_round_trips(tmp_path):
    result = DefinitionDischarge(
        name="Foo.bar",
        theorem_mention_count=3,
        statements_sampled=1,
        attempted=1,
        discharged=1,
        winning_tactic_counts={"rfl": 1},
        per_statement=[
            StatementDischarge(
                statement="Foo.bar = 1",
                attempts=[TacticAttempt(tactic="rfl", status="discharged", elapsed_s=0.01)],
                discharged=True,
                winning_tactic="rfl",
            )
        ],
    )
    path = tmp_path / "discharge.jsonl"
    write_discharge_manifest([result], path)
    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    data = json.loads(lines[0])
    assert data["name"] == "Foo.bar"
    assert data["per_statement"][0]["attempts"][0]["tactic"] == "rfl"
    assert data["winning_tactic_counts"] == {"rfl": 1}
