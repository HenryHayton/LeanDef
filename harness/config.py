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
DEFAULT_CHECK_TIMEOUT = 60.0
DEFAULT_WARMUP_TIMEOUT = 600.0  # 10 minutes: LeanREPLConfig/AutoLeanServer construction + imports
