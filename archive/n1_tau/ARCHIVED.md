# Archived: n=1 τ probe

This is the hand-built n=1 probe for the divisor function τ, archived 21 July 2026. It
validated the splice-and-score pipeline end to end: 7 decidable facts over the true
definition, 7 typed mutants, and a junk candidate — all 72 predictions matched reality.

It is archived, not deleted: it will later become a golden fixture / dataset entry once the
task schema exists, and `score.py` here is the source the generic scorer will be extracted
from (see `docs/repo_audit.md`).

Known issues, frozen as-is per the audit: `task.lean` reflects an older 1-mutant/10-fact
version and disagrees with `score.py` (7 mutants/7 facts) — `score.py` is the authoritative
one; the `PREDICTIONS` block is one-off calibration scaffolding, not infrastructure; no
admissibility gate or timeouts exist in this code; the dossier never specifies behaviour at
n = 0 and facts/mutants were not scoped to a declared domain.

Do not edit any code in `archive/n1_tau/` — it's archived exactly as audited.
