# n=1 calibration probe: τ (tau), the divisor-counting function

Throwaway experiment, not project content. Purpose: watch the scoring machinery (fact suite
+ mutant detection) work end-to-end against one case where the right answer is already known,
before building anything general. Will be deleted later. This folder is gitignored and has
never been pushed.

- `task.lean` — the pinned true definition, a sanity check against Mathlib's own divisor
  count, the fact suite (as Lean `example`s), and the mutant/junk candidates.
- `score.py` — scores the three candidates (true/mutant/junk) against the fact suite via
  LeanInteract, splicing each candidate under the pinned name `tau`.
