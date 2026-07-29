"""Unit tests for bedrock.spend, using a small in-test fixture JSONL -- deliberately NOT the
real bedrock/output/call_log.jsonl (per this session's task instructions), so the tests stay
stable regardless of what the real log happens to contain on any given day."""

import json

from bedrock import spend
from bedrock.spend import SpendTotals, aggregate_spend, project_batch_cost


def _record(*, outcome: str, system: str = "", input_tokens=None, output_tokens=None) -> dict:
    response = None
    if outcome == "success":
        response = {"usage": {"input_tokens": input_tokens, "output_tokens": output_tokens}}
    return {
        "outcome": outcome,
        "request": {"system": system},
        "response": response,
    }


def _write_fixture_log(path, records: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")


def test_aggregate_spend_totals_and_dollars(tmp_path):
    log_path = tmp_path / "call_log.jsonl"
    _write_fixture_log(log_path, [
        _record(outcome="success", system="You are classifying a Mathlib definition's regime",
                input_tokens=1000, output_tokens=200),
        _record(outcome="success", system="You are writing the authoritative informal dossier",
                input_tokens=2000, output_tokens=500),
    ])

    report = aggregate_spend(log_path)

    assert report.total == SpendTotals(calls=2, input_tokens=3000, output_tokens=700)
    expected_dollars = (3000 / 1000) * 0.003 + (700 / 1000) * 0.015
    assert report.total.dollars == expected_dollars


def test_aggregate_spend_buckets_by_call_type(tmp_path):
    log_path = tmp_path / "call_log.jsonl"
    _write_fixture_log(log_path, [
        _record(outcome="success", system="You are classifying a Mathlib definition's regime",
                input_tokens=100, output_tokens=10),
        _record(outcome="success", system="You are classifying a Mathlib definition's regime",
                input_tokens=100, output_tokens=10),
        _record(outcome="success", system="You are proposing a fact suite for a Mathlib definition",
                input_tokens=300, output_tokens=30),
        _record(outcome="success", system="You are given only a pinned Lean 4 signature",
                input_tokens=400, output_tokens=40),
        _record(outcome="success", system="You are terse test assistant, matches no marker",
                input_tokens=5, output_tokens=1),
    ])

    report = aggregate_spend(log_path)

    assert report.by_call_type["classification"] == SpendTotals(calls=2, input_tokens=200, output_tokens=20)
    assert report.by_call_type["fact_proposal"] == SpendTotals(calls=1, input_tokens=300, output_tokens=30)
    assert report.by_call_type["round_trip"] == SpendTotals(calls=1, input_tokens=400, output_tokens=40)
    assert report.by_call_type["other"] == SpendTotals(calls=1, input_tokens=5, output_tokens=1)
    assert "dossier" not in report.by_call_type
    assert report.total.calls == 5


def test_aggregate_spend_skips_non_success_outcomes_but_counts_them(tmp_path):
    log_path = tmp_path / "call_log.jsonl"
    _write_fixture_log(log_path, [
        _record(outcome="throttled", system="You are classifying a Mathlib definition's regime"),
        _record(outcome="error", system="You are classifying a Mathlib definition's regime"),
        _record(outcome="success", system="You are classifying a Mathlib definition's regime",
                input_tokens=50, output_tokens=5),
    ])

    report = aggregate_spend(log_path)

    assert report.total == SpendTotals(calls=1, input_tokens=50, output_tokens=5)
    assert report.errored_calls == 2


def test_aggregate_spend_skips_malformed_lines_without_raising(tmp_path):
    log_path = tmp_path / "call_log.jsonl"
    log_path.write_text(
        "not json at all\n"
        + json.dumps(_record(outcome="success", system="classifying a Mathlib definition",
                              input_tokens=10, output_tokens=2))
        + "\n"
        + "\n"  # blank line
    )

    report = aggregate_spend(log_path)

    assert report.total == SpendTotals(calls=1, input_tokens=10, output_tokens=2)


def test_aggregate_spend_missing_file_returns_empty_report(tmp_path):
    report = aggregate_spend(tmp_path / "does_not_exist.jsonl")
    assert report.total == SpendTotals()
    assert report.by_call_type == {}
    assert report.errored_calls == 0


def test_classify_matches_all_four_contract_call_types():
    assert spend._classify("You are classifying a Mathlib definition's fact-suite regime") == "classification"
    assert spend._classify("You are writing the authoritative informal dossier for a Mathlib def") == "dossier"
    assert spend._classify("You are proposing a fact suite for a Mathlib definition") == "fact_proposal"
    assert spend._classify("You are given only a pinned Lean 4 signature and an informal dossier") == "round_trip"
    assert spend._classify("You are a terse test assistant.") == "other"


def test_project_batch_cost_scales_linearly_with_task_count():
    per_task = {
        "classification": (500, 100),
        "dossier": (2000, 800),
    }

    projected = project_batch_cost(per_task, n_tasks=10)

    assert projected.calls == 20
    assert projected.input_tokens == 25000
    assert projected.output_tokens == 9000
