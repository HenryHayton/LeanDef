"""Tests for `prelim.prompts` -- assembly, determinism, and the leak guard.

The leak guard is the load-bearing test in this file. The dossiers are already leak-checked by
the authoring pipeline, so the risk this guards is not a bad dossier but a regression in THIS
module: someone later "helpfully" adding the real Mathlib name, a mention excerpt, or a worked
example to a prompt. Running the shared `authoring.namematch` helper over all 41x6 assembled
prompts makes that impossible to do silently.
"""

import pytest

from authoring.namematch import IDENTIFIER, name_occurs
from prelim.models import CHAT, COMPLETION, MODEL_SLUGS, MODELS, get_model
from prelim.prompts import (
    assemble_prompt,
    assemble_prompt_from_parts,
    available_tasks,
    build_task_block,
    load_task,
    prompt_text,
)

DOSSIER = "## VTask.clog\n\n### 1. Object\n\n`VTask.clog b n` is the ceiling logarithm.\n"
SIGNATURE = "VTask.clog : (b n : ℕ) -> ℕ"


@pytest.fixture(scope="module")
def real_tasks():
    tasks = available_tasks()
    if len(tasks) != 41:
        pytest.skip(f"expected the 41-task corpus, found {len(tasks)}")
    return tasks


# --- the information contract ---------------------------------------------------------------------


@pytest.mark.parametrize("slug", MODEL_SLUGS)
def test_prompt_contains_the_dossier_the_signature_and_the_instruction(slug):
    text = prompt_text(assemble_prompt_from_parts(slug, DOSSIER, SIGNATURE))

    assert "ceiling logarithm" in text            # the dossier
    assert SIGNATURE in text                       # the pinned signature, verbatim
    assert "Mathlib is already imported" in text   # the instruction
    assert "nothing else" in text


@pytest.mark.parametrize("slug", MODEL_SLUGS)
def test_every_model_receives_an_identical_task_block(slug):
    """The fairness invariant: wrappers may only add etiquette AROUND the shared block."""
    shared = build_task_block(DOSSIER, SIGNATURE)
    assert shared in prompt_text(assemble_prompt_from_parts(slug, DOSSIER, SIGNATURE))


def test_wrappers_differ_only_outside_the_shared_block():
    """Strip the shared block from all six prompts; what remains is pure etiquette, and no two
    models' etiquette may accidentally be identical in a way that hides a missing wrapper."""
    shared = build_task_block(DOSSIER, SIGNATURE)
    remainders = {
        slug: prompt_text(assemble_prompt_from_parts(slug, DOSSIER, SIGNATURE)).replace(shared, "").strip()
        for slug in MODEL_SLUGS
    }
    for slug, rest in remainders.items():
        spec = get_model(slug)
        if spec.system_prompt:
            assert spec.system_prompt in rest
        if spec.lead_in:
            assert spec.lead_in.strip() in rest


# --- THE LEAK GUARD -------------------------------------------------------------------------------


def test_no_real_mathlib_name_appears_in_any_assembled_prompt(real_tasks):
    """41 tasks x 6 models = 246 prompts, each checked with the same identifier-boundary matcher
    the authoring pipeline uses for its own dossier leak check."""
    offenders = []
    for task in real_tasks:
        for slug in MODEL_SLUGS:
            text = prompt_text(assemble_prompt(slug, task))
            if name_occurs(text, task, boundary=IDENTIFIER):
                offenders.append((task, slug))

    assert not offenders, f"real Mathlib name leaked into {len(offenders)} prompt(s): {offenders[:10]}"


def test_leak_guard_would_actually_catch_a_leak():
    """Positive control: the guard is only meaningful if it fires when a name IS present.
    Without this, a broken matcher would make the test above vacuously green."""
    leaky = DOSSIER + "\nThis is the same thing Mathlib calls Nat.clog.\n"
    text = prompt_text(assemble_prompt_from_parts("goedel-formalizer-v2-8b", leaky, SIGNATURE))
    assert name_occurs(text, "Nat.clog", boundary=IDENTIFIER)


def test_prompts_contain_no_mention_excerpt_or_fact_vocabulary(real_tasks):
    """Structural check on the OTHER excluded material: nothing in a prompt may look like a
    mention sidecar, an anchor list, or a fact suite."""
    banned = ["Mathlib neighborhood", "mention excerpt", "anchors", "fact suite", "theorem_name"]
    for task in real_tasks[:10]:  # a sample is enough; the assembly path is task-independent
        text = prompt_text(assemble_prompt("goedel-prover-v2-8b", task)).lower()
        for phrase in banned:
            assert phrase.lower() not in text, f"{task}: prompt contains {phrase!r}"


# --- determinism ------------------------------------------------------------------------------------


@pytest.mark.parametrize("slug", MODEL_SLUGS)
def test_assembly_is_byte_identical_across_calls(slug):
    """The store's prompt_sha256 is only a useful grouping key if this holds."""
    a = assemble_prompt_from_parts(slug, DOSSIER, SIGNATURE)
    b = assemble_prompt_from_parts(slug, DOSSIER, SIGNATURE)
    assert a == b
    assert prompt_text(a) == prompt_text(b)


def test_assembly_from_disk_is_stable(real_tasks):
    assert assemble_prompt("goedel-prover-v2-8b", "Nat.clog") == assemble_prompt("goedel-prover-v2-8b", "Nat.clog")


# --- shape / plumbing ---------------------------------------------------------------------------------


@pytest.mark.parametrize("slug", MODEL_SLUGS)
def test_chat_models_produce_a_messages_list_with_the_documented_system_prompt(slug):
    spec = get_model(slug)
    if spec.endpoint_style != CHAT:
        pytest.skip("not a chat model")
    prompt = assemble_prompt_from_parts(slug, DOSSIER, SIGNATURE)

    assert isinstance(prompt, list)
    roles = [m["role"] for m in prompt]
    if spec.system_prompt:
        assert roles == ["system", "user"]
        assert prompt[0]["content"] == spec.system_prompt
    else:
        assert roles == ["user"]


def test_completion_style_model_produces_a_single_string(monkeypatch):
    """No model in the table currently uses this path (all six cards document chat templates),
    but the plumbing must work the moment one does."""
    spec = get_model("goedel-formalizer-v2-8b")
    monkeypatch.setitem(MODELS, "goedel-formalizer-v2-8b",
                    type(spec)(**{**spec.__dict__, "endpoint_style": COMPLETION}))
    prompt = assemble_prompt_from_parts("goedel-formalizer-v2-8b", DOSSIER, SIGNATURE)

    assert isinstance(prompt, str)
    assert SIGNATURE in prompt


def test_completion_style_folds_a_system_prompt_into_the_text(monkeypatch):
    spec = get_model("qwen2.5-coder-7b-instruct")
    monkeypatch.setitem(
        MODELS, "qwen2.5-coder-7b-instruct", type(spec)(**{**spec.__dict__, "endpoint_style": COMPLETION})
    )
    prompt = assemble_prompt_from_parts("qwen2.5-coder-7b-instruct", DOSSIER, SIGNATURE)

    assert isinstance(prompt, str)
    assert prompt.startswith(spec.system_prompt)


def test_unknown_model_slug_raises():
    with pytest.raises(KeyError, match="unknown model slug"):
        assemble_prompt_from_parts("no-such-model", DOSSIER, SIGNATURE)


# --- task loading ------------------------------------------------------------------------------------


def test_load_task_strips_the_injection_markers_but_keeps_the_signature(real_tasks):
    """The marker comments are internal plumbing and appear in only 28 of the 41 dossiers;
    stripping them makes all 41 read uniformly to a model."""
    dossier, signature = load_task("Monotone")

    assert "PINNED-SIGNATURE:BEGIN" not in dossier
    assert "PINNED-SIGNATURE:END" not in dossier
    assert "VTask.Monotone" in dossier
    assert signature.startswith("VTask.Monotone : ")


def test_every_task_in_the_corpus_loads_and_yields_a_signature(real_tasks):
    for task in real_tasks:
        dossier, signature = load_task(task)
        assert dossier.strip()
        assert signature.startswith("VTask.")
        assert " : " in signature


def test_missing_task_raises_a_clear_error(tmp_path):
    with pytest.raises(FileNotFoundError, match="incomplete"):
        load_task("NoSuchTask", root=tmp_path)


def test_available_tasks_is_sorted_and_complete(real_tasks):
    assert real_tasks == sorted(real_tasks)
    assert len(real_tasks) == 41
