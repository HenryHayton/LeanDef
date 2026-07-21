"""Shared configuration: paths and REPL tuning.

Single source of truth for values previously copy-pasted across `scripts/smoke_test.py`,
`tests/conftest.py`, and `archive/n1_tau/score.py` (see `docs/repo_audit.md` §4, §7,
observations 6-7).
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LEAN_PROJECT_DIR = REPO_ROOT / "lean"

# AutoLeanServer refuses to run once system-wide memory usage is above this fraction (default
# 0.8) to protect against OOM. Raised here since dev laptops often sit above 80% used from
# unrelated apps -- see CLAUDE.md "Known follow-ups": revisit once on a machine with more
# headroom, or before the guard's protection actually matters.
MAX_TOTAL_MEMORY = 0.95

# Timeouts (seconds). Every REPL call in this package is expected to pass one of these
# explicitly rather than relying on lean_interact's own default of no timeout at all -- see
# docs/repo_audit.md observation 2 for the hang this is meant to prevent.
#
# Per-mechanism, per task_schema_v1.md "Scoring semantics" and
# docs/decidability_bias_survey.md finding 4 (which this split resolves): a single timeout
# tuned for decidable-scale cost was previously applied to every fact regardless of type.
#
# DECIDE_TIMEOUT covers mechanism `decide`: kernel computation, milliseconds in practice.
# Used for decidable facts, splicing, and other REPL-infrastructure checks (admissibility's
# axiom probe, warm-up imports) that are all decide/elaboration-scale today.
DECIDE_TIMEOUT = 60.0

# PROOF_TIMEOUT covers mechanism `proof`: reward-structure design §2.3 puts genuine proof
# search at "seconds to minutes" per attempt, and the tri-state protocol
# (verifier_architecture_2026-07-20.md §4) needs two attempts (fact, negation) per fact.
# PLACEHOLDER VALUE, UNUSED until the prover scaffold exists -- nothing in this codebase
# calls a prover yet (harness.scoring.run_facts raises NotImplementedError for mechanism
# `proof`), so this number has not been validated against anything real. Revisit once real
# prover-agent latency is known.
PROOF_TIMEOUT = 300.0

DEFAULT_WARMUP_TIMEOUT = 600.0  # 10 minutes: LeanREPLConfig/AutoLeanServer construction + imports

# EXCESSIVE_UNKNOWN alarm threshold (task_schema_v1.md "Scoring semantics"): fraction of a
# candidate's proof-mechanism facts allowed to come back UNKNOWN before the score is flagged
# for review. "The 10% value is a dial, not a commitment" per the schema doc -- hence living
# here, not hardcoded where it's used.
EXCESSIVE_UNKNOWN_THRESHOLD = 0.10
