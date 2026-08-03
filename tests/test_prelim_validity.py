"""Tests for `prelim.validity` -- the first-3 gate.

The gate's job is to distinguish "our wrapper is broken for this model" from "this model is bad
at the task", early and cheaply. Both directions matter: a false PASS wastes a night on 410
useless samples, and a false FAIL throws away a legitimate low-scoring model whose numbers we
actually want.
"""

import pytest

from prelim.models import MODEL_SLUGS
from prelim.validity import GATE_SAMPLE_COUNT, check_early_samples
from tests.fixtures import prelim_completions as fx


def _samples(*texts, finish_reason=None):
    return [(t, finish_reason) for t in texts]


# --- passing ---------------------------------------------------------------------------------------


@pytest.mark.parametrize("slug", MODEL_SLUGS)
def test_gate_passes_on_each_model_s_realistic_output(slug):
    """All six dialects clear the gate -- if any did not, that model's night would be cancelled
    before it began."""
    result = check_early_samples(slug, _samples(*[fx.BY_MODEL[slug]] * GATE_SAMPLE_COUNT))

    assert result.passed
    assert result.n_plausible == GATE_SAMPLE_COUNT


def test_one_good_sample_out_of_three_is_enough():
    """Deliberately permissive: a model producing two failures and one rough definition is a
    legitimate low scorer, not a broken template."""
    result = check_early_samples("herald-7b", _samples(fx.NO_DEF, fx.HERALD, fx.NO_DEF))

    assert result.passed
    assert result.n_plausible == 1
    assert [v.extracted for v in result.verdicts] == [False, True, False]


def test_renamed_symbol_still_passes_the_gate():
    """The gate asks whether output is structurally plausible Lean, not whether it obeyed the
    naming instruction -- that is scoring's business."""
    assert check_early_samples("herald-7b", _samples(fx.RENAMED)).passed


# --- failing -----------------------------------------------------------------------------------------


def test_gate_fails_when_nothing_extracts():
    result = check_early_samples("qwen2.5-coder-7b-instruct", _samples(fx.NO_DEF, fx.NO_DEF, fx.NO_DEF))

    assert result.passed is False
    assert result.n_plausible == 0
    assert "template" in result.summary  # points the reader at OUR bug first
    assert "no_def_found" in result.summary


def test_gate_fails_on_three_truncations_and_names_the_reason():
    result = check_early_samples(
        "deepseek-prover-v2-7b", _samples(*[fx.TRUNCATED] * 3, finish_reason="length")
    )

    assert result.passed is False
    assert "truncated_mid_def" in result.summary


def test_gate_fails_on_trivially_short_definitions():
    """`def f := 0` extracts fine but is not an answer to any signature in this corpus."""
    result = check_early_samples("herald-7b", _samples("```lean\ndef VTask.f := 0\n```"))

    assert result.passed is False
    assert result.verdicts[0].extracted is True   # it DID extract...
    assert result.verdicts[0].plausible is False  # ...but is too short to be real
    assert result.verdicts[0].length < 40


def test_gate_fails_on_empty_sample_list():
    """No evidence of working output is not the same as evidence of working output."""
    result = check_early_samples("herald-7b", [])

    assert result.passed is False
    assert result.n_checked == 0
    assert "cannot establish" in result.summary


def test_gate_fails_when_extraction_succeeds_but_there_is_no_assignment():
    """A theorem-shaped or stub-shaped body with no `:=` is not a definition."""
    result = check_early_samples("herald-7b", _samples("```lean\ndef VTask.clog (b n : ℕ) : ℕ\n```"))

    assert result.passed is False
    assert result.verdicts[0].has_assign is False


# --- reporting ---------------------------------------------------------------------------------------


def test_report_lines_are_loud_and_per_sample():
    result = check_early_samples("herald-7b", _samples(fx.NO_DEF, fx.HERALD))
    lines = result.report_lines()

    assert lines[0].startswith("[gate] herald-7b: PASS")
    assert len(lines) == 3  # header + one line per sample
    assert "reason=no_def_found" in lines[1]
    assert "reason=" not in lines[2]  # the successful one carries no failure reason


def test_failing_report_says_fail_in_the_header():
    result = check_early_samples("herald-7b", _samples(fx.NO_DEF))
    assert result.report_lines()[0].startswith("[gate] herald-7b: FAIL")
