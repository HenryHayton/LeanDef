# Harvest Batch 3 Digest

Skimmable companion to `docs/harvest_review_batch3.md` (the full mechanical review, gate-attrition analysis, and changelog vs. batch 2). Same format as `docs/harvest_digest_batch2.md`. The eligible set (120) is small enough to cover in full below, not truncated to a top-N slice.

## Shape of the batch

120 definitions are eligible this round — more than double batch 2's 52, on the identical corpus, purely from the selection-mechanism recalibration (see the review doc's §2 changelog). By subject: a large, genuinely systematic **order-theory cluster** (`Monotone`/`Antitone`/`StrictMono`/`StrictAnti` and their `...On` set-restricted variants from `Order/Monotone/Defs.lean`, plus `Monovary`/`Antivary`/`MonovaryOn`/`AntivaryOn`, `CovBy`/`WCovBy`, `Directed`/`DirectedOn`), a **relation-properties cluster** (`Relator.LeftUnique`/`RightUnique`/`BiUnique`, `Function.Semiconj`/`Commute`/`IsFixedPt`/`FactorsThrough`, `Pairwise`/`Set.Pairwise`/`AntisymmRel`), a **dependent-equivalence cluster** (`Equiv.piEquivPiSubtypeProd`, `Equiv.sumPiEquivProdPi`, `Equiv.piCurry`, `Equiv.piFinsetUnion` — genuinely dependent-type-indexed, not proof-scaffolding noise), and the familiar **Nat arithmetic-function family** (`Nat.log`/`clog`, `choose`, `factorial`, `ascFactorial`/`descFactorial`, `pair`/`unpair`, `bell`, `numDerangements`).

Richness is doing real, visible work at the top now (`Nat.leRec` at 12, `Nat.clog` at 10, `Relation.Map` at 8) without the lambda-arm noise that inflated several `Equiv.*` entries in batch 2 — none of the fixed-away entries (`Equiv.prodAssoc`, `Equiv.Set.univ`, `Equiv.sumCongr`, `Equiv.swap`) reappear here; see the review doc §2 for the direct before/after.

**Systematic near-duplicate families, flagged for curation attention** (not acted on here, per this task's scope): the eight `Order/Monotone/Defs.lean` monotone/antitone variants (ranks 37-45) are a single underlying concept (`a ≤ b → f a ≤ f b`, and its strict/on-a-set/reversed variants) mined as eight separate candidates. Same pattern, smaller, for `Monovary`/`Antivary`/`MonovaryOn`/`AntivaryOn` (ranks 16-17, 21-22) and `Relator.LeftUnique`/`RightUnique` (ranks 54-55). Whether these should all be separate mining targets or curated down to a representative few (the way `miner/curation.yaml` already notes `Pairwise`/`Set.Pairwise` as a pair) is a judgment call for whoever edits curation next, not something gates or richness can or should resolve mechanically.

Best formalization targets this batch:

- **`Nat.clog`/`Nat.log`** (ranks 2, 4) — the same fuel-recursive floor/ceiling logarithm pair from batch 2, still the strongest concrete-arithmetic candidates.
- **`Nat.leRec`** (rank 1, new) — a genuine dependent induction principle (recursion from a base point `n` upward), real quantifier/comparison/hypothesis-binder content, not proof scaffolding.
- **`Relation.Map`** (rank 3, new) — a real relation-transport construction with existential/conjunction content.
- **`Equiv.piEquivPiSubtypeProd`/`Equiv.sumPiEquivProdPi`** (ranks 5, 10) — genuinely dependent-type-indexed equivalences, good tests of whether a candidate can handle real dependent typing, not just notation.
- **The `Monotone`/`StrictMono` family** (ranks 37-45) — individually clean, two-clause conditional-implication definitions; excellent boundary-condition/mutant material even if curation eventually thins the family down to a representative subset.
- **`DependsOn`** (rank 12) — an unusually candid docstring about its own scope and a named companion lemma (`dependsOn_univ`), good dossier raw material.

## Full eligible list (rank order)

1. **Nat.leRec** — recursion up from a base point `n`: given a base case and a step from any `k ≥ n` to `k+1`, produces a value at every `m ≥ n`. [docstring]
   Data/Nat/Init.lean · richness 12: 2 cond, 2 quant, 6 comp, 2 hyp · value · CW=none/Mem=none/Glob=thin
2. **Nat.clog** — the ceiling (round-up) base-`b` logarithm of `n`. [docstring]
   Data/Nat/Log.lean · richness 10: 1 conj, 5 cond, 4 comp · value · CW=rich/Mem=none/Glob=rich
3. **Relation.Map** — pushes a relation `r` on `α × β` to a relation on `γ × δ` through a pair of functions `f : α → γ`, `g : β → δ`. [docstring]
   Logic/Relation.lean · richness 8: 2 conj, 1 quant, 2 comp, 3 hyp · prop · CW=none/Mem=thin/Glob=rich
4. **Nat.log** — the floor (round-down) base-`b` logarithm of `n`. [docstring]
   Data/Nat/Log.lean · richness 8: 5 cond, 3 comp · value · CW=rich/Mem=none/Glob=rich
5. **Equiv.piEquivPiSubtypeProd** — splits the type of dependent functions on `α` into a product, by separating indices satisfying a predicate `p` from those that don't. [docstring]
   Logic/Equiv/Prod.lean · richness 8: 1 cond, 3 quant, 2 comp, 2 hyp · bundled · CW=none/Mem=none/Glob=thin
6. **Int.leInduction** — an induction principle for integers starting from a lower bound `m` and stepping upward. [inferred from signature; docstring only cross-references a sibling lemma]
   Data/Int/Init.lean · richness 8: 3 quant, 3 comp, 2 hyp · value · CW=none/Mem=none/Glob=thin
7. **Int.leInductionDown** — the downward-direction counterpart of `Int.leInduction`: induction from an upper bound `m` stepping down. [inferred from signature; docstring only cross-references a sibling lemma]
   Data/Int/Init.lean · richness 8: 3 quant, 3 comp, 2 hyp · value · CW=none/Mem=none/Glob=thin
8. **Function.extend** — extends a function `g` defined along `f` to the whole codomain, using a junk-value function `j` off the range of `f`. [docstring]
   Logic/Function/Basic.lean · richness 6: 1 cond, 1 quant, 1 comp, 3 hyp · value · CW=none/Mem=none/Glob=rich
9. **Equiv.sumCompl** — for a predicate `p`, the sum of `{a // p a}` and its complement is equivalent to the whole type. [docstring]
   Logic/Equiv/Sum.lean · richness 6: 1 cond, 4 comp, 1 hyp · bundled · CW=none/Mem=none/Glob=rich
10. **Equiv.sumPiEquivProdPi** — dependent functions on a sum-type index are equivalent to pairs of dependent functions on each summand. [docstring]
    Logic/Equiv/Prod.lean · richness 6: 3 quant, 2 comp, 1 hyp · bundled · CW=none/Mem=none/Glob=rich
11. **finSumNatEquiv** — equivalence between `Fin n ⊕ ℕ` and `ℕ`, sending a `Fin n` element to its value and an `ℕ` element `a` to `n + a`. [docstring]
    Logic/Equiv/Fin/Basic.lean · richness 6: 2 cond, 4 comp · bundled · CW=none/Mem=none/Glob=thin
12. **DependsOn** — a function depends only on a set `s` if agreeing on `s` forces agreeing outputs. [docstring]
    Logic/Function/DependsOn.lean · richness 5: 2 quant, 2 comp, 1 hyp · prop · CW=none/Mem=thin/Glob=rich
13. **Function.Semiconj** — `f` semiconjugates `ga` to `gb` if `f ∘ ga = gb ∘ f`. [docstring]
    Logic/Function/Conjugate.lean · richness 5: 1 quant, 1 comp, 3 hyp · prop · CW=none/Mem=thin/Glob=rich
14. **Directed** — a family is directed w.r.t. a relation if some member sits above any pair in the family. [docstring]
    Order/Directed.lean · richness 5: 1 conj, 2 quant, 2 hyp · prop · CW=none/Mem=thin/Glob=rich
15. **DirectedOn** — a subset is directed if some element of the set sits above any pair in the set. [docstring]
    Order/Directed.lean · richness 5: 1 conj, 3 quant, 1 hyp · prop · CW=none/Mem=thin/Glob=rich
16. **MonovaryOn** — `f` monovaries with `g` on `s` if `g i < g j` implies `f i ≤ f j`, for all `i, j ∈ s`. [docstring]
    Order/Monotone/Monovary.lean · richness 5: 1 quant, 2 comp, 2 hyp · prop · CW=none/Mem=thin/Glob=rich
17. **AntivaryOn** — `f` antivaries with `g` on `s` if `g i < g j` implies `f j ≤ f i`, for all `i, j ∈ s`. [docstring]
    Order/Monotone/Monovary.lean · richness 5: 1 quant, 2 comp, 2 hyp · prop · CW=none/Mem=thin/Glob=rich
18. **StrongLT** — a function `a` is strongly less than `b` if `a i < b i` for every index `i`. [docstring]
    Order/Basic.lean · richness 5: 3 quant, 1 comp, 1 hyp · prop · CW=none/Mem=thin/Glob=rich
19. **WCovBy** — `a` weakly covers `b` (or `b` covers `a`): `a ≤ b` with nothing strictly between. [docstring]
    Order/Defs/PartialOrder.lean · richness 5: 1 conj, 1 quant, 3 comp · prop · CW=none/Mem=thin/Glob=rich
20. **List.Forall** — `l.Forall p` unfolds directly to the conjunction of `p` over each element of `l`. [docstring]
    Data/List/Defs.lean · richness 5: 1 conj, 3 cond, 1 hyp · prop · CW=none/Mem=thin/Glob=rich
21. **Monovary** — `f` monovaries with `g` if `g i < g j` implies `f i ≤ f j`, everywhere. [docstring]
    Order/Monotone/Monovary.lean · richness 5: 1 quant, 2 comp, 2 hyp · prop · CW=none/Mem=thin/Glob=rich
22. **Antivary** — `f` antivaries with `g` if `g i < g j` implies `f j ≤ f i`, everywhere. [docstring]
    Order/Monotone/Monovary.lean · richness 5: 1 quant, 2 comp, 2 hyp · prop · CW=none/Mem=thin/Glob=rich
23. **hyperoperation** — the `n`th hyperoperation between `m` and `k` (the generalized succession/addition/multiplication/exponentiation... hierarchy). [docstring]
    Data/Nat/Hyperoperation.lean · richness 5: 5 cond · value · CW=rich/Mem=none/Glob=rich
24. **CovBy** — `b` covers `a`: `a < b` with nothing strictly between. [docstring]
    Order/Defs/PartialOrder.lean · richness 5: 1 conj, 1 quant, 3 comp · prop · CW=none/Mem=thin/Glob=rich
25. **Equiv.piFinsetUnion** — dependent functions on the disjoint union of two finsets are equivalent to pairs of dependent functions on each. [docstring]
    Data/Finset/Basic.lean · richness 5: 3 quant, 1 comp, 1 hyp · bundled · CW=none/Mem=none/Glob=rich
26. **OrderHom.antisymmetrization** — turns an order homomorphism into one between the antisymmetrizations of its domain and codomain. [docstring]
    Order/Antisymmetrization.lean · richness 5: 1 cond, 3 comp, 1 hyp · value · CW=none/Mem=none/Glob=thin
27. **subtypeOrLeftEmbedding** — a subtype over a disjunction `p ∨ q` embeds injectively into the sum of the two individual subtypes. [docstring]
    Logic/Embedding/Basic.lean · richness 5: 1 disj, 1 cond, 2 comp, 1 hyp · bundled · CW=none/Mem=none/Glob=thin
28. **Set.piecewise** — the function equal to `f` on a set `s` and to `g` on its complement. [docstring]
    Logic/Function/Basic.lean · richness 5: 1 cond, 3 quant, 1 hyp · value · CW=none/Mem=thin/Glob=rich
29. **ExistsUnique** — there exists a unique `x` satisfying `p`. [docstring]
    Logic/ExistsUnique.lean · richness 5: 1 conj, 2 quant, 1 comp, 1 hyp · prop · CW=none/Mem=thin/Glob=rich
30. **List.sym** — all unordered `n`-tuples drawn from a list, in some order. [docstring]
    Data/List/Sym.lean · richness 5: 4 cond, 1 comp · value · CW=none/Mem=thin/Glob=thin
31. **Function.FactorsThrough** — `g` factors through `f` if `f a = f b` implies `g a = g b`. [docstring]
    Logic/Function/Basic.lean · richness 5: 1 quant, 2 comp, 2 hyp · prop · CW=none/Mem=thin/Glob=thin
32. **Equiv.sumAssoc** — sum of types is associative up to equivalence. [docstring]
    Logic/Equiv/Sum.lean · richness 5: 5 comp · bundled · CW=none/Mem=none/Glob=rich
33. **Equiv.subtypeEquiv** — if `α ≃ β` and corresponding predicates `p`/`q` agree under that equivalence, the subtypes `{a // p a}` and `{b // q b}` are equivalent. [docstring]
    Logic/Equiv/Basic.lean · richness 4: 1 quant, 2 comp, 1 hyp · bundled · CW=none/Mem=none/Glob=thin
34. **Set.Pairwise** — a relation `r` holds pairwise on a set `s` if it relates every two distinct elements of `s`. [docstring]
    Logic/Pairwise.lean · richness 4: 2 quant, 1 comp, 1 hyp · prop · CW=none/Mem=thin/Glob=rich [note]
35. **IsDvdSequence** — `f` is a divisibility sequence if `a ∣ b` implies `f a ∣ f b`. [docstring]
    Data/Nat/DvdSequence.lean · richness 4: 1 quant, 2 comp, 1 hyp · prop · CW=none/Mem=thin/Glob=rich
36. **Equiv.piCurry** — dependent functions on a sigma type are equivalent to dependent functions of two arguments (curried form). [docstring]
    Logic/Equiv/Basic.lean · richness 4: 3 quant, 1 hyp · bundled · CW=none/Mem=none/Glob=thin
37. **StrictMono** — `f` is strictly monotone if `a < b` implies `f a < f b`. [docstring]
    Order/Monotone/Defs.lean · richness 4: 1 quant, 2 comp, 1 hyp · prop · CW=none/Mem=thin/Glob=rich
38. **StrictAnti** — `f` is strictly antitone if `a < b` implies `f b < f a`. [docstring]
    Order/Monotone/Defs.lean · richness 4: 1 quant, 2 comp, 1 hyp · prop · CW=none/Mem=thin/Glob=rich
39. **Nat.findGreatest** — the largest `i ≤ n` satisfying `P`, or `0` if none does. [docstring]
    Data/Nat/Find.lean · richness 4: 3 cond, 1 hyp · value · CW=none/Mem=none/Glob=rich
40. **Monotone** — `f` is monotone if `a ≤ b` implies `f a ≤ f b`. [docstring]
    Order/Monotone/Defs.lean · richness 4: 1 quant, 2 comp, 1 hyp · prop · CW=none/Mem=thin/Glob=rich
41. **Antitone** — `f` is antitone if `a ≤ b` implies `f b ≤ f a`. [docstring]
    Order/Monotone/Defs.lean · richness 4: 1 quant, 2 comp, 1 hyp · prop · CW=none/Mem=thin/Glob=rich
42. **StrictMonoOn** — `f` is strictly monotone on `s` if `a < b` implies `f a < f b` for `a, b ∈ s`. [docstring]
    Order/Monotone/Defs.lean · richness 4: 1 quant, 2 comp, 1 hyp · prop · CW=none/Mem=thin/Glob=rich
43. **StrictAntiOn** — `f` is strictly antitone on `s` if `a < b` implies `f b < f a` for `a, b ∈ s`. [docstring]
    Order/Monotone/Defs.lean · richness 4: 1 quant, 2 comp, 1 hyp · prop · CW=none/Mem=thin/Glob=rich
44. **MonotoneOn** — `f` is monotone on `s` if `a ≤ b` implies `f a ≤ f b` for `a, b ∈ s`. [docstring]
    Order/Monotone/Defs.lean · richness 4: 1 quant, 2 comp, 1 hyp · prop · CW=none/Mem=thin/Glob=rich
45. **AntitoneOn** — `f` is antitone on `s` if `a ≤ b` implies `f b ≤ f a` for `a, b ∈ s`. [docstring]
    Order/Monotone/Defs.lean · richness 4: 1 quant, 2 comp, 1 hyp · prop · CW=none/Mem=thin/Glob=rich
46. **Pi.map** — applies a family of functions `f i` componentwise to a dependent function. [docstring]
    Logic/Function/Defs.lean · richness 4: 3 quant, 1 hyp · value · CW=none/Mem=none/Glob=rich
47. **Function.prod** — pairs two dependent functions into one returning both outputs together. [docstring]
    Logic/Function/Defs.lean · richness 4: 2 quant, 2 hyp · value · CW=none/Mem=none/Glob=rich
48. **PartialEquiv.pi** — the product of a family of partial equivalences, as a partial equivalence on the Pi type. [docstring]
    Logic/Equiv/PartialEquiv.lean · richness 4: 3 quant, 1 hyp · bundled · CW=none/Mem=none/Glob=thin
49. **Int.xor** — bitwise xor of two integers. [docstring]
    Data/Int/Bitwise.lean · richness 4: 4 cond · value · CW=rich/Mem=none/Glob=thin
50. **Function.update** — replaces the value of a function at one point. [docstring]
    Logic/Function/Basic.lean · richness 4: 1 cond, 1 quant, 1 comp, 1 hyp · value · CW=none/Mem=none/Glob=rich
51. **Xor** — exclusive or of two propositions. [docstring]
    Logic/Basic.lean · richness 4: 2 conj, 1 disj, 1 hyp · prop · CW=none/Mem=thin/Glob=rich
52. **finSumFinEquiv** — the bijection between a disjoint union of two finite ordinals and one ordinal of the summed size. [docstring]
    Logic/Equiv/Fin/Basic.lean · richness 4: 4 comp · bundled · CW=none/Mem=none/Glob=rich
53. **ArithmeticFunction.IsMultiplicative** — an arithmetic function is multiplicative if it respects products of coprime arguments. [inferred from name and type; docstring is only the two-word title]
    NumberTheory/ArithmeticFunction/Defs.lean · richness 4: 1 conj, 1 quant, 2 comp · prop · CW=none/Mem=thin/Glob=thin
54. **Relator.RightUnique** — a relation is right-unique if every left element pairs with at most one right element. [docstring]
    Logic/Relator.lean · richness 3: 1 quant, 1 comp, 1 hyp · prop · CW=none/Mem=thin/Glob=thin
55. **Relator.LeftUnique** — a relation is left-unique if every right element pairs with at most one left element. [docstring]
    Logic/Relator.lean · richness 3: 1 quant, 1 comp, 1 hyp · prop · CW=none/Mem=thin/Glob=thin
56. **Nat.choose** — the number of `k`-element subsets of an `n`-element set (binomial coefficient). [docstring]
    Data/Nat/Choose/Basic.lean · richness 3: 3 cond · value · CW=rich/Mem=none/Glob=rich
57. **List.TFAE** — "the following are equivalent": a list of propositions that all imply each other. [docstring]
    Data/List/TFAE.lean · richness 3: 2 quant, 1 hyp · prop · CW=none/Mem=thin/Glob=rich
58. **Nat.primeFactorsList** — the prime factorization of `n`, listed in increasing order. [docstring]
    Data/Nat/Factors.lean · richness 3: 3 cond · value · CW=rich/Mem=thin/Glob=thin
59. **Pairwise** — a relation `r` holds pairwise if it relates every two distinct elements. [docstring]
    Logic/Pairwise.lean · richness 3: 1 quant, 1 comp, 1 hyp · prop · CW=none/Mem=thin/Glob=rich [note]
60. **Finset.sym** — lifts a finset to the finset of unordered `n`-tuples drawn from it. [docstring]
    Data/Finset/Sym.lean · richness 3: 2 cond, 1 quant · value · CW=none/Mem=thin/Glob=rich
61. **Nat.bell** — the `n`th Bell number: the count of partitions of an `n`-element set. [docstring]
    Combinatorics/Enumerative/Bell.lean · richness 3: 2 cond, 1 comp · value · CW=rich/Mem=none/Glob=thin
62. **IsNilpotent** — an element is nilpotent if some power of it equals zero. [docstring]
    Algebra/GroupWithZero/Basic.lean · richness 2: 1 quant, 1 comp · prop · CW=none/Mem=thin/Glob=rich
63. **npowRec'** — a variant of the natural-number-power recursor that's a semigroup homomorphism from positive naturals. [docstring]
    Algebra/Group/Defs.lean · richness 3: 3 cond · value · CW=none/Mem=none/Glob=rich
64. **Equiv.piCongrLeft'** — transports dependent functions along an equivalence of the base (index) space. [docstring]
    Logic/Equiv/Basic.lean · richness 3: 2 quant, 1 hyp · bundled · CW=none/Mem=none/Glob=thin
65. **numDerangements** — the number of derangements (fixed-point-free permutations) of an `n`-element set. [docstring]
    Combinatorics/Derangements/Finite.lean · richness 3: 3 cond · value · CW=rich/Mem=none/Glob=rich
66. **Nat.descFactorial** — the descending factorial `n!/(n-k)!`, computed recursively. [docstring]
    Data/Nat/Factorial/Basic.lean · richness 2: 2 cond · value · CW=rich/Mem=none/Glob=rich
67. **Finset.orderEmbOfFin** — the increasing bijection between `Fin k` and a cardinality-`k` finset in a linear order, as an order embedding. [docstring]
    Data/Finset/Sort.lean · richness 2: 1 comp, 1 hyp · bundled · CW=none/Mem=thin/Glob=thin
68. **Finset.disjiUnion** — the union of `f i` over `i ∈ s`, given a proof the images are pairwise disjoint. [docstring]
    Data/Finset/Union.lean · richness 2: 1 comp, 1 hyp · value · CW=none/Mem=thin/Glob=thin
69. **AddMonoidHom.mul** — multiplication by a ring element, bundled as an additive homomorphism in both arguments. [docstring]
    Algebra/Ring/Basic.lean · richness 2: 2 comp · value · CW=none/Mem=none/Glob=rich
70. **Relation.SymmGen** — the symmetric closure of a relation: `r a b` or `r b a`. [docstring]
    Logic/Relation.lean · richness 2: 1 disj, 1 hyp · prop · CW=none/Mem=thin/Glob=rich
71. **Nat.shiftLeft'** — left-shifts `m` by `n`, inserting bit `b` at the low end each time. [docstring]
    Data/Nat/Bits.lean · richness 2: 2 cond · value · CW=rich/Mem=none/Glob=thin
72. **Function.Bijective** — a function is bijective if it is both injective and surjective. [docstring]
    Logic/Function/Defs.lean · richness 2: 1 conj, 1 hyp · prop · CW=none/Mem=thin/Glob=rich
73. **Relator.BiUnique** — a relation is bi-unique if it is both left- and right-unique. [docstring]
    Logic/Relator.lean · richness 2: 1 conj, 1 hyp · prop · CW=none/Mem=thin/Glob=thin
74. **Finset.fold** — folds a commutative associative operation over the image of a finset under `f`. [docstring]
    Data/Finset/Fold.lean · richness 2: 2 hyp · value · CW=none/Mem=thin/Glob=rich
75. **Finset.noncommProd** — the product of a function's values over a finset under a possibly-noncommutative operation, given a proof it commutes on the values actually used. [docstring]
    Data/Finset/NoncommProd.lean · richness 2: 1 comp, 1 hyp · value · CW=none/Mem=thin/Glob=thin
76. **Function.IsFixedPt** — `x` is a fixed point of `f` if `f x = x`. [docstring]
    Logic/Function/Defs.lean · richness 2: 1 comp, 1 hyp · prop · CW=none/Mem=thin/Glob=thin
77. **derangements** — the set of fixed-point-free permutations of a type. [docstring]
    Combinatorics/Derangements/Basic.lean · richness 2: 1 quant, 1 comp · bundled · CW=none/Mem=thin/Glob=rich
78. **finSuccEquiv'** — an equivalence removing one index `i` and mapping it to `none`. [docstring]
    Logic/Equiv/Fin/Basic.lean · richness 2: 2 comp · bundled · CW=none/Mem=none/Glob=rich
79. **Nat.ascFactorial** — the ascending factorial `n(n+1)⋯(n+k-1)`. [docstring]
    Data/Nat/Factorial/Basic.lean · richness 2: 2 cond · value · CW=rich/Mem=none/Glob=thin
80. **Finset.subtype** — the finset of `Subtype p` elements belonging to a given finset `s`. [docstring]
    Data/Finset/Image.lean · richness 2: 1 comp, 1 hyp · value · CW=none/Mem=thin/Glob=thin
81. **Equiv.piUnique** — when the domain has a unique element, dependent functions on it are equivalent to their single value. [docstring]
    Logic/Equiv/Defs.lean · richness 2: 1 quant, 1 hyp · bundled · CW=none/Mem=none/Glob=thin
82. **AntisymmRel** — two elements are antisymmetrization-related under `r` if each relates to the other. [docstring]
    Order/Antisymmetrization.lean · richness 2: 1 conj, 1 hyp · prop · CW=none/Mem=thin/Glob=rich
83. **Equiv.arrowProdEquivProdArrow** — functions into a product are equivalent to pairs of functions into each factor. [docstring]
    Logic/Equiv/Prod.lean · richness 2: 2 hyp · bundled · CW=none/Mem=none/Glob=thin
84. **Equiv.sumArrowEquivProdArrow** — functions on a sum type are equivalent to pairs of functions on each summand. [docstring]
    Logic/Equiv/Prod.lean · richness 2: 2 comp · bundled · CW=none/Mem=none/Glob=thin
85. **Set.Sized** — every finset in a family has the same size `r`. [docstring]
    Data/Finset/Slice.lean · richness 2: 1 quant, 1 comp · prop · CW=none/Mem=thin/Glob=rich
86. **Equiv.optionCongr** — a universe-polymorphic version of mapping an equivalence over `Option`. [docstring]
    Logic/Equiv/Option.lean · richness 2: 2 comp · bundled · CW=none/Mem=none/Glob=thin
87. **Function.FromTypes** — the type of `n`-ary functions across a family of types indexed by `Fin n`. [docstring]
    Logic/Function/FromTypes.lean · richness 2: 2 cond · bundled · CW=none/Mem=none/Glob=thin
88. **Nat.minFac** — the smallest prime factor of a natural number. [docstring]
    Data/Nat/Prime/Defs.lean · richness 2: 1 cond, 1 comp · value · CW=rich/Mem=none/Glob=thin
89. **Nat.unpair** — recovers the pair of naturals encoded by `Nat.pair`. [docstring]
    Data/Nat/Pairing.lean · richness 2: 1 cond, 1 comp · value · CW=rich/Mem=none/Glob=rich
90. **Nat.factorial** — the factorial of a natural number. [docstring]
    Data/Nat/Factorial/Basic.lean · richness 2: 2 cond · value · CW=rich/Mem=none/Glob=rich
91. **Nat.pair** — a pairing function encoding two naturals as one. [docstring]
    Data/Nat/Pairing.lean · richness 2: 1 cond, 1 comp · value · CW=rich/Mem=none/Glob=rich
92. **Nat.find** — the smallest natural number satisfying a decidable predicate, given a proof one exists. [docstring]
    Data/Nat/Find.lean · richness 1: 1 hyp · value · CW=none/Mem=none/Glob=rich
93. **OrderIso.dualAntisymmetrization** — antisymmetrization commutes with taking the order-dual. [docstring]
    Order/Antisymmetrization.lean · richness 2: 2 comp · bundled · CW=none/Mem=none/Glob=thin
94. **Equiv.cast** — the equivalence between two types known to be equal. [docstring]
    Logic/Equiv/Defs.lean · richness 2: 1 comp, 1 hyp · bundled · CW=none/Mem=none/Glob=rich
95. **Finset.filter** — the elements of a finset satisfying a predicate. [docstring]
    Data/Finset/Filter.lean · richness 1: 1 hyp · value · CW=none/Mem=thin/Glob=rich
96. **Finset.cons** — inserts an element into a finset, given a proof it isn't already present. [docstring]
    Data/Finset/Insert.lean · richness 1: 1 hyp · value · CW=none/Mem=thin/Glob=rich
97. **Int.sqrt** — the integer square root: largest `r` with `r*r ≤ n` for positive input, `0` otherwise. [docstring]
    Data/Int/Sqrt.lean · richness 1: 1 comp · value · CW=rich/Mem=none/Glob=thin
98. **Finset.Nonempty** — a finset is nonempty. [docstring]
    Data/Finset/Empty.lean · richness 1: 1 quant · prop · CW=none/Mem=thin/Glob=rich
99. **Function.Commute** — two self-maps commute if applying them in either order agrees. [docstring]
    Logic/Function/Conjugate.lean · richness 1: 1 hyp · prop · CW=none/Mem=thin/Glob=rich
100. **Nat.properDivisors** — the divisors of `n` other than `n` itself. [docstring]
     NumberTheory/Divisors.lean · richness 1: 1 comp · value · CW=rich/Mem=thin/Glob=thin
101. **Nat.divisors** — the finset of divisors of `n`. [docstring]
     NumberTheory/Divisors.lean · richness 1: 1 comp · value · CW=rich/Mem=thin/Glob=rich
102. **List.dedup** — removes duplicates from a list, keeping only the last occurrence of each. [docstring]
     Data/List/Defs.lean · richness 1: 1 comp · value · CW=none/Mem=thin/Glob=thin
103. **Nat.multinomial** — the multinomial coefficient for a multiset of symbol multiplicities. [docstring]
     Data/Nat/Choose/Multinomial.lean · richness 1: 1 hyp · value · CW=none/Mem=thin/Glob=rich
104. **Finset.restrict₂** — restricts a function already restricted to `t` down further to a subset `s ⊆ t`. [docstring]
     Data/Finset/Pi.lean · richness 1: 1 hyp · value · CW=none/Mem=none/Glob=rich
105. **Finset.biUnion** — the union of `t a` over `a ∈ s`. [docstring]
     Data/Finset/Union.lean · richness 1: 1 hyp · value · CW=none/Mem=thin/Glob=rich
106. **Nat.ModEq** — two naturals are congruent modulo `n` if they leave the same remainder. [docstring]
     Data/Nat/ModEq.lean · richness 1: 1 comp · prop · CW=rich/Mem=rich/Glob=rich
107. **Finset.offDiag** — the pairs `(a, b)` in `s × s` with `a ≠ b`. [docstring]
     Data/Finset/Prod.lean · richness 1: 1 comp · value · CW=none/Mem=thin/Glob=thin
108. **IsComplemented** — an element is complemented if it has a complement. [docstring]
     Order/Disjoint.lean · richness 1: 1 quant · prop · CW=none/Mem=thin/Glob=rich
109. **ArithmeticFunction.zeta** — the arithmetic function that is `0` at `0` and `1` everywhere else (the Riemann zeta Dirichlet series). [docstring]
     NumberTheory/ArithmeticFunction/Zeta.lean · richness 1: 1 comp · value · CW=none/Mem=none/Glob=thin
110. **Int.ModEq** — two integers are congruent modulo `n` if they leave the same remainder. [docstring]
     Data/Int/ModEq.lean · richness 1: 1 comp · prop · CW=rich/Mem=rich/Glob=thin
111. **Nat.factorization** — the finitely-supported function mapping each prime factor of `n` to its multiplicity. [docstring]
     Data/Nat/Factorization/Defs.lean · richness 1: 1 cond · value · CW=none/Mem=none/Glob=thin
112. **Finset.sup** — the supremum of a function's image over a finset. [docstring]
     Data/Finset/Lattice/Fold.lean · richness 1: 1 hyp · value · CW=none/Mem=thin/Glob=rich
113. **Finset.restrict** — restricts a function to a finite subset of its domain. [docstring]
     Data/Finset/Pi.lean · richness 1: 1 hyp · value · CW=none/Mem=thin/Glob=rich
114. **Finset.image** — the image of a finset under a function. [docstring]
     Data/Finset/Image.lean · richness 1: 1 hyp · value · CW=none/Mem=thin/Glob=rich
115. **zmultiplesHom** — additive homomorphisms from `ℤ`, determined by the image of `1`. [docstring]
     Data/Int/Cast/Lemmas.lean · richness 1: 1 comp · bundled · CW=none/Mem=none/Glob=thin
116. **Set.iInter** — the intersection of an indexed family of sets. [docstring]
     Order/SetNotation.lean · richness 1: 1 hyp · value · CW=none/Mem=thin/Glob=rich
117. **Function.Coequalizer.mk** — the canonical projection into a coequalizer. [docstring]
     Logic/Function/Coequalizer.lean · richness 1: 1 hyp · value · CW=none/Mem=none/Glob=thin
118. **toAntisymmetrization** — turns an element into its antisymmetrization class. [docstring]
     Order/Antisymmetrization.lean · richness 1: 1 hyp · value · CW=none/Mem=none/Glob=rich
119. **Functor.mapEquiv** — applies a functor to an equivalence. [docstring]
     Logic/Equiv/Functor.lean · richness 1: 1 hyp · bundled · CW=none/Mem=none/Glob=thin
120. **Function.Embedding.subtype** — the inclusion of a subtype into its ambient type, as an injective embedding. [docstring]
     Logic/Embedding/Basic.lean · richness 1: 1 hyp · bundled · CW=none/Mem=none/Glob=rich

## Worth a second look

- **Int.leInduction (6) and Int.leInductionDown (7)** — genuinely hard to describe from the docstring alone: both say only "See `Int.inductionOn'` for an induction in both directions," a cross-reference rather than a self-contained description. The one-liners above are inferred from the signature, not the docstring; a dossier author will need the same signature-reading, or a look at `Int.inductionOn'` itself.
- **ArithmeticFunction.IsMultiplicative (53)** — docstring is a two-word title ("Multiplicative functions"), no stated condition. The description above is inferred from the name and the standard number-theoretic meaning, not stated in the source docstring itself — worth confirming against the actual definition body before using in a dossier.
- **The eight-way `Order/Monotone/Defs.lean` family (37-45) and the `Monovary`/`Antivary` four-way family (16-17, 21-22)** — not hard to describe individually (each is a clean one-clause implication), but genuinely hard to justify mining as eight/four *separate* targets rather than one representative each plus documented variants. Flagged here as the clearest curation-worthy near-duplicate cluster this batch, larger in scope than batch 1's single `Pairwise`/`Set.Pairwise` pair.
- **`Relator.LeftUnique`/`RightUnique`/`BiUnique` (54, 55, 73)** — same near-duplicate concern as above, smaller cluster (three relation-uniqueness properties that are pairwise/compositionally related).
- **`Pairwise` (59) and `Set.Pairwise` (34)** — both back in the eligible set after the vocabulary-gate fix (see the review doc §2); `miner/curation.yaml` already carries a `note` entry for this pair from batch 1, unchanged and still applicable.
