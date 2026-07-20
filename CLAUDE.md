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

- Lean version: `v4.32.0` (newest stable Lean release, 2026-07-13). Chosen by checking
  lean-interact's *actual GitHub release notes* (not just its README table, which lagged) —
  0.11.5 (published 2026-07-16) added support for "v4.31.0-rc2 to v4.33.0-rc1", a range that
  covers v4.32.0 stable.
- Mathlib tag/commit: tag `v4.32.0` (its `lean-toolchain` file targets `leanprover/lean4:v4.32.0`
  exactly — verified before pinning). Pinned as an exact tag in `lean/lakefile.toml`, not a
  moving branch.
- lean-interact version: 0.11.5 (latest on PyPI as of setup; its supported-version range
  determined the Lean version choice above).
- Python: 3.12, managed with `uv`. `pyproject.toml` lives at the repo root (single-package
  repo, keeps `uv run` / `pytest` invocations simple); the `harness/` directory is the
  installable package itself (`packages = ["harness"]` in `[tool.hatch.build.targets.wheel]`).
- Lean subproject scaffolded via `lake init definition_verifier math` (named `definition_verifier`
  because the directory name `lean` is a reserved package name). The `math` template auto-pinned
  Mathlib to the exact matching tag and auto-ran a full Mathlib cache download as a side effect —
  worth knowing if re-scaffolding, since it's a multi-GB download with no separate warning.
  It also added GitHub Actions workflows (CI, auto-release-tagging, docs→Pages deploy) and a
  `weak.linter.mathlibStandardSet` style-linter (copyright headers, doc-strings) — both removed/
  disabled since Step 0 doesn't need CI and the Mathlib contributor style rules don't apply to
  our own files.

## Constraints

- No heavyweight deps (torch, transformers, etc.) at this stage.
- Prefer boring, standard choices. This is research infrastructure.
- If Lean/Mathlib/lean-interact versions conflict, lean-interact's supported version wins;
  document the decision here.
