"""Tests for `authoring.pipeline.author_task`/`author_batch` -- the top-level driver chaining
every station built across the prior two sessions. No real Bedrock call anywhere (the loopback
stub only, extended here with scripted responses for a full happy path and the four required
unhappy paths); real Mathlib REPL throughout, since most stages (dossier consistency, mechanical
validation, round-trip scoring, axiom baseline) are fundamentally REPL-backed and there's no
ground truth to fake.

**Why a fresh stand-in definition, not the real `Nat.clog`, for the pinned/spliced identity**:
confirmed empirically while building this file -- splicing a round-trip candidate under a name
that already exists in the base (Mathlib-imported) environment fails outright:
`` `Nat.clog` has already been declared ``. This blocks round-trip scoring for ANY genuinely
mined task pinned under its real Mathlib name in the SAME environment Mathlib was imported
into -- a pre-existing architectural gap in `harness.scoring`/`harness.admissibility` (both
built in an earlier session), not something this task's Parts 1/2 were asked to fix, and
squarely out of this task's "no harness/ scoring-semantics changes" rule. Reported prominently
in the implementation report, not silently worked around: this file's `pipelineClog` is a
fresh, non-colliding stand-in mirroring `Nat.clog`'s own junk-value shape closely enough to
write a believable dossier/facts about (the same workaround `tests/test_authoring_roundtrip.py`
already established with its own `rtDouble`, applied here at the pipeline level).

The end-to-end test still uses **genuinely real** mention-sidecar data -- `Nat.clog`'s own
34 real mentions, loaded from `miner/output/mention_names.jsonl` -- as `pipelineClog`'s
`mention_records`, since the station actually being exercised with real production data is
mention retrieval, not the round-trip splice identity.
"""

import json
from pathlib import Path

import pytest

from authoring.pipeline import DefinitionInput, PipelineConfig, author_batch, author_task, render_batch_review
from bedrock.client import BedrockClient
from harness.repl import get_warm_environment, run_checked
from harness.results import CheckStatus
from harness.task_schema import validate_task_dir
from lean_interact import Command
from miner.harvest import DefinitionMentions, MentionRecord
from tests.fixtures.bedrock_stub import ScriptedResponse, StubBedrockServer, success_body

DEF_NAME = "pipelineClog"
SIGNATURE_DICT = {"name": DEF_NAME, "type": "Nat -> Nat -> Nat", "imports": []}
PINNED_SIG = f"{DEF_NAME} : Nat -> Nat -> Nat"
DEFINITION_SOURCE = f"def {DEF_NAME} (b n : Nat) : Nat := if b <= 1 ∨ n <= 1 then 0 else Nat.clog b n"

SYNTHETIC_MENTIONS = [
    MentionRecord(theorem_name="Nat.clog_pow", source_file="Data/Nat/Log.lean", statement_text="Nat.clog b (b ^ n) = n"),
]


@pytest.fixture(scope="module")
def mathlib_env():
    """Yields `(server, ground_truth_env, round_trip_base_env)`. Two DIFFERENT environments,
    deliberately: `ground_truth_env` has `pipelineClog` already declared (needed for mechanical
    validation, §3.4(b)'s worked-example execution, and the axiom baseline); `round_trip_base_env`
    is the plain import BEFORE that splice, since round-trip candidate splicing under the SAME
    name into an environment that already has it declared fails outright (see this module's own
    docstring -- confirmed against real `Nat.clog`, and the reason `PipelineConfig` grew a
    second env field while building this file)."""
    server, import_result = get_warm_environment()
    assert import_result.status is CheckStatus.PASSED, import_result.detail
    define = run_checked(server, Command(cmd=DEFINITION_SOURCE, env=import_result.env), timeout=60.0)
    assert define.status is CheckStatus.PASSED, define.detail
    yield server, define.env, import_result.env
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


def _config(server, env, rt_base_env, tmp_path, bedrock_server, *, max_calls_per_task=12, mention_records=None) -> PipelineConfig:
    client = BedrockClient(endpoint_url=bedrock_server.url, log_path=tmp_path / "log.jsonl", sleep_fn=lambda s: None)

    def _resolve(name: str) -> DefinitionInput:
        return DefinitionInput(
            name=DEF_NAME,
            signature_dict=SIGNATURE_DICT,
            definition_source=DEFINITION_SOURCE,
            docstring="a ceiling-log-like helper for pipeline tests",
            mention_records=mention_records if mention_records is not None else SYNTHETIC_MENTIONS,
        )

    return PipelineConfig(
        client=client, authoring_model_id="test-authoring-model", flagship_model_id="test-flagship-model",
        server=server, base_env=env, round_trip_base_env=rt_base_env, resolve_definition=_resolve,
        output_dir=tmp_path / "output", batch_review_dir=tmp_path / "review",
        max_calls_per_task=max_calls_per_task,
    )


CLASSIFICATION_JSON = json.dumps(
    {
        "regimes": ["casework", "global"], "difficulty": 2,
        "rationale": "computable, boundary-rich, ceiling-log-like",
        "expected_fact_mix": {"casework": 2, "membership": 0, "global": 1},
    }
)


def _dossier_json(worked_example_claim_2_37: str) -> str:
    dossier_md = (
        "# Object\nA ceiling-logarithm-like helper.\n\n"
        f"# Signature\nThe pinned signature is `{PINNED_SIG}`.\n\n"
        f"# Conventions\nFor b<=1 or n<=1, {DEF_NAME} b n = 0 (junk value convention).\n\n"
        "# Worked examples\n"
        f"- Claim: {worked_example_claim_2_37}\n"
        "  ```lean\n"
        f"  example : {worked_example_claim_2_37} := by decide\n"
        "  ```\n\n"
        "# Boundaries\nAt b<=1 or n<=1, junk value 0.\n\n"
        "# Not to be confused with\nNat.clog itself (the real Mathlib ceiling log).\n"
    )
    return json.dumps(
        {
            "dossier_md": dossier_md,
            "domain": {
                "constraint": "1 < b ∧ 1 < n", "variables": ["b", "n"],
                "conventions": [
                    {"point": "b<=1 or n<=1", "statement": f"{DEF_NAME} b n = 0 for b<=1 or n<=1", "note": "junk value convention"}
                ],
            },
        }
    )


GOOD_DOSSIER_JSON = _dossier_json(f"{DEF_NAME} 2 37 = 6")
BAD_EXAMPLE_DOSSIER_JSON = _dossier_json(f"{DEF_NAME} 2 37 = 5")  # false claim -> EXECUTION_FAILED

GOOD_FACTS_JSON = json.dumps(
    [
        {"id": "f1", "type": "casework", "mechanism": "decide", "statement": f"example : {DEF_NAME} 2 37 = 6 := by decide", "domain_inputs": {"b": "2", "n": "37"}},
        {"id": "f2", "type": "casework", "mechanism": "decide", "statement": f"example : {DEF_NAME} 3 10 = 3 := by decide", "domain_inputs": {"b": "3", "n": "10"}},
        # Hypothesis deliberately contains the domain constraint's own text verbatim ("1 < b ∧
        # 1 < n") -- authoring.validate._global_domain_looks_unchecked's crude "is the
        # constraint's text present in the statement" proxy would otherwise FLAG (not reject,
        # but also not accept) a correctly-quantified global fact phrased differently, exactly
        # as tests/fixtures/authoring_facts.py's own clog_global_pow entry documents. Matching
        # that phrasing here so this fact lands PROVISIONALLY_VALIDATED, not flagged-and-dropped.
        {"id": "g1", "type": "global", "mechanism": "proof", "statement": f"∀ b n : ℕ, (1 < b ∧ 1 < n) → {DEF_NAME} b n = Nat.clog b n", "anchors": ["Nat.clog_pow"]},
    ]
)

BAD_FORMAT_FACTS_JSON = json.dumps(
    [
        {"id": "f1", "type": "casework", "mechanism": "decide", "statement": f"example : {DEF_NAME} 2 37 = 6 := by decide", "domain_inputs": {"b": "2", "n": "37"}},
        {"id": "bad1", "type": "casework", "mechanism": "decide", "statement": f"{DEF_NAME} 3 10 = 3", "domain_inputs": {"b": "3", "n": "10"}},
    ]
)
FIXED_FACT_JSON = json.dumps(
    [{"id": "bad1", "type": "casework", "mechanism": "decide", "statement": f"example : {DEF_NAME} 3 10 = 3 := by decide", "domain_inputs": {"b": "3", "n": "10"}}]
)

GOOD_ROUND_TRIP_BODY = "fun b n => if b <= 1 ∨ n <= 1 then 0 else Nat.clog b n"
WRONG_ROUND_TRIP_BODY = "fun b n => 0"


# --- Happy path -----------------------------------------------------------------------------


def test_author_task_happy_path_ships_a_schema_valid_task(mathlib_env, stub_server, tmp_path):
    server, env, rt_base_env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),
            ScriptedResponse(200, success_body(GOOD_FACTS_JSON)),
            ScriptedResponse(200, success_body(GOOD_ROUND_TRIP_BODY)),
        ]
    )
    config = _config(server, env, rt_base_env, tmp_path, bedrock_server)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "SHIPPED", result.stage_records
    assert result.task_dir is not None
    assert result.round_trip_score is not None and result.round_trip_score.passed
    assert result.calls_made == 4

    validated = validate_task_dir(result.task_dir)
    assert validated.data["task_id"] == DEF_NAME
    assert len(validated.data["facts"]) == 3


# --- Unhappy path 1: dossier fails check (b) then repairs -----------------------------------


def test_dossier_fails_worked_example_then_repairs_and_ships(mathlib_env, stub_server, tmp_path):
    server, env, rt_base_env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(BAD_EXAMPLE_DOSSIER_JSON)),  # attempt 1: fails (b)
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),  # attempt 2: repairs
            ScriptedResponse(200, success_body(GOOD_FACTS_JSON)),
            ScriptedResponse(200, success_body(GOOD_ROUND_TRIP_BODY)),
        ]
    )
    config = _config(server, env, rt_base_env, tmp_path, bedrock_server)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "SHIPPED", result.stage_records
    assert len(bedrock_server.requests_received) == 5  # confirms the dossier retry actually happened
    # the retry prompt must carry the failure detail (contract row 6: "with the failure shown")
    retry_prompt = bedrock_server.requests_received[2]["messages"][0]["content"]
    assert "failed a mechanical check" in retry_prompt


def test_dossier_fails_both_attempts_rotates_at_dossier_consistency(mathlib_env, stub_server, tmp_path):
    server, env, rt_base_env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(BAD_EXAMPLE_DOSSIER_JSON)),
            ScriptedResponse(200, success_body(BAD_EXAMPLE_DOSSIER_JSON)),
        ]
    )
    config = _config(server, env, rt_base_env, tmp_path, bedrock_server)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "ROTATED"
    assert result.rotated_at_stage == "dossier_consistency"
    assert result.task_dir is None


# --- Unhappy path 2: a fact rejected for format then retried --------------------------------


def test_fact_rejected_for_format_then_retried_and_ships(mathlib_env, stub_server, tmp_path):
    server, env, rt_base_env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),
            ScriptedResponse(200, success_body(BAD_FORMAT_FACTS_JSON)),  # bad1 not command-shaped
            ScriptedResponse(200, success_body(FIXED_FACT_JSON)),  # the one retry, batched
            ScriptedResponse(200, success_body(GOOD_ROUND_TRIP_BODY)),
        ]
    )
    config = _config(server, env, rt_base_env, tmp_path, bedrock_server)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "SHIPPED", result.stage_records
    assert result.parser_rejected_facts == []  # the retry fixed it
    validated = validate_task_dir(result.task_dir)
    assert {f["id"] for f in validated.data["facts"]} == {"f1", "bad1"}


# --- Unhappy path 3: budget exhaustion mid-task ----------------------------------------------


def test_budget_exhaustion_mid_task_rotates_with_full_record(mathlib_env, stub_server, tmp_path):
    server, env, rt_base_env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),
        ]
    )
    # exactly enough budget for classification (1) + dossier (1); fact_proposal's first charge
    # must raise CallBudgetExceeded before any third HTTP call is even attempted.
    config = _config(server, env, rt_base_env, tmp_path, bedrock_server, max_calls_per_task=2)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "ROTATED"
    assert result.rotated_at_stage == "fact_proposal"
    assert "CallBudgetExceeded" in result.stage_records[-1].detail
    assert len(bedrock_server.requests_received) == 2  # never attempted a third call
    assert result.calls_made == 2


# --- Unhappy path 4: round-trip failure -> repair -> rotate ----------------------------------


def test_round_trip_failure_repairs_once_then_rotates(mathlib_env, stub_server, tmp_path):
    server, env, rt_base_env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),
            ScriptedResponse(200, success_body(GOOD_FACTS_JSON)),
            ScriptedResponse(200, success_body(WRONG_ROUND_TRIP_BODY)),  # attempt 1: wrong
            ScriptedResponse(200, success_body(WRONG_ROUND_TRIP_BODY)),  # attempt 2 (repair): still wrong
        ]
    )
    config = _config(server, env, rt_base_env, tmp_path, bedrock_server)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "ROTATED"
    assert result.rotated_at_stage == "round_trip_scoring"
    assert len(bedrock_server.requests_received) == 5  # confirms the one repair attempt happened
    assert result.task_dir is None


# --- author_batch: continue-on-rotation, batch review file -----------------------------------


def test_author_batch_never_halts_on_a_rotated_task_and_writes_review(mathlib_env, stub_server, tmp_path):
    server, env, rt_base_env = mathlib_env
    # Task 1: budget exhausted immediately (rotates). Task 2: full happy path (ships).
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),  # task 1: burns its only call
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),  # task 2
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),
            ScriptedResponse(200, success_body(GOOD_FACTS_JSON)),
            ScriptedResponse(200, success_body(GOOD_ROUND_TRIP_BODY)),
        ]
    )
    config = _config(server, env, rt_base_env, tmp_path, bedrock_server, max_calls_per_task=1)
    # Task 1 uses the low-budget config (rotates after classification); task 2 needs a fresh
    # config with real budget, so results are driven via two explicit author_task calls instead
    # of author_batch's single shared config, EXCEPT the task under test here is that
    # `author_batch` itself doesn't halt -- exercised directly below with a per-name config
    # swap is not supported by `author_batch`'s signature (one config for the whole batch), so
    # this test instead gives both tasks the SAME low budget, confirming both rotate and the
    # batch still completes and writes a review covering both.
    results, review_path = author_batch([DEF_NAME, DEF_NAME], config)

    assert len(results) == 2
    assert all(r.outcome == "ROTATED" for r in results)
    assert review_path.is_file()
    review_text = review_path.read_text()
    assert review_text.count(f"### {DEF_NAME} -- ROTATED") == 2
    assert "self-restatement declarations: none recorded" in review_text


def test_render_batch_review_is_well_formed_markdown_for_a_shipped_and_a_rotated_task(mathlib_env, stub_server, tmp_path):
    server, env, rt_base_env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),
            ScriptedResponse(200, success_body(GOOD_FACTS_JSON)),
            ScriptedResponse(200, success_body(GOOD_ROUND_TRIP_BODY)),
        ]
    )
    config = _config(server, env, rt_base_env, tmp_path, bedrock_server)
    shipped = author_task(DEF_NAME, config)
    rotated = shipped.__class__(  # a trivially-constructed rotated record, no second REPL run needed
        definition_name="other_def", outcome="ROTATED", rotated_at_stage="classification",
        stage_records=[shipped.stage_records[0]],
    )
    text = render_batch_review([shipped, rotated])
    assert text.startswith("# Authoring batch review")
    assert "Tasks: 2 (1 shipped, 1 rotated)" in text
    assert f"### {DEF_NAME} -- SHIPPED" in text
    assert "### other_def -- ROTATED (rotated at `classification`)" in text
    assert "stage-by-stage record" in text


# --- End-to-end: real Nat.clog mention-sidecar data -------------------------------------------


MENTION_NAMES_PATH = Path(__file__).resolve().parent.parent / "miner" / "output" / "mention_names.jsonl"


def _load_real_clog_mentions() -> list[MentionRecord]:
    with MENTION_NAMES_PATH.open(encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            if record["name"] == "Nat.clog":
                dm = DefinitionMentions(name=record["name"], mentions=[MentionRecord(**m) for m in record["mentions"]])
                return dm.mentions
    raise AssertionError("Nat.clog not found in miner/output/mention_names.jsonl")


@pytest.mark.skipif(not MENTION_NAMES_PATH.is_file(), reason="miner/output/mention_names.jsonl not present in this checkout")
def test_end_to_end_with_real_nat_clog_mention_sidecar_data(mathlib_env, stub_server, tmp_path):
    real_mentions = _load_real_clog_mentions()
    assert len(real_mentions) > 0  # confirms this is genuinely real, non-empty production data

    server, env, rt_base_env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),
            ScriptedResponse(200, success_body(GOOD_FACTS_JSON)),
            ScriptedResponse(200, success_body(GOOD_ROUND_TRIP_BODY)),
        ]
    )
    config = _config(server, env, rt_base_env, tmp_path, bedrock_server, mention_records=real_mentions)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "SHIPPED", result.stage_records
    validated = validate_task_dir(result.task_dir)
    assert validated.data["task_id"] == DEF_NAME

    # the mention excerpt actually sent to the model must be built from the real sidecar data
    classification_request = bedrock_server.requests_received[0]
    user_message = classification_request["messages"][0]["content"]
    real_names = {m.theorem_name for m in real_mentions}
    assert any(name in user_message for name in real_names)

    results, review_path = author_batch([], config)  # write an (empty) review to sanity-check the writer path
    assert review_path.is_file()
    assert "Tasks: 0" in review_path.read_text()
