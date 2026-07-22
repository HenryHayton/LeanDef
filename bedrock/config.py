"""Shared configuration for the Bedrock LLM client: region, pinned model IDs, transport
override, and the provenance log path.

Single config module, mirroring `harness/config.py`'s pattern (see that module's own
docstring) -- one source of truth rather than values copy-pasted across call sites.

**Reproducibility rule** (`docs/design/verifier_architecture_2026-07-20.md` §4, "Rules for
the prover layer"): "the exact Bedrock model ID is pinned and recorded alongside the
Lean/Mathlib pins." `AUTHORING_MODEL_ID`/`FLAGSHIP_MODEL_ID` are that pin for this client;
`bedrock.client.BedrockClient` records whichever one was used on every logged call (see
`bedrock.client`'s module docstring), the same way `CLAUDE.md`/`README.md` record the pinned
Lean/Mathlib/lean-interact versions.

**Placeholder values, AWS access pending.** The company Bedrock account has an access problem
being resolved by an admin (see the task that introduced this module) -- there is nothing real
to point these at yet. Every value below is a placeholder to be filled in once access arrives;
`docs/design/`-level review of which actual Claude model(s) stage 2 should use has not happened
either, so even the *choice* of model (not just its exact ID string) is unresolved. See this
package's own README-equivalent (the module docstring of `bedrock.client`) for exactly what
changes when real access lands.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REGION = "us-east-1"  # placeholder -- not yet confirmed against the company AWS account

# Two pinned model ID slots (task instructions): dossier generation will use FLAGSHIP_MODEL_ID;
# other stage-2 authoring calls use AUTHORING_MODEL_ID. Both hold the same placeholder for now
# -- nothing yet distinguishes what "flagship" vs "authoring" should actually mean model-wise,
# since no stage-2 prompt work exists yet (out of scope for this task).
AUTHORING_MODEL_ID = "PLACEHOLDER-authoring-model-id"
FLAGSHIP_MODEL_ID = "PLACEHOLDER-flagship-model-id"

# When None: real Bedrock, resolved by boto3's own region-based endpoint resolution. When set
# (a "http://host:port" string): every call goes to that URL instead, with no AWS
# authentication attempted at all -- see `bedrock.client`'s module docstring for exactly which
# code path this switches. This is the ONLY thing tests set; nothing else in this module
# changes between stub and real use.
ENDPOINT_URL: str | None = None

# Structured provenance log (JSONL, one record per call attempt -- see `bedrock.client`'s
# `_log_attempt`): every LLM-populated value in a stage-2 task must be traceable to a logged
# call, per the task that introduced this client. Directory created on first write, not here,
# matching `miner.rank.write_manifest`'s own lazy-mkdir convention.
CALL_LOG_PATH = REPO_ROOT / "bedrock" / "output" / "call_log.jsonl"

# Retry tuning (task instructions: "maximum 3 attempts total"). A dial, not a commitment --
# named here rather than a literal buried in `bedrock.client`, matching every other
# threshold in this codebase (e.g. `miner.config`'s gate thresholds).
MAX_ATTEMPTS = 3
RETRY_BASE_DELAY_S = 1.0  # backoff: RETRY_BASE_DELAY_S * 2**(attempt_index), attempt_index from 0

# Per-call HTTP timeouts (seconds). Bedrock's own default request timeout is much longer than
# this project needs for short authoring prompts; kept explicit rather than relying on an SDK
# default, per this codebase's standing rule that every network/REPL call passes an explicit
# timeout (see `harness/config.py`'s own DECIDE_TIMEOUT/PROOF_TIMEOUT comment for the hang this
# rule exists to prevent).
CONNECT_TIMEOUT_S = 10.0
READ_TIMEOUT_S = 60.0
