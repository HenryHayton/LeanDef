"""Unit tests for `harness.facts.Fact`/`FactProvenance`, in particular `Fact.from_dict` against
a full schema v1.1 fact entry -- nothing previously exercised this reader at all (confirmed by
grep before this task), despite `harness.task_schema` having required every field it reads
since schema v1. Uses the `is_sorted_v1` fixture's real fact entries so this test tracks the
same shape the schema validator accepts, rather than an independently-invented one.
"""

import json
from pathlib import Path

from harness.facts import Fact, FactProvenance

FIXTURE_TASK = json.loads(
    (Path(__file__).resolve().parent / "fixtures" / "tasks" / "is_sorted_v1" / "task.json").read_text()
)


def _fact_dict(fact_id: str) -> dict:
    return next(f for f in FIXTURE_TASK["facts"] if f["id"] == fact_id)


def test_from_dict_reads_a_certified_casework_fact():
    f = Fact.from_dict(_fact_dict("casework_empty"))
    assert f.id == "casework_empty"
    assert f.type == "casework"
    assert f.mechanism == "decide"
    # Schema v1.1.3 canonical form: every `domain_inputs` value is a LIST of strings, never a
    # bare string (`harness.task_schema._validate_domain_inputs`). This assertion predated that
    # change and went stale -- the fixture and all 454 values in the real 41-task corpus are
    # lists. Normalizing a model's scalar output into a single-element list is
    # `authoring.parse`'s job, upstream of here, so nothing at this layer sees a scalar.
    assert f.domain_inputs == {"l": ["[]"]}
    assert f.anchors == []
    assert f.validation_status == "CERTIFIED"
    assert f.discharge is None
    assert f.cached_script is None
    assert f.axiom_closure is None
    assert f.provenance == FactProvenance(
        validation_run_id="fixture-v1.1",
        note="hand-authored for the schema validator fixture, not a real task",
    )


def test_from_dict_reads_a_provisionally_validated_global_fact_with_anchors():
    f = Fact.from_dict(_fact_dict("global_singleton_or_reverse"))
    assert f.type == "global"
    assert f.mechanism == "proof"
    assert f.validation_status == "PROVISIONALLY_VALIDATED"
    assert f.anchors == ["List.Sorted.reverse_of_length_le_one"]
    assert f.discharge is None
    assert f.cached_script is None
    assert f.axiom_closure is None


def test_from_dict_reads_a_certified_global_fact_with_full_discharge_evidence():
    f = Fact.from_dict(_fact_dict("global_certified_example"))
    assert f.validation_status == "CERTIFIED"
    assert f.discharge == {"tier": 2, "wall_clock_s": 0.42, "at": "authoring"}
    assert f.cached_script == "by intro l h1 h2; exact isSorted_reverse_iff.mp h2 h1"
    assert f.axiom_closure == ["propext", "Classical.choice", "Quot.sound"]


def test_from_dict_reads_membership_specific_fields():
    f = Fact.from_dict(_fact_dict("membership_reject_adjacent_swap"))
    assert f.instance == "[2, 1, 3]"
    assert f.polarity == "reject"
    assert f.violated_property == "ascending order violated between index 0 and 1"


def test_from_dict_defaults_when_optional_fields_absent():
    """A minimal dict missing every schema v1.1 addition still builds a Fact -- from_dict does
    not itself validate (that's harness.task_schema's job), it just reads what's there."""
    f = Fact.from_dict({"id": "x", "type": "casework", "mechanism": "decide", "statement": "s"})
    assert f.domain_inputs == {}
    assert f.anchors == []
    assert f.validation_status is None
    assert f.discharge is None
    assert f.cached_script is None
    assert f.axiom_closure is None
    assert f.provenance is None


def test_fact_provenance_from_dict():
    p = FactProvenance.from_dict({"validation_run_id": "run-7", "note": "n"})
    assert p == FactProvenance(validation_run_id="run-7", note="n")
