# Harvest Batch 4 Digest — "Wide Mine"

Skimmable companion to `docs/harvest_review_batch4.md` (the full mechanical review: per-territory yield, gate attrition, vocabulary-exclusion breakdown, richness/supply composition, scan-parser vigilance findings, the tier-2 discharge measurement, and the changelog confirming zero regressions vs. batch 3). Same format as `docs/harvest_digest_batch3.md`.

**This batch is a corpus expansion for measurement, not a selection change.** `TARGET_MODULES` grew roughly 3.3x (964 → 3,185 scanned candidates: full `Order/`, full `Combinatorics/`, broad `Algebra/` basics, deeper `NumberTheory/`, `Topology/` core, `Analysis/SpecialFunctions/` basics, full `Dynamics/`, `Data/Set/` core, and several small `Data/` completions) — every gate, threshold, and the preference score itself are byte-for-byte unchanged from batch 3. **Eligible set: 256 → 727**, with all 256 batch-3 candidates confirmed still eligible (see the review doc §9) — the entire gain is new territory, not re-scoring.

## Shape of the batch

The widened territories land very unevenly. `Order` (full subtree, 957 scanned) and `Combinatorics` (full subtree, 605 scanned) are the two biggest contributors by volume (199 and 139 newly-eligible-territory candidates respectively), but neither is where the *richest* new content concentrates — that distinction still goes to a handful of individual definitions (`WithTop.subtypeOrderIso`, richness 11, is the single richest genuinely-new-territory find). `Topology core`, by contrast, is nearly a bust for this design's purposes: 101 scanned, only 2 eligible, killed almost entirely by `dependency_vocabulary` — Topology infrastructure leans on other Topology/order/filter machinery that wasn't on the common-vocabulary list before this batch (see the review doc §4's missing-module-kind table; `Data/Fintype` and `Topology/Defs` are now the clearest candidates for that list's next widening, a decision deliberately left unmade here since the selection machinery is frozen this round).

Structurally, the new territory skews away from casework: `Order` produces **zero** casework-rich eligible candidates (Order-theoretic definitions are overwhelmingly `Prop`-valued relations over arbitrary, non-enumerable preorders — casework in the reward-structure sense doesn't apply), and the same holds nearly as starkly for `Data/Set` and `Combinatorics`. Global-fact supply is rich almost everywhere in the new territory instead — theorem-mention-backed global facts, not casework or membership, are what this batch's expansion mostly adds.

Two scan-parser findings came out of this batch's own vigilance work (both detailed in the review doc §7): a genuine new bug where Lean's `_root_.` namespace-escape prefix produces a wrong, doubly-qualified name (7 candidates corpus-wide, 6 of 7 concentrated in the new territory — flagged prominently, not fixed, per this task's stop points); and a pre-existing, NOT new-territory-specific scanner blind spot around `/-!` module-doc blocks containing illustrative code examples (3 files, all in corners scanned since batch 1, confirmed harmless — the real declarations they collide with remain eligible and unaffected).

Best formalization targets this batch:

- **`WithTop.subtypeOrderIso`** — the richest new-territory find (Order); a genuine order-isomorphism construction, not a trivial relabeling.
- **`Int.leInduction`/`Int.leInductionDown`** — already visible as siblings to batch 3's induction-principle cluster (`Nat.leRec`, `Nat.decreasingInduction`), now both independently eligible.
- **`SimpleGraph.Walk.mapToSubgraph`/`SimpleGraph.replaceVertex`** — genuine graph-combinatorics content, richness 9 and 8 respectively, from the newly-full `Combinatorics/SimpleGraph/` subtree.
- **`Finset.sumLift₂`/`Finset.sumLexLift`** — real Sum-type lifting combinators from the `Data/Sum` completion, richness 7–8, good side-condition density.
- **`Pi.Lex`** — the lexicographic order on dependent products, from `Order/PiLex.lean`; richness 8, `Prop`-shaped, a strong candidate for testing whether a definition-writer handles a genuinely order-theoretic construction correctly.

## Top 25 (rank order)

1. **Int.greatestOfBdd** — a computable version of "there's a greatest value satisfying a bounded, decidable predicate": given an upper bound and a witness the predicate holds somewhere, returns the greatest satisfying value. [docstring]
   Data/Int/LeastGreatest.lean · richness 13 · value · unchanged from batch 3 (rank 1 there too)
2. **Nat.leRec** — recursion up from a base point `n`: given a base case and a step from any `k ≥ n` to `k+1`, produces a value at every `m ≥ n`. [docstring]
   Data/Nat/Init.lean · richness 12 · value · unchanged from batch 3 (rank 2 there)
3. **Nat.binaryRec** — a recursion principle for binary (`bit`) representations of naturals. [docstring]
   Data/Nat/BinaryRec.lean · richness 11 · value · unchanged from batch 3 (rank 3 there)
4. **WithTop.subtypeOrderIso** — any `OrderBot` is order-isomorphic to `WithBot` of the subtype excluding the bottom element. [docstring]
   Order/Hom/WithTopBot.lean · richness 11 · bundled · **new this batch** (Order, full-subtree expansion)
5. **Nat.clog** — the ceiling (round-up) base-`b` logarithm of `n`. [docstring]
   Data/Nat/Log.lean · richness 10 · value · unchanged from batch 3 (rank 4 there)
6. **Int.leastOfBdd** — the least-value dual of rank 1. [docstring]
   Data/Int/LeastGreatest.lean · richness 10 · value · unchanged from batch 3 (rank 5 there)
7. **List.prev** — given a proof `x ∈ l`, returns the element immediately before `x`'s first occurrence in `l`. [docstring]
   Data/List/Cycle.lean · richness 9 · value · unchanged from batch 3 (rank 6 there)
8. **Finset.strongDownwardInduction** — an induction principle building a value on a finset from values on all larger-or-equal-cardinality supersets, working downward. [docstring]
   Data/Finset/Card.lean · richness 9 · value · unchanged from batch 3 (rank 7 there)
9. **Equiv.sigmaSigmaSubtypeEq** — a specialization of a nested-sigma equivalence to the case of plain equality constraints (useful for categorical `Hom`-like types). [docstring]
   Logic/Equiv/Basic.lean · richness 9 · bundled · unchanged from batch 3 (rank 8 there)
10. **List.recNeNil** — a dependent recursion principle for nonempty lists, avoiding the need to handle an impossible empty case. [docstring]
    Data/List/Induction.lean · richness 9 · value · unchanged from batch 3 (rank 9 there)
11. **SimpleGraph.Walk.mapToSubgraph** — maps a walk to its own subgraph. [docstring]
    Combinatorics/SimpleGraph/Connectivity/Subgraph.lean · richness 9 · value · **new this batch** (Combinatorics, full-subtree expansion)
12. **Nat.decreasingInduction** — induction downward: if `P(k+1)` implies `P(k)` for all `k < n`, then `P(n)` implies `P(m)` for every `m ≤ n`. [docstring]
    Data/Nat/Init.lean · richness 8 · value · unchanged from batch 3 (rank 10 there)
13. **Finset.sumLexLift** — lifts maps between sum types into a map on `Finset` of the sum, generalizing pointwise lifting to the lexicographic case. [docstring]
    Data/Sum/Interval.lean · richness 8 · value · **new this batch** (Data/Sum completion)
14. **Relation.Map** — pushes a relation on `α × β` to a relation on `γ × δ` through a pair of functions `f`, `g`. [docstring]
    Logic/Relation.lean · richness 8 · prop · unchanged from batch 3 (rank 11 there)
15. **Nat.log** — the floor (round-down) base-`b` logarithm of `n`. [docstring]
    Data/Nat/Log.lean · richness 8 · value · unchanged from batch 3 (rank 12 there)
16. **OrderHom.prevFixed** — the greatest fixed point of a monotone self-map of a complete lattice that is ≤ a given point. [docstring]
    Order/FixedPoints.lean · richness 8 · value · **new this batch** (Order, full-subtree expansion)
17. **Pi.Lex** — the lexicographic order relation on dependent functions `Π i, β i`, ordering by the first index (under `r`) where two functions differ (under `s`). [docstring]
    Order/PiLex.lean · richness 8 · prop · **new this batch** (Order, full-subtree expansion)
18. **Function.Embedding.setValue** — changes an embedding's value at one point, swapping with whatever point previously mapped there if occupied. [docstring]
    Logic/Embedding/Basic.lean · richness 8 · bundled · unchanged from batch 3 (rank 13 there)
19. **SimpleGraph.replaceVertex** — the graph formed by forgetting one vertex's neighbours and instead giving it another's, removing the edge between them if present. [docstring]
    Combinatorics/SimpleGraph/Operations.lean · richness 8 · value · **new this batch** (Combinatorics, full-subtree expansion)
20. **Equiv.subtypePreimage** — functions agreeing with a fixed function `x₀` on a subtype are equivalent to functions on the complementary subtype. [docstring]
    Logic/Equiv/Basic.lean · richness 8 · bundled · unchanged from batch 3 (rank 14 there)
21. **Set.PartiallyWellOrderedOn.IsMinBadSeq** — a "minimal bad sequence" property used in well-quasi-ordering proofs: every bad sequence agreeing on the first `n` terms scores no better at term `n`. [docstring]
    Order/WellFoundedSet.lean · richness 8 · prop · **new this batch** (Order, full-subtree expansion)
22. **Equiv.piEquivPiSubtypeProd** — splits dependent functions on `α` into a product by separating indices satisfying a predicate from those that don't. [docstring]
    Logic/Equiv/Prod.lean · richness 8 · bundled · unchanged from batch 3 (rank 15 there)
23. **Equiv.ofLeftInverse** — if `f` has a left-inverse (when `α` is nonempty), `α` is computably equivalent to `f`'s range. [docstring]
    Logic/Equiv/Set.lean · richness 7 · bundled · unchanged from batch 3 (rank 16 there)
24. **Filter.Germ.IsConstant** — a germ of functions is constant with respect to its filter. [docstring]
    Order/Filter/Germ/Basic.lean · richness 8 · prop · **new this batch** (Order, full-subtree expansion)
25. **Graph.banana** — a graph with exactly two vertices and no loops (a standard small combinatorial building block/counterexample). [docstring]
    Combinatorics/Graph/Basic.lean · richness 8 · value · **new this batch** (Combinatorics, full-subtree expansion)

Complete ranked list of all 727 eligible candidates (and every excluded candidate with its failing gates) in `miner/output/harvest_manifest.jsonl`; the tier-2 discharge-measurement record for each is in `miner/output/discharge_manifest.jsonl` (see the review doc §8).
