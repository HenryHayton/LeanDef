"""Tests for `authoring.rotation_queue`: pure classification/extraction logic, plus
`append_rotation`'s file-writing behavior. No REPL/Bedrock needed -- everything here is either
pure text processing or file I/O against constructed fixtures."""

import json

from authoring.pipeline import StageRecord, TaskResult
from authoring.rotation_queue import (
    AGENT_FIXABLE,
    NOT_AGENT_FIXABLE,
    STATUS_PENDING,
    append_rotation,
    classify_rotation,
    find_rejected_dossier_md,
    load_queue,
    save_queue,
)


# --- classify_rotation (pure) ----------------------------------------------------------------


def test_classify_dossier_consistency_is_agent_fixable():
    assert classify_rotation("dossier_consistency", "DOSSIER_LEAKS_REAL_NAME: ...") == AGENT_FIXABLE


def test_classify_round_trip_compile_exhaustion_is_agent_fixable():
    assert classify_rotation("round_trip_scoring", "exhausted 4 compile attempt(s): attempt 1: ...") == AGENT_FIXABLE


def test_classify_round_trip_fact_suite_failure_is_not_agent_fixable():
    """The load-bearing distinction: a compile exhaustion is agent-fixable (the dossier may be
    unclear); a fact-suite failure is NOT (fixing it would mean showing the repair call
    fact-validation outcomes, which the guardrails forbid)."""
    assert classify_rotation("round_trip_scoring", "compiled but failed the fact suite (no retry, per policy): ...") == NOT_AGENT_FIXABLE


def test_classify_truth_splice_is_not_agent_fixable():
    assert classify_rotation("truth_splice", "LeanError: Unknown environment.") == NOT_AGENT_FIXABLE


def test_classify_unexpected_error_is_not_agent_fixable():
    assert classify_rotation("unexpected_error", "KeyError: 'x'") == NOT_AGENT_FIXABLE


def test_classify_mechanical_validation_is_not_agent_fixable():
    assert classify_rotation("mechanical_validation", "no facts survived mechanical validation") == NOT_AGENT_FIXABLE


# --- find_rejected_dossier_md (pure, fixture call log) ---------------------------------------


def _log_record(*, outcome: str, system: str = "", text: str = "") -> dict:
    response = {"content": [{"type": "text", "text": text}]} if outcome == "success" else None
    return {"outcome": outcome, "request": {"system": system}, "response": response}


def _write_log(path, records: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")


def test_find_rejected_dossier_md_extracts_from_range(tmp_path):
    log_path = tmp_path / "call_log.jsonl"
    dossier_text = json.dumps({"dossier_md": "# Object\nleaks Nat.clog", "domain": {"constraint": "True", "variables": [], "conventions": []}})
    _write_log(log_path, [
        _log_record(outcome="success", system="classifying a Mathlib definition", text="{}"),
        _log_record(outcome="success", system="You are writing the authoritative informal dossier", text=dossier_text),
    ])
    result = find_rejected_dossier_md(log_path, 0, 2)
    assert result == "# Object\nleaks Nat.clog"


def test_find_rejected_dossier_md_takes_the_last_one_in_range(tmp_path):
    """With the pipeline's own one-shot repair, the REJECTED dossier for a dossier_consistency
    rotation is the retried (second) attempt, not the first draft -- the last match wins."""
    log_path = tmp_path / "call_log.jsonl"
    first = json.dumps({"dossier_md": "draft one", "domain": {"constraint": "True", "variables": [], "conventions": []}})
    second = json.dumps({"dossier_md": "draft two (rejected)", "domain": {"constraint": "True", "variables": [], "conventions": []}})
    _write_log(log_path, [
        _log_record(outcome="success", system="You are writing the authoritative informal dossier", text=first),
        _log_record(outcome="success", system="You are writing the authoritative informal dossier", text=second),
    ])
    assert find_rejected_dossier_md(log_path, 0, 2) == "draft two (rejected)"


def test_find_rejected_dossier_md_strips_markdown_fence(tmp_path):
    log_path = tmp_path / "call_log.jsonl"
    payload = json.dumps({"dossier_md": "# Object\nfenced", "domain": {"constraint": "True", "variables": [], "conventions": []}})
    fenced = f"```json\n{payload}\n```"
    _write_log(log_path, [_log_record(outcome="success", system="You are writing the authoritative informal dossier", text=fenced)])
    assert find_rejected_dossier_md(log_path, 0, 1) == "# Object\nfenced"


def test_find_rejected_dossier_md_none_when_only_non_dossier_calls_in_range(tmp_path):
    """A truth_splice rotation never reaches the dossier call at all -- confirms the function
    returns None rather than mis-picking a classification/fact-proposal response."""
    log_path = tmp_path / "call_log.jsonl"
    _write_log(log_path, [_log_record(outcome="success", system="classifying a Mathlib definition", text="{}")])
    assert find_rejected_dossier_md(log_path, 0, 1) is None


def test_find_rejected_dossier_md_none_when_no_calls_in_range(tmp_path):
    log_path = tmp_path / "call_log.jsonl"
    _write_log(log_path, [])
    assert find_rejected_dossier_md(log_path, 0, 0) is None


def test_find_rejected_dossier_md_ignores_calls_outside_the_range(tmp_path):
    log_path = tmp_path / "call_log.jsonl"
    inside = json.dumps({"dossier_md": "inside range", "domain": {"constraint": "True", "variables": [], "conventions": []}})
    outside = json.dumps({"dossier_md": "OUTSIDE range -- must not be picked up", "domain": {"constraint": "True", "variables": [], "conventions": []}})
    _write_log(log_path, [
        _log_record(outcome="success", system="You are writing the authoritative informal dossier", text=outside),
        _log_record(outcome="success", system="You are writing the authoritative informal dossier", text=inside),
        _log_record(outcome="success", system="You are writing the authoritative informal dossier", text=outside),
    ])
    assert find_rejected_dossier_md(log_path, 1, 2) == "inside range"


# --- append_rotation / load_queue / save_queue (file I/O, no REPL) ---------------------------


def _rotated_result(name: str, stage: str, detail: str) -> TaskResult:
    return TaskResult(
        definition_name=name, outcome="ROTATED", rotated_at_stage=stage,
        stage_records=[StageRecord(stage="lookup", status="ok"), StageRecord(stage=stage, status="rotated", detail=detail)],
    )


def test_append_rotation_writes_a_new_entry_with_correct_category(tmp_path):
    queue_path = tmp_path / "pending_safety_updates.json"
    log_path = tmp_path / "call_log.jsonl"
    dossier_payload = json.dumps({"dossier_md": "# Object\nleaks Nat.foo", "domain": {"constraint": "True", "variables": [], "conventions": []}})
    _write_log(log_path, [_log_record(outcome="success", system="You are writing the authoritative informal dossier", text=dossier_payload)])

    result = _rotated_result("Nat.foo", "dossier_consistency", "DOSSIER_LEAKS_REAL_NAME: dossier contains 'Nat.foo'")
    entry = append_rotation(
        result, "authoring/batches/batch_x.txt", call_log_path=log_path,
        log_line_start=0, log_line_end=1, queue_path=queue_path,
    )

    assert entry.name == "Nat.foo"
    assert entry.category == AGENT_FIXABLE
    assert entry.status == STATUS_PENDING
    assert entry.artifacts["rejected_dossier_md"] == "# Object\nleaks Nat.foo"
    assert entry.artifacts["call_log_lines"] == [0, 1]
    assert entry.repair_log == []

    on_disk = load_queue(queue_path)
    assert len(on_disk) == 1
    assert on_disk[0]["name"] == "Nat.foo"


def test_append_rotation_appends_not_overwrites(tmp_path):
    queue_path = tmp_path / "pending_safety_updates.json"
    log_path = tmp_path / "call_log.jsonl"
    _write_log(log_path, [])

    append_rotation(
        _rotated_result("First.name", "truth_splice", "LeanError: Unknown environment."),
        "b.txt", call_log_path=log_path, log_line_start=0, log_line_end=0, queue_path=queue_path,
    )
    append_rotation(
        _rotated_result("Second.name", "truth_splice", "LeanError: Unknown environment."),
        "b.txt", call_log_path=log_path, log_line_start=0, log_line_end=0, queue_path=queue_path,
    )
    entries = load_queue(queue_path)
    assert [e["name"] for e in entries] == ["First.name", "Second.name"]
    assert entries[0]["category"] == NOT_AGENT_FIXABLE


def test_load_queue_missing_file_returns_empty_list(tmp_path):
    assert load_queue(tmp_path / "does_not_exist.json") == []


def test_save_and_load_queue_round_trips(tmp_path):
    path = tmp_path / "q.json"
    save_queue([{"name": "X", "status": "pending"}], path)
    assert load_queue(path) == [{"name": "X", "status": "pending"}]
