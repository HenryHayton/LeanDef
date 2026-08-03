"""Client + store end-to-end against the stub endpoint -- the shape Stage 3's driver will have,
minus the driver itself.

Deliberately small: two samples for one model/task, checked for full provenance on disk and for
the resume contract holding across a simulated relaunch. Everything real about this test is the
seam between the two modules (does a `GenerationResult` carry what a `Sample` needs?), which is
exactly the thing neither module's own tests can check.
"""

import json

from prelim.client import generate
from prelim.store import build_sample, is_complete, summarize_totals, write_sample
from prelim.stubserver import ScriptedResponse, StubEndpointServer, chat_completion_body

MODEL = "Goedel-LM/Goedel-Prover-V2-8B"
TASK = "Nat.clog"
MESSAGES = [
    {"role": "system", "content": "You are a Lean 4 expert."},
    {"role": "user", "content": "Write the definition described by this dossier."},
]


def _run_one(server, tmp_path, idx, *, temperature=0.7):
    result = generate(
        MESSAGES, temperature=temperature, max_tokens=2048, model_name=MODEL,
        endpoint_url=server.url, log_path=tmp_path / "call_log.jsonl", sleep_fn=lambda s: None,
    )
    sample = build_sample(
        model_name=MODEL, task_name=TASK, sample_index=idx, temperature=temperature,
        max_tokens=2048, prompt_messages=MESSAGES, completion=result.text,
        finish_reason=result.finish_reason, prompt_tokens=result.prompt_tokens,
        completion_tokens=result.completion_tokens, wall_time_s=result.wall_time_s,
        attempts=result.attempts, endpoint_url=server.url,
    )
    return result, write_sample(sample, samples_dir=tmp_path / "samples")


def test_two_samples_land_on_disk_with_full_provenance(tmp_path):
    server = StubEndpointServer([
        ScriptedResponse(200, chat_completion_body("fun b n => sorry", prompt_tokens=210, completion_tokens=12)),
        # Second sample retries once first -- so the stored `attempts` is exercised as a real
        # value rather than always 1.
        ScriptedResponse(500, {"error": {"message": "transient", "type": "InternalError", "code": 500}}),
        ScriptedResponse(200, chat_completion_body("fun b n => Nat.log b n + 1", prompt_tokens=210, completion_tokens=31)),
    ])
    try:
        _run_one(server, tmp_path, 0)
        _run_one(server, tmp_path, 1)
    finally:
        server.stop()

    first = json.loads((tmp_path / "samples" / "goedel-prover-v2-8b" / TASK / "sample_00.json").read_text(encoding="utf-8"))
    second = json.loads((tmp_path / "samples" / "goedel-prover-v2-8b" / TASK / "sample_01.json").read_text(encoding="utf-8"))

    assert first["completion"] == "fun b n => sorry"
    assert first["attempts"] == 1
    assert second["completion"] == "fun b n => Nat.log b n + 1"
    assert second["attempts"] == 2  # the 500 was retried through

    for data, idx in ((first, 0), (second, 1)):
        assert data["model_name"] == MODEL
        assert data["model_slug"] == "goedel-prover-v2-8b"
        assert data["task_name"] == TASK
        assert data["sample_index"] == idx
        assert data["prompt_messages"] == MESSAGES
        assert data["prompt_sha256"] == first["prompt_sha256"]  # same prompt -> same hash
        assert data["prompt_tokens"] == 210
        assert data["finish_reason"] == "stop"
        assert data["wall_time_s"] > 0
        assert data["timestamp"]

    assert summarize_totals(samples_dir=tmp_path / "samples") == {"goedel-prover-v2-8b": 2}

    # Provenance: every attempt logged, including the retried 500 (3 calls -> 3 records).
    log_lines = [json.loads(l) for l in (tmp_path / "call_log.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    assert [r["outcome"] for r in log_lines] == ["success", "retryable_error", "success"]


def test_relaunch_skips_finished_samples_and_only_generates_the_rest(tmp_path):
    """The resume path Stage 3 depends on: after a 'crash' at 2 of 4, a relaunch makes exactly
    two more endpoint calls."""
    server = StubEndpointServer([ScriptedResponse(200, chat_completion_body("body"))])
    try:
        _run_one(server, tmp_path, 0)
        _run_one(server, tmp_path, 1)
        calls_before = server.call_count

        for idx in range(4):
            if is_complete("goedel-prover-v2-8b", TASK, idx, samples_dir=tmp_path / "samples"):
                continue
            _run_one(server, tmp_path, idx)

        assert server.call_count - calls_before == 2  # only samples 2 and 3 regenerated
    finally:
        server.stop()

    assert summarize_totals(samples_dir=tmp_path / "samples") == {"goedel-prover-v2-8b": 4}
