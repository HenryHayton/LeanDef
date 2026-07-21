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
  (name and type; body is the hole a candidate fills) + a **two-sided fact suite** + **mutant
  suites** (copies of the fact suite, each encoding one typed plausible misreading — boundary
  shifted, side condition dropped, inequality flipped — each containing at least one fact the
  true object refutes). The fact suite is **not** decidable statements checked via `decide` in
  general — see `docs/design/reward_structure_2026-07-21.md` §2 for the design of record:
  three fact types (decidable casework, membership facts, global theorem facts), the latter
  two adjudicated by a kernel-checking LLM prover agent wherever finiteness/decidability runs
  out (e.g. a compactness-style property on an infinite carrier has almost no decidable facts
  at all). `decide` dominates only for cheap, casework-rich objects like this repo's one
  worked example (the divisor function τ, `archive/n1_tau/`) — that example is not
  representative of the target task distribution and must not be read as "facts are decide
  checks."
- Scoring: (0) admissibility gate (compiles against pinned signature, no `sorry` — REPL
  reports this as a *warning*, not an error — no new axioms, no dependency tampering),
  (1) fidelity = fraction of true fact suite certified, (2) separation = fraction of mutant
  suites refuted. Vacuous defs pass all facts but kill no mutants; empty defs kill all
  mutants but fail the facts. Only the intended object scores well on both.
- Mining candidate definitions from Mathlib uses **gates-then-preference-score selection**,
  not a weighted sum: see `docs/design/definition_selection_2026-07-21.md` for the design of
  record (and its 22 July 2026 revision section for the post-batch-2 recalibration). Hard
  eligibility gates (theorem-mention floor, length band, docstring floor, dependency
  vocabulary tier, anti-plumbing name patterns, richness floor, non-`none` fact supply) define
  the includable set; a small preference score dominated by structural richness (a proxy for
  how many distinguishable ways a definition can be misread) orders every gate-survivor — there
  is no top-N cutoff; the manifest is exactly two populations, eligible (ranked, in full) and
  excluded (with the gate(s) that fired), and how many tasks to draw from the ranked list is a
  stage-2 consumption decision, not a mining parameter. This supersedes miner stage 1's single
  weighted score of quality/in-degree/dependency-footprint, which was found to select for
  fundamental, memorized-verbatim vocabulary rather than content worth training or evaluating
  on.
- All checking runs through the **Lean REPL**, driven from Python via **LeanInteract**
  (`lean-interact` on PyPI, github.com/augustepoiroux/LeanInteract). Cold Mathlib import
  takes ~1 minute; the REPL holds a warm environment in memory after that. Per-check cost
  after that point depends entirely on the fact's adjudication mechanism, not on the REPL
  being warm: decidable facts are milliseconds (kernel computation only), while global/
  membership facts requiring a genuine proof search go through the prover agent and cost
  seconds to minutes, per fact, with a real chance of UNKNOWN (neither direction proved in
  budget) rather than a fast answer. The REPL can pickle a warmed environment to `.olean` for
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
- `AutoLeanServer` refuses to run once system-wide memory usage is above `max_total_memory`
  (default 0.8 = 80%). Dev laptops sit above that from unrelated apps often enough that this
  needs raising (we use 0.95 in `scripts/smoke_test.py` and `tests/conftest.py`) — otherwise it
  restart-loops and raises `MemoryError` before even trying. Real Mathlib-import memory use was
  ~2.5 GB RSS in our one measurement.
- `lean_interact.LocalProject` creates an empty concurrency-control lock file as a sibling of
  the project directory (`lean.lock` next to `lean/`, not to be confused with `uv.lock`).
  Gitignored via `/lean.lock`.
- The pytest-facing tests (`tests/test_lean_repl.py`) deliberately skip `import Mathlib` — the
  two required known-answer checks (`decide` on arithmetic, `sorry`-as-warning) don't need it,
  and skipping keeps `uv run pytest` fast (~18s) rather than 2+ minutes per run. Full
  Mathlib-environment behavior (cold import, warm checks, splice pattern, pickling) is what
  `scripts/smoke_test.py` exercises separately — see README "Timings".

## Known follow-ups (from 2026-07-20 verification pass)

- **Dial the `AutoLeanServer` memory guard back down.** It's currently raised to
  `max_total_memory=0.95` in `scripts/smoke_test.py` and `tests/conftest.py` (default is
  `0.8`) because this dev machine regularly sits above 80% system memory used from unrelated
  apps. Revisit once on a machine with more headroom, or before the guard's protection
  actually matters (e.g. running many REPL sessions at once).
- **Lean v4.32.0's support status is not unambiguously confirmed.** lean-interact 0.11.5's own
  bundled README (installed with the package, in `*.dist-info/METADATA`) states support for
  "all Lean versions between `v4.8.0-rc1` and `v4.32.0-rc1`" — note the upper bound is the
  release candidate, not the `v4.32.0` stable release we pinned. Separately, 0.11.5's GitHub
  release notes say it "added support for v4.31.0-rc2 to v4.33.0-rc1," which would cover
  v4.32.0 stable — but that's the changelog, not the shipped docs, and the two sources
  disagree. In practice `lake build` and every REPL check in `scripts/smoke_test.py` and
  `tests/` pass cleanly against v4.32.0, so it works; it just isn't stated as supported by the
  package's own installed documentation. Worth watching for lean-interact updates that
  explicitly bump the stated ceiling.
- **Environment unpickling has not yet been shown to be fast.** Two independent full runs of
  `scripts/smoke_test.py` (2026-07-20) both show unpickle time in the same order of magnitude
  as the cold `import Mathlib` (run 1: 138.2s unpickle vs 141.7s cold import; run 2: 133.5s vs
  161.4s). Both runs were on a machine under real memory pressure (~87% system memory used,
  ~2.1–2.4 GB free), so this may be disk-swapping overhead rather than something intrinsic to
  the pickle mechanism — but that's unconfirmed. If pickling's speed matters for a later
  milestone, re-run `scripts/smoke_test.py` on a quiet machine (most other apps closed) before
  relying on it, or investigate further.

## Constraints

- No heavyweight deps (torch, transformers, etc.) at this stage.
- Prefer boring, standard choices. This is research infrastructure.
- If Lean/Mathlib/lean-interact versions conflict, lean-interact's supported version wins;
  document the decision here.
