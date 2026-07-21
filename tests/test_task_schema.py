"""Tests for harness.task_schema against docs/design/task_schema_v1.md.

Uses a hand-authored fixture task (`tests/fixtures/tasks/is_sorted_v1/`) -- deliberately not
the archived τ probe, to keep schema testing independent of that one worked example. Each
violation test starts from a deep copy of the valid fixture's data and mutates exactly one
thing, so a failure pinpoints which rule broke.
"""

import json
from pathlib import Path

import pytest

from harness.task_schema import TaskSchemaError, validate_task_data, validate_task_dir

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "tasks" / "is_sorted_v1"


@pytest.fixture
def valid_data() -> dict:
    return json.loads((FIXTURE_DIR / "task.json").read_text())


def test_valid_fixture_directory_passes(valid_data):
    validated = validate_task_dir(FIXTURE_DIR)
    assert validated.data["task_id"] == "is_sorted_v1"


def test_valid_fixture_data_passes(valid_data):
    validate_task_data(valid_data)  # must not raise


def test_missing_dossier_md_fails(tmp_path, valid_data):
    task_dir = tmp_path / "no_dossier"
    task_dir.mkdir()
    (task_dir / "task.json").write_text(json.dumps(valid_data))
    with pytest.raises(TaskSchemaError, match="dossier.md"):
        validate_task_dir(task_dir)


def test_missing_task_json_fails(tmp_path):
    task_dir = tmp_path / "no_task_json"
    task_dir.mkdir()
    (task_dir / "dossier.md").write_text("# empty")
    with pytest.raises(TaskSchemaError, match="task.json"):
        validate_task_dir(task_dir)


def test_wrong_schema_version_fails(valid_data):
    valid_data["schema_version"] = "2"
    with pytest.raises(TaskSchemaError, match="schema_version"):
        validate_task_data(valid_data)


def test_missing_conventions_fails(valid_data):
    del valid_data["domain"]["conventions"]
    with pytest.raises(TaskSchemaError, match="conventions"):
        validate_task_data(valid_data)


def test_empty_conventions_array_without_sentinel_fails(valid_data):
    valid_data["domain"]["conventions"] = []
    with pytest.raises(TaskSchemaError, match="conventions"):
        validate_task_data(valid_data)


def test_conventions_sentinel_is_accepted(valid_data):
    valid_data["domain"]["conventions"] = [
        {"point": None, "statement": None, "note": "NONE_DECLARED: no meaningful edge cases"}
    ]
    validate_task_data(valid_data)  # must not raise


def test_conventions_sentinel_with_bad_note_fails(valid_data):
    valid_data["domain"]["conventions"] = [{"point": None, "statement": None, "note": "no conventions"}]
    with pytest.raises(TaskSchemaError, match="NONE_DECLARED"):
        validate_task_data(valid_data)


def test_conventions_sentinel_alongside_other_entries_fails(valid_data):
    valid_data["domain"]["conventions"].append(
        {"point": None, "statement": None, "note": "NONE_DECLARED: contradicts the entry above"}
    )
    with pytest.raises(TaskSchemaError, match="sentinel"):
        validate_task_data(valid_data)


def test_global_fact_with_mechanism_decide_fails(valid_data):
    for fact in valid_data["facts"]:
        if fact["type"] == "global":
            fact["mechanism"] = "decide"
    with pytest.raises(TaskSchemaError, match="global.*mechanism 'proof'"):
        validate_task_data(valid_data)


def test_casework_fact_with_mechanism_proof_fails(valid_data):
    for fact in valid_data["facts"]:
        if fact["type"] == "casework":
            fact["mechanism"] = "proof"
    with pytest.raises(TaskSchemaError, match="casework.*mechanism 'decide'"):
        validate_task_data(valid_data)


def test_membership_fact_missing_polarity_fails(valid_data):
    for fact in valid_data["facts"]:
        if fact["type"] == "membership":
            del fact["polarity"]
            break
    with pytest.raises(TaskSchemaError, match="polarity"):
        validate_task_data(valid_data)


def test_membership_fact_non_string_instance_fails(valid_data):
    for fact in valid_data["facts"]:
        if fact["type"] == "membership":
            fact["instance"] = ["1", "2", "3"]
            break
    with pytest.raises(TaskSchemaError, match="instance"):
        validate_task_data(valid_data)


def test_membership_reject_missing_violated_property_fails(valid_data):
    for fact in valid_data["facts"]:
        if fact["type"] == "membership" and fact["polarity"] == "reject":
            del fact["violated_property"]
    with pytest.raises(TaskSchemaError, match="violated_property"):
        validate_task_data(valid_data)


def test_duplicate_fact_ids_fail(valid_data):
    valid_data["facts"][1]["id"] = valid_data["facts"][0]["id"]
    with pytest.raises(TaskSchemaError, match="duplicate fact id"):
        validate_task_data(valid_data)


def test_populated_mutants_fails(valid_data):
    valid_data["mutants"] = [{"label": "off_by_one"}]
    with pytest.raises(TaskSchemaError, match="mutants"):
        validate_task_data(valid_data)


def test_non_null_prover_budget_fails(valid_data):
    valid_data["prover_budget"] = {"seconds": 60}
    with pytest.raises(TaskSchemaError, match="prover_budget"):
        validate_task_data(valid_data)


def test_missing_review_status_fails(valid_data):
    del valid_data["provenance"]["review_status"]
    with pytest.raises(TaskSchemaError, match="review_status"):
        validate_task_data(valid_data)


def test_bad_review_status_value_fails(valid_data):
    valid_data["provenance"]["review_status"] = "looks fine to me"
    with pytest.raises(TaskSchemaError, match="review_status"):
        validate_task_data(valid_data)


def test_bad_provenance_source_fails(valid_data):
    valid_data["provenance"]["source"] = "made_up"
    with pytest.raises(TaskSchemaError, match="source"):
        validate_task_data(valid_data)


def test_admissibility_contract_false_fails(valid_data):
    valid_data["admissibility_contract"]["single_declaration"] = False
    with pytest.raises(TaskSchemaError, match="single_declaration"):
        validate_task_data(valid_data)


def test_missing_axiom_baseline_fails(valid_data):
    del valid_data["axiom_baseline"]
    with pytest.raises(TaskSchemaError, match="axiom_baseline"):
        validate_task_data(valid_data)


def test_duplicated_axiom_baseline_validates_and_normalizes(tmp_path, valid_data):
    """Duplicates don't fail validation -- axiom_baseline is a set in spirit, and
    validate_task_dir normalizes (sorts, deduplicates) it rather than rejecting the source
    file for something that doesn't affect gate behaviour."""
    valid_data["axiom_baseline"] = ["Quot.sound", "propext", "propext", "Classical.choice"]
    task_dir = tmp_path / "dup_axioms"
    task_dir.mkdir()
    (task_dir / "task.json").write_text(json.dumps(valid_data))
    (task_dir / "dossier.md").write_text((FIXTURE_DIR / "dossier.md").read_text())

    validated = validate_task_dir(task_dir)
    assert validated.data["axiom_baseline"] == ["Classical.choice", "Quot.sound", "propext"]


def test_missing_signature_field_fails(valid_data):
    del valid_data["signature"]["type"]
    with pytest.raises(TaskSchemaError, match="type"):
        validate_task_data(valid_data)


def test_missing_heldout_fails(valid_data):
    del valid_data["heldout"]
    with pytest.raises(TaskSchemaError, match="heldout"):
        validate_task_data(valid_data)


def test_fact_missing_provenance_fails(valid_data):
    del valid_data["facts"][0]["provenance"]
    with pytest.raises(TaskSchemaError, match="provenance"):
        validate_task_data(valid_data)
