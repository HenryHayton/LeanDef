"""Tests for `prelim.driver` and `prelim.podcontrol` against the stub endpoint.

Everything the driver does that matters is orchestration under failure: gate halts, resume,
per-sample error isolation, and the pod handshake. Those are tested here against a real loopback
server and a fake pod, with no GPU anywhere.
"""

import json

import pytest

from prelim import config as cfg
from prelim.driver import RunLog, run_model, run_prelim
from prelim.podcontrol import PodControl, PodControlError
from prelim.stubserver import ScriptedResponse, StubEndpointServer, chat_completion_body

GOOD = "```lean\ndef VTask.clog (b n : ℕ) : ℕ :=\n  if 1 < b ∧ 1 < n then VTask.clog b (n / b) + 1 else 0\n```"
GARBAGE = "I'm afraid I can't help with that request."


@pytest.fixture
def stub():
    servers = []

    def _make(script=None):
        s = StubEndpointServer(script)
        servers.append(s)
        return s

    yield _make
    for s in servers:
        s.stop()


@pytest.fixture
def paths(tmp_path):
    return {
        "samples_dir": tmp_path / "samples",
        "call_log_path": tmp_path / "call_log.jsonl",
        "run_log_path": tmp_path / "run_log.txt",
        "summary_path": tmp_path / "run_summary.json",
    }


def _run_log(paths):
    return RunLog(paths["run_log_path"], echo=False)


# --- happy path -----------------------------------------------------------------------------------


def test_run_model_generates_every_sample_and_stores_them(stub, paths):
    server = stub([ScriptedResponse(200, chat_completion_body(GOOD))])
    outcome = run_model(
        "herald-7b", ["Nat.clog", "Nat.ModEq"], samples_per_task=2,
        samples_dir=paths["samples_dir"], endpoint_url=server.url,
        call_log_path=paths["call_log_path"], run_log=_run_log(paths), concurrency=4,
    )

    assert outcome.status == "completed"
    assert outcome.completed == 4
    assert outcome.extraction_failures == 0
    files = sorted(p.name for p in (paths["samples_dir"] / "herald-translator").rglob("sample_*.json"))
    assert files == ["sample_00.json", "sample_00.json", "sample_01.json", "sample_01.json"]


def test_stored_sample_carries_extraction_and_regime_provenance(stub, paths):
    server = stub([ScriptedResponse(200, chat_completion_body(GOOD))])
    run_model(
        "herald-7b", ["Nat.clog"], samples_per_task=1, samples_dir=paths["samples_dir"],
        endpoint_url=server.url, run_log=_run_log(paths),
    )
    data = json.loads((paths["samples_dir"] / "herald-translator" / "Nat.clog" / "sample_00.json").read_text())

    assert data["extra"]["extraction_ok"] is True
    assert data["extra"]["declared_name"] == "VTask.clog"
    assert data["extra"]["top_p"] == cfg.TOP_P
    assert data["extra"]["endpoint_style"] == "chat"
    assert data["extra"]["card_sampling"] == {}  # Herald's card documents none
    assert data["temperature"] == 0.7  # sample 0 -> first temperature


def test_temperature_regime_is_applied_per_sample_index(stub, paths):
    server = stub([ScriptedResponse(200, chat_completion_body(GOOD))])
    run_model(
        "herald-7b", ["Nat.clog"], samples_per_task=cfg.SAMPLES_PER_TASK,
        samples_dir=paths["samples_dir"], endpoint_url=server.url, run_log=_run_log(paths),
    )
    temps = [
        json.loads((paths["samples_dir"] / "herald-translator" / "Nat.clog" / f"sample_{i:02d}.json").read_text())["temperature"]
        for i in range(cfg.SAMPLES_PER_TASK)
    ]
    assert temps == [0.7] * 5 + [1.0] * 5


# --- the gate ---------------------------------------------------------------------------------------


def test_gate_failure_halts_that_model_only(stub, paths):
    server = stub([ScriptedResponse(200, chat_completion_body(GARBAGE))])
    outcome = run_model(
        "herald-7b", ["Nat.clog"], samples_per_task=10, samples_dir=paths["samples_dir"],
        endpoint_url=server.url, run_log=_run_log(paths),
    )

    assert outcome.status == "gate_failed"
    assert server.call_count == 3  # stopped after the gate, not 10
    assert "template" in outcome.detail
    log = paths["run_log_path"].read_text()
    assert "GATE FAILED" in log
    assert "BEFORE concluding anything" in log  # points at our bug first


def test_gate_pass_proceeds_to_the_full_set(stub, paths):
    server = stub([ScriptedResponse(200, chat_completion_body(GOOD))])
    outcome = run_model(
        "herald-7b", ["Nat.clog"], samples_per_task=5, samples_dir=paths["samples_dir"],
        endpoint_url=server.url, run_log=_run_log(paths), concurrency=2,
    )
    assert outcome.status == "completed"
    assert server.call_count == 5


def test_gate_reuses_samples_already_on_disk_after_a_relaunch(stub, paths):
    """A relaunch must not spend fresh generations re-answering a settled question."""
    server = stub([ScriptedResponse(200, chat_completion_body(GOOD))])
    run_model("herald-7b", ["Nat.clog"], samples_per_task=4, samples_dir=paths["samples_dir"],
              endpoint_url=server.url, run_log=_run_log(paths))
    first_pass_calls = server.call_count

    outcome = run_model("herald-7b", ["Nat.clog"], samples_per_task=4, samples_dir=paths["samples_dir"],
                        endpoint_url=server.url, run_log=_run_log(paths))
    assert outcome.status == "completed"
    assert server.call_count == first_pass_calls  # nothing regenerated


# --- resume ------------------------------------------------------------------------------------------


def test_relaunch_generates_only_the_missing_samples(stub, paths):
    server = stub([ScriptedResponse(200, chat_completion_body(GOOD))])
    run_model("herald-7b", ["Nat.clog"], samples_per_task=2, samples_dir=paths["samples_dir"],
              endpoint_url=server.url, run_log=_run_log(paths))
    assert server.call_count == 2

    # Simulate a crash that lost one sample.
    (paths["samples_dir"] / "herald-translator" / "Nat.clog" / "sample_01.json").unlink()

    outcome = run_model("herald-7b", ["Nat.clog", "Nat.ModEq"], samples_per_task=2,
                        samples_dir=paths["samples_dir"], endpoint_url=server.url,
                        run_log=_run_log(paths))
    assert outcome.completed == 4
    assert server.call_count == 2 + 3  # the lost one + both of the new task


def test_corrupt_sample_is_regenerated_not_skipped(stub, paths):
    server = stub([ScriptedResponse(200, chat_completion_body(GOOD))])
    run_model("herald-7b", ["Nat.clog"], samples_per_task=1, samples_dir=paths["samples_dir"],
              endpoint_url=server.url, run_log=_run_log(paths))
    path = paths["samples_dir"] / "herald-translator" / "Nat.clog" / "sample_00.json"
    path.write_text("{truncated", encoding="utf-8")

    run_model("herald-7b", ["Nat.clog"], samples_per_task=1, samples_dir=paths["samples_dir"],
              endpoint_url=server.url, run_log=_run_log(paths))
    assert json.loads(path.read_text())["completion"]  # regenerated, valid again


# --- error isolation ------------------------------------------------------------------------------------


def test_a_failing_sample_costs_only_itself(stub, paths):
    """One 400 among many: that sample is lost, the rest still land."""
    server = stub([
        ScriptedResponse(200, chat_completion_body(GOOD)),  # gate x3
        ScriptedResponse(200, chat_completion_body(GOOD)),
        ScriptedResponse(200, chat_completion_body(GOOD)),
        ScriptedResponse(400, {"error": {"message": "bad", "code": 400}}),  # one failure
        ScriptedResponse(200, chat_completion_body(GOOD)),  # then fine again
    ])
    outcome = run_model("herald-7b", ["Nat.clog"], samples_per_task=5,
                        samples_dir=paths["samples_dir"], endpoint_url=server.url,
                        run_log=_run_log(paths), concurrency=1)

    assert outcome.status == "completed"
    assert outcome.completed == 4  # 5 attempted, 1 lost
    assert "errored" in paths["run_log_path"].read_text()


def test_extraction_failure_is_recorded_but_does_not_gate(stub, paths):
    """A model that cannot produce an extractable def is reporting its score -- the sample is
    still stored, because discarding it would erase the measurement."""
    server = stub([
        ScriptedResponse(200, chat_completion_body(GOOD)),
        ScriptedResponse(200, chat_completion_body(GOOD)),
        ScriptedResponse(200, chat_completion_body(GOOD)),
        ScriptedResponse(200, chat_completion_body(GARBAGE)),
    ])
    outcome = run_model("herald-7b", ["Nat.clog"], samples_per_task=4,
                        samples_dir=paths["samples_dir"], endpoint_url=server.url,
                        run_log=_run_log(paths), concurrency=1)

    assert outcome.completed == 4
    assert outcome.extraction_failures == 1
    data = json.loads((paths["samples_dir"] / "herald-translator" / "Nat.clog" / "sample_03.json").read_text())
    assert data["extra"]["extraction_ok"] is False
    assert data["extra"]["extraction_failure_reason"] == "no_def_found"
    assert data["completion"] == GARBAGE  # kept verbatim


# --- pod handshake -------------------------------------------------------------------------------------


class _FakePod:
    def __init__(self, *, fail_wait_on=None, fail_advance_on=None):
        self.waited, self.advanced = [], []
        self.fail_wait_on = fail_wait_on
        self.fail_advance_on = fail_advance_on
        self._current = None

    def wait_for_model(self, hf_name, *, timeout_s=900.0, **kw):
        if hf_name == self.fail_wait_on:
            raise PodControlError(f"timed out waiting for {hf_name}")
        self.waited.append(hf_name)
        self._current = hf_name

    def advance(self):
        if self._current == self.fail_advance_on:
            raise PodControlError("advance failed")
        self.advanced.append(self._current)
        return {"model": "next", "terminating": False}


def test_run_prelim_waits_for_each_model_then_advances(stub, paths):
    server = stub([ScriptedResponse(200, chat_completion_body(GOOD))])
    pod = _FakePod()
    result = run_prelim(
        ["herald-7b", "qwen2.5-coder-7b-instruct"], ["Nat.clog"], samples_per_task=1,
        samples_dir=paths["samples_dir"], endpoint_url=server.url, pod=pod,
        run_log_path=paths["run_log_path"], summary_path=paths["summary_path"], echo=False,
    )

    assert [o.status for o in result.outcomes] == ["completed", "completed"]
    assert pod.waited == ["FrenzyMath/Herald_translator", "Qwen/Qwen2.5-Coder-7B-Instruct"]
    assert len(pod.advanced) == 2  # including the final advance that terminates the pod
    assert "final advance requested" in paths["run_log_path"].read_text()


def test_pod_wait_failure_halts_the_whole_run(stub, paths):
    """The one failure that corrupts rather than reduces: generating against an unknown model."""
    server = stub([ScriptedResponse(200, chat_completion_body(GOOD))])
    pod = _FakePod(fail_wait_on="Qwen/Qwen2.5-Coder-7B-Instruct")
    result = run_prelim(
        ["herald-7b", "qwen2.5-coder-7b-instruct"], ["Nat.clog"], samples_per_task=1,
        samples_dir=paths["samples_dir"], endpoint_url=server.url, pod=pod,
        run_log_path=paths["run_log_path"], summary_path=paths["summary_path"], echo=False,
    )

    assert result.stopped_reason and "pod failure" in result.stopped_reason
    assert len(result.outcomes) == 1  # second model never ran
    assert "would corrupt the results" in paths["run_log_path"].read_text()


def test_gate_failure_does_not_stop_later_models(stub, paths):
    """One bad wrapper must not cost the others their night."""
    server = stub([ScriptedResponse(200, chat_completion_body(GARBAGE))])
    pod = _FakePod()
    result = run_prelim(
        ["herald-7b", "qwen2.5-coder-7b-instruct"], ["Nat.clog"], samples_per_task=3,
        samples_dir=paths["samples_dir"], endpoint_url=server.url, pod=pod,
        run_log_path=paths["run_log_path"], summary_path=paths["summary_path"], echo=False,
    )

    assert [o.status for o in result.outcomes] == ["gate_failed", "gate_failed"]
    assert result.stopped_reason is None  # the RUN completed; both models were judged
    assert len(pod.advanced) == 2


def test_summary_is_written_with_per_model_outcomes(stub, paths):
    server = stub([ScriptedResponse(200, chat_completion_body(GOOD))])
    run_prelim(["herald-7b"], ["Nat.clog"], samples_per_task=2,
               samples_dir=paths["samples_dir"], endpoint_url=server.url,
               run_log_path=paths["run_log_path"], summary_path=paths["summary_path"], echo=False)

    payload = json.loads(paths["summary_path"].read_text())
    assert payload["models"][0]["slug"] == "herald-7b"
    assert payload["models"][0]["status"] == "completed"
    assert payload["totals"]["herald-translator"] == 2
    assert payload["stopped_reason"] is None
    assert "ALL DONE" in paths["run_log_path"].read_text()


# --- PodControl ------------------------------------------------------------------------------------------


def test_wait_for_model_returns_once_the_name_matches():
    seen = []

    class P(PodControl):
        def loaded_model(self):
            seen.append(1)
            return "target" if len(seen) >= 3 else "previous"

    P(control_url="http://x", models_url="http://y").wait_for_model(
        "target", timeout_s=100, poll_s=0, sleep_fn=lambda s: None,
    )
    assert len(seen) == 3


def test_wait_for_model_times_out_loudly():
    class P(PodControl):
        def loaded_model(self):
            return "wrong-model"

    ticks = iter([0, 1, 2, 3, 999])
    with pytest.raises(PodControlError, match="wrong-model"):
        P(control_url="http://x", models_url="http://y").wait_for_model(
            "target", timeout_s=10, poll_s=0, sleep_fn=lambda s: None, clock=lambda: next(ticks),
        )
