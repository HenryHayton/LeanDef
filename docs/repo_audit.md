# Repository audit — definition-verifier

Read-only audit. No files modified, no git state changed. Snapshot as of the current working
tree (`git log --oneline` head: `9c63477 gitignore scratch/ for local-only calibration probes`,
clean `git status`).

---

## 1. Tree and purpose

Full tree (heavy/generated dirs collapsed; gitignore status noted per top-level entry):

```
.
├── .gitignore                      [tracked]
├── .python-version                 [tracked]
├── .pytest_cache/                  [gitignored — pytest cache]
├── .ruff_cache/                    [gitignored — ruff cache]
├── .venv/                          [gitignored — uv-managed virtualenv]
├── CLAUDE.md                       [tracked]
├── README.md                       [tracked]
├── docs/
│   └── README.md                   [tracked — placeholder, "# design notes"]
├── harness/
│   └── __init__.py                 [tracked]
├── lean/
│   ├── .gitignore                  [tracked]
│   ├── .lake/                      [gitignored — lake build artifacts, multi-GB]
│   ├── DefinitionVerifier/
│   │   └── Basic.lean              [tracked]
│   ├── DefinitionVerifier.lean     [tracked]
│   ├── README.md                   [tracked]
│   ├── lake-manifest.json          [tracked]
│   ├── lakefile.toml               [tracked]
│   └── lean-toolchain              [tracked]
├── lean.lock                       [gitignored — empty concurrency-control file created
│                                     by lean_interact.LocalProject next to lean/]
├── pickles/                        [gitignored — dir itself + contents]
│   └── mathlib_env.olean           [gitignored — pickled warm REPL env from smoke_test.py]
├── pyproject.toml                  [tracked]
├── scratch/                        [gitignored — entire directory, never pushed]
│   ├── n1_tau/
│   │   ├── README.md               [gitignored]
│   │   ├── score.py                [gitignored]
│   │   └── task.lean               [gitignored]
│   └── repo_audit.md               [gitignored — this report]
├── scripts/
│   ├── README.md                   [tracked — placeholder, "# one-off scripts"]
│   ├── __pycache__/                [gitignored]
│   └── smoke_test.py               [tracked]
├── tasks/
│   ├── README.md                   [tracked — placeholder, "# tasks"]
│   ├── handbuilt/
│   │   └── .gitkeep                [tracked — empty]
│   └── schema/
│       └── .gitkeep                [tracked — empty]
├── tests/
│   ├── __pycache__/                [gitignored]
│   ├── conftest.py                 [tracked]
│   ├── test_lean_repl.py           [tracked]
│   └── test_sanity.py              [tracked]
└── uv.lock                         [tracked]
```

`git ls-files` (23 tracked paths) matches the non-bracketed entries above exactly; `git status`
is clean (no untracked/modified files outside what's shown).

### Python files: purpose, public API, internal imports

**`harness/__init__.py`**
Purpose: package placeholder for the permanent verifier package. Currently contains only a
one-line module docstring (`"""Verifier for Lean 4 definitional faithfulness."""`) — no
functions, no classes, no logic. Imports: none. Imported by: nothing else in the repo imports
from `harness` (no code currently exercises this package at all; it exists only so
`pyproject.toml`'s `packages = ["harness"]` has something to point at).

**`scripts/smoke_test.py`**
Purpose: one-off, hand-run script proving the LeanInteract + pinned Lean/Mathlib project work
end to end (cold import, warm `decide`, splice pattern, `sorry`-as-warning detection,
environment pickling), and printing wall-clock timings that were copied into README's
"Timings" section.
Public functions:
- `timed(label: str, fn)` — generic instrumentation helper; runs `fn()`, prints/records
  elapsed wall time under `label` in the module-level `timings` dict, returns `fn()`'s result.
- `main() -> None` — runs the full smoke-test sequence described above.
Module-level data: `REPO_ROOT`, `LEAN_PROJECT_DIR`, `PICKLE_DIR` (all `pathlib.Path`),
`MAX_TOTAL_MEMORY = 0.95`, `timings: dict[str, float]`.
Imports from within the repo: **none**. Only external imports (`time`, `pathlib.Path`,
`psutil`, `lean_interact.*`). Not imported by any other file in the repo.

**`tests/conftest.py`**
Purpose: pytest fixture module. Provides a single session-scoped `AutoLeanServer` (bare Lean,
no Mathlib import) shared across the test session.
Public fixture: `lean_server()` — `@pytest.fixture(scope="session")`; builds
`LeanREPLConfig(project=LocalProject(directory=str(LEAN_PROJECT_DIR)))`, then
`AutoLeanServer(config, max_total_memory=0.95)`; yields the server; kills it on teardown.
Module-level data: `LEAN_PROJECT_DIR` (own independent re-derivation of the `lean/` path).
Imports from within the repo: none (only `pathlib`, `pytest`, `lean_interact`).

**`tests/test_lean_repl.py`**
Purpose: the two "known-answer" REPL-backed regression tests referenced in README's
definition of done.
Public functions (pytest test functions, consuming the `lean_server` fixture by name):
- `test_decide_proves_arithmetic(lean_server)` — asserts `example : (2 : Nat) + 2 = 4 := by decide`
  produces no errors.
- `test_sorry_is_reported_as_warning_not_error(lean_server)` — asserts
  `def mySorryDef : Nat := sorry` produces no errors, and that at least one warning message
  contains the substring `"sorry"`.
Imports from within the repo: none (only `lean_interact.Command`; the `lean_server` fixture is
picked up implicitly via pytest's conftest discovery, not an explicit import).

**`tests/test_sanity.py`**
Purpose: trivial harness-proving test (`assert True`), predates the REPL-backed tests.
Public function: `test_sanity()`. Imports: none.

**`archive/n1_tau/score.py`** (gitignored, not part of the permanent package)
Purpose: scores a battery of hand-written candidate bodies for `tau` (the divisor-counting
function) — the true definition, 7 mutants representing distinct categories of plausible
misreading, and a junk/vacuous candidate — against 7 positive exact-value facts, via a single
warm (Mathlib-imported) REPL session. This is the current, most-evolved iteration of the
calibration probe (superseding an earlier 3-candidate / 10-fact version from the same session).
Public function: `main() -> None` — the entire program; everything else is module-level data.
Module-level data:
- `REPO_ROOT`, `LEAN_PROJECT_DIR` (own independent re-derivation of the `lean/` path, 3
  `.parent` calls since this file is 2 directories deeper than `scripts/` or `tests/`),
  `MAX_TOTAL_MEMORY = 0.95`.
- `FACTS: list[str]` — 7 Lean `example ... := by decide` source strings.
- `CANDIDATES: dict[str, str]` — 9 entries (`"true"`, `"m1_proper_divisors"` … `"m7_sum_not_count"`,
  `"junk"`), each value a full `def tau : ℕ → ℕ := ...` source string.
- `PREDICTIONS: dict[str, list[bool]]` — 9 entries, hand-computed expected pass/fail per fact
  per candidate, used only for the prediction-vs-actual comparison printed at the end.
Imports from within the repo: **none** — despite the module docstring saying the
LeanREPLConfig/AutoLeanServer pattern was "copied [from `scripts/smoke_test.py`]... to keep
this scratch probe self-contained," there is no actual Python import connecting the two files;
the pattern is independently retyped. (Only external imports: `time`, `pathlib.Path`,
`lean_interact.*`.)

**`archive/n1_tau/task.lean`** (gitignored, not Python — included here for completeness since
it's the other executable artifact in the probe)
Purpose: one-time, hand-checked Lean source proving (a) the hand-written `tau` body agrees
with Mathlib's own `Nat.divisors` for `n < 40`, and (b) the original 10-fact suite (7 positive
+ 3 `≠`-refuting) all `decide` cleanly. Checked via `lake env lean ../archive/n1_tau/task.lean`
run from `lean/` — never added as a source file inside the `lean/` project itself.
Content: `def tau`, one `∀ n, n < 40 → ...` sanity-check `example`, 10 fact `example`s, plus
`def tau_mutant` (the single proper-divisor mutant only) and `def tau_junk`. **Note:** this
file was not updated when `score.py` was extended to 7 mutants — it still only reflects the
original 3-candidate probe. See §2 and §6 for the resulting drift.

---

## 2. Generic vs. τ-specific classification (`archive/n1_tau/`)

| Piece | Classification | Notes |
|---|---|---|
| REPL bootstrap (`LeanREPLConfig(project=LocalProject(...))`, `AutoLeanServer(config, max_total_memory=...)`) | **(a) generic** | Identical shape to `scripts/smoke_test.py` and `tests/conftest.py`. Ready to lift into `harness/` as e.g. a `get_server()` helper — but see hidden-assumption note on `MAX_TOTAL_MEMORY` below; the constant itself would need to become a parameter, not a copied literal. |
| Cold `import Mathlib` + reuse as shared base env for all candidates | **(a) generic** | The "import once, splice every candidate off the same base env" pattern is exactly the pipeline behavior a general scorer needs. No τ-specific content in this step. |
| Candidate splicing (`server.run(Command(cmd=def_body, env=base_env))`, checking `has_errors()`, taking `.env`) | **(a) generic mechanism, (b) specific payload** | The *act* of splicing is generic and directly promotable. The *payload* — `CANDIDATES`'s 9 literal `def tau : ℕ → ℕ := ...` strings — is τ-specific data. To separate: extract a function like `splice_candidate(server, base_env, name: str, type_sig: str, body: str) -> int` that builds the `def {name} : {type_sig} := {body}` string itself, so callers pass only `(name, type_sig, body)` as data rather than a pre-formatted string. Currently the name (`tau`) and type (`ℕ → ℕ`) are baked into every candidate string rather than factored out once. |
| `FACTS: list[str]` | **(b) τ-specific data** | Pure data about `tau`'s expected values at 7 inputs. Should become a fixture (e.g. a list of `(input, expected_value)` pairs or raw fact strings loaded from a task file), not inline in a scoring script. |
| `CANDIDATES: dict[str, str]` | **(b) τ-specific data**, mixed with **(a)** as above | The dict-of-labeled-bodies *shape* is generic (any task will have a true def + mutants + junk); the actual bodies are τ-specific. Separating requires the splice-template change above so bodies alone (not full `def ... :=` strings) are the stored data. |
| `PREDICTIONS: dict[str, list[bool]]` and the "prediction vs actual" comparison block | **(c) one-off scaffolding** | This exists only because a human hand-verified τ's arithmetic before running the probe, specifically to sanity-check *this one calibration exercise*. A general pipeline scoring mined/unknown candidates has no "predicted" answer to compare against by construction. Could in principle be repurposed as a golden-output regression test for `tau` specifically, but as written it's calibration scaffolding, not pipeline infrastructure. |
| Fact-checking loop (`for fact in FACTS: server.run(Command(cmd=fact, env=candidate_env)); passed.append(not fact_resp.has_errors())`) | **(a) generic** | Directly promotable as-is (modulo the admissibility gap noted in §3/§4 — it only checks `has_errors()`, nothing else). |
| Results table / fidelity computation / "candidates passing ALL facts" / per-fact discrimination tally | **(a) generic reporting** | None of this printing logic references `tau` by name or assumes anything τ-specific beyond consuming `FACTS`/`CANDIDATES`/`results` as generic-shaped data. Directly promotable to a `harness.report` module. |
| Timing instrumentation (`wall_start`, `fact_check_times`, cold-import timing) | **(a) generic** | Same shape as `scripts/smoke_test.py`'s `timed()` helper, reimplemented ad hoc rather than reused. |
| `task.lean` (entire file) | **(b) τ-specific data / one-time validation artifact** | Not read by any other code at runtime; it's a standalone, manually-run Lean source file. Its role (proving the fact suite `decide`s cleanly, and that the hand-written body agrees with Mathlib's library definition) is a real and reusable *pattern* for a general pipeline's pre-flight check, but the file itself is 100% τ-specific content, and it's now out of sync with `score.py` (see §6). |

**Summary of what would need to change to fully separate (a) from (b)/(c):**
1. Introduce a splice function parameterized by `(name, type_sig, body)` instead of storing
   pre-formatted `def name : type := body` strings as the data.
2. Move `FACTS` and `CANDIDATES`' bodies (not the def-strings) into a data fixture format
   (e.g. one file per task) separate from the scoring code.
3. Extract the REPL-bootstrap + splice + fact-check + report loop out of `main()` into
   reusable functions in `harness/`, with `MAX_TOTAL_MEMORY`, `LEAN_PROJECT_DIR`, and timeout
   values passed in rather than hardcoded module constants.
4. Drop or clearly separate the `PREDICTIONS` comparison — it's calibration-only and has no
   place in a pipeline that scores candidates with unknown correctness.

---

## 3. The harness contract (as currently implemented, `archive/n1_tau/score.py`)

**Splice template — quoted verbatim** (`archive/n1_tau/score.py`, `CANDIDATES` dict):

```python
CANDIDATES: dict[str, str] = {
    "true": "def tau : ℕ → ℕ := fun n => ((Finset.Icc 1 n).filter (· ∣ n)).card",
    "m1_proper_divisors": "def tau : ℕ → ℕ := fun n => ((Finset.Icc 1 (n - 1)).filter (· ∣ n)).card",
    "m2_include_zero": "def tau : ℕ → ℕ := fun n => ((Finset.range (n + 1)).filter (· ∣ n)).card",
    "m3_strict_bound": "def tau : ℕ → ℕ := fun n => ((Finset.Ico 1 n).filter (· ∣ n)).card",
    "m4_off_by_one_up": "def tau : ℕ → ℕ := fun n => ((Finset.Icc 1 (n + 1)).filter (· ∣ n)).card",
    "m5_multiples_confusion": "def tau : ℕ → ℕ := fun n => ((Finset.Icc 1 n).filter (n ∣ ·)).card",
    "m6_count_primes": (
        "def tau : ℕ → ℕ := fun n => ((Finset.Icc 1 n).filter (fun d => d ∣ n ∧ Nat.Prime d)).card"
    ),
    "m7_sum_not_count": "def tau : ℕ → ℕ := fun n => ((Finset.Icc 1 n).filter (· ∣ n)).sum id",
    "junk": "def tau : ℕ → ℕ := fun _ => 0",
}
```

There is **no separate template** — each dict value is a complete, literal, ready-to-send Lean
`def` statement. Nothing is interpolated at runtime; the name `tau` and the type `ℕ → ℕ` are
typed out identically in all 9 entries.

**Splicing mechanism — quoted verbatim** (`archive/n1_tau/score.py`, inside `main()`):

```python
base_resp = server.run(Command(cmd="import Mathlib"))
assert not base_resp.has_errors(), base_resp.messages
base_env = base_resp.env
...
for label, def_body in CANDIDATES.items():
    def_resp = server.run(Command(cmd=def_body, env=base_env))
    assert not def_resp.has_errors(), f"candidate {label!r} failed to even compile: {def_resp.messages}"
    candidate_env = def_resp.env

    passed = []
    for fact in FACTS:
        t_fact = time.perf_counter()
        fact_resp = server.run(Command(cmd=fact, env=candidate_env))
        fact_check_times.append(time.perf_counter() - t_fact)
        passed.append(not fact_resp.has_errors())
    results[label] = passed
```

So: one `import Mathlib` command establishes `base_env` (a single `CommandResponse.env` int);
every candidate is spliced as its own `Command(cmd=def_body, env=base_env)`, forking a fresh
`candidate_env` off the same immutable base; every fact is then run as
`Command(cmd=fact, env=candidate_env)`.

**Pinned signature representation:** not represented as data at all. There is no
`PinnedSignature` object, no separate name/type fields — the signature (`tau : ℕ → ℕ`) exists
only as a substring inside each of the 9 hand-typed `CANDIDATES` values. Changing the pinned
name or type means editing all 9 strings by hand.

**`sorry`/axiom/admissibility checks — where performed:** **nowhere in the scoring path.**
Both the candidate-splice step and every fact-check step check only
`response.has_errors()` — a boolean derived from whether any `Message.severity == "error"`.
Neither `response.get_warnings()` nor `response.sorries` is ever inspected in
`archive/n1_tau/score.py`, and no command resembling `#print axioms tau` is ever sent. This
means:
- If a spliced candidate body contained `sorry`, `has_errors()` would still be `False` for the
  splice step (sorry is a warning, not an error, as already proven in `scripts/smoke_test.py`
  and `tests/test_lean_repl.py`), so the candidate would proceed to be scored. In practice a
  `sorry`-containing definition can't be reduced by `decide` (which needs a computable value),
  so downstream fact checks would likely fail with kernel-reduction errors rather than silently
  succeeding — but this is incidental, not an enforced admissibility gate.
- No axiom-introduction check exists anywhere in the codebase outside the general REPL-warning
  proof-of-capability in `scripts/smoke_test.py`/`tests/test_lean_repl.py`. The admissibility
  gate described in `CLAUDE.md`/`README.md` ("no `sorry`... no new axioms, no dependency
  tampering") is **fully unimplemented** in the actual scoring code; only the *capability* to
  detect a `sorry` warning has been proven in isolation, never wired into `score.py`'s loop.

**Fact representation:** plain Python strings — raw Lean source text, e.g.
`"example : tau 1 = 1 := by decide"`. No structured representation (no separate
input/expected-value fields, no fact IDs, no metadata). `FACTS` is a flat `list[str]`; pairing
a fact with its outcome is purely positional (`results[label][i]` corresponds to `FACTS[i]`).
(An earlier iteration of this same file, superseded by the current version, used
`list[tuple[str, bool]]` with an `is_refuting` flag — that structure has since been dropped
along with the refuting facts themselves.)

**Raw result shape before scoring:** each `server.run(Command(...))` call returns a
`lean_interact.interface.CommandResponse` (a pydantic model), with (per the installed
`lean_interact` package) fields including `env: int`, `messages: list[Message]` (each
`Message` having `severity: Literal["error","warning","info","trace"]`, `data: str`,
`start_pos`/`end_pos`), and `sorries: list[Sorry]`, plus methods `.has_errors()`,
`.get_errors()`, `.get_warnings()`. `score.py` reduces every response to a single `bool`
(`not response.has_errors()`) and discards the rest — no messages, positions, or sorry data
are retained past the immediate check.

---

## 4. Hidden assumptions (what a general pipeline would need to parameterize)

- **Name**: `"tau"` is hardcoded as a literal substring inside every `FACTS` and `CANDIDATES`
  string (18 occurrences total across the two lists) — not a variable anywhere.
- **Type**: `"ℕ → ℕ"` is likewise hardcoded inline in all 9 `CANDIDATES` def-strings.
- **Import list**: exactly the single literal string `"import Mathlib"`, hardcoded identically
  in `scripts/smoke_test.py` and `archive/n1_tau/score.py` (and implicitly assumed-absent in
  `tests/conftest.py`, which deliberately never imports Mathlib). No support for a
  task-specific or partial import list.
- **Timeouts**: no call site anywhere in the repo (`scripts/smoke_test.py`,
  `tests/conftest.py`, `archive/n1_tau/score.py`) ever passes `timeout=` to `server.run(...)`
  or `LeanREPLConfig(...)`; every call relies on `lean_interact`'s library default
  (`DEFAULT_TIMEOUT = None`, i.e. no timeout). A hang blocks forever with no automatic
  recovery — which is exactly what was observed and had to be killed manually during the
  `archive/n1_tau/` mutant-battery run in this session.
- **`max_total_memory` (the `AutoLeanServer` guard)**: value `0.95` is duplicated as a literal
  in three places — `scripts/smoke_test.py` (`MAX_TOTAL_MEMORY = 0.95` constant),
  `tests/conftest.py` (inline `0.95` argument, no named constant), and
  `archive/n1_tau/score.py` (`MAX_TOTAL_MEMORY = 0.95` constant, independently declared). No
  shared config or environment variable.
- **Paths**: `LEAN_PROJECT_DIR` is independently re-derived in three files via a different
  number of `Path(__file__).resolve().parent...` hops depending on each file's own depth
  (`scripts/smoke_test.py`: `.parent.parent`; `tests/conftest.py`: `.parent.parent`;
  `archive/n1_tau/score.py`: `.parent.parent.parent`). No single source of truth for "where is
  the Lean project"; moving any of these files would silently break the path derivation.
- **Mathlib/toolchain pin locations**: Lean version lives in `lean/lean-toolchain`
  (`leanprover/lean4:v4.32.0`); Mathlib tag lives in `lean/lakefile.toml`'s
  `[[require]] rev = "v4.32.0"`, further resolved to exact commit
  `81a5d257c8e410db227a6665ed08f64fea08e997` in `lean/lake-manifest.json`. No code anywhere
  reads or asserts these values at runtime — `LeanREPLConfig(project=LocalProject(...))`
  simply infers the Lean version from whatever `lean/` currently contains, so a manual edit to
  either pin file would silently change what every script/test runs against.
- **`lean-interact` version**: pinned only transitively, via `uv.lock`'s resolved
  `version = "0.11.5"`. `pyproject.toml` itself declares the dependency as the bare string
  `"lean-interact"` with no version specifier — an `uv lock --upgrade` (or any lockfile
  regeneration) could silently move to a newer `lean-interact` release with no `pyproject.toml`
  diff to signal the change.
- **Fact/prediction positional coupling**: `archive/n1_tau/score.py`'s `FACTS` (list) and
  `PREDICTIONS` (dict of lists) must stay in exact positional sync by hand — there are no
  fact IDs, so editing one without the other would silently misalign predictions to facts.
- **`n < 40` bound**: hardcoded in `archive/n1_tau/task.lean`'s Mathlib-agreement sanity check
  (`∀ n, n < 40 → tau n = n.divisors.card`) — an arbitrary cutoff chosen only because it's
  `decide`-cheap, not derived from any config.
- **Splice shape**: both `task.lean` and `score.py` assume a candidate is always exactly one
  `def <name> : <type> := <single-expression-body>`. No support for multi-declaration
  candidates, auxiliary lemmas, `theorem`/`abbrev` signature kinds, or bodies requiring `by`
  tactic blocks rather than term-mode expressions.

---

## 5. Test suite

`pytest --collect-only -q` output (3 tests, 0 errors):

```
tests/test_lean_repl.py::test_decide_proves_arithmetic
tests/test_lean_repl.py::test_sorry_is_reported_as_warning_not_error
tests/test_sanity.py::test_sanity
```

What each asserts:
- **`test_sanity`**: `assert True` — proves the pytest harness itself runs; no REPL
  involvement.
- **`test_decide_proves_arithmetic`**: sends `example : (2 : Nat) + 2 = 4 := by decide`
  against a fresh (`env=None`) session on the shared bare-Lean `lean_server` fixture; asserts
  `not response.has_errors()`.
- **`test_sorry_is_reported_as_warning_not_error`**: sends `def mySorryDef : Nat := sorry`;
  asserts `not response.has_errors()` **and** that `response.get_warnings()` contains a
  message whose `.data` includes the substring `"sorry"`.

Both REPL-backed tests run against **bare Lean** (no `import Mathlib`), via the session-scoped
`lean_server` fixture in `tests/conftest.py`.

**Coupling to `archive/n1_tau/`: none.** No test imports, reads, or references anything under
`scratch/` — not `task.lean`, not `score.py`, not `tau`/mutants/facts. The fixture and both
tests are pure REPL-plumbing checks, entirely independent of the calibration probe's content.

**Consequence for the question "which tests would break if `archive/n1_tau/` were
restructured": none of the 3 current tests would break**, because none of them touch it. The
inverse point is more load-bearing for planning: if `archive/n1_tau/`'s splice/fact-check/
report logic is later promoted into `harness/`, **no existing test would catch a regression**
in that promoted logic — there is currently zero test coverage for candidate-splicing,
fact-scoring, or mutant-discrimination behavior; that logic exists today only in the untested,
non-pytest `archive/n1_tau/score.py` script.

---

## 6. Dependencies and environment

**Python dependencies actually imported** (by grep across all `.py` files, tracked and
gitignored):
- `lean_interact` — `AutoLeanServer`, `Command`, `LeanREPLConfig`, `LocalProject`,
  `PickleEnvironment`, `UnpickleEnvironment` (only in `scripts/smoke_test.py`), and
  `lean_interact.utils.get_total_memory_usage` (only in `scripts/smoke_test.py`).
- `psutil` — only in `scripts/smoke_test.py`, for REPL-process RSS measurement.
- `pytest` — test discovery/fixtures (`tests/conftest.py`).
- Stdlib only elsewhere: `time`, `pathlib.Path`.
- `ruff` is declared in `pyproject.toml`'s dependency list but **never imported** by any
  Python file — it's used only as a CLI tool (`uv run ruff check .`).

**`uv.lock` resolves 27 packages total.** Beyond the direct deps above, the rest are
transitive: `pydantic`/`pydantic-core` (lean_interact's response models), `gitpython`/
`gitdb`/`smmap` (lean_interact's REPL git-repo management), `filelock` (lean_interact's
concurrency locks), `requests`/`urllib3`/`idna`/`charset-normalizer`/`certifi` and `rich`/
`pygments`/`markdown-it-py`/`mdurl`/`tqdm`/`colorama` (lean_interact utilities/CLI output),
`packaging`, `annotated-types`/`typing-extensions`/`typing-inspection` (pydantic transitive),
`iniconfig`/`pluggy` (pytest transitive).

**`lean-interact` version**: `0.11.5`, pinned only via `uv.lock`'s resolved version.
`pyproject.toml` declares it unpinned (bare `"lean-interact"` string).

**Toolchain/Mathlib pin locations** (see also §4):
- Lean: `lean/lean-toolchain` → `leanprover/lean4:v4.32.0`
- Mathlib: `lean/lakefile.toml` → `rev = "v4.32.0"`, resolved in `lean/lake-manifest.json` →
  commit `81a5d257c8e410db227a6665ed08f64fea08e997`.

**README staleness relative to actual code/history:**
- README's "Timings" table reflects only the *first* of two `scripts/smoke_test.py` runs
  performed during the Step-0 verification pass (cold import 141.7s / unpickle 138.2s). A
  second run (161.4s / 133.5s) is documented only in `CLAUDE.md`'s "Known follow-ups" section,
  not reflected in README — so README currently understates the unpickle-speed uncertainty
  that CLAUDE.md itself flags as unresolved.
- README's "Layout" section doesn't mention `scratch/` — expected and correct by design (the
  user's own instruction was that scratch content must never be presented as project content),
  not a bug, but noted here for completeness since this audit does cover `scratch/`.
- `archive/n1_tau/README.md` (not the root README) is stale relative to its own directory's
  content: it states `score.py` "scores the three candidates (true/mutant/junk)," but the
  current `score.py` scores **9** candidates (true + 7 mutants + junk). This file was not
  updated when `score.py` was extended.
- `archive/n1_tau/task.lean` is stale relative to `score.py` for the same reason: it only
  defines `tau_mutant` (the single proper-divisor mutant, equivalent to `score.py`'s
  `m1_proper_divisors`) and `tau_junk`; it has no Lean-side counterpart for `m2`–`m7`. The two
  files were kept in sync manually for the first probe iteration and have since diverged —
  `task.lean`'s one-time `lake env lean` validation no longer covers most of what `score.py`
  currently scores.
- `CLAUDE.md`'s "Current milestone: Step 0 (environment setup) — ONLY" section is accurate as
  written (Step 0 work is what's tracked there) but doesn't acknowledge that
  `archive/n1_tau/` calibration work has since happened in the same session — this is by
  design (scratch content is deliberately excluded from `CLAUDE.md`'s project narrative per
  explicit instruction), not a defect, but worth naming here since a reader of `CLAUDE.md`
  alone would have no record that this probe exists.

---

## 7. Observations

Everything below is a description of the current state, not a recommendation to act — no
changes were made.

1. **The admissibility gate described in the project's own README/CLAUDE.md
   ("no `sorry`, no new axioms, no dependency tampering") is not implemented anywhere in the
   scoring path.** `archive/n1_tau/score.py` checks only `has_errors()`. The capability to
   detect a `sorry` warning exists and is tested (`scripts/smoke_test.py`,
   `tests/test_lean_repl.py`), but it's never called from the scoring loop. No code checks for
   introduced axioms at all (no `#print axioms` or equivalent, anywhere).
2. **No timeout is set on any REPL call anywhere in the repo.** This is a live risk, not a
   hypothetical one — a genuine multi-minute hang occurred during this session's
   `archive/n1_tau/` work and required manually killing the process; nothing in the codebase
   would have recovered from it automatically.
3. **`archive/n1_tau/task.lean` and `archive/n1_tau/score.py` have drifted out of sync.**
   `task.lean` reflects an earlier, smaller iteration of the probe (1 mutant, 10 facts
   including 3 refuting facts) while `score.py` reflects the current iteration (7 mutants, 7
   facts, no refuting facts). Nothing enforces or checks consistency between them; there is no
   programmatic link between the two files at all — `score.py` never reads `task.lean`.
4. **`archive/n1_tau/README.md` is stale** (says "three candidates," actual is nine) — a
   direct consequence of point 3.
5. **The pinned signature (`tau : ℕ → ℕ`) is duplicated as a literal substring 9 times** in
   `CANDIDATES` rather than factored out once, meaning any future signature change requires
   editing every candidate string by hand and is easy to get inconsistent.
6. **`LEAN_PROJECT_DIR` is independently re-derived (with a different `.parent` chain) in three
   separate files** (`scripts/smoke_test.py`, `tests/conftest.py`, `archive/n1_tau/score.py`)
   rather than sourced from one place — moving any of those files would silently break its
   path derivation without any error until the next run.
7. **`MAX_TOTAL_MEMORY = 0.95` is duplicated in three places** rather than centralized, and
   `CLAUDE.md`'s own "Known follow-ups" section already flags this value as something to "dial
   back down later" — currently there is no single place to do that dialing.
8. **`lean-interact`'s version is unpinned in `pyproject.toml` itself** (only pinned via the
   generated `uv.lock`), so the intent to pin it (documented prominently in `CLAUDE.md` and
   README) is not enforced by the dependency declaration a reader would look at first.
9. **README's "Timings" table reflects only one of the two `scripts/smoke_test.py` runs**
   performed during the Step-0 verification pass; the second run's numbers (and the
   still-unresolved "is unpickling actually fast" question) live only in `CLAUDE.md`, creating
   a split-source-of-truth for timing data.
10. **`harness/` is currently empty of any implementation** — a single docstring, no functions,
    no classes, nothing importable beyond the bare package. All working REPL-interaction logic
    that exists today lives either in the disposable `archive/n1_tau/score.py` or the one-off
    `scripts/smoke_test.py`, neither of which is imported by `harness/` or vice versa.
