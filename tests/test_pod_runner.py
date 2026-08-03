"""Tests for `scripts/pod_runner.py` -- the parts that can be honestly tested from a Mac.

The vLLM subprocess is mocked throughout: there is no GPU here and no `vllm` binary, so what is
verified is the SEQUENCING (right models, right order, old process stopped before the next
starts), the WATCHDOG timer logic, and the CONTROL server's advance/status handling. Whether
`vllm serve` itself works is verified by the runbook's smoke test on the real pod, and nothing
here pretends otherwise.

`scripts/` is not a package, so the module is loaded by path.
"""

import importlib.util
import json
import threading
import urllib.request
from pathlib import Path

import pytest

_SPEC = importlib.util.spec_from_file_location(
    "pod_runner", Path(__file__).resolve().parent.parent / "scripts" / "pod_runner.py"
)
pod_runner = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(pod_runner)


class FakeProc:
    """Stands in for a `vllm serve` subprocess."""

    def __init__(self, name):
        self.name = name
        self.terminated = False
        self.killed = False
        self._alive = True
        self.returncode = None

    def terminate(self):
        self.terminated = True
        self._alive = False

    def kill(self):
        self.killed = True
        self._alive = False

    def wait(self, timeout=None):
        return 0

    def poll(self):
        return None if self._alive else 0


class StubbornProc(FakeProc):
    """Ignores SIGTERM -- a model mid-load. Must be escalated to kill()."""

    def terminate(self):
        self.terminated = True  # but stays alive

    def wait(self, timeout=None):
        if not self.killed:
            raise pod_runner.subprocess.TimeoutExpired(cmd="vllm", timeout=timeout)
        return 0


@pytest.fixture
def sequencer():
    spawned = []

    def spawn(name):
        p = FakeProc(name)
        spawned.append(p)
        return p

    seq = pod_runner.Sequencer(["model-a", "model-b", "model-c"], spawn=spawn)
    seq._spawned = spawned
    return seq


# --- sequencing ---------------------------------------------------------------------------------


def test_models_are_served_in_order(sequencer):
    assert sequencer.start_next() == "model-a"
    assert sequencer.start_next() == "model-b"
    assert sequencer.start_next() == "model-c"


def test_exhausted_list_returns_none(sequencer):
    for _ in range(3):
        sequencer.start_next()
    assert sequencer.start_next() is None


def test_previous_vllm_is_stopped_before_the_next_starts(sequencer):
    """A stuck old process holding VRAM would make the NEXT model fail to load."""
    sequencer.start_next()
    first = sequencer._spawned[0]
    assert first.terminated is False

    sequencer.start_next()
    assert first.terminated is True
    assert len(sequencer._spawned) == 2


def test_a_process_ignoring_sigterm_is_escalated_to_kill():
    seq = pod_runner.Sequencer(["a", "b"], spawn=lambda n: StubbornProc(n))
    seq.start_next()
    stubborn = seq.proc
    seq.start_next()

    assert stubborn.terminated is True
    assert stubborn.killed is True


def test_status_reports_position_and_model(sequencer):
    sequencer.start_next()
    sequencer.start_next()
    s = sequencer.status()

    assert s["model"] == "model-b"
    assert s["index"] == 1
    assert s["total"] == 3
    assert s["vllm_running"] is True
    assert s["terminating"] is False
    assert s["uptime_s"] >= 0


def test_the_shipped_model_list_matches_the_driver_side_table():
    """A mismatch stalls the run at 2am: the driver waits for a name the pod never serves."""
    from prelim.models import MODEL_SLUGS, get_model

    assert pod_runner.MODELS == [get_model(s).hf_name for s in MODEL_SLUGS]


# --- the control server ---------------------------------------------------------------------------


@pytest.fixture
def control(sequencer):
    server = pod_runner.make_control_server(sequencer, None, port=0, on_finished=lambda: None)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host, port = server.server_address
    yield sequencer, f"http://{host}:{port}"
    server.shutdown()
    server.server_close()


def _get(url):
    with urllib.request.urlopen(url, timeout=5) as r:
        return json.loads(r.read())


def _post(url):
    req = urllib.request.Request(url, data=b"", method="POST")
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.loads(r.read())


def test_status_endpoint_reports_the_current_model(control):
    sequencer, base = control
    sequencer.start_next()
    assert _get(f"{base}/status")["model"] == "model-a"


def test_advance_endpoint_moves_to_the_next_model(control):
    sequencer, base = control
    sequencer.start_next()

    body = _post(f"{base}/advance")
    assert body["model"] == "model-b"
    assert body["terminating"] is False
    assert sequencer.current_model == "model-b"


def test_advance_past_the_last_model_reports_terminating(control):
    sequencer, base = control
    for _ in range(3):
        sequencer.start_next()

    body = _post(f"{base}/advance")
    assert body["model"] is None
    assert body["terminating"] is True
    assert sequencer.terminating is True


def test_advance_replies_before_terminating_so_the_driver_never_hangs(sequencer):
    """The driver's advance call must not block on a pod busy killing itself."""
    started = threading.Event()
    server = pod_runner.make_control_server(sequencer, None, port=0, on_finished=started.set)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host, port = server.server_address
    try:
        for _ in range(3):
            sequencer.start_next()
        body = _post(f"http://{host}:{port}/advance")  # returns promptly
        assert body["terminating"] is True
        assert started.wait(timeout=5) is True  # termination happened, just not inline
    finally:
        server.shutdown()
        server.server_close()


def test_unknown_route_is_404(control):
    _, base = control
    with pytest.raises(urllib.error.HTTPError) as exc:
        _get(f"{base}/nope")
    assert exc.value.code == 404


# --- idle watchdog -------------------------------------------------------------------------------


def test_watchdog_terminates_after_the_idle_timeout(sequencer):
    """A Mac that died at 2am must not leave an A100 billing until morning."""
    fired = []
    now = [0.0]
    wd = pod_runner.IdleWatchdog(
        sequencer, timeout_s=100, poll_s=10, on_idle=lambda: fired.append(True),
        clock=lambda: now[0], sleep_fn=lambda s: now.__setitem__(0, now[0] + s),
    )
    wd.run()
    assert fired == [True]
    assert sequencer.terminating is True


def test_watchdog_does_not_fire_while_activity_continues(sequencer):
    fired = []
    now = [0.0]
    wd = pod_runner.IdleWatchdog(
        sequencer, timeout_s=100, poll_s=10, on_idle=lambda: fired.append(True),
        clock=lambda: now[0], sleep_fn=lambda s: now.__setitem__(0, now[0] + s),
    )

    def busy(s):
        now[0] += s
        wd.touch()  # something hit the control server
        if now[0] > 500:
            wd.stop()

    wd._sleep = busy
    wd.run()
    assert fired == []


def test_touch_resets_the_idle_clock(sequencer):
    now = [0.0]
    wd = pod_runner.IdleWatchdog(sequencer, clock=lambda: now[0])
    now[0] = 50
    assert wd.idle_for() == 50
    wd.touch()
    assert wd.idle_for() == 0


def test_control_requests_touch_the_watchdog(sequencer):
    now = [0.0]
    wd = pod_runner.IdleWatchdog(sequencer, clock=lambda: now[0])
    server = pod_runner.make_control_server(sequencer, wd, port=0, on_finished=lambda: None)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host, port = server.server_address
    try:
        now[0] = 500
        assert wd.idle_for() == 500
        _get(f"http://{host}:{port}/status")
        assert wd.idle_for() == 0
    finally:
        server.shutdown()
        server.server_close()


# --- termination ------------------------------------------------------------------------------------


def test_missing_credentials_prints_a_banner_instead_of_raising(monkeypatch, capsys):
    """An un-terminated pod is bad; a script that crashes on startup is worse."""
    monkeypatch.delenv("RUNPOD_API_KEY", raising=False)
    monkeypatch.delenv("RUNPOD_POD_ID", raising=False)

    assert pod_runner.terminate_pod() is False
    assert "PLEASE TERMINATE THIS POD MANUALLY" in capsys.readouterr().out


def test_termination_failure_is_reported_not_raised(monkeypatch):
    monkeypatch.setenv("RUNPOD_API_KEY", "k")
    monkeypatch.setenv("RUNPOD_POD_ID", "p")

    def boom(*a, **kw):
        raise OSError("network down")

    monkeypatch.setattr(pod_runner.urllib.request, "urlopen", boom)
    assert pod_runner.terminate_pod() is False
