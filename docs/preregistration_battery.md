# Pre-registration — decode/exemplar battery (2026-08-07)

Committed **before any cell has produced a sample**. The decision rules below were stated by the
operator in the run brief; they are recorded here so that the reading of the results cannot be
fitted to the results.

Run: Goedel-Formalizer-V2-8B, 41 tasks × 10 samples per cell, temperature 0.7, one pod session.
Prompt axis fixed at **S-A_R0** for every cell (the eight-cell run's quality winner on conditional
admissibility; R1 is dead per that run's Finding 3). vLLM pinned to **v0.26.0** — the version the
eight-cell run served — so T0 is a paired control on the same server version, not merely the same
prompt.

## Batteries

**T — decode interventions**, exemplars held at the three-plain block:

| cell | intervention |
|---|---|
| T0 | none (paired in-session control) |
| T1 | `sorry`/`admit` token ban at decode time |
| T2 | assistant prefill: completion forced to begin at the spliced header |
| T3 | ban + prefill |

**A — exemplar fixes**, no decode intervention:

| cell | treatment |
|---|---|
| A1 | zero exemplars (instructions + conformance + glossary only) |
| A2 | three exemplars, reframed and structurally fenced |
| A3 | one exemplar (slot 1, `ceilRoot`), same reframe and fencing |

**C1 — composition** of the T winner and the A winner. Deliberately not defined in advance; built
by `pretuning.battery.compose` once T and A are scored, and run last.

## Decision rules, pre-stated

- **T battery** is judged on **admissible/100** and **non-verbatim admissible**, with the escape-
  route bucket table as mechanism. A T3 that beats T0 by more than ~2–3 points on adm/100 shrinks
  stage-0's job and goes into the frozen protocol.
- **A battery** is judged on **substitution rate first** — a fix that does not kill contamination
  fails regardless of what else it moves — then adm/100 and reach.
- **C1** must not materially underperform either winner. If it does, the finding is reported and
  **nothing freezes**.
- If C1 is clean, the prompt+decode architecture is frozen and recorded as the sampling protocol
  for all future measurement, stage-0 harvesting, and both training arms.
- Nothing about **scoring** changes in this session. Readout is admissibility-only; any fidelity
  column, if computed, is labelled indicative and carries its resolution rate alongside.

## Why the sorry rate is not the metric

Banning `sorry` cannot make a model able to write a definition it could not write. It can only
make it stop saying `sorry`, so the punt rate in T1/T3 is guaranteed to fall and reporting that
fall would be measuring the intervention against itself. What is in question is where the punt
**goes**. The six escape-route buckets are fixed in code (`pretuning/buckets.py`) before any T1/T3
sample exists:

    truncation_at_cap > exemplar_substitution > degenerate_body > tactic_junk_body
                      > real_construction_attempt > other

Precedence is total, so every sample lands in exactly one. Buckets are an axis **separate** from
the funnel, not a refinement of it: a `tactic_junk_body` can be admissible, and an
`exemplar_substitution` is well-formed Lean that never answers the task. The cross-tab of bucket
against admissibility is the readable object, not either alone.

A banned token reaching the output anyway is reported as a **leak count**, separately from the
buckets — it is a statement about whether the intervention was applied at all, not about what the
model chose.

## Interventions that must be verifiably present

Two failure modes here are silent, and both would read as "the intervention did not work":

1. **A ban with no resolved variants** makes T1 byte-identical to T0. Variants are resolved
   against the *served* tokenizer via `/tokenize`, their id sequences written to
   `scoring_output/battery_ban_resolution.json`, and a ban cell **refuses to run** without them.
2. **A prefill that never reaches the wire**, or that reaches it but is not re-attached to the
   stored completion, measures a prompt that was not run. Asserted in
   `tests/test_battery.py::test_prefill_reaches_the_wire_and_the_stored_completion`.

## Reading caveats fixed in advance

- **`WRONG_TYPE` is near-impossible by construction in T2/T3.** The prefill hands the model the
  pinned type, so their funnels must be read against T0/T1 with that in mind rather than as an
  improvement in type discipline.
- **The prefill removes the modifier slot.** A prefilled candidate cannot write `noncomputable`
  itself, so the splice ladder's retry is the only thing between a classical definition and a
  false compile error. Verified live before the run (see below).
- **Think-block presence is expected to fall in T2/T3**, since generation begins mid-declaration.
  Recorded per cell either way; either outcome is data.

## Pre-run checks, run against live Lean v4.32.2 before the pod was created

Both found real defects; both are fixed and tested.

1. **`@[reducible, reducible]` is a hard Lean error** — "failed to set `[reducible]`, `f` is not
   currently `[semireducible]`, but `[reducible]`". The prefill hands over the spliced header
   including `@[reducible]`, which scoring then applies again. Unfixed, 100% of T2/T3 candidates
   would have returned `compile_error` and it would have read as the intervention failing.
   `harness.signature.reducible_declaration` is now idempotent.
2. **Lean has two noncomputable messages, not one.** Only `consider marking it as 'noncomputable'`
   was matched; a body naming `Classical.choice` directly produces `consider marking definition as
   \`noncomputable\`` and never triggered the retry. Revises no past verdict — one record in the
   1,039-record tree carries the string and its real failure is a type mismatch — but it was a
   live gap, and load-bearing here for the reason above.

Confirmed after the fixes: prefill-shaped declarations splice and score admissible, and the
noncomputable retry fires through the prefill shape (`path=NONCOMPUTABLE`).
