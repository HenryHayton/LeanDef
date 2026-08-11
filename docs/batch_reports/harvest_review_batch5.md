# Harvest Batch 5 Review — "Full-Math Widening"

Run 10–11 Aug 2026. Mathlib pin unchanged (`v4.32.0`, commit `81a5d257…`); no re-pin was needed
or made. Extends the batch-4 review's format with the per-area breakdowns the batch-5 brief
requires.

---

## 0. Corpus scope

`TARGET_MODULES` replaced wholesale with **tranche A**: 24 mathematical Mathlib subtrees
(~5,800 of the pin's 8,264 files). The batch-1..4 entry list was not extended but *superseded* —
every prior entry was a corner of one of these subtrees (`Data/Nat` ⊂ `Data`, `Topology/Order/*`
⊂ `Topology`, …), so keeping both granularities would have double-scanned those files.

**Excluded permanently** (infrastructure/meta, not mathematics): `Tactic`, `Util`, `Lean`,
`Testing`, `Deprecated`. No `Init` exists at this pin.

**Deferred, tranche B** (recorded in `docs/deferred.md` with trigger): `CategoryTheory`,
`AlgebraicGeometry`, `AlgebraicTopology`, `Condensed`, `RepresentationTheory`, `MeasureTheory`,
`Probability`, `Geometry/Manifold`.

`Geometry` is entered per-subdirectory because `Geometry/Manifold` is deferred; the pin has no
loose `Geometry/*.lean` files, so the six subdirectory entries *are* the subtree minus Manifold.

---

## 1. Corpus counts

| | batch 4 | **batch 5** |
|---|---|---|
| Scanned (pre-filter hits) | 3,185 | **15,387** |
| Verified (elaborates) | 3,145 | 15,294 |
| Does not elaborate | 40 | 93 |
| **Eligible** | 721 | **2,609** |
| — of which new | — | **1,891** |

Target was ≥2,500 with 2,000–3,500 declared success: **met**, after vocabulary round 2.

Eligible density fell from batch 4's 22.6% to **17.0%**, exactly as the brief predicted for
newer, more abstract territory.

---

## 2. Gate attrition (independent — every gate evaluated for every candidate)

| Gate | Fails | % of verified |
|---|---|---|
| `richness_floor` | 7,354 | 47.8% |
| `theorem_mention_floor` | 7,060 | 45.9% |
| `fact_supply` | 4,716 | 30.6% |
| `dependency_vocabulary` | 4,362 | 28.3% |
| `length_band` | 1,163 | 7.6% |
| `docstring_floor` | 765 | 5.0% |
| `anti_plumbing` | 147 | 1.0% |

No threshold moved this batch. The only config changes were `TARGET_MODULES` and
`COMMON_VOCABULARY_MODULES`, both monotone.

---

## 3. Per-area yield (headline deliverable)

| Area | Scanned | Eligible | New | Yield |
|---|---|---|---|---|
| Data | 2,062 | 535 | 297 | 25.9% |
| Algebra | 3,434 | 487 | 453 | 14.2% |
| Topology | 2,068 | 247 | 245 | 11.9% |
| Order | 957 | 203 | 5 | 21.2% |
| LinearAlgebra | 1,139 | 202 | 202 | 17.7% |
| RingTheory | 1,408 | 198 | 198 | 14.1% |
| Analysis | 1,113 | 168 | 166 | 15.1% |
| Combinatorics | 605 | 152 | 15 | 25.1% |
| NumberTheory | 474 | 88 | 58 | 18.6% |
| GroupTheory | 539 | 87 | 87 | 16.1% |
| Logic | 403 | 76 | 7 | 18.9% |
| ModelTheory | 238 | 42 | 42 | 17.6% |
| Computability | 248 | 36 | 36 | 14.5% |
| SetTheory | 168 | 26 | 26 | 15.5% |
| Geometry | 186 | 25 | 25 | 13.4% |
| FieldTheory | 181 | 18 | 18 | 9.9% |
| Dynamics | 38 | 11 | 3 | 28.9% |
| Control | 120 | 6 | 6 | 5.0% |
| InformationTheory | 6 | 2 | 2 | 33.3% |
| **TOTAL** | **15,387** | **2,609** | **1,891** | **17.0%** |

**Cross-check that the granularity change was clean.** Order, Combinatorics, Logic and Dynamics
contribute 5/15/7/3 new — near zero, which is correct: batch 4 already scanned those subtrees in
full. Had the file→subtree rewrite duplicated or shifted records, these would not be ~0.

`RingTheory` (198), `LinearAlgebra` (202) and `Topology` (245) are the largest genuinely new
territories. `Control` is the weakest at 5.0% — monadic plumbing, largely correctly rejected.

### Per-area dominant gates

| Area | Top three gates |
|---|---|
| Data | mention=875, richness=681, vocabulary=531 |
| Algebra | richness=1,920, mention=1,845, fact_supply=1,428 |
| Topology | mention=1,096, richness=1,080, fact_supply=782 |
| LinearAlgebra | richness=599, mention=415, vocabulary=358 |
| RingTheory | richness=679, mention=572, vocabulary=508 |
| Analysis | richness=507, **vocabulary=431**, mention=402 |
| SetTheory | **vocabulary=84**, richness=83, mention=53 |
| Control | mention=82, vocabulary=63, fact_supply=57 |

Vocabulary bites hardest in Analysis, SetTheory and Computability — the areas whose natural
dependencies sit furthest from the foundational corners the list grew up around.

---

## 4. Vocabulary rounds

**Round 1** (conservative, pre-scan): 12 seeds, every directory existence-checked at the pin —
`Data/Rat`, `Data/Fintype`, `Data/ZMod`, `Data/Vector`, `Data/Array`, `Data/PNat`, `Data/Sum`,
`Data/Matrix`, `GroupTheory/Perm`, `GroupTheory/Subgroup`, `RingTheory/Ideal`,
`Algebra/GCDMonoid`. Yield: 2,263 eligible.

**Round 2** (evidence-driven, from the round-1 exclusion table). Each entry was the *sole* gate
blocking a named set of definitions; the count is blocked references observed.

| Added | Refs | Example definitions recovered |
|---|---|---|
| `Analysis/Normed` | 538 | `ZSpan.fundamentalDomain`, `ZLattice.covolume` |
| `Algebra/Module` | 365 | `Unitization.starMap`, `Module.DirectLimit` |
| `Topology/Defs` | 261 | `Asymptotics.SuperpolynomialDecay`, `IsThetaTVS` |
| `Algebra/Algebra` | 243 | `AlgEquiv.piCongrLeft`, `AlgEquiv.prodCongr` |
| `Computability/Partrec` | 124 | `WithOne.recOneCoe`, `MvPolynomial.optionEquivLeft` |
| `Topology/MetricSpace` | 55 | `IsPrimePow`, `LieModule.genWeightSpaceChain` |
| `Combinatorics/SimpleGraph` | 46 | `SimpleGraph.mulCayley`, `SimpleGraph.toTopEdgeLabeling` |
| `Data/Seq` | 45 | `GenContFract.squashSeq`, `Stream'.Seq1.map` |
| `LinearAlgebra/Matrix` | 45 | `Matrix.gram`, `Matrix.compl` |

**Deliberately rejected despite high reference counts** — heavy abstract infrastructure, exactly
what the gate exists to catch, and tranche-B in character: `Algebra/Homology` (501),
`CategoryTheory/Subfunctor` (375), `Algebra/Category` (193), `AlgebraicTopology/*` (156),
`AlgebraicGeometry/*` (115), `Algebra/Lie` (81), `Data/QPF` (46).

**Round-2 delta: +346 eligible, −0 lost** (2,263 → 2,609). Biggest gains LinearAlgebra +88,
Topology +75, Analysis +56, Algebra +41, RingTheory +32.

Round 2 was applied by **re-gating recorded metadata** — `scripts/regate_batch5.py`, 253s, no
Lean, no re-scan. This is the brief's "one expensive pass, cheap iterations after" rule working
as intended.

---

## 5. Monotonicity assertion

> **Every batch-4 eligible definition must remain eligible in batch 5.**

**Result: 0 gate-driven drops.** Exactly three batch-4 eligibles are not eligible in batch 5:

| Definition | `gates_failed` | Cause |
|---|---|---|
| `Nat.ceilRoot` | `[]` | curation: exemplar burn (slot 1) |
| `SimpleGraph.LocallyLinear` | `[]` | curation: exemplar burn (slot 2) |
| `Filter.limsSup` | `[]` | curation: exemplar burn (slot 3) |

All three have **empty `gates_failed`** — no gate rejected them. They are excluded by
`miner/curation.yaml`, whose exemplar burns were committed in `d1020b4`, *after* the batch-4
manifest was written. The brief requires those burns persist untouched, and they do;
`curation.yaml` was not modified this batch. Monotonicity holds on the axis it is asserted over.

---

## 6. Composition (for later strata quotas)

### Return shape, eligible, per area

| Area | value | prop | **bundled** |
|---|---|---|---|
| Data | 434 | 55 | 46 |
| Algebra | 372 | 38 | **77** |
| Topology | 167 | 44 | 36 |
| Order | 108 | 76 | 19 |
| LinearAlgebra | 149 | 27 | 26 |
| RingTheory | 148 | 28 | 22 |
| Analysis | 130 | 19 | 19 |
| Combinatorics | 107 | 41 | 4 |
| Logic | 12 | 24 | **40** |
| GroupTheory | 55 | 19 | 13 |

Bundled counts called out explicitly per the brief. `Logic` inverts the usual profile — 40
bundled against 12 value-typed. `Order` and `Combinatorics` are the richest `prop` sources.

### Execution mechanism (eligible)

`none = 2,542` · `eval = 59` · `decide = 8`

**97.4% of the eligible pool has no executable mechanism at all.** This is the single most
consequential number in the review for stage-2 planning: it confirms, at corpus scale, the
CLAUDE.md warning that `decide`-dominated fact suites (the τ example) are unrepresentative.
Essentially every batch-5 task will need the adjudication ladder, not kernel computation.

### Richness (eligible)

mean 2.50 · median 2 · min 1 · max 24

---

## 7. Blind-spot counters (Step 5 — metadata only)

Implemented as recorded metadata on every candidate. **They do not enter `richness_total`, the
preference score, or any gate**, and a load-bearing test asserts that exclusion so a later change
folding them in fails loudly rather than silently reshuffling eligibility.

| Counter | Eligible with ≥1 | Share |
|---|---|---|
| `blind_disjoint_binders` | 14 | 0.5% |
| `blind_heyting` | 5 | 0.2% |
| `blind_cond` | 1 | 0.0% |

Concentrated in Data (5), Order (5), then scattered singletons.

**Recommendation: do not promote.** The deferred entry's trigger was "recurring at scale in a
wider harvest". At 20 definitions in 2,609 (0.8%) across a 4.8×-larger corpus, the answer is that
they do **not** recur at scale. Promoting them would reshuffle the ranking for <1% of the pool.
Recorded in `docs/deferred.md` as measured-and-declined rather than left open.

---

## 8. Top 10 by preference score

| # | Definition | Richness | Module |
|---|---|---|---|
| 1 | `CartanMatrix.D` | 24 | LinearAlgebra/Matrix/Cartan.lean |
| 2 | `Nat.Partrec.Code.eval` | 18 | Computability/PartrecCode.lean |
| 3 | `PythagoreanTriple.IsPrimitiveClassified` | 18 | NumberTheory/PythagoreanTriples.lean |
| 4 | `GromovHausdorff.candidates` | 17 | Topology/MetricSpace/GromovHausdorffRealized.lean |
| 5 | `Turing.PartrecToTM2.trStmts₁` | 17 | Computability/TuringMachine/ToPartrec.lean |
| 6 | `normFromBounded` | 15 | Analysis/Normed/Unbundled/SeminormFromBounded.lean |
| 7 | `FermatLastTheoremWith'` | 14 | NumberTheory/FLT/Basic.lean |
| 8 | `CoxeterMatrix.B` | 14 | GroupTheory/Coxeter/Matrix.lean |
| 9 | `Int.greatestOfBdd` | 13 | Data/Int/LeastGreatest.lean |
| 10 | `Turing.PartrecToTM2.contSupp` | 13 | Computability/TuringMachine/ToPartrec.lean |

Nine of ten come from newly-scanned territory. `Int.greatestOfBdd` (rank 9) was batch 4's rank 1
— the widening genuinely displaced it rather than merely appending.

Two Turing-machine internals in the top 10 is a mild recurrence of the batch-4
`Nat.leRec` observation (proof/computational infrastructure scoring high on structural richness).
Not acted on; noted for the recorded richness blind-spot entry.

---

## 9. Near-duplicate families (list only — no curation changes)

Representative selection is a stage-2 decision, per the brief.

| Stem | Eligible | Sample |
|---|---|---|
| `Set` | 62 | BijOn, Bounded, EqOn, Icc, IccExtend, IciExtend |
| `LinearMap` | 59 | HasFiniteRange, IsAdjointPair, IsAlt, IsOrthogonal |
| `Nat` | 54 | Abundant, Deficient, FermatPsp, IsAlmostPrime, ModEq |
| `Finset` | 44 | Nonempty, Shatters, affineCombination, biUnion |
| `Matrix` | 44 | BlockTriangular, IsSymm, IsTotallyUnimodular |
| `SimpleGraph` | 41 | CliqueFree, DeleteFar, IsAcyclic, IsAlternating |
| `Finsupp` | 40 | Lex, comapDomain, cons, curry, embDomain |
| `Polynomial` | 35 | IsPrimitive, IsRoot, Monic, IsUnitTrinomial |
| `List` | 33 | Forall, HasPeriod, IsRotated, Shortlex, TFAE |
| `Equiv` | 33 | cast, functor, ofLeftInverse, optionCongr |
| `Filter` | 33 | Eventually, EventuallyConst, Frequently, IsBounded |
| `Submodule` | 30 | ClosedComplemented, IsPrimary, comap, dualAnnihilator |

---

## 10. Surprises

**(a) The harvest ran in 12 minutes, not the projected 11 hours.** Two performance bugs were
found and fixed mid-batch, both invisible at batch-4 scale:

1. `compute_mention_counts` spawned **one recursive `grep` over all 8,264 files per candidate**
   (~0.85s each). Batch 4's 3,185 candidates absorbed it (~29 min); batch 5's 15,387 projected to
   **~3.6 hours** — to populate a field that, by its own docstring, **no gate reads**. Rewritten
   as one corpus pass: **2.7s**.
2. Fixing it exposed a correctness bug it had been hiding. `grep -F` is a substring search, so
   `Nat.log` matched every `Nat.log_le`, `Nat.log_lt_of_lt_pow`, … Under Mathlib's naming
   convention most names prefix a longer sibling, so most recorded `mention_count`s were
   **inflated**. Now counts identifier tokens. Counts drop relative to batch 4; the drop is a
   correction. Safe against monotonicity precisely because `mention_count` gates nothing — it was
   retired as a gate input on 22 July 2026, leaving `theorem_mention_count` (a different,
   statement-scoped measure) as the gated one.

**(b) A 200-hour projection that was pure measurement error.** An early calibration sample
reported 60–150s per candidate, projecting ~200h and threatening the brief's 24h stop-and-split
condition. The true figure was batch 4's own recorded **3.23 s/candidate**. The sample had been
measuring laptop memory contention (0.2 GB free while three prover arms ran) plus repeated
environment-death re-imports amortised over only 20 candidates. A full run amortises them over
thousands. **Lesson: calibrate against the last batch's recorded rate before escalating a
projection.**

**(c) The verification cache paid for itself immediately.** `miner/verified_cache.py` was added
for an expected 11-hour run (reuse 3,145 records; checkpoint every 50 so a lost process costs a
chunk). The run turned out to take 12 minutes — but the cache is what made round 2's re-gate
possible **without any Lean at all**, which is the more durable win.

**(d) 97.4% of eligible definitions have no executable mechanism.** Expected in direction,
larger than anticipated in magnitude. See §6.

**(e) 93 candidates verified but do not elaborate** (0.6%), up from batch 4's 40 (1.3%) — a
*lower* rate despite far more exotic territory. No systematic per-area parse failure was found;
no area was silently dropped.

---

## 11. Changelog vs batch 4

- Corpus 3,185 → 15,387 scanned (4.8×); eligible 721 → 2,609 (3.6×)
- `TARGET_MODULES`: entry list superseded by 24 subtree entries + documented exclusions/deferrals
- `COMMON_VOCABULARY_MODULES`: 21 → 42 entries across two rounds
- New: `miner/verified_cache.py`, `scripts/regate_batch5.py`
- Rewritten: `compute_mention_counts` (one pass, token matching)
- Batch 4 preserved at `miner/output/harvest_manifest_batch4.jsonl`
- Monotonicity: 0 gate-driven drops; 3 pre-existing curation burns accounted
