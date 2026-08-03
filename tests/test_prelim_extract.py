"""Tests for `prelim.extract` -- pure text, no endpoint, milliseconds.

The six per-model fixtures are the headline: extraction must survive six genuinely different
output dialects. The adversarial fixtures cover the failure modes that are DATA rather than bugs
(no def, truncation, ambiguity) and the ones that are recoverable-with-a-flag (renamed symbol).
"""

import pytest

from prelim.extract import (
    MULTIPLE_AMBIGUOUS,
    NO_DEF_FOUND,
    TRUNCATED_MID_DEF,
    Extraction,
    ExtractionFailure,
    extract_definition,
)
from prelim.models import MODEL_SLUGS
from tests.fixtures import prelim_completions as fx


# --- the six model dialects ---------------------------------------------------------------------


@pytest.mark.parametrize("slug", MODEL_SLUGS)
def test_extracts_from_every_model_dialect(slug):
    """6/6: one realistic completion per candidate model, each in that model's own style."""
    result = extract_definition(slug, fx.BY_MODEL[slug])

    assert isinstance(result, Extraction), f"{slug}: {result}"
    assert result.declared_name == "VTask.clog"
    assert result.renamed_symbol is False
    assert result.code.startswith(("def", "noncomputable def"))
    assert ":=" in result.code
    assert "VTask.clog" in result.code


@pytest.mark.parametrize("slug", MODEL_SLUGS)
def test_extraction_never_captures_surrounding_prose(slug):
    """The commentary these models wrap around their code must not survive into the definition."""
    code = extract_definition(slug, fx.BY_MODEL[slug]).code

    for prose in ("Proof Plan", "step by step", "Let me know", "<think>", "This handles all"):
        assert prose not in code


def test_goedel_cot_plan_is_stripped_but_body_survives_intact():
    """The long plan before the fence goes; the multi-line body -- including its indented
    `have` -- stays whole."""
    result = extract_definition("goedel-prover-v2-8b", fx.GOEDEL)

    assert "We need to define" not in result.code
    assert "have : (n + b - 1) / b < n" in result.code  # indented continuation kept
    assert result.from_fence is True


def test_kimina_think_block_is_not_mistaken_for_code():
    result = extract_definition("kimina-prover-distill-7b", fx.KIMINA_PROVER)
    assert "</think>" not in result.code
    assert result.code.startswith("noncomputable def")


def test_autoformalizer_header_import_is_not_part_of_the_definition():
    """It emits `import Mathlib` first; the extracted definition must start at the `def`."""
    result = extract_definition("kimina-autoformalizer-7b", fx.KIMINA_AUTOFORMALIZER)
    assert "import Mathlib" not in result.code
    assert result.code.startswith("def VTask.clog")


def test_bare_declaration_without_any_fence_is_found():
    result = extract_definition("qwen2.5-coder-7b-instruct", fx.BARE_NO_FENCE)
    assert isinstance(result, Extraction)
    assert result.from_fence is False
    assert result.code.startswith("noncomputable def VTask.clog")
    assert "That should satisfy" not in result.code  # trailing prose cut
    assert result.truncated_trailing is True


# --- choosing between candidates -----------------------------------------------------------------


def test_multiple_fences_takes_the_last_vtask_declaration():
    """A model that sketches then revises: the fix comes last."""
    result = extract_definition("goedel-prover-v2-8b", fx.TWO_FENCES_LAST_WINS)
    assert isinstance(result, Extraction)
    assert result.n_candidates == 2
    assert ":= sorry" not in result.code  # took the filled-in one, not the stub


def test_single_renamed_declaration_is_accepted_and_flagged():
    """Scoring splices under our name anyway, so this is an answer -- but the flag records that
    the naming instruction was not followed, which is itself a measurement."""
    result = extract_definition("herald-7b", fx.RENAMED)
    assert isinstance(result, Extraction)
    assert result.renamed_symbol is True
    assert result.declared_name == "clog"


def test_multiple_declarations_none_named_vtask_is_ambiguous():
    """Guessing would silently score the wrong body."""
    result = extract_definition("herald-7b", fx.AMBIGUOUS)
    assert isinstance(result, ExtractionFailure)
    assert result.reason == MULTIPLE_AMBIGUOUS
    assert result.n_candidates == 2
    assert "clogFloor" in result.detail and "clogCeil" in result.detail


# --- failures that are data ------------------------------------------------------------------------


def test_no_declaration_anywhere_is_no_def_found():
    result = extract_definition("qwen2.5-coder-7b-instruct", fx.NO_DEF)
    assert isinstance(result, ExtractionFailure)
    assert result.reason == NO_DEF_FOUND
    assert result.partial  # keeps a fragment for eyeballing


def test_empty_completion_is_no_def_found():
    result = extract_definition("herald-7b", "")
    assert isinstance(result, ExtractionFailure)
    assert result.reason == NO_DEF_FOUND


def test_truncated_generation_with_length_finish_reason_is_reported_as_truncation():
    """Distinguished from a refusal: the model was cut off, it did not decline."""
    result = extract_definition("deepseek-prover-v2-7b", fx.TRUNCATED, finish_reason="length")
    assert isinstance(result, ExtractionFailure)
    assert result.reason == TRUNCATED_MID_DEF


def test_same_truncated_text_without_length_finish_reason_is_not_called_truncation():
    """`finish_reason` is what separates 'ran out of tokens' from 'produced something odd' --
    without it we must not claim truncation we cannot see."""
    result = extract_definition("deepseek-prover-v2-7b", fx.TRUNCATED)
    if isinstance(result, ExtractionFailure):
        assert result.reason != TRUNCATED_MID_DEF
    else:
        assert isinstance(result, Extraction)  # a partial def is still extractable text


def test_complete_definition_with_length_finish_reason_is_still_accepted():
    """A generation that hit the cap AFTER finishing the declaration is fine -- the cap fell in
    the trailing prose, not the code."""
    text = fx.HERALD + "\n\nAdditional commentary that got cut off half way thr"
    result = extract_definition("herald-7b", text, finish_reason="length")
    assert isinstance(result, Extraction)
    assert result.declared_name == "VTask.clog"


# --- determinism ------------------------------------------------------------------------------------


@pytest.mark.parametrize("slug", MODEL_SLUGS)
def test_extraction_is_deterministic(slug):
    a = extract_definition(slug, fx.BY_MODEL[slug])
    b = extract_definition(slug, fx.BY_MODEL[slug])
    assert a == b
