# CLAUDE.md

Context for future sessions working on this repo.

## Who I am / how to work with me

- I am a mathematician, comfortable with math and Python, but **new to git, GitHub, and
  project tooling**. Explain what you're doing in a sentence or two before significant steps;
  briefly explain non-obvious commands.
- Commit early and often, short present-tense messages ("pin Lean toolchain", "add smoke
  test"). Push after each meaningful milestone.
- Ask before anything destructive (deleting files, force-pushing, amending pushed history).
  Never force-push.
- If something fails, show the error, explain it in plain language, propose a fix before
  applying it.
- `gh` CLI is used for GitHub operations. Verify `gh auth status` before creating remotes.

## Project

Building a **verifier for the faithfulness of Lean 4 definitions**. Autoformalization
systems can produce sorry-free proofs whose definitions still don't denote the intended
mathematical object — the Lean kernel only checks type-correctness, not intent. This project
builds a kernel-adjudicated signal for definitional faithfulness.

- A **task** = an informal dossier for a mathematical object + a **pinned Lean signature**
  (name and type; body is the hole a candidate fills) + a **two-sided fact suite** (concrete
  decidable statements checked via `decide`) + **mutant suites** (copies of the fact suite,
  each encoding one typed plausible misreading — boundary shifted, side condition dropped,
  inequality flipped — each containing at least one fact the true object refutes).
- Scoring: (0) admissibility gate (compiles against pinned signature, no `sorry` — REPL
  reports this as a *warning*, not an error — no new axioms, no dependency tampering),
  (1) fidelity = fraction of true fact suite certified, (2) separation = fraction of mutant
  suites refuted. Vacuous defs pass all facts but kill no mutants; empty defs kill all
  mutants but fail the facts. Only the intended object scores well on both.
- All checking runs through the **Lean REPL**, driven from Python via **LeanInteract**
  (`lean-interact` on PyPI, github.com/augustepoiroux/LeanInteract). Cold Mathlib import
  takes ~1 minute; the REPL holds a warm environment in memory after that, so each
  subsequent check takes seconds. The REPL can pickle a warmed environment to `.olean` for
  fast reload.
- CPU-only for now. No model training, no GPU code, no data mining yet.

## Current milestone: Step 0 (environment setup) — ONLY

Not to be started yet: hand-built n=1 task with known-answer verifier tests, admissibility
hardening pass, Mathlib mining pipeline, model experiments.

## Decisions / pinned versions

_Filled in as Step 0 progresses — see README.md "Pinned versions" and "Timings" sections,
which should stay in sync with this file._

- Lean version: TBD
- Mathlib tag/commit: TBD
- lean-interact version: TBD
- Python version / packaging layout: TBD

## Constraints

- No heavyweight deps (torch, transformers, etc.) at this stage.
- Prefer boring, standard choices. This is research infrastructure.
- If Lean/Mathlib/lean-interact versions conflict, lean-interact's supported version wins;
  document the decision here.
