"""Shared configuration for prelim testing. Mirrors `bedrock/config.py`'s pattern: one module
holding the paths and dials, rather than values copy-pasted across call sites.

**Endpoint configuration is environment-only, and deliberately so.** `PRELIM_ENDPOINT_URL` and
`PRELIM_API_KEY` are read from the environment at call time, never stored in this file and never
committed. There is no provider-specific code anywhere in this package -- a URL is a URL. The
endpoint is a RunPod-hosted vLLM server today; pointing at anything else that speaks the
OpenAI completions/chat shape is purely an env-var change, with nothing to edit here.

`PRELIM_API_KEY` is OPTIONAL: vLLM is frequently run keyless behind a private network, and an
absent/empty key means no `Authorization` header is sent at all (not an empty one).
"""

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# On-disk output tree. Note the asymmetry with the package name (`prelim/` vs
# `prelim_testing/output/`): the package is short because it is imported constantly; the output
# directory is spelled out because it sits at the repo root next to `bedrock/output/` and
# `miner/output/`, where the extra clarity is worth more than the brevity.
OUTPUT_DIR = REPO_ROOT / "prelim_testing" / "output"

# Structured provenance log (JSONL, one record per attempt) -- same discipline as
# `bedrock.config.CALL_LOG_PATH`: every call, success or final failure, is traceable. Directory
# created on first write, not here (matching that module's lazy-mkdir convention).
CALL_LOG_PATH = OUTPUT_DIR / "call_log.jsonl"

SAMPLES_DIR = OUTPUT_DIR / "samples"

# The pinned input corpus: one directory per task, each with `dossier.md` + `task.json`.
# Consolidated from the authoring pipeline's own scratch output dirs and TRACKED in git (unlike
# `output/`) -- it is the experiment's input, it cost real Bedrock spend to produce, and prelim
# testing is not reproducible without exactly these 41 dossiers. Overridable per run via
# `$PRELIM_TASKS_DIR` (see `prelim.prompts.tasks_dir`).
TASKS_DIR = REPO_ROOT / "prelim_testing" / "tasks"

# --- Environment variable names (the whole configuration contract) ---------------------------
ENV_ENDPOINT_URL = "PRELIM_ENDPOINT_URL"
ENV_API_KEY = "PRELIM_API_KEY"


def endpoint_url() -> str | None:
    """The configured endpoint, or None if unset. Read at call time (not import time) so tests
    and a long-running driver can both change it without reimporting."""
    value = os.environ.get(ENV_ENDPOINT_URL, "").strip()
    return value or None


def api_key() -> str | None:
    """The configured key, or None if unset/empty. None means: send no auth header at all."""
    value = os.environ.get(ENV_API_KEY, "").strip()
    return value or None


# --- Retry / timeout dials --------------------------------------------------------------------
#
# Dials, not commitments -- same status as every other threshold in this codebase.
#
# The timeout is deliberately generous. These are reasoning/prover models writing long chains of
# thought at temperature; a 60s-style API default would turn ordinary slow generations into
# spurious retries, and retrying a 4-minute generation is far more expensive than waiting for it.
DEFAULT_TIMEOUT_S = 300.0

# "up to 3 attempts" = the initial call plus 2 retries, matching bedrock.config.MAX_ATTEMPTS'
# own reading of the same phrase.
MAX_ATTEMPTS = 3
RETRY_BASE_DELAY_S = 1.0  # backoff: RETRY_BASE_DELAY_S * 2**(attempt_index), attempt_index from 0
