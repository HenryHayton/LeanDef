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
    validate_classification_against_shape,
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


# --- validate_classification_against_shape (2026-07-30) ----------------------------------
# Mechanization of contract §2's stated rule -- a Prop-valued definition must not receive
# 'casework'. `authoring/prompts/classification.txt` states the SAME rule in prose (its own
# "Rule:" line, checked in the drift-guard test below); this is the mechanical enforcement of
# it, checked against `return_shape` rather than left to the model's own inference.


def _classification(regimes: list[str]) -> Classification:
    return Classification(regimes=regimes, difficulty=2, rationale="x", expected_fact_mix={})


def test_validate_classification_against_shape_rejects_casework_on_prop():
    with pytest.raises(ParseError) as exc_info:
        validate_classification_against_shape(_classification(["casework"]), "prop")
    assert exc_info.value.reason_code == ReasonCode.MALFORMED_SCHEMA_SHAPE
    assert "casework" in exc_info.value.detail
    assert "prop" in exc_info.value.detail


def test_validate_classification_against_shape_allows_membership_and_global_on_prop():
    result = validate_classification_against_shape(_classification(["membership", "global"]), "prop")
    assert result.regimes == ["membership", "global"]


def test_validate_classification_against_shape_allows_casework_on_value():
    result = validate_classification_against_shape(_classification(["casework"]), "value")
    assert result.regimes == ["casework"]


def test_validate_classification_against_shape_allows_casework_on_bundled():
    """`bundled` (Equiv/Embedding/RingHom-shaped) is a separate return_shape from 'prop' --
    the rule is specifically about Prop-valued objects, not anything non-'value'."""
    result = validate_classification_against_shape(_classification(["casework"]), "bundled")
    assert result.regimes == ["casework"]


def test_classification_prompt_states_the_same_rule_the_parser_enforces():
    """Drift guard: if `authoring/prompts/classification.txt`'s own 'Rule:' line is edited to
    no longer state the Prop/casework rule (or the parser's enforcement above is removed),
    this test catches the divergence -- prompt and parser must not silently drift apart."""
    from authoring.prompt_loader import load_prompt_template

    template = load_prompt_template("classification")
    system, _ = template.render(
        pinned_signature="x", definition_source="y", docstring="z",
        mention_sidecar_excerpt="(none)", return_shape="prop",
    )
    assert "must not receive \"casework\"" in system
    assert "{return_shape}" not in system  # the placeholder actually got substituted
    assert "return shape is: prop" in system


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


def test_parse_facts_casework_wrong_mechanism_is_a_rejection():
    """(2026-07-28, second pass): a type<->mechanism mismatch on one fact must not discard
    the rest of an otherwise-good batch -- per-fact rejection, not a whole-call raise."""
    entry = {"id": "x", "type": "casework", "mechanism": "proof", "statement": "n = n"}
    facts, rejections = parse_facts(json.dumps([entry]))
    assert facts == []
    assert len(rejections) == 1
    assert rejections[0].reason_code == ReasonCode.MALFORMED_BAD_MECHANISM


def test_parse_facts_global_wrong_mechanism_is_a_rejection():
    entry = {"id": "x", "type": "global", "mechanism": "decide", "statement": "#eval 1"}
    facts, rejections = parse_facts(json.dumps([entry]))
    assert facts == []
    assert len(rejections) == 1
    assert rejections[0].reason_code == ReasonCode.MALFORMED_BAD_MECHANISM


def test_parse_facts_membership_missing_instance_is_a_rejection():
    """(2026-07-28, second pass): was a whole-call raise; now per-fact, same principle."""
    entry = {
        "id": "x", "type": "membership", "mechanism": "decide",
        "statement": "example : P := by decide", "polarity": "accept",
    }
    facts, rejections = parse_facts(json.dumps([entry]))
    assert facts == []
    assert len(rejections) == 1
    assert rejections[0].reason_code == ReasonCode.MALFORMED_MISSING_FIELD


def test_parse_facts_membership_reject_missing_violated_property_is_a_rejection():
    """(2026-07-28, second pass): was a whole-call raise; now per-fact, same principle."""
    entry = {
        "id": "x", "type": "membership", "mechanism": "decide",
        "statement": "example : P := by decide", "instance": "(0)", "polarity": "reject",
    }
    facts, rejections = parse_facts(json.dumps([entry]))
    assert facts == []
    assert len(rejections) == 1
    assert rejections[0].reason_code == ReasonCode.MALFORMED_MISSING_VIOLATED_PROPERTY


def test_parse_facts_membership_decide_on_undecidable_prop_is_a_rejection():
    entry = {
        "id": "x", "type": "membership", "mechanism": "decide",
        "statement": "example : P 0 := by decide", "instance": "P 0", "polarity": "accept",
    }
    facts, rejections = parse_facts(json.dumps([entry]), decidability="undecidable")
    assert facts == []
    assert len(rejections) == 1
    assert rejections[0].reason_code == ReasonCode.MALFORMED_DECIDE_ON_UNDECIDABLE_PROP


def test_parse_facts_membership_decide_on_indeterminate_prop_is_also_a_rejection():
    """`indeterminate` gates too -- a probe that couldn't determine decidability is not
    permission to guess it can."""
    entry = {
        "id": "x", "type": "membership", "mechanism": "decide",
        "statement": "example : P 0 := by decide", "instance": "P 0", "polarity": "accept",
    }
    facts, rejections = parse_facts(json.dumps([entry]), decidability="indeterminate")
    assert facts == []
    assert len(rejections) == 1
    assert rejections[0].reason_code == ReasonCode.MALFORMED_DECIDE_ON_UNDECIDABLE_PROP


def test_parse_facts_membership_decide_on_decidable_prop_parses_clean():
    entry = {
        "id": "x", "type": "membership", "mechanism": "decide",
        "statement": "example : P 0 := by decide", "instance": "P 0", "polarity": "accept",
    }
    facts, rejections = parse_facts(json.dumps([entry]), decidability="decidable")
    assert rejections == []
    assert len(facts) == 1


def test_parse_facts_membership_decide_when_decidability_not_supplied_parses_clean():
    """`decidability=None` (default) means no check -- backward compatible with every existing
    caller that has no such context (e.g. a value-typed task, where this never applies)."""
    entry = {
        "id": "x", "type": "membership", "mechanism": "decide",
        "statement": "example : P 0 := by decide", "instance": "P 0", "polarity": "accept",
    }
    facts, rejections = parse_facts(json.dumps([entry]))
    assert rejections == []
    assert len(facts) == 1


def test_parse_facts_membership_proof_mechanism_unaffected_by_decidability():
    """The gate is specifically about mechanism 'decide' -- a proof-mechanism membership fact
    on an undecidable Prop is exactly the intended path, never rejected by this check."""
    entry = {
        "id": "x", "type": "membership", "mechanism": "proof",
        "statement": "P 0", "instance": "P 0", "polarity": "accept",
    }
    facts, rejections = parse_facts(json.dumps([entry]), decidability="undecidable")
    assert rejections == []
    assert len(facts) == 1


def test_parse_facts_duplicate_ids_within_one_response_raises():
    entry1 = {"id": "dup", "type": "casework", "mechanism": "decide", "statement": "#eval 1", "domain_inputs": {"n": "1"}}
    entry2 = {"id": "dup", "type": "casework", "mechanism": "decide", "statement": "#eval 2", "domain_inputs": {"n": "2"}}
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


@pytest.mark.parametrize("real_name", ["Monotone", "DependsOn", "memPartition"])
def test_parse_facts_task_symbol_of_an_unnamespaced_name_is_not_a_raw_name_leak(real_name):
    """For an UNNAMESPACED real name the task symbol CONTAINS it (`VTask.Monotone` contains
    `Monotone`), so this plain-substring matcher flagged the very symbol every statement is
    required to use. Live regression (2026-07-31): 100% of proposed facts were rejected this way
    -- 12/12, 14/14 and 15/15 for these three names -- so `mechanical_validation` reported "no
    facts survived" when in truth none had been allowed through the parser at all."""
    entry = {
        "id": "clean", "type": "global", "mechanism": "proof",
        "statement": f"∀ f, VTask.{real_name} f → VTask.{real_name} f", "anchors": ["Nat.clog_pow"],
    }
    facts, rejections = parse_facts(
        json.dumps([entry]), task_symbol=f"VTask.{real_name}", forbidden_name=real_name
    )
    assert rejections == [], rejections
    assert len(facts) == 1


@pytest.mark.parametrize("real_name", ["Monotone", "DependsOn", "memPartition"])
def test_parse_facts_bare_unnamespaced_real_name_is_still_a_raw_name_leak(real_name):
    """The fix must not blind the check: a BARE occurrence still rejects."""
    entry = {
        "id": "leak", "type": "global", "mechanism": "proof",
        "statement": f"∀ f, {real_name} f → {real_name} f", "anchors": ["Nat.clog_pow"],
    }
    facts, rejections = parse_facts(
        json.dumps([entry]), task_symbol=f"VTask.{real_name}", forbidden_name=real_name
    )
    assert facts == []
    assert rejections[0].reason_code == ReasonCode.MALFORMED_RAW_NAME_IN_STATEMENT


def test_parse_facts_statement_mixing_task_symbol_and_bare_real_name_still_leaks():
    """Stripping the task symbol must not become a blanket exemption -- a statement that uses
    the symbol correctly AND also names the real declaration is still a leak."""
    entry = {
        "id": "mixed", "type": "global", "mechanism": "proof",
        "statement": "∀ f, VTask.Monotone f → Monotone f", "anchors": ["Nat.clog_pow"],
    }
    facts, rejections = parse_facts(
        json.dumps([entry]), task_symbol="VTask.Monotone", forbidden_name="Monotone"
    )
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


# --- Type-conditional required-field pre-checks (2026-07-28), mirroring ---------------------
# `harness.task_schema._validate_fact` exactly -- see that module's docstring in
# `authoring/pipeline.py`'s module docstring, decision 4, for why these exist: a real slice run
# shipped 15/15 casework facts with an empty `domain_inputs` all the way to `emit_task` before
# anything caught it.


def test_parse_facts_casework_missing_domain_inputs_is_a_rejection():
    entry = {"id": "cw1", "type": "casework", "mechanism": "decide", "statement": "example : VTask.clog 2 8 = 3 := by decide"}
    facts, rejections = parse_facts(json.dumps([entry]))
    assert facts == []
    assert len(rejections) == 1
    assert rejections[0].reason_code == ReasonCode.MALFORMED_MISSING_DOMAIN_INPUTS
    assert "cw1" in rejections[0].detail
    assert "domain_inputs" in rejections[0].detail


def test_parse_facts_casework_with_domain_inputs_parses_clean():
    entry = {
        "id": "cw1", "type": "casework", "mechanism": "decide",
        "statement": "example : VTask.clog 2 8 = 3 := by decide", "domain_inputs": {"b": "2", "n": "8"},
    }
    facts, rejections = parse_facts(json.dumps([entry]))
    assert rejections == []
    assert len(facts) == 1


def test_parse_facts_membership_missing_domain_inputs_is_a_rejection_when_domain_constrained():
    entry = {
        "id": "m1", "type": "membership", "mechanism": "decide",
        "statement": "example : Monotone (fun n : Fin 3 => n) := by decide",
        "instance": "(fun n : Fin 3 => n)", "polarity": "accept", "expected_type": "Fin 3 → Fin 3",
    }
    facts, rejections = parse_facts(json.dumps([entry]), domain_constraint="1 < b ∧ 1 < n")
    assert facts == []
    assert len(rejections) == 1
    assert rejections[0].reason_code == ReasonCode.MALFORMED_MISSING_DOMAIN_INPUTS
    assert "m1" in rejections[0].detail


def test_parse_facts_membership_missing_domain_inputs_ok_when_constraint_is_unrestricted():
    """The schema's own carve-out (harness.task_schema._validate_fact): domain_inputs is not
    required for membership when domain.constraint is the unrestricted 'True' sentinel."""
    entry = {
        "id": "m1", "type": "membership", "mechanism": "decide",
        "statement": "example : Monotone (fun n : Fin 3 => n) := by decide",
        "instance": "(fun n : Fin 3 => n)", "polarity": "accept", "expected_type": "Fin 3 → Fin 3",
    }
    facts, rejections = parse_facts(json.dumps([entry]), domain_constraint="True")
    assert rejections == []
    assert len(facts) == 1


def test_parse_facts_membership_missing_domain_inputs_ok_when_domain_constraint_not_supplied():
    """Backward compatible: a caller with no domain context yet (domain_constraint=None, the
    default) does not enforce this check at all."""
    entry = {
        "id": "m1", "type": "membership", "mechanism": "decide",
        "statement": "example : Monotone (fun n : Fin 3 => n) := by decide",
        "instance": "(fun n : Fin 3 => n)", "polarity": "accept", "expected_type": "Fin 3 → Fin 3",
    }
    facts, rejections = parse_facts(json.dumps([entry]))
    assert rejections == []
    assert len(facts) == 1


# --- domain_inputs: schema v1.1.3 list-valued canonicalization + safeguards (2026-07-30) -----


def test_parse_facts_domain_inputs_scalar_is_canonicalized_to_single_element_list():
    entry = {
        "id": "cw1", "type": "casework", "mechanism": "decide",
        "statement": "example : VTask.clog 2 8 = 3 := by decide", "domain_inputs": {"b": "2", "n": "8"},
    }
    facts, rejections = parse_facts(json.dumps([entry]))
    assert rejections == []
    assert facts[0].domain_inputs == {"b": ["2"], "n": ["8"]}


def test_parse_facts_domain_inputs_list_form_passes_through():
    entry = {
        "id": "m1", "type": "membership", "mechanism": "decide",
        "statement": "example : VTask.clog 2 8 ≤ VTask.clog 2 9 := by decide",
        "instance": "VTask.clog 2 8 ≤ VTask.clog 2 9", "polarity": "accept",
        "domain_inputs": {"b": ["2"], "n": ["8", "9"]},
    }
    facts, rejections = parse_facts(json.dumps([entry]))
    assert rejections == []
    assert facts[0].domain_inputs == {"b": ["2"], "n": ["8", "9"]}


def test_parse_facts_domain_inputs_empty_list_value_raises():
    entry = {"id": "cw1", "type": "casework", "mechanism": "decide", "statement": "#eval 1", "domain_inputs": {"n": []}}
    with pytest.raises(ParseError) as exc_info:
        parse_facts(json.dumps([entry]))
    assert exc_info.value.reason_code == ReasonCode.MALFORMED_SCHEMA_SHAPE


def test_parse_facts_domain_inputs_non_string_list_element_raises():
    entry = {"id": "cw1", "type": "casework", "mechanism": "decide", "statement": "#eval 1", "domain_inputs": {"n": [8]}}
    with pytest.raises(ParseError) as exc_info:
        parse_facts(json.dumps([entry]))
    assert exc_info.value.reason_code == ReasonCode.MALFORMED_SCHEMA_SHAPE


# Rule 5's parse-time mirror. Real trigger (2026-07-30, "Rule-5 Mirror" build session): the
# 41-name batch's Gate 1 re-run rotated at `emit_task` because a monotonicity-probing fact
# needed two values of `n` and the model invented keys `n1`/`n2` instead -- see
# docs/deferred.md's now-closed rule-5 entry and docs/design/task_schema_v1_1.md's v1.1.3
# changelog. `_REAL_2026_07_30_MONOTONICITY_FACT` reproduces that exact fact, verbatim.

_REAL_2026_07_30_MONOTONICITY_FACT_BAD = {
    "id": "clog_mem_monotone_accept", "type": "membership", "mechanism": "decide",
    "statement": "example : VTask.clog 2 8 ≤ VTask.clog 2 9 := by decide",
    "instance": "VTask.clog 2 8 ≤ VTask.clog 2 9", "polarity": "accept",
    "domain_inputs": {"b": "2", "n1": "8", "n2": "9"},
}


def test_parse_facts_domain_inputs_undeclared_key_is_a_rejection_reproducing_the_real_incident():
    facts, rejections = parse_facts(
        json.dumps([_REAL_2026_07_30_MONOTONICITY_FACT_BAD]), domain_variables=["b", "n"],
    )
    assert facts == []
    assert len(rejections) == 1
    assert rejections[0].reason_code == ReasonCode.MALFORMED_UNKNOWN_DOMAIN_VARIABLE
    assert "n1" in rejections[0].detail and "n2" in rejections[0].detail
    assert "['b', 'n']" in rejections[0].detail  # names the declared variables
    assert "list" in rejections[0].detail.lower()  # names the actual fix, not just the violation


def test_parse_facts_domain_inputs_correctly_reshaped_fact_parses_clean():
    """The same real fact, rewritten in the canonical list form the rejection feedback asks
    for -- proves the fix, not just the failure."""
    fixed = {
        **_REAL_2026_07_30_MONOTONICITY_FACT_BAD,
        "domain_inputs": {"b": ["2"], "n": ["8", "9"]},
    }
    facts, rejections = parse_facts(json.dumps([fixed]), domain_variables=["b", "n"])
    assert rejections == []
    assert len(facts) == 1
    assert facts[0].domain_inputs == {"b": ["2"], "n": ["8", "9"]}


def test_parse_facts_domain_inputs_undeclared_key_not_checked_when_domain_variables_not_supplied():
    """Backward compatible: domain_variables=None (the default) means no rule-5 check at all."""
    facts, rejections = parse_facts(json.dumps([_REAL_2026_07_30_MONOTONICITY_FACT_BAD]))
    assert rejections == []
    assert len(facts) == 1


def test_parse_facts_domain_inputs_cap_safeguard_rejects_more_than_three_values():
    entry = {
        "id": "m1", "type": "membership", "mechanism": "decide",
        "statement": "example : VTask.clog 2 1 ≤ VTask.clog 2 2 ∧ VTask.clog 2 2 ≤ VTask.clog 2 3 ∧ VTask.clog 2 3 ≤ VTask.clog 2 4 := by decide",
        "instance": "chain", "polarity": "accept",
        "domain_inputs": {"b": ["2"], "n": ["1", "2", "3", "4"]},
    }
    facts, rejections = parse_facts(json.dumps([entry]))
    assert facts == []
    assert len(rejections) == 1
    assert rejections[0].reason_code == ReasonCode.MALFORMED_TOO_MANY_DOMAIN_INPUT_VALUES


def test_parse_facts_domain_inputs_cap_safeguard_allows_exactly_three_values():
    entry = {
        "id": "m1", "type": "membership", "mechanism": "decide",
        "statement": "example : VTask.clog 2 1 ≤ VTask.clog 2 2 ∧ VTask.clog 2 2 ≤ VTask.clog 2 3 := by decide",
        "instance": "chain", "polarity": "accept",
        "domain_inputs": {"b": ["2"], "n": ["1", "2", "3"]},
    }
    facts, rejections = parse_facts(json.dumps([entry]))
    assert rejections == []
    assert len(facts) == 1


def test_parse_facts_domain_inputs_semantic_presence_safeguard_rejects_value_not_in_statement():
    entry = {
        "id": "cw1", "type": "casework", "mechanism": "decide",
        "statement": "example : VTask.clog 2 8 = 3 := by decide",
        "domain_inputs": {"b": ["2"], "n": ["8", "999"]},  # 999 never appears in the statement
    }
    facts, rejections = parse_facts(json.dumps([entry]))
    assert facts == []
    assert len(rejections) == 1
    assert rejections[0].reason_code == ReasonCode.MALFORMED_DOMAIN_INPUT_NOT_IN_STATEMENT
    assert "999" in rejections[0].detail


def test_parse_facts_domain_inputs_semantic_presence_safeguard_allows_values_present_in_statement():
    entry = {
        "id": "m1", "type": "membership", "mechanism": "decide",
        "statement": "example : VTask.clog 2 8 ≤ VTask.clog 2 9 := by decide",
        "instance": "VTask.clog 2 8 ≤ VTask.clog 2 9", "polarity": "accept",
        "domain_inputs": {"b": ["2"], "n": ["8", "9"]},
    }
    facts, rejections = parse_facts(json.dumps([entry]))
    assert rejections == []
    assert len(facts) == 1


def test_task_schema_doc_states_the_same_rule_5_the_parser_enforces():
    """Drift guard: if docs/design/task_schema_v1_1.md's v1.1.3 changelog entry is edited to no
    longer state the list-valued-domain_inputs / rule-5-mirror rule (or the parser enforcement
    above is removed), this test catches the divergence."""
    from harness.config import REPO_ROOT

    doc_text = (REPO_ROOT / "docs" / "design" / "task_schema_v1_1.md").read_text(encoding="utf-8")
    assert "v1.1.3" in doc_text
    assert "non-empty lists of strings" in doc_text or "non-empty list" in doc_text
    assert "Rule 5 closed" in doc_text
    assert "MAX_DOMAIN_INPUT_VALUES" in doc_text


def test_parse_facts_global_missing_anchors_is_a_rejection():
    entry = {"id": "g1", "type": "global", "mechanism": "proof", "statement": "∀ n : ℕ, VTask.clog 2 n ≥ 0"}
    facts, rejections = parse_facts(json.dumps([entry]))
    assert facts == []
    assert len(rejections) == 1
    assert rejections[0].reason_code == ReasonCode.MALFORMED_MISSING_ANCHORS
    assert "g1" in rejections[0].detail


def test_parse_facts_global_with_anchors_parses_clean():
    entry = {"id": "g1", "type": "global", "mechanism": "proof", "statement": "∀ n : ℕ, VTask.clog 2 n ≥ 0", "anchors": ["Nat.clog_pos"]}
    facts, rejections = parse_facts(json.dumps([entry]))
    assert rejections == []
    assert len(facts) == 1


def test_parse_facts_casework_with_anchors_is_a_rejection():
    entry = {
        "id": "cw1", "type": "casework", "mechanism": "decide",
        "statement": "example : VTask.clog 2 8 = 3 := by decide", "domain_inputs": {"b": "2", "n": "8"},
        "anchors": ["Nat.clog_pow"],
    }
    facts, rejections = parse_facts(json.dumps([entry]))
    assert facts == []
    assert len(rejections) == 1
    assert rejections[0].reason_code == ReasonCode.MALFORMED_ANCHORS_NOT_ALLOWED
    assert "cw1" in rejections[0].detail


def test_parse_facts_membership_with_anchors_is_a_rejection():
    entry = {
        "id": "m1", "type": "membership", "mechanism": "decide",
        "statement": "example : Monotone (fun n : Fin 3 => n) := by decide",
        "instance": "(fun n : Fin 3 => n)", "polarity": "accept", "expected_type": "Fin 3 → Fin 3",
        "anchors": ["Foo.bar"],
    }
    facts, rejections = parse_facts(json.dumps([entry]))
    assert facts == []
    assert rejections[0].reason_code == ReasonCode.MALFORMED_ANCHORS_NOT_ALLOWED


def test_parse_facts_regression_fifteen_casework_facts_all_missing_domain_inputs():
    """The exact shape of the real 2026-07-28 clog incident: 15 well-formed casework facts,
    statements all valid, domain_inputs entirely absent from every one. All 15 must come back
    as rejections (not silently accepted with an empty dict), none as parsed facts."""
    entries = [
        {"id": f"clog_casework_{i}", "type": "casework", "mechanism": "decide", "statement": f"example : VTask.clog 2 {i} = 0 := by decide"}
        for i in range(15)
    ]
    facts, rejections = parse_facts(json.dumps(entries))
    assert facts == []
    assert len(rejections) == 15
    assert {r.reason_code for r in rejections} == {ReasonCode.MALFORMED_MISSING_DOMAIN_INPUTS}
    assert {r.fragment["id"] for r in rejections} == {e["id"] for e in entries}


# --- Drift guard: everything parse_facts accepts must also pass harness.task_schema's ---------
# per-fact validation. If a future schema rule change adds a new type-conditional requirement
# without a matching mirror here, this test is the one that goes red.


def _minimal_fact_dict_for_schema(proposed, *, run_id: str = "drift-guard-run") -> dict:
    """Wrap an already-parse-clean `ProposedFact` in the extra fields `emit_task` always adds
    (validation_status/discharge/cached_script/axiom_closure/provenance) using the exact
    convention `authoring/pipeline.py` decision 1 documents (decide -> CERTIFIED, proof ->
    PROVISIONALLY_VALIDATED, discharge/cached_script/axiom_closure always null), then convert
    via `authoring.emit._fact_to_dict` -- the exact reverse of `harness.facts.Fact.from_dict`
    -- so this is the SAME shape a real shipped task.json fact would have."""
    from authoring.emit import _fact_to_dict
    from harness.facts import Fact, FactProvenance

    validation_status = "CERTIFIED" if proposed.mechanism == "decide" else "PROVISIONALLY_VALIDATED"
    fact = Fact(
        id=proposed.id, type=proposed.type, mechanism=proposed.mechanism, statement=proposed.statement,
        instance=proposed.instance, polarity=proposed.polarity, violated_property=proposed.violated_property,
        domain_inputs=proposed.domain_inputs, anchors=proposed.anchors,
        validation_status=validation_status, discharge=None, cached_script=None, axiom_closure=None,
        provenance=FactProvenance(validation_run_id=run_id, note="drift-guard test fact"),
    )
    return _fact_to_dict(fact)


@pytest.mark.parametrize(
    "entry",
    [
        {"id": "cw1", "type": "casework", "mechanism": "decide", "statement": "example : VTask.isSorted [] = true := by decide", "domain_inputs": {"l": "[]"}},
        {
            "id": "m1", "type": "membership", "mechanism": "decide",
            "statement": "example : VTask.isSorted [1] = true := by decide",
            "instance": "[1]", "polarity": "accept", "expected_type": "List Nat",
        },
        {"id": "g1", "type": "global", "mechanism": "proof", "statement": "∀ l, VTask.isSorted l = VTask.isSorted l", "anchors": ["List.Sorted.refl"]},
    ],
    ids=["casework", "membership", "global"],
)
def test_a_fact_that_parses_clean_also_passes_schema_per_fact_validation(entry):
    """For each fact type: build the minimal fact `parse_facts` accepts (with the fixture's own
    domain, constraint 'True'/variables ['l']), wrap it exactly as `emit_task` would, and assert
    `harness.task_schema._validate_fact` (the authoritative per-fact rule set this module's own
    checks are supposed to mirror) raises nothing for it."""
    from harness.task_schema import _validate_fact

    facts, rejections = parse_facts(json.dumps([entry]), domain_constraint="True")
    assert rejections == [], f"fact was unexpectedly rejected at parse time: {rejections}"
    assert len(facts) == 1

    fact_dict = _minimal_fact_dict_for_schema(facts[0])
    _validate_fact(fact_dict, index=0, domain_constraint="True", domain_variables=["l"])  # must not raise


# --- Regression: the real 2026-07-28 gate incident (Nat.clog, second batch-50 attempt) --------
#
# The exact 27-fact response a real Bedrock call produced for Nat.clog's fact-proposal stage --
# 12 casework, 7 membership (every one missing `expected_type`, which the parser at the time
# demanded via a whole-call raise), 8 global. This single response rotated the task at
# `fact_proposal` before Stage 2 of a planned 50-task batch could even start. Captured verbatim
# from `bedrock/output/call_log.jsonl` at the time of the incident.

_REAL_2026_07_28_GATE_RESPONSE = [
    {"id": "clog_casework_2_8", "type": "casework", "mechanism": "decide", "statement": "example : VTask.clog 2 8 = 3 := by decide", "domain_inputs": {"b": "2", "n": "8"}},
    {"id": "clog_casework_2_9", "type": "casework", "mechanism": "decide", "statement": "example : VTask.clog 2 9 = 4 := by decide", "domain_inputs": {"b": "2", "n": "9"}},
    {"id": "clog_casework_10_100", "type": "casework", "mechanism": "decide", "statement": "example : VTask.clog 10 100 = 2 := by decide", "domain_inputs": {"b": "10", "n": "100"}},
    {"id": "clog_casework_10_101", "type": "casework", "mechanism": "decide", "statement": "example : VTask.clog 10 101 = 3 := by decide", "domain_inputs": {"b": "10", "n": "101"}},
    {"id": "clog_casework_base1", "type": "casework", "mechanism": "decide", "statement": "example : VTask.clog 1 5 = 0 := by decide", "domain_inputs": {"b": "1", "n": "5"}},
    {"id": "clog_casework_n1", "type": "casework", "mechanism": "decide", "statement": "example : VTask.clog 2 1 = 0 := by decide", "domain_inputs": {"b": "2", "n": "1"}},
    {"id": "clog_casework_n0", "type": "casework", "mechanism": "decide", "statement": "example : VTask.clog 2 0 = 0 := by decide", "domain_inputs": {"b": "2", "n": "0"}},
    {"id": "clog_casework_base0", "type": "casework", "mechanism": "decide", "statement": "example : VTask.clog 0 7 = 0 := by decide", "domain_inputs": {"b": "0", "n": "7"}},
    {"id": "clog_casework_pow_3_3", "type": "casework", "mechanism": "decide", "statement": "example : VTask.clog 3 27 = 3 := by decide", "domain_inputs": {"b": "3", "n": "27"}},
    {"id": "clog_casework_2_16", "type": "casework", "mechanism": "decide", "statement": "example : VTask.clog 2 16 = 4 := by decide", "domain_inputs": {"b": "2", "n": "16"}},
    {"id": "clog_casework_2_17", "type": "casework", "mechanism": "decide", "statement": "example : VTask.clog 2 17 = 5 := by decide", "domain_inputs": {"b": "2", "n": "17"}},
    {"id": "clog_casework_antitone_ex", "type": "casework", "mechanism": "decide", "statement": "example : VTask.clog 4 16 ≤ VTask.clog 2 16 := by decide", "domain_inputs": {"b1": "4", "b2": "2", "n": "16"}},
    {"id": "clog_mem_nle_pow", "type": "membership", "mechanism": "decide", "statement": "example : VTask.clog 2 9 ∈ {k : ℕ | 9 ≤ 2 ^ k} := by decide", "instance": "VTask.clog 2 9", "polarity": "accept", "domain_inputs": {"b": "2", "n": "9"}},
    {"id": "clog_mem_pow_exact", "type": "membership", "mechanism": "decide", "statement": "example : VTask.clog 2 8 ∈ {k : ℕ | 2 ^ k = 8} := by decide", "instance": "VTask.clog 2 8", "polarity": "accept", "domain_inputs": {"b": "2", "n": "8"}},
    {"id": "clog_mem_nonzero_for_large_n", "type": "membership", "mechanism": "decide", "statement": "example : VTask.clog 2 9 ∈ {k : ℕ | 0 < k} := by decide", "instance": "VTask.clog 2 9", "polarity": "accept", "domain_inputs": {"b": "2", "n": "9"}},
    {"id": "clog_mem_zero_base1", "type": "membership", "mechanism": "decide", "statement": "example : VTask.clog 1 100 ∈ ({0} : Set ℕ) := by decide", "instance": "VTask.clog 1 100", "polarity": "accept", "domain_inputs": {"b": "1", "n": "100"}},
    {"id": "clog_mem_reject_wrong_value", "type": "membership", "mechanism": "decide", "statement": "example : VTask.clog 2 8 ∉ {k : ℕ | k = 4} := by decide", "instance": "VTask.clog 2 8", "polarity": "reject", "violated_property": "clog 2 8 equals 3, not 4", "domain_inputs": {"b": "2", "n": "8"}},
    {"id": "clog_mem_monotone_witness", "type": "membership", "mechanism": "decide", "statement": "example : VTask.clog 2 8 ∈ {k : ℕ | k ≤ VTask.clog 2 9} := by decide", "instance": "VTask.clog 2 8", "polarity": "accept", "domain_inputs": {"b": "2", "n1": "8", "n2": "9"}},
    {"id": "clog_mem_antitone_witness", "type": "membership", "mechanism": "decide", "statement": "example : VTask.clog 4 64 ∈ {k : ℕ | k ≤ VTask.clog 2 64} := by decide", "instance": "VTask.clog 4 64", "polarity": "accept", "domain_inputs": {"b1": "4", "b2": "2", "n": "64"}},
    {"id": "clog_one_left_global", "type": "global", "mechanism": "proof", "statement": "∀ n : ℕ, VTask.clog 1 n = 0", "anchors": ["Nat.clog_one_left"], "self_restatement": True},
    {"id": "clog_one_right_global", "type": "global", "mechanism": "proof", "statement": "∀ b : ℕ, VTask.clog b 1 = 0", "anchors": ["Nat.clog_one_right"], "self_restatement": True},
    {"id": "clog_monotone_global", "type": "global", "mechanism": "proof", "statement": "∀ b : ℕ, Monotone (VTask.clog b)", "anchors": ["Nat.clog_monotone"], "self_restatement": True},
    {"id": "clog_pow_global", "type": "global", "mechanism": "proof", "statement": "∀ (b x : ℕ), 1 < b → VTask.clog b (b ^ x) = x", "anchors": ["Nat.clog_pow"], "self_restatement": True},
    {"id": "clog_antitone_left_global", "type": "global", "mechanism": "proof", "statement": "∀ n : ℕ, AntitoneOn (fun b : ℕ => VTask.clog b n) (Set.Ioi 1)", "anchors": ["Nat.clog_antitone_left"], "self_restatement": True},
    {"id": "clog_ge_log_global", "type": "global", "mechanism": "proof", "statement": "∀ (b n : ℕ), Nat.log b n ≤ VTask.clog b n", "anchors": ["Nat.log_le_clog"], "self_restatement": True},
    {"id": "clog_zero_right_global", "type": "global", "mechanism": "proof", "statement": "∀ b : ℕ, VTask.clog b 0 = 0", "anchors": ["Nat.clog_one_right", "Nat.clog_monotone"]},
    {"id": "clog_le_pow_global", "type": "global", "mechanism": "proof", "statement": "∀ (b n : ℕ), 1 < b → n ≤ b ^ VTask.clog b n", "anchors": ["Nat.clog_pow", "Nat.clog_monotone"]},
]


def test_parse_facts_regression_real_2026_07_28_gate_incident_response_now_parses_clean():
    assert len(_REAL_2026_07_28_GATE_RESPONSE) == 27
    facts, rejections = parse_facts(json.dumps(_REAL_2026_07_28_GATE_RESPONSE))

    assert rejections == [], f"real incident response should now parse with zero rejections, got: {rejections}"
    assert len(facts) == 27

    membership_facts = [f for f in facts if f.type == "membership"]
    assert len(membership_facts) == 7
    for f in membership_facts:
        assert f.expected_type is None  # never supplied in the real response; now legitimately optional

    casework_facts = [f for f in facts if f.type == "casework"]
    assert len(casework_facts) == 12
    global_facts = [f for f in facts if f.type == "global"]
    assert len(global_facts) == 8
