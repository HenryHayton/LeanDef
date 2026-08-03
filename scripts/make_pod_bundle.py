#!/usr/bin/env python3
"""Emit one self-contained bootstrap script for the pod, with `pod_runner.py` inlined.

The pod has no checkout of this repo and no credentials to get one, so the human pastes a single
file into the web terminal. Assembling it here -- rather than asking them to paste two files in
the right order at 11pm -- removes the step most likely to go wrong.

    uv run python scripts/make_pod_bundle.py | pbcopy     # then paste into the pod terminal
    uv run python scripts/make_pod_bundle.py --key KEY --pod-id ID > /tmp/bootstrap.sh
"""

import argparse
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent


def build(api_key: str | None = None, pod_id: str | None = None) -> str:
    setup = (SCRIPTS / "pod_setup.sh").read_text(encoding="utf-8")
    runner = (SCRIPTS / "pod_runner.py").read_text(encoding="utf-8")

    if "__POD_RUNNER_PY__" not in setup:
        raise SystemExit("pod_setup.sh no longer contains the __POD_RUNNER_PY__ placeholder")
    # The runner is emitted inside a quoted heredoc ('PYEOF'), so the shell performs no
    # expansion on it -- no escaping needed, and no risk of $VAR inside the Python being eaten.
    if "\nPYEOF\n" in runner:
        raise SystemExit("pod_runner.py contains the heredoc terminator; change the terminator")
    out = setup.replace("__POD_RUNNER_PY__", runner.rstrip("\n"))

    # Substitute ONLY on the export lines, never globally: the placeholders also appear in the
    # "did you forget to fill these in?" guard, and a global replace rewrites that guard into
    # `if pod_id == <the real pod id>` -- i.e. it warns that the value is missing precisely when
    # it is present. Found while preparing the live bundle, 2026-08-03.
    lines = out.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if api_key and line.startswith("export RUNPOD_API_KEY="):
            lines[i] = f'export RUNPOD_API_KEY="${{RUNPOD_API_KEY:-{api_key}}}"\n'
        elif pod_id and line.startswith("export RUNPOD_POD_ID="):
            lines[i] = f'export RUNPOD_POD_ID="${{RUNPOD_POD_ID:-{pod_id}}}"\n'
    return "".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--key", default=None, help="RunPod API key to bake in (optional)")
    p.add_argument("--pod-id", default=None, help="RunPod pod id to bake in (optional)")
    args = p.parse_args()
    print(build(args.key, args.pod_id))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
