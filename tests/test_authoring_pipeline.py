"""Tests for `authoring.pipeline.author_task`/`author_batch` -- the top-level driver chaining
every station built across the prior sessions. No real Bedrock call anywhere (the loopback
stub only, extended here with scripted responses for a full happy path and the four required
unhappy paths); real Mathlib REPL throughout, since most stages (dossier consistency, mechanical
validation, round-trip scoring, axiom baseline) are fundamentally REPL-backed and there's no
ground truth to fake.

**Uses the REAL `Nat.clog` directly**, unlike the prior session's version of this file (which
used a fresh stand-in, `pipelineClog`, to sidestep a splice-collision bug this session's
task-symbol convention (contract §4.4) now fixes at the driver level). Every statement in these
fixtures references `VTask.clog` (`authoring.task_symbol.task_symbol_for("Nat.clog")`), never
`Nat.clog` itself -- proving the fix directly, not around a synthetic substitute. No pre-splice
setup is needed in the `mathlib_env` fixture anymore either: `author_task`'s own truth-splice
stage aliases `VTask.clog := Nat.clog` internally.
"""

import json
from pathlib import Path

import pytest

from authoring.pipeline import DefinitionInput, PipelineConfig, author_batch, author_task, render_batch_review
from authoring.task_symbol import task_symbol_for
from bedrock.client import BedrockClient
from harness.repl import get_warm_environment
from harness.results import CheckStatus
from harness.task_schema import validate_task_dir
from miner.harvest import DefinitionMentions, MentionRecord
from tests.fixtures.bedrock_stub import ScriptedResponse, StubBedrockServer, success_body

DEF_NAME = "Nat.clog"
TASK_SYMBOL = task_symbol_for(DEF_NAME)  # "VTask.clog"
SIGNATURE_DICT = {"name": DEF_NAME, "type": "Nat -> Nat -> Nat", "imports": []}
PINNED_SIG = f"{TASK_SYMBOL} : Nat -> Nat -> Nat"
DEFINITION_SOURCE = "Nat.clog (b n : ℕ) : ℕ -- the real Mathlib ceiling log (context only, never written to statements)"

SYNTHETIC_MENTIONS = [
    MentionRecord(theorem_name="Nat.clog_pow", source_file="Data/Nat/Log.lean", statement_text="Nat.clog b (b ^ n) = n"),
]


@pytest.fixture(scope="module")
def mathlib_env():
    """Just the plain warm environment -- no pre-splice needed. `author_task`'s own
    truth-splice stage aliases `VTask.clog := Nat.clog` internally, off this untouched base."""
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


def _config(server, env, tmp_path, bedrock_server, *, max_calls_per_task=12, mention_records=None) -> PipelineConfig:
    client = BedrockClient(endpoint_url=bedrock_server.url, log_path=tmp_path / "log.jsonl", sleep_fn=lambda s: None)

    def _resolve(name: str) -> DefinitionInput:
        return DefinitionInput(
            name=DEF_NAME,
            signature_dict=SIGNATURE_DICT,
            definition_source=DEFINITION_SOURCE,
            docstring="the ceiling logarithm",
            mention_records=mention_records if mention_records is not None else SYNTHETIC_MENTIONS,
        )

    return PipelineConfig(
        client=client, authoring_model_id="test-authoring-model", flagship_model_id="test-flagship-model",
        server=server, base_env=env, resolve_definition=_resolve,
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
        "# Object\nThe ceiling logarithm.\n\n"
        f"# Signature\nThe pinned signature is `{PINNED_SIG}`.\n\n"
        f"# Conventions\nFor b<=1 or n<=1, {TASK_SYMBOL} b n = 0 (junk value convention).\n\n"
        "# Worked examples\n"
        f"- Claim: {worked_example_claim_2_37}\n"
        "  ```lean\n"
        f"  example : {worked_example_claim_2_37} := by decide\n"
        "  ```\n\n"
        "# Boundaries\nAt b<=1 or n<=1, junk value 0.\n\n"
        "# Not to be confused with\nThe floor logarithm.\n"
    )
    return json.dumps(
        {
            "dossier_md": dossier_md,
            "domain": {
                "constraint": "1 < b ∧ 1 < n", "variables": ["b", "n"],
                "conventions": [
                    {"point": "b<=1 or n<=1", "statement": f"{TASK_SYMBOL} b n = 0 for b<=1 or n<=1", "note": "junk value convention"}
                ],
            },
        }
    )


GOOD_DOSSIER_JSON = _dossier_json(f"{TASK_SYMBOL} 2 37 = 6")
BAD_EXAMPLE_DOSSIER_JSON = _dossier_json(f"{TASK_SYMBOL} 2 37 = 5")  # false claim -> EXECUTION_FAILED

# Real-name-leak fixture: the Claim line correctly uses the task symbol, but the fenced command
# leaks the real Mathlib name -- exactly the 2026-07-28 slice incident's shape (attempt 3's
# `Claim: VTask.clog 2 8 = 3` next to `example : Nat.clog 2 8 = 3 := by decide`). This EXECUTES
# cleanly against the true definition (real name, genuinely true there), so (b) alone would
# never catch it -- only the new real-name-leak check does.
LEAKED_NAME_DOSSIER_JSON = json.dumps(
    {
        "dossier_md": (
            "# Object\nThe ceiling logarithm.\n\n"
            f"# Signature\nThe pinned signature is `{PINNED_SIG}`.\n\n"
            f"# Conventions\nFor b<=1 or n<=1, {TASK_SYMBOL} b n = 0 (junk value convention).\n\n"
            f"# Worked examples\n- Claim: {TASK_SYMBOL} 2 37 = 6\n"
            "  ```lean\n"
            f"  example : {DEF_NAME} 2 37 = 6 := by decide\n"
            "  ```\n\n"
            "# Boundaries\nAt b<=1 or n<=1, junk value 0.\n\n"
            "# Not to be confused with\nThe floor logarithm.\n"
        ),
        "domain": {
            "constraint": "1 < b ∧ 1 < n", "variables": ["b", "n"],
            "conventions": [
                {"point": "b<=1 or n<=1", "statement": f"{TASK_SYMBOL} b n = 0 for b<=1 or n<=1", "note": "junk value convention"}
            ],
        },
    }
)

GOOD_FACTS_JSON = json.dumps(
    [
        {"id": "f1", "type": "casework", "mechanism": "decide", "statement": f"example : {TASK_SYMBOL} 2 37 = 6 := by decide", "domain_inputs": {"b": "2", "n": "37"}},
        {"id": "f2", "type": "casework", "mechanism": "decide", "statement": f"example : {TASK_SYMBOL} 3 10 = 3 := by decide", "domain_inputs": {"b": "3", "n": "10"}},
        # Self-contained (never compares to the real name -- that would trip the raw-name-leak
        # check); contains the domain constraint's own text verbatim so
        # authoring.validate._global_domain_looks_unchecked doesn't flag it.
        {"id": "g1", "type": "global", "mechanism": "proof", "statement": f"∀ b n : ℕ, (1 < b ∧ 1 < n) → {TASK_SYMBOL} b n ≥ 0", "anchors": ["Nat.clog_pow"], "self_restatement": True},
    ]
)

BAD_FORMAT_FACTS_JSON = json.dumps(
    [
        {"id": "f1", "type": "casework", "mechanism": "decide", "statement": f"example : {TASK_SYMBOL} 2 37 = 6 := by decide", "domain_inputs": {"b": "2", "n": "37"}},
        {"id": "bad1", "type": "casework", "mechanism": "decide", "statement": f"{TASK_SYMBOL} 3 10 = 3", "domain_inputs": {"b": "3", "n": "10"}},
    ]
)
FIXED_FACT_JSON = json.dumps(
    [{"id": "bad1", "type": "casework", "mechanism": "decide", "statement": f"example : {TASK_SYMBOL} 3 10 = 3 := by decide", "domain_inputs": {"b": "3", "n": "10"}}]
)

# The candidate body is spliced as `def VTask.clog : T := <body>` -- unlike fact statements,
# NOTHING forbids a candidate body from referencing the real name internally (only
# authoring.parse's fact-statement check does that, and candidate bodies never go through it).
# Deliberately an ETA-EXPANDED lambda, not a bare point-free alias (`"Nat.clog"`) -- confirmed
# empirically that a bare alias makes Lean's declaration report for the splice list the real
# `Nat.clog` alongside `VTask.clog`, which trips harness.admissibility's shadowing check as a
# false positive ("candidate declared name(s) beyond the pinned 'VTask.clog': ['Nat.clog']").
# The eta-expanded form does not trigger this.
GOOD_ROUND_TRIP_BODY = "fun b n => Nat.clog b n"
WRONG_ROUND_TRIP_BODY = "fun b n => 0"

# A COMPILE failure whose error is purely a termination-checker complaint -- empirically
# confirmed (2026-07-28 probe against the real warm Mathlib env) to produce a
# "failed to infer structural recursion" / "Could not find a decreasing measure" error, matching
# `authoring.pipeline._TERMINATION_ERROR_MARKERS`. Ignores `b`; only `n` matters for the
# probe's fuel/accumulator shape, adapted here to the two-argument `Nat -> Nat -> Nat` signature.
TERMINATION_FAILURE_ROUND_TRIP_BODY = (
    "fun b n =>\n"
    "  let rec go (k acc : Nat) : Nat :=\n"
    "    if acc >= n then k else go (k + 1) (acc * 2)\n"
    "  go 0 1"
)

# A COMPILE failure that is NOT termination-related -- an unknown identifier, so the error text
# contains none of `_TERMINATION_ERROR_MARKERS`. Used for the mixed-failure test (d).
UNKNOWN_IDENTIFIER_ROUND_TRIP_BODY = "fun b n => totallyUndefinedIdentifierXYZ b n"


# --- Happy path -----------------------------------------------------------------------------


def test_author_task_happy_path_ships_a_schema_valid_task(mathlib_env, stub_server, tmp_path):
    server, env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),
            ScriptedResponse(200, success_body(GOOD_FACTS_JSON)),
            ScriptedResponse(200, success_body(GOOD_ROUND_TRIP_BODY)),
        ]
    )
    config = _config(server, env, tmp_path, bedrock_server)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "SHIPPED", result.stage_records
    assert result.task_dir is not None
    assert result.round_trip_score is not None and result.round_trip_score.passed
    assert result.calls_made == 4
    assert result.self_restatement_fact_ids == ["g1"]

    validated = validate_task_dir(result.task_dir)
    assert validated.data["task_id"] == DEF_NAME
    assert validated.data["task_symbol"] == TASK_SYMBOL
    assert validated.data["signature"]["name"] == TASK_SYMBOL
    assert len(validated.data["facts"]) == 3
    # every shipped statement uses the task symbol, never the real name
    for fact in validated.data["facts"]:
        assert DEF_NAME not in fact["statement"]
        assert TASK_SYMBOL in fact["statement"]


# --- Unhappy path 1: dossier fails check (b) then repairs -----------------------------------


def test_dossier_fails_worked_example_then_repairs_and_ships(mathlib_env, stub_server, tmp_path):
    server, env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(BAD_EXAMPLE_DOSSIER_JSON)),  # attempt 1: fails (b)
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),  # attempt 2: repairs
            ScriptedResponse(200, success_body(GOOD_FACTS_JSON)),
            ScriptedResponse(200, success_body(GOOD_ROUND_TRIP_BODY)),
        ]
    )
    config = _config(server, env, tmp_path, bedrock_server)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "SHIPPED", result.stage_records
    assert len(bedrock_server.requests_received) == 5  # confirms the dossier retry actually happened
    # the retry prompt must carry the failure detail (contract row 6: "with the failure shown")
    retry_prompt = bedrock_server.requests_received[2]["messages"][0]["content"]
    assert "failed a mechanical check" in retry_prompt


def test_dossier_fails_both_attempts_rotates_at_dossier_consistency(mathlib_env, stub_server, tmp_path):
    server, env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(BAD_EXAMPLE_DOSSIER_JSON)),
            ScriptedResponse(200, success_body(BAD_EXAMPLE_DOSSIER_JSON)),
        ]
    )
    config = _config(server, env, tmp_path, bedrock_server)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "ROTATED"
    assert result.rotated_at_stage == "dossier_consistency"
    assert result.task_dir is None


def test_dossier_real_name_leak_feeds_the_repair_cycle_with_the_violation_quoted(mathlib_env, stub_server, tmp_path):
    """The pipeline-level wiring for the new check (§3.4(d)): a leaking dossier response must
    trigger the SAME repair cycle a worked-example failure does, with the specific violation
    (not a generic message) appended to the retry prompt -- and if the repair also leaks,
    rotate at `dossier_consistency`, same stage label as any other consistency failure."""
    server, env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(LEAKED_NAME_DOSSIER_JSON)),  # attempt 1: leaks
            ScriptedResponse(200, success_body(LEAKED_NAME_DOSSIER_JSON)),  # attempt 2: leaks again
        ]
    )
    config = _config(server, env, tmp_path, bedrock_server)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "ROTATED"
    assert result.rotated_at_stage == "dossier_consistency"
    retry_prompt = bedrock_server.requests_received[2]["messages"][0]["content"]
    assert "failed a mechanical check" in retry_prompt
    assert DEF_NAME in retry_prompt  # the specific leaked name is quoted, not a generic message


def test_dossier_real_name_leak_then_clean_repair_ships(mathlib_env, stub_server, tmp_path):
    """The other direction at the pipeline level: a leak on attempt 1, a clean (task-symbol-
    only) dossier on the repair attempt, ships normally."""
    server, env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(LEAKED_NAME_DOSSIER_JSON)),  # attempt 1: leaks
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),  # attempt 2: clean
            ScriptedResponse(200, success_body(GOOD_FACTS_JSON)),
            ScriptedResponse(200, success_body(GOOD_ROUND_TRIP_BODY)),
        ]
    )
    config = _config(server, env, tmp_path, bedrock_server)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "SHIPPED", result.stage_records


# --- Unhappy path 2: a fact rejected for format then retried --------------------------------


def test_fact_rejected_for_format_then_retried_and_ships(mathlib_env, stub_server, tmp_path):
    server, env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),
            ScriptedResponse(200, success_body(BAD_FORMAT_FACTS_JSON)),  # bad1 not command-shaped
            ScriptedResponse(200, success_body(FIXED_FACT_JSON)),  # the one retry, batched
            ScriptedResponse(200, success_body(GOOD_ROUND_TRIP_BODY)),
        ]
    )
    config = _config(server, env, tmp_path, bedrock_server)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "SHIPPED", result.stage_records
    assert result.parser_rejected_facts == []  # the retry fixed it
    validated = validate_task_dir(result.task_dir)
    assert {f["id"] for f in validated.data["facts"]} == {"f1", "bad1"}


# --- Unhappy path 2b: a fact rejected for leaking the real name (task-symbol convention) ----


def test_fact_rejected_for_raw_name_leak_is_dropped(mathlib_env, stub_server, tmp_path):
    leaked = {
        "id": "leak", "type": "casework", "mechanism": "decide",
        "statement": f"example : {DEF_NAME} 2 37 = 6 := by decide", "domain_inputs": {"b": "2", "n": "37"},
    }
    still_leaked = dict(leaked)  # unfixed on retry
    server, env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),
            ScriptedResponse(200, success_body(json.dumps([leaked]))),
            ScriptedResponse(200, success_body(json.dumps([still_leaked]))),
        ]
    )
    config = _config(server, env, tmp_path, bedrock_server)
    result = author_task(DEF_NAME, config)

    # no facts survive at all in this suite (only the leaking one was proposed) -> rotates
    assert result.outcome == "ROTATED"
    assert result.rotated_at_stage == "mechanical_validation"
    assert len(result.parser_rejected_facts) == 1
    assert result.parser_rejected_facts[0].reason_code == "MALFORMED_RAW_NAME_IN_STATEMENT"


# --- Unhappy path 3: budget exhaustion mid-task ----------------------------------------------


def test_budget_exhaustion_mid_task_rotates_with_full_record(mathlib_env, stub_server, tmp_path):
    server, env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),
        ]
    )
    # exactly enough budget for classification (1) + dossier (1); fact_proposal's first charge
    # must raise CallBudgetExceeded before any third HTTP call is even attempted.
    config = _config(server, env, tmp_path, bedrock_server, max_calls_per_task=2)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "ROTATED"
    assert result.rotated_at_stage == "fact_proposal"
    assert "CallBudgetExceeded" in result.stage_records[-1].detail
    assert len(bedrock_server.requests_received) == 2  # never attempted a third call
    assert result.calls_made == 2


# --- Unexpected-error rotation must still report real spend ----------------------------------


def test_unexpected_error_rotation_still_reports_calls_made_and_tokens(mathlib_env, stub_server, tmp_path, monkeypatch):
    """A crash unrelated to malformed LLM output (some other bug entirely) still lands in
    `author_task`'s outer catch-all -- but the classification call before it was real, billed,
    and logged, and the resulting `TaskResult` must say so. Before this session's fix, the
    outer `except` branch always returned `calls_made=0, input_tokens=0, output_tokens=0`
    regardless of what had actually happened -- confirmed for real on 2026-07-28, where a
    genuine classification call spent 1773+257 tokens and then a parsing bug (since fixed)
    crashed before that spend was ever recorded on the `TaskResult`."""
    server, env = mathlib_env
    bedrock_server = stub_server([ScriptedResponse(200, success_body(CLASSIFICATION_JSON))])
    config = _config(server, env, tmp_path, bedrock_server)

    def _boom(*args, **kwargs):
        raise RuntimeError("injected failure, unrelated to Bedrock or parsing")

    monkeypatch.setattr("authoring.pipeline.run_dossier_call", _boom)

    result = author_task(DEF_NAME, config)

    assert result.outcome == "ROTATED"
    assert result.rotated_at_stage == "unexpected_error"
    assert "injected failure" in result.stage_records[-1].detail
    # the classification call really happened (one HTTP request, one logged call) -- the
    # TaskResult must reflect that, not report a crash-shaped zero.
    assert len(bedrock_server.requests_received) == 1
    assert result.calls_made == 1
    assert result.input_tokens > 0
    assert result.output_tokens > 0


# --- Unhappy path 4: round-trip -- feedback-carrying retries, no-retry-on-fact-failure, --------
# --- ship-with-flag on pure termination failure (2026-07-28 policy) ---------------------------


def test_round_trip_fact_failure_is_immediately_terminal(mathlib_env, stub_server, tmp_path):
    """(e) A compiled-but-fact-failing attempt gets ZERO retries: the round-trip stage ends
    after exactly one round-trip call, and the task rotates for review rather than regenerating.
    `WRONG_ROUND_TRIP_BODY` ("fun b n => 0") compiles cleanly -- it's a fact failure, not a
    compile failure."""
    server, env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),
            ScriptedResponse(200, success_body(GOOD_FACTS_JSON)),
            ScriptedResponse(200, success_body(WRONG_ROUND_TRIP_BODY)),  # compiles, fails facts
        ]
    )
    config = _config(server, env, tmp_path, bedrock_server)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "ROTATED"
    assert result.rotated_at_stage == "round_trip_scoring"
    assert "no retry, per policy" in result.stage_records[-1].detail
    assert len(bedrock_server.requests_received) == 4  # zero further round-trip calls beyond the one
    assert result.task_dir is None
    assert result.round_trip_flag is None
    assert result.self_restatement_fact_ids == ["g1"]  # preserved through to the rotation record


def test_round_trip_compile_failure_retries_with_feedback_and_succeeds_on_attempt_2(mathlib_env, stub_server, tmp_path):
    """(b) part 1: a termination compile failure on attempt 1, success on attempt 2. The retry
    request must carry the attempt-1 body and its compiler error verbatim."""
    server, env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),
            ScriptedResponse(200, success_body(GOOD_FACTS_JSON)),
            ScriptedResponse(200, success_body(TERMINATION_FAILURE_ROUND_TRIP_BODY)),  # attempt 1: fails to compile
            ScriptedResponse(200, success_body(GOOD_ROUND_TRIP_BODY)),  # attempt 2: succeeds
        ]
    )
    config = _config(server, env, tmp_path, bedrock_server)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "SHIPPED", result.stage_records
    assert result.round_trip_score is not None and result.round_trip_score.passed
    assert result.round_trip_flag is None
    assert len(bedrock_server.requests_received) == 5
    retry_prompt = bedrock_server.requests_received[4]["messages"][0]["content"]
    assert "Your previous attempt is below" in retry_prompt
    assert TERMINATION_FAILURE_ROUND_TRIP_BODY in retry_prompt
    assert "termination" in retry_prompt.lower()


def test_round_trip_compile_failure_retries_with_feedback_and_succeeds_on_attempt_4(mathlib_env, stub_server, tmp_path):
    """(b) part 2: three straight termination compile failures, success on the last permitted
    (4th) attempt -- confirms the cap is inclusive, not off-by-one."""
    server, env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),
            ScriptedResponse(200, success_body(GOOD_FACTS_JSON)),
            ScriptedResponse(200, success_body(TERMINATION_FAILURE_ROUND_TRIP_BODY)),  # attempt 1
            ScriptedResponse(200, success_body(TERMINATION_FAILURE_ROUND_TRIP_BODY)),  # attempt 2
            ScriptedResponse(200, success_body(TERMINATION_FAILURE_ROUND_TRIP_BODY)),  # attempt 3
            ScriptedResponse(200, success_body(GOOD_ROUND_TRIP_BODY)),  # attempt 4: succeeds
        ]
    )
    config = _config(server, env, tmp_path, bedrock_server)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "SHIPPED", result.stage_records
    assert result.round_trip_score is not None and result.round_trip_score.passed
    assert result.round_trip_flag is None
    assert len(bedrock_server.requests_received) == 7  # 3 non-rt calls + 4 round-trip attempts


def test_round_trip_four_pure_termination_failures_ships_with_flag(mathlib_env, stub_server, tmp_path):
    """(c) All 4 attempts fail to compile, every one purely on the termination checker: the task
    SHIPS (not rotated), with `round_trip_flag` set on the TaskResult and surfaced in the batch
    review."""
    server, env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),
            ScriptedResponse(200, success_body(GOOD_FACTS_JSON)),
            ScriptedResponse(200, success_body(TERMINATION_FAILURE_ROUND_TRIP_BODY)),  # attempt 1
            ScriptedResponse(200, success_body(TERMINATION_FAILURE_ROUND_TRIP_BODY)),  # attempt 2
            ScriptedResponse(200, success_body(TERMINATION_FAILURE_ROUND_TRIP_BODY)),  # attempt 3
            ScriptedResponse(200, success_body(TERMINATION_FAILURE_ROUND_TRIP_BODY)),  # attempt 4
        ]
    )
    config = _config(server, env, tmp_path, bedrock_server)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "SHIPPED", result.stage_records
    assert result.round_trip_flag == "UNVERIFIED_TERMINATION_ONLY"
    assert result.task_dir is not None
    assert len(bedrock_server.requests_received) == 7  # 3 non-rt calls + 4 round-trip attempts

    review_text = render_batch_review([result])
    assert "UNVERIFIED_TERMINATION_ONLY" in review_text


def test_round_trip_mixed_compile_failures_rotates_not_flagged(mathlib_env, stub_server, tmp_path):
    """(d) 4 compile failures, but NOT all termination-only (one is an unrelated unknown-
    identifier error) -- ship-with-flag does not apply; the task rotates as before."""
    server, env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),
            ScriptedResponse(200, success_body(GOOD_FACTS_JSON)),
            ScriptedResponse(200, success_body(TERMINATION_FAILURE_ROUND_TRIP_BODY)),  # attempt 1: termination
            ScriptedResponse(200, success_body(TERMINATION_FAILURE_ROUND_TRIP_BODY)),  # attempt 2: termination
            ScriptedResponse(200, success_body(TERMINATION_FAILURE_ROUND_TRIP_BODY)),  # attempt 3: termination
            ScriptedResponse(200, success_body(UNKNOWN_IDENTIFIER_ROUND_TRIP_BODY)),  # attempt 4: NOT termination
        ]
    )
    config = _config(server, env, tmp_path, bedrock_server)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "ROTATED"
    assert result.rotated_at_stage == "round_trip_scoring"
    assert result.round_trip_flag is None
    assert result.task_dir is None
    assert len(bedrock_server.requests_received) == 7  # 3 non-rt calls + 4 round-trip attempts


def test_round_trip_budget_exhaustion_mid_retry_loop_rotates_cleanly(mathlib_env, stub_server, tmp_path):
    """(f) budget interaction: with only enough budget for 2 of the 4 possible round-trip
    attempts, the loop must stop and rotate at `round_trip_generation` on `CallBudgetExceeded`,
    never exceeding the configured call budget."""
    server, env = mathlib_env
    # classification + dossier + facts = 3 calls, then 2 round-trip attempts = 5 total budget.
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),
            ScriptedResponse(200, success_body(GOOD_FACTS_JSON)),
            ScriptedResponse(200, success_body(TERMINATION_FAILURE_ROUND_TRIP_BODY)),  # attempt 1
            ScriptedResponse(200, success_body(TERMINATION_FAILURE_ROUND_TRIP_BODY)),  # attempt 2
        ]
    )
    config = _config(server, env, tmp_path, bedrock_server, max_calls_per_task=5)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "ROTATED"
    assert result.rotated_at_stage == "round_trip_generation"
    assert "CallBudgetExceeded" in result.stage_records[-1].detail
    assert result.calls_made == 5
    assert len(bedrock_server.requests_received) == 5  # never exceeded the configured budget


# --- Unhappy path 5: emit-stage schema rotation preserves a real round-trip score (2026-07-28) -


def test_emit_stage_rotation_preserves_round_trip_score(mathlib_env, stub_server, tmp_path):
    """Regression for the real 2026-07-28 clog run: a rotation discovered at `emit` (a stage
    that runs AFTER round-trip scoring) must not discard a round trip that already fully
    succeeded. The vehicle here is a duplicate fact id spanning the fact-proposal batch and its
    row-3 retry -- `authoring.parse.parse_facts` only dedupes ids WITHIN one response, so this
    still reaches `emit_task`'s schema validation today (a known, separate gap, not the one
    this fix addresses) -- exactly what's needed to exercise the `except TaskSchemaError`
    branch without depending on the domain_inputs gap this session's fix already closed."""
    server, env = mathlib_env
    dup_a = {"id": "dup_id", "type": "casework", "mechanism": "decide", "statement": f"example : {TASK_SYMBOL} 2 37 = 6 := by decide", "domain_inputs": {"b": "2", "n": "37"}}
    bad_format = {"id": "bad_fmt", "type": "casework", "mechanism": "decide", "statement": f"{TASK_SYMBOL} 3 10 = 3", "domain_inputs": {"b": "3", "n": "10"}}  # triggers the row-3 retry
    dup_b = {"id": "dup_id", "type": "casework", "mechanism": "decide", "statement": f"example : {TASK_SYMBOL} 3 10 = 3 := by decide", "domain_inputs": {"b": "3", "n": "10"}}  # retry response reuses "dup_id"

    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),
            ScriptedResponse(200, success_body(json.dumps([dup_a, bad_format]))),
            ScriptedResponse(200, success_body(json.dumps([dup_b]))),
            ScriptedResponse(200, success_body(GOOD_ROUND_TRIP_BODY)),
        ]
    )
    config = _config(server, env, tmp_path, bedrock_server)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "ROTATED"
    assert result.rotated_at_stage == "emit"
    assert "duplicate fact id" in result.stage_records[-1].detail
    # the fix under test: round-trip already succeeded before the emit-stage rotation, and that
    # must survive into the rotation record, not come back None.
    assert result.round_trip_score is not None
    assert result.round_trip_score.passed is True
    assert result.round_trip_flag is None


# --- author_batch: continue-on-rotation, batch review file -----------------------------------


def test_author_batch_never_halts_on_a_rotated_task_and_writes_review(mathlib_env, stub_server, tmp_path):
    server, env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),  # task 1: burns its only call
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),  # task 2: burns its only call
        ]
    )
    config = _config(server, env, tmp_path, bedrock_server, max_calls_per_task=1)
    results, review_path = author_batch([DEF_NAME, DEF_NAME], config)

    assert len(results) == 2
    assert all(r.outcome == "ROTATED" for r in results)
    assert review_path.is_file()
    review_text = review_path.read_text()
    assert review_text.count(f"### {DEF_NAME} -- ROTATED") == 2
    assert "self-restatement declarations: none" in review_text


def test_render_batch_review_is_well_formed_markdown_for_a_shipped_and_a_rotated_task(mathlib_env, stub_server, tmp_path):
    server, env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),
            ScriptedResponse(200, success_body(GOOD_FACTS_JSON)),
            ScriptedResponse(200, success_body(GOOD_ROUND_TRIP_BODY)),
        ]
    )
    config = _config(server, env, tmp_path, bedrock_server)
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
    assert "self-restatement declarations (§4.2" in text  # shipped task's g1 declaration
    assert "- `g1`" in text


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
    """The end-to-end proof that the task-symbol convention resolves the driver session's
    collision finding: the REAL `Nat.clog`, spliced (truth-side and round-trip) under
    `VTask.clog`, with genuinely real mention-sidecar data -- no stand-in anywhere."""
    real_mentions = _load_real_clog_mentions()
    assert len(real_mentions) > 0  # confirms this is genuinely real, non-empty production data

    server, env = mathlib_env
    bedrock_server = stub_server(
        [
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
            ScriptedResponse(200, success_body(GOOD_DOSSIER_JSON)),
            ScriptedResponse(200, success_body(GOOD_FACTS_JSON)),
            ScriptedResponse(200, success_body(GOOD_ROUND_TRIP_BODY)),
        ]
    )
    config = _config(server, env, tmp_path, bedrock_server, mention_records=real_mentions)
    result = author_task(DEF_NAME, config)

    assert result.outcome == "SHIPPED", result.stage_records
    validated = validate_task_dir(result.task_dir)
    assert validated.data["task_id"] == DEF_NAME
    assert validated.data["task_symbol"] == "VTask.clog"

    # the mention excerpt actually sent to the model must be built from the real sidecar data
    classification_request = bedrock_server.requests_received[0]
    user_message = classification_request["messages"][0]["content"]
    real_names = {m.theorem_name for m in real_mentions}
    assert any(name in user_message for name in real_names)

    results, review_path = author_batch([], config)  # write an (empty) review to sanity-check the writer path
    assert review_path.is_file()
    assert "Tasks: 0" in review_path.read_text()
