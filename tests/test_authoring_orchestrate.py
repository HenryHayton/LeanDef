"""Tests for `authoring.orchestrate`'s fast, deterministic paths: the §6 retry table's rows
1-3 (JSON/schema-shape retry, per-fact statement-format retry), the call budget, round-trip
generation, and the generic repair-cycle primitive (rows 6-7's shared shape). All against the
loopback Bedrock stub (`tests/fixtures/bedrock_stub.py`) -- no real Bedrock call, no REPL.

Rows 4-5 (mechanical adjudication) need a real Mathlib environment and are covered separately
in `tests/test_authoring_orchestrate_adjudication.py`, which also contains the one test that
deliberately triggers a REPL timeout -- kept out of this file for the same reason
`test_authoring_validate_hardening.py` is its own module (a timeout-induced server restart
must not poison other tests sharing a warm environment).
"""

import json

import pytest

from authoring.orchestrate import (
    AuthoringCallFailed,
    CallBudget,
    CallBudgetExceeded,
    RepairCycleOutcome,
    run_classification_call,
    run_dossier_call,
    run_fact_proposal_call,
    run_round_trip_generation_call,
    with_one_repair_cycle,
)
from bedrock.client import BedrockClient
from tests.fixtures.bedrock_stub import ScriptedResponse, StubBedrockServer, success_body


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


def _client(server, tmp_path) -> BedrockClient:
    return BedrockClient(endpoint_url=server.url, log_path=tmp_path / "log.jsonl", sleep_fn=lambda s: None)


CLASSIFICATION_JSON = json.dumps(
    {
        "regimes": ["casework"],
        "difficulty": 2,
        "rationale": "computable, boundary-rich",
        "expected_fact_mix": {"casework": 5, "membership": 0, "global": 1},
    }
)

DOSSIER_JSON = json.dumps(
    {
        "dossier_md": "# Object\n...",
        "domain": {
            "constraint": "True",
            "variables": [],
            "conventions": [{"point": None, "statement": None, "note": "NONE_DECLARED: none"}],
        },
    }
)


# --- Call 1/2: rows 1-2 (shared _call_llm_json path) --------------------------------------


def test_classification_call_succeeds_first_try(stub_server, tmp_path):
    server = stub_server([ScriptedResponse(200, success_body(CLASSIFICATION_JSON))])
    client = _client(server, tmp_path)
    result = run_classification_call(
        client, "test-model",
        pinned_signature="Nat.clog : Nat -> Nat -> Nat", definition_source="def clog := ...",
        docstring="ceiling log", mention_sidecar_excerpt="(none)",
    )
    assert result.regimes == ["casework"]
    assert len(server.requests_received) == 1


def test_classification_call_retries_once_on_malformed_json_then_succeeds(stub_server, tmp_path):
    server = stub_server(
        [
            ScriptedResponse(200, success_body("this is not json{{{")),
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
        ]
    )
    client = _client(server, tmp_path)
    result = run_classification_call(
        client, "test-model",
        pinned_signature="x", definition_source="y", docstring="z", mention_sidecar_excerpt="(none)",
    )
    assert result.difficulty == 2
    assert len(server.requests_received) == 2
    # the retry prompt must actually carry feedback about what went wrong
    retry_message = server.requests_received[1]["messages"][0]["content"]
    assert "could not be used" in retry_message


def test_classification_call_terminal_after_retry_also_fails(stub_server, tmp_path):
    server = stub_server(
        [
            ScriptedResponse(200, success_body("not json")),
            ScriptedResponse(200, success_body("still not json")),
        ]
    )
    client = _client(server, tmp_path)
    with pytest.raises(AuthoringCallFailed):
        run_classification_call(
            client, "test-model",
            pinned_signature="x", definition_source="y", docstring="z", mention_sidecar_excerpt="(none)",
        )
    assert len(server.requests_received) == 2  # exactly one retry, never a third attempt


def test_classification_call_retries_once_on_malformed_shape_then_succeeds(stub_server, tmp_path):
    """Reproduces the real 2026-07-28 incident end to end: a well-formed-JSON-but-wrong-shape
    response (`regimes` as a list of objects, not strings -- exactly what a real Bedrock call
    sent) must trigger the same one-retry-with-feedback path as malformed JSON, not crash the
    whole call. Before this session's hardening, `parse_classification` raised a raw
    `TypeError` here, which `_call_llm_json`'s `except ParseError` doesn't catch -- the retry
    never fired at all."""
    malformed_shape = json.dumps({
        "regimes": [
            {"type": "casework", "description": "...", "estimated_count": 10},
            {"type": "membership", "description": "...", "estimated_count": 15},
        ]
    })
    server = stub_server(
        [
            ScriptedResponse(200, success_body(malformed_shape)),
            ScriptedResponse(200, success_body(CLASSIFICATION_JSON)),
        ]
    )
    client = _client(server, tmp_path)
    result = run_classification_call(
        client, "test-model",
        pinned_signature="x", definition_source="y", docstring="z", mention_sidecar_excerpt="(none)",
    )
    assert result.difficulty == 2
    assert len(server.requests_received) == 2  # the retry fired -- a second call was actually made
    retry_message = server.requests_received[1]["messages"][0]["content"]
    assert "could not be used" in retry_message
    assert "flat array of strings" in retry_message  # the specific, actionable feedback reached the retry prompt


def test_dossier_call_succeeds_and_carries_domain(stub_server, tmp_path):
    server = stub_server([ScriptedResponse(200, success_body(DOSSIER_JSON))])
    client = _client(server, tmp_path)
    result = run_dossier_call(
        client, "test-model",
        pinned_signature="x", definition_source="y", docstring="z",
        mention_sidecar_excerpt="(none)", classification="casework, difficulty 2",
    )
    assert result.dossier_md == "# Object\n..."
    assert result.domain.constraint == "True"


# --- Call 3: rows 1-2 (whole array) + row 3 (per-fact, batched retry) ---------------------


def _fact_json(fact_id: str, statement: str = "example : Nat.clog 2 37 = 6 := by decide") -> dict:
    return {"id": fact_id, "type": "casework", "mechanism": "decide", "statement": statement, "domain_inputs": {"b": "2", "n": "37"}}


def test_fact_proposal_all_clean_no_extra_call(stub_server, tmp_path):
    facts_json = json.dumps([_fact_json("f1"), _fact_json("f2")])
    server = stub_server([ScriptedResponse(200, success_body(facts_json))])
    client = _client(server, tmp_path)
    result = run_fact_proposal_call(
        client, "test-model",
        pinned_signature="Nat.clog : Nat -> Nat -> Nat", dossier_md="# Object\n...",
        mention_sidecar_excerpt="(none)", classification="casework",
    )
    assert [f.id for f in result.facts] == ["f1", "f2"]
    assert result.dropped == []
    assert len(server.requests_received) == 1  # no format violations -> no follow-up call


def test_fact_proposal_retries_and_merges_corrected_fact(stub_server, tmp_path):
    good = _fact_json("good")
    bad = _fact_json("bad", statement="Nat.clog 2 37 = 6")  # not command-shaped
    first_response = json.dumps([good, bad])
    fixed = _fact_json("bad", statement="example : Nat.clog 2 37 = 6 := by decide")
    retry_response = json.dumps([fixed])

    server = stub_server(
        [ScriptedResponse(200, success_body(first_response)), ScriptedResponse(200, success_body(retry_response))]
    )
    client = _client(server, tmp_path)
    result = run_fact_proposal_call(
        client, "test-model",
        pinned_signature="x", dossier_md="d", mention_sidecar_excerpt="(none)", classification="c",
    )
    assert sorted(f.id for f in result.facts) == ["bad", "good"]
    assert result.dropped == []
    assert len(server.requests_received) == 2
    retry_message = server.requests_received[1]["messages"][0]["content"]
    assert "bad" in retry_message and "statement-format" in retry_message


def test_fact_proposal_drops_fact_still_bad_after_the_one_retry(stub_server, tmp_path):
    bad = _fact_json("bad", statement="Nat.clog 2 37 = 6")
    first_response = json.dumps([bad])
    still_bad = _fact_json("bad", statement="still not command shaped")
    retry_response = json.dumps([still_bad])

    server = stub_server(
        [ScriptedResponse(200, success_body(first_response)), ScriptedResponse(200, success_body(retry_response))]
    )
    client = _client(server, tmp_path)
    result = run_fact_proposal_call(
        client, "test-model",
        pinned_signature="x", dossier_md="d", mention_sidecar_excerpt="(none)", classification="c",
    )
    assert result.facts == []
    assert len(result.dropped) == 1
    assert result.dropped[0].fragment["id"] == "bad"
    assert len(server.requests_received) == 2  # never a third call


def test_fact_proposal_whole_call_json_failure_gets_row_1_retry(stub_server, tmp_path):
    good_response = json.dumps([_fact_json("f1")])
    server = stub_server(
        [ScriptedResponse(200, success_body("not an array at all")), ScriptedResponse(200, success_body(good_response))]
    )
    client = _client(server, tmp_path)
    result = run_fact_proposal_call(
        client, "test-model",
        pinned_signature="x", dossier_md="d", mention_sidecar_excerpt="(none)", classification="c",
    )
    assert [f.id for f in result.facts] == ["f1"]
    assert len(server.requests_received) == 2


def test_fact_proposal_raw_name_leak_dropped_when_task_symbol_context_given(stub_server, tmp_path):
    leaked = _fact_json("leak", statement="example : Nat.clog 2 37 = 6 := by decide")
    first_response = json.dumps([leaked])
    still_leaked = _fact_json("leak", statement="example : Nat.clog 2 37 = 6 := by decide")  # unfixed on retry
    retry_response = json.dumps([still_leaked])

    server = stub_server(
        [ScriptedResponse(200, success_body(first_response)), ScriptedResponse(200, success_body(retry_response))]
    )
    client = _client(server, tmp_path)
    result = run_fact_proposal_call(
        client, "test-model",
        pinned_signature="VTask.clog : Nat -> Nat -> Nat", dossier_md="d", mention_sidecar_excerpt="(none)",
        classification="c", task_symbol="VTask.clog", forbidden_name="Nat.clog",
    )
    assert result.facts == []
    assert len(result.dropped) == 1
    assert result.dropped[0].reason_code == "MALFORMED_RAW_NAME_IN_STATEMENT"
    assert len(server.requests_received) == 2  # the one row-3 retry, then terminal for that fact


# --- Call budget --------------------------------------------------------------------------


def test_call_budget_charges_and_raises_when_exceeded():
    budget = CallBudget(max_calls=2)
    budget.charge()
    budget.charge()
    with pytest.raises(CallBudgetExceeded):
        budget.charge()


def test_classification_call_respects_exhausted_budget_before_sending(stub_server, tmp_path):
    server = stub_server([ScriptedResponse(200, success_body(CLASSIFICATION_JSON))])
    client = _client(server, tmp_path)
    budget = CallBudget(max_calls=0)
    with pytest.raises(CallBudgetExceeded):
        run_classification_call(
            client, "test-model",
            pinned_signature="x", definition_source="y", docstring="z",
            mention_sidecar_excerpt="(none)", budget=budget,
        )
    assert len(server.requests_received) == 0  # budget checked before the call, not after


def test_classification_call_charges_two_on_a_retry(stub_server, tmp_path):
    server = stub_server(
        [ScriptedResponse(200, success_body("bad json")), ScriptedResponse(200, success_body(CLASSIFICATION_JSON))]
    )
    client = _client(server, tmp_path)
    budget = CallBudget(max_calls=5)
    run_classification_call(
        client, "test-model",
        pinned_signature="x", definition_source="y", docstring="z",
        mention_sidecar_excerpt="(none)", budget=budget,
    )
    assert budget.calls_made == 2


# --- Call 4: round-trip generation ---------------------------------------------------------


def test_round_trip_generation_returns_raw_text(stub_server, tmp_path):
    server = stub_server([ScriptedResponse(200, success_body("fun n => n + n"))])
    client = _client(server, tmp_path)
    body = run_round_trip_generation_call(client, "test-model", pinned_signature="rtDouble : Nat -> Nat", dossier_md="# Object\n...")
    assert body == "fun n => n + n"


def test_round_trip_generation_strips_markdown_fence():
    from authoring.orchestrate import _strip_markdown_fence

    assert _strip_markdown_fence("```lean\nfun n => n + n\n```") == "fun n => n + n"
    assert _strip_markdown_fence("```\nfun n => n + n\n```") == "fun n => n + n"
    assert _strip_markdown_fence("fun n => n + n") == "fun n => n + n"


def test_round_trip_generation_call_never_receives_definition_source_or_facts(stub_server, tmp_path):
    """Information-hygiene guarantee (contract §5): the function's own signature has no
    parameter through which a definition source or fact suite could leak."""
    import inspect

    sig = inspect.signature(run_round_trip_generation_call)
    assert set(sig.parameters) == {"client", "model_id", "pinned_signature", "dossier_md", "budget"}


# --- Rows 6-7: generic repair-cycle primitive ----------------------------------------------


def test_repair_cycle_passes_on_first_attempt_no_repair_invoked():
    repairs = []
    outcome = with_one_repair_cycle(lambda: (True, "ok"), lambda: repairs.append(1))
    assert outcome == RepairCycleOutcome(passed=True, attempt=1, detail="ok")
    assert repairs == []


def test_repair_cycle_repairs_once_then_passes():
    attempts = iter([(False, "first fail"), (True, "fixed")])
    repairs = []
    outcome = with_one_repair_cycle(lambda: next(attempts), lambda: repairs.append(1))
    assert outcome == RepairCycleOutcome(passed=True, attempt=2, detail="fixed")
    assert repairs == [1]


def test_repair_cycle_terminal_after_one_repair_still_fails():
    attempts = iter([(False, "first fail"), (False, "second fail")])
    repairs = []
    outcome = with_one_repair_cycle(lambda: next(attempts), lambda: repairs.append(1))
    assert outcome == RepairCycleOutcome(passed=False, attempt=2, detail="second fail")
    assert repairs == [1]  # exactly one repair invoked, never a second
