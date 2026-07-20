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

_To be filled in during Step 0 (Task 3)._

- Lean: TBD
- Mathlib: TBD
- lean-interact: TBD

## Timings

_To be filled in during Step 0 (Task 4), from `scripts/smoke_test.py`._
