# Harvest Batch 2 Digest

Skimmable companion to `docs/harvest_review_batch2.md` (the full mechanical review, tables, and gate-attrition analysis). This is the first digest produced under this format — no batch-1 digest exists to compare against; this document is the standing spec going forward.

## Shape of the batch

52 definitions made it through every gate this round (well below the requested top-100 — see the review doc's Finding A/B for why). By subject: equivalences and bijections dominate (14 of 52, mostly `Logic/Equiv/*`), finite-set operations are the other big cluster (14, `Data/Finset/*`), with a smaller but genuine spread of natural-number functions (9), a handful of order-theoretic set-operator definitions (`Order/SetNotation.lean`'s `iInter`/`sInter`/`sUnion`), and single representatives each from `Algebra/GroupWithZero` and `NumberTheory/ArithmeticFunction`. **No `Combinatorics/` definition survived** — worth noting, since widening into that territory was one of this round's explicit goals; see the review doc for why.

Roughly **23 of the 52 (44%) are trivially-easy one-liners or thin delegations** by the richness measure (zero counted structure) — `List.toFinset := Multiset.toFinset l`, `Equiv.symm`, `Finset.range`, and similar. That is *not* the "far fewer one-liners" outcome the gates were hoped to produce, and the reason is mechanical, not a failure of richness itself: the eligible pool (52) sits below `top_n` (100), so nothing gets ranked out — every gate survivor is included regardless of how low it scores. Richness is doing real, visible work at the *top* of the list (the ten definitions below with genuine boundary/conditional/quantifier content), it just isn't yet large enough a pool to also do its intended job of pushing the trivial tail out of the final set.

Best formalization targets this batch, each for a different reason:

- **`Nat.clog` / `Nat.log`** (ranks 1, 3) — genuine fuel-recursive floor/ceiling logarithms with real boundary conditions (`b ≤ 1`, `n < b`), the two most structurally rich definitions in the set and a strong pair for boundary-focused fact suites.
- **`Finset.pi`** (rank 5) — a genuinely dependent-typed construction (a finite set of dependently-typed functions), rare structural depth for something this short.
- **`Xor`** (rank 10) — the cleanest example of richness measuring real content rather than notation noise: two conjunctions, one disjunction, nothing hidden behind lambda-arm syntax.
- **`Function.prod`** (rank 9) — clean dependent-pairing content, no lambda-arm noise contaminating its richness score (contrast with several `Equiv.*` entries below).
- **`Nat.pair` / `Nat.unpair`** (ranks 18-19) — a genuine conditional pairing/unpairing function pair, natural mutant material (boundary at `n - s*s < s`).
- **`IsNilpotent`** (rank 12) — a clean existential definition (`∃ n, x ^ n = 0`) with an unusually candid docstring about its own scope limits, worth reading for dossier material alone.
- **`AntisymmRel`** (rank 14) — a compact, self-contained relational definition, good membership-fact material (accept/reject pairs over a concrete order).

## Full included list (rank order)

1. **Nat.clog** — the ceiling (round-up) base-`b` logarithm of `n`: the smallest `k` with `n ≤ b^k`. [docstring]
   Data/Nat/Log.lean · richness 14: 1 conj, 5 cond, 8 comp · CW=rich/Mem=none/Glob=thin
2. **finSumFinEquiv** — the bijection between a disjoint union of two finite ordinals and one ordinal of the summed size. [docstring]
   Logic/Equiv/Fin/Basic.lean · richness 13: 3 cond, 10 comp · CW=none/Mem=none/Glob=rich
3. **Nat.log** — the floor (round-down) base-`b` logarithm of `n`: the largest `k` with `b^k ≤ n`. [docstring]
   Data/Nat/Log.lean · richness 12: 5 cond, 7 comp · CW=rich/Mem=none/Glob=rich
4. **Equiv.prodAssoc** — the equivalence witnessing that Cartesian product of three types is associative. [docstring]
   Logic/Equiv/Prod.lean · richness 12: 4 cond, 8 comp · CW=none/Mem=none/Glob=thin
5. **Finset.pi** — the finite set of dependently-typed functions on a finset, taking values in a chosen finset per element. [docstring]
   Data/Finset/Pi.lean · richness 9: 2 cond, 2 quant, 4 comp, 1 hyp · CW=none/Mem=thin/Glob=none
6. **Equiv.Set.univ** — the equivalence between a type's universal set and the type itself. [docstring]
   Logic/Equiv/Set.lean · richness 9: 3 cond, 6 comp · CW=none/Mem=thin/Glob=none
7. **Equiv.sumCongr** — combines two equivalences into an equivalence between the corresponding disjoint unions. [docstring]
   Logic/Equiv/Sum.lean · richness 6: 2 cond, 4 comp · CW=none/Mem=none/Glob=thin
8. **Equiv.swap** — the permutation that exchanges two elements and fixes everything else. [docstring]
   Logic/Equiv/Basic.lean · richness 6: 2 cond, 4 comp · CW=none/Mem=none/Glob=rich
9. **Function.prod** — pairs two dependent functions into one function returning both outputs together. [docstring]
   Logic/Function/Defs.lean · richness 4: 2 quant, 2 hyp · CW=none/Mem=none/Glob=thin
10. **Xor** — exclusive or of two propositions: exactly one holds, not both. [docstring]
    Logic/Basic.lean · richness 4: 2 conj, 1 disj, 1 hyp · CW=none/Mem=thin/Glob=rich
11. **Function.Embedding.subtype** — the inclusion of a subtype into its ambient type, as an injective embedding. [docstring]
    Logic/Embedding/Basic.lean · richness 4: 1 cond, 2 comp, 1 hyp · CW=none/Mem=none/Glob=thin
12. **IsNilpotent** — a ring element is nilpotent if some natural-number power of it equals zero. [docstring]
    Algebra/GroupWithZero/Basic.lean · richness 2: 1 quant, 1 comp · CW=none/Mem=thin/Glob=rich
13. **Function.Bijective** — a function is bijective if it is both injective and surjective. [docstring]
    Logic/Function/Defs.lean · richness 2: 1 conj, 1 hyp · CW=none/Mem=thin/Glob=rich
14. **AntisymmRel** — two elements are antisymmetrization-related under `r` if each relates to the other. [docstring]
    Order/Antisymmetrization.lean · richness 2: 1 conj, 1 hyp · CW=none/Mem=thin/Glob=rich
15. **Finset.noncommProd** — the product, under a possibly-noncommutative operation, of a function's values over a finset, given a proof the operation commutes on all pairs used. [docstring]
    Data/Finset/NoncommProd.lean · richness 2: 1 comp, 1 hyp · CW=none/Mem=thin/Glob=none
16. **Nat.find** — the smallest natural number satisfying a decidable predicate, given a proof one exists. [docstring]
    Data/Nat/Find.lean · richness 1: 1 hyp · CW=none/Mem=none/Glob=rich
17. **Nat.minFac** — the smallest prime factor of a natural number. [docstring]
    Data/Nat/Prime/Defs.lean · richness 2: 1 cond, 1 comp · CW=rich/Mem=none/Glob=none
18. **Nat.unpair** — recovers the pair of naturals encoded by `Nat.pair`'s pairing function. [docstring]
    Data/Nat/Pairing.lean · richness 2: 1 cond, 1 comp · CW=rich/Mem=none/Glob=none
19. **Nat.pair** — a pairing function encoding two naturals as one. [docstring]
    Data/Nat/Pairing.lean · richness 2: 1 cond, 1 comp · CW=rich/Mem=none/Glob=none
20. **Equiv.cast** — the equivalence between two types known to be equal. [docstring]
    Logic/Equiv/Defs.lean · richness 2: 1 comp, 1 hyp · CW=none/Mem=none/Glob=thin
21. **Finset.filter** — the subset of a finset consisting of elements satisfying a predicate. [docstring]
    Data/Finset/Filter.lean · richness 1: 1 hyp · CW=none/Mem=thin/Glob=thin
22. **Finset.cons** — inserts an element into a finset, given a proof it isn't already present. [docstring]
    Data/Finset/Insert.lean · richness 1: 1 hyp · CW=none/Mem=thin/Glob=thin
23. **Function.Commute** — two self-maps commute if applying them in either order gives the same result. [docstring]
    Logic/Function/Conjugate.lean · richness 1: 1 hyp · CW=none/Mem=thin/Glob=thin
24. **Finset.sup'** — the supremum of a function's image over a nonempty finset, in a (possibly bottomless) semilattice. [docstring]
    Data/Finset/Lattice/Fold.lean · richness 1: 1 hyp · CW=none/Mem=thin/Glob=none
25. **Nat.ModEq** — two naturals are congruent modulo `n` if they leave the same remainder. [docstring]
    Data/Nat/ModEq.lean · richness 1: 1 comp · CW=rich/Mem=rich/Glob=none
26. **Int.ModEq** — two integers are congruent modulo `n` if they leave the same remainder. [docstring]
    Data/Int/ModEq.lean · richness 1: 1 comp · CW=rich/Mem=rich/Glob=none
27. **Finset.sup** — the supremum of a function's image over a finset. [docstring]
    Data/Finset/Lattice/Fold.lean · richness 1: 1 hyp · CW=none/Mem=thin/Glob=thin
28. **Finset.image** — the image of a finset under a function. [docstring]
    Data/Finset/Image.lean · richness 1: 1 hyp · CW=none/Mem=thin/Glob=rich
29. **Set.iInter** — the intersection of an indexed family of sets. [docstring]
    Order/SetNotation.lean · richness 1: 1 hyp · CW=none/Mem=thin/Glob=none
30. **Finset.min** — the minimum of a finset in a linear order, or `⊤` if empty. [docstring]
    Data/Finset/Max.lean · richness 0: none · CW=none/Mem=thin/Glob=thin
31. **Finset.map** — the image finset of an embedding applied to a finset, guaranteed duplicate-free. [docstring]
    Data/Finset/Image.lean · richness 0: none · CW=none/Mem=thin/Glob=thin
32. **Equiv.toEmbedding** — converts an equivalence into an injective embedding. [docstring]
    Logic/Embedding/Basic.lean · richness 0: none · CW=none/Mem=none/Glob=thin
33. **ArithmeticFunction** — a function from `ℕ` to a zero-object that sends `0` to `0`. [docstring]
    NumberTheory/ArithmeticFunction/Defs.lean · richness 0: none · CW=none/Mem=none/Glob=rich
34. **Finset.card** — the number of elements in a finset. [docstring]
    Data/Finset/Card.lean · richness 0: none · CW=none/Mem=thin/Glob=rich
35. **PartialEquiv.trans** — composes two partial equivalences, restricting to where the composition is defined. [docstring]
    Logic/Equiv/PartialEquiv.lean · richness 0: none · CW=none/Mem=none/Glob=thin
36. **finSuccEquiv** — the equivalence between `Fin (n+1)` and `Option (Fin n)`. [docstring]
    Logic/Equiv/Fin/Basic.lean · richness 0: none · CW=none/Mem=none/Glob=rich
37. **Nat.bit** — appends a bit to the low end of a natural number's binary representation. [docstring]
    Data/Nat/BinaryRec.lean · richness 0: none · CW=rich/Mem=none/Glob=thin
38. **Finset.erase** — a finset with one element removed. [docstring]
    Data/Finset/Erase.lean · richness 0: none · CW=none/Mem=thin/Glob=thin
39. **Finset.range** — the finset of natural numbers below a given bound. [docstring]
    Data/Finset/Range.lean · richness 0: none · CW=rich/Mem=thin/Glob=rich
40. **Multiset.toFinset** — removes duplicates from a multiset to produce a finset. [docstring]
    Data/Finset/Dedup.lean · richness 0: none · CW=none/Mem=thin/Glob=rich
41. **Equiv.prodComm** — the equivalence witnessing that Cartesian product is commutative. [docstring]
    Logic/Equiv/Prod.lean · richness 0: none · CW=none/Mem=none/Glob=thin
42. **List.toFinset** — removes duplicates from a list to produce a finset. [docstring]
    Data/Finset/Dedup.lean · richness 0: none · CW=none/Mem=thin/Glob=rich
43. **symmDiff** — the symmetric difference of two elements in a type with join and set-difference. [docstring]
    Order/SymmDiff.lean · richness 0: none · CW=none/Mem=none/Glob=rich
44. **Nat.primeFactors** — the finset of prime factors of a natural number. [docstring]
    Data/Nat/PrimeFin.lean · richness 0: none · CW=rich/Mem=thin/Glob=none
45. **Equiv.trans** — composes two equivalences into one. [docstring]
    Logic/Equiv/Defs.lean · richness 0: none · CW=none/Mem=none/Glob=thin
46. **Equiv.image** — a set is equivalent to its image under an equivalence. [docstring]
    Logic/Equiv/Set.lean · richness 0: none · CW=none/Mem=thin/Glob=none
47. **Equiv.symm** — the inverse of an equivalence. [docstring]
    Logic/Equiv/Defs.lean · richness 0: none · CW=none/Mem=none/Glob=rich
48. **PartialEquiv.symm** — the inverse of a partial equivalence. [docstring]
    Logic/Equiv/PartialEquiv.lean · richness 0: none · CW=none/Mem=none/Glob=thin
49. **Equiv.ulift** — `ULift` of a type is equivalent to the original type. [docstring]
    Logic/Equiv/Defs.lean · richness 0: none · CW=none/Mem=none/Glob=thin
50. **Set.sInter** — the intersection of a set of sets. [docstring]
    Order/SetNotation.lean · richness 0: none · CW=none/Mem=thin/Glob=none
51. **Int.castRingHom** — the canonical ring homomorphism from the integers into any ring. [docstring]
    Data/Int/Cast/Lemmas.lean · richness 0: none · CW=none/Mem=none/Glob=thin
52. **Set.sUnion** — the union of a set of sets. [docstring]
    Order/SetNotation.lean · richness 0: none · CW=none/Mem=thin/Glob=none

## Worth a second look

- **Equiv.prodAssoc (4), Equiv.Set.univ (6), Equiv.sumCongr (7), Equiv.swap (8)** — not hard to *describe* (their docstrings are clear), but their richness scores are misleading: most of the counted structure is `=>` from `where`-block/anonymous-constructor lambda arms building the four components of an equivalence proof (`toFun`/`invFun`/`left_inv`/`right_inv`), not case-based branching on the definition's own mathematical content. These rank artificially high relative to their actual conceptual difficulty — see `docs/harvest_review_batch2.md` §5, item 3.
- **Finset.noncommProd (15) and Finset.sup' (24)** — both docstrings end in a stray `-/]` fragment (visible in the raw manifest's `docstring` field), a scanner docstring-capture artifact, not part of the actual documentation. The descriptions above are still accurate (the garbage is at the very end, after the meaningful content), but the raw field shouldn't be used verbatim in a dossier without trimming it first.
- **ArithmeticFunction (33)** — the name itself is the whole namespace root (no dotted prefix), and its docstring describes a *type* (`ZeroHom ℕ R`) rather than a function; worth confirming this is meant to be mined as a definitional target the same way a predicate or computation would be, rather than treated as a structural/type-former case needing different dossier treatment (cf. `Cycle` in batch 1, flagged for the same reason).
- **Int.castRingHom (51)** — docstring is terse to the point of being closer to a type signature restated in words (`coe : ℤ → α as a RingHom`) than a description of *why* this exists; a dossier author will need to supply more context than the docstring alone gives.
