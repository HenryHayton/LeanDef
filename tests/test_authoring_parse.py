"""Tests for `authoring.parse` -- pure JSON-in, typed-object-out, no REPL/Bedrock involved.
Covers the two distinct failure shapes the module docstring names: whole-call `ParseError`
(malformed JSON, schema-shape violations) vs. per-fact `FactParseRejection` (statement-format
pre-check, contract §4.1/§6 row 3)."""

import json

import pytest

from authoring.parse import (
    Classification,
    DossierPayload,
    FactParseRejection,
    ParseError,
    parse_classification,
    parse_dossier,
    parse_facts,
)
from authoring.validate import ReasonCode


# --- parse_classification -----------------------------------------------------------------


def test_parse_classification_valid():
    text = json.dumps(
        {
            "regimes": ["casework", "membership"],
            "difficulty": 3,
            "rationale": "computable, boundary-rich",
            "expected_fact_mix": {"casework": 5, "membership": 3, "global": 0},
        }
    )
    result = parse_classification(text)
    assert result == Classification(
        regimes=["casework", "membership"],
        difficulty=3,
        rationale="computable, boundary-rich",
        expected_fact_mix={"casework": 5, "membership": 3, "global": 0},
    )


def test_parse_classification_rejects_decidable_vocabulary():
    """Contract §2's own vocabulary note: 'casework', not 'decidable' -- an unknown regime
    string must not silently pass through."""
    text = json.dumps(
        {"regimes": ["decidable"], "difficulty": 2, "rationale": "x", "expected_fact_mix": {}}
    )
    with pytest.raises(ParseError) as exc_info:
        parse_classification(text)
    assert exc_info.value.reason_code == ReasonCode.MALFORMED_SCHEMA_SHAPE


def test_parse_classification_rejects_out_of_range_difficulty():
    text = json.dumps(
        {"regimes": ["casework"], "difficulty": 9, "rationale": "x", "expected_fact_mix": {}}
    )
    with pytest.raises(ParseError):
        parse_classification(text)


def test_parse_classification_malformed_json_raises_parse_error_with_no_reason_code():
    with pytest.raises(ParseError) as exc_info:
        parse_classification("{not json")
    assert exc_info.value.reason_code is None
    assert "not valid JSON" in exc_info.value.detail


def test_parse_classification_top_level_must_be_object():
    with pytest.raises(ParseError) as exc_info:
        parse_classification(json.dumps(["not", "an", "object"]))
    assert exc_info.value.reason_code == ReasonCode.MALFORMED_SCHEMA_SHAPE


def test_parse_classification_missing_field_reports_missing_field_code():
    text = json.dumps({"regimes": ["casework"], "difficulty": 1, "rationale": "x"})
    with pytest.raises(ParseError) as exc_info:
        parse_classification(text)
    assert exc_info.value.reason_code == ReasonCode.MALFORMED_MISSING_FIELD


# --- parse_dossier -----------------------------------------------------------------------


def _valid_dossier_json(**overrides) -> str:
    payload = {
        "dossier_md": "# Object\n...",
        "domain": {
            "constraint": "True",
            "variables": [],
            "conventions": [{"point": None, "statement": None, "note": "NONE_DECLARED: no edge cases"}],
        },
    }
    payload.update(overrides)
    return json.dumps(payload)


def test_parse_dossier_valid_with_sentinel_convention():
    result = parse_dossier(_valid_dossier_json())
    assert isinstance(result, DossierPayload)
    assert result.dossier_md == "# Object\n..."
    assert result.domain.constraint == "True"
    assert len(result.domain.conventions) == 1
    assert result.domain.conventions[0].predicate is None  # never invented by the parser


def test_parse_dossier_valid_with_real_convention_point():
    text = _valid_dossier_json(
        domain={
            "constraint": "n >= 1",
            "variables": ["n"],
            "conventions": [{"point": "0", "statement": "f 0 = 0", "note": "junk value"}],
        }
    )
    result = parse_dossier(text)
    cp = result.domain.conventions[0]
    assert cp.point == "0"
    assert cp.statement == "f 0 = 0"
    assert cp.predicate is None


def test_parse_dossier_empty_conventions_array_rejected():
    text = _valid_dossier_json(domain={"constraint": "True", "variables": [], "conventions": []})
    with pytest.raises(ParseError):
        parse_dossier(text)


def test_parse_dossier_sentinel_with_bad_note_rejected():
    text = _valid_dossier_json(
        domain={
            "constraint": "True",
            "variables": [],
            "conventions": [{"point": None, "statement": None, "note": "no conventions here"}],
        }
    )
    with pytest.raises(ParseError):
        parse_dossier(text)


def test_parse_dossier_missing_dossier_md_raises():
    text = json.dumps({"domain": {"constraint": "True", "variables": [], "conventions": [{"point": None, "statement": None, "note": "NONE_DECLARED: x"}]}})
    with pytest.raises(ParseError) as exc_info:
        parse_dossier(text)
    assert exc_info.value.reason_code == ReasonCode.MALFORMED_MISSING_FIELD


# --- parse_facts: whole-call ParseError paths --------------------------------------------


def test_parse_facts_malformed_json_raises():
    with pytest.raises(ParseError):
        parse_facts("[not json")


def test_parse_facts_top_level_must_be_array():
    with pytest.raises(ParseError) as exc_info:
        parse_facts(json.dumps({"facts": []}))
    assert exc_info.value.reason_code == ReasonCode.MALFORMED_SCHEMA_SHAPE


def test_parse_facts_unknown_type_raises():
    entry = {"id": "x", "type": "bogus", "mechanism": "decide", "statement": "#eval 1"}
    with pytest.raises(ParseError) as exc_info:
        parse_facts(json.dumps([entry]))
    assert exc_info.value.reason_code == ReasonCode.MALFORMED_UNKNOWN_TYPE


def test_parse_facts_casework_wrong_mechanism_raises():
    entry = {"id": "x", "type": "casework", "mechanism": "proof", "statement": "n = n"}
    with pytest.raises(ParseError) as exc_info:
        parse_facts(json.dumps([entry]))
    assert exc_info.value.reason_code == ReasonCode.MALFORMED_BAD_MECHANISM


def test_parse_facts_global_wrong_mechanism_raises():
    entry = {"id": "x", "type": "global", "mechanism": "decide", "statement": "#eval 1"}
    with pytest.raises(ParseError) as exc_info:
        parse_facts(json.dumps([entry]))
    assert exc_info.value.reason_code == ReasonCode.MALFORMED_BAD_MECHANISM


def test_parse_facts_membership_missing_instance_raises():
    entry = {
        "id": "x", "type": "membership", "mechanism": "decide",
        "statement": "example : P := by decide", "polarity": "accept", "expected_type": "Nat",
    }
    with pytest.raises(ParseError) as exc_info:
        parse_facts(json.dumps([entry]))
    assert exc_info.value.reason_code == ReasonCode.MALFORMED_MISSING_FIELD


def test_parse_facts_membership_reject_missing_violated_property_raises():
    entry = {
        "id": "x", "type": "membership", "mechanism": "decide",
        "statement": "example : P := by decide", "instance": "(0)", "polarity": "reject",
        "expected_type": "Nat",
    }
    with pytest.raises(ParseError) as exc_info:
        parse_facts(json.dumps([entry]))
    assert exc_info.value.reason_code == ReasonCode.MALFORMED_MISSING_VIOLATED_PROPERTY


def test_parse_facts_duplicate_ids_within_one_response_raises():
    entry1 = {"id": "dup", "type": "casework", "mechanism": "decide", "statement": "#eval 1"}
    entry2 = {"id": "dup", "type": "casework", "mechanism": "decide", "statement": "#eval 2"}
    with pytest.raises(ParseError):
        parse_facts(json.dumps([entry1, entry2]))


# --- parse_facts: per-fact FactParseRejection paths (does NOT raise) ----------------------


def test_parse_facts_decide_bad_statement_shape_is_a_rejection_not_a_raise():
    good = {"id": "good", "type": "casework", "mechanism": "decide", "statement": "example : Nat.clog 2 37 = 6 := by decide", "domain_inputs": {"b": "2", "n": "37"}}
    bad = {"id": "bad", "type": "casework", "mechanism": "decide", "statement": "Nat.clog 2 37 = 6", "domain_inputs": {"b": "2", "n": "37"}}
    facts, rejections = parse_facts(json.dumps([good, bad]))
    assert [f.id for f in facts] == ["good"]
    assert len(rejections) == 1
    r = rejections[0]
    assert isinstance(r, FactParseRejection)
    assert r.index == 1
    assert r.reason_code == ReasonCode.MALFORMED_STATEMENT_FORMAT
    assert r.fragment["id"] == "bad"


def test_parse_facts_proof_statement_with_assignment_is_a_rejection():
    bad = {"id": "bad", "type": "global", "mechanism": "proof", "statement": "example : Nat.clog 2 37 = 6 := by decide", "anchors": ["Nat.clog_pow"]}
    facts, rejections = parse_facts(json.dumps([bad]))
    assert facts == []
    assert len(rejections) == 1
    assert rejections[0].reason_code == ReasonCode.MALFORMED_STATEMENT_FORMAT


def test_parse_facts_proof_statement_with_standalone_by_is_a_rejection():
    bad = {"id": "bad", "type": "global", "mechanism": "proof", "statement": "∀ n, P n by trivial", "anchors": ["Foo.bar"]}
    facts, rejections = parse_facts(json.dumps([bad]))
    assert facts == []
    assert rejections[0].reason_code == ReasonCode.MALFORMED_STATEMENT_FORMAT


def test_parse_facts_proof_statement_with_by_embedded_in_identifier_is_not_flagged():
    """Word-boundary check: an identifier that happens to contain 'by' as a substring (e.g. a
    hypothetical 'dividedByZero') must not trip the tactic-shape heuristic."""
    ok = {
        "id": "ok", "type": "global", "mechanism": "proof",
        "statement": "∀ n, dividedByZero n = 0", "anchors": ["Foo.bar"],
    }
    facts, rejections = parse_facts(json.dumps([ok]))
    assert rejections == []
    assert len(facts) == 1


def test_parse_facts_valid_global_fact_parses_clean():
    entry = {
        "id": "g1", "type": "global", "mechanism": "proof",
        "statement": "∀ n : ℕ, Nat.clog 2 n ≥ 0", "anchors": ["Nat.clog_pos"],
    }
    facts, rejections = parse_facts(json.dumps([entry]))
    assert rejections == []
    assert len(facts) == 1
    assert facts[0].anchors == ["Nat.clog_pos"]


def test_parse_facts_valid_membership_fact_parses_clean():
    entry = {
        "id": "m1", "type": "membership", "mechanism": "decide",
        "statement": "example : Monotone (fun n : Fin 3 => n) := by decide",
        "instance": "(fun n : Fin 3 => n)", "polarity": "accept", "expected_type": "Fin 3 → Fin 3",
    }
    facts, rejections = parse_facts(json.dumps([entry]))
    assert rejections == []
    assert facts[0].expected_type == "Fin 3 → Fin 3"


# --- task-symbol convention (contract §4.4): raw-name-leak rejection ----------------------


def test_parse_facts_raw_name_in_statement_is_a_rejection_when_forbidden_name_given():
    entry = {
        "id": "leak", "type": "casework", "mechanism": "decide",
        "statement": "example : Nat.clog 2 37 = 6 := by decide", "domain_inputs": {"b": "2", "n": "37"},
    }
    facts, rejections = parse_facts(json.dumps([entry]), task_symbol="VTask.clog", forbidden_name="Nat.clog")
    assert facts == []
    assert len(rejections) == 1
    assert rejections[0].reason_code == ReasonCode.MALFORMED_RAW_NAME_IN_STATEMENT
    assert "VTask.clog" in rejections[0].detail


def test_parse_facts_task_symbol_statement_is_clean_when_forbidden_name_given():
    entry = {
        "id": "clean", "type": "casework", "mechanism": "decide",
        "statement": "example : VTask.clog 2 37 = 6 := by decide", "domain_inputs": {"b": "2", "n": "37"},
    }
    facts, rejections = parse_facts(json.dumps([entry]), task_symbol="VTask.clog", forbidden_name="Nat.clog")
    assert rejections == []
    assert len(facts) == 1


def test_parse_facts_no_forbidden_name_check_when_not_supplied():
    """Backward compatible: omitting task_symbol/forbidden_name (both default None) disables
    the check entirely -- unaffected callers (or fresh, non-mined tasks) see no behavior change."""
    entry = {
        "id": "x", "type": "casework", "mechanism": "decide",
        "statement": "example : Nat.clog 2 37 = 6 := by decide", "domain_inputs": {"b": "2", "n": "37"},
    }
    facts, rejections = parse_facts(json.dumps([entry]))
    assert rejections == []
    assert len(facts) == 1


def test_parse_facts_raw_name_leak_in_instance_field_is_also_rejected():
    entry = {
        "id": "leak2", "type": "membership", "mechanism": "decide",
        "statement": "example : Monotone (Nat.clog 2) := by decide",
        "instance": "(Nat.clog 2)", "polarity": "accept", "expected_type": "Nat -> Nat",
    }
    facts, rejections = parse_facts(json.dumps([entry]), task_symbol="VTask.clog", forbidden_name="Nat.clog")
    assert facts == []
    assert rejections[0].reason_code == ReasonCode.MALFORMED_RAW_NAME_IN_STATEMENT


def test_parse_facts_anchors_are_exempt_from_the_raw_name_check():
    """Anchors legitimately (and routinely) contain the forbidden name as a substring of a
    real Mathlib theorem's own qualified name -- 'Nat.clog_pow' contains 'Nat.clog'."""
    entry = {
        "id": "g1", "type": "global", "mechanism": "proof",
        "statement": "∀ b n : ℕ, (1 < b ∧ 1 < n) → VTask.clog b n ≥ 0", "anchors": ["Nat.clog_pow"],
    }
    facts, rejections = parse_facts(json.dumps([entry]), task_symbol="VTask.clog", forbidden_name="Nat.clog")
    assert rejections == []
    assert facts[0].anchors == ["Nat.clog_pow"]


# --- self_restatement (contract §4.2) -------------------------------------------------------


def test_parse_facts_self_restatement_true_is_parsed():
    entry = {
        "id": "g1", "type": "global", "mechanism": "proof",
        "statement": "∀ b n : ℕ, VTask.clog b n ≥ 0", "anchors": ["Nat.clog_pow"], "self_restatement": True,
    }
    facts, rejections = parse_facts(json.dumps([entry]))
    assert rejections == []
    assert facts[0].self_restatement is True


def test_parse_facts_self_restatement_defaults_to_false_when_absent():
    entry = {"id": "g1", "type": "global", "mechanism": "proof", "statement": "∀ b n : ℕ, VTask.clog b n ≥ 0", "anchors": ["Nat.clog_pow"]}
    facts, _ = parse_facts(json.dumps([entry]))
    assert facts[0].self_restatement is False


def test_parse_facts_self_restatement_non_bool_raises():
    entry = {
        "id": "g1", "type": "global", "mechanism": "proof",
        "statement": "∀ b n : ℕ, VTask.clog b n ≥ 0", "anchors": ["Nat.clog_pow"], "self_restatement": "yes",
    }
    with pytest.raises(ParseError) as exc_info:
        parse_facts(json.dumps([entry]))


# --- hardening: malformed input of any shape must raise ParseError, never a raw exception -----
#
# The real bug (2026-07-28): a genuine Bedrock response sent `regimes` as a list of
# `{type, description, estimated_count}` objects instead of flat strings, and
# `parse_classification` crashed with `TypeError: unhashable type: 'dict'` -- `r in REGIMES`
# where `REGIMES` is a frozenset and `r` is a dict. `authoring.orchestrate._call_llm_json`'s
# retry wrapper only catches `ParseError`, so this escaped past the designed retry (contract §6
# rows 1-2) and took the whole task down. Every case below asserts `ParseError` specifically
# (not just "raises something") -- a bare `pytest.raises(Exception)` would have passed even
# before the fix, since `TypeError` is an `Exception` too.


def test_parse_classification_regimes_as_real_logged_response_shape():
    """The EXACT shape of the real 2026-07-28 Bedrock response that crashed this function."""
    text = json.dumps({
        "regimes": [
            {"type": "casework", "description": "Concrete numeric evaluations.", "estimated_count": 10},
            {"type": "membership", "description": "Boundary and structural facts.", "estimated_count": 15},
            {"type": "global", "description": "Higher-level properties.", "estimated_count": 8},
        ]
    })
    with pytest.raises(ParseError) as exc_info:
        parse_classification(text)
    assert exc_info.value.reason_code == ReasonCode.MALFORMED_SCHEMA_SHAPE
    assert "flat array of strings" in exc_info.value.detail


@pytest.mark.parametrize(
    "bad_classification",
    [
        {"regimes": {"casework": True}, "difficulty": 2, "rationale": "x", "expected_fact_mix": {}},
        {"regimes": [1, 2, 3], "difficulty": 2, "rationale": "x", "expected_fact_mix": {}},
        {"regimes": [["casework"]], "difficulty": 2, "rationale": "x", "expected_fact_mix": {}},
        {"regimes": ["casework"], "difficulty": 2, "rationale": "x", "expected_fact_mix": ["casework", "membership"]},
        {"regimes": ["casework"], "difficulty": "high", "rationale": "x", "expected_fact_mix": {}},
        {"regimes": ["casework"], "difficulty": 2, "rationale": {"nested": "object"}, "expected_fact_mix": {}},
        "just a bare string, not even an object",
        ["a", "bare", "array"],
        42,
        None,
    ],
)
def test_parse_classification_malformed_shape_battery_never_raises_raw_exception(bad_classification):
    text = json.dumps(bad_classification)
    with pytest.raises(ParseError):
        parse_classification(text)


@pytest.mark.parametrize(
    "bad_dossier",
    [
        {"dossier_md": "# Object", "domain": ["not", "an", "object"]},
        {"dossier_md": "# Object", "domain": {"constraint": "True", "variables": "not-a-list", "conventions": []}},
        {"dossier_md": "# Object", "domain": {"constraint": "True", "variables": [], "conventions": ["not-an-object"]}},
        {"dossier_md": "# Object", "domain": {"constraint": {"nested": True}, "variables": [], "conventions": [{"note": "x"}]}},
        {"dossier_md": 12345, "domain": {}},
        "a bare string",
        [],
    ],
)
def test_parse_dossier_malformed_shape_battery_never_raises_raw_exception(bad_dossier):
    text = json.dumps(bad_dossier)
    with pytest.raises(ParseError):
        parse_dossier(text)


@pytest.mark.parametrize(
    "bad_entry",
    [
        "a bare string, not an object",
        42,
        ["nested", "array"],
        {"id": "f1", "type": "global", "mechanism": "proof", "statement": "P", "anchors": ["A"], "instance": {"nested": "dict"}},
        {"id": "f1", "type": "global", "mechanism": "proof", "statement": "P", "anchors": ["A"], "expected_type": ["a", "list"]},
        {"id": "f1", "type": "casework", "mechanism": "decide", "statement": "#eval 1", "domain_inputs": ["not", "a", "dict"]},
        {"id": "f1", "type": "casework", "mechanism": "decide", "statement": "#eval 1", "domain_inputs": {"n": 5}},
        {"id": "f1", "type": "global", "mechanism": "proof", "statement": "P", "anchors": [{"nested": "dict"}]},
        {"id": {"nested": "dict"}, "type": "casework", "mechanism": "decide", "statement": "#eval 1"},
    ],
)
def test_parse_facts_malformed_entry_battery_never_raises_raw_exception(bad_entry):
    text = json.dumps([bad_entry])
    with pytest.raises(ParseError):
        parse_facts(text)


def test_parse_facts_top_level_not_a_list_of_any_kind():
    with pytest.raises(ParseError):
        parse_facts(json.dumps({"not": "a list"}))


def test_parse_facts_instance_as_dict_is_a_structured_error_not_a_typeerror_from_name_leak_check():
    """The specific gap this session's hardening closes: `instance`/`expected_type` weren't
    type-checked before being fed to the raw-name-leak substring check, so a non-membership
    fact with a dict `instance` could reach `forbidden_name in instance` -- a `TypeError` for
    any non-string, non-container `part`, and a silently-wrong check for a dict/list one."""
    entry = {
        "id": "f1", "type": "global", "mechanism": "proof", "statement": "∀ n, P n",
        "anchors": ["Real.Anchor"], "instance": {"weird": "shape"},
    }
    with pytest.raises(ParseError) as exc_info:
        parse_facts(json.dumps([entry]), task_symbol="VTask.clog", forbidden_name="Nat.clog")
    assert exc_info.value.reason_code == ReasonCode.MALFORMED_SCHEMA_SHAPE
    assert exc_info.value.reason_code == ReasonCode.MALFORMED_SCHEMA_SHAPE
