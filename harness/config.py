"""Shared configuration: paths and REPL tuning.

Single source of truth for values previously copy-pasted across `scripts/smoke_test.py`,
`tests/conftest.py`, and `archive/n1_tau/score.py` (see `docs/repo_audit.md` §4, §7,
observations 6-7).
"""

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Which Lean project the REPL runs against. Overridable via `$VERIFIER_LEAN_PROJECT_DIR`
# (2026-08-05) because the EC2 scoring box has TWO projects and the choice is not cosmetic:
#
#   ~/definition-verifier/lean   -- the plain project, what the Mac uses
#   ~/verifier-lean              -- Hammer-enabled, required for tier 3 (`docs/ec2_runbook.md`)
#
# Scoring on the box runs against the Hammer-enabled one from the start, so a C->C2 trigger does
# not force an environment switch mid-phase. Named explicitly rather than resolved from the
# working directory: a scoring run that silently picked its Lean project from wherever it was
# launched could produce verdicts against a different Mathlib than the corpus was validated
# against, which is precisely the failure the pin gate exists to prevent.
ENV_LEAN_PROJECT_DIR = "VERIFIER_LEAN_PROJECT_DIR"
_override = os.environ.get(ENV_LEAN_PROJECT_DIR, "").strip()
LEAN_PROJECT_DIR = Path(_override).expanduser() if _override else REPO_ROOT / "lean"

# The REPL binary LeanInteract drives. Normally None -- LeanInteract fetches and builds its own.
#
# On the EC2 box, tier 3 (hammer) needs `libcvc5_cvc5.so`'s symbols loaded into the interpreter or
# the process SIGABRTs, and there is no CLI-flag path through LeanInteract to `--load-dynlib`
# (`LeanServer.start()` hardcodes its argv, and the stock REPL's `main` discards its args --
# both verified by reading the sources, see `ladder/tier3.py`). The resolution is a patched REPL
# checkout whose `main` calls `Lean.loadDynlib` directly, reading `LEAN_INTERACT_LOAD_DYNLIB`.
#
# That patched REPL is a no-op when the env var is unset, so it is safe for every tier, not just
# tier 3 -- which is why this is one setting rather than a tier-3-only code path.
ENV_REPL_PATH = "VERIFIER_REPL_PATH"
_repl_override = os.environ.get(ENV_REPL_PATH, "").strip()
LOCAL_REPL_PATH = Path(_repl_override).expanduser() if _repl_override else None

# AutoLeanServer refuses to start once system-wide memory usage is above this fraction.
#
# Back to lean_interact's own 0.8 default (2026-08-05), from the 0.95 this repo had been
# carrying. The reason it was raised -- dev laptops sit above 80% from unrelated apps, so the
# guard was a nuisance -- was real but is now outweighed: on 2026-08-04 the guard's protection
# stopped being hypothetical. Several interrupted test runs stranded Mathlib servers (orphans
# reparent to launchd and are not reaped by `harness.repl._kill_stray_children`, which only
# reaps children of the current process); at 0.95 each subsequent run cheerfully started
# ANOTHER ~2.5 GB server on an already-full machine instead of refusing, and six of them
# reached 15.8 GB of 16 GB, forcing a hard restart. Refusing to start is the correct behaviour
# there, and a `MemoryError` naming the real problem beats a wedged laptop.
#
# If this makes the suite refuse to run on a busy laptop, that is the guard working: close
# something, or run `scripts/reap_repls.py` to clear strays from an earlier interrupted run.
# The shared session-scoped fixture (`tests/conftest.py`) means one server now serves the whole
# suite, so the headroom actually needed is far smaller than when this was raised.
MAX_TOTAL_MEMORY = 0.8

# Timeouts (seconds). Every REPL call in this package is expected to pass one of these
# explicitly rather than relying on lean_interact's own default of no timeout at all -- see
# docs/repo_audit.md observation 2 for the hang this is meant to prevent.
#
# Per-mechanism, per task_schema_v1_1.md "Scoring semantics" and
# docs/decidability_bias_survey.md finding 4 (which this split resolves): a single timeout
# tuned for decidable-scale cost was previously applied to every fact regardless of type.
#
# DECIDE_TIMEOUT covers mechanism `decide`: kernel computation, milliseconds in practice.
# Used for decidable facts, splicing, and other REPL-infrastructure checks (admissibility's
# axiom probe, warm-up imports) that are all decide/elaboration-scale today.
DECIDE_TIMEOUT = 60.0

# mechanism `proof` timeouts: retired from here (was PROOF_TIMEOUT, an unused placeholder --
# see docs/deferred.md's now-actioned entry). Superseded by ladder.budgets.LadderBudgets, per
# docs/design/reward_structure_2026-07-21.md §7 ("One configuration object governs all ladder
# execution... It replaces harness.config.PROOF_TIMEOUT").

DEFAULT_WARMUP_TIMEOUT = 600.0  # 10 minutes: LeanREPLConfig/AutoLeanServer construction + imports

# EXCESSIVE_UNKNOWN alarm threshold (task_schema_v1_1.md "Scoring semantics"): fraction of a
# candidate's proof-mechanism facts allowed to come back UNKNOWN before the score is flagged
# for review. "The 10% value is a dial, not a commitment" per the schema doc -- hence living
# here, not hardcoded where it's used.
EXCESSIVE_UNKNOWN_THRESHOLD = 0.10
