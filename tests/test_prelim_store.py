"""Tests for `prelim.store` -- pure filesystem, no endpoint, no GPU, milliseconds.

The load-bearing behaviour here is the resume contract (`is_complete`): Stage 3's driver relaunches
against a partly-populated tree and must skip exactly the finished work and no more. Both
directions are tested, plus the two ways a file can look present without being done.
"""

import json
import os

import pytest

from prelim.store import (
    SAMPLE_SCHEMA_VERSION,
    build_sample,
    is_complete,
    model_slug,
    prompt_sha256,
    read_sample,
    sample_path,
    summarize,
    summarize_totals,
    write_sample,
)

MESSAGES = [{"role": "user", "content": "Define the ceiling logarithm."}]


def _sample(tmp_path, *, model="Goedel-LM/Goedel-Prover-V2-8B", task="Nat.clog", idx=0, completion="a body"):
    s = build_sample(
        model_name=model, task_name=task, sample_index=idx, temperature=0.7, max_tokens=2048,
        prompt_messages=MESSAGES, completion=completion, finish_reason="stop",
        prompt_tokens=120, completion_tokens=44, wall_time_s=3.5, attempts=1,
        endpoint_url="http://127.0.0.1:8000/v1/chat/completions",
    )
    return s, write_sample(s, samples_dir=tmp_path)


# --- slug ---------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "name,expected",
    [
        ("Goedel-LM/Goedel-Prover-V2-8B", "goedel-prover-v2-8b"),
        ("deepseek-ai/DeepSeek-Prover-V2-7B", "deepseek-prover-v2-7b"),
        ("internlm/internlm2_5-step-prover", "internlm2-5-step-prover"),
        ("Qwen/Qwen2.5-Math-7B-Instruct", "qwen2-5-math-7b-instruct"),
        ("bare-name-no-org", "bare-name-no-org"),
    ],
)
def test_model_slug_is_filesystem_safe(name, expected):
    slug = model_slug(name)
    assert slug == expected
    assert "/" not in slug and " " not in slug
    assert slug == slug.lower()


@pytest.mark.parametrize("bad", ["", "   ", "///", "!!!"])
def test_model_slug_rejects_unusable_names(bad):
    with pytest.raises(ValueError):
        model_slug(bad)


# --- prompt hash --------------------------------------------------------------------------------


def test_prompt_sha256_is_stable_and_order_insensitive_within_a_message():
    a = [{"role": "user", "content": "x"}]
    b = [{"content": "x", "role": "user"}]  # same message, keys written in a different order
    assert prompt_sha256(a) == prompt_sha256(b)


def test_prompt_sha256_differs_for_different_prompts():
    assert prompt_sha256([{"role": "user", "content": "x"}]) != prompt_sha256([{"role": "user", "content": "y"}])


# --- write / read -------------------------------------------------------------------------------


def test_write_sample_lands_at_the_documented_path(tmp_path):
    _, path = _sample(tmp_path)
    assert path == tmp_path / "goedel-prover-v2-8b" / "Nat.clog" / "sample_00.json"
    assert path.exists()


def test_written_sample_is_self_describing(tmp_path):
    sample, path = _sample(tmp_path, idx=7)
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["schema_version"] == SAMPLE_SCHEMA_VERSION
    assert data["model_name"] == "Goedel-LM/Goedel-Prover-V2-8B"
    assert data["model_slug"] == "goedel-prover-v2-8b"
    assert data["task_name"] == "Nat.clog"
    assert data["sample_index"] == 7
    assert data["temperature"] == 0.7
    assert data["max_tokens"] == 2048
    assert data["prompt_messages"] == MESSAGES  # the EXACT prompt sent
    assert data["prompt_sha256"] == prompt_sha256(MESSAGES)
    assert data["completion"] == "a body"
    assert data["finish_reason"] == "stop"
    assert data["prompt_tokens"] == 120 and data["completion_tokens"] == 44
    assert data["wall_time_s"] == 3.5
    assert data["attempts"] == 1
    assert data["endpoint_url"].startswith("http://")
    assert data["timestamp"].endswith("+00:00")


def test_write_is_atomic_leaving_no_temp_files_behind(tmp_path):
    _, path = _sample(tmp_path)
    leftovers = [p.name for p in path.parent.iterdir() if p.name != path.name]
    assert leftovers == []


def test_write_uses_same_directory_temp_so_replace_stays_atomic(tmp_path, monkeypatch):
    """`os.replace` is only atomic within one filesystem, so the temp file must be created in the
    destination directory -- not /tmp. Asserted by capturing mkstemp's `dir=`."""
    seen = {}
    import tempfile as _tempfile

    real_mkstemp = _tempfile.mkstemp

    def spy(*args, **kwargs):
        seen["dir"] = kwargs.get("dir")
        return real_mkstemp(*args, **kwargs)

    monkeypatch.setattr("prelim.store.tempfile.mkstemp", spy)
    _, path = _sample(tmp_path)
    assert seen["dir"] == str(path.parent)


def test_overwriting_an_existing_sample_replaces_it_cleanly(tmp_path):
    _sample(tmp_path, completion="first")
    _, path = _sample(tmp_path, completion="second")
    assert json.loads(path.read_text(encoding="utf-8"))["completion"] == "second"


def test_read_sample_returns_none_for_missing_or_unparseable(tmp_path):
    assert read_sample(tmp_path / "nope.json") is None
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    assert read_sample(bad) is None


# --- the resume contract ------------------------------------------------------------------------


def test_is_complete_false_when_absent(tmp_path):
    assert is_complete("goedel-prover-v2-8b", "Nat.clog", 0, samples_dir=tmp_path) is False


def test_is_complete_true_for_a_written_sample(tmp_path):
    _sample(tmp_path)
    assert is_complete("goedel-prover-v2-8b", "Nat.clog", 0, samples_dir=tmp_path) is True


def test_resume_skips_complete_and_retries_incomplete(tmp_path):
    """The driver's actual question, both directions in one place."""
    _sample(tmp_path, idx=0)
    _sample(tmp_path, idx=1)
    todo = [i for i in range(4) if not is_complete("goedel-prover-v2-8b", "Nat.clog", i, samples_dir=tmp_path)]
    assert todo == [2, 3]


def test_corrupt_file_is_not_complete_and_is_renamed_aside(tmp_path):
    """A half-written file must never be mistaken for finished work -- and must be preserved for
    inspection, not silently overwritten."""
    path = sample_path("goedel-prover-v2-8b", "Nat.clog", 3, samples_dir=tmp_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('{"model_name": "truncated mid-w', encoding="utf-8")

    assert is_complete("goedel-prover-v2-8b", "Nat.clog", 3, samples_dir=tmp_path) is False
    assert not path.exists()
    quarantined = path.with_suffix(path.suffix + ".corrupt")
    assert quarantined.exists()
    assert quarantined.read_text(encoding="utf-8").startswith('{"model_name": "truncated')


def test_null_completion_is_not_complete_and_is_renamed_aside(tmp_path):
    """Parses fine, but the work genuinely is not done."""
    sample, path = _sample(tmp_path, idx=4, completion=None)
    assert is_complete("goedel-prover-v2-8b", "Nat.clog", 4, samples_dir=tmp_path) is False
    assert path.with_suffix(path.suffix + ".corrupt").exists()


def test_quarantined_file_does_not_block_a_later_rewrite(tmp_path):
    """After quarantine the driver regenerates: the new write must land normally."""
    path = sample_path("goedel-prover-v2-8b", "Nat.clog", 5, samples_dir=tmp_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("garbage", encoding="utf-8")
    assert is_complete("goedel-prover-v2-8b", "Nat.clog", 5, samples_dir=tmp_path) is False

    _sample(tmp_path, idx=5, completion="regenerated")
    assert is_complete("goedel-prover-v2-8b", "Nat.clog", 5, samples_dir=tmp_path) is True


# --- summarize ------------------------------------------------------------------------------------


def test_summarize_counts_per_model_and_task(tmp_path):
    _sample(tmp_path, task="Nat.clog", idx=0)
    _sample(tmp_path, task="Nat.clog", idx=1)
    _sample(tmp_path, task="Monotone", idx=0)
    _sample(tmp_path, model="deepseek-ai/DeepSeek-Prover-V2-7B", task="Nat.clog", idx=0)

    assert summarize(samples_dir=tmp_path) == {
        "deepseek-prover-v2-7b": {"Nat.clog": 1},
        "goedel-prover-v2-8b": {"Monotone": 1, "Nat.clog": 2},
    }


def test_summarize_excludes_incomplete_samples(tmp_path):
    """The summary must never claim work the resume logic would redo."""
    _sample(tmp_path, idx=0)
    bad = sample_path("goedel-prover-v2-8b", "Nat.clog", 1, samples_dir=tmp_path)
    bad.write_text("truncated", encoding="utf-8")

    assert summarize(samples_dir=tmp_path) == {"goedel-prover-v2-8b": {"Nat.clog": 1}}


def test_summarize_totals_gives_the_one_line_form(tmp_path):
    _sample(tmp_path, task="Nat.clog", idx=0)
    _sample(tmp_path, task="Monotone", idx=0)
    _sample(tmp_path, model="deepseek-ai/DeepSeek-Prover-V2-7B", task="Nat.clog", idx=0)

    assert summarize_totals(samples_dir=tmp_path) == {
        "deepseek-prover-v2-7b": 1,
        "goedel-prover-v2-8b": 2,
    }


def test_summarize_on_an_empty_tree_is_empty_not_an_error(tmp_path):
    assert summarize(samples_dir=tmp_path / "does-not-exist") == {}
