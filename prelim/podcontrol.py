"""Thin client for the pod-side control server (`scripts/pod_runner.py`) and for vLLM's own
readiness route.

Kept separate from `prelim.driver` so the driver's orchestration can be tested against a fake
control server without any HTTP mocking gymnastics, and separate from `prelim.client` because
this talks to a different service with different failure semantics: a control call that fails is
a run-ending event, not something to retry into a 5-minute backoff.
"""

import time
from dataclasses import dataclass

import requests


class PodControlError(RuntimeError):
    """The pod did not do what was asked. Always run-ending for the current model."""


@dataclass
class PodControl:
    """`control_url` is the pod runner's port-8001 proxy URL; `models_url` is vLLM's own
    `/v1/models` on port 8000. Both are full URLs -- no path guessing, same rule as the client."""

    control_url: str
    models_url: str
    timeout_s: float = 30.0

    def status(self) -> dict:
        try:
            r = requests.get(f"{self.control_url.rstrip('/')}/status", timeout=self.timeout_s)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            raise PodControlError(f"pod status check failed: {e}") from e

    def advance(self) -> dict:
        """Ask the pod to kill the current vLLM and start the next model. Returns the pod's
        report of what it did (including `terminating: true` after the last model)."""
        try:
            r = requests.post(f"{self.control_url.rstrip('/')}/advance", timeout=self.timeout_s)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            raise PodControlError(f"pod advance failed: {e}") from e

    def loaded_model(self) -> str | None:
        """The model id vLLM currently reports, or None if it is not answering yet. A model
        still loading refuses connections or 503s -- both mean 'not ready', neither is an error
        worth raising during a poll loop."""
        try:
            r = requests.get(self.models_url, timeout=self.timeout_s)
            if r.status_code != 200:
                return None
            data = r.json().get("data") or []
            return data[0].get("id") if data else None
        except (requests.RequestException, ValueError):
            return None

    def wait_for_model(
        self, hf_name: str, *, timeout_s: float = 900.0, poll_s: float = 10.0, sleep_fn=time.sleep,
        clock=time.monotonic,
    ) -> None:
        """Block until vLLM reports `hf_name` loaded.

        15 minutes by default: a cold 8B download-and-load on a fresh pod genuinely takes several
        minutes, and a too-eager timeout would abandon a working run. Exceeding it is loud and
        run-ending for the model -- a pod that has not produced the expected model in 15 minutes
        is broken, and continuing would silently generate every remaining sample against the
        WRONG model, which is far worse than stopping.
        """
        deadline = clock() + timeout_s
        last_seen = None
        while clock() < deadline:
            last_seen = self.loaded_model()
            if last_seen == hf_name:
                return
            sleep_fn(poll_s)
        raise PodControlError(
            f"timed out after {timeout_s:.0f}s waiting for {hf_name!r} to load; "
            f"vLLM last reported {last_seen!r}"
        )
