# Harvest Batch 4 Review — "Wide Mine"

Human-readable review of the fourth mechanical harvest (`miner/output/harvest_manifest.jsonl`). This batch's purpose is **measurement**, not selection improvement: `TARGET_MODULES` was expanded into a much wider slice of Mathlib to see what composition statistics (gate attrition, vocabulary-exclusion shape, richness/supply distribution, and a new tier-2 discharge measurement) look like at roughly 3x the corpus size — while the selection machinery itself (every gate, every threshold, the preference score, curation) was **frozen for this run**. Every number below reflects that frozen machinery applied to a bigger corpus; nothing in `miner/gates.py`, `miner/rank.py`, `miner/richness.py`, `miner/proxies.py`, or `miner/config.py`'s gate thresholds changed. The one piece of new code this batch adds is `miner/discharge.py`, the tier-2 discharge measurement itself — new capability, not a change to anything that already existed.

## 0. Corpus scope expansion

`TARGET_MODULES` (`miner/config.py`) grew from the batch-2/3 corpus (964 scanned hits: the original five corners plus batch 2's widening into Order/Algebra/Combinatorics/NumberTheory "basics") to the following, in addition to everything already scanned:

- **Full `Mathlib/Order/`** (was: 13 individual batch-2 files/subdirs — now the whole subtree; the old entries were removed, not left redundant, to avoid double-scanning the files they already covered).
- **Full `Mathlib/Combinatorics/`** (same treatment — was 11 individual batch-2 entries, now the whole subtree).
- **Broad `Mathlib/Algebra/`**: top-level files only (not subdirectories) of `Group/`, `Ring/`, `Field/`, `BigOperators/`, `Module/`. `Algebra/GroupPower/` was also requested but **does not exist in this pinned Mathlib version** (the concept has been reorganized into `Group`/`Monoid` infrastructure upstream since Mathlib 3) — skipped, not substituted.
- **Deeper `Mathlib/NumberTheory/`**: `Primorial.lean` (new) and `Padics/` top-level files (new). `Divisors.lean` and `ArithmeticFunction/` were already fully scanned since batch 2 — reaffirmed, not expanded.
- **`Mathlib/Topology/` core**: `Basic.lean`, `Order/` top-level files, and the full (flat, no-subdirectory) `Separation/`, `Connected/`, `Compactness/` directories. "Compactness-related files" was read as the `Topology/Compactness/` directory specifically (Compact.lean, LocallyCompact.lean, SigmaCompact.lean, CountablyCompact.lean, Paracompact.lean, and three more) rather than every file with "compact" in its name across all of `Topology/` (which would have pulled in category-theory and continuous-map-space material far past "core") — a judgment call, flagged here.
- **`Mathlib/Analysis/SpecialFunctions/` basics only**: the 24 top-level files, excluding the `Complex/`, `Gamma/`, `Gaussian/`, `Log/`, `Pow/`, `Trigonometric/` subdirectory trees.
- **Full `Mathlib/Dynamics/`** (new, 34 files).
- **`Mathlib/Data/Set/` core**: read as top-level files only (40 files), excluding the `Card/`, `Finite/`, `Lattice/`, `Pairwise/`, `Pointwise/` subdirectories — "core" is not a term the design doc or existing config uses elsewhere, so this is an interpretation, flagged as a judgment call.
- **Data completions**: full `Rat/`, `Multiset/`, `Sym/`, `Fin/`, `Bool/`, `Prod/`, `Sum/`, `Option/`; `Real/` "top-level" — which turns out to be identical to "full", since `Data/Real/` has no subdirectories at all in this Mathlib version (12 flat files).
- **`Logic/Relation` and `Logic/Function/`**: requested, but **already a no-op** — the bare `"Logic"` entry has scanned this recursively since batch 1. Nothing added.

### Dry-scan (pure text scan, no REPL) — file and candidate counts per territory

| Territory | Files | Candidates (`def` hits) |
|---|---|---|
| Original corpus (unchanged) | 320 | 830 |
| Order (full) | 312 | 957 |
| Combinatorics (full) | 194 | 605 |
| Data completions (Rat/Real/Multiset/Sym/Fin/Bool/Prod/Sum/Option) | 100 | 272 |
| Algebra/Ring (top-level) | 44 | 110 |
| Topology core | 78 | 101 |
| Algebra/Group (top-level) | 32 | 92 |
| Data/Set (core, top-level) | 41 | 81 |
| Dynamics (full) | 34 | 38 |
| NumberTheory additions (Primorial + Padics top-level) | 13 | 36 |
| Algebra/Module (top-level) | 31 | 36 |
| Analysis/SpecialFunctions (basics) | 24 | 18 |
| Algebra/BigOperators (top-level) | 15 | 7 |
| Algebra/Field (top-level) | 16 | 2 |
| **Total** | **1,254** | **3,185** |

3,185 is well under the ~8,000 threshold that would have triggered the "report the breakdown and proceed anyway, overnight accepted" clause — no overnight framing was needed, but the run was still multi-hour.

**Wall-clock estimate vs. actual.** At the established ~800/43min rate (≈3.23s/candidate), 3,185 candidates projected to ≈170 minutes (2.8 hours). Actual harvest runtime (scan → verify-with-recovery → gate → rank, all combined): **9,435.5s (157.3 minutes, 2.6 hours)** — within the estimate despite two mid-run environment-death recoveries (see §7).

## 1. Corpus counts

- Scanned: 3,185
- Verified (elaborates): 3,145
- Does not elaborate: 40
- Eligible (passed every gate, pre-curation): 727
- Curation-excluded (of the gate-eligible pool): 1 (`Nat.digitsAux1` — independently gate-excluded too this round as well, so curation contributes zero net change to the eligible count)
- **Net eligible after curation: 727**

For comparison, batch 3 (revision 2): 964 scanned → 950 verified → 256 eligible. The corpus grew 3.3x (964→3,185); the eligible set grew 2.84x (256→727) — a slightly lower yield density than the original+batch-2 corpus, consistent with much of the new territory (Order, Topology, Analysis) being more abstract/structural, with correspondingly higher `dependency_vocabulary` and `richness_floor` attrition (see §3, §4).

## 2. Gate-attrition table (sequential, established format)

Start: 3,145 verified candidates. Every gate is evaluated for every candidate regardless of earlier failures (per `miner.gates.evaluate_gates`); this table is sequential (each row's "fails" is of those that survived every prior row), matching the established format.

| Gate | Fails (of those reaching it) | Cumulative survivors |
|---|---|---|
| (a) theorem_mention_floor | 1,365 | 1,780 |
| (b) length_band | 93 | 1,687 |
| (c) docstring_floor | 50 | 1,637 |
| (d) dependency_vocabulary | 386 | 1,251 |
| (e) anti_plumbing | 11 | 1,240 |
| (g) richness_floor | 513 | 727 |
| (f) fact_supply | 0 | 727 |
| **eligible (pre-curation)** | | **727** |
| curation-excluded | 1 (already gate-excluded, net 0) | **727 net eligible** |

`fact_supply` fails 0 candidates reaching it, exactly as design doc §3(f) predicted ("expected to rarely bind, since gate (a) alone... already implies some global-fact supply for almost every survivor") — unchanged from batch 3's own observation.

## 3. Per-territory yield table (headline deliverable)

Scanned / verified / eligible, and each territory's top-3 killing gates by fail count, sorted by scanned size:

| Territory | Scanned | Verified | Eligible | Top-3 killing gates |
|---|---|---|---|---|
| Order (full) | 957 | 948 | 199 | theorem_mention_floor (474), richness_floor (422), fact_supply (317)* |
| Original corpus (unchanged) | 830 | 816 | 212 | theorem_mention_floor (350), richness_floor (300), fact_supply (200)* |
| Combinatorics (full) | 605 | 601 | 139 | richness_floor (273), theorem_mention_floor (239), dependency_vocabulary (186) |
| Data completions | 272 | 264 | 79 | richness_floor (100), theorem_mention_floor (92), fact_supply (53)* |
| Algebra/Ring (top-level) | 110 | 109 | 13 | richness_floor (71), theorem_mention_floor (51), fact_supply (37)* |
| Topology core | 101 | 101 | 2 | dependency_vocabulary (63), richness_floor (54), theorem_mention_floor (48) |
| Algebra/Group (top-level) | 92 | 88 | 18 | richness_floor (59), theorem_mention_floor (35), fact_supply (28)* |
| Data/Set (core, top-level) | 81 | 81 | 43 | richness_floor (29), theorem_mention_floor (17), dependency_vocabulary (13) |
| Dynamics (full) | 38 | 38 | 8 | richness_floor (16), dependency_vocabulary (14), theorem_mention_floor (14) |
| NumberTheory additions | 36 | 36 | 10 | richness_floor (15), dependency_vocabulary (11), theorem_mention_floor (6) |
| Algebra/Module (top-level) | 36 | 36 | 1 | theorem_mention_floor (27), fact_supply (26)*, richness_floor (18) |
| Analysis/SpecialFunctions | 18 | 18 | 2 | richness_floor (15), dependency_vocabulary (9), theorem_mention_floor (8) |
| Algebra/BigOperators (top-level) | 7 | 7 | 1 | dependency_vocabulary (5), length_band (3), theorem_mention_floor (2) |
| Algebra/Field (top-level) | 2 | 2 | 0 | theorem_mention_floor (2), fact_supply (2)*, richness_floor (1) |

*These are **independent** per-gate fail counts (each gate evaluated against every verified candidate in that territory, regardless of other gates), not sequential — a candidate failing `richness_floor` almost always also fails `fact_supply` (a richness-zero definition is reliably an unscoreable pure delegation too), so `fact_supply`'s high independent count in some rows is substantially the same population `richness_floor` already caught, not an additional 300+ genuinely distinct exclusions. Flagged here rather than presented without comment, since a reader skimming raw counts could otherwise double-count this population.

**Reading the table**: `Topology core`'s near-total exclusion (2 of 101 eligible, 2.0% yield — by far the lowest of any territory) is dominated by `dependency_vocabulary`, not richness or mention-count — Topology infrastructure depends heavily on other Topology/order/filter machinery that (before this batch) was never on `COMMON_VOCABULARY_MODULES` at all. `Algebra/Field` and `Algebra/BigOperators` (top-level) are vanishingly small territories in candidate terms (2 and 7 scanned respectively) — most of `Field/`'s and `BigOperators/`'s actual content lives in their (excluded, per this task's "top-level only" scope) subdirectories.

## 4. Vocabulary-gate exclusions grouped by missing-module kind

646 candidates failed `dependency_vocabulary` (an independent, all-candidates count; 386 of these are the *first* gate they failed, per the sequential table in §2 — the remaining 260 failed it in addition to an earlier gate). For each, every referenced constant that resolved to a real Mathlib module outside `COMMON_VOCABULARY_MODULES` was attributed to that module's top-level directory:

| Missing-module kind | Count |
|---|---|
| Algebra (non-whitelisted corners, e.g. `Algebra/AddConstMap/`, `Algebra/Module/Congruence/`) | 184 |
| Data (non-whitelisted corners, e.g. `Data/Fintype/`, `Data/Seq/`, `Data/QPF/`) | 180 |
| Combinatorics (e.g. `Combinatorics/Quiver/`, `Combinatorics/Young/`) | 140 |
| Topology | 107 |
| CategoryTheory | 89 |
| Analysis | 38 |
| Computability | 33 |
| NumberTheory | 24 |
| AlgebraicTopology | 23 |
| Dynamics | 11 |
| RingTheory | 6 |
| Control | 5 |
| LinearAlgebra | 5 |
| AlgebraicGeometry | 3 |
| SetTheory | 3 |
| Geometry | 2 |
| GroupTheory | 2 |
| MeasureTheory | 1 |

As expected ("expect this list to be large in Topology/, Analysis/ — that is data, not failure"): Topology and Analysis together account for 145 exclusions, and CategoryTheory (which nothing in this batch's expansion targeted directly, but which Order/Combinatorics/Topology candidates reach into constantly for categorical structure) is a genuine surprise entry at 89 — the single largest missing-module kind *not* explicitly requested by this task.

The single most common **exact** missing module is `Data/Fintype/Defs.lean` (41 occurrences) — `Fintype` is pervasive across the whole widened corpus (finite-type reasoning shows up in Order, Combinatorics, and Data alike) and is not on `COMMON_VOCABULARY_MODULES` at all. `Topology/Defs/Basic.lean` (56) and `CategoryTheory/Sites/Pretopology.lean` (33) are the next largest. Per the design doc's own standing note ("expected to keep growing empirically, corner by corner"), `Data/Fintype` in particular reads as a strong, low-risk candidate for the *next* vocabulary-list widening — not made here, since this run's machinery is frozen, but recorded as the clearest actionable finding this section produced.

## 5. Return-shape and supply-tier composition per territory

Overall eligible set (727):

| Shape | Count |
|---|---|
| value | 452 |
| prop | 183 |
| bundled | 92 |

Per territory (eligible only; territories with 727 total; smallest four omitted, single digits each, see raw manifest):

| Territory | n | value | prop | bundled | casework rich | membership rich/thin | global rich/thin |
|---|---|---|---|---|---|---|---|
| Original corpus | 212 | 129 | 43 | 40 | 41 | 5 / 99 | 155 / 57 |
| Order (full) | 199 | 107 | 74 | 18 | 0 | 0 / 113 | 124 / 75 |
| Combinatorics (full) | 139 | 96 | 39 | 4 | 7 | 0 / 77 | 99 / 40 |
| Data completions | 79 | 55 | 6 | 18 | 1 | 1 / 31 | 54 / 25 |
| Data/Set (core) | 43 | 29 | 11 | 3 | 0 | 0 / 41 | 37 / 6 |
| Algebra/Group | 18 | 11 | 4 | 3 | 0 | 0 / 5 | 14 / 4 |
| Algebra/Ring | 13 | 8 | 3 | 2 | 0 | 0 / 3 | 9 / 4 |
| NumberTheory additions | 10 | 9 | 0 | 1 | 0 | 0 / 0 | 4 / 6 |
| Dynamics (full) | 8 | 5 | 3 | 0 | 0 | 0 / 6 | 7 / 1 |

**`Order` produces zero casework-rich candidates** — striking, and mechanically sound: `casework_tier` requires a concretely-checkable (decidable or `output_decidable_eq`) result over enumerable argument types (`miner.proxies._is_concretely_checkable`), and Order-theoretic definitions are overwhelmingly `Prop`-valued relations/structures over arbitrary (non-enumerable) preorders/lattices, not computations over `ℕ`/`List`/etc. — casework in the reward-structure sense simply doesn't apply to most of this territory. The same holds, less starkly, for `Data/Set` (0 casework-rich) and `Combinatorics` (7 of 139). `Global` supply is rich almost everywhere (Order 124/199, Combinatorics 99/139, Data/Set 37/43) — theorem-mention-backed global facts are this batch's dominant new supply, not casework.

## 6. Richness distribution per territory

Corpus-wide (eligible set, n=727): mean 2.73, median 2, min 1, max 13.

| Territory | n | mean | median | max |
|---|---|---|---|---|
| Original corpus | 212 | 3.26 | 2 | 13 |
| Algebra/Ring | 13 | 3.23 | 3 | 6 |
| Order (full) | 199 | 2.76 | 2 | 11 |
| Topology core | 2 | 2.50 | 2.5 | 3 |
| Combinatorics (full) | 139 | 2.45 | 2 | 9 |
| Data completions | 79 | 2.37 | 2 | 8 |
| NumberTheory additions | 10 | 2.20 | 2 | 5 |
| Data/Set (core) | 43 | 2.16 | 2 | 7 |
| Dynamics (full) | 8 | 2.00 | 2 | 3 |
| Algebra/Group | 18 | 1.89 | 2 | 3 |
| Analysis/SpecialFunctions | 2 | 1.50 | 1.5 | 2 |

The richness *floor* (≥1) is doing real, uneven work by territory: the widened corpus's mean richness (2.73) is noticeably lower than batch 3's mix was — the new territories, on the whole, clear the floor but don't run especially rich above it, except where a territory happens to concentrate genuine induction/recursion-principle-shaped content (the original corpus's long tail up to richness 13 is `Int.greatestOfBdd`; Order's up to 11 is `WithTop.subtypeOrderIso`).

## 7. Scan-parser vigilance

Two findings, one genuinely new-territory-concentrated and one pre-existing.

### (a) New: `_root_.` namespace-escape prefix not recognized (namespace-tracking surprise)

Lean's `_root_.` prefix means "resolve from the global root, ignoring every enclosing namespace" — used to declare a name in a *different* namespace than the one textually enclosing it (e.g. `namespace Finset ... def _root_.Equiv.Finset.prod ... end Finset` declares `Equiv.Finset.prod`, not `Finset.Equiv.Finset.prod`). `miner.scan`'s namespace-stack qualification (`scan_text`'s `qualified = ".".join([*ns_parts, def_match.group("name")])`) has no special case for this: it unconditionally prepends every enclosing `namespace` onto whatever the `_DEF_RE` match captured as the name — and since `_root_` itself matches the identifier character class, `_root_.Equiv.Finset.prod` is captured whole as "the name" and gets the enclosing namespace prepended anyway, producing a wrong, doubly-qualified name.

**7 candidates affected corpus-wide**, found via a duplicate-name / deep-dot-count sweep of the full scanned corpus:

| Wrong name produced | Real name | Territory |
|---|---|---|
| `Finset._root_.Equiv.Finset.prod` | `Equiv.Finset.prod` | Original corpus (`Data/Finset/Prod.lean`) |
| `WithTop._root_.Function.Embedding.coeWithTop` | `Function.Embedding.coeWithTop` | Order (new) |
| `Quiver.Symmetrify._root_.Prefunctor.symmetrify` | `Prefunctor.symmetrify` | Combinatorics (new) |
| `SimpleGraph.Subgraph._root_.SimpleGraph.toSubgraph` | `SimpleGraph.toSubgraph` | Combinatorics (new) |
| `Equiv.Perm._root_.MonoidHom.toHomPerm` | `MonoidHom.toHomPerm` | Algebra/Group (new) |
| `Equiv.Perm._root_.Equiv.permCongrHom` | `Equiv.permCongrHom` | Algebra/Group (new) |
| `Sym2._root_.Function.Embedding.sym2Map` | `Function.Embedding.sym2Map` | Data/Sym (new) |

**6 of 7 (86%) are in newly-widened territory** — flagged prominently per the task's instruction, since this rate is materially above the original/batch-2 corners (1 occurrence there, in a corpus of 830 candidates, vs. 6 in 2,355 new-territory candidates — still a low absolute rate either way, but the concentration is real and makes sense: `_root_.`-qualified definitions are a technique for organizing a definition under a *different* namespace than its surrounding `section`/`namespace` block for readability, which is more common in richer, more cross-referential territory (endomorphism/automorphism files, category-adjacent combinatorics) than in the foundational corners.

**Consequence**: each of these 7 gets a wrong fully-qualified name in the manifest, which then fails `#check` in `miner.verify` (`Unknown identifier`) and is recorded as "does not elaborate" — 7 of the 40 non-elaborating candidates this batch (17.5%) are attributable to this one bug, not to any real problem with the definitions themselves. **Not fixed here** (explicit stop point: no parser fixes mid-mine) — flagged for a dedicated follow-up.

### (b) Pre-existing, NOT new-territory-specific: `/-!` module-doc blocks containing illustrative `def` examples

`miner.scan.scan_text`'s main loop recognizes `/--` (declaration docstring, immediately preceding a `def`) but has no concept of `/-!` (module/section-level doc comment) at all — a `def`-shaped line appearing *inside* a `/-! ... -/` block, purely as prose illustrating what the file defines, is scanned as if it were a real top-level declaration.

**Found in exactly 3 files**, via a targeted search for a `def`-shaped line inside a `/-! ... -/` span across the whole scanned corpus: `Data/Nat/Log.lean`, `Data/Int/Log.lean`, `Logic/Equiv/Functor.lean`. **All three are in corners scanned since batch 1** (`Data/Nat`, `Data/Int`, `Logic`) — this is a real, previously-unreported scanner blind spot surfaced as a side effect of this batch's own vigilance work, but it is **not concentrated in new territory** at all; it just happened to only get noticed now.

Concretely: `Logic/Equiv/Functor.lean`'s docstring illustrates `def Functor.mapEquiv (f : ...) : α ≃ β → f α ≃ f β` and `def Bifunctor.mapEquiv (F : ...) : ...` as prose examples — both happen to share their fully-qualified name with a *real* nested declaration later in the same file (`namespace Functor ... def mapEquiv ...`), producing exactly 2 duplicate-named `ScanHit`s corpus-wide (confirmed: 3,185 scanned hits, 3,183 unique names). Checked directly against the real manifest: **both phantom entries end up excluded via `docstring_floor`** (the illustrative snippet has no docstring of its own) rather than "does not elaborate" as might be expected — because `miner.verify.verify_definition`'s `#check <name>` resolves against the live, fully-compiled Mathlib environment, which already contains the *real* declaration under that name; the phantom `ScanHit`'s own (syntactically incomplete, bodyless) captured text is never itself compiled, only its *name* is checked. This is worth stating precisely rather than assumed: the pre-filter's false positives are caught downstream, but by whichever gate happens to apply to the phantom's own (wrong) scanned metadata, not uniformly by "does not elaborate." §9 confirms this costs nothing — the real `Functor.mapEquiv`/`Bifunctor.mapEquiv` entries remain eligible, unaffected.

`Data/Nat/Log.lean` and `Data/Int/Log.lean`'s docstring-embedded `logTR`-style examples are genuinely orphaned (no real declaration shares their name) — one harmless phantom `ScanHit` each, excluded on their own (low-quality, no real docstring) merits.

### Checked and cleared

- **Identifier-shape oddities** (the subscript-truncation bug class from prior batches): zero names failing the expected identifier-character-class shape across the full 3,185-hit corpus — the earlier fix holds up in every new territory.
- **Docstring-capture swallowing following code**: 20 hits have a docstring containing an embedded code fence or the word "def" (e.g. `Nat.leRec`'s docstring illustrates its own `induction ... using` idiom) — checked individually; all are ordinary, well-formed `/-- ... -/` blocks with legitimate embedded example prose, correctly bounded by the scanner. Not a bug, no action needed.
- **Near-empty captured source**: zero hits with fewer than 5 characters of captured body text.

## 8. Tier-2 discharge measurement

**Methodology.** For every eligible definition with `theorem_mention_count ≥ 1` (in this batch, all 727 — the mention floor of 2 already implies this for every survivor), up to 3 of its mentioning theorem statements (namespace-scoped matching, identical rule to `theorem_mention_count` itself) were sampled and each attempted against the true definition with the tactic ladder `rfl → omega → simp → exact? → aesop`, stopping at the first success, under a 30s per-attempt budget (`miner.config.DISCHARGE_TACTIC_TIMEOUT`). This is a measurement only — no gate, no score, reads nothing back into the manifest built in §1–§6.

**A real infrastructure bug was found and fixed mid-task, disclosed here rather than glossed over.** The first discharge run used its own freshly-opened warm environment (separate from the harvest's own, already-closed one) and had no recovery logic for a dead environment — unlike `miner.verify.verify_all_with_recovery`, which the harvest phase already uses. That environment died after only 9 of 727 definitions (most likely from one slow `aesop`/`exact?` call exceeding some internal limit), and every subsequent attempt for the remaining 718 definitions failed with a cascading "Unknown environment" error — 10,230 of 10,335 total tactic attempts in that first run were this one artifact, not a real measurement of anything. This was diagnosed from the raw discharge manifest (`errored` status with `"Unknown environment"` detail, concentrated after record #9), fixed by adding the same reimport-and-retry recovery `verify_all_with_recovery` already uses (now in `miner.discharge._attempt_statement_with_recovery`/`measure_discharge`, with new tests covering both the recovery path and the "no recovery when the environment is alive" path via a scripted fake server), and the discharge pass was re-run in full against the already-computed (unaffected) harvest manifest.

**A second, tighter budgeting problem showed up immediately after the recovery fix**, and is reported here just as plainly. Even recovery-fixed, a fresh full-corpus attempt at the task-suggested `DISCHARGE_TACTIC_TIMEOUT=30s` ran **past 7 hours without finishing** (stopped by hand at 67/727 definitions). Root cause, read off the timing data directly: the per-*statement* average cost (~108s) was far above the ~40s theoretical maximum even if every one of the 5 ladder tactics fully timed out — meaning recurring environment-death recoveries (each costing roughly a minute to reimport Mathlib) were the dominant cost, not the tactic budget itself, at that rate of occurrence. Two changes followed, both disclosed as deliberate deviations from the task's own suggestion rather than silently applied:

- **`DISCHARGE_TACTIC_TIMEOUT` lowered from the suggested 30s to 8s** (`miner/config.py`) — real successes and fast failures (the overwhelming majority of attempts) are essentially unaffected; only genuinely slow searches are bounded more tightly.
- **A hard 8-hour wall-clock cap added to `measure_discharge`** (`miner.config.DISCHARGE_MAX_WALL_CLOCK_S`, new parameter `max_wall_clock_s`), plus a progress callback and per-step manifest writes (`scripts/rerun_discharge_batch4.py`) — so an unattended overnight run is guaranteed to stop with a usable, honestly-partial manifest rather than run indefinitely. New tests cover both the cutoff and the progress callback (`tests/test_miner_discharge.py`).

**Even with both changes, the corpus-wide measurement did not complete.** The run was executed in two bounded passes — an 8-hour pass (104/727 definitions, stopped cleanly at its own cutoff) followed by a 2-hour resume pass reusing the same on-disk results and covering only the remaining, not-yet-measured definitions (`scripts/resume_discharge_batch4.py`, 27 more) — for a combined:

**131 of 727 eligible definitions measured (18.0%)**, 372 statements attempted, before the combined ~10-hour budget was exhausted. This is reported as an honest partial measurement, not extrapolated to the full corpus — per the task's own explicit allowance ("if exact?/aesop availability... is a problem, report what IS runnable and measure with that subset rather than skipping"), this *is* that subset, sized by wall-clock budget rather than by any deliberate sampling choice. The 596 unmeasured definitions are simply absent from `miner/output/discharge_manifest.jsonl`, not recorded with a fabricated zero.

| | Count | Rate |
|---|---|---|
| Definitions measured | 131 / 727 | 18.0% |
| Statements attempted | 372 | — |
| Statements discharged | 14 | **3.76%** |
| Tactic attempts, `not_discharged` (clean failure) | 1,055 | 58.5% of all attempts |
| Tactic attempts, `errored` | 747 | 41.5% of all attempts |

**By winning tactic** (of the 14 discharged): `rfl` 8, `simp` 6 — `omega`, `exact?`, and `aesop` won **zero** statements in this sample. Too small a sample (131 of 727) to conclude these three are unproductive corpus-wide, but worth flagging plainly rather than silently: in the portion actually measured, all discharge success came from the two cheapest, most syntactic tactics in the ladder.

**The 41.5% `errored` rate is itself a finding, not noise.** Environment-death recoveries do *not* show up here — `_attempt_statement_with_recovery` discards a dead attempt's record entirely and replaces it with the clean retry, so a death never persists as a recorded `errored` attempt. This 41.5% is overwhelmingly genuine per-tactic timeouts (a tactic — almost certainly `simp`/`exact?`/`aesop` — ran the full 8s without resolving). Combined with the 58.5% clean `not_discharged` rate, the picture is: roughly three in five sampled statements fail every tactic cleanly and quickly (consistent with the context-loss caveat in `attempt_statement`'s own docstring — a statement extracted standalone, outside its file's `variable`/`open`/section context, often can't even elaborate as a sensible goal), while a substantial two in five *do* engage a tactic long enough to run out the clock — meaning a real fraction of sampled statements are posing genuine, non-trivial proof obligations to the ladder, not just malformed goals.

**By territory** (measured subset only — coverage is uneven simply because measurement proceeds in eligible-rank order, not because any territory was prioritized or skipped):

| Territory | Definitions measured | Statements attempted | Discharged |
|---|---|---|---|
| Original corpus | 58 | 165 | 10 |
| Order (full) | 37 | 102 | 0 |
| Combinatorics (full) | 20 | 59 | 3 |
| Data completions | 10 | 29 | 0 |
| Data/Set (core) | 3 | 9 | 1 |
| Algebra/Ring (top-level) | 2 | 6 | 0 |
| NumberTheory additions | 1 | 2 | 0 |

The 8 definitions with at least one discharged statement: `Nat.leRec`, `memPartition`, `Function.dcomp`, `finSumNatEquiv`, `SimpleGraph.boxProd`, `hyperoperation`, `subtypeOrLeftEmbedding`, `Equiv.subtypeEquiv`. `Order`'s zero-discharge showing (0 of 102 attempted, across 37 definitions) despite decent coverage is worth naming plainly as a data point, not explained away — consistent with §5's finding that Order-territory candidates are heavily `Prop`-shaped and mention-supplied by genuinely general theorems (not close, easily-rfl'd instantiations), so a ladder this shallow finding nothing there is not surprising in hindsight, but it is a real, reportable zero.

## 9. Changelog vs. batch 3 — existing candidates confirmed unchanged

**All 256 candidates eligible in batch 3 (revision 2) remain eligible in batch 4. Zero regressions, zero candidates missing from the batch-4 manifest.** (An initial pass of this check found what looked like 2 regressions — `Functor.mapEquiv`/`Bifunctor.mapEquiv` "no longer eligible" — which turned out to be an artifact of the check itself picking the wrong one of two same-named manifest entries, per §7(b)'s duplicate-name finding; the real entries for both names are confirmed still eligible, `gates_failed: []`, docstrings intact.)

- Batch 3 eligible: 256
- Still eligible in batch 4: 256
- No longer eligible: 0
- Missing entirely from the batch-4 manifest: 0
- Batch 4 total eligible: 727
- **Newly eligible this batch (new territory or previously-unreached corners): 473**

This confirms the batch's own framing: nothing about the selection machinery or the previously-scanned corpus changed. Every batch-3 candidate's gate outcomes, richness, and rank-eligibility are exactly as they were; the entire net gain (256 → 727) comes from the widened `TARGET_MODULES` reaching candidates that were never in scope before, not from any recalculation of existing ones.

## 10. Detail cards: new top 10 (by preference score, batch 4)

### 1. Int.greatestOfBdd
*Data/Int/LeastGreatest.lean* — richness 13, value-shaped, theorem_mention_count 3

A computable version of `exists_greatest_of_bdd`: given a decidable predicate on the integers, with an explicit upper bound and a proof that it is somewhere true, return the greatest value for which the predicate is true. (Already eligible in batch 3 at rank 1 — unchanged status, now surrounded by much more competing content but still the single richest candidate in the corpus.)

### 2. Nat.leRec
*Data/Nat/Init.lean* — richness 12, value-shaped, theorem_mention_count 15

Recursion starting at a non-zero number: given a map `C k → C (k+1)` for each `k ≥ n`, produces a map from `C n` to each `C m`, `n ≤ m`. A version of `Nat.le.rec` for `Sort u`.

### 3. Nat.binaryRec
*Data/Nat/BinaryRec.lean* — richness 11, value-shaped, theorem_mention_count 8

A recursion principle for `bit` representations of natural numbers: given base and step cases, constructs a value for every natural number via its binary representation.

### 4. WithTop.subtypeOrderIso
*Order/Hom/WithTopBot.lean* — richness 11, bundled, theorem_mention_count 2

Any `OrderBot` is order-isomorphic to `WithBot` of the subtype excluding `⊥`. **New this batch** — the single richest genuinely-new-territory candidate (Order).

### 5. Nat.clog
*Data/Nat/Log.lean* — richness 10, value-shaped, theorem_mention_count 34

The upper (ceiling) logarithm: the smallest `k` such that `n ≤ b^k`. (Already used as the worked fixture example for the authoring-side validation layer built in this project's stage-2 pause.)

### 6. Int.leastOfBdd
*Data/Int/LeastGreatest.lean* — richness 10, value-shaped, theorem_mention_count 3

The least-value dual of rank 1: given a lower bound and a witness, returns the least value satisfying a bounded, decidable predicate.

### 7. List.prev
*Data/List/Cycle.lean* — richness 9, value-shaped, theorem_mention_count 21

Given a proof `x ∈ l`, returns the element immediately before `x`'s first occurrence in `l`. Worked examples baked directly into the docstring.

### 8. Finset.strongDownwardInduction
*Data/Finset/Card.lean* — richness 9, value-shaped, theorem_mention_count 2

An induction principle building a value on a finset from values on all larger-or-equal-cardinality supersets, working downward from a fixed bound.

### 9. Equiv.sigmaSigmaSubtypeEq
*Logic/Equiv/Basic.lean* — richness 9, bundled, theorem_mention_count 2

A specialization of a nested-sigma equivalence to the case of plain equality constraints — useful where the second base type doesn't depend on the first (e.g. `Hom` inside a category).

### 10. List.recNeNil
*Data/List/Induction.lean* — richness 9, value-shaped, theorem_mention_count 2

A dependent recursion principle for nonempty lists — avoids needing to handle an impossible empty case, useful for operations like `List.head` that aren't defined on `[]`.

## 11. Full ranked table

727 rows is too large to usefully embed as a markdown table (batch 3's own precedent capped in-document tables around 150–256 rows before deferring to the raw manifest) — the complete ranked list of all 727 eligible candidates, every excluded candidate with its failing gate(s), and every discharge-measurement record is in `miner/output/harvest_manifest.jsonl` and `miner/output/discharge_manifest.jsonl` respectively. `docs/harvest_digest_batch4.md` covers the top 25 in the same skimmable format as the batch-3 digest.
