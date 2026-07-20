# A Verifiable Faithfulness Signal for Definition Writing

A kernel-adjudicated verifier that checks whether a candidate Lean 4 definition denotes the
*intended* mathematical object, not merely that it type-checks. Faithfulness is scored via a
two-sided fact suite (things the true object satisfies) and mutant suites (typed plausible
misreadings the true object must refute), all certified through the Lean kernel.

## Status

**Step 0: environment setup.** No task schema, no Mathlib mining, no model work yet.

## Layout

- `harness/` — Python package: verifier logic, Lean REPL client code
- `lean/` — Lean 4 subproject (pinned toolchain, Mathlib dependency)
- `tasks/` — task definitions and schema (`tasks/schema/`, `tasks/handbuilt/`)
- `docs/` — design notes
- `scripts/` — one-off scripts (e.g. smoke test)
- `tests/` — pytest suite

## Pinned versions

- Lean: [`v4.32.0`](https://github.com/leanprover/lean4/releases/tag/v4.32.0)
- Mathlib: [`v4.32.0`](https://github.com/leanprover-community/mathlib4/releases/tag/v4.32.0)
  (exact tag, pinned in `lean/lakefile.toml`)
- lean-interact: `0.11.5` (pinned via `uv.lock`)
- Python: `3.12`

## Timings

From `scripts/smoke_test.py` (run on a MacBook, Apple Silicon, with the Mathlib cache
already downloaded). Run under real memory pressure from other apps (~86% system memory
used, ~2.4 GB free) — cold-import and unpickle times are likely inflated versus a quiet
machine; re-run and update these numbers if they matter for planning later milestones.

| Stage | Time |
|---|---|
| `LeanREPLConfig` setup (builds REPL against `lean/` project) | 16.9 s |
| Start `AutoLeanServer` | <0.01 s |
| Cold command: `import Mathlib` | 141.7 s |
| REPL process RSS after Mathlib import (approx. peak) | 2546 MB |
| Warm: trivial `#eval` | 0.07 s |
| Warm: small `decide` (`2 + 2 = 4`) | 0.01 s |
| Warm: heavier `decide` (bounded `∀ n < 100`) | 0.04 s |
| Splice: `def` in its own command | 0.01 s |
| Splice: follow-up `example` via `decide`, reusing env id | <0.01 s |
| Sorry detection (`def ... := sorry`) | 0.01 s |
| Pickle warm Mathlib environment to disk | <0.01 s |
| Start a fresh `AutoLeanServer` | <0.01 s |
| Unpickle environment from disk | 138.2 s (see caveat above — expected to be much faster under normal memory conditions) |
| `decide` check against the unpickled environment | 1.49 s |

`AutoLeanServer`'s default memory guard (`max_total_memory=0.8`, meaning it refuses to run
above 80% system-wide memory usage) tripped on this machine even after freeing some memory;
the smoke test and test suite raise it to `0.95`. Worth lowering back down once running on a
machine with more headroom, or if you want the guard to actually protect you.
