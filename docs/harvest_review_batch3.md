# Harvest Batch 3 Review

Human-readable review of the third mechanical harvest (`miner/output/harvest_manifest.jsonl`), generated read-only from that file. This batch implements "Selection round 2" — the 22 July 2026 recalibration recorded in `docs/design/definition_selection_2026-07-21.md`'s revision section, following up on `docs/harvest_review_batch2.md`'s Findings A–B and §5. Same corpus as batch 2 (964 scanned hits, 5 original corners + the 69-file widened selection) — nothing changed in `TARGET_MODULES` this round; everything below is a selection-mechanism change, not a corpus change.

**This is revision 2.** `docs/theorem_mention_audit.md` audited `theorem_mention_count` (the metric backing the `theorem_mention_floor` gate) and found the measurement itself was undercounting — see §0 below for the fix and its effect. **Manifest shape** is unchanged from revision 1: two populations, `eligible` (passed all seven gates, ranked by preference score, in full) and excluded (with the specific gate(s) that fired) — no top-N cutoff.

## 0. Revision 2 changelog: theorem-mention counting fix

`docs/theorem_mention_audit.md` traced `theorem_mention_floor`'s 75.2% independent kill rate (revision 1's §3/§5) to a measurement artifact, not corpus reality: the counter matched only a candidate's *fully-qualified* name, missing the majority of real mentions, which Lean's own namespace convention writes unqualified from inside a definition's own namespace. Two fixes, both implemented exactly as the audit recommended and nothing further:

- **Namespace-scoped mention counting** (`miner.scan.scan_theorem_statements_with_namespace`, `miner.harvest.compute_theorem_mention_counts`): a statement now counts as a mention if it contains the candidate's qualified name *anywhere*, **or** its bare name from within a namespace block that resolves to that candidate. Deliberately **not** an unscoped bare-name match — the audit quantified that as up to 98% collision noise on short names (`pi`, `empty`, `fix`, ...).
- **Bracket-aware statement splitting** (reusing the exact technique `miner.verify._split_check_output` already used for `#check` output): the statement/proof split now finds the first `:=` at bracket depth 0, so named-argument syntax like `(a := a)` inside a statement's own type no longer truncates extraction before a later mention.

**No re-verification was needed or performed** — nothing about any candidate's source, richness, docstring, or dependencies changed; only the theorem-mention count input changed, so the manifest was rebuilt by recounting and re-gating against the exact same verification data batch 3 (revision 1) already produced. Recount runtime: **17.0s** for both fixes combined (comparable to revision 1's original ~13-15s single-fix cost; no caching needed, consistent with the audit's own finding that this scan is cheap).

### (i) Corpus-wide old vs. new mention-count distribution

| | Old (revision 1) | New (revision 2) |
|---|---|---|
| Zero-mention candidates (of 950 verified) | 624 (65.7%) | 309 (32.5%) |
| Mean | 15.22 | 25.64 |
| p50 (median) | 0 | 3 |
| p75 | 1 | 11 |
| p90 | 8 | 38 |
| p95 | 33 | 96 |
| p99 | 429 | 492 |
| Max | 1,804 | 1,810 |

The zero-mention population halved (65.7% → 32.5%) and every non-trivial percentile moved up by roughly an order of magnitude at the low-to-middle end (p50 0→3, p75 1→11, p90 8→38) — exactly the shape the audit predicted: the fix recovers real supply for the *typical* candidate, not just a few outliers (the top end, p99/max, barely moves, since heavily-qualified-in-other-files candidates were already counted reasonably well by the old qualified-only method).

### (ii) Rebuilt `THEOREM_MENTION_FLOOR` sensitivity table

All six other gates held fixed at their actual configured values, both columns computed the identical way (only the mention-count input differs):

| `THEOREM_MENTION_FLOOR` | Eligible-set size, old counts | Eligible-set size, new counts |
|---|---|---|
| 1 | 147 | 288 |
| **2 (current)** | **120** | **256** |
| 3 | 100 | 230 |
| 5 | 76 | 191 |

At the current floor of 2, the corrected count **more than doubles** the eligible set the floor alone would allow (120 → 256) — consistent with revision 1's own honest framing of its sensitivity table as "evidence for a future call," now updated with the measurement it was always meant to be re-evaluated against once fixed.

### (iii) Eligibility status changes

**135 candidates became eligible; 0 became ineligible.** This asymmetry is not a coincidence — it is a mathematical guarantee of how the fix works: the new count is provably `>= ` the old count for every candidate (the bracket-aware split only ever finds a `:=` at or after the naive split's position, so the qualified-match portion of the count cannot decrease, and the namespace-scoped bare-match portion only adds more matches on top). `theorem_mention_floor` can therefore only newly *pass* for a candidate under this fix, never newly *fail* — and no other gate reads `theorem_mention_count` except indirectly through `fact_supply`'s `global_tier` input, which is monotonic in the same count for the same reason. The two independent per-gate fail-rate columns confirm this precisely:

| Gate | Revision 1 fail rate | Revision 2 fail rate |
|---|---|---|
| `theorem_mention_floor` | 75.2% | **41.6%** |
| `length_band` | 5.1% | 5.1% (unchanged — no input touched) |
| `docstring_floor` | 1.6% | 1.6% (unchanged) |
| `dependency_vocabulary` | 20.5% | 20.5% (unchanged) |
| `anti_plumbing` | 1.8% | 1.8% (unchanged) |
| `richness_floor` | 35.9% | 35.9% (unchanged — richness is a pure function of source text, untouched by this fix) |
| `fact_supply` | 35.9% | **23.8%** (moved, since `global_tier` reads `theorem_mention_count`) |

All 135 candidates that changed status, with old vs. new counts (module distribution: 75 `Data/*`, 27 `Logic/*`, 16 `NumberTheory/*`, 15 `Combinatorics/*`, 2 `Order/*` — the widened-corpus corners this whole redesign was reaching for are exactly where the fix's yield concentrated):

| Rank | Name | Module | old_tmc | new_tmc |
|---|---|---|---|---|
| 1 | Int.greatestOfBdd | Data/Int/LeastGreatest.lean | 0 | 3 |
| 3 | Nat.binaryRec | Data/Nat/BinaryRec.lean | 0 | 8 |
| 5 | Int.leastOfBdd | Data/Int/LeastGreatest.lean | 0 | 3 |
| 6 | List.prev | Data/List/Cycle.lean | 0 | 21 |
| 7 | Finset.strongDownwardInduction | Data/Finset/Card.lean | 0 | 2 |
| 8 | Equiv.sigmaSigmaSubtypeEq | Logic/Equiv/Basic.lean | 0 | 2 |
| 9 | List.recNeNil | Data/List/Induction.lean | 0 | 2 |
| 10 | Nat.decreasingInduction | Data/Nat/Init.lean | 0 | 5 |
| 13 | Function.Embedding.setValue | Logic/Embedding/Basic.lean | 0 | 4 |
| 14 | Equiv.subtypePreimage | Logic/Equiv/Basic.lean | 0 | 2 |
| 16 | Equiv.ofLeftInverse | Logic/Equiv/Set.lean | 0 | 2 |
| 19 | Relation.Fibration | Logic/Relation.lean | 1 | 11 |
| 20 | Nat.nthRoot | Data/Nat/NthRoot/Defs.lean | 0 | 15 |
| 21 | Multiset.noncommFoldr | Data/Finset/NoncommProd.lean | 0 | 4 |
| 23 | Equiv.piCongrRight | Logic/Equiv/Basic.lean | 1 | 2 |
| 24 | Nat.evenOddRec | Data/Nat/EvenOddRec.lean | 0 | 3 |
| 25 | Relation.CutExpand | Logic/Hydra.lean | 0 | 19 |
| 26 | Finset.strongInduction | Data/Finset/Card.lean | 0 | 2 |
| 27 | Nat.bitCasesOn | Data/Nat/BinaryRec.lean | 0 | 5 |
| 28 | ArithmeticFunction.dirichletInverseFun | NumberTheory/ArithmeticFunction/Defs.lean | 0 | 3 |
| 29 | List.nextOr | Data/List/Cycle.lean | 0 | 12 |
| 32 | Function.dcomp | Logic/Function/Defs.lean | 0 | 2 |
| 33 | Composition.embedding | Combinatorics/Enumerative/Composition.lean | 0 | 12 |
| 37 | Finset.Colex.IsInitSeg | Combinatorics/Colex.lean | 0 | 5 |
| 38 | Nat.psub | Data/Nat/PSub.lean | 0 | 8 |
| 53 | Function.updateFinset | Data/Finset/Update.lean | 1 | 14 |
| 56 | Finset.sigmaLift | Data/Finset/Sigma.lean | 0 | 8 |
| 57 | Int.bitwise | Data/Int/Bitwise.lean | 0 | 6 |
| 59 | AList.insertRec | Data/List/AList.lean | 0 | 3 |
| 62 | Nat.ceilRoot | Data/Nat/Factorization/Root.lean | 0 | 4 |
| 63 | Nat.floorRoot | Data/Nat/Factorization/Root.lean | 0 | 4 |
| 65 | List.dlookup | Data/List/Sigma.lean | 0 | 29 |
| 66 | List.choose | Data/List/Defs.lean | 0 | 8 |
| 67 | List.orderedInsert | Data/List/Sort.lean | 1 | 16 |
| 69 | Int.ldiff | Data/Int/Bitwise.lean | 0 | 3 |
| 71 | Finset.choose | Data/Finset/Basic.lean | 0 | 27 |
| 72 | Nat.stirlingFirst | Combinatorics/Enumerative/Stirling.lean | 0 | 10 |
| 74 | Nat.stirlingSecond | Combinatorics/Enumerative/Stirling.lean | 0 | 10 |
| 78 | Multiset.noncommFold | Data/Finset/NoncommProd.lean | 0 | 8 |
| 81 | List.getLastI | Data/List/Defs.lean | 0 | 2 |
| 84 | Finset.piecewise | Data/Finset/Piecewise.lean | 0 | 31 |
| 85 | Equiv.Perm.prodExtendRight | Logic/Equiv/Prod.lean | 0 | 6 |
| 89 | List.lookupAll | Data/List/Sigma.lean | 0 | 11 |
| 91 | Cycle.Nontrivial | Data/List/Cycle.lean | 0 | 6 |
| 93 | Int.land | Data/Int/Bitwise.lean | 0 | 3 |
| 94 | Equiv.sumProdDistrib | Logic/Equiv/Prod.lean | 0 | 4 |
| 96 | Int.lor | Data/Int/Bitwise.lean | 0 | 3 |
| 100 | Equiv.swapCore | Logic/Equiv/Basic.lean | 0 | 3 |
| 101 | Nat.FermatPsp | NumberTheory/FermatPsp.lean | 0 | 6 |
| 102 | Relation.Join | Logic/Relation.lean | 0 | 6 |
| 104 | Finset.pi | Data/Finset/Pi.lean | 0 | 97 |
| 105 | Nat.IsAlmostPrime | NumberTheory/AlmostPrime.lean | 0 | 7 |
| 106 | List.permutations' | Data/List/Defs.lean | 0 | 15 |
| 107 | List.destutter | Data/List/Defs.lean | 1 | 34 |
| 110 | Nat.Perfect | NumberTheory/Divisors.lean | 0 | 8 |
| 112 | List.Pi.cons | Data/List/Pi.lean | 0 | 3 |
| 113 | Finset.attachFin | Data/Finset/Fin.lean | 0 | 9 |
| 114 | Relator.RightTotal | Logic/Relator.lean | 1 | 2 |
| 119 | Nat.factorizationLCMRight | Data/Nat/Factorization/Defs.lean | 1 | 5 |
| 121 | Nat.IsAtMostAlmostPrime | NumberTheory/AlmostPrime.lean | 0 | 2 |
| 122 | Nat.multichoose | Data/Nat/Choose/Basic.lean | 1 | 9 |
| 123 | Nat.smallSchroder | Combinatorics/Enumerative/Schroder.lean | 0 | 3 |
| 124 | ArithmeticFunction.carmichael | NumberTheory/ArithmeticFunction/Carmichael.lean | 0 | 15 |
| 125 | Set.Bounded | Order/RelClasses.lean | 0 | 47 |
| 127 | Nat.doubleFactorial | Data/Nat/Factorial/DoubleFactorial.lean | 1 | 9 |
| 131 | Nat.factorizationLCMLeft | Data/Nat/Factorization/Defs.lean | 1 | 5 |
| 132 | ArithmeticFunction.prodPrimeFactors | NumberTheory/ArithmeticFunction/Misc.lean | 0 | 3 |
| 133 | Equiv.setCongr | Logic/Equiv/Set.lean | 0 | 5 |
| 134 | Function.FromTypes.const | Logic/Function/FromTypes.lean | 0 | 4 |
| 135 | Set.Unbounded | Order/RelClasses.lean | 0 | 38 |
| 137 | ArithmeticFunction.liouville | NumberTheory/ArithmeticFunction/Liouville.lean | 0 | 5 |
| 138 | List.Shortlex | Data/List/Shortlex.lean | 0 | 8 |
| 140 | List.sym2 | Data/List/Sym.lean | 0 | 18 |
| 141 | List.ranges | Data/List/Range.lean | 0 | 5 |
| 142 | DyckWord.toTree | Combinatorics/Enumerative/DyckWord.lean | 0 | 3 |
| 144 | Finset.image₂ | Data/Finset/NAry.lean | 1 | 98 |
| 150 | List.IsRotated | Data/List/Rotate.lean | 0 | 14 |
| 151 | PartialEquiv.EqOnSource | Logic/Equiv/PartialEquiv.lean | 1 | 9 |
| 152 | Relator.BiTotal | Logic/Relator.lean | 1 | 3 |
| 155 | Nat.ofDigits | Data/Nat/Digits/Defs.lean | 0 | 49 |
| 156 | Nat.largeSchroder | Combinatorics/Enumerative/Schroder.lean | 0 | 4 |
| 157 | Composition.boundary | Combinatorics/Enumerative/Composition.lean | 0 | 3 |
| 164 | LucasLehmer.norm_num_ext.sModNat | NumberTheory/LucasLehmer.lean | 0 | 5 |
| 166 | Int.bodd | Data/Int/Bitwise.lean | 1 | 12 |
| 167 | DyckWord.ofTree | Combinatorics/Enumerative/DyckWord.lean | 0 | 2 |
| 168 | DyckWord.take | Combinatorics/Enumerative/DyckWord.lean | 0 | 2 |
| 169 | DyckWord.outsidePart | Combinatorics/Enumerative/DyckWord.lean | 0 | 5 |
| 172 | Equiv.psigmaCongrRight | Logic/Equiv/Defs.lean | 0 | 3 |
| 173 | Equiv.sigmaCongrRight | Logic/Equiv/Defs.lean | 0 | 8 |
| 174 | Int.gcdA | Data/Int/GCD.lean | 0 | 2 |
| 175 | Int.lnot | Data/Int/Bitwise.lean | 0 | 2 |
| 176 | LucasLehmer.sMod | NumberTheory/LucasLehmer.lean | 0 | 5 |
| 177 | LucasLehmer.sZMod | NumberTheory/LucasLehmer.lean | 0 | 2 |
| 179 | Nat.superFactorial | Data/Nat/Factorial/SuperFactorial.lean | 0 | 8 |
| 180 | Composition.cast | Combinatorics/Enumerative/Composition.lean | 0 | 4 |
| 183 | LucasLehmer.s | NumberTheory/LucasLehmer.lean | 0 | 11 |
| 188 | Int.log | Data/Int/Log.lean | 1 | 37 |
| 189 | ArithmeticFunction.ppow | NumberTheory/ArithmeticFunction/Zeta.lean | 0 | 5 |
| 190 | Int.clog | Data/Int/Log.lean | 1 | 22 |
| 191 | Composition.single | Combinatorics/Enumerative/Composition.lean | 1 | 9 |
| 194 | PartialEquiv.IsImage | Logic/Equiv/PartialEquiv.lean | 1 | 4 |
| 195 | List.maximum_of_length_pos | Data/List/MinMax.lean | 0 | 5 |
| 196 | List.minimum_of_length_pos | Data/List/MinMax.lean | 0 | 5 |
| 197 | List.IsZeckendorfRep | Data/Nat/Fib/Zeckendorf.lean | 0 | 2 |
| 199 | List.map₂Right' | Data/List/Defs.lean | 0 | 5 |
| 200 | Nat.ProbablePrime | NumberTheory/FermatPsp.lean | 0 | 2 |
| 201 | List.map₂Right | Data/List/Defs.lean | 0 | 10 |
| 202 | Finset.sup' | Data/Finset/Lattice/Fold.lean | 0 | 61 |
| 209 | List.next | Data/List/Cycle.lean | 0 | 30 |
| 210 | List.HasPeriod | Data/List/PeriodicityLemma.lean | 0 | 12 |
| 211 | ArithmeticFunction.moebius | NumberTheory/ArithmeticFunction/Moebius.lean | 1 | 36 |
| 213 | List.toFinsupp | Data/List/ToFinsupp.lean | 0 | 14 |
| 216 | Finsupp.pi | Data/Finset/Finsupp.lean | 0 | 5 |
| 222 | Multiset.noncommProd | Data/Finset/NoncommProd.lean | 0 | 13 |
| 225 | Equiv.Perm.subtypeCongr | Logic/Equiv/Basic.lean | 0 | 3 |
| 226 | Finset.sigma | Data/Finset/Sigma.lean | 0 | 36 |
| 227 | Cycle.Mem | Data/List/Cycle.lean | 0 | 2 |
| 229 | Equiv.uniqueSigma | Logic/Equiv/Prod.lean | 0 | 2 |
| 230 | List.offDiag | Data/List/OffDiag.lean | 0 | 13 |
| 231 | List.insertionSort | Data/List/Sort.lean | 0 | 16 |
| 232 | Equiv.prodCongrLeft | Logic/Equiv/Prod.lean | 0 | 4 |
| 233 | Equiv.prodCongrRight | Logic/Equiv/Prod.lean | 0 | 6 |
| 234 | Nat.greatestFib | Data/Nat/Fib/Zeckendorf.lean | 0 | 6 |
| 235 | Function.Fiber.mk | Logic/Function/FiberPartition.lean | 0 | 2 |
| 236 | Finsupp.multinomial | Data/Nat/Choose/Multinomial.lean | 1 | 4 |
| 237 | Finset.bipartiteBelow | Combinatorics/Enumerative/DoubleCounting.lean | 0 | 15 |
| 238 | Finset.bipartiteAbove | Combinatorics/Enumerative/DoubleCounting.lean | 0 | 15 |
| 240 | Function.Involutive.toPerm | Logic/Equiv/Basic.lean | 0 | 3 |
| 242 | Nat.chineseRemainder | Data/Nat/ModEq.lean | 0 | 8 |
| 243 | Nat.Subtype.succ | Logic/Denumerable.lean | 0 | 5 |
| 245 | ArithmeticFunction.dirichletInverse | NumberTheory/ArithmeticFunction/Defs.lean | 0 | 5 |
| 247 | Cycle.Subsingleton | Data/List/Cycle.lean | 0 | 7 |
| 248 | Nat.count | Data/Nat/Count.lean | 1 | 48 |
| 250 | List.kerase | Data/List/Sigma.lean | 1 | 26 |
| 251 | Finset.finsupp | Data/Finset/Finsupp.lean | 0 | 17 |

### (iv) New eligible-set size and top-of-ranking movement

**Eligible set: 120 → 256.** The new top of the ranking is dominated by candidates the old counting couldn't see at all (`old_tmc = 0`) rather than by re-ordering among revision 1's survivors:

| Rank | Name | Richness | Old status | Old tmc → New tmc |
|---|---|---|---|---|
| 1 | `Int.greatestOfBdd` | 13 | excluded | 0 → 3 |
| 2 | `Nat.leRec` | 12 | eligible, rank 1 | 3 → 15 |
| 3 | `Nat.binaryRec` | 11 | excluded | 0 → 8 |
| 4 | `Nat.clog` | 10 | eligible, rank 2 | 9 → 34 |
| 5 | `Int.leastOfBdd` | 10 | excluded | 0 → 3 |
| 6 | `List.prev` | 9 | excluded | 0 → 21 |
| 7 | `Finset.strongDownwardInduction` | 9 | excluded | 0 → 2 |
| 8 | `Equiv.sigmaSigmaSubtypeEq` | 9 | excluded | 0 → 2 |
| 9 | `List.recNeNil` | 9 | excluded | 0 → 2 |
| 10 | `Nat.decreasingInduction` | 8 | excluded | 0 → 5 |
| 11 | `Relation.Map` | 8 | eligible, rank 3 | 17 → 17 (unchanged — already well-qualified) |
| 12 | `Nat.log` | 8 | eligible, rank 4 | 22 → 99 |

Revision 1's own top 5 (`Nat.leRec`, `Nat.clog`, `Relation.Map`, `Nat.log`, `Equiv.piEquivPiSubtypeProd`) all remain eligible, but each dropped several ranks (1→2, 2→4, 3→11, 4→12, 5→15) — displaced not by anything wrong with them, but by richer, previously-invisible candidates (dependent-induction principles like `Nat.leRec`'s siblings `Nat.decreasingInduction`/`Int.leastOfBdd`, and `Nat.binaryRec`/`List.prev`) finally getting the theorem-mention credit their real, well-established Mathlib presence always had. **`Finset.pi`** — revision 1's §2 changelog named this as "a new casualty of item (a)'s recalibration... worth a second look" — is now **eligible at rank 104** (`old_tmc=0 → new_tmc=97`), directly resolving the concern that section raised.

### (v) Residual genuinely-zero-mention population

**309 of 950 verified candidates (32.5%) still show `theorem_mention_count = 0`** even under the corrected counting — down from 624 (65.7%) under the old count, but a real, sizeable population remains. Breaking it down for the pending conditional-floor design question (design doc, "whether the floor should be conditional on other supply being thin" — reported here, **not implemented**, per this task's explicit scope):

- Of the 309 zero-mention candidates, **6 (1.9%) are already `casework_tier: rich` or `membership_tier: rich`**: `Nat.fast_choose`, `Nat.digitsAux0`, `Nat.digitsAux1`, `Nat.decidablePrime'`, `Int.castDef`, `Denumerable.raise'Finset` (all `casework_tier: rich`; none reach `membership_tier: rich`). Every one of these also fails at least one *other* gate independently (`richness_floor` or `anti_plumbing`, mostly) — so for this specific population, `theorem_mention_floor` is essentially never the sole reason a casework-rich candidate is excluded.
- Narrowing further to candidates excluded **only** by `theorem_mention_floor` (would be eligible under every other gate as currently configured): **32 candidates**, of which **exactly 1** (`Int.castDef`, `Data/Int/Cast/Defs.lean`, `casework_tier: rich`) has non-`none` casework or membership supply. The other 31 are uniformly `casework_tier: none`, `membership_tier: thin` (never `rich`), `global_tier: none` — genuinely thin across the board, not merely under-mentioned.

**Read on the design question:** at floor 2, post-fix, the population a conditional floor (bypass when other supply is already rich) would actually rescue is small — 1 candidate (`Int.castDef`) among the 32 "floor-only" exclusions, not the 21%-of-149 finding the pre-fix audit reported against revision 1's data. That earlier, larger number was itself partly an artifact of the same undercounting this revision fixes: many of revision 1's 149 "floor-only" casualties are among the 135 that *became eligible* here without needing any conditional-floor logic at all. The residual zero-mention population is now smaller and its casework/membership-rich fraction is smaller too — the corrected measurement did much of the conditional-floor idea's intended work already, for the cases where it would have mattered most.

## 1. Corpus counts (updated)

- Scanned: 964
- Verified (elaborates): 950
- Eligible (passed every gate): 256
- Excluded: 708
  - failed one or more gates: 694
  - curation-excluded (of the gate-eligible pool): 1 (`Nat.digitsAux1` — independently gate-excluded too, see `miner/curation.yaml`)
  - does not elaborate: 14

## 2. Gate-attrition table (sequential, established format; updated)

Start: 950 verified candidates.

| Gate | Fails (of those reaching it) | Cumulative survivors |
|---|---|---|
| (a) theorem_mention_floor | 395 | 555 |
| (b) length_band | 26 | 529 |
| (c) docstring_floor | 12 | 517 |
| (d) dependency_vocabulary | 109 | 408 |
| (e) anti_plumbing | 8 | 400 |
| (g) richness_floor | 144 | 256 |
| (f) fact_supply | 0 | 256 |
| **eligible (pre-curation)** | | **256** |
| curation-excluded | 1 | **255 net eligible after curation** |

Sequential fail counts at each step differ from the independent per-gate rates in §0(iii) because more candidates now survive far enough to *reach* each later gate — e.g. `richness_floor`'s sequential fail count rose from 68 (revision 1) to 144 here purely because far more candidates now clear `theorem_mention_floor` and arrive at `richness_floor` in the first place; `richness_floor`'s own *independent* rate (35.9%, over all 950) is exactly unchanged, confirming richness itself was untouched by this fix.

## 3. Vocabulary-gate exclusions and richness-zero characterization — unchanged from revision 1

`docs/harvest_review_batch3.md` revision 1's §4 (vocabulary-gate exclusions, 195 candidates, unchanged count) and the *nature* of low-richness candidates generally are unaffected by this fix — `dependency_vocabulary`, `anti_plumbing`, `length_band`, `docstring_floor`, and `richness_floor`'s independent fail rate are all bit-for-bit identical to revision 1, since none of their inputs read `theorem_mention_count`. See `docs/theorem_mention_audit.md` and revision 1's own §4/§6 for that material; not reproduced here. (Revision 1's specific "68 richness-zero-only exclusions" *list* is superseded by a larger set of 144 under this revision — candidates that previously failed both `theorem_mention_floor` and `richness_floor` together now fail only the latter — but this is a knock-on effect of more candidates reaching that far, not a change in what richness itself measures; see §0(v) above for the genuinely-zero-*mention* population, which is the axis this revision's fix actually bears on.)

## 4. Return-shape composition (updated)

Overall eligible set (256, up from 120):

| Shape | Count |
|---|---|
| value | 148 |
| prop | 65 |
| bundled | 43 |

Top 50 by rank (of 256 eligible):

| Shape | Count |
|---|---|
| value | 23 |
| prop | 16 |
| bundled | 11 |

Module distribution of the eligible set (top-level corner): `Data` 121, `Logic` 69, `Order` 25, `NumberTheory` 20, `Combinatorics` 18, `Algebra` 3 — the widened corpus's non-`Data`/`Logic` corners (`Order`, `NumberTheory`, `Combinatorics`) now contribute meaningfully (63 of 256, 25%) where revision 1 had them heavily underrepresented by the undercounted floor.

## 5. Detail cards: new top 10

### 1. Int.greatestOfBdd
*Data/Int/LeastGreatest.lean* — new to the eligible set (`old_tmc=0 → new_tmc=3`)

**Docstring:** A computable version of `exists_greatest_of_bdd`: given a decidable predicate on the integers, with an explicit upper bound and a proof that it is somewhere true, return the greatest value for which the predicate is true.

**Richness:** 13, return-shape `value`. **Notes:** Genuine existential/hypothesis-binder-rich construction (a computable witness extraction under a boundedness hypothesis) — exactly the shape of candidate the theorem-mention floor was hiding under the old count.

### 2. Nat.leRec
*Data/Nat/Init.lean* — was revision 1's rank 1 (`old_tmc=3 → new_tmc=15`), now rank 2. Unchanged in substance; see revision 1's own detail card.

### 3. Nat.binaryRec
*Data/Nat/BinaryRec.lean* — new to the eligible set (`old_tmc=0 → new_tmc=8`)

**Docstring:** A recursion principle for `bit` representations of natural numbers. For a predicate `motive : Nat → Sort u`, if instances can be constructed for natural numbers of the form `bit b n`, they can be constructed for all natural numbers.

**Richness:** 11, return-shape `value`. **Notes:** A real induction/recursion principle over binary representations — this is exactly the kind of foundational-but-substantive `Data/Nat` definition the widened-corpus redesign was meant to surface, previously invisible entirely under the old floor (raw `mention_count=26`, per `docs/theorem_mention_audit.md`'s own sample, vs. `theorem_mention_count=0` before this fix).

### 4. Nat.clog
Unchanged in substance from revision 1's rank-2 card (now rank 4, `old_tmc=9 → new_tmc=34`).

### 5. Int.leastOfBdd
*Data/Int/LeastGreatest.lean* — the least-value dual of rank 1's `Int.greatestOfBdd`, same story (`old_tmc=0 → new_tmc=3`). Both surfacing together is expected, not a coincidence — the same pattern as `Nat.log`/`Nat.clog` and `Int.leInduction`/`Int.leInductionDown` pairing up in revision 1.

### 6. List.prev
*Data/List/Cycle.lean* — new to the eligible set (`old_tmc=0 → new_tmc=21`)

**Docstring:** Given an element `x : α` of `l : List α` such that `x ∈ l`, get the previous element of `l`. This works from head to tail (including a check for last element) so it will match on first hit, ignoring later duplicates.

**Richness:** 9, return-shape `value`. **Notes:** Genuine multi-case conditional structure (three-way pattern match with an `if`/`else` inside), plus worked examples in its own docstring — strong dossier raw material.

### 7. Finset.strongDownwardInduction
*Data/Finset/Card.lean* — new to the eligible set (`old_tmc=0 → new_tmc=2`). A genuine downward-induction principle on finset cardinality, dual to `Finset.strongInduction`.

### 8. Equiv.sigmaSigmaSubtypeEq
*Logic/Equiv/Basic.lean* — new to the eligible set (`old_tmc=0 → new_tmc=2`). A specialized dependent-sigma equivalence; genuinely structured (`bundled` shape), not lambda-arm noise.

### 9. List.recNeNil
*Data/List/Induction.lean* — new to the eligible set (`old_tmc=0 → new_tmc=2`). A dependent recursion principle for nonempty lists — same family as `Nat.leRec`/`Nat.decreasingInduction`.

### 10. Nat.decreasingInduction
*Data/Nat/Init.lean* — new to the eligible set (`old_tmc=0 → new_tmc=5`). Decreasing induction, the downward counterpart to `Nat.leRec`'s upward recursion — both from the same file, both previously invisible under the old count.

## 6. Full ranked table (all 256 eligible)

Description: docstring (truncated to fit) where present. `old_tmc`/`new_tmc` columns show the theorem-mention count before and after this revision's fix, for direct auditability of every rank's movement.

| Rank | Name | Module | Description | Richness | Return | Signature | CW | Mem | Glob | Score | old_tmc | new_tmc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Int.greatestOfBdd | Data/Int/LeastGreatest.lean | A computable version of `exists_greatest_of_bdd`: given a decidable predicate on the inte… | 13 | value | `{P : ℤ → Prop} [DecidablePred P] (b : ℤ) (Hb : ∀ (z : ℤ), P z → z ≤ b) (Hinh : ∃ z, P z) : { ub // P ub ∧ ∀ (z : ℤ), P z → z ≤ ub }` | none | none | thin | 141.62 | 0 | 3 |
| 2 | Nat.leRec | Data/Nat/Init.lean | Recursion starting at a non-zero number: given a map `C k → C (k+1)` for each `k ≥ n`, th… | 12 | value | `{n : ℕ} {motive : (m : ℕ) → n ≤ m → Sort u_1} (refl : motive n ⋯) (le_succ_of_le : ⦃k : ℕ⦄ → (h : n ≤ k) → motive k h → motive (k + 1) ⋯) {m : ℕ} (h : n ≤ m) : motive m h` | none | none | rich | 132.49 | 3 | 15 |
| 3 | Nat.binaryRec | Data/Nat/BinaryRec.lean | A recursion principle for `bit` representations of natural numbers.   For a predicate `mo… | 11 | value | `{motive : ℕ → Sort u} (zero : motive 0) (bit : (b : Bool) → (n : ℕ) → motive n → motive (Nat.bit b n)) (n : ℕ) : motive n` | none | none | rich | 123.72 | 0 | 8 |
| 4 | Nat.clog | Data/Nat/Log.lean | `clog b n`, is the upper logarithm of natural number `n` in base `b`. It returns the smal… | 10 | value | `(b n : ℕ) : ℕ` | rich | none | rich | 113.94 | 9 | 34 |
| 5 | Int.leastOfBdd | Data/Int/LeastGreatest.lean | A computable version of `exists_least_of_bdd`: given a decidable predicate on the integer… | 10 | value | `{P : ℤ → Prop} [DecidablePred P] (b : ℤ) (Hb : ∀ (z : ℤ), P z → b ≤ z) (Hinh : ∃ z, P z) : { lb // P lb ∧ ∀ (z : ℤ), P z → lb ≤ z }` | none | none | thin | 111.56 | 0 | 3 |
| 6 | List.prev | Data/List/Cycle.lean | Given an element `x : α` of `l : List α` such that `x ∈ l`, get the previous element of `… | 9 | value | `{α : Type u_1} [DecidableEq α] (l : List α) (x : α) : x ∈ l → α` | none | thin | rich | 103.69 | 0 | 21 |
| 7 | Finset.strongDownwardInduction | Data/Finset/Card.lean | Suppose that, given that `p t` can be defined on all supersets of `s` of cardinality less… | 9 | value | `{α : Type u_1} {p : Finset α → Sort u_4} {n : ℕ} (H : (t₁ : Finset α) → ({t₂ : Finset α} → t₂.card ≤ n → t₁ ⊂ t₂ → p t₂) → t₁.card ≤ n → p t₁) (s : Finset α) : s.card ≤ n → p s` | none | thin | thin | 103.49 | 0 | 2 |
| 8 | Equiv.sigmaSigmaSubtypeEq | Logic/Equiv/Basic.lean | A specialization of `sigmaSigmaSubtype` to the case where the second base does not depend… | 9 | bundled | `{α : Type u_9} {β : Type u_10} {γ : α → β → Type u_11} (a : α) (b : β) : { s // s.fst = a ∧ s.snd.fst = b } ≃ γ a b` | none | none | thin | 103.47 | 0 | 2 |
| 9 | List.recNeNil | Data/List/Induction.lean | A dependent recursion principle for nonempty lists. Useful for dealing with operations li… | 9 | value | `{α : Type u_1} {motive : (l : List α) → l ≠ [] → Sort u_2} (singleton : (x : α) → motive [x] ⋯) (cons : (x : α) → (xs : List α) → (h : xs ≠ []) → motive xs h → motive (x :: xs) ⋯) (l : List α) (h : l ≠ []) : motive l h` | none | thin | thin | 101.66 | 0 | 2 |
| 10 | Nat.decreasingInduction | Data/Nat/Init.lean | Decreasing induction: if `P (k+1)` implies `P k` for all `k < n`, then `P n` implies `P m… | 8 | value | `{n : ℕ} {motive : (m : ℕ) → m ≤ n → Sort u_1} (of_succ : (k : ℕ) → (h : k < n) → motive (k + 1) h → motive k ⋯) (self : motive n ⋯) {m : ℕ} (mn : m ≤ n) : motive m mn` | none | none | rich | 95.54 | 0 | 5 |
| 11 | Relation.Map | Logic/Relation.lean | The map of a relation `r` through a pair of functions pushes the relation to the codomain… | 8 | prop | `{α : Type u_1} {β : Type u_2} {γ : Type u_3} {δ : Type u_4} (r : α → β → Prop) (f : α → γ) (g : β → δ) : γ → δ → Prop` | none | thin | rich | 94.55 | 17 | 17 |
| 12 | Nat.log | Data/Nat/Log.lean | `log b n`, is the logarithm of natural number `n` in base `b`. It returns the largest `k … | 8 | value | `(b n : ℕ) : ℕ` | rich | none | rich | 93.83 | 22 | 99 |
| 13 | Function.Embedding.setValue | Logic/Embedding/Basic.lean | Change the value of an embedding `f` at one point. If the prescribed image is already occ… | 8 | bundled | `{α : Sort u_1} {β : Sort u_2} (f : α ↪ β) (a : α) (b : β) [(a' : α) → Decidable (a' = a)] [(a' : α) → Decidable (f a' = b)] : α ↪ β` | none | none | thin | 92.78 | 0 | 4 |
| 14 | Equiv.subtypePreimage | Logic/Equiv/Basic.lean | For a fixed function `x₀ : {a // p a} → β` defined on a subtype of `α`, the subtype of fu… | 8 | bundled | `{α : Sort u_1} {β : Sort u_4} (p : α → Prop) [DecidablePred p] (x₀ : { a // p a } → β) : { x // x ∘ Subtype.val = x₀ } ≃ ({ a // ¬p a } → β)` | none | none | thin | 91.67 | 0 | 2 |
| 15 | Equiv.piEquivPiSubtypeProd | Logic/Equiv/Prod.lean | The type `∀ (i : α), β i` can be split as a product by separating the indices in `α` depe… | 8 | bundled | `{α : Type u_9} (p : α → Prop) (β : α → Type u_10) [DecidablePred p] : ((i : α) → β i) ≃ ((i : { x // p x }) → β ↑i) × ((i : { x // ¬p x }) → β ↑i)` | none | none | rich | 90.62 | 4 | 5 |
| 16 | Equiv.ofLeftInverse | Logic/Equiv/Set.lean | If `f : α → β` has a left-inverse when `α` is nonempty, then `α` is computably equivalent… | 7 | bundled | `{α : Sort u_3} {β : Type u_4} (f : α → β) (f_inv : Nonempty α → β → α) (hf : ∀ (h : Nonempty α), Function.LeftInverse (f_inv h) f) : α ≃ ↑(Set.range f)` | none | thin | thin | 90.05 | 0 | 2 |
| 17 | Int.leInduction | Data/Int/Init.lean | See `Int.inductionOn'` for an induction in both directions. | 8 | value | `{m : ℤ} {motive : (n : ℤ) → m ≤ n → Sort u_1} (base : motive m ⋯) (succ : (n : ℤ) → (hmn : m ≤ n) → motive n hmn → motive (n + 1) ⋯) (n : ℤ) (hmn : m ≤ n) : motive n hmn` | none | none | thin | 88.38 | 4 | 4 |
| 18 | Int.leInductionDown | Data/Int/Init.lean | See `Int.inductionOn'` for an induction in both directions. | 8 | value | `{m : ℤ} {motive : (n : ℤ) → n ≤ m → Sort u_1} (base : motive m ⋯) (pred : (n : ℤ) → (hnm : n ≤ m) → motive n hnm → motive (n - 1) ⋯) (n : ℤ) (hnm : n ≤ m) : motive n hnm` | none | none | thin | 88.38 | 2 | 2 |
| 19 | Relation.Fibration | Logic/Relation.lean | A function `f : α → β` is a fibration between the relation `rα` and `rβ` if for all   `a … | 7 | prop | `{α : Type u_1} {β : Type u_2} (rα : α → α → Prop) (rβ : β → β → Prop) (f : α → β) : Prop` | none | thin | rich | 84.75 | 1 | 11 |
| 20 | Nat.nthRoot | Data/Nat/NthRoot/Defs.lean | `Nat.nthRoot n a = ⌊(a : ℝ) ^ (1 / n : ℝ)⌋₊` defined in terms of natural numbers.  We use… | 7 | value | `: ℕ → ℕ → ℕ` | rich | none | rich | 82.09 | 0 | 15 |
| 21 | Multiset.noncommFoldr | Data/Finset/NoncommProd.lean | Fold of a `s : Multiset α` with `f : α → β → β`, given a proof that `LeftCommutative f` o… | 7 | value | `{α : Type u_3} {β : Type u_4} (f : α → β → β) (s : Multiset α) (comm : {x | x ∈ s}.Pairwise fun x y => ∀ (b : β), f x (f y b) = f y (f x b)) (b : β) : β` | none | thin | thin | 81.07 | 0 | 4 |
| 22 | Function.extend | Logic/Function/Basic.lean | Extension of a function `g : α → γ` along a function `f : α → β`.  For every `a : α`, `f … | 6 | value | `{α : Sort u_1} {β : Sort u_2} {γ : Sort u_3} (f : α → β) (g : α → γ) (j : β → γ) : β → γ` | none | none | rich | 80.21 | 12 | 26 |
| 23 | Equiv.piCongrRight | Logic/Equiv/Basic.lean | A family of equivalences `∀ a, β₁ a ≃ β₂ a` generates an equivalence between `∀ a, β₁ a` … | 7 | bundled | `{α : Sort u_1} {β₁ : α → Sort u_9} {β₂ : α → Sort u_10} (F : (a : α) → β₁ a ≃ β₂ a) : ((a : α) → β₁ a) ≃ ((a : α) → β₂ a)` | none | none | thin | 79.91 | 1 | 2 |
| 24 | Nat.evenOddRec | Data/Nat/EvenOddRec.lean | Recursion principle on even and odd numbers: if we have `P 0`, and for all `i : ℕ` we can… | 6 | value | `{P : ℕ → Sort u_1} (h0 : P 0) (h_even : (n : ℕ) → P n → P (2 * n)) (h_odd : (n : ℕ) → P n → P (2 * n + 1)) (n : ℕ) : P n` | none | none | thin | 74.31 | 0 | 3 |
| 25 | Relation.CutExpand | Logic/Hydra.lean | The relation that specifies valid moves in our hydra game. `CutExpand r s' s`   means tha… | 5 | prop | `{α : Type u_1} (r : α → α → Prop) (s' s : Multiset α) : Prop` | none | thin | rich | 73.41 | 0 | 19 |
| 26 | Finset.strongInduction | Data/Finset/Card.lean | Suppose that, given objects defined on all strict subsets of any finset `s`, one knows ho… | 6 | value | `{α : Type u_1} {p : Finset α → Sort u_4} (H : (s : Finset α) → ((t : Finset α) → t ⊂ s → p t) → p s) (s : Finset α) : p s` | none | thin | thin | 73.15 | 0 | 2 |
| 27 | Nat.bitCasesOn | Data/Nat/BinaryRec.lean | For a predicate `motive : Nat → Sort u`, if instances can be   constructed for natural nu… | 6 | value | `{motive : ℕ → Sort u} (n : ℕ) (bit : (b : Bool) → (n : ℕ) → motive (Nat.bit b n)) : motive n` | none | none | rich | 73.02 | 0 | 5 |
| 28 | ArithmeticFunction.dirichletInverseFun | NumberTheory/ArithmeticFunction/Defs.lean | Given an inverse of `f 1`, construct the Dirichlet inverse of `f`. We use `Invertible` to… | 6 | value | `{R : Type u_1} [Ring R] (f : ℕ → R) (hf : Invertible (f 1)) (n : ℕ) : R` | none | none | thin | 72.67 | 0 | 3 |
| 29 | List.nextOr | Data/List/Cycle.lean | Return the `z` such that `x :: z :: _` appears in `xs`, or `default` if there is no such … | 6 | value | `{α : Type u_1} [DecidableEq α] : List α → α → α → α` | none | thin | rich | 72.61 | 0 | 12 |
| 30 | Equiv.sumCompl | Logic/Equiv/Sum.lean | For any predicate `p` on `α`, the sum of the two subtypes `{a // p a}` and its complement… | 6 | bundled | `{α : Type u_9} (p : α → Prop) [DecidablePred p] : { a // p a } ⊕ { a // ¬p a } ≃ α` | none | none | rich | 72.33 | 5 | 11 |
| 31 | Equiv.sumPiEquivProdPi | Logic/Equiv/Prod.lean | The type of dependent functions on a sum type `ι ⊕ ι'` is equivalent to the type of pairs… | 6 | bundled | `{ι : Type u_10} {ι' : Type u_11} (π : ι ⊕ ι' → Type u_9) : ((i : ι ⊕ ι') → π i) ≃ ((i : ι) → π (Sum.inl i)) × ((i' : ι') → π (Sum.inr i'))` | none | none | rich | 71.22 | 6 | 9 |
| 32 | Function.dcomp | Logic/Function/Defs.lean | Composition of dependent functions: `(f ∘' g) x = f (g x)`, where type of `g x` depends o… | 6 | value | `{α : Sort u₁} {β : α → Sort u₂} {φ : {x : α} → β x → Sort u₃} (f : {x : α} → (y : β x) → φ y) (g : (x : α) → β x) (x : α) : φ (g x)` | none | none | thin | 70.62 | 0 | 2 |
| 33 | Composition.embedding | Combinatorics/Enumerative/Composition.lean | Embedding the `i`-th block of a composition (identified with `Fin (c.blocksFun i)`) into … | 6 | bundled | `{n : ℕ} (c : Composition n) (i : Fin c.length) : Fin (c.blocksFun i) ↪o Fin n` | none | none | rich | 70.27 | 0 | 12 |
| 34 | finSumNatEquiv | Logic/Equiv/Fin/Basic.lean | Equivalence between `Fin n ⊕ ℕ` and `ℕ` that sends `inl (a : Fin n)` to `(a : ℕ)` and `in… | 6 | bundled | `(n : ℕ) : Fin n ⊕ ℕ ≃ ℕ` | none | none | thin | 69.91 | 3 | 3 |
| 35 | DependsOn | Logic/Function/DependsOn.lean | A function `f` depends on `s` if, whenever `x` and `y` coincide over `s`, `f x = f y`.  I… | 5 | prop | `{ι : Type u_1} {α : ι → Type u_2} {β : Type u_3} (f : ((i : ι) → α i) → β) (s : Set ι) : Prop` | none | thin | rich | 65.65 | 21 | 21 |
| 36 | Function.Semiconj | Logic/Function/Conjugate.lean | We say that `f : α → β` semiconjugates `ga : α → α` to `gb : β → β` if `f ∘ ga = gb ∘ f`.… | 5 | prop | `{α : Type u_1} {β : Type u_2} (f : α → β) (ga : α → α) (gb : β → β) : Prop` | none | thin | rich | 65.03 | 17 | 22 |
| 37 | Finset.Colex.IsInitSeg | Combinatorics/Colex.lean | `𝒜` is an initial segment of the colexicographic order on sets of `r`, and that if `t` is… | 5 | prop | `{α : Type u_1} [LinearOrder α] (𝒜 : Finset (Finset α)) (r : ℕ) : Prop` | none | thin | rich | 64.94 | 0 | 5 |
| 38 | Nat.psub | Data/Nat/PSub.lean | Partial subtraction operation. Returns `psub m n = some k`   if `m = n + k`, otherwise `n… | 5 | value | `(m : ℕ) : ℕ → Option ℕ` | rich | none | rich | 64.58 | 0 | 8 |
| 39 | Directed | Order/Directed.lean | A family of elements of `α` is directed (with respect to a relation `≼` on `α`)   if ther… | 5 | prop | `{α : Type u_1} {ι : Sort u_3} (r : α → α → Prop) (f : ι → α) : Prop` | none | thin | rich | 63.72 | 445 | 445 |
| 40 | DirectedOn | Order/Directed.lean | A subset of `α` is directed if there is an element of the set `≼`-above any   pair of ele… | 5 | prop | `{α : Type u_1} (r : α → α → Prop) (s : Set α) : Prop` | none | thin | rich | 62.89 | 175 | 175 |
| 41 | MonovaryOn | Order/Monotone/Monovary.lean | `f` monovaries with `g` on `s` if `g i < g j` implies `f i ≤ f j` for all `i, j ∈ s`. | 5 | prop | `{ι : Type u_1} {α : Type u_3} {β : Type u_4} [Preorder α] [Preorder β] (f : ι → α) (g : ι → β) (s : Set ι) : Prop` | none | thin | rich | 62.38 | 77 | 77 |
| 42 | AntivaryOn | Order/Monotone/Monovary.lean | `f` antivaries with `g` on `s` if `g i < g j` implies `f j ≤ f i` for all `i, j ∈ s`. | 5 | prop | `{ι : Type u_1} {α : Type u_3} {β : Type u_4} [Preorder α] [Preorder β] (f : ι → α) (g : ι → β) (s : Set ι) : Prop` | none | thin | rich | 62.38 | 76 | 76 |
| 43 | StrongLT | Order/Basic.lean | A function `a` is strongly less than a function `b` if `a i < b i` for all `i`. | 5 | prop | `{ι : Type u_1} {π : ι → Type u_4} [(i : ι) → LT (π i)] (a b : (i : ι) → π i) : Prop` | none | thin | rich | 62.19 | 6 | 6 |
| 44 | WCovBy | Order/Defs/PartialOrder.lean | `WCovBy a b` means that `a = b` or `b` covers `a`. This means that `a ≤ b` and there is n… | 5 | prop | `{α : Type u_1} [Preorder α] (a b : α) : Prop` | none | thin | rich | 61.51 | 23 | 23 |
| 45 | List.Forall | Data/List/Defs.lean | `l.Forall p` is equivalent to `∀ a ∈ l, p a`, but unfolds directly to a conjunction, i.e.… | 5 | prop | `{α : Type u_1} (p : α → Prop) : List α → Prop` | none | thin | rich | 61.49 | 5 | 69 |
| 46 | Monovary | Order/Monotone/Monovary.lean | `f` monovaries with `g` if `g i < g j` implies `f i ≤ f j`. | 5 | prop | `{ι : Type u_1} {α : Type u_3} {β : Type u_4} [Preorder α] [Preorder β] (f : ι → α) (g : ι → β) : Prop` | none | thin | rich | 61.38 | 133 | 133 |
| 47 | Antivary | Order/Monotone/Monovary.lean | `f` antivaries with `g` if `g i < g j` implies `f j ≤ f i`. | 5 | prop | `{ι : Type u_1} {α : Type u_3} {β : Type u_4} [Preorder α] [Preorder β] (f : ι → α) (g : ι → β) : Prop` | none | thin | rich | 61.38 | 131 | 131 |
| 48 | hyperoperation | Data/Nat/Hyperoperation.lean | Implementation of the hyperoperation sequence where `hyperoperation n m k` is the `n`th h… | 5 | value | `: ℕ → ℕ → ℕ → ℕ` | rich | none | rich | 61.29 | 10 | 10 |
| 49 | CovBy | Order/Defs/PartialOrder.lean | `CovBy a b` means that `b` covers `a`. This means that `a < b` and there is no element in… | 5 | prop | `{α : Type u_2} [LT α] (a b : α) : Prop` | none | thin | rich | 61.29 | 66 | 66 |
| 50 | Equiv.piFinsetUnion | Data/Finset/Basic.lean | The type of dependent functions on the disjoint union of finsets `s ∪ t` is equivalent to… | 5 | bundled | `{ι : Type u_5} [DecidableEq ι] (α : ι → Type u_4) {s t : Finset ι} (h : Disjoint s t) : ((i : ↥s) → α ↑i) × ((i : ↥t) → α ↑i) ≃ ((i : ↥(s ∪ t)) → α ↑i)` | none | none | rich | 61.21 | 5 | 6 |
| 51 | OrderHom.antisymmetrization | Order/Antisymmetrization.lean | Turns an order homomorphism from `α` to `β` into one from `Antisymmetrization α` to `Anti… | 5 | value | `{α : Type u_1} {β : Type u_2} [Preorder α] [Preorder β] (f : α →o β) : (Antisymmetrization α fun x1 x2 => x1 ≤ x2) → o Antisymmetrization β fun x1 x2 => x1 ≤ x2` | none | none | thin | 61.20 | 2 | 2 |
| 52 | subtypeOrLeftEmbedding | Logic/Embedding/Basic.lean | A subtype `{x // p x ∨ q x}` over a disjunction of `p q : α → Prop` can be injectively sp… | 5 | bundled | `{α : Type u_1} (p q : α → Prop) [DecidablePred p] : { x // p x ∨ q x } ↪ { x // p x } ⊕ { x // q x }` | none | none | thin | 61.18 | 3 | 3 |
| 53 | Function.updateFinset | Data/Finset/Update.lean | `updateFinset x s y` is the vector `x` with the coordinates in `s` changed to the values … | 5 | value | `{ι : Type u_1} {π : ι → Sort u_2} [DecidableEq ι] (x : (i : ι) → π i) (s : Finset ι) (y : (i : ↥s) → π ↑i) (i : ι) : π i` | none | thin | rich | 60.69 | 1 | 14 |
| 54 | Set.piecewise | Logic/Function/Basic.lean | `s.piecewise f g` is the function equal to `f` on the set `s`, and to `g` on its compleme… | 5 | value | `{α : Type u} {β : α → Sort v} (s : Set α) (f g : (i : α) → β i) [(j : α) → Decidable (j ∈ s)] (i : α) : β i` | none | thin | rich | 60.58 | 7 | 47 |
| 55 | ExistsUnique | Logic/ExistsUnique.lean | For `p : α → Prop`, `ExistsUnique p` means that there exists a unique `x : α` with `p x`. | 5 | prop | `{α : Sort u_1} (p : α → Prop) : Prop` | none | thin | rich | 60.50 | 10 | 10 |
| 56 | Finset.sigmaLift | Data/Finset/Sigma.lean | Lifts maps `α i → β i → Finset (γ i)` to a map `Σ i, α i → Σ i, β i → Finset (Σ i, γ i)`. | 5 | value | `{ι : Type u_1} {α : ι → Type u_2} {β : ι → Type u_3} {γ : ι → Type u_4} [DecidableEq ι] (f : ⦃i : ι⦄ → α i → β i → Finset (γ i)) (a : Sigma α) (b : Sigma β) : Finset (Sigma γ)` | none | thin | rich | 60.50 | 0 | 8 |
| 57 | Int.bitwise | Data/Int/Bitwise.lean | `Int.bitwise` applies the function `f` to pairs of bits in the same position in   the bin… | 5 | value | `(f : Bool → Bool → Bool) : ℤ → ℤ → ℤ` | none | none | rich | 60.25 | 0 | 6 |
| 58 | List.sym | Data/List/Sym.lean | `xs.sym n` is all unordered `n`-tuples from the list `xs` in some order. | 5 | value | `{α : Type u_1} (n : ℕ) : List α → List (Sym α n)` | none | thin | rich | 59.94 | 2 | 53 |
| 59 | AList.insertRec | Data/List/AList.lean | Recursion on an `AList`, using `insert`. Use as `induction l`. | 5 | value | `{α : Type u} {β : α → Type v} [DecidableEq α] {C : AList β → Sort u_1} (H0 : C ∅) (IH : (a : α) → (b : β a) → (l : AList β) → a ∉ l → C l → C (AList.insert a b l)) (l : AList β) : C l` | none | thin | thin | 59.52 | 0 | 3 |
| 60 | Function.FactorsThrough | Logic/Function/Basic.lean | g factors through f : `f a = f b → g a = g b` | 5 | prop | `{α : Sort u_1} {β : Sort u_2} {γ : Sort u_3} (g : α → γ) (f : α → β) : Prop` | none | thin | rich | 58.52 | 3 | 7 |
| 61 | Equiv.sumAssoc | Logic/Equiv/Sum.lean | Sum of types is associative up to an equivalence. | 5 | bundled | `(α : Type u_9) (β : Type u_10) (γ : Type u_11) : (α ⊕ β) ⊕ γ ≃ α ⊕ β ⊕ γ` | none | none | rich | 57.80 | 7 | 13 |
| 62 | Nat.ceilRoot | Data/Nat/Factorization/Root.lean | Ceiling root of a natural number. This divides the valuation of every prime number roundi… | 4 | value | `(n a : ℕ) : ℕ` | rich | none | thin | 56.38 | 0 | 4 |
| 63 | Nat.floorRoot | Data/Nat/Factorization/Root.lean | Flooring root of a natural number. This divides the valuation of every prime number round… | 4 | value | `(n a : ℕ) : ℕ` | rich | none | thin | 56.24 | 0 | 4 |
| 64 | Equiv.subtypeEquiv | Logic/Equiv/Basic.lean | If `α` is equivalent to `β` and the predicates `p : α → Prop` and `q : β → Prop` are equi… | 4 | bundled | `{α : Sort u_1} {β : Sort u_4} {p : α → Prop} {q : β → Prop} (e : α ≃ β) (h : ∀ (a : α), p a ↔ q (e a)) : { a // p a } ≃ { b // q b }` | none | none | rich | 53.88 | 2 | 14 |
| 65 | List.dlookup | Data/List/Sigma.lean | `dlookup a l` is the first value in `l` corresponding to the key `a`,   or `none` if no s… | 4 | value | `{α : Type u} {β : α → Type v} [DecidableEq α] (a : α) : List (Sigma β) → Option (β a)` | none | thin | rich | 52.93 | 0 | 29 |
| 66 | List.choose | Data/List/Defs.lean | Given a decidable predicate `p` and a proof of existence of `a ∈ l` such that `p a`, choo… | 4 | value | `{α : Type u_1} (p : α → Prop) [DecidablePred p] (l : List α) (hp : ∃ a ∈ l, p a) : α` | none | thin | rich | 52.64 | 0 | 8 |
| 67 | List.orderedInsert | Data/List/Sort.lean | `orderedInsert a l` inserts `a` into `l` at such that   `orderedInsert a l` is sorted if … | 4 | value | `{α : Type u_1} (r : α → α → Prop) [DecidableRel r] (a : α) : List α → List α` | none | thin | rich | 52.63 | 1 | 16 |
| 68 | Set.Pairwise | Logic/Pairwise.lean | The relation `r` holds pairwise on the set `s` if `r x y` for all *distinct* `x y ∈ s`. | 4 | prop | `{α : Type u_1} (s : Set α) (r : α → α → Prop) : Prop` | none | thin | rich | 52.44 | 67 | 174 |
| 69 | Int.ldiff | Data/Int/Bitwise.lean | `ldiff a b` performs bitwise set difference. For each corresponding   pair of bits taken … | 4 | value | `: ℤ → ℤ → ℤ` | rich | none | thin | 52.41 | 0 | 3 |
| 70 | IsDvdSequence | Data/Nat/DvdSequence.lean | A function `f : α → β` is a divisibility sequence if `a ∣ b` implies `f a ∣ f b`. | 4 | prop | `{α : Type u_1} {β : Type u_2} [Dvd α] [Dvd β] (f : α → β) : Prop` | none | thin | rich | 52.25 | 7 | 7 |
| 71 | Finset.choose | Data/Finset/Basic.lean | Given a finset `l` and a predicate `p`, associate to a proof that there is a unique eleme… | 4 | value | `{α : Type u_1} (p : α → Prop) [DecidablePred p] (l : Finset α) (hp : ∃! a, a ∈ l ∧ p a) : α` | none | thin | rich | 52.02 | 0 | 27 |
| 72 | Nat.stirlingFirst | Combinatorics/Enumerative/Stirling.lean | `Nat.stirlingFirst n k` is the (unsigned) Stirling number of the first kind, counting the… | 4 | value | `: ℕ → ℕ → ℕ` | rich | none | rich | 51.93 | 0 | 10 |
| 73 | Equiv.piCurry | Logic/Equiv/Basic.lean | Dependent `curry` equivalence: the type of dependent functions on `Σ i, β i` is equivalen… | 4 | bundled | `{α : Type u_11} {β : α → Type u_9} (γ : (a : α) → β a → Type u_10) : ((x : (i : α) × β i) → γ x.fst x.snd) ≃ ((a : α) → (b : β a) → γ a b)` | none | none | thin | 51.89 | 2 | 2 |
| 74 | Nat.stirlingSecond | Combinatorics/Enumerative/Stirling.lean | `Nat.stirlingSecond n k` is the Stirling number of the second kind, counting the number o… | 4 | value | `: ℕ → ℕ → ℕ` | rich | none | rich | 51.85 | 0 | 10 |
| 75 | StrictMono | Order/Monotone/Defs.lean | A function `f` is strictly monotone if `a < b` implies `f a < f b`. | 4 | prop | `{α : Type u} {β : Type v} [Preorder α] [Preorder β] (f : α → β) : Prop` | none | thin | rich | 51.74 | 929 | 929 |
| 76 | StrictAnti | Order/Monotone/Defs.lean | A function `f` is strictly antitone if `a < b` implies `f b < f a`. | 4 | prop | `{α : Type u} {β : Type v} [Preorder α] [Preorder β] (f : α → β) : Prop` | none | thin | rich | 51.74 | 234 | 234 |
| 77 | Nat.findGreatest | Data/Nat/Find.lean | `Nat.findGreatest P n` is the largest `i ≤ n` such that `P i` holds, or `0` if no such `i… | 4 | value | `(P : ℕ → Prop) [DecidablePred P] : ℕ → ℕ` | none | none | rich | 51.71 | 14 | 15 |
| 78 | Multiset.noncommFold | Data/Finset/NoncommProd.lean | Fold of a `s : Multiset α` with an associative `op : α → α → α`, given a proofs that `op`… | 4 | value | `{α : Type u_3} (op : α → α → α) [assoc : Std.Associative op] (s : Multiset α) (comm : {x | x ∈ s}.Pairwise fun x y => op x y = op y x) : α → α` | none | thin | rich | 51.40 | 0 | 8 |
| 79 | Monotone | Order/Monotone/Defs.lean | A function `f` is monotone if `a ≤ b` implies `f a ≤ f b`. | 4 | prop | `{α : Type u} {β : Type v} [Preorder α] [Preorder β] (f : α → β) : Prop` | none | thin | rich | 51.33 | 1296 | 1296 |
| 80 | Antitone | Order/Monotone/Defs.lean | A function `f` is antitone if `a ≤ b` implies `f b ≤ f a`. | 4 | prop | `{α : Type u} {β : Type v} [Preorder α] [Preorder β] (f : α → β) : Prop` | none | thin | rich | 51.33 | 664 | 665 |
| 81 | List.getLastI | Data/List/Defs.lean | The last element of a list, with the default if list empty | 4 | value | `{α : Type u_1} [Inhabited α] : List α → α` | none | thin | thin | 51.33 | 0 | 2 |
| 82 | StrictMonoOn | Order/Monotone/Defs.lean | A function `f` is strictly monotone on `s` if, for all `a, b ∈ s`, `a < b` implies `f a <… | 4 | prop | `{α : Type u} {β : Type v} [Preorder α] [Preorder β] (f : α → β) (s : Set α) : Prop` | none | thin | rich | 50.66 | 151 | 151 |
| 83 | StrictAntiOn | Order/Monotone/Defs.lean | A function `f` is strictly antitone on `s` if, for all `a, b ∈ s`, `a < b` implies `f b <… | 4 | prop | `{α : Type u} {β : Type v} [Preorder α] [Preorder β] (f : α → β) (s : Set α) : Prop` | none | thin | rich | 50.66 | 101 | 101 |
| 84 | Finset.piecewise | Data/Finset/Piecewise.lean | `s.piecewise f g` is the function equal to `f` on the finset `s`, and to `g` on its compl… | 4 | value | `{ι : Type u_1} {π : ι → Sort u_2} (s : Finset ι) (f g : (i : ι) → π i) [(j : ι) → Decidable (j ∈ s)] (i : ι) : π i` | none | thin | rich | 50.66 | 0 | 31 |
| 85 | Equiv.Perm.prodExtendRight | Logic/Equiv/Prod.lean | `prodExtendRight a e` extends `e : Perm β` to `Perm (α × β)` by sending `(a, b)` to `(a, … | 4 | bundled | `{α₁ : Type u_9} {β₁ : Type u_10} [DecidableEq α₁] (a : α₁) (e : Equiv.Perm β₁) : Equiv.Perm (α₁ × β₁)` | none | none | rich | 50.47 | 0 | 6 |
| 86 | MonotoneOn | Order/Monotone/Defs.lean | A function `f` is monotone on `s` if, for all `a, b ∈ s`, `a ≤ b` implies `f a ≤ f b`. | 4 | prop | `{α : Type u} {β : Type v} [Preorder α] [Preorder β] (f : α → β) (s : Set α) : Prop` | none | thin | rich | 50.41 | 273 | 273 |
| 87 | AntitoneOn | Order/Monotone/Defs.lean | A function `f` is antitone on `s` if, for all `a, b ∈ s`, `a ≤ b` implies `f b ≤ f a`. | 4 | prop | `{α : Type u} {β : Type v} [Preorder α] [Preorder β] (f : α → β) (s : Set α) : Prop` | none | thin | rich | 50.41 | 230 | 230 |
| 88 | Pi.map | Logic/Function/Defs.lean | Sends a dependent function `a : ∀ i, α i` to a dependent function `Pi.map f a : ∀ i, β i`… | 4 | value | `{ι : Sort u_1} {α : ι → Sort u_2} {β : ι → Sort u_3} (f : (i : ι) → α i → β i) : ((i : ι) → α i) → (i : ι) → β i` | none | none | rich | 50.38 | 57 | 64 |
| 89 | List.lookupAll | Data/List/Sigma.lean | `lookup_all a l` is the list of all values in `l` corresponding to the key `a`. | 4 | value | `{α : Type u} {β : α → Type v} [DecidableEq α] (a : α) : List (Sigma β) → List (β a)` | none | thin | rich | 50.19 | 0 | 11 |
| 90 | Function.prod | Logic/Function/Defs.lean | Product of functions: `Function.prod f g i = (f i, g i)`, where the types of `f i` and `g… | 4 | value | `{ι : Sort u_3} {α : ι → Type u_1} {β : ι → Type u_2} (f : (i : ι) → α i) (g : (i : ι) → β i) (i : ι) : α i × β i` | none | none | rich | 50.04 | 16 | 35 |
| 91 | Cycle.Nontrivial | Data/List/Cycle.lean | A `s : Cycle α` that is made up of at least two unique elements. | 4 | prop | `{α : Type u_1} (s : Cycle α) : Prop` | none | thin | rich | 49.61 | 0 | 6 |
| 92 | PartialEquiv.pi | Logic/Equiv/PartialEquiv.lean | The product of a family of partial equivalences, as a partial equivalence on the pi type. | 4 | bundled | `{ι : Type u_5} {αi : ι → Type u_6} {βi : ι → Type u_7} (ei : (i : ι) → PartialEquiv (αi i) (βi i)) : PartialEquiv ((i : ι) → αi i) ((i : ι) → βi i)` | none | none | rich | 49.50 | 4 | 6 |
| 93 | Int.land | Data/Int/Bitwise.lean | `land` takes two integers and returns their bitwise `and` | 4 | value | `: ℤ → ℤ → ℤ` | rich | none | thin | 49.28 | 0 | 3 |
| 94 | Equiv.sumProdDistrib | Logic/Equiv/Prod.lean | Type product is right distributive with respect to type sum up to an equivalence. | 4 | bundled | `(α : Type u_9) (β : Type u_10) (γ : Type u_11) : (α ⊕ β) × γ ≃ α × γ ⊕ β × γ` | none | none | thin | 49.25 | 0 | 4 |
| 95 | Int.xor | Data/Int/Bitwise.lean | `xor` computes the bitwise `xor` of two natural numbers | 4 | value | `: ℤ → ℤ → ℤ` | rich | none | rich | 49.17 | 3 | 7 |
| 96 | Int.lor | Data/Int/Bitwise.lean | `lor` takes two integers and returns their bitwise `or` | 4 | value | `: ℤ → ℤ → ℤ` | rich | none | thin | 49.17 | 0 | 3 |
| 97 | Function.update | Logic/Function/Basic.lean | Replacing the value of a function at a given point by a given value. | 4 | value | `{α : Sort u} {β : α → Sort v} [DecidableEq α] (f : (a : α) → β a) (a' : α) (v : β a') (a : α) : β a` | none | none | rich | 48.78 | 90 | 142 |
| 98 | Xor | Logic/Basic.lean | `Xor a b` is the exclusive-or of propositions. | 4 | prop | `(a b : Prop) : Prop` | none | thin | rich | 48.59 | 26 | 26 |
| 99 | finSumFinEquiv | Logic/Equiv/Fin/Basic.lean | Equivalence between `Fin m ⊕ Fin n` and `Fin (m + n)` | 4 | bundled | `{m n : ℕ} : Fin m ⊕ Fin n ≃ Fin (m + n)` | none | none | rich | 48.05 | 9 | 10 |
| 100 | Equiv.swapCore | Logic/Equiv/Basic.lean | A helper function for `Equiv.swap`. | 4 | value | `{α : Sort u_1} [DecidableEq α] (a b r : α) : α` | none | none | thin | 46.55 | 0 | 3 |
| 101 | Nat.FermatPsp | NumberTheory/FermatPsp.lean | `n` is a Fermat pseudoprime to base `b` if `n` is a probable prime to base `b` and is com… | 3 | prop | `(n b : ℕ) : Prop` | rich | rich | rich | 46.17 | 0 | 6 |
| 102 | Relation.Join | Logic/Relation.lean | The join of a relation on a single type is a new relation for which pairs of terms are re… | 3 | prop | `{α : Type u_1} (r : α → α → Prop) : α → α → Prop` | none | thin | rich | 45.73 | 0 | 6 |
| 103 | ArithmeticFunction.IsMultiplicative | NumberTheory/ArithmeticFunction/Defs.lean | Multiplicative functions | 4 | prop | `{R : Type u_1} [MonoidWithZero R] (f : ArithmeticFunction R) : Prop` | none | thin | rich | 45.22 | 3 | 16 |
| 104 | Finset.pi | Data/Finset/Pi.lean | Given a finset `s` of `α` and for all `a : α` a finset `t a` of `β a`, then one can defin… | 3 | value | `{α : Type u_1} {β : α → Type u} [DecidableEq α] (s : Finset α) (t : (a : α) → Finset (β a)) : Finset ((a : α) → a ∈ s → β a)` | none | thin | rich | 44.98 | 0 | 97 |
| 105 | Nat.IsAlmostPrime | NumberTheory/AlmostPrime.lean | `IsAlmostPrime k n` means that `n` is `k`-almost prime: it has exactly `k` prime factors,… | 3 | prop | `(k n : ℕ) : Prop` | none | thin | rich | 44.13 | 0 | 7 |
| 106 | List.permutations' | Data/List/Defs.lean | List of all permutations of `l`. This version of `permutations` is less efficient but has… | 3 | value | `{α : Type u_1} : List α → List (List α)` | none | thin | rich | 43.60 | 0 | 15 |
| 107 | List.destutter | Data/List/Defs.lean | Greedily create a sublist of `l` such that, for every two adjacent elements `a, b ∈ l`, `… | 3 | value | `{α : Type u_1} (R : α → α → Prop) [DecidableRel R] : List α → List α` | none | thin | rich | 43.10 | 1 | 34 |
| 108 | Relator.RightUnique | Logic/Relator.lean | A relation is "right unique" if every element on the left is paired with at most one elem… | 3 | prop | `{α : Sort u₁} {β : Sort u₂} (R : α → β → Prop) : Prop` | none | thin | thin | 42.93 | 3 | 4 |
| 109 | Relator.LeftUnique | Logic/Relator.lean | A relation is "left unique" if every element on the right is paired with at most one elem… | 3 | prop | `{α : Sort u₁} {β : Sort u₂} (R : α → β → Prop) : Prop` | none | thin | rich | 42.91 | 4 | 6 |
| 110 | Nat.Perfect | NumberTheory/Divisors.lean | `n : ℕ` is perfect if and only the sum of the proper divisors of `n` is `n` and `n`   is … | 3 | prop | `(n : ℕ) : Prop` | none | thin | rich | 42.69 | 0 | 8 |
| 111 | Nat.choose | Data/Nat/Choose/Basic.lean | `choose n k` is the number of `k`-element subsets in an `n`-element set. Also known as bi… | 3 | value | `: ℕ → ℕ → ℕ` | rich | none | rich | 42.65 | 31 | 138 |
| 112 | List.Pi.cons | Data/List/Pi.lean | Given `α : ι → Sort*`, a list `l` and a term `i`, as well as a term `a : α i` and a funct… | 3 | value | `{ι : Type u_1} [DecidableEq ι] {α : ι → Sort u_2} (i : ι) (l : List ι) (a : α i) (f : (j : ι) → j ∈ l → α j) (j : ι) : j ∈ i :: l → α j` | none | thin | thin | 42.58 | 0 | 3 |
| 113 | Finset.attachFin | Data/Finset/Fin.lean | Given a Finset `s` of `ℕ` contained in `{0,..., n-1}`, the corresponding Finset in `Fin n… | 3 | value | `(s : Finset ℕ) {n : ℕ} (h : ∀ m ∈ s, m < n) : Finset (Fin n)` | none | thin | rich | 42.09 | 0 | 9 |
| 114 | Relator.RightTotal | Logic/Relator.lean | A relation is "right total" if every element appears on the right. | 3 | prop | `{α : Sort u₁} {β : Sort u₂} (R : α → β → Prop) : Prop` | none | thin | thin | 41.70 | 1 | 2 |
| 115 | List.TFAE | Data/List/TFAE.lean | TFAE: The Following (propositions) Are Equivalent.  The `tfae_have` and `tfae_finish` tac… | 3 | prop | `(l : List Prop) : Prop` | none | thin | rich | 41.51 | 49 | 60 |
| 116 | Nat.primeFactorsList | Data/Nat/Factors.lean | `primeFactorsList n` is the prime factorization of `n`, listed in increasing order. | 3 | value | `: ℕ → List ℕ` | rich | thin | rich | 41.32 | 2 | 49 |
| 117 | Pairwise | Logic/Pairwise.lean | A relation `r` holds pairwise if `r i j` for all `i ≠ j`. | 3 | prop | `{α : Type u_1} (r : α → α → Prop) : Prop` | none | thin | rich | 41.28 | 725 | 725 |
| 118 | Finset.sym | Data/Finset/Sym.lean | Lifts a finset to `Sym α n`. `s.sym n` is the finset of all unordered tuples of cardinali… | 3 | value | `{α : Type u_1} [DecidableEq α] (s : Finset α) (n : ℕ) : Finset (Sym α n)` | none | thin | rich | 41.17 | 8 | 85 |
| 119 | Nat.factorizationLCMRight | Data/Nat/Factorization/Defs.lean | If `a = ∏ pᵢ ^ nᵢ` and `b = ∏ pᵢ ^ mᵢ`, then `factorizationLCMRight = ∏ pᵢ ^ kᵢ`, where `… | 2 | value | `(a b : ℕ) : ℕ` | rich | none | rich | 40.89 | 1 | 5 |
| 120 | Nat.bell | Combinatorics/Enumerative/Bell.lean | The `n`th standard Bell number, which counts the number of partitions of a set of cardina… | 3 | value | `: ℕ → ℕ` | rich | none | rich | 40.74 | 3 | 7 |
| 121 | Nat.IsAtMostAlmostPrime | NumberTheory/AlmostPrime.lean | `IsAtMostAlmostPrime k n` means that `n` has at most `k` prime factors, counted with mult… | 3 | prop | `(k n : ℕ) : Prop` | none | thin | thin | 40.74 | 0 | 2 |
| 122 | Nat.multichoose | Data/Nat/Choose/Basic.lean | `multichoose n k` is the number of multisets of cardinality `k` from a type of cardinalit… | 3 | value | `: ℕ → ℕ → ℕ` | rich | none | rich | 40.66 | 1 | 9 |
| 123 | Nat.smallSchroder | Combinatorics/Enumerative/Schroder.lean | The small Schröder number is equal to : `largeSchroder n = 2 * smallSchroder (n + 1), n ≥… | 3 | value | `: ℕ → ℕ` | rich | none | thin | 40.58 | 0 | 3 |
| 124 | ArithmeticFunction.carmichael | NumberTheory/ArithmeticFunction/Carmichael.lean | `λ` is the Carmichael function, also known as the reduced totient function, defined as th… | 3 | value | `: ArithmeticFunction ℕ` | none | none | rich | 40.42 | 0 | 15 |
| 125 | Set.Bounded | Order/RelClasses.lean | A bounded or final set. Not to be confused with `Bornology.IsBounded`. | 3 | prop | `{α : Type u} (r : α → α → Prop) (s : Set α) : Prop` | none | thin | rich | 39.86 | 0 | 47 |
| 126 | IsNilpotent | Algebra/GroupWithZero/Basic.lean | An element is said to be nilpotent if some natural-number-power of it equals zero.  Note … | 2 | prop | `{R : Type u_3} [Zero R] [Pow R ℕ] (x : R) : Prop` | none | thin | rich | 39.22 | 252 | 256 |
| 127 | Nat.doubleFactorial | Data/Nat/Factorial/DoubleFactorial.lean | `Nat.doubleFactorial n` is the double factorial of `n`. | 3 | value | `: ℕ → ℕ` | rich | none | rich | 39.17 | 1 | 9 |
| 128 | npowRec' | Algebra/Group/Defs.lean | A variant of `npowRec` which is a semigroup homomorphism from `ℕ₊` to `M`. | 3 | value | `{M : Type u_2} [One M] [Mul M] : ℕ → M → M` | none | none | rich | 39.01 | 5 | 5 |
| 129 | Equiv.piCongrLeft' | Logic/Equiv/Basic.lean | Transport dependent functions through an equivalence of the base space. | 3 | bundled | `{α : Sort u_1} {β : Sort u_4} (P : α → Sort u_9) (e : α ≃ β) : ((a : α) → P a) ≃ ((b : β) → P (e.symm b))` | none | none | rich | 38.90 | 4 | 7 |
| 130 | numDerangements | Combinatorics/Derangements/Finite.lean | The number of derangements of an `n`-element set. | 3 | value | `: ℕ → ℕ` | rich | none | rich | 38.80 | 8 | 8 |
| 131 | Nat.factorizationLCMLeft | Data/Nat/Factorization/Defs.lean | If `a = ∏ pᵢ ^ nᵢ` and `b = ∏ pᵢ ^ mᵢ`, then `factorizationLCMLeft = ∏ pᵢ ^ kᵢ`, where `k… | 2 | value | `(a b : ℕ) : ℕ` | rich | none | rich | 38.80 | 1 | 5 |
| 132 | ArithmeticFunction.prodPrimeFactors | NumberTheory/ArithmeticFunction/Misc.lean | The map $n \mapsto \prod_{p \mid n} f(p)$ as an arithmetic function | 3 | value | `{R : Type u_1} [CommMonoidWithZero R] (f : ℕ → R) : ArithmeticFunction R` | none | none | thin | 38.74 | 0 | 3 |
| 133 | Equiv.setCongr | Logic/Equiv/Set.lean | The subtypes corresponding to equal sets are equivalent. | 3 | bundled | `{α : Type u_3} {s t : Set α} (h : s = t) : ↑s ≃ ↑t` | none | none | rich | 38.22 | 0 | 5 |
| 134 | Function.FromTypes.const | Logic/Function/FromTypes.lean | Constant `n`-ary function with value `t`. | 3 | value | `{n : ℕ} (p : Fin n → Type u) {τ : Type u} (t : τ) : Function.FromTypes p τ` | none | none | thin | 37.18 | 0 | 4 |
| 135 | Set.Unbounded | Order/RelClasses.lean | An unbounded or cofinal set. | 3 | prop | `{α : Type u} (r : α → α → Prop) (s : Set α) : Prop` | none | thin | rich | 36.39 | 0 | 38 |
| 136 | Nat.descFactorial | Data/Nat/Factorial/Basic.lean | `n.descFactorial k = n! / (n - k)!` (as seen in `Nat.descFactorial_eq_div`), but implemen… | 2 | value | `(n : ℕ) : ℕ → ℕ` | rich | none | rich | 34.68 | 6 | 36 |
| 137 | ArithmeticFunction.liouville | NumberTheory/ArithmeticFunction/Liouville.lean | The Liouville function `λ(n)` defined to be `1` if `n` has an even number of prime factor… | 2 | value | `: ArithmeticFunction ℤ` | none | none | rich | 34.49 | 0 | 5 |
| 138 | List.Shortlex | Data/List/Shortlex.lean | Given a relation `r` on `α`, the shortlex order on `List α`, for which `[a0, ..., an] < [… | 2 | prop | `{α : Type u_1} (r : α → α → Prop) : List α → List α → Prop` | none | thin | rich | 34.47 | 0 | 8 |
| 139 | Finset.orderEmbOfFin | Data/Finset/Sort.lean | Given a finset `s` of cardinality `k` in a linear order `α`, the map `orderEmbOfFin s h` … | 2 | bundled | `{α : Type u_1} [LinearOrder α] (s : Finset α) {k : ℕ} (h : s.card = k) : Fin k ↪o α` | none | thin | rich | 33.55 | 2 | 25 |
| 140 | List.sym2 | Data/List/Sym.lean | `xs.sym2` is a list of all unordered pairs of elements from `xs`. If `xs` has no duplicat… | 2 | value | `{α : Type u_1} : List α → List (Sym2 α)` | none | thin | rich | 33.23 | 0 | 18 |
| 141 | List.ranges | Data/List/Range.lean | From `l : List ℕ`, construct `l.ranges : List (List ℕ)` such that `l.ranges.map List.leng… | 2 | value | `: List ℕ → List (List ℕ)` | rich | thin | rich | 33.16 | 0 | 5 |
| 142 | DyckWord.toTree | Combinatorics/Enumerative/DyckWord.lean | Convert a Dyck word to a binary rooted tree.  `f(0) = nil`. For a nonzero word find the `… | 2 | value | `(p : DyckWord) : BinaryTree Unit` | none | none | thin | 33.05 | 0 | 3 |
| 143 | Finset.disjiUnion | Data/Finset/Union.lean | `disjiUnion s f h` is the set such that `a ∈ disjiUnion s f` iff `a ∈ f i` for some `i ∈ … | 2 | value | `{α : Type u_1} {β : Type u_2} (s : Finset α) (t : α → Finset β) (hf : (↑s).PairwiseDisjoint t) : Finset β` | none | thin | rich | 32.72 | 2 | 25 |
| 144 | Finset.image₂ | Data/Finset/NAry.lean | The image of a binary function `f : α → β → γ` as a function `Finset α → Finset β → Finse… | 2 | value | `{α : Type u_1} {β : Type u_3} {γ : Type u_5} [DecidableEq γ] (f : α → β → γ) (s : Finset α) (t : Finset β) : Finset γ` | none | thin | rich | 32.29 | 1 | 98 |
| 145 | AddMonoidHom.mul | Algebra/Ring/Basic.lean | Multiplication of an element of a (semi)ring is an `AddMonoidHom` in both arguments.  Thi… | 2 | value | `{R : Type u_1} [NonUnitalNonAssocSemiring R] : R → + R → + R` | none | none | rich | 32.18 | 8 | 19 |
| 146 | Relation.SymmGen | Logic/Relation.lean | `SymmGen r`: symmetric closure of `r`. This is also the comparability relation, such   th… | 2 | prop | `{α : Type u_1} (r : α → α → Prop) (a b : α) : Prop` | none | thin | rich | 32.11 | 6 | 10 |
| 147 | Nat.shiftLeft' | Data/Nat/Bits.lean | `shiftLeft' b m n` performs a left shift of `m` `n` times and adds the bit `b` as the lea… | 2 | value | `(b : Bool) (m : ℕ) : ℕ → ℕ` | rich | none | rich | 31.88 | 3 | 10 |
| 148 | Function.Bijective | Logic/Function/Defs.lean | A function is called bijective if it is both injective and surjective. | 2 | prop | `{α : Sort u₁} {β : Sort u₂} (f : α → β) : Prop` | none | thin | rich | 31.86 | 429 | 451 |
| 149 | Relator.BiUnique | Logic/Relator.lean | A relation is "bi-unique" if it is both left unique and right unique. | 2 | prop | `{α : Sort u₁} {β : Sort u₂} (R : α → β → Prop) : Prop` | none | thin | thin | 31.82 | 2 | 3 |
| 150 | List.IsRotated | Data/List/Rotate.lean | `IsRotated l₁ l₂` or `l₁ ~r l₂` asserts that `l₁` and `l₂` are cyclic permutations   of e… | 2 | prop | `{α : Type u} (l l' : List α) : Prop` | none | thin | rich | 31.81 | 0 | 14 |
| 151 | PartialEquiv.EqOnSource | Logic/Equiv/PartialEquiv.lean | `EqOnSource e e'` means that `e` and `e'` have the same source, and coincide there. Then … | 2 | prop | `{α : Type u_1} {β : Type u_2} (e e' : PartialEquiv α β) : Prop` | none | thin | rich | 31.80 | 1 | 9 |
| 152 | Relator.BiTotal | Logic/Relator.lean | A relation is "bi-total" if it is both right total and left total. | 2 | prop | `{α : Sort u₁} {β : Sort u₂} (R : α → β → Prop) : Prop` | none | thin | thin | 31.70 | 1 | 3 |
| 153 | Finset.fold | Data/Finset/Fold.lean | `fold op b f s` folds the commutative associative operation `op` over the   `f`-image of … | 2 | value | `{α : Type u_1} {β : Type u_2} (op : β → β → β) [hc : Std.Commutative op] [ha : Std.Associative op] (b : β) (f : α → β) (s : Finset α) : β` | none | thin | rich | 31.62 | 5 | 35 |
| 154 | Finset.noncommProd | Data/Finset/NoncommProd.lean | Sum of a `s : Finset α` mapped with `f : α → β` with `[AddMonoid β]`, given a proof that … | 2 | value | `{α : Type u_3} {β : Type u_4} [Monoid β] (s : Finset α) (f : α → β) (comm : (↑s).Pairwise (Function.onFun Commute f)) : β` | none | thin | rich | 31.59 | 3 | 26 |
| 155 | Nat.ofDigits | Data/Nat/Digits/Defs.lean | `ofDigits b L` takes a list `L` of natural numbers, and interprets them as a number in se… | 2 | value | `{α : Type u_1} [Semiring α] (b : α) : List ℕ → α` | none | thin | rich | 31.54 | 0 | 49 |
| 156 | Nat.largeSchroder | Combinatorics/Enumerative/Schroder.lean | The recursive definition of the sequence of the large Schröder numbers : `a (n + 1) = a n… | 2 | value | `: ℕ → ℕ` | rich | none | thin | 31.35 | 0 | 4 |
| 157 | Composition.boundary | Combinatorics/Enumerative/Composition.lean | The `i`-th boundary of a composition, i.e., the leftmost point of the `i`-th block. We in… | 2 | bundled | `{n : ℕ} (c : Composition n) : Fin (c.length + 1) ↪o Fin (n + 1)` | none | none | thin | 31.33 | 0 | 3 |
| 158 | Function.IsFixedPt | Logic/Function/Defs.lean | A point `x` is a fixed point of `f : α → α` if `f x = x`. | 2 | prop | `{α : Type u₁} (f : α → α) (x : α) : Prop` | none | thin | rich | 31.28 | 4 | 17 |
| 159 | derangements | Combinatorics/Derangements/Basic.lean | A permutation is a derangement if it has no fixed points. | 2 | bundled | `(α : Type u_1) : Set (Equiv.Perm α)` | none | thin | rich | 31.28 | 6 | 6 |
| 160 | finSuccEquiv' | Logic/Equiv/Fin/Basic.lean | An equivalence that removes `i` and maps it to `none`. This is a version of `Fin.predAbov… | 2 | bundled | `{n : ℕ} (i : Fin (n + 1)) : Fin (n + 1) ≃ Option (Fin n)` | none | none | rich | 31.16 | 16 | 16 |
| 161 | Nat.ascFactorial | Data/Nat/Factorial/Basic.lean | `n.ascFactorial k = n (n + 1) ⋯ (n + k - 1)`. This is closely related to `ascPochhammer`,… | 2 | value | `(n : ℕ) : ℕ → ℕ` | rich | none | rich | 31.07 | 2 | 31 |
| 162 | Finset.subtype | Data/Finset/Image.lean | Given a finset `s` and a predicate `p`, `s.subtype p` is the finset of `Subtype p` whose … | 2 | value | `{α : Type u_4} (p : α → Prop) [DecidablePred p] (s : Finset α) : Finset (Subtype p)` | none | thin | rich | 31.07 | 2 | 39 |
| 163 | Equiv.piUnique | Logic/Equiv/Defs.lean | The equivalence `(∀ i, β i) ≃ β ⋆` when the domain of `β` only contains `⋆` | 2 | bundled | `{α : Sort u} [Unique α] (β : α → Sort u_1) : ((i : α) → β i) ≃ β default` | none | none | thin | 31.05 | 2 | 2 |
| 164 | LucasLehmer.norm_num_ext.sModNat | NumberTheory/LucasLehmer.lean | Version of `sMod` that is `ℕ`-valued. One should have `q = 2 ^ p - 1`. This can be reduce… | 2 | value | `(q : ℕ) : ℕ → ℕ` | rich | none | rich | 30.91 | 0 | 5 |
| 165 | AntisymmRel | Order/Antisymmetrization.lean | The antisymmetrization relation `AntisymmRel r` is defined so that `AntisymmRel r a b ↔ r… | 2 | prop | `{α : Type u_1} (r : α → α → Prop) (a b : α) : Prop` | none | thin | rich | 30.86 | 74 | 74 |
| 166 | Int.bodd | Data/Int/Bitwise.lean | `bodd n` returns `true` if `n` is odd | 2 | value | `: ℤ → Bool` | rich | rich | rich | 30.78 | 1 | 12 |
| 167 | DyckWord.ofTree | Combinatorics/Enumerative/DyckWord.lean | Convert a binary rooted tree to a Dyck word.  `g(nil) = 0`. A nonempty tree with left sub… | 2 | value | `: BinaryTree Unit → DyckWord` | none | none | thin | 30.74 | 0 | 2 |
| 168 | DyckWord.take | Combinatorics/Enumerative/DyckWord.lean | Prefix of a Dyck word as a Dyck word, given that the count of `U`s and `D`s in it are equ… | 2 | value | `(p : DyckWord) (i : ℕ) (hi : List.count DyckStep.U (List.take i ↑p) = List.count DyckStep.D (List.take i ↑p)) : DyckWord` | none | thin | thin | 30.58 | 0 | 2 |
| 169 | DyckWord.outsidePart | Combinatorics/Enumerative/DyckWord.lean | The right part of the Dyck word decomposition, outside the `U, D` pair that `firstReturn`… | 2 | value | `(p : DyckWord) : DyckWord` | none | none | rich | 30.25 | 0 | 5 |
| 170 | Equiv.arrowProdEquivProdArrow | Logic/Equiv/Prod.lean | The type of functions to a product `β × γ` is equivalent to the type of pairs of function… | 2 | bundled | `(α : Type u_9) (β : α → Type u_10) (γ : α → Type u_11) : ((i : α) → β i × γ i) ≃ ((i : α) → β i) × ((i : α) → γ i)` | none | none | thin | 30.04 | 2 | 2 |
| 171 | Equiv.sumArrowEquivProdArrow | Logic/Equiv/Prod.lean | The type of functions on a sum type `α ⊕ β` is equivalent to the type of pairs of functio… | 2 | bundled | `(α : Type u_9) (β : Type u_10) (γ : Type u_11) : (α ⊕ β → γ) ≃ (α → γ) × (β → γ)` | none | none | rich | 30.02 | 4 | 8 |
| 172 | Equiv.psigmaCongrRight | Logic/Equiv/Defs.lean | A family of equivalences `Π a, β₁ a ≃ β₂ a` generates an equivalence between `Σ' a, β₁ a`… | 2 | bundled | `{α : Sort u} {β₁ : α → Sort u_1} {β₂ : α → Sort u_2} (F : (a : α) → β₁ a ≃ β₂ a) : (a : α) ×' β₁ a ≃ (a : α) ×' β₂ a` | none | none | thin | 29.95 | 0 | 3 |
| 173 | Equiv.sigmaCongrRight | Logic/Equiv/Defs.lean | A family of equivalences `Π a, β₁ a ≃ β₂ a` generates an equivalence between `Σ a, β₁ a` … | 2 | bundled | `{α : Type u_3} {β₁ : α → Type u_1} {β₂ : α → Type u_2} (F : (a : α) → β₁ a ≃ β₂ a) : (a : α) × β₁ a ≃ (a : α) × β₂ a` | none | none | rich | 29.91 | 0 | 8 |
| 174 | Int.gcdA | Data/Int/GCD.lean | The extended GCD `a` value in the equation `gcd x y = x * a + y * b`. | 2 | value | `: ℤ → ℤ → ℤ` | rich | none | thin | 29.82 | 0 | 2 |
| 175 | Int.lnot | Data/Int/Bitwise.lean | `lnot` flips all the bits in the binary representation of its input | 2 | value | `: ℤ → ℤ` | rich | none | thin | 29.74 | 0 | 2 |
| 176 | LucasLehmer.sMod | NumberTheory/LucasLehmer.lean | The recurrence `s (i+1) = ((s i)^2 - 2) % (2^p - 1)` in `ℤ`. | 2 | value | `(p : ℕ) : ℕ → ℤ` | rich | none | rich | 29.43 | 0 | 5 |
| 177 | LucasLehmer.sZMod | NumberTheory/LucasLehmer.lean | The recurrence `s (i+1) = (s i)^2 - 2` in `ZMod (2^p - 1)`. | 2 | value | `(p a✝ : ℕ) : ZMod (2 ^ p - 1)` | rich | none | thin | 29.38 | 0 | 2 |
| 178 | Set.Sized | Data/Finset/Slice.lean | `Sized r A` means that every Finset in `A` has size `r`. | 2 | prop | `{α : Type u_1} (r : ℕ) (A : Set (Finset α)) : Prop` | none | thin | rich | 29.22 | 6 | 16 |
| 179 | Nat.superFactorial | Data/Nat/Factorial/SuperFactorial.lean | `Nat.superFactorial n` is the superfactorial of `n`. | 2 | value | `: ℕ → ℕ` | rich | none | rich | 28.99 | 0 | 8 |
| 180 | Composition.cast | Combinatorics/Enumerative/Composition.lean | Change `n` in `(c : Composition n)` to a propositionally equal value. | 2 | value | `{n m : ℕ} (c : Composition m) (hmn : m = n) : Composition n` | none | none | thin | 28.82 | 0 | 4 |
| 181 | Equiv.optionCongr | Logic/Equiv/Option.lean | A universe-polymorphic version of `EquivFunctor.mapEquiv Option e`. | 2 | bundled | `{α : Type u_1} {β : Type u_2} (e : α ≃ β) : Option α ≃ Option β` | none | none | rich | 28.74 | 4 | 10 |
| 182 | Function.FromTypes | Logic/Function/FromTypes.lean | The type of `n`-ary functions `p 0 → p 1 → ... → p (n - 1) → τ`. | 2 | bundled | `{n : ℕ} : (Fin n → Type u) → Type u → Type u` | none | none | rich | 28.61 | 4 | 8 |
| 183 | LucasLehmer.s | NumberTheory/LucasLehmer.lean | The recurrence `s (i+1) = (s i)^2 - 2` in `ℤ`. | 2 | value | `: ℕ → ℤ` | rich | none | rich | 28.59 | 0 | 11 |
| 184 | Nat.minFac | Data/Nat/Prime/Defs.lean | Returns the smallest prime factor of `n ≠ 1`. | 2 | value | `(n : ℕ) : ℕ` | rich | none | rich | 28.52 | 3 | 33 |
| 185 | Nat.unpair | Data/Nat/Pairing.lean | Unpairing function for the natural numbers. | 2 | value | `(n : ℕ) : ℕ × ℕ` | rich | none | rich | 28.36 | 9 | 18 |
| 186 | Nat.factorial | Data/Nat/Factorial/Basic.lean | `Nat.factorial n` is the factorial of `n`. | 2 | value | `: ℕ → ℕ` | rich | none | rich | 28.27 | 10 | 80 |
| 187 | Nat.pair | Data/Nat/Pairing.lean | Pairing function for the natural numbers. | 2 | value | `(a b : ℕ) : ℕ` | rich | none | rich | 28.18 | 13 | 37 |
| 188 | Int.log | Data/Int/Log.lean | The greatest power of `b` such that `b ^ log b r ≤ r`. | 2 | value | `{R : Type u_1} [Semifield R] [LinearOrder R] [FloorSemiring R] (b : ℕ) (r : R) : ℤ` | none | none | rich | 28.11 | 1 | 37 |
| 189 | ArithmeticFunction.ppow | NumberTheory/ArithmeticFunction/Zeta.lean | This is the pointwise power of `ArithmeticFunction`s. | 2 | value | `{R : Type u_1} [Semiring R] (f : ArithmeticFunction R) (k : ℕ) : ArithmeticFunction R` | none | none | rich | 28.05 | 0 | 5 |
| 190 | Int.clog | Data/Int/Log.lean | The least power of `b` such that `r ≤ b ^ log b r`. | 2 | value | `{R : Type u_1} [Semifield R] [LinearOrder R] [FloorSemiring R] (b : ℕ) (r : R) : ℤ` | none | none | rich | 27.93 | 1 | 22 |
| 191 | Composition.single | Combinatorics/Enumerative/Composition.lean | The composition made of a single block of size `n`. | 2 | value | `(n : ℕ) (h : 0 < n) : Composition n` | none | none | rich | 27.93 | 1 | 9 |
| 192 | Nat.find | Data/Nat/Find.lean | If `p` is a (decidable) predicate on `ℕ` and `hp : ∃ (n : ℕ), p n` is a proof that there … | 1 | value | `{p : ℕ → Prop} [DecidablePred p] (H : ∃ n, p n) : ℕ` | none | none | rich | 27.64 | 64 | 75 |
| 193 | OrderIso.dualAntisymmetrization | Order/Antisymmetrization.lean | `Antisymmetrization` and `orderDual` commute. | 2 | bundled | `(α : Type u_1) [Preorder α] : (Antisymmetrization α fun x1 x2 => x1 ≤ x2)ᵒᵈ ≃o Antisymmetrization αᵒᵈ fun x1 x2 => x1 ≤ x2` | none | none | thin | 27.52 | 2 | 3 |
| 194 | PartialEquiv.IsImage | Logic/Equiv/PartialEquiv.lean | We say that `t : Set β` is an image of `s : Set α` under a partial equivalence if any of … | 1 | prop | `{α : Type u_1} {β : Type u_2} (e : PartialEquiv α β) (s : Set α) (t : Set β) : Prop` | none | thin | thin | 27.14 | 1 | 4 |
| 195 | List.maximum_of_length_pos | Data/List/MinMax.lean | The maximum value in a non-empty `List`. | 2 | value | `{α : Type u_1} [LinearOrder α] {l : List α} (h : 0 < l.length) : α` | none | none | rich | 27.09 | 0 | 5 |
| 196 | List.minimum_of_length_pos | Data/List/MinMax.lean | The minimum value in a non-empty `List`. | 2 | value | `{α : Type u_1} [LinearOrder α] {l : List α} (h : 0 < l.length) : α` | none | none | rich | 27.09 | 0 | 5 |
| 197 | List.IsZeckendorfRep | Data/Nat/Fib/Zeckendorf.lean | A list of natural numbers is a Zeckendorf representation (of a natural number) if it is a… | 1 | prop | `(l : List ℕ) : Prop` | none | thin | thin | 26.16 | 0 | 2 |
| 198 | Equiv.cast | Logic/Equiv/Defs.lean | Equivalence between equal types. | 2 | bundled | `{α β : Sort u_1} (h : α = β) : α ≃ β` | none | none | rich | 26.13 | 6 | 11 |
| 199 | List.map₂Right' | Data/List/Defs.lean | Right-biased version of `List.map₂`. `map₂Right' f as bs` applies `f` to each pair of ele… | 1 | value | `{α : Type u_1} {β : Type u_2} {γ : Type u_3} (f : Option α → β → γ) (as : List α) (bs : List β) : List γ × List α` | none | thin | rich | 25.90 | 0 | 5 |
| 200 | Nat.ProbablePrime | NumberTheory/FermatPsp.lean | `n` is a probable prime to base `b` if `n` passes the Fermat primality test; that is, `n`… | 1 | prop | `(n b : ℕ) : Prop` | rich | rich | thin | 25.82 | 0 | 2 |
| 201 | List.map₂Right | Data/List/Defs.lean | Right-biased version of `List.map₂`. `map₂Right f as bs` applies `f` to each pair `aᵢ ∈ a… | 1 | value | `{α : Type u_1} {β : Type u_2} {γ : Type u_3} (f : Option α → β → γ) (as : List α) (bs : List β) : List γ` | none | thin | rich | 25.61 | 0 | 10 |
| 202 | Finset.sup' | Data/Finset/Lattice/Fold.lean | Given nonempty finset `s` then `s.inf' H f` is the infimum of its image under `f` in (pos… | 1 | value | `{α : Type u_2} {β : Type u_3} [SemilatticeSup α] (s : Finset β) (H : s.Nonempty) (f : β → α) : α` | none | thin | rich | 25.00 | 0 | 61 |
| 203 | Finset.filter | Data/Finset/Filter.lean | `Finset.filter p s` is the set of elements of `s` that satisfy `p`.  For example, one can… | 1 | value | `{α : Type u_1} (p : α → Prop) [DecidablePred p] (s : Finset α) : Finset α` | none | thin | rich | 24.71 | 6 | 158 |
| 204 | Finset.cons | Data/Finset/Insert.lean | `cons a s h` is the set `{a} ∪ s` containing `a` and the elements of `s`. It is the same … | 1 | value | `{α : Type u_1} (a : α) (s : Finset α) (h : a ∉ s) : Finset α` | none | thin | rich | 24.69 | 7 | 111 |
| 205 | Int.sqrt | Data/Int/Sqrt.lean | `sqrt z` is the square root of an integer `z`. If `z` is positive, it returns the largest… | 1 | value | `(z : ℤ) : ℤ` | rich | none | rich | 24.57 | 3 | 8 |
| 206 | Finset.Nonempty | Data/Finset/Empty.lean | The property `s.Nonempty` expresses the fact that the finset `s` is not empty. It should … | 1 | prop | `{α : Type u_1} (s : Finset α) : Prop` | none | thin | rich | 24.56 | 15 | 325 |
| 207 | Function.Commute | Logic/Function/Conjugate.lean | Two maps `f g : α → α` commute if `f (g x) = g (f x)` for all `x : α`. Given `h : Functio… | 1 | prop | `{α : Type u_1} (f g : α → α) : Prop` | none | thin | rich | 24.20 | 16 | 24 |
| 208 | Nat.properDivisors | NumberTheory/Divisors.lean | `properDivisors n` is the `Finset` of divisors of `n`, other than `n`. By convention, we … | 1 | value | `(n : ℕ) : Finset ℕ` | rich | thin | rich | 24.15 | 4 | 35 |
| 209 | List.next | Data/List/Cycle.lean | Given an element `x : α` of `l : List α` such that `x ∈ l`, get the next element of `l`. … | 1 | value | `{α : Type u_1} [DecidableEq α] (l : List α) (x : α) (h : x ∈ l) : α` | none | thin | rich | 23.76 | 0 | 30 |
| 210 | List.HasPeriod | Data/List/PeriodicityLemma.lean | `HasPeriod w p`, means that the list `w` has the period `p`, which can be seen in two equ… | 1 | prop | `{α : Type u_1} (w : List α) (p : ℕ) : Prop` | none | thin | rich | 23.65 | 0 | 12 |
| 211 | ArithmeticFunction.moebius | NumberTheory/ArithmeticFunction/Moebius.lean | `μ` is the Möbius function. If `n` is squarefree with an even number of distinct prime fa… | 1 | value | `: ArithmeticFunction ℤ` | none | none | rich | 23.63 | 1 | 36 |
| 212 | Nat.divisors | NumberTheory/Divisors.lean | `divisors n` is the `Finset` of divisors of `n`. By convention, we set `divisors 0 = ∅`. | 1 | value | `(n : ℕ) : Finset ℕ` | rich | thin | rich | 23.47 | 8 | 82 |
| 213 | List.toFinsupp | Data/List/ToFinsupp.lean | Indexing into a `l : List M`, as a finitely-supported function, where the support are all… | 1 | value | `{M : Type u_1} [Zero M] (l : List M) [DecidablePred fun x => l.getD x 0 ≠ 0] : ℕ → ₀ M` | none | thin | rich | 23.14 | 0 | 14 |
| 214 | List.dedup | Data/List/Defs.lean | `dedup l` removes duplicates from `l` (taking only the last occurrence). Defined as `pwFi… | 1 | value | `{α : Type u_1} [DecidableEq α] : List α → List α` | none | thin | rich | 22.87 | 2 | 39 |
| 215 | Nat.multinomial | Data/Nat/Choose/Multinomial.lean | The multinomial coefficient. Gives the number of strings consisting of symbols from `s`, … | 1 | value | `{α : Type u_1} (s : Finset α) (f : α → ℕ) : ℕ` | none | thin | rich | 22.20 | 6 | 24 |
| 216 | Finsupp.pi | Data/Finset/Finsupp.lean | Given a finitely supported function `f : ι →₀ Finset α`, one can define the finset `f.pi`… | 1 | value | `{ι : Type u_1} {α : Type u_2} [Zero α] (f : ι →₀ Finset α) : Finset (ι →₀ α)` | none | thin | rich | 22.02 | 0 | 5 |
| 217 | Finset.restrict₂ | Data/Finset/Pi.lean | If a function `f` is restricted to a finite set `t`, and `s ⊆ t`, this is the restriction… | 1 | value | `{ι : Type u_2} {π : ι → Type u_3} {s t : Finset ι} (hst : s ⊆ t) (f : (i : ↥t) → π ↑i) (i : ↥s) : π ↑i` | none | none | rich | 21.71 | 8 | 12 |
| 218 | Finset.biUnion | Data/Finset/Union.lean | `Finset.biUnion s t` is the union of `t a` over `a ∈ s`.  (This was formerly `bind` due t… | 1 | value | `{α : Type u_1} {β : Type u_2} [DecidableEq β] (s : Finset α) (t : α → Finset β) : Finset β` | none | thin | rich | 21.57 | 5 | 97 |
| 219 | Nat.ModEq | Data/Nat/ModEq.lean | Modular equality. `n.ModEq a b`, or `a ≡ b [MOD n]`, means that `a % n = b % n`. | 1 | prop | `(n a b : ℕ) : Prop` | rich | rich | rich | 21.22 | 6 | 6 |
| 220 | Finset.offDiag | Data/Finset/Prod.lean | Given a finite set `s`, the off-diagonal, `s.offDiag` is the set of pairs `(a, b)` with `… | 1 | value | `{α : Type u_1} (s : Finset α) : Finset (α × α)` | none | thin | rich | 21.04 | 2 | 19 |
| 221 | IsComplemented | Order/Disjoint.lean | An element is *complemented* if it has a complement. | 1 | prop | `{α : Type u_1} [Lattice α] [BoundedOrder α] (a : α) : Prop` | none | thin | rich | 20.99 | 9 | 9 |
| 222 | Multiset.noncommProd | Data/Finset/NoncommProd.lean | Sum of a `s : Multiset α` with `[AddMonoid α]`, given a proof that `+` commutes       on … | 1 | value | `{α : Type u_3} [Monoid α] (s : Multiset α) (comm : {x | x ∈ s}.Pairwise Commute) : α` | none | thin | rich | 20.98 | 0 | 13 |
| 223 | ArithmeticFunction.zeta | NumberTheory/ArithmeticFunction/Zeta.lean | `ζ 0 = 0`, otherwise `ζ x = 1`. The Dirichlet Series is the Riemann `ζ`. | 1 | value | `: ArithmeticFunction ℕ` | none | none | rich | 20.94 | 2 | 37 |
| 224 | Int.ModEq | Data/Int/ModEq.lean | `a ≡ b [ZMOD n]` when `a % n = b % n`. | 1 | prop | `(n a b : ℤ) : Prop` | rich | rich | thin | 20.89 | 3 | 3 |
| 225 | Equiv.Perm.subtypeCongr | Logic/Equiv/Basic.lean | Combining permutations on `ε` that permute only inside or outside the subtype split induc… | 1 | bundled | `{ε : Type u_9} {p : ε → Prop} [DecidablePred p] (ep : Equiv.Perm { a // p a }) (en : Equiv.Perm { a // ¬p a }) : Equiv.Perm ε` | none | none | thin | 20.62 | 0 | 3 |
| 226 | Finset.sigma | Data/Finset/Sigma.lean | `s.sigma t` is the finset of dependent pairs `⟨i, a⟩` such that `i ∈ s` and `a ∈ t i`. | 1 | value | `{ι : Type u_1} {α : ι → Type u_2} (s : Finset ι) (t : (i : ι) → Finset (α i)) : Finset ((i : ι) × α i)` | none | thin | rich | 20.41 | 0 | 36 |
| 227 | Cycle.Mem | Data/List/Cycle.lean | For `x : α`, `s : Cycle α`, `x ∈ s` indicates that `x` occurs at least once in `s`. | 1 | prop | `{α : Type u_1} (s : Cycle α) (a : α) : Prop` | none | thin | thin | 20.32 | 0 | 2 |
| 228 | Nat.factorization | Data/Nat/Factorization/Defs.lean | `n.factorization` is the finitely supported function `ℕ →₀ ℕ` mapping each prime factor o… | 1 | value | `(n : ℕ) : ℕ → ₀ ℕ` | none | none | rich | 20.27 | 2 | 118 |
| 229 | Equiv.uniqueSigma | Logic/Equiv/Prod.lean | Any `Unique` type is a left identity for type sigma up to equivalence. Compare with `uniq… | 1 | bundled | `{α : Type u_10} (β : α → Type u_9) [Unique α] : (i : α) × β i ≃ β default` | none | none | thin | 20.23 | 0 | 2 |
| 230 | List.offDiag | Data/List/OffDiag.lean | `List.offDiag l` is the product `l.product l` with the diagonal removed. | 1 | value | `{α : Type u_1} (l : List α) : List (α × α)` | none | thin | rich | 19.94 | 0 | 13 |
| 231 | List.insertionSort | Data/List/Sort.lean | `insertionSort l` returns `l` sorted using the insertion sort algorithm. | 1 | value | `{α : Type u_1} (r : α → α → Prop) [DecidableRel r] : List α → List α` | none | thin | rich | 19.94 | 0 | 16 |
| 232 | Equiv.prodCongrLeft | Logic/Equiv/Prod.lean | A family of equivalences `∀ (a : α₁), β₁ ≃ β₂` generates an equivalence between `β₁ × α₁`… | 1 | bundled | `{α₁ : Type u_9} {β₁ : Type u_11} {β₂ : Type u_12} (e : α₁ → β₁ ≃ β₂) : β₁ × α₁ ≃ β₂ × α₁` | none | none | thin | 19.89 | 0 | 4 |
| 233 | Equiv.prodCongrRight | Logic/Equiv/Prod.lean | A family of equivalences `∀ (a : α₁), β₁ ≃ β₂` generates an equivalence between `α₁ × β₁`… | 1 | bundled | `{α₁ : Type u_9} {β₁ : Type u_11} {β₂ : Type u_12} (e : α₁ → β₁ ≃ β₂) : α₁ × β₁ ≃ α₁ × β₂` | none | none | rich | 19.89 | 0 | 6 |
| 234 | Nat.greatestFib | Data/Nat/Fib/Zeckendorf.lean | The greatest index of a Fibonacci number less than or equal to `n`. | 1 | value | `(n : ℕ) : ℕ` | rich | none | rich | 19.74 | 0 | 6 |
| 235 | Function.Fiber.mk | Logic/Function/FiberPartition.lean | Given `y : Y`, `Fiber.mk f y` is the fiber of `f` that `y` belongs to, as an element of `… | 1 | value | `{Y : Type u_2} {Z : Type u_3} (f : Y → Z) (y : Y) : Function.Fiber f` | none | none | thin | 19.74 | 0 | 2 |
| 236 | Finsupp.multinomial | Data/Nat/Choose/Multinomial.lean | Alternative multinomial definition based on a finsupp, using the support   for the big op… | 1 | value | `{α : Type u_1} (f : α →₀ ℕ) : ℕ` | none | none | thin | 19.66 | 1 | 4 |
| 237 | Finset.bipartiteBelow | Combinatorics/Enumerative/DoubleCounting.lean | Elements of `s` which are "below" `b` according to relation `r`. | 1 | value | `{α : Type u_2} {β : Type u_3} (r : α → β → Prop) (s : Finset α) (b : β) [(a : α) → Decidable (r a b)] : Finset α` | none | thin | rich | 19.61 | 0 | 15 |
| 238 | Finset.bipartiteAbove | Combinatorics/Enumerative/DoubleCounting.lean | Elements of `t` which are "above" `a` according to relation `r`. | 1 | value | `{α : Type u_2} {β : Type u_3} (r : α → β → Prop) (t : Finset β) (a : α) [DecidablePred (r a)] : Finset β` | none | thin | rich | 19.61 | 0 | 15 |
| 239 | Finset.sup | Data/Finset/Lattice/Fold.lean | Supremum of a finite set: `sup {a, b, c} f = f a ⊔ f b ⊔ f c` | 1 | value | `{α : Type u_2} {β : Type u_3} [SemilatticeSup α] [OrderBot α] (s : Finset β) (f : β → α) : α` | none | thin | rich | 19.48 | 11 | 289 |
| 240 | Function.Involutive.toPerm | Logic/Equiv/Basic.lean | Convert an involutive function `f` to a permutation with `toFun = invFun = f`. | 1 | bundled | `{α : Sort u_1} (f : α → α) (h : Function.Involutive f) : Equiv.Perm α` | none | none | thin | 19.16 | 0 | 3 |
| 241 | Finset.restrict | Data/Finset/Pi.lean | Restrict domain of a function `f` to a finite set `s`. | 1 | value | `{ι : Type u_2} {π : ι → Type u_3} (s : Finset ι) (f : (i : ι) → π i) (i : ↥s) : π ↑i` | none | thin | rich | 19.11 | 9 | 20 |
| 242 | Nat.chineseRemainder | Data/Nat/ModEq.lean | The natural number less than `n*m` congruent to `a` mod `n` and `b` mod `m` | 1 | value | `{m n : ℕ} (co : n.Coprime m) (a b : ℕ) : { k // k ≡ a [MOD n] ∧ k ≡ b [MOD m] }` | none | none | rich | 19.05 | 0 | 8 |
| 243 | Nat.Subtype.succ | Logic/Denumerable.lean | Returns the next natural in a set, according to the usual ordering of `ℕ`. | 1 | value | `{s : Set ℕ} [Infinite ↑s] [DecidablePred fun x => x ∈ s] (x : ↑s) : ↑s` | none | none | rich | 19.01 | 0 | 5 |
| 244 | Finset.image | Data/Finset/Image.lean | `image f s` is the forward image of `s` under `f`. | 1 | value | `{α : Type u_1} {β : Type u_2} [DecidableEq β] (f : α → β) (s : Finset α) : Finset β` | none | thin | rich | 18.87 | 39 | 411 |
| 245 | ArithmeticFunction.dirichletInverse | NumberTheory/ArithmeticFunction/Defs.lean | Given an inverse of `f 1`, construct the Dirichlet inverse of `f`. | 1 | value | `{R : Type u_1} [Ring R] (f : ℕ → R) (hf : Invertible (f 1)) : ArithmeticFunction R` | none | none | rich | 18.70 | 0 | 5 |
| 246 | zmultiplesHom | Data/Int/Cast/Lemmas.lean | Additive homomorphisms from `ℤ` are defined by the image of `1`. | 1 | bundled | `(β : Type u_4) [AddGroup β] : β ≃ (ℤ →+ β)` | none | none | thin | 18.61 | 4 | 4 |
| 247 | Cycle.Subsingleton | Data/List/Cycle.lean | A `s : Cycle α` that is at most one element. | 1 | prop | `{α : Type u_1} (s : Cycle α) : Prop` | none | thin | rich | 18.44 | 0 | 7 |
| 248 | Nat.count | Data/Nat/Count.lean | Count the number of naturals `k < n` satisfying `p k`. | 1 | value | `(p : ℕ → Prop) [DecidablePred p] (n : ℕ) : ℕ` | none | none | rich | 18.11 | 1 | 48 |
| 249 | Set.iInter | Order/SetNotation.lean | Indexed intersection of a family of sets | 1 | value | `{α : Type u} {ι : Sort v} (s : ι → Set α) : Set α` | none | thin | rich | 18.09 | 10 | 199 |
| 250 | List.kerase | Data/List/Sigma.lean | Remove the first pair with the key `a`. | 1 | value | `{α : Type u} {β : α → Type v} [DecidableEq α] (a : α) : List (Sigma β) → List (Sigma β)` | none | thin | rich | 17.99 | 1 | 26 |
| 251 | Finset.finsupp | Data/Finset/Finsupp.lean | Finitely supported product of finsets. | 1 | value | `{ι : Type u_1} {α : Type u_2} [Zero α] (s : Finset ι) (t : ι → Finset α) : Finset (ι →₀ α)` | none | thin | rich | 17.89 | 0 | 17 |
| 252 | Function.Coequalizer.mk | Logic/Function/Coequalizer.lean | The canonical projection to the coequalizer. | 1 | value | `{α : Type u_1} {β : Type u_2} (f g : α → β) (x : β) : Function.Coequalizer f g` | none | none | thin | 17.44 | 2 | 4 |
| 253 | toAntisymmetrization | Order/Antisymmetrization.lean | Turn an element into its antisymmetrization. | 1 | value | `{α : Type u_1} (r : α → α → Prop) [IsPreorder α r] : α → Antisymmetrization α r` | none | none | rich | 17.44 | 11 | 11 |
| 254 | Bifunctor.mapEquiv | Logic/Equiv/Functor.lean | Apply a bifunctor to a pair of `Equiv`s. | 1 | bundled | `{α β : Type u} {α' β' : Type v} (F : Type u → Type v → Type w) [Bifunctor F] [LawfulBifunctor F] (h : α ≃ β) (h' : α' ≃ β') : F α α' ≃ F β β'` | none | none | thin | 17.09 | 0 | 3 |
| 255 | Functor.mapEquiv | Logic/Equiv/Functor.lean | Apply a functor to an `Equiv`. | 1 | bundled | `{α β : Type u} (f : Type u → Type v) [Functor f] [LawfulFunctor f] (h : α ≃ β) : f α ≃ f β` | none | none | rich | 15.80 | 2 | 5 |
| 256 | Function.Embedding.subtype | Logic/Embedding/Basic.lean | Embedding of a `Subtype`. | 1 | bundled | `{α : Sort u_1} (p : α → Prop) : Subtype p ↪ α` | none | none | rich | 14.58 | 5 | 8 |
