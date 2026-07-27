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
