"""Tests for `authoring.consistency` -- contract §3.4's three sub-checks. Section-extraction,
convention-matching, and signature-substring are pure text (no REPL); worked-example execution
needs a real warm Mathlib environment, same pattern as `tests/test_authoring_validate.py`
(there's no ground truth to fake -- `Nat.clog` must be the real Mathlib declaration).
"""

import pytest

from authoring.consistency import (
    ELABORATED,
    EXECUTED,
    EXECUTION_FAILED,
    MALFORMED_NO_WORKED_EXAMPLES,
    UNCHECKED_PROSE_EXAMPLE,
    check_conventions_prose_match,
    check_dossier_consistency,
    check_signature_substring,
    check_worked_examples,
    extract_sections,
    parse_worked_examples,
)
from authoring.facts import ConventionPoint, DomainSpec
from harness.repl import get_warm_environment
from harness.results import CheckStatus


# --- extract_sections (pure) ----------------------------------------------------------------


def test_extract_sections_basic_headers():
    md = "# Object\nfoo bar\n\n# Signature\nbaz qux\n"
    sections = extract_sections(md)
    assert sections["object"] == "foo bar"
    assert sections["signature"] == "baz qux"


def test_extract_sections_tolerates_numbered_headers_and_header_levels():
    md = "## 1. Object\nA\n\n### 3. Conventions\nB\n\n#### Worked examples\nC\n"
    sections = extract_sections(md)
    assert sections["object"] == "A"
    assert sections["conventions"] == "B"
    assert sections["worked_examples"] == "C"


def test_extract_sections_ignores_unrecognized_headers():
    md = "# Random header\nignored\n\n# Boundaries\nreal content\n"
    sections = extract_sections(md)
    assert "random header" not in sections
    assert sections["boundaries"] == "real content"


def test_extract_sections_last_section_runs_to_end_of_document():
    md = "# Object\nA\n\n# Not to be confused with\nZ\n"
    sections = extract_sections(md)
    assert sections["not_to_be_confused_with"] == "Z"


# --- (a) conventions <-> prose matching (pure) -----------------------------------------------


def test_convention_match_via_statement_substring():
    domain = DomainSpec(
        constraint="n >= 1", variables=["n"],
        conventions=[ConventionPoint(point="0", statement="tau 0 = 0", note="empty divisor set")],
    )
    dossier = "# Conventions\nBy convention, tau 0 = 0 since 0 has no divisors.\n"
    results = check_conventions_prose_match(domain, dossier)
    assert results[0].matched
    assert results[0].matcher == "statement_substring"


def test_convention_match_via_note_keyword_when_statement_absent():
    domain = DomainSpec(
        constraint="n >= 1", variables=["n"],
        conventions=[ConventionPoint(point="0", statement=None, note="Mathlib convention: divisors empty")],
    )
    dossier = "# Conventions\nThe divisors set is empty at the boundary case.\n"
    results = check_conventions_prose_match(domain, dossier)
    assert results[0].matched
    assert results[0].matcher == "note_keyword"


def test_convention_no_match_flags_not_rejects():
    domain = DomainSpec(
        constraint="n >= 1", variables=["n"],
        conventions=[ConventionPoint(point="0", statement="tau 0 = 0", note="empty divisor set")],
    )
    dossier = "# Conventions\nNothing relevant here at all.\n"
    results = check_conventions_prose_match(domain, dossier)
    assert results[0].matched is False
    assert results[0].matcher == "no_match"


def test_sentinel_convention_always_matches():
    domain = DomainSpec(
        constraint="True", variables=[],
        conventions=[ConventionPoint(point=None, statement=None, note="NONE_DECLARED: none")],
    )
    dossier = "# Conventions\nanything\n"
    results = check_conventions_prose_match(domain, dossier)
    assert results[0].matched
    assert results[0].matcher == "sentinel_skip"


def test_convention_flags_never_appear_in_passed_computation_via_top_level_result():
    """(a) is documented as flag-only -- a ConsistencyCheckResult with an unmatched convention
    but otherwise-clean (b)/(c) must still report passed=True."""
    from authoring.consistency import ConsistencyCheckResult, ConventionMatchResult

    result = ConsistencyCheckResult(
        convention_matches=[ConventionMatchResult(point="0", matched=False, matcher="no_match")],
        worked_example_checks=[],
        signature_substring_ok=True,
    )
    assert result.passed is True
    assert len(result.flags) == 1


# --- (c) signature substring (pure) -----------------------------------------------------------


def test_signature_substring_present():
    dossier = "# Signature\nThe pinned signature is `Nat.clog : Nat -> Nat -> Nat`, meaning...\n"
    ok, detail = check_signature_substring("Nat.clog : Nat -> Nat -> Nat", dossier)
    assert ok
    assert detail == ""


def test_signature_substring_missing_fails_with_detail():
    dossier = "# Signature\nSomething else entirely.\n"
    ok, detail = check_signature_substring("Nat.clog : Nat -> Nat -> Nat", dossier)
    assert not ok
    assert "not found verbatim" in detail


# --- (b) worked-example parsing (pure) ---------------------------------------------------------


def test_parse_worked_examples_extracts_claim_and_fenced_command():
    dossier = (
        "# Worked examples\n"
        "- Claim: Nat.clog 2 37 = 6\n"
        "  ```lean\n"
        "  example : Nat.clog 2 37 = 6 := by decide\n"
        "  ```\n"
        "- Claim: Nat.clog 5 1 = 0 (junk value)\n"
        "  ```lean\n"
        "  example : Nat.clog 5 1 = 0 := by decide\n"
        "  ```\n"
    )
    items = parse_worked_examples(dossier)
    assert len(items) == 2
    assert items[0].claim == "Nat.clog 2 37 = 6"
    assert items[0].command == "example : Nat.clog 2 37 = 6 := by decide"
    assert items[1].command == "example : Nat.clog 5 1 = 0 := by decide"


def test_parse_worked_examples_bullet_without_fence_has_no_command():
    dossier = "# Worked examples\n- Claim: Monotone (fun n : Nat => n)\n"
    items = parse_worked_examples(dossier)
    assert items[0].command is None


def test_parse_worked_examples_empty_section_yields_no_items():
    dossier = "# Object\nsomething\n"
    assert parse_worked_examples(dossier) == []


# --- (b) worked-example execution (real Mathlib) ------------------------------------------------


@pytest.fixture(scope="module")
def mathlib_env():
    server, import_result = get_warm_environment()
    assert import_result.status is CheckStatus.PASSED, import_result.detail
    yield server, import_result.env
    server.kill()


def test_worked_example_true_command_is_executed(mathlib_env):
    server, env = mathlib_env
    dossier = "# Worked examples\n- Claim: Nat.clog 2 37 = 6\n  ```lean\n  example : Nat.clog 2 37 = 6 := by decide\n  ```\n"
    checks = check_worked_examples(server, env, dossier)
    assert len(checks) == 1
    assert checks[0].kind == EXECUTED


def test_worked_example_false_command_execution_failed(mathlib_env):
    server, env = mathlib_env
    dossier = "# Worked examples\n- Claim: Nat.clog 2 37 = 5\n  ```lean\n  example : Nat.clog 2 37 = 5 := by decide\n  ```\n"
    checks = check_worked_examples(server, env, dossier)
    assert checks[0].kind == EXECUTION_FAILED


def test_worked_example_no_command_but_elaborating_claim_is_elaborated(mathlib_env):
    server, env = mathlib_env
    dossier = "# Worked examples\n- Claim: Nat.clog 2 37 = 6\n"
    checks = check_worked_examples(server, env, dossier)
    assert checks[0].kind == ELABORATED


def test_worked_example_no_command_and_non_elaborating_claim_is_unchecked_prose(mathlib_env):
    server, env = mathlib_env
    dossier = "# Worked examples\n- Claim: this is just prose about the function, not Lean\n"
    checks = check_worked_examples(server, env, dossier)
    assert checks[0].kind == UNCHECKED_PROSE_EXAMPLE


def test_no_worked_examples_found_is_malformed(mathlib_env):
    server, env = mathlib_env
    dossier = "# Object\nnothing here\n"
    checks = check_worked_examples(server, env, dossier)
    assert checks[0].kind == MALFORMED_NO_WORKED_EXAMPLES


def test_check_dossier_consistency_end_to_end_passes_for_a_clean_dossier(mathlib_env):
    server, env = mathlib_env
    domain = DomainSpec(
        constraint="1 < b ∧ 1 < n", variables=["b", "n"],
        conventions=[ConventionPoint(point="b<=1", statement="Nat.clog b n = 0 for b <= 1", note="junk value below 2")],
    )
    dossier = (
        "# Object\nThe ceiling logarithm.\n\n"
        "# Signature\nThe pinned signature is `Nat.clog : Nat -> Nat -> Nat`.\n\n"
        "# Conventions\nFor b <= 1 the junk value 0 is returned.\n\n"
        "# Worked examples\n- Claim: Nat.clog 2 37 = 6\n  ```lean\n  example : Nat.clog 2 37 = 6 := by decide\n  ```\n\n"
        "# Boundaries\nAt b <= 1.\n\n"
        "# Not to be confused with\nNat.log.\n"
    )
    result = check_dossier_consistency(server, env, "Nat.clog : Nat -> Nat -> Nat", dossier, domain)
    assert result.passed
    assert result.flags == []


def test_check_dossier_consistency_end_to_end_fails_on_bad_signature_and_bad_example(mathlib_env):
    server, env = mathlib_env
    domain = DomainSpec(constraint="True", variables=[], conventions=[ConventionPoint(point=None, statement=None, note="NONE_DECLARED: x")])
    dossier = (
        "# Signature\nWrong signature entirely.\n\n"
        "# Worked examples\n- Claim: Nat.clog 2 37 = 5\n  ```lean\n  example : Nat.clog 2 37 = 5 := by decide\n  ```\n"
    )
    result = check_dossier_consistency(server, env, "Nat.clog : Nat -> Nat -> Nat", dossier, domain)
    assert not result.passed
