"""Tests for `authoring.emit` -- write task.json + dossier.md, then self-check via
`harness.task_schema.validate_task_dir`. No REPL/Bedrock involved: every `Fact` here is
hand-constructed, exactly like `tests/fixtures/tasks/is_sorted_v1/task.json` is hand-authored
for `tests/test_task_schema.py`.
"""

import json

import pytest

from authoring.emit import emit_task
from authoring.facts import ConventionPoint, DomainSpec
from harness.facts import Fact, FactProvenance
from harness.task_schema import TaskSchemaError


def _minimal_domain() -> DomainSpec:
    return DomainSpec(
        constraint="True",
        variables=["n"],
        conventions=[ConventionPoint(point=None, statement=None, note="NONE_DECLARED: no edge cases", predicate="ignored-should-be-dropped")],
    )


def _casework_fact(fact_id: str = "cw1") -> Fact:
    return Fact(
        id=fact_id,
        type="casework",
        mechanism="decide",
        statement="example : 1 + 1 = 2 := by decide",
        domain_inputs={"n": "1"},
        anchors=[],
        validation_status="CERTIFIED",
        discharge=None,
        cached_script=None,
        axiom_closure=None,
        provenance=FactProvenance(validation_run_id="run-1", note="emitted by test"),
    )


def _membership_reject_fact() -> Fact:
    return Fact(
        id="mem1",
        type="membership",
        mechanism="decide",
        statement="example : Nat.lt 2 1 = false := by decide",
        instance="(2 : Nat)",
        polarity="reject",
        violated_property="2 < 1 is false",
        domain_inputs={"n": "2"},
        anchors=[],
        validation_status="CERTIFIED",
        discharge=None,
        cached_script=None,
        axiom_closure=None,
        provenance=FactProvenance(validation_run_id="run-1", note="emitted by test"),
    )


def _global_provisional_fact() -> Fact:
    return Fact(
        id="g1",
        type="global",
        mechanism="proof",
        statement="∀ n : ℕ, n + 0 = n",
        domain_inputs={},
        anchors=["Nat.add_zero"],
        validation_status="PROVISIONALLY_VALIDATED",
        discharge=None,
        cached_script=None,
        axiom_closure=None,
        provenance=FactProvenance(validation_run_id="run-1", note="emitted by test"),
    )


def _base_kwargs(task_dir, facts):
    return dict(
        task_dir=task_dir,
        task_id="emit_test_task",
        signature={"name": "emitTestFn", "type": "Nat -> Nat", "imports": []},
        domain=_minimal_domain(),
        axiom_baseline=["propext"],
        facts=facts,
        dossier_md="# Object\n\nA test object.\n",
        heldout=False,
        provenance={
            "source": "fresh",
            "dossier_generator": "test-fixture",
            "validation_run_id": "run-1",
            "review_status": "human_reviewed",
        },
    )


def test_emit_writes_both_files(tmp_path):
    task_dir = tmp_path / "emit_test_task"
    emit_task(**_base_kwargs(task_dir, [_casework_fact()]))
    assert (task_dir / "task.json").is_file()
    assert (task_dir / "dossier.md").is_file()


def test_emit_round_trips_through_validate_task_dir(tmp_path):
    task_dir = tmp_path / "emit_test_task"
    result = emit_task(**_base_kwargs(task_dir, [_casework_fact(), _membership_reject_fact(), _global_provisional_fact()]))
    assert result.validated.data["task_id"] == "emit_test_task"
    assert len(result.validated.data["facts"]) == 3


def test_emit_drops_convention_predicate_authoring_only_field(tmp_path):
    """ConventionPoint.predicate is authoring-only; the schema's conventions entry shape is
    only {point, statement, note} -- writing it verbatim would itself fail validate_task_dir,
    which is exactly what this test guards against silently regressing."""
    task_dir = tmp_path / "emit_test_task"
    emit_task(**_base_kwargs(task_dir, [_casework_fact()]))
    written = json.loads((task_dir / "task.json").read_text())
    convention = written["domain"]["conventions"][0]
    assert set(convention.keys()) == {"point", "statement", "note"}
    assert "predicate" not in convention


def test_emit_membership_reject_carries_violated_property(tmp_path):
    task_dir = tmp_path / "emit_test_task"
    emit_task(**_base_kwargs(task_dir, [_membership_reject_fact()]))
    written = json.loads((task_dir / "task.json").read_text())
    fact = written["facts"][0]
    assert fact["polarity"] == "reject"
    assert fact["violated_property"] == "2 < 1 is false"


def test_emit_mutants_always_empty_list(tmp_path):
    task_dir = tmp_path / "emit_test_task"
    emit_task(**_base_kwargs(task_dir, [_casework_fact()]))
    written = json.loads((task_dir / "task.json").read_text())
    assert written["mutants"] == []


def test_emit_self_check_failure_propagates_and_leaves_files_on_disk(tmp_path):
    """A decide-mechanism fact whose validation_status is PROVISIONALLY_VALIDATED is invalid
    per schema (decide facts have no provisional state) -- an emitter bug or bad upstream data
    producing this must fail loudly at emit time, not ship silently, and the files must remain
    for post-mortem rather than being cleaned up."""
    bad_fact = Fact(
        id="bad1",
        type="casework",
        mechanism="decide",
        statement="example : 1 + 1 = 2 := by decide",
        domain_inputs={"n": "1"},
        anchors=[],
        validation_status="PROVISIONALLY_VALIDATED",
        discharge=None,
        cached_script=None,
        axiom_closure=None,
        provenance=FactProvenance(validation_run_id="run-1", note="deliberately invalid"),
    )
    task_dir = tmp_path / "emit_test_task"
    with pytest.raises(TaskSchemaError):
        emit_task(**_base_kwargs(task_dir, [bad_fact]))
    assert (task_dir / "task.json").is_file()  # left in place, not cleaned up
    assert (task_dir / "dossier.md").is_file()


def test_emit_ladder_budget_override_defaults_to_null(tmp_path):
    task_dir = tmp_path / "emit_test_task"
    emit_task(**_base_kwargs(task_dir, [_casework_fact()]))
    written = json.loads((task_dir / "task.json").read_text())
    assert written["ladder_budget_override"] is None
