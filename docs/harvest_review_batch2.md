# Harvest Batch 2 Review

Human-readable review of the second mechanical harvest (`miner/output/harvest_manifest.jsonl`), generated read-only from that file. This batch implements the gates-then-preference-score selection redesign — see `docs/design/definition_selection_2026-07-21.md` for the design of record this harvest follows, and `docs/harvest_review_batch1.md` for the prior (revision 2) harvest this one replaces in `miner/output/`.

**What changed since batch 1, mechanically:** the corpus widened from the original 5 corners (782 scanned hits) to 5 corners + 69 "basics"/"shallows" files across `Order/`, `Algebra/`, `Combinatorics/`, `NumberTheory/` (964 scanned hits total — see `miner/config.py`'s `TARGET_MODULES` comment for the exact file list and the dry-scan count that confirmed it before the full run). Selection replaced miner stage 1's single weighted score with six hard eligibility gates (`miner/gates.py`) followed by a small preference score dominated by structural richness (`miner/richness.py`), per the design doc.

## 0. Headline finding: the gate-eligible set is far smaller than `top_n`

**Only 52 candidates passed all six gates, against a requested `top_n = 100`.** Every gate-eligible candidate is therefore included — the top-N cutoff never actually engaged this batch, and there was no "eligible but outranked" tier at all (0 candidates). This is reported prominently per this task's own instruction, and the run was completed rather than aborted or silently re-tuned; the two findings below are exactly the kind of evidence the design doc's thresholds are meant to be adjusted from.

### Finding A: `MENTION_FLOOR = 30` is by far the most aggressive gate

| Gate | Fails (of 950 verified) | % |
|---|---|---|
| **mention_floor** | **831** | **87.5%** |
| dependency_vocabulary | 430 | 45.3% |
| fact_supply | 410 | 43.2% |
| length_band | 48 | 5.1% |
| anti_plumbing | 17 | 1.8% |
| docstring_floor | 15 | 1.6% |

`length_band`, `docstring_floor`, and `anti_plumbing` all behave close to their batch-1-derived design intent (low single-digit percentages). `mention_floor` alone excludes the overwhelming majority of the *widened* corpus — close to, though just under, the ">90%" pathological example the task instructions named. This is not a bug: `mention_count` (full-corpus raw occurrence count) is genuinely much lower, on average, for definitions freshly scanned from `Order/`, `Algebra/`, `Combinatorics/`, and `NumberTheory/` "basics" files than for the original five foundational corners, which were selected in batch 1 partly *because* they're heavily used everywhere. Widening the corpus into less-central territory (design doc §6's explicit goal) directly trades against a flat mention floor tuned on the old corpus. **This is the clearest single piece of evidence that `MENTION_FLOOR` (or its scope — see the config comment on why `mention_count` rather than `theorem_mention_count` was chosen) is the first dial worth revisiting before the next mining round.**

### Finding B: the dependency-vocabulary gate has a real, quantified false-failure mechanism

Investigating why `Pairwise` and `Set.Pairwise` — both present and richly-mentioned in batch 1 — now fail `dependency_vocabulary` surfaced a genuine bug, not a threshold-tuning issue:

`Pairwise`'s only `referenced_constants` are `['i', 'j']` — the bound variables from its own body (`∀ ⦃i j⦄, i ≠ j → r i j`), a known noise source of the `referenced_constants` extraction (see `miner.verify`'s module docstring). `miner.depindex`'s declaration index, built by scanning the **entire** Mathlib tree, happens to also index unrelated real declarations that are bare-named `i` and `j` in some completely different file (`Algebra/Homology/Factorizations/CM5a.lean` and `AlgebraicGeometry/EllipticCurve/Weierstrass.lean`, respectively) — a short bare-identifier collision, not a real dependency. The gate then (correctly, given its inputs) sees `i` "resolving" to a non-vocabulary module and fails the candidate for a dependency it doesn't actually have.

Quantified impact: of the 430 candidates failing `dependency_vocabulary`, **342 (79.5%) have at least one short (≤3-char), lowercase, unqualified token among their references** — exactly the shape of this collision, not a real qualified constant. Recomputing the gate with those tokens excluded shows **230 of the 430 (53.5%) would pass outright** if this noise were filtered before resolution. This is very likely a meaningfully undercounted eligible set, not a reflection of the corpus genuinely depending on exotic infrastructure at that rate. **Flagged here, not fixed** — per this task's explicit scope (no threshold tuning or gate-logic changes beyond what was specified), but this is the second clear candidate for a follow-up fix: either filter short/lowercase bare tokens out of `referenced_constants` before gate resolution, or stop indexing single-token bare names in `miner.depindex` (require qualified-name matches, or a minimum name length) so a real reference can't collide with an unrelated three-letter local variable.

Both findings point the same direction: the *true* gate-eligible set, once these two dials are revisited, is almost certainly larger than 52 — this batch's small included set is a measurement artifact of first-pass threshold choices on a wider, less-central corpus, not evidence that the widened corpus lacks good candidates.

## 1. Summary

### Corpus counts

- **Scanned**: 964 (782 original + 182 from the widened corners)
- **Verified** (elaborates): 950
- **Gate-eligible** (passed all six gates): 52
- **Included** (== gate-eligible, since 52 < top_n=100): 52
- **Excluded**: 912 (= 898 gate-failed + 0 eligible-but-outranked + 14 does-not-elaborate)
  - failed one or more gates: 898
  - eligible but outranked: 0
  - does not elaborate: 14
  - of the above, 1 (`Nat.digitsAux1`) also independently carries a curation `exclude` note (see `miner/curation.yaml`) -- it was excluded by gates regardless, so this is a subset annotation, not an additional bucket; the curation "final pass" never had to act this round, since nothing reached it that curation would have pulled

### Gate-attrition table (sequential survival)

Gates applied in design-doc §3 order; each row shows how many of the *remaining* pool at that point fail this specific gate, and how many survive into the next row. (The independent, non-sequential fail rate per gate — used for Finding A above — is a different, larger number for gates applied later in this sequence, since by then the pool has already shrunk.)

| Gate | Fails (of those reaching it) | Cumulative survivors |
|---|---|---|
| (start: verified candidates) | | 950 |
| (a) mention_floor | 831 | 119 |
| (b) length_band | 2 | 117 |
| (c) docstring_floor | 5 | 112 |
| (d) dependency_vocabulary | 50 | 62 |
| (e) anti_plumbing | 0 | 62 |
| (f) fact_supply | 10 | 52 |
| **eligible set** | | **52** |
| top_n=100 cutoff | (never engaged — eligible set smaller than top_n) | **52** |

### Supply tier distribution (52 included)

| Tier | Casework | Membership | Global |
|---|---|---|---|
| Rich | 10 | 2 | 17 |
| Thin | 0 | 25 | 21 |
| None | 42 | 25 | 14 |

### Distribution across source modules (52 included)

| Module | Count |
|---|---|
| Logic/Equiv | 14 |
| Data/Finset | 14 |
| Data/Nat | 9 |
| Logic/Function | 3 |
| Order/SetNotation.lean | 3 |
| Logic/Embedding | 2 |
| Data/Int | 2 |
| Logic/Basic.lean | 1 |
| Algebra/GroupWithZero | 1 |
| Order/Antisymmetrization.lean | 1 |
| NumberTheory/ArithmeticFunction | 1 |
| Order/SymmDiff.lean | 1 |

Notably: **no `Combinatorics/` candidate survives all six gates.** The 13 Combinatorics files scanned (Pigeonhole, Colex, Derangements, and six Enumerative counting-sequence files) contributed hits, but every one was filtered out — mostly by `mention_floor` (elementary combinatorics definitions like `Nat.centralBinom`-adjacent material are used far less across the corpus than core `Nat`/`Finset` vocabulary) with some falling to `dependency_vocabulary` (their natural dependencies — `Multiset`, `Sym`, `Polynomial`-adjacent machinery for generating functions — sit outside this round's vocabulary list). Worth a specific look once Finding A/B are addressed, since the whole point of widening into Combinatorics was lost this round.

### Richness-score distribution (52 included, total component)

| Richness | Count |
|---|---|
| 0 | 23 |
| 1 | 10 |
| 2 | 8 |
| 4 | 3 |
| 6 | 2 |
| 9 | 2 |
| 12 | 2 |
| 13 | 1 |
| 14 | 1 |

Nearly half the included set (23/52) has zero measured structural richness — every one of these is either a delegation/projection (`List.toFinset := Multiset.toFinset l`) or a definition whose real structure is hidden behind notation (`Equiv.symm`, `sInter := sInf S`), exactly the blind spots `miner.richness`'s own module docstring names. These candidates are included only because the eligible pool is small enough (52, below top_n) that nothing outranks them — not because richness endorses them. Once Finding A/B grow the eligible pool, richness-zero candidates like these should mostly fall out of a real top-100 on their own, without needing a separate fix.

## 2. Full ranked table (all 52 included)

Description: docstring (truncated to fit) where present. Score components: `r` = richness total, `d` = docstring-substance score, `b` = breadth (count of non-`none` supply tiers). No `Curation` column entries this round — the only curated name (`Nat.digitsAux1`) was independently gate-excluded before curation ran, so its curation note appears only in the gate-excluded section, not here.

| Rank | Name | Module | Description | Richness | Signature | CW | Mem | Glob | Score (components) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Nat.clog | Data/Nat/Log.lean | `clog b n`, is the upper logarithm of natural number `n` in base `b`. It returns the smal… | 14 | `(b n : ℕ) : ℕ` | Rich | None | Thin | 153.94 (r=14, d=5.97, b=2) |
| 2 | finSumFinEquiv | Logic/Equiv/Fin/Basic.lean | Equivalence between `Fin m ⊕ Fin n` and `Fin (m + n)` | 13 | `{m n : ℕ} : Fin m ⊕ Fin n ≃ Fin (m + n)` | None | None | Rich | 138.05 (r=13, d=3.53, b=1) |
| 3 | Nat.log | Data/Nat/Log.lean | `log b n`, is the logarithm of natural number `n` in base `b`. It returns the largest `k … | 12 | `(b n : ℕ) : ℕ` | Rich | None | Rich | 133.83 (r=12, d=5.91, b=2) |
| 4 | Equiv.prodAssoc | Logic/Equiv/Prod.lean | Type product is associative up to an equivalence. | 12 | `(α : Type u_9) (β : Type u_10) (γ : Type u_11) : (α × β) × γ ≃ α × β × γ` | None | None | Thin | 127.80 (r=12, d=3.40, b=1) |
| 5 | Finset.pi | Data/Finset/Pi.lean | Given a finset `s` of `α` and for all `a : α` a finset `t a` of `β a`, then one can defin… | 9 | `{α : Type u_1} {β : α → Type u} [DecidableEq α] (s : Finset α) (t : (a : α) → Finset (β a)) : Finset ((a : α) → a ∈ s → β a)` | None | Thin | None | 103.98 (r=9, d=6.49, b=1) |
| 6 | Equiv.Set.univ | Logic/Equiv/Set.lean | `univ α` is equivalent to `α`. | 9 | `(α : Type u_3) : ↑Set.univ ≃ α` | None | Thin | None | 95.80 (r=9, d=2.40, b=1) |
| 7 | Equiv.sumCongr | Logic/Equiv/Sum.lean | If `α ≃ α'` and `β ≃ β'`, then `α ⊕ β ≃ α' ⊕ β'`. This is `Sum.map` as an equivalence. | 6 | `{α₁ : Type u_9} {α₂ : Type u_10} {β₁ : Type u_11} {β₂ : Type u_12} (ea : α₁ ≃ α₂) (eb : β₁ ≃ β₂) : α₁ ⊕ β₁ ≃ α₂ ⊕ β₂` | None | None | Thin | 71.41 (r=6, d=5.20, b=1) |
| 8 | Equiv.swap | Logic/Equiv/Basic.lean | `swap a b` is the permutation that swaps `a` and `b` and leaves other values as is. | 6 | `{α : Sort u_1} [DecidableEq α] (a b : α) : Equiv.Perm α` | None | None | Rich | 69.32 (r=6, d=4.16, b=1) |
| 9 | Function.prod | Logic/Function/Defs.lean | Product of functions: `Function.prod f g i = (f i, g i)`, where the types of `f i` and `g… | 4 | `{ι : Sort u_3} {α : ι → Type u_1} {β : ι → Type u_2} (f : (i : ι) → α i) (g : (i : ι) → β i) (i : ι) : α i × β i` | None | None | Thin | 50.04 (r=4, d=4.52, b=1) |
| 10 | Xor | Logic/Basic.lean | `Xor a b` is the exclusive-or of propositions. | 4 | `(a b : Prop) : Prop` | None | Thin | Rich | 48.59 (r=4, d=3.30, b=2) |
| 11 | Function.Embedding.subtype | Logic/Embedding/Basic.lean | Embedding of a `Subtype`. | 4 | `{α : Sort u_1} (p : α → Prop) : Subtype p ↪ α` | None | None | Thin | 44.58 (r=4, d=1.79, b=1) |
| 12 | IsNilpotent | Algebra/GroupWithZero/Basic.lean | An element is said to be nilpotent if some natural-number-power of it equals zero. Note … | 2 | `{R : Type u_3} [Zero R] [Pow R ℕ] (x : R) : Prop` | None | Thin | Rich | 39.22 (r=2, d=8.61, b=2) |
| 13 | Function.Bijective | Logic/Function/Defs.lean | A function is called bijective if it is both injective and surjective. | 2 | `{α : Sort u₁} {β : Sort u₂} (f : α → β) : Prop` | None | Thin | Rich | 31.86 (r=2, d=4.93, b=2) |
| 14 | AntisymmRel | Order/Antisymmetrization.lean | The antisymmetrization relation `AntisymmRel r` is defined so that `AntisymmRel r a b ↔ r… | 2 | `{α : Type u_1} (r : α → α → Prop) (a b : α) : Prop` | None | Thin | Rich | 30.86 (r=2, d=4.43, b=2) |
| 15 | Finset.noncommProd | Data/Finset/NoncommProd.lean | Sum of a `s : Finset α` mapped with `f : α → β` with `[AddMonoid β]`, given a proof that … | 2 | `{α : Type u_3} {β : Type u_4} [Monoid β] (s : Finset α) (f : α → β) (comm : (↑s).Pairwise (Function.onFun Commute f)) : β` | None | Thin | None | 30.59 (r=2, d=4.80, b=1) |
| 16 | Nat.find | Data/Nat/Find.lean | If `p` is a (decidable) predicate on `ℕ` and `hp : ∃ (n : ℕ), p n` is a proof that there … | 1 | `{p : ℕ → Prop} [DecidablePred p] (H : ∃ n, p n) : ℕ` | None | None | Rich | 27.64 (r=1, d=8.32, b=1) |
| 17 | Nat.minFac | Data/Nat/Prime/Defs.lean | Returns the smallest prime factor of `n ≠ 1`. | 2 | `(n : ℕ) : ℕ` | Rich | None | None | 27.52 (r=2, d=3.26, b=1) |
| 18 | Nat.unpair | Data/Nat/Pairing.lean | Unpairing function for the natural numbers. | 2 | `(n : ℕ) : ℕ × ℕ` | Rich | None | None | 27.36 (r=2, d=3.18, b=1) |
| 19 | Nat.pair | Data/Nat/Pairing.lean | Pairing function for the natural numbers. | 2 | `(a b : ℕ) : ℕ` | Rich | None | None | 27.18 (r=2, d=3.09, b=1) |
| 20 | Equiv.cast | Logic/Equiv/Defs.lean | Equivalence between equal types. | 2 | `{α β : Sort u_1} (h : α = β) : α ≃ β` | None | None | Thin | 26.13 (r=2, d=2.56, b=1) |
| 21 | Finset.filter | Data/Finset/Filter.lean | `Finset.filter p s` is the set of elements of `s` that satisfy `p`. For example, one can… | 1 | `{α : Type u_1} (p : α → Prop) [DecidablePred p] (s : Finset α) : Finset α` | None | Thin | Thin | 24.71 (r=1, d=6.36, b=2) |
| 22 | Finset.cons | Data/Finset/Insert.lean | `cons a s h` is the set `{a} ∪ s` containing `a` and the elements of `s`. It is the same … | 1 | `{α : Type u_1} (a : α) (s : Finset α) (h : a ∉ s) : Finset α` | None | Thin | Thin | 24.69 (r=1, d=6.35, b=2) |
| 23 | Function.Commute | Logic/Function/Conjugate.lean | Two maps `f g : α → α` commute if `f (g x) = g (f x)` for all `x : α`. Given `h : Functio… | 1 | `{α : Type u_1} (f g : α → α) : Prop` | None | Thin | Thin | 24.20 (r=1, d=6.10, b=2) |
| 24 | Finset.sup' | Data/Finset/Lattice/Fold.lean | Given nonempty finset `s` then `s.inf' H f` is the infimum of its image under `f` in (pos… | 1 | `{α : Type u_2} {β : Type u_3} [SemilatticeSup α] (s : Finset β) (H : s.Nonempty) (f : β → α) : α` | None | Thin | None | 24.00 (r=1, d=6.50, b=1) |
| 25 | Nat.ModEq | Data/Nat/ModEq.lean | Modular equality. `n.ModEq a b`, or `a ≡ b [MOD n]`, means that `a % n = b % n`. | 1 | `(n a b : ℕ) : Prop` | Rich | Rich | None | 20.22 (r=1, d=4.11, b=2) |
| 26 | Int.ModEq | Data/Int/ModEq.lean | `a ≡ b [ZMOD n]` when `a % n = b % n`. | 1 | `(n a b : ℤ) : Prop` | Rich | Rich | None | 19.89 (r=1, d=3.94, b=2) |
| 27 | Finset.sup | Data/Finset/Lattice/Fold.lean | Supremum of a finite set: `sup {a, b, c} f = f a ⊔ f b ⊔ f c` | 1 | `{α : Type u_2} {β : Type u_3} [SemilatticeSup α] [OrderBot α] (s : Finset β) (f : β → α) : α` | None | Thin | Thin | 19.48 (r=1, d=3.74, b=2) |
| 28 | Finset.image | Data/Finset/Image.lean | `image f s` is the forward image of `s` under `f`. | 1 | `{α : Type u_1} {β : Type u_2} [DecidableEq β] (f : α → β) (s : Finset α) : Finset β` | None | Thin | Rich | 18.87 (r=1, d=3.43, b=2) |
| 29 | Set.iInter | Order/SetNotation.lean | Indexed intersection of a family of sets | 1 | `{α : Type u} {ι : Sort v} (s : ι → Set α) : Set α` | None | Thin | None | 17.09 (r=1, d=3.04, b=1) |
| 30 | Finset.min | Data/Finset/Max.lean | Let `s` be a finset in a linear order. Then `s.min` is the minimum of `s` if `s` is not e… | 0 | `{α : Type u_2} [LinearOrder α] (s : Finset α) : WithTop α` | None | Thin | Thin | 16.31 (r=0, d=7.15, b=2) |
| 31 | Finset.map | Data/Finset/Image.lean | When `f` is an embedding of `α` in `β` and `s` is a finset in `α`, then `s.map f` is the … | 0 | `{α : Type u_1} {β : Type u_2} (f : α ↪ β) (s : Finset α) : Finset β` | None | Thin | Thin | 16.25 (r=0, d=7.12, b=2) |
| 32 | Equiv.toEmbedding | Logic/Embedding/Basic.lean | Convert an `α ≃ β` to `α ↪ β`. This is also available as a coercion `Equiv.coeEmbedding`… | 0 | `{α : Sort u} {β : Sort v} (f : α ≃ β) : α ↪ β` | None | None | Thin | 13.56 (r=0, d=6.28, b=1) |
| 33 | ArithmeticFunction | NumberTheory/ArithmeticFunction/Defs.lean | An arithmetic function is a function from `ℕ` that maps 0 to 0. In the literature, they a… | 0 | `(R : Type u_1) [Zero R] : Type u_1` | None | None | Rich | 11.46 (r=0, d=5.23, b=1) |
| 34 | Finset.card | Data/Finset/Card.lean | `s.card` is the number of elements of `s`, aka its cardinality. The notation `#s` can be… | 0 | `{α : Type u_1} (s : Finset α) : ℕ` | None | Thin | Rich | 11.25 (r=0, d=4.62, b=2) |
| 35 | PartialEquiv.trans | Logic/Equiv/PartialEquiv.lean | Composing two partial equivs, by restricting to the maximal domain where their compositio… | 0 | `{α : Type u_1} {β : Type u_2} {γ : Type u_3} (e : PartialEquiv α β) (e' : PartialEquiv β γ) : PartialEquiv α γ` | None | None | Thin | 11.16 (r=0, d=5.08, b=1) |
| 36 | finSuccEquiv | Logic/Equiv/Fin/Basic.lean | Equivalence between `Fin (n + 1)` and `Option (Fin n)`. This is a version of `Fin.pred` t… | 0 | `(n : ℕ) : Fin (n + 1) ≃ Option (Fin n)` | None | None | Rich | 11.09 (r=0, d=5.04, b=1) |
| 37 | Nat.bit | Data/Nat/BinaryRec.lean | `bit b` appends the digit `b` to the little end of the binary representation of its natur… | 0 | `(b : Bool) (n : ℕ) : ℕ` | Rich | None | Thin | 10.91 (r=0, d=4.45, b=2) |
| 38 | Finset.erase | Data/Finset/Erase.lean | `erase s a` is the set `s - {a}`, that is, the elements of `s` which are not equal to `… | 0 | `{α : Type u_1} [DecidableEq α] (s : Finset α) (a : α) : Finset α` | None | Thin | Thin | 10.53 (r=0, d=4.26, b=2) |
| 39 | Finset.range | Data/Finset/Range.lean | `range n` is the set of natural numbers less than `n`. | 0 | `(n : ℕ) : Finset ℕ` | Rich | Thin | Rich | 10.11 (r=0, d=3.56, b=3) |
| 40 | Multiset.toFinset | Data/Finset/Dedup.lean | `toFinset s` removes duplicates from the multiset `s` to produce a finset. | 0 | `{α : Type u_1} [DecidableEq α] (s : Multiset α) : Finset α` | None | Thin | Rich | 10.01 (r=0, d=4.01, b=2) |
| 41 | Equiv.prodComm | Logic/Equiv/Prod.lean | Type product is commutative up to an equivalence: `α × β ≃ β × α`. This is `Prod.swap` as… | 0 | `(α : Type u_9) (β : Type u_10) : α × β ≃ β × α` | None | None | Thin | 9.91 (r=0, d=4.45, b=1) |
| 42 | List.toFinset | Data/Finset/Dedup.lean | `toFinset l` removes duplicates from the list `l` to produce a finset. | 0 | `{α : Type u_1} [DecidableEq α] (l : List α) : Finset α` | None | Thin | Rich | 9.86 (r=0, d=3.93, b=2) |
| 43 | symmDiff | Order/SymmDiff.lean | The symmetric difference operator on a type with `⊔` and `\` is `(A \ B) ⊔ (B \ A)`. | 0 | `{α : Type u_2} [Max α] [SDiff α] (a b : α) : α` | None | None | Rich | 9.35 (r=0, d=4.17, b=1) |
| 44 | Nat.primeFactors | Data/Nat/PrimeFin.lean | The prime factors of a natural number as a finset. | 0 | `(n : ℕ) : Finset ℕ` | Rich | Thin | None | 8.87 (r=0, d=3.43, b=2) |
| 45 | Equiv.trans | Logic/Equiv/Defs.lean | Composition of equivalences `e₁ : α ≃ β` and `e₂ : β ≃ γ`. | 0 | `{α : Sort u} {β : Sort v} {γ : Sort w} (e₁ : α ≃ β) (e₂ : β ≃ γ) : α ≃ γ` | None | None | Thin | 8.33 (r=0, d=3.66, b=1) |
| 46 | Equiv.image | Logic/Equiv/Set.lean | A set is equivalent to its image under an equivalence. | 0 | `{α : Type u_3} {β : Type u_4} (e : α ≃ β) (s : Set α) : ↑s ≃ ↑(⇑e '' s)` | None | Thin | None | 8.11 (r=0, d=3.56, b=1) |
| 47 | Equiv.symm | Logic/Equiv/Defs.lean | Inverse of an equivalence `e : α ≃ β`. | 0 | `{α : Sort u} {β : Sort v} (e : α ≃ β) : β ≃ α` | None | None | Rich | 6.89 (r=0, d=2.94, b=1) |
| 48 | PartialEquiv.symm | Logic/Equiv/PartialEquiv.lean | The inverse of a partial equivalence | 0 | `{α : Type u_1} {β : Type u_2} (e : PartialEquiv α β) : PartialEquiv β α` | None | None | Thin | 6.67 (r=0, d=2.83, b=1) |
| 49 | Equiv.ulift | Logic/Equiv/Defs.lean | `ULift α` is equivalent to `α`. | 0 | `{α : Type v} : ULift.{u, v} α ≃ α` | None | None | Thin | 5.97 (r=0, d=2.48, b=1) |
| 50 | Set.sInter | Order/SetNotation.lean | Intersection of a set of sets. | 0 | `{α : Type u} (S : Set (Set α)) : Set α` | None | Thin | None | 5.80 (r=0, d=2.40, b=1) |
| 51 | Int.castRingHom | Data/Int/Cast/Lemmas.lean | `coe : ℤ → α` as a `RingHom`. | 0 | `(α : Type u_3) [NonAssocRing α] : ℤ → +* α` | None | None | Thin | 5.61 (r=0, d=2.30, b=1) |
| 52 | Set.sUnion | Order/SetNotation.lean | Union of a set of sets. | 0 | `{α : Type u} (S : Set (Set α)) : Set α` | None | Thin | None | 3.77 (r=0, d=1.39, b=1) |

## 3. Detail cards: top 10

Only the top 10 get cards this round (not top 25, as in batch 1) — with the eligible set at 52, cards for all richness-bearing entries would essentially duplicate §2's table; the top 10 are the ones where richness actually did its intended job of picking out condition-bearing definitions over trivial ones.

### 1. Nat.clog
*Data/Nat/Log.lean*

**Docstring:**
> `clog b n`, is the upper logarithm of natural number `n` in base `b`. It returns the smallest `k : ℕ` such that `n ≤ b^k`, so if `b^k = n`, it returns exactly `k`.

**Source:**
```lean
def clog (b n : ℕ) : ℕ :=
  if 1 < b ∧ 1 < n then (go b n).2 + 1 else 0 where
  go : ℕ → ℕ → ℕ × ℕ
  | b, 0 => (b / n, 0)
  | b, fuel + 1 =>
    if n ≤ b then (b / n, 0)
    else
      let (q, e) := go (b * b) fuel
      if q < b then (q, 2 * e + 1) else (q / b, 2 * e)
```

**Richness:** 14 total — 1 conjunction, 5 conditionals (three `if`s plus two match arms in the `where`-clause `go`), 8 comparisons. **Notes:** Richness correctly identifies this as the most structurally complex definition in the batch: a guarded top-level conditional plus a fuel-recursive auxiliary with its own nested conditionals. Exactly the kind of definition — genuine boundary logic, not a one-liner — the redesign was meant to surface, and it does, at rank 1 (batch 1 had it at rank 25, well down the old dependency-count-dominated order).

### 2. finSumFinEquiv
*Logic/Equiv/Fin/Basic.lean*

**Docstring:**
> Equivalence between `Fin m ⊕ Fin n` and `Fin (m + n)`

**Source:**
```lean
def finSumFinEquiv : Fin m ⊕ Fin n ≃ Fin (m + n) where
  toFun := Sum.elim (Fin.castAdd n) (Fin.natAdd m)
  invFun i := @Fin.addCases m n (fun _ => Fin m ⊕ Fin n) Sum.inl Sum.inr i
  left_inv x := by rcases x with y | y <;> simp
  right_inv x := by refine Fin.addCases (fun i => ?_) (fun i => ?_) x <;> simp
```

**Richness:** 13 — 3 conditionals (`=>` in the structure-instance fields and `rcases`/pattern branches), 10 comparisons (mostly `=` from the `where`-style field assignments, textually indistinguishable from propositional equality by this stage's heuristic — see richness's blind-spot list). **Notes:** A genuine caution here: much of this richness count comes from Lean's `where`-block field-assignment syntax (`toFun := ...`), not from mathematically meaningful equalities — a real blind spot of textual `=`-counting worth watching as more `where`-structured equivalences enter the corpus.

### 3. Nat.log
*Data/Nat/Log.lean*

**Docstring:**
> `log b n`, is the logarithm of natural number `n` in base `b`. It returns the largest `k : ℕ` such that `b^k ≤ n`, so if `b^k = n`, it returns exactly `k`.

**Source:**
```lean
def log (b n : ℕ) : ℕ :=
  if b ≤ 1 then 0 else (go b n).2 where
  go : ℕ → ℕ → ℕ × ℕ
  | _, 0 => (n, 0)
  | b, fuel + 1 =>
    if n < b then
      (n, 0)
    else
      let (q, e) := go (b * b) fuel
      if q < b then (q, 2 * e) else (q / b, 2 * e + 1)
```

**Richness:** 12 — 5 conditionals, 7 comparisons. **Notes:** `clog`'s dual (ceiling vs. floor log), same fuel-recursive shape; both surfacing at the top is expected, not a coincidence — see rank 1's card.

### 4. Equiv.prodAssoc
*Logic/Equiv/Prod.lean*

**Docstring:**
> Type product is associative up to an equivalence.

**Source:**
```lean
def prodAssoc (α β γ) : (α × β) × γ ≃ α × β × γ :=
  ⟨fun p => (p.1.1, p.1.2, p.2), fun p => ((p.1, p.2.1), p.2.2), fun ⟨⟨_, _⟩, _⟩ => rfl,
    fun ⟨_, ⟨_, _⟩⟩ => rfl⟩
```

**Richness:** 12 — 4 conditionals, 8 comparisons, both entirely from the four `fun ... =>` lambda arms of the anonymous-constructor equivalence proof and its `_`-pattern destructuring. **Notes:** A clear miscount by the "`=>` means a match arm" heuristic (richness's documented blind spot): these are lambda bodies of an equivalence's four components (`toFun`/`invFun`/`left_inv`/`right_inv`), not case-based branching on the *definition's own* input — the definition itself (rearranging a nested product) has essentially no real conditional structure. Worth a second look before trusting this rank at face value; see the digest's "worth a second look" list.

### 5. Finset.pi
*Data/Finset/Pi.lean*

**Docstring:**
> Given a finset `s` of `α` and for all `a : α` a finset `t a` of `β a`, then one can define the finset `s.pi t` of all functions defined on elements of `s` taking values in `t a` for `a ∈ s`. Note that the elements of `s.pi t` are only partially defined, on `s`.

**Source:**
```lean
def pi (s : Finset α) (t : ∀ a, Finset (β a)) : Finset (∀ a ∈ s, β a) :=
  ⟨s.1.pi fun a => (t a).1, s.nodup.pi fun a _ => (t a).nodup⟩
```

**Richness:** 9 — 2 conditionals (lambda arms, same blind spot as rank 4), 2 quantifiers (from the dependent-Pi signature `∀ a, Finset (β a)` and the return type's `∀ a ∈ s, β a`), 4 comparisons, 1 hypothesis binder. **Notes:** Unlike rank 4, this one's quantifier/hypothesis-binder richness is genuinely earned — the signature itself is a dependent product over a finite index set, real content, not lambda-arm noise.

### 6. Equiv.Set.univ
*Logic/Equiv/Set.lean*

**Docstring:**
> `univ α` is equivalent to `α`.

**Source:**
```lean
protected def univ (α) : @univ α ≃ α :=
  ⟨Subtype.val, fun a => ⟨a, trivial⟩, fun ⟨_, _⟩ => rfl, fun _ => rfl⟩
```

**Richness:** 9 — same lambda-arm-as-conditional blind spot as ranks 4 and 5's equivalence proofs; the definition (a very short, essentially content-free equivalence) doesn't intuitively feel like a top-10 candidate by inspection. Flagged in the digest.

### 7. Equiv.sumCongr
*Logic/Equiv/Sum.lean*

**Docstring:**
> If `α ≃ α'` and `β ≃ β'`, then `α ⊕ β ≃ α' ⊕ β'`. This is `Sum.map` as an equivalence.

**Source:**
```lean
def sumCongr {α₁ α₂ β₁ β₂} (ea : α₁ ≃ α₂) (eb : β₁ ≃ β₂) : α₁ ⊕ β₁ ≃ α₂ ⊕ β₂ :=
  ⟨Sum.map ea eb, Sum.map ea.symm eb.symm, fun x => by simp, fun x => by simp⟩
```

**Richness:** 6 — same equivalence-constructor lambda-arm pattern as above.

### 8. Equiv.swap
*Logic/Equiv/Basic.lean*

**Docstring:**
> `swap a b` is the permutation that swaps `a` and `b` and leaves other values as is.

**Source:**
```lean
def swap (a b : α) : Perm α :=
  ⟨swapCore a b, swapCore a b, fun r => swapCore_swapCore r a b,
    fun r => swapCore_swapCore r a b⟩
```

**Richness:** 6 — again mostly the lambda-arm pattern. **Notes:** Genuinely a well-known, well-used permutation constructor (batch 1 also ranked it reasonably, rank 30 there); the richness score here is more accident than signal, per the blind-spot pattern documented above.

### 9. Function.prod
*Logic/Function/Defs.lean*

**Docstring:**
> Product of functions: `Function.prod f g i = (f i, g i)`, where the types of `f i` and `g i` may depend on `i`.

**Source:**
```lean
protected def prod {ι} {α β : ι → Type*} (f : ∀ i, α i) (g : ∀ i, β i) (i : ι) :
    α i × β i := (f i, g i)
```

**Richness:** 4 — 2 quantifiers, 2 hypothesis binders, all genuinely from the dependent-function signature, not lambda-arm noise. **Notes:** A clean, correctly-identified example of real (if modest) structural content: a dependent-type-indexed pairing.

### 10. Xor
*Logic/Basic.lean*

**Docstring:**
> `Xor a b` is the exclusive-or of propositions.

**Source:**
```lean
def Xor (a b : Prop) := (a ∧ ¬b) ∨ (b ∧ ¬a)
```

**Richness:** 4 — 2 conjunctions, 1 disjunction, 1 hypothesis binder. **Notes:** Self-contained propositional formula, genuinely rich for its length — the cleanest example this batch of richness doing exactly its intended job on a short definition (contrast with the equivalence-constructor cases above, where similar or higher richness scores came from lambda-arm noise, not genuine content).

## 4. Edge lists

### (a) The 10 lowest-ranked included

| Rank | Name | Module | Tiers (CW/Mem/Glob) | Score |
|---|---|---|---|---|
| 43 | symmDiff | Order/SymmDiff.lean | none/none/rich | 9.35 |
| 44 | Nat.primeFactors | Data/Nat/PrimeFin.lean | rich/thin/none | 8.87 |
| 45 | Equiv.trans | Logic/Equiv/Defs.lean | none/none/thin | 8.33 |
| 46 | Equiv.image | Logic/Equiv/Set.lean | none/thin/none | 8.11 |
| 47 | Equiv.symm | Logic/Equiv/Defs.lean | none/none/rich | 6.89 |
| 48 | PartialEquiv.symm | Logic/Equiv/PartialEquiv.lean | none/none/thin | 6.67 |
| 49 | Equiv.ulift | Logic/Equiv/Defs.lean | none/none/thin | 5.97 |
| 50 | Set.sInter | Order/SetNotation.lean | none/thin/none | 5.80 |
| 51 | Int.castRingHom | Data/Int/Cast/Lemmas.lean | none/none/thin | 5.61 |
| 52 | Set.sUnion | Order/SetNotation.lean | none/thin/none | 3.77 |

### (b) Highest-ranked excluded (verified but outranked) -- empty this round

**This edge list is empty.** With only 52 gate-eligible candidates against `top_n = 100`, nothing was ranked-and-cut; every gate survivor is included. There is no "just missed the cutoff" tier to show this batch — a direct consequence of Finding A/B above, not a separate issue.

### (c) Highest-scoring gate-excluded candidates -- what a bigger eligible pool would likely recover first

In place of edge list (b), the more informative view this round: gate-excluded candidates that would have scored highest had they passed every gate, ranked by their (fully computed, just not gate-cleared) preference score. All three below are excluded *only* by `dependency_vocabulary`, and all three are exactly the kind of case Finding B describes.

| Name | Module | Gates failed | Would-be score | Notes |
|---|---|---|---|---|
| Pairwise | Logic/Pairwise.lean | dependency_vocabulary | 44.17 | Bound-variable collision (`i`, `j`) -- see Finding B |
| Set.Pairwise | Logic/Pairwise.lean | dependency_vocabulary | 37.26 | Same collision pattern (`x`, `y`) |
| Nat.Prime | Data/Nat/Prime/Defs.lean | length_band | — | Correctly excluded: `Prime p := Irreducible p` is a genuine one-line delegation, the exact case design §3b names |

`Nat.Prime`'s exclusion is included here for contrast: unlike the `Pairwise` pair, it is *not* evidence of a gate bug — it's the gate working exactly as designed and previously validated in this task's own unit tests (`tests/test_miner_gates.py::test_length_band_gate_fails_nat_prime_style_delegation`).

## 5. Known limitations carried into this batch (not fixed here, per this task's scope)

1. **`MENTION_FLOOR = 30` is too aggressive for the widened corpus** (Finding A). Revisit either the threshold or its scope (`mention_count` vs. some corpus-relative measure) before the next mining round.
2. **`dependency_vocabulary` has a quantified false-failure mechanism** via short bare-identifier collisions between `referenced_constants` noise and `miner.depindex`'s bare-name index entries (Finding B, ~230 candidates recoverable by a targeted fix).
3. **Richness's `"=>"`-counts-as-conditional heuristic over-counts `where`-block field assignments and lambda-arm equivalence proofs** as if they were case-based branching on the definition's own input (ranks 2, 4, 6, 7, 8 above) — `miner.richness`'s own module docstring already names textual blind spots in the abstract; this batch is the first concrete evidence of which one actually bites in practice, and how often (5 of the top 10).
4. **No `Combinatorics/` candidate survived to the eligible set** — the corpus-widening's coverage of that area was effectively zero-yield this round, entirely attributable to findings 1 and 2 above, not to a lack of good candidates in that territory.
