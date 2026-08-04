"""Scoring configuration. Every path is derived here so nothing downstream assumes a laptop.

The box and the laptop run identical code against different roots; `SCORES_DIR` and
`TASKS_DIR` are the only things that move, and both are env-overridable so an rsync'd tree can
live anywhere.
"""

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

ENV_SCORES_DIR = "SCORING_SCORES_DIR"
ENV_TASKS_DIR = "SCORING_TASKS_DIR"
ENV_SAMPLES_DIR = "SCORING_SAMPLES_DIR"
ENV_WORKERS = "SCORING_WORKERS"

SCHEMA_VERSION = 1


def scores_dir() -> Path:
    override = os.environ.get(ENV_SCORES_DIR, "").strip()
    return Path(override) if override else REPO_ROOT / "scoring_output" / "scores"


def tasks_dir() -> Path:
    override = os.environ.get(ENV_TASKS_DIR, "").strip()
    return Path(override) if override else REPO_ROOT / "prelim_testing" / "tasks"


def samples_dir() -> Path:
    override = os.environ.get(ENV_SAMPLES_DIR, "").strip()
    return Path(override) if override else REPO_ROOT / "prelim_testing" / "output" / "samples"


def worker_count() -> int:
    """Sequential by default. The pool is designed for but not built; 5.7 GB of resident Mathlib
    per worker (measured 2026-08-05) is what bounds this, not CPU."""
    try:
        return max(1, int(os.environ.get(ENV_WORKERS, "1")))
    except ValueError:
        return 1


# Recycle the scoring server on the same growth-relative rule the test fixture uses, plus a
# candidate-count belt: a full pass is a far longer server lifetime than any test session.
SERVER_GROWTH_FACTOR = 1.5
SERVER_ABSOLUTE_CAP_GB = 10.0
# The candidate-count belt is a backstop, not the primary control -- growth-from-baseline is.
# Set from measurement (2026-08-06): a cold Mathlib import costs ~40 s on the Mac, so a belt of
# 50 adds ~0.8 s/candidate against a measured ~0.9 s/candidate of actual work, i.e. it would
# roughly DOUBLE the run for protection the RSS check already provides. 300 keeps a bound on
# unbounded server lifetime without paying for it on every batch.
RECYCLE_EVERY_N_CANDIDATES = 300

# One retry for infrastructure failures (ENV_DEATH/ERRORED) before a fact is recorded ERROR.
INFRA_RETRY_ATTEMPTS = 1

# The truth definition's symbol during the tier-4 equivalence probe. MUST differ from the task
# symbol (`VTask.`) so fact statements -- which name `VTask.*` -- can never resolve against the
# truth definition. See `scoring.equivalence` for the inertness argument and its adversarial test.
TRUTH_SYMBOL_PREFIX = "VTruth."
