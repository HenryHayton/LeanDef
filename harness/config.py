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
# DEFAULT_CHECK_TIMEOUT is tuned for decidable facts (reward-structure design §2.1) and
# decidable membership checks -- kernel computation, milliseconds. It is far too short for a
# genuine global/proof-based fact (§2.3), which the design doc puts at "seconds to minutes"
# per attempt. There is currently only this one tier; a prover-agent adjudication path, when
# built, will need its own (larger, budget-shaped, not just a longer timeout) parameter rather
# than reusing this constant. See docs/decidability_bias_survey.md.
DEFAULT_CHECK_TIMEOUT = 60.0
DEFAULT_WARMUP_TIMEOUT = 600.0  # 10 minutes: LeanREPLConfig/AutoLeanServer construction + imports
