"""Tests for `authoring.consistency` -- contract §3.4's three sub-checks. Section-extraction,
convention-matching, and signature-substring are pure text (no REPL); worked-example execution
needs a real warm Mathlib environment, same pattern as `tests/test_authoring_validate.py`
(there's no ground truth to fake -- `Nat.clog` must be the real Mathlib declaration).
"""

import pytest
from lean_interact import Command

from authoring.consistency import (
    ELABORATED,
    EXECUTED,
    EXECUTION_FAILED,
    MALFORMED_NO_WORKED_EXAMPLES,
    SIGNATURE_INJECTION_END,
    SIGNATURE_INJECTION_START,
    UNCHECKED_PROSE_EXAMPLE,
    check_conventions_prose_match,
    check_dossier_consistency,
    check_no_real_name_leak,
    check_round_trip_recalls_target,
    check_signature_injection,
    check_worked_examples,
    extract_sections,
    inject_pinned_signature,
    parse_worked_examples,
)
from authoring.facts import ConventionPoint, DomainSpec
from authoring.validate import ReasonCode
from harness.repl import run_checked
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
        signature_injection_ok=True,
    )
    assert result.passed is True
    assert len(result.flags) == 1


# --- (c) signature injection (pure, 2026-07-31 -- retires the old substring check) -------------


def test_inject_pinned_signature_inserts_marker_block_right_after_the_header():
    dossier = "# Signature\nThe first argument is the base.\n\n# Boundaries\nnone\n"
    injected = inject_pinned_signature(dossier, "Nat.clog : Nat -> Nat -> Nat")
    expected_block = f"{SIGNATURE_INJECTION_START}\nNat.clog : Nat -> Nat -> Nat\n{SIGNATURE_INJECTION_END}"
    assert expected_block in injected
    # inserted BEFORE the model's own prose, not appended after it
    assert injected.index(SIGNATURE_INJECTION_START) < injected.index("The first argument")


def test_inject_pinned_signature_tolerates_numbered_and_leveled_headers():
    dossier = "## 2. Signature\nprose\n"
    injected = inject_pinned_signature(dossier, "X : Nat")
    assert f"{SIGNATURE_INJECTION_START}\nX : Nat\n{SIGNATURE_INJECTION_END}" in injected


def test_inject_pinned_signature_raises_without_a_signature_header():
    with pytest.raises(ValueError, match="no 'Signature' section header"):
        inject_pinned_signature("# Object\nno signature section at all\n", "X : Nat")


def test_inject_pinned_signature_raises_if_already_injected():
    dossier = "# Signature\nprose\n"
    once = inject_pinned_signature(dossier, "X : Nat")
    with pytest.raises(ValueError, match="already contains an injected signature block"):
        inject_pinned_signature(once, "X : Nat")


def test_check_signature_injection_present_after_injection():
    dossier = "# Signature\nThe first argument is the base.\n"
    injected = inject_pinned_signature(dossier, "Nat.clog : Nat -> Nat -> Nat")
    ok, detail = check_signature_injection("Nat.clog : Nat -> Nat -> Nat", injected)
    assert ok
    assert detail == ""


def test_check_signature_injection_missing_fails_with_detail():
    dossier = "# Signature\nSomething else entirely, never injected.\n"
    ok, detail = check_signature_injection("Nat.clog : Nat -> Nat -> Nat", dossier)
    assert not ok
    assert "missing or modified" in detail


def test_check_signature_injection_not_confused_by_a_wrong_signature_string_in_model_prose():
    """A model that (against its own instructions) writes a WRONG signature-shaped string into
    the Signature section must not accidentally satisfy the integrity check -- it looks for the
    exact marker-delimited block `inject_pinned_signature` writes, not a bare substring search
    that a coincidental (and wrong) signature-looking string could satisfy on its own."""
    dossier_with_wrong_string = "# Signature\nThe pinned signature is `Nat.wrong : Bool -> Bool`.\n"
    ok, _ = check_signature_injection("VTask.clog : Nat -> Nat -> Nat", dossier_with_wrong_string)
    assert not ok  # the wrong string alone never satisfies the check

    injected = inject_pinned_signature(dossier_with_wrong_string, "VTask.clog : Nat -> Nat -> Nat")
    ok2, detail2 = check_signature_injection("VTask.clog : Nat -> Nat -> Nat", injected)
    assert ok2  # the correct injected block passes, even alongside the leftover wrong string
    assert detail2 == ""


# --- (d) real-name leak, the round-trip information barrier (pure) -----------------------------


def test_real_name_leak_detected_as_a_standalone_word():
    dossier = "# Object\nThis computes the same thing as Nat.clog in Mathlib.\n"
    ok, detail = check_no_real_name_leak(dossier, "Nat.clog")
    assert not ok
    assert ReasonCode.DOSSIER_LEAKS_REAL_NAME in detail
    assert "Nat.clog" in detail


def test_real_name_leak_absent_when_only_task_symbol_used():
    dossier = "# Object\nVTask.clog computes the ceiling logarithm.\n"
    ok, detail = check_no_real_name_leak(dossier, "Nat.clog")
    assert ok
    assert detail == ""


def test_real_name_leak_check_is_word_boundary_not_bare_substring():
    """`Nat.clog` must not false-positive merely because it's a substring of a longer,
    unrelated-enough identifier -- word-boundary matched, per instruction, not a bare `in`
    check (which is what `authoring.parse`'s fact-level leak check uses; this one is
    deliberately stricter)."""
    dossier = "# Object\nSee SomeOtherOuterNat.clogVariant for a related idea.\n"
    ok, _ = check_no_real_name_leak(dossier, "Nat.clog")
    assert ok  # no word boundary before "Nat" (preceded by "Outer", a word character)


# --- round-trip recalled-target detection (2026-07-29, pure) -----------------------------------


def test_round_trip_recalls_target_detected_on_qualified_name():
    body = "fun b n => Nat.clog b n"
    assert check_round_trip_recalls_target(body, "Nat.clog") is True


def test_round_trip_recalls_target_absent_when_only_task_symbol_used():
    body = "fun b n => if b ≤ 1 ∨ n ≤ 1 then 0 else Nat.log b (n - 1) + 1"
    assert check_round_trip_recalls_target(body, "Nat.clog") is False


def test_round_trip_recalls_target_is_word_boundary_not_bare_substring():
    """`Nat.clog2` must NOT fire -- word-boundary matched, same semantics as (d)'s dossier
    check (both now share `authoring.consistency._contains_real_name`)."""
    body = "fun b n => Nat.clog2 b n"
    assert check_round_trip_recalls_target(body, "Nat.clog") is False


# --- Task-symbol exclusion in the shared matcher (2026-07-31 fix) -------------------------------
#
# For an UNNAMESPACED real name, the task symbol is that name plus a prefix (`Monotone` ->
# `VTask.Monotone`), so the old `\b`-based matcher fired on the very symbol the model is
# required to use -- making those dossiers unshippable regardless of quality. Confirmed live on
# three names (Monotone 9/9, DependsOn 14/14, memPartition 12/12 occurrences were all correct
# `VTask.`-prefixed usage, zero genuine leaks). Both callers of the shared matcher are covered
# below, since unnamespaced names are exactly where the two checks could interfere.


@pytest.mark.parametrize("real_name", ["Monotone", "DependsOn", "memPartition"])
def test_dossier_using_only_the_task_symbol_of_an_unnamespaced_name_is_not_a_leak(real_name):
    dossier = (
        f"# Object\n`VTask.{real_name} f` is the proposition that ...\n\n"
        f"# Conventions\n`VTask.{real_name}` holds vacuously in that case.\n"
    )
    ok, detail = check_no_real_name_leak(dossier, real_name)
    assert ok, detail


@pytest.mark.parametrize("real_name", ["Monotone", "DependsOn", "memPartition"])
def test_bare_unnamespaced_real_name_is_still_a_leak(real_name):
    """The fix must not blind the check: a BARE occurrence (no `VTask.` prefix) still fails."""
    dossier = f"# Object\nThis is the same thing Mathlib calls {real_name}.\n"
    ok, detail = check_no_real_name_leak(dossier, real_name)
    assert not ok
    assert real_name in detail


def test_primed_variant_is_a_different_declaration_and_not_a_leak():
    """`Equiv.ofLeftInverse'` is a real declaration DISTINCT from `Equiv.ofLeftInverse`. Python's
    `\\b` treats `'` as a boundary (unlike a digit), so the shorter name matched inside the
    longer one -- the same false-positive class the `Nat.clog2` test above already forbids."""
    dossier = "# Not to be confused with\n- `Equiv.ofLeftInverse'`: the unconditional variant.\n"
    ok, detail = check_no_real_name_leak(dossier, "Equiv.ofLeftInverse")
    assert ok, detail


def test_exact_qualified_name_is_still_a_leak_even_when_a_primed_variant_is_also_present():
    dossier = "# Object\nSee `Equiv.ofLeftInverse'` and also `Equiv.ofLeftInverse` itself.\n"
    ok, _ = check_no_real_name_leak(dossier, "Equiv.ofLeftInverse")
    assert not ok


def test_round_trip_recalled_target_fires_on_bare_unnamespaced_name_but_not_the_task_symbol():
    """Both directions for the OTHER caller of the shared matcher: RECALLED_TARGET must still
    fire when a candidate body names the real unnamespaced declaration, and must NOT fire when
    it correctly uses the task symbol."""
    assert check_round_trip_recalls_target("fun f => Monotone f", "Monotone") is True
    assert check_round_trip_recalls_target("fun f => VTask.Monotone f", "Monotone") is False


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


def test_worked_example_undecidable_prop_commandless_claim_checked_structurally_not_rejected(mathlib_env):
    """Item 4.1 (2026-07-30): for an undecidable Prop, the dossier prompt now instructs the
    model to omit the runnable command entirely -- this confirms the EXISTING commandless-claim
    path (the `ELABORATED`/`UNCHECKED_PROSE_EXAMPLE` branch above) already does exactly the
    'check structurally, don't execute' thing Item 4.1 asks for, against a genuinely undecidable
    real Prop (an unbounded existential over ℕ -- no `Decidable` instance exists for it, the
    same shape `authoring.preflight`'s own decidability-probe tests use), not a synthetic stand-in."""
    server, env = mathlib_env
    setup = run_checked(
        server,
        Command(cmd="def ConsistencyProbeUndecidable (n : ℕ) : Prop := ∃ m : ℕ, m > n ∧ Even m", env=env),
        timeout=30.0,
    )
    assert setup.status is CheckStatus.PASSED, setup.detail

    dossier = "# Worked examples\n- Claim: ConsistencyProbeUndecidable 5\n"
    checks = check_worked_examples(server, setup.env, dossier)
    assert checks[0].kind == ELABORATED  # elaborates as a Prop -- checked, not rejected, not executed


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
        "# Signature\nThe first argument is the base; the second is the value.\n\n"
        "# Conventions\nFor b <= 1 the junk value 0 is returned.\n\n"
        "# Worked examples\n- Claim: Nat.clog 2 37 = 6\n  ```lean\n  example : Nat.clog 2 37 = 6 := by decide\n  ```\n\n"
        "# Boundaries\nAt b <= 1.\n\n"
        "# Not to be confused with\nNat.log.\n"
    )
    dossier = inject_pinned_signature(dossier, "Nat.clog : Nat -> Nat -> Nat")  # the mechanical, single choke point
    result = check_dossier_consistency(server, env, "Nat.clog : Nat -> Nat -> Nat", dossier, domain)
    assert result.passed
    assert result.flags == []


def test_check_dossier_consistency_end_to_end_fails_on_bad_signature_and_bad_example(mathlib_env):
    """No `inject_pinned_signature` call was made -- exactly what happens if a caller bypasses
    the choke point (a real bug, since both authoring.pipeline and authoring.cleanup always
    call it) -- (c) rejects, same as a genuinely wrong signature always did under the old check."""
    server, env = mathlib_env
    domain = DomainSpec(constraint="True", variables=[], conventions=[ConventionPoint(point=None, statement=None, note="NONE_DECLARED: x")])
    dossier = (
        "# Signature\nWrong signature entirely, never injected.\n\n"
        "# Worked examples\n- Claim: Nat.clog 2 37 = 5\n  ```lean\n  example : Nat.clog 2 37 = 5 := by decide\n  ```\n"
    )
    result = check_dossier_consistency(server, env, "Nat.clog : Nat -> Nat -> Nat", dossier, domain)
    assert not result.passed


# --- (d) real-name leak, end to end: confirms (b) alone cannot catch this ----------------------


def test_worked_example_check_alone_does_not_catch_a_real_name_leak_in_the_code_block(mathlib_env):
    """Confirms the doubt raised in the 2026-07-27 slice report: a worked-example code block
    that (illegitimately) cites the real name instead of the task symbol still EXECUTES
    successfully, because the real name genuinely is true there -- `check_worked_examples`
    alone has no way to tell this apart from a legitimate example. This is exactly what
    happened in the real 2026-07-28 slice run's dossier attempt 3 (`Claim: VTask.clog 2 8 = 3`
    immediately followed by `example : Nat.clog 2 8 = 3 := by decide`)."""
    server, env = mathlib_env
    dossier = (
        "# Worked examples\n- Claim: VTask.clog 2 37 = 6\n"
        "  ```lean\n  example : Nat.clog 2 37 = 6 := by decide\n  ```\n"
    )
    checks = check_worked_examples(server, env, dossier)
    assert checks[0].kind == EXECUTED  # confirmed: (b) alone sees this as a clean pass


def test_check_dossier_consistency_rejects_a_dossier_that_leaks_the_real_name(mathlib_env):
    """The fix: with `forbidden_name` supplied, the SAME leaking dossier from the test above
    now fails `check_dossier_consistency` overall, even though its worked-example check alone
    still (correctly, per that check's own job) reports EXECUTED."""
    server, env = mathlib_env
    domain = DomainSpec(constraint="True", variables=[], conventions=[ConventionPoint(point=None, statement=None, note="NONE_DECLARED: x")])
    dossier = (
        "# Signature\nprose only.\n\n"
        "# Worked examples\n- Claim: VTask.clog 2 37 = 6\n"
        "  ```lean\n  example : Nat.clog 2 37 = 6 := by decide\n  ```\n"
    )
    dossier = inject_pinned_signature(dossier, "VTask.clog : Nat -> Nat -> Nat")
    result = check_dossier_consistency(
        server, env, "VTask.clog : Nat -> Nat -> Nat", dossier, domain, forbidden_name="Nat.clog",
    )
    assert not result.passed
    assert not result.real_name_leak_ok
    assert ReasonCode.DOSSIER_LEAKS_REAL_NAME in result.real_name_leak_detail


def test_check_dossier_consistency_passes_a_clean_task_symbol_only_dossier_with_forbidden_name_given(mathlib_env):
    """Both directions, per instruction: a dossier that correctly uses ONLY the task symbol
    must still pass cleanly once `forbidden_name` is supplied -- no false positive."""
    server, env = mathlib_env
    domain = DomainSpec(constraint="True", variables=[], conventions=[ConventionPoint(point=None, statement=None, note="NONE_DECLARED: x")])
    dossier = (
        "# Signature\nprose only.\n\n"
        "# Worked examples\n- Claim: VTask.clog 2 37 = 6\n"
        "  ```lean\n  example : VTask.clog 2 37 = 6 := by decide\n  ```\n"
    )
    dossier = inject_pinned_signature(dossier, "VTask.clog : Nat -> Nat -> Nat")
    result = check_dossier_consistency(
        server, env, "VTask.clog : Nat -> Nat -> Nat", dossier, domain, forbidden_name="Nat.clog",
    )
    assert result.real_name_leak_ok
    assert result.real_name_leak_detail == ""


def test_check_dossier_consistency_no_forbidden_name_skips_the_leak_check(mathlib_env):
    """Backward compatible: omitting `forbidden_name` (the default) never rejects on this
    check alone, even for a dossier that would otherwise leak -- matching
    `authoring.parse.parse_facts`'s own `forbidden_name=None` convention."""
    server, env = mathlib_env
    domain = DomainSpec(constraint="True", variables=[], conventions=[ConventionPoint(point=None, statement=None, note="NONE_DECLARED: x")])
    dossier = (
        "# Signature\nprose only.\n\n"
        "# Worked examples\n- Claim: Nat.clog 2 37 = 6\n"
        "  ```lean\n  example : Nat.clog 2 37 = 6 := by decide\n  ```\n"
    )
    dossier = inject_pinned_signature(dossier, "Nat.clog : Nat -> Nat -> Nat")
    result = check_dossier_consistency(server, env, "Nat.clog : Nat -> Nat -> Nat", dossier, domain)
    assert result.real_name_leak_ok
    assert result.passed


# --- Matcher consolidation (2026-07-31): one helper, three migrated sites --------------------
#
# Three private "does this text name this declaration" implementations had drifted apart and,
# between them, carried the same self-trigger bug three times. They now share
# `authoring.namematch.name_occurs`. These tests pin the per-site behaviour after migration;
# the existing matcher tests above already cover the semantics themselves.


def test_namematch_is_the_single_implementation_behind_the_consistency_checks():
    """Site 1+2 (dossier leak, round-trip recalled-target): both go through the shared helper
    with IDENTIFIER boundaries -- behaviour unchanged from before consolidation."""
    from authoring.namematch import IDENTIFIER, name_occurs

    for text, forbidden in [
        ("VTask.Monotone f", "Monotone"),
        ("Monotone f", "Monotone"),
        ("fun b n => Nat.clog2 b n", "Nat.clog"),
        ("Equiv.ofLeftInverse'", "Equiv.ofLeftInverse"),
    ]:
        expected = name_occurs(text, forbidden, boundary=IDENTIFIER)
        assert check_no_real_name_leak(text, forbidden)[0] is (not expected)
        assert check_round_trip_recalls_target(text, forbidden) is expected


def test_namematch_substring_mode_preserves_the_parse_layer_semantics():
    """Site 3 (per-fact raw-name leak) keeps its deliberately-stricter no-boundary behaviour,
    now as an explicit SUBSTRING parameter rather than a separate implementation: a name glued
    to more identifier characters still counts there, but NOT under IDENTIFIER mode."""
    from authoring.namematch import IDENTIFIER, SUBSTRING, name_occurs

    assert name_occurs("Nat.clog2 b", "Nat.clog", boundary=SUBSTRING) is True
    assert name_occurs("Nat.clog2 b", "Nat.clog", boundary=IDENTIFIER) is False


def test_namematch_rejects_an_unknown_boundary_mode():
    from authoring.namematch import name_occurs

    with pytest.raises(ValueError, match="boundary must be"):
        name_occurs("x", "x", boundary="fuzzy")
