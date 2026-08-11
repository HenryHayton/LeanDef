# Batch 5 Digest — one page

**What changed:** stage-1 mining widened from a hand-listed set of Mathlib corners to 24 whole
mathematical subtrees (~5,800 of 8,264 files). Gates and thresholds unchanged; only
`TARGET_MODULES` and `COMMON_VOCABULARY_MODULES` moved.

| | batch 4 | batch 5 |
|---|---|---|
| scanned | 3,185 | **15,387** |
| eligible | 721 | **2,609** (1,891 new) |
| yield | 22.6% | 17.0% |
| wall-clock | 2.6 h | **12 min** |

**Target met.** Brief asked for ≥2,500 (2,000–3,500 = success).

**Monotonicity: 0 gate-driven drops.** The only three batch-4 eligibles now excluded are the
protected exemplar burns (`Nat.ceilRoot`, `SimpleGraph.LocallyLinear`, `Filter.limsSup`), all
with empty `gates_failed`, excluded by curation committed after batch 4 ran.

**Vocabulary grew twice:** round 1 (12 conservative seeds, pre-scan) → 2,263 eligible; round 2
(9 entries, each justified by named blocked definitions) → **+346, −0 lost** → 2,609. Round 2 ran
as a pure re-gate of recorded metadata: 253s, no Lean.

**Three findings that outlive this batch:**

1. **97.4% of eligible definitions have no executable mechanism** (`none=2,542`, `eval=59`,
   `decide=8`). Confirms at corpus scale that `decide`-dominated fact suites are unrepresentative;
   essentially every batch-5 task needs the adjudication ladder.
2. **`compute_mention_counts` was O(candidates × corpus)** — one full `grep` of 8,264 files per
   candidate, ~3.6h projected, for a field no gate reads. Now one pass, 2.7s. Fixing it exposed
   that `grep -F` substring matching had been **inflating** every count whose name prefixes a
   longer sibling (`Nat.log` ⊂ `Nat.log_le`). Now token-matched; counts drop, and the drop is a
   correction.
3. **A 200h projection was measurement error, not workload.** Calibrated on a 120-candidate
   sample under memory pressure; the real rate was batch 4's recorded 3.23 s/candidate. Calibrate
   against the previous batch's recorded rate before escalating.

**Blind-spot counters** (`cond`, Heyting ops, `Disjoint`-style binders) implemented as metadata
only, excluded from richness/ranking/gates with a test pinning that. Incidence 20/2,609 (0.8%) —
**recommendation: do not promote**; the "recurring at scale" trigger did not fire.

**Artifacts:** `miner/output/harvest_manifest_batch5.jsonl` (ranked eligible + excluded-with-gates);
batch 4 preserved at `harvest_manifest_batch4.jsonl`. Full review:
`docs/batch_reports/harvest_review_batch5.md`.
