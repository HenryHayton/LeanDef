"""Tests for harness.task_schema against docs/design/task_schema_v1_1.md.

Uses a hand-authored fixture task (`tests/fixtures/tasks/is_sorted_v1/`) -- deliberately not
the archived τ probe, to keep schema testing independent of that one worked example. Each
violation test starts from a deep copy of the valid fixture's data and mutates exactly one
thing, so a failure pinpoints which rule broke.

The fixture itself covers all three fact types, including both a `PROVISIONALLY_VALIDATED`
and a `CERTIFIED` global fact with anchors -- the shape schema v1 could not express -- so
`test_valid_fixture_data_passes`/`test_valid_fixture_directory_passes` double as the
end-to-end "a full three-fact-type v1.1 task validates" test.
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


def test_old_v1_schema_version_now_fails(valid_data):
    """v1.1 is a breaking migration (schema doc Changelog): a v1 payload's version string is
    no longer accepted, not even as a fallback."""
    valid_data["schema_version"] = "1"
    with pytest.raises(TaskSchemaError, match="schema_version"):
        validate_task_data(valid_data)


# --- v1.1: statement format by mechanism -------------------------------------------------


def _fact(data: dict, fact_id: str) -> dict:
    return next(f for f in data["facts"] if f["id"] == fact_id)


def test_decide_statement_without_command_form_fails(valid_data):
    _fact(valid_data, "casework_empty")["statement"] = "isSorted [] = true"
    with pytest.raises(TaskSchemaError, match="full runnable command"):
        validate_task_data(valid_data)


def test_decide_statement_as_hash_command_passes(valid_data):
    _fact(valid_data, "casework_empty")["statement"] = "#eval decide (isSorted [] = true)"
    validate_task_data(valid_data)  # must not raise


def test_proof_statement_with_assignment_fails(valid_data):
    _fact(valid_data, "global_singleton_or_reverse")["statement"] = (
        "example : forall l : List Nat, isSorted l = true -> isSorted l.reverse = true := by sorry"
    )
    with pytest.raises(TaskSchemaError, match="bare Prop"):
        validate_task_data(valid_data)


# --- v1.1: domain.variables and per-fact domain_inputs ------------------------------------


def test_domain_missing_variables_fails(valid_data):
    del valid_data["domain"]["variables"]
    with pytest.raises(TaskSchemaError, match="variables"):
        validate_task_data(valid_data)


def test_domain_variables_duplicate_fails(valid_data):
    valid_data["domain"]["variables"] = ["l", "l"]
    with pytest.raises(TaskSchemaError, match="unique"):
        validate_task_data(valid_data)


def test_domain_variables_non_string_entry_fails(valid_data):
    valid_data["domain"]["variables"] = [1]
    with pytest.raises(TaskSchemaError, match="variables"):
        validate_task_data(valid_data)


def test_casework_missing_domain_inputs_fails(valid_data):
    _fact(valid_data, "casework_empty")["domain_inputs"] = {}
    with pytest.raises(TaskSchemaError, match="domain_inputs"):
        validate_task_data(valid_data)


def test_domain_inputs_key_not_in_domain_variables_fails(valid_data):
    _fact(valid_data, "casework_empty")["domain_inputs"] = {"not_a_declared_variable": "[]"}
    with pytest.raises(TaskSchemaError, match="domain.variables"):
        validate_task_data(valid_data)


def test_membership_domain_inputs_may_be_empty_when_domain_is_true_sentinel(valid_data):
    """is_sorted_v1's domain constraint is the 'True' sentinel, so membership facts are not
    required to bind domain_inputs (unlike casework, which always must)."""
    _fact(valid_data, "membership_accept_ascending")["domain_inputs"] = {}
    validate_task_data(valid_data)  # must not raise


def test_membership_missing_domain_inputs_fails_when_domain_non_trivial(valid_data):
    valid_data["domain"]["constraint"] = "l.length > 0"
    _fact(valid_data, "membership_accept_ascending")["domain_inputs"] = {}
    with pytest.raises(TaskSchemaError, match="domain_inputs"):
        validate_task_data(valid_data)


# --- v1.1: anchors ------------------------------------------------------------------------


def test_global_fact_missing_anchors_fails(valid_data):
    _fact(valid_data, "global_singleton_or_reverse")["anchors"] = []
    with pytest.raises(TaskSchemaError, match="anchor"):
        validate_task_data(valid_data)


def test_non_global_fact_with_anchors_fails(valid_data):
    _fact(valid_data, "casework_empty")["anchors"] = ["Nat.add_comm"]
    with pytest.raises(TaskSchemaError, match="anchors.*must be empty"):
        validate_task_data(valid_data)


def test_anchor_with_whitespace_fails(valid_data):
    _fact(valid_data, "global_singleton_or_reverse")["anchors"] = ["Nat add_comm"]
    with pytest.raises(TaskSchemaError, match="whitespace"):
        validate_task_data(valid_data)


# --- v1.1: validation_status ----------------------------------------------------------------


def test_decide_fact_provisional_status_fails(valid_data):
    _fact(valid_data, "casework_empty")["validation_status"] = "PROVISIONALLY_VALIDATED"
    with pytest.raises(TaskSchemaError, match="no provisional state"):
        validate_task_data(valid_data)


def test_bad_validation_status_value_fails(valid_data):
    _fact(valid_data, "casework_empty")["validation_status"] = "MAYBE"
    with pytest.raises(TaskSchemaError, match="validation_status"):
        validate_task_data(valid_data)


# --- v1.1: discharge / cached_script / axiom_closure coherence -----------------------------


def test_certified_proof_fact_without_discharge_fails(valid_data):
    _fact(valid_data, "global_certified_example")["discharge"] = None
    with pytest.raises(TaskSchemaError, match="discharge.*must be non-null"):
        validate_task_data(valid_data)


def test_provisional_proof_fact_with_nonnull_discharge_fails(valid_data):
    _fact(valid_data, "global_singleton_or_reverse")["discharge"] = {
        "tier": 2, "wall_clock_s": 1.0, "at": "authoring",
    }
    with pytest.raises(TaskSchemaError, match="discharge.*must be null"):
        validate_task_data(valid_data)


def test_discharge_bad_tier_fails(valid_data):
    _fact(valid_data, "global_certified_example")["discharge"]["tier"] = 6
    with pytest.raises(TaskSchemaError, match="tier"):
        validate_task_data(valid_data)


def test_discharge_bad_stage_fails(valid_data):
    _fact(valid_data, "global_certified_example")["discharge"]["at"] = "somewhere"
    with pytest.raises(TaskSchemaError, match="'at'"):
        validate_task_data(valid_data)


def test_discharge_negative_wall_clock_fails(valid_data):
    _fact(valid_data, "global_certified_example")["discharge"]["wall_clock_s"] = -1
    with pytest.raises(TaskSchemaError, match="wall_clock_s"):
        validate_task_data(valid_data)


def test_certified_proof_fact_without_cached_script_fails(valid_data):
    fact = _fact(valid_data, "global_certified_example")
    fact["cached_script"] = None
    fact["axiom_closure"] = None
    with pytest.raises(TaskSchemaError, match="cached_script.*must be non-null"):
        validate_task_data(valid_data)


def test_cached_script_without_axiom_closure_fails(valid_data):
    _fact(valid_data, "global_certified_example")["axiom_closure"] = None
    with pytest.raises(TaskSchemaError, match="axiom_closure.*must be non-null"):
        validate_task_data(valid_data)


def test_axiom_closure_without_cached_script_fails(valid_data):
    _fact(valid_data, "global_singleton_or_reverse")["axiom_closure"] = ["propext"]
    with pytest.raises(TaskSchemaError, match="axiom_closure.*must be null"):
        validate_task_data(valid_data)


# --- v1.1: ladder_budget_override (optional, task-level) ------------------------------------


def test_ladder_budget_override_must_be_object_when_present(valid_data):
    valid_data["ladder_budget_override"] = "not an object"
    with pytest.raises(TaskSchemaError, match="ladder_budget_override"):
        validate_task_data(valid_data)


def test_ladder_budget_override_may_be_a_populated_object(valid_data):
    valid_data["ladder_budget_override"] = {"tier_2_timeout_s": 5}
    validate_task_data(valid_data)  # must not raise


def test_ladder_budget_override_may_be_omitted_entirely(valid_data):
    del valid_data["ladder_budget_override"]
    validate_task_data(valid_data)  # must not raise
