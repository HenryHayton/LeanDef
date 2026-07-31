"""Tests for `authoring.cleanup`: `_feedback_text`'s pure guardrail logic, plus real-REPL+stub
integration tests for `repair_one`/`run_cleanup` -- reuses `tests/test_authoring_pipeline.py`'s
own fixture shapes (real `Nat.clog`, `VTask.clog`) rather than importing them, matching this
test suite's existing convention of self-contained fixture files."""

import json

import pytest

from authoring.cleanup import CleanupRunResult, _feedback_text, repair_one, run_cleanup
from authoring.pipeline import DefinitionInput, PipelineConfig, StageRecord, TaskResult
from authoring.rotation_queue import (
    AGENT_FIXABLE,
    NOT_AGENT_FIXABLE,
    STATUS_ESCALATE_TO_HUMAN,
    STATUS_PENDING,
    STATUS_REPAIRED_AND_SHIPPED,
)
from authoring.task_symbol import task_symbol_for
from bedrock.client import BedrockClient
from harness.repl import get_warm_environment
from harness.results import CheckStatus
from harness.task_schema import validate_task_dir
from miner.harvest import MentionRecord
from tests.fixtures.bedrock_stub import ScriptedResponse, StubBedrockServer, success_body

DEF_NAME = "Nat.clog"
TASK_SYMBOL = task_symbol_for(DEF_NAME)
SIGNATURE_DICT = {"name": DEF_NAME, "type": "Nat -> Nat -> Nat", "imports": []}
PINNED_SIG = f"{TASK_SYMBOL} : Nat -> Nat -> Nat"
DEFINITION_SOURCE = "Nat.clog (b n : ℕ) : ℕ -- context only, never written to statements"
SYNTHETIC_MENTIONS = [MentionRecord(theorem_name="Nat.clog_pow", source_file="Data/Nat/Log.lean", statement_text="Nat.clog b (b ^ n) = n")]


# --- _feedback_text (pure) ---------------------------------------------------------------------


def _rotated(stage: str, detail: str) -> TaskResult:
    return TaskResult(
        definition_name="X", outcome="ROTATED", rotated_at_stage=stage,
        stage_records=[StageRecord(stage=stage, status="rotated", detail=detail)],
    )


def test_feedback_text_dossier_consistency_is_eligible():
    assert _feedback_text(_rotated("dossier_consistency", "DOSSIER_LEAKS_REAL_NAME: ...")) == "DOSSIER_LEAKS_REAL_NAME: ..."


def test_feedback_text_round_trip_compile_exhaustion_is_eligible():
    r = _rotated("round_trip_scoring", "exhausted 4 compile attempt(s): attempt 1: compile_error: ...")
    assert _feedback_text(r) == "exhausted 4 compile attempt(s): attempt 1: compile_error: ..."


def test_feedback_text_round_trip_fact_suite_failure_is_not_eligible():
    """Guardrail: never feed back fact-validation/fact-score information."""
    r = _rotated("round_trip_scoring", "compiled but failed the fact suite (no retry, per policy): failing decide facts: ['f1']")
    assert _feedback_text(r) is None


def test_feedback_text_mechanical_validation_is_not_eligible():
    assert _feedback_text(_rotated("mechanical_validation", "no facts survived mechanical validation")) is None


def test_feedback_text_shipped_result_is_not_eligible():
    shipped = TaskResult(definition_name="X", outcome="SHIPPED", rotated_at_stage=None, stage_records=[])
    assert _feedback_text(shipped) is None


# --- repair_one / run_cleanup (real REPL + stub Bedrock) ---------------------------------------


@pytest.fixture(scope="module")
def mathlib_env():
    server, import_result = get_warm_environment()
    assert import_result.status is CheckStatus.PASSED, import_result.detail
    yield server, import_result.env
    server.kill()


@pytest.fixture
def stub_server():
    server = None

    def _make(script):
        nonlocal server
        server = StubBedrockServer(script)
        return server

    yield _make
    if server is not None:
        server.stop()


def _config(server, env, tmp_path, bedrock_server) -> PipelineConfig:
    client = BedrockClient(endpoint_url=bedrock_server.url, log_path=tmp_path / "log.jsonl", sleep_fn=lambda s: None)

    def _resolve(name: str) -> DefinitionInput:
        return DefinitionInput(
            name=DEF_NAME, signature_dict=SIGNATURE_DICT, definition_source=DEFINITION_SOURCE,
            docstring="the ceiling logarithm", return_shape="value", mention_records=SYNTHETIC_MENTIONS,
        )

    return PipelineConfig(
        client=client, authoring_model_id="test-authoring-model", flagship_model_id="test-flagship-model",
        server=server, base_env=env, resolve_definition=_resolve,
        output_dir=tmp_path / "output", batch_review_dir=tmp_path / "review",
    )


def _dossier_json(leak: bool) -> str:
    body_ref = DEF_NAME if leak else TASK_SYMBOL  # leaks the real name in the fenced command
    dossier_md = (
        "# Object\nThe ceiling logarithm.\n\n"
        # 2026-07-31: the model no longer restates the pinned signature (contract §3.4(c)) --
        # `authoring.cleanup.repair_one` injects it mechanically, same as the normal pipeline.
        "# Signature\nThe first argument is the base; the second is the value.\n\n"
        f"# Conventions\nFor b<=1 or n<=1, {TASK_SYMBOL} b n = 0 (junk value convention).\n\n"
        f"# Worked examples\n- Claim: {TASK_SYMBOL} 2 37 = 6\n"
        "  ```lean\n"
        f"  example : {body_ref} 2 37 = 6 := by decide\n"
        "  ```\n\n"
        "# Boundaries\nAt b<=1 or n<=1, junk value 0.\n\n"
        "# Not to be confused with\nThe floor logarithm.\n"
    )
    return json.dumps({
        "dossier_md": dossier_md,
        "domain": {
            "constraint": "1 < b ∧ 1 < n", "variables": ["b", "n"],
            "conventions": [{"point": "b<=1 or n<=1", "statement": f"{TASK_SYMBOL} b n = 0 for b<=1 or n<=1", "note": "junk value convention"}],
        },
    })


LEAKED_DOSSIER_JSON = _dossier_json(leak=True)
CLEAN_DOSSIER_JSON = _dossier_json(leak=False)

CLASSIFICATION_JSON = json.dumps({
    "regimes": ["casework", "global"], "difficulty": 2, "rationale": "computable, boundary-rich",
    "expected_fact_mix": {"casework": 2, "membership": 0, "global": 1},
})
GOOD_FACTS_JSON = json.dumps([
    {"id": "f1", "type": "casework", "mechanism": "decide", "statement": f"example : {TASK_SYMBOL} 2 37 = 6 := by decide", "domain_inputs": {"b": ["2"], "n": ["37"]}},
    {"id": "g1", "type": "global", "mechanism": "proof", "statement": f"∀ b n : ℕ, (1 < b ∧ 1 < n) → {TASK_SYMBOL} b n ≥ 0", "anchors": ["Nat.clog_pow"], "self_restatement": True},
])
GOOD_ROUND_TRIP_BODY = "fun b n => if b ≤ 1 ∨ n ≤ 1 then 0 else Nat.log b (n - 1) + 1"


def _base_entry(rotation_reason: str) -> dict:
    return {
        "name": DEF_NAME, "batch": "b.txt", "rotation_stage": "dossier_consistency",
        "rotation_reason": rotation_reason, "category": AGENT_FIXABLE,
        "artifacts": {}, "repair_log": [], "status": STATUS_PENDING,
    }


def test_repair_one_succeeds_on_first_repair_attempt(mathlib_env, stub_server, tmp_path):
    server, env = mathlib_env
    bedrock_server = stub_server([
        ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
        ScriptedResponse(200, success_body(CLEAN_DOSSIER_JSON)),  # repair attempt 1: clean immediately
        ScriptedResponse(200, success_body(GOOD_FACTS_JSON)),
        ScriptedResponse(200, success_body(GOOD_ROUND_TRIP_BODY)),
    ])
    config = _config(server, env, tmp_path, bedrock_server)
    entry = _base_entry("DOSSIER_LEAKS_REAL_NAME: dossier contains the real Mathlib name 'Nat.clog'")

    result = repair_one(entry, config)

    assert result.status == STATUS_REPAIRED_AND_SHIPPED
    assert result.attempts_used == 1
    assert entry["status"] == STATUS_REPAIRED_AND_SHIPPED
    assert len(entry["repair_log"]) == 1
    assert entry["repair_log"][0]["check_result"] == "pass -- shipped"
    assert result.shipped_task_dir is not None
    validated = validate_task_dir(result.shipped_task_dir)
    assert validated.data["task_id"] == DEF_NAME


def test_repair_one_also_injects_the_signature_mechanically(mathlib_env, stub_server, tmp_path):
    """`authoring.cleanup.repair_one` is the SECOND caller of `inject_pinned_signature` (the
    other is `authoring.pipeline`'s normal dossier_attempt) -- confirms the repair loop's own
    revised dossier gets the same mechanical treatment, not just the first-attempt path."""
    from authoring.consistency import SIGNATURE_INJECTION_END, SIGNATURE_INJECTION_START
    from pathlib import Path

    server, env = mathlib_env
    bedrock_server = stub_server([
        ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
        ScriptedResponse(200, success_body(CLEAN_DOSSIER_JSON)),
        ScriptedResponse(200, success_body(GOOD_FACTS_JSON)),
        ScriptedResponse(200, success_body(GOOD_ROUND_TRIP_BODY)),
    ])
    config = _config(server, env, tmp_path, bedrock_server)
    entry = _base_entry("DOSSIER_LEAKS_REAL_NAME: dossier contains the real Mathlib name 'Nat.clog'")

    result = repair_one(entry, config)

    assert result.status == STATUS_REPAIRED_AND_SHIPPED
    dossier_text = (Path(result.shipped_task_dir) / "dossier.md").read_text(encoding="utf-8")
    expected_block = f"{SIGNATURE_INJECTION_START}\n{PINNED_SIG}\n{SIGNATURE_INJECTION_END}"
    assert expected_block in dossier_text


def test_repair_one_recovers_after_one_failed_attempt(mathlib_env, stub_server, tmp_path):
    server, env = mathlib_env
    bedrock_server = stub_server([
        ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
        ScriptedResponse(200, success_body(LEAKED_DOSSIER_JSON)),  # repair attempt 1: still leaks
        ScriptedResponse(200, success_body(CLEAN_DOSSIER_JSON)),   # repair attempt 2: clean
        ScriptedResponse(200, success_body(GOOD_FACTS_JSON)),
        ScriptedResponse(200, success_body(GOOD_ROUND_TRIP_BODY)),
    ])
    config = _config(server, env, tmp_path, bedrock_server)
    entry = _base_entry("DOSSIER_LEAKS_REAL_NAME: dossier contains the real Mathlib name 'Nat.clog'")

    result = repair_one(entry, config)

    assert result.status == STATUS_REPAIRED_AND_SHIPPED
    assert result.attempts_used == 2
    assert len(entry["repair_log"]) == 2
    assert entry["repair_log"][0]["check_result"] == "fail (dossier_consistency)"
    assert entry["repair_log"][1]["check_result"] == "pass -- shipped"


def test_repair_one_escalates_after_cap_exhausted(mathlib_env, stub_server, tmp_path):
    server, env = mathlib_env
    bedrock_server = stub_server(
        [ScriptedResponse(200, success_body(CLASSIFICATION_JSON))]
        + [ScriptedResponse(200, success_body(LEAKED_DOSSIER_JSON))] * 5  # never fixed, all 5 attempts leak
    )
    config = _config(server, env, tmp_path, bedrock_server)
    entry = _base_entry("DOSSIER_LEAKS_REAL_NAME: dossier contains the real Mathlib name 'Nat.clog'")

    result = repair_one(entry, config)

    assert result.status == STATUS_ESCALATE_TO_HUMAN
    assert result.attempts_used == 5
    assert entry["status"] == STATUS_ESCALATE_TO_HUMAN
    assert len(entry["repair_log"]) == 5
    assert all(e["check_result"] == "fail (dossier_consistency)" for e in entry["repair_log"])


def test_run_cleanup_only_attempts_agent_fixable_pending_entries(mathlib_env, stub_server, tmp_path):
    server, env = mathlib_env
    bedrock_server = stub_server([
        ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
        ScriptedResponse(200, success_body(CLEAN_DOSSIER_JSON)),
        ScriptedResponse(200, success_body(GOOD_FACTS_JSON)),
        ScriptedResponse(200, success_body(GOOD_ROUND_TRIP_BODY)),
    ])
    config = _config(server, env, tmp_path, bedrock_server)
    queue_path = tmp_path / "queue.json"

    from authoring.rotation_queue import save_queue
    save_queue([
        _base_entry("DOSSIER_LEAKS_REAL_NAME: ..."),  # the only eligible entry
        {**_base_entry("x"), "category": NOT_AGENT_FIXABLE},  # skipped: wrong category
        {**_base_entry("x"), "status": STATUS_REPAIRED_AND_SHIPPED},  # skipped: already done
    ], queue_path)

    run_result = run_cleanup(config, queue_path=queue_path, run_budget_usd=4.0)

    assert isinstance(run_result, CleanupRunResult)
    assert len(run_result.results) == 1  # only the one eligible entry attempted
    assert run_result.results[0].status == STATUS_REPAIRED_AND_SHIPPED
    assert run_result.stopped_reason is None


def test_run_cleanup_stops_at_budget_ceiling(tmp_path):
    """No REPL/Bedrock needed -- the budget check fires before the first name is even
    attempted, same "refuse before spending" shape as authoring.batch.run_batch."""
    from authoring.rotation_queue import save_queue

    def _unreachable_resolve(name):
        raise AssertionError("resolve_definition called -- budget ceiling must stop before this")

    config = PipelineConfig(
        client=None, authoring_model_id="m", flagship_model_id="m",
        server=None, base_env=0, resolve_definition=_unreachable_resolve,
    )
    queue_path = tmp_path / "queue.json"
    save_queue([_base_entry("x")], queue_path)

    run_result = run_cleanup(config, queue_path=queue_path, run_budget_usd=0.0)

    assert run_result.results == []
    assert run_result.stopped_reason is not None and "budget" in run_result.stopped_reason
