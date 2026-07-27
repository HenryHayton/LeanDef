"""Tests for `authoring.prompt_loader` against the real files under `authoring/prompts/` --
this is the one place those files are exercised as code, not just read as text."""

import pytest

from authoring.prompt_loader import PromptTemplateError, load_prompt_template

ALL_CALL_NAMES = ["classification", "dossier", "fact_proposal", "round_trip"]


@pytest.mark.parametrize("name", ALL_CALL_NAMES)
def test_every_contract_call_has_a_template_file(name):
    template = load_prompt_template(name)
    assert template.name == name
    assert template.system_template.strip() != ""
    assert template.user_template.strip() != ""


def test_classification_template_renders_with_its_declared_inputs():
    template = load_prompt_template("classification")
    system, user = template.render(
        pinned_signature="Nat.clog : Nat -> Nat -> Nat",
        docstring="ceiling log",
        definition_source="def clog := ...",
        mention_sidecar_excerpt="- Nat.clog_pow: ...",
    )
    assert "Nat.clog" in user
    assert "casework" in system  # vocabulary note present, not "decidable"
    assert "{" not in user  # no leftover unrendered placeholder


def test_fact_proposal_template_does_not_declare_definition_source_as_an_input():
    """Contract §4: facts are proposed from the dossier only -- the definition source must not
    be one of this template's placeholders."""
    template = load_prompt_template("fact_proposal")
    assert "{definition_source}" not in template.user_template
    assert "{definition_source}" not in template.system_template


def test_round_trip_template_only_declares_dossier_and_signature_as_inputs():
    """Contract §5's information hygiene: no definition source, no fact suite, no mention
    sidecar in the round-trip prompt."""
    template = load_prompt_template("round_trip")
    combined = template.system_template + template.user_template
    for forbidden in ("{definition_source}", "{mention_sidecar_excerpt}", "{facts}"):
        assert forbidden not in combined
    system, user = template.render(
        pinned_signature="rtDouble : Nat -> Nat",
        dossier_md="# Object\n...",
    )
    assert "{" not in user


def test_missing_input_raises_prompt_template_error():
    template = load_prompt_template("classification")
    with pytest.raises(PromptTemplateError):
        template.render(pinned_signature="x")  # missing docstring/definition_source/mentions


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_prompt_template("does_not_exist")
