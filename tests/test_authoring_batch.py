"""Tests for `authoring.batch` -- the promoted general batch runner (2026-07-29). Refusal paths
(no preflight, curated-out name) never touch the REPL or Bedrock -- `run_batch` validates before
doing anything else, so a bare-bones `PipelineConfig` with unusable `server`/`client` fields is
fine for those. The credential-expiry/resume path needs a real chunk of the pipeline to actually
run, so it uses the same real-Mathlib-REPL + loopback-stub pattern as `test_authoring_pipeline.py`.
"""

import json

import pytest

from authoring.batch import BatchRefused, load_name_list, run_batch
from authoring.pipeline import DefinitionInput, PipelineConfig
from authoring.task_symbol import task_symbol_for
from bedrock.client import BedrockClient
from harness.repl import get_warm_environment
from harness.results import CheckStatus
from miner.harvest import MentionRecord
from tests.fixtures.bedrock_stub import ScriptedResponse, StubBedrockServer, success_body

DEF_NAME = "Nat.clog"
TASK_SYMBOL = task_symbol_for(DEF_NAME)
SIGNATURE_DICT = {"name": DEF_NAME, "type": "Nat -> Nat -> Nat", "imports": []}

CLASSIFICATION_JSON = json.dumps(
    {
        "regimes": ["casework", "global"], "difficulty": 2,
        "rationale": "computable, boundary-rich, ceiling-log-like",
        "expected_fact_mix": {"casework": 2, "membership": 0, "global": 1},
    }
)


# --- Refusal paths (no REPL, no Bedrock) --------------------------------------------------------


def _dummy_config(tmp_path) -> PipelineConfig:
    """Never actually invoked by the refusal-path tests -- `run_batch` must refuse before
    touching `resolve_definition`/`server`/`client` at all."""
    def _resolve(name: str) -> DefinitionInput:
        raise AssertionError(f"resolve_definition({name!r}) called -- refusal path must not reach this")

    return PipelineConfig(
        client=None, authoring_model_id="m", flagship_model_id="m",
        server=None, base_env=0, resolve_definition=_resolve,
        output_dir=tmp_path / "output", batch_review_dir=tmp_path / "review",
    )


def test_refuses_without_a_preflight_file(tmp_path):
    names_file = tmp_path / "names.txt"
    names_file.write_text("Nat.clog\nNat.choose\n")
    config = _dummy_config(tmp_path)

    with pytest.raises(BatchRefused, match="no preflight file"):
        run_batch(names_file, config, preflight_path=tmp_path / "does_not_exist.json")


def test_refuses_when_a_name_is_missing_from_preflight(tmp_path):
    names_file = tmp_path / "names.txt"
    names_file.write_text("Nat.clog\nNat.choose\n")
    preflight_path = tmp_path / "preflight.json"
    preflight_path.write_text(json.dumps({"Nat.clog": {"status": "pass"}}))  # Nat.choose missing
    config = _dummy_config(tmp_path)

    with pytest.raises(BatchRefused, match="Nat.choose"):
        run_batch(names_file, config, preflight_path=preflight_path)


def test_refuses_when_a_name_failed_preflight(tmp_path):
    names_file = tmp_path / "names.txt"
    names_file.write_text("Nat.leRec\n")
    preflight_path = tmp_path / "preflight.json"
    preflight_path.write_text(json.dumps({"Nat.leRec": {"status": "fail", "category": "pp_elision"}}))
    config = _dummy_config(tmp_path)

    with pytest.raises(BatchRefused):
        run_batch(names_file, config, preflight_path=preflight_path)


def test_refuses_a_curated_out_name_even_with_passing_preflight(tmp_path):
    """Belt-and-braces: a name can have a clean preflight pass (its pinned type really does
    re-elaborate) and still be refused because curation excludes it -- the two checks are
    independent, matching `miner/output/excluded_recursor_class.json`'s own framing (the
    pretty-printer failure was NOT the load-bearing reason those 6 stay excluded)."""
    names_file = tmp_path / "names.txt"
    names_file.write_text("Nat.leRec\n")
    preflight_path = tmp_path / "preflight.json"
    preflight_path.write_text(json.dumps({"Nat.leRec": {"status": "pass", "pinned_type": "whatever"}}))
    curation_path = tmp_path / "curation.yaml"
    curation_path.write_text("entries:\n  - name: Nat.leRec\n    action: exclude\n    reason: test\n")
    config = _dummy_config(tmp_path)

    with pytest.raises(BatchRefused, match="Nat.leRec"):
        run_batch(names_file, config, preflight_path=preflight_path, curation_yaml_path=curation_path)


def test_clean_preflight_and_no_curation_conflict_does_not_refuse_at_validation(tmp_path):
    """Positive control for the two refusal tests above -- confirms the validation step itself
    doesn't over-fire (a subtly-broken `_validate_preflight_and_curation` could refuse
    everything, and the negative tests alone wouldn't catch that)."""
    from authoring.batch import _validate_preflight_and_curation

    preflight_path = tmp_path / "preflight.json"
    preflight_path.write_text(json.dumps({"Nat.clog": {"status": "pass"}}))
    curation_path = tmp_path / "curation.yaml"
    curation_path.write_text("entries:\n  - name: SomeOtherName\n    action: exclude\n    reason: test\n")
    _validate_preflight_and_curation(["Nat.clog"], preflight_path, curation_path)  # must not raise


def test_load_name_list_ignores_blank_lines_and_comments(tmp_path):
    names_file = tmp_path / "names.txt"
    names_file.write_text("# a comment\nNat.clog\n\nNat.choose\n  \n")
    assert load_name_list(names_file) == ["Nat.clog", "Nat.choose"]


# --- Credential-expiry / resume path (real REPL + loopback stub) --------------------------------


@pytest.fixture(scope="module")
def mathlib_env():
    server, import_result = get_warm_environment()
    assert import_result.status is CheckStatus.PASSED, import_result.detail
    yield server, import_result.env
    server.kill()


@pytest.fixture
def stub_server():
    server = None

    def _make(script):
        nonlocal server
        server = StubBedrockServer(script)
        return server

    yield _make
    if server is not None:
        server.stop()


def _real_config(server, env, tmp_path, bedrock_server) -> PipelineConfig:
    client = BedrockClient(endpoint_url=bedrock_server.url, log_path=tmp_path / "log.jsonl", sleep_fn=lambda s: None)

    def _resolve(name: str) -> DefinitionInput:
        return DefinitionInput(
            name=DEF_NAME, signature_dict=SIGNATURE_DICT, definition_source="context only",
            docstring="the ceiling logarithm", return_shape="value",
            mention_records=[MentionRecord(theorem_name="Nat.clog_pow", source_file="Data/Nat/Log.lean", statement_text="Nat.clog b (b ^ n) = n")],
        )

    return PipelineConfig(
        client=client, authoring_model_id="test-model", flagship_model_id="test-model",
        server=server, base_env=env, resolve_definition=_resolve,
        output_dir=tmp_path / "output", batch_review_dir=tmp_path / "review",
        max_calls_per_task=1,  # every task rotates immediately at classification -- cheap, fast
    )


def test_credential_expiry_writes_resume_file_with_exactly_the_unprocessed_names(mathlib_env, stub_server, tmp_path):
    server, env = mathlib_env
    names_file = tmp_path / "names.txt"
    names_file.write_text("Nat.clog\nNat.clog\nNat.clog\n")  # 3 entries, chunk_size=1 -> 3 chunks
    preflight_path = tmp_path / "preflight.json"
    preflight_path.write_text(json.dumps({"Nat.clog": {"status": "pass"}}))

    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),  # chunk 1: burns its only call
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),  # chunk 2: burns its only call
            # chunk 3 must never be sent -- credentials fail before it starts
        ]
    )
    config = _real_config(server, env, tmp_path, bedrock_server)

    calls = {"n": 0}

    def fake_credentials_check():
        calls["n"] += 1
        return calls["n"] <= 2  # True, True, then False on the 3rd chunk

    result = run_batch(
        names_file, config, preflight_path=preflight_path, chunk_size=1,
        credentials_check=fake_credentials_check,
    )

    assert result.status == "credentials_expired"
    assert len(result.results) == 2  # exactly the 2 processed chunks
    assert result.processed_names == ["Nat.clog", "Nat.clog"]
    assert result.unprocessed_names == ["Nat.clog"]
    assert result.resume_path is not None
    assert result.resume_path.exists()
    resume_names = load_name_list(result.resume_path)
    assert resume_names == ["Nat.clog"]
    assert len(bedrock_server.requests_received) == 2  # never touched the 3rd chunk's response


def test_resuming_from_the_resume_file_does_not_rerun_processed_names(mathlib_env, stub_server, tmp_path):
    """Calling `run_batch` again with the resume file AS the new names_file only runs the
    unprocessed remainder -- no special 'resume mode' needed, confirmed by exact call count."""
    server, env = mathlib_env
    names_file = tmp_path / "names.txt"
    names_file.write_text("Nat.clog\nNat.clog\nNat.clog\n")
    preflight_path = tmp_path / "preflight.json"
    preflight_path.write_text(json.dumps({"Nat.clog": {"status": "pass"}}))

    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
        ]
    )
    config = _real_config(server, env, tmp_path, bedrock_server)
    calls = {"n": 0}
    first = run_batch(
        names_file, config, preflight_path=preflight_path, chunk_size=1,
        credentials_check=lambda: (calls.__setitem__("n", calls["n"] + 1) or calls["n"] <= 2),
    )
    assert first.status == "credentials_expired"
    assert len(bedrock_server.requests_received) == 2

    # Resume: credentials are alive again now; only the resume file's 1 remaining name must run.
    bedrock_server2 = stub_server([ScriptedResponse(200, success_body(CLASSIFICATION_JSON))])
    config2 = _real_config(server, env, tmp_path, bedrock_server2)
    second = run_batch(
        first.resume_path, config2, preflight_path=preflight_path, chunk_size=1,
        credentials_check=lambda: True,
    )
    assert second.status == "completed"
    assert len(second.results) == 1
    assert len(bedrock_server2.requests_received) == 1  # exactly the 1 remaining name, nothing re-run


def test_batch_review_written_and_carry_on_mode_never_halts(mathlib_env, stub_server, tmp_path):
    server, env = mathlib_env
    names_file = tmp_path / "names.txt"
    names_file.write_text("Nat.clog\nNat.clog\n")
    preflight_path = tmp_path / "preflight.json"
    preflight_path.write_text(json.dumps({"Nat.clog": {"status": "pass"}}))

    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
        ]
    )
    config = _real_config(server, env, tmp_path, bedrock_server)
    result = run_batch(
        names_file, config, preflight_path=preflight_path, chunk_size=8,
        credentials_check=lambda: True,
    )

    assert result.status == "completed"
    assert len(result.results) == 2
    assert all(r.outcome == "ROTATED" for r in result.results)  # max_calls_per_task=1 forces this
    assert result.review_path is not None
    assert result.review_path.exists()
    assert "Tasks: 2" in result.review_path.read_text()
