# Harvest Batch 3 Review

Human-readable review of the third mechanical harvest (`miner/output/harvest_manifest.jsonl`), generated read-only from that file. This batch implements "Selection round 2" — the 22 July 2026 recalibration recorded in `docs/design/definition_selection_2026-07-21.md`'s revision section, following up on `docs/harvest_review_batch2.md`'s Findings A–B and §5. Same corpus as batch 2 (964 scanned hits, 5 original corners + the 69-file widened selection) — nothing changed in `TARGET_MODULES` this round; everything below is a selection-mechanism change, not a corpus change.

**Manifest shape change:** there is no top-N cutoff anymore. Every verified candidate is either `eligible` (passed all seven gates, ranked by preference score, in full) or excluded (with the specific gate(s) that fired). "Outranked" no longer exists as a category.

## 0. Headline

**120 candidates are eligible** — more than double batch 2's 52, using the *same* underlying corpus, purely from the four selection-mechanism fixes below. This is direct, measured confirmation that batch 2's small eligible set was a measurement artifact of first-pass threshold choices, not a reflection of the widened corpus lacking good candidates, exactly as batch 2's own review predicted.

| | Batch 2 | Batch 3 |
|---|---|---|
| Scanned | 964 | 964 |
| Verified | 950 | 950 |
| Eligible | 52 | **120** |
| Cutoff mechanism | top_n=100 (never engaged) | none |

## 1. Corpus counts

- Scanned: 964
- Verified (elaborates): 950
- Eligible (passed every gate): 120
- Excluded: 844
  - failed one or more gates: 830
  - curation-excluded (of the gate-eligible pool): 1 (`Nat.digitsAux1` — independently gate-excluded too, see `miner/curation.yaml`)
  - does not elaborate: 14

## 2. Changelog vs. batch 2

Four selection-mechanism changes this round (design doc's 22 July 2026 revision, items (a)–(e)): the raw mention floor retired in favor of a full-corpus theorem-mention floor (`THEOREM_MENTION_FLOOR=2`); the `dependency_vocabulary` bound-variable collision fixed (batch 2's Finding B); the vocabulary list widened (`Data/Sym`, `Algebra/Polynomial`, `Algebra/BigOperators`, `Algebra/GroupWithZero`, `Algebra/Field`); richness's `=>`-counting bug fixed (batch 2's §5 item 3); and a new richness-floor gate (`richness_total >= 1`) added now that richness itself is trustworthy.

### `Pairwise` and `Set.Pairwise`: the vocabulary-gate fix, confirmed directly

Both were batch 2's clearest Finding-B casualties (excluded because their own bound variables `i`/`j` and `x`/`y` collided with unrelated real declarations sharing those short bare names). Both are eligible now:

| | Batch 2 | Batch 3 |
|---|---|---|
| `Pairwise` | excluded (`dependency_vocabulary`) | **eligible, rank 59** |
| `Set.Pairwise` | excluded (`dependency_vocabulary`) | **eligible, rank 34** |

Post-fix `dependency_vocabulary` failure count: **195** (of 950 verified, 20.5%), against batch 2's 430 — a drop of 235, close to (and exceeding) the ~230 batch 2's own review estimated would be recoverable by this exact fix. See §4 for the full post-fix exclusion list, which no longer contains either `Pairwise` name.

### `Nat.Prime`: still correctly excluded, now for two independent reasons

`Nat.Prime := Irreducible p` remains excluded — `length_band` (unaffected by this round's fixes) and, newly, `richness_floor` (its richness is genuinely 0: a bare rename has no conjunctions, conditionals, quantifiers, comparisons, or hypothesis binders). Two independent gates agreeing is the gates-and-bands design working as intended: no single fix accidentally let a one-line delegation back in.

### The five lambda-arm-inflated `Equiv.*` entries (batch 2 §5 item 3): fate after the richness fix

| Name | Batch 2 rank | Batch 2 richness | Batch 3 status | Batch 3 richness |
|---|---|---|---|---|
| `finSumFinEquiv` | 2 | 13 | **eligible, rank 52** | 4 (genuine: `rcases`/`refine` case splits survive the fix) |
| `Equiv.prodAssoc` | 4 | 12 | excluded (`richness_floor`) | 0 |
| `Equiv.Set.univ` | 6 | 9 | excluded (`theorem_mention_floor`, `richness_floor`) | 0 |
| `Equiv.sumCongr` | 7 | 6 | excluded (`richness_floor`) | 0 |
| `Equiv.swap` | 8 | 6 | excluded (`richness_floor`) | 0 |

Four of the five drop to exactly zero richness and get caught by the new richness floor — direct confirmation that their batch-2 richness was pure lambda-arm noise, not genuine structure. `finSumFinEquiv` alone retains real richness (4: `rcases x with y | y` and `refine ... <;> simp`-style genuine case splits are actual pattern matches, not lambda arms) and stays eligible, correctly demoted from rank 2 to rank 52 now that its score reflects real content rather than inflated noise.

### Where batch 2's top 10 landed

| Rank (batch 2) | Name | Batch 3 status |
|---|---|---|
| 1 | `Nat.clog` | eligible, **rank 2** (richness 14→10; still top-tier, unaffected in substance — its richness was genuine match arms + real comparisons, only the double-counted bare `=` from its own `=>` tokens dropped out) |
| 2 | `finSumFinEquiv` | eligible, rank 52 (see above) |
| 3 | `Nat.log` | eligible, **rank 4** (richness 12→8, same story as `Nat.clog`) |
| 4 | `Equiv.prodAssoc` | excluded (`richness_floor`) |
| 5 | `Finset.pi` | **excluded** (`theorem_mention_floor`) — a new casualty of item (a)'s recalibration, not a bug: its full-corpus theorem-mention count is below 2. Worth a second look (§6) since it's a substantively interesting dependent-Pi definition; the mechanism working as designed doesn't mean every individual outcome is obviously correct, which is exactly why `THEOREM_MENTION_FLOOR` stays a named, re-tunable dial. |
| 6 | `Equiv.Set.univ` | excluded (`theorem_mention_floor`, `richness_floor`) |
| 7 | `Equiv.sumCongr` | excluded (`richness_floor`) |
| 8 | `Equiv.swap` | excluded (`richness_floor`) |
| 9 | `Function.prod` | eligible, rank 47 (richness unaffected: 4, genuine quantifier/hypothesis-binder content, no lambda-arm noise to begin with) |
| 10 | `Xor` | eligible, rank 51 (richness unaffected: 4, self-contained propositional formula) |

Net: 5 of batch 2's top 10 remain eligible (`Nat.clog`, `finSumFinEquiv`, `Nat.log`, `Function.prod`, `Xor`); the other 5 are gone, and every departure is individually explained above by a specific, named mechanism, not an unexplained reshuffle.

## 3. Gate-attrition table (sequential, established format)

Start: 950 verified candidates.

| Gate | Fails (of those reaching it) | Cumulative survivors |
|---|---|---|
| (a) theorem_mention_floor | 714 | 236 |
| (b) length_band | 8 | 228 |
| (c) docstring_floor | 7 | 221 |
| (d) dependency_vocabulary | 33 | 188 |
| (e) anti_plumbing | 0 | 188 |
| (g) richness_floor | 68 | 120 |
| (f) fact_supply | 0 | 120 |
| **eligible (pre-curation)** | | **120** |
| curation-excluded | 1 | **119 net eligible after curation** |

### Per-gate fail rate (independent, not sequential)

| Gate | Fails (of all 950 verified) | % |
|---|---|---|
| theorem_mention_floor | 714 | 75.2% |
| length_band | 48 | 5.1% |
| docstring_floor | 15 | 1.6% |
| dependency_vocabulary | 195 | 20.5% |
| anti_plumbing | 17 | 1.8% |
| richness_floor | 341 | 35.9% |
| fact_supply | 341 | 35.9% |

`theorem_mention_floor`'s 75.2% independent fail rate is still the single most aggressive gate — expected and not itself a problem (see §5's sensitivity table): a floor of 2 is deliberately low, but the *majority* of definitions freshly scanned from this widened, less-central corpus genuinely have fewer than 2 full-corpus theorem-statement mentions, which is a real fact about the corpus, not a miscalibration the way batch 2's raw-mention floor was. (`fact_supply`'s 35.9% is identical to `richness_floor`'s because, on this data, every candidate failing `fact_supply` also happens to fail `richness_floor` — a richness-zero definition is almost definitionally supply-thin too, per `miner.proxies`' own tier logic.)

## 4. Vocabulary-gate exclusions (post-fix, post-widening) — for continued list growth

195 candidates still fail `dependency_vocabulary` after this round's fix and vocabulary widening. Representative sample (full detail — every excluded name plus its referenced constants — is in the manifest; this table groups the recurring *kinds* of exotic dependency observed, for whoever tunes `COMMON_VOCABULARY_MODULES` next):

| Exotic dependency area observed | Example candidates | Suggests adding |
|---|---|---|
| `Encodable`/`Denumerable` machinery | `Encodable.chooseX`, `Encodable.decodeSigma`, `Denumerable.lower`, `Nat.Subtype.ofNat` | `Logic/Encodable`, `Logic/Denumerable.lean` |
| `Order.Bounds`/lattice-order primitives (`upperBounds`, `IsLUB`, `IsLeast`) | `IsLUB`, `IsLeast`, `BddAbove`, `IsCofinal` | Already under `Order` prefix in principle, but these resolve to `Order/Bounds/Defs.lean` and `Order/Defs/Unbundled.lean` specifically -- confirms the existing broad `"Order"` vocabulary entry is working; these are flagged because their *other* references (`LE`, `Nonempty`) are core-Lean, not Mathlib-indexed, and don't independently block them -- listed here as a sanity check, not a gap |
| Bundled-equivalence composition helpers (`Equiv.sigmaCongrRight`, `Equiv.piCongrRight`, `Trans.trans`) | Most of the `Equiv.*`/`derangements.*` entries in this list | These are genuinely `Logic/Equiv` names already in scope; they appear here because a *sibling* reference in the same definition (often an unrelated `Denumerable`/`Encodable`/`Fintype` helper) is what actually fails -- the gate correctly reports the whole candidate as blocked even when only one reference is exotic |
| `Fintype`/cardinality machinery | `Fintype.orderIsoFinOfCardEq`, `Encodable.fintypeArrow`, `Finset.dens` | `Data/Fintype` |
| `List` recursion/well-founded-recursion internals (`invImage`, `sizeOfWFRel`, `_f` fresh names from auto-generated equation compiler helpers) | `List.bidirectionalRec`, `List.twoStepInduction`, `Cycle.decidableNontrivialCoe` | Not a vocabulary gap -- these are compiler-generated auxiliary names (`_f`, `x_1`, `invImage`) that `referenced_constants` picks up as noise from equation-compiler-generated recursors; a future round could extend the anti-plumbing-style filtering to this shape rather than widening vocabulary for it |
| `Combinatorics/*` internals (`DyckWord`, `Composition`) | `DyckWord.IsNested`, `Composition.recOnAppendSingle` | These reference each other within the already-scanned Combinatorics files, but resolve to modules not on the vocabulary list; `Combinatorics/Enumerative`, `Combinatorics/Derangements` as vocabulary entries would recover several of these |

This list is expected to keep shaping `COMMON_VOCABULARY_MODULES` empirically, per the design doc's revision item (d) — no widening was done in this pass beyond what phase 2 specified.

## 5. Sensitivity table: `THEOREM_MENTION_FLOOR`

Eligible-set size (pre-curation) at each candidate floor value, all six other gates held fixed at their actual configured values:

| THEOREM_MENTION_FLOOR | Eligible-set size |
|---|---|
| 1 | 147 |
| **2 (current)** | **120** |
| 3 | 100 |
| 5 | 76 |

Smoothly monotonic, no cliff — a good sign that 2 isn't sitting on a knife-edge. Moving to 3 would still leave a comfortably large eligible set (100) if global-fact supply at floor 2 turns out too thin in practice; moving to 1 buys 27 more candidates at the cost of a weaker supply guarantee. This table is provided as evidence for that future call, not a recommendation to change it now (out of this task's scope).

## 6. Richness-zero exclusions: population characterization

68 candidates are gate-excluded *purely* by `richness_floor` (no other gate fired) — i.e., candidates that would otherwise be eligible, screened out only because they scored zero on the post-fix richness measure. (341 richness-zero candidates exist in total among gate-excluded records, but most of those also fail other gates independently; the 68 below are the ones where richness alone is doing the work, the cleanest test of what this new gate actually catches.)

**Nature of the population**, by inspection of all 68:

- **~27 (40%): one-line delegations, projections, or renames** to another named Mathlib definition — `Finset.card := Multiset.card s.1`, `List.toFinset := Multiset.toFinset l`, `Set.sInter S := sInf S`, `finSuccEquiv n := finSuccEquiv' 0`, `List.SortedLE l := Monotone l.get`. This is exactly the target population the length band was supposed to catch and didn't (batch 2's 44% richness-zero rate at a *larger* length band was the original motivation for this gate) — confirmed working as intended.
- **~27 (40%): bundled-equivalence/hom "scaffolding" with no case-based content of its own** — anonymous-constructor equivalence proofs (`Equiv.symm`, `Equiv.trans`, `Equiv.prodComm`) and `where`-block structure literals (`AddMonoidHom.mulLeft`, `Int.castRingHom`, `PartialEquiv.ofSet`) whose only content is field assignment, not conditionals/quantifiers/comparisons. This is the *other* half of the same delegation problem richness targets, in bundled-morphism clothing rather than plain-function clothing.
- **~7 (10%): subtype-literal projections** — `Finset.erase`, `Finset.range`, `Finset.powerset`, all of the shape `⟨_, proof_obligation⟩` where the "proof obligation" is itself a delegation to a named lemma (`nodup_range n`), not visible case structure.
- **3 (4%): type-formers** — `ArithmeticFunction`, `Shrink`, `ULower` all return `Type`/`Type w`, not a value or `Prop`; classified `bundled` by `miner.shape`, and genuinely have no case-based content as *type aliases*, whatever richness their *use* might have elsewhere.
- **A small remainder (`Nat.bit`, `bihimp`, `symmDiff`): genuine confirmed instances of richness's documented "boolean/notation-hidden" blind spot** — `Nat.bit`'s `cond b (2*n+1) (2*n)` is a real two-way branch that isn't textually `if`/`bif`; `bihimp`/`symmDiff`'s Heyting-algebra notation (`(b ⇨ a) ⊓ (a ⇨ b)`, `a \ b ⊔ b \ a`) encodes real mathematical content that the operator list doesn't recognize. These are correctly predicted by richness's own module docstring, now empirically confirmed rather than hypothetical — worth revisiting if this pattern recurs at scale in a future batch, but a small minority (3 of 68) this round, not the dominant story.

Full name/module list (see the manifest for each entry's docstring and source):

`AddMonoidHom.mulLeft`, `AddMonoidHom.mulRight`, `ArithmeticFunction`, `Composition.toCompositionAsSet`, `CompositionAsSet.toComposition`, `Equiv.Set.sumCompl`, `Equiv.Set.union`, `Equiv.arrowCongr`, `Equiv.curry`, `Equiv.funUnique`, `Equiv.image`, `Equiv.ofUnique`, `Equiv.permCongr`, `Equiv.prodAssoc`, `Equiv.prodComm`, `Equiv.prodCongr`, `Equiv.prodProdProdComm`, `Equiv.sumCongr`, `Equiv.swap`, `Equiv.symm`, `Equiv.toEmbedding`, `Equiv.trans`, `Equiv.ulift`, `Finset.card`, `Finset.disjUnion`, `Finset.erase`, `Finset.map`, `Finset.max`, `Finset.min`, `Finset.powerset`, `Finset.range`, `Finset.sym2`, `Function.Embedding.refl`, `Function.Embedding.toEquivRange`, `Int.castAddHom`, `Int.castRingHom`, `Int.ofNatHom`, `List.SortedLE`, `List.SortedLT`, `List.rdrop`, `List.toAList`, `List.toFinset`, `Multiset.toFinset`, `Nat.Primes`, `Nat.bit`, `Nat.castRingHom`, `Nat.centralBinom`, `Nat.fib`, `Nat.primeFactors`, `Nat.size`, `PartialEquiv.ofSet`, `PartialEquiv.prod`, `PartialEquiv.restr`, `PartialEquiv.symm`, `PartialEquiv.trans`, `Set.sInter`, `Set.sUnion`, `Shrink`, `ULower`, `ULower.down`, `bihimp`, `finSuccEquiv`, `finSuccEquivLast`, `finTwoArrowEquiv`, `notMemRangeEquiv`, `symmDiff`, `uniqueElim`, `zpowersMulHom`.

One incidental finding while categorizing: `Finset.disjUnion (h : Disjoint s t)` has a genuine hypothesis binder that `looks_like_prop_type`'s marker list doesn't catch (`"Disjoint s t"` contains none of `∈∀∃∧∨¬≤≥<>≠∣=↔→Prop`) — a real, small gap in the hypothesis-binder heuristic, distinct from the `=>`/`:=` bug fixed this round. Noted, not fixed, per this task's scope.

## 7. Return-shape composition

Overall eligible set (120):

| Shape | Count |
|---|---|
| value | 52 |
| prop | 43 |
| bundled | 25 |

Top 50 by rank (of 120 eligible):

| Shape | Count |
|---|---|
| value | 15 |
| prop | 25 |
| bundled | 10 |

`prop` is over-represented at the top of the ranking relative to its overall share (25/50 = 50% in the top 50, vs. 43/120 = 36% overall) — consistent with richness being dominated by logical-connective/quantifier/comparison counts, which `Prop`-valued predicates (`Monotone`, `StrictMono`, `DependsOn`, the `Order/Monotone/Defs.lean` family) tend to accumulate more of per unit of source length than plain value-returning functions do. `bundled` (mostly `Equiv`/`Embedding`/hom types) is proportionally similar top vs. overall (20% vs. 21%) — the richness fix specifically targeted *spurious* bundled-equivalence richness, so a bundled definition making the top 50 now is more likely to be there on genuine structural grounds (`Equiv.piEquivPiSubtypeProd`, `Equiv.sumPiEquivProdPi` — both genuinely dependent-type-indexed equivalences with real quantifier/comparison content in their signatures) rather than proof-scaffolding noise.

## 8. Detail cards: top 10

### 1. Nat.leRec
*Data/Nat/Init.lean*

**Docstring:** Recursion starting at a non-zero number: given a map `C k → C (k+1)` for each `k ≥ n`, this gives a map `C n → C m` for every `m ≥ n`.

**Signature:** `{n : ℕ} {motive : (m : ℕ) → n ≤ m → Sort u_1} (refl : motive n ⋯) (le_succ_of_le : ⦃k : ℕ⦄ → (h : n ≤ k) → motive k h → motive (k + 1) ⋯) {m : ℕ} (h : n ≤ m) : motive m h`

**Richness:** 12, return-shape `value`. **Notes:** A genuinely rich dependent-recursion principle -- the `motive`/`refl`/`le_succ_of_le` shape is real induction machinery, not proof scaffolding. New to the eligible set this round (excluded from both prior batches' rankings, since it never previously reached this rank under either scoring scheme) -- rank 1 is earned on real quantifier/comparison content in a dependently-typed induction principle, not an artifact.

### 2. Nat.clog
*Data/Nat/Log.lean* -- unchanged from batch 2's rank-1 detail card in substance (see `docs/harvest_review_batch2.md` §3); richness dropped 14→10 from the `=>`-double-counting fix, still clearly the richest concrete arithmetic function in the corpus.

### 3. Relation.Map
*Logic/Relation.lean*

**Docstring:** The map of a relation `r` through a pair of functions pushes the relation to the codomains of the functions.

**Signature:** `{α} {β} {γ} {δ} (r : α → β → Prop) (f : α → γ) (g : β → δ) : γ → δ → Prop`

**Richness:** 8, return-shape `prop`. **Notes:** Genuine quantifier/hypothesis-binder richness from a real relation-transport construction; not previously eligible in either batch 1 or 2.

### 4. Nat.log
See batch 2's rank-3 card; richness 12→8 from the same fix as `Nat.clog`, same dual-log pairing.

### 5. Equiv.piEquivPiSubtypeProd
*Logic/Equiv/Prod.lean*

**Docstring:** The type `∀ (i : α), β i` can be split as a product by separating the indices in `α` depending on whether they satisfy a predicate `p` or not.

**Richness:** 8, return-shape `bundled`. **Notes:** A genuinely dependent-type-indexed equivalence (splitting a Pi-type by a decidable predicate) -- exactly the kind of `bundled`-shape candidate §7 notes making the top 50 on real content post-fix, not lambda-arm noise.

*(Ranks 6-10 -- `Int.leInduction`, `Int.leInductionDown`, `Function.extend`, `Equiv.sumCompl`, `Equiv.sumPiEquivProdPi` -- are all similarly genuine dependent-recursion or dependent-equivalence constructions; see the full ranked table in the manifest for their signatures and docstrings.)*
