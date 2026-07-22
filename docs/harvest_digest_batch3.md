# Harvest Batch 3 Digest

Skimmable companion to `docs/harvest_review_batch3.md` (the full mechanical review, gate-attrition analysis, and changelogs vs. batch 2 and — this revision — vs. batch 3 revision 1). Same format as `docs/harvest_digest_batch2.md`.

**Revision 2.** `docs/theorem_mention_audit.md` found the theorem-mention count backing `theorem_mention_floor` was undercounting (qualified-name-only matching missed most real, unqualified, same-namespace mentions). Fixed; see the review doc's §0 for the full changelog. **Eligible set: 120 → 256.** At 256, the set exceeds this digest's own "cover in full if readable" threshold (the design commits to "top ~150, total stated" past that point) — given the doc has just over doubled in one revision, this digest covers the **top 40** below in full (a smaller, deliberately proportionate slice given the size jump, not the full ~150 the design allows) and states the total; the complete ranked list of all 256, including ranks 41-256, is in the review doc's §6.

## Shape of the batch (revision 2)

The mention-count fix's yield concentrated exactly where the corpus-widening effort (batch 2) was aimed: 75 of the 135 newly-eligible candidates are `Data/*`, but the *proportional* gain is largest outside the original five corners — `Order`, `NumberTheory`, and `Combinatorics` together went from 22+37+51 = a small fringe under revision 1 to a combined 63 of 256 eligible (25%) under this revision. A new, previously entirely invisible **dependent-induction/recursion cluster** now anchors the top of the ranking: `Nat.leRec`, `Nat.binaryRec`, `Nat.decreasingInduction`, `Nat.evenOddRec`, `Int.leInduction`/`Int.leInductionDown`, `Int.greatestOfBdd`/`Int.leastOfBdd`, `List.recNeNil` — genuine `motive`-based induction principles, real quantifier/hypothesis-binder content, none of it lambda-arm noise. The revision-1 top 5 (`Nat.leRec`, `Nat.clog`, `Relation.Map`, `Nat.log`, `Equiv.piEquivPiSubtypeProd`) are all still eligible but have been overtaken by this new cluster and by `Nat.binaryRec`/`List.prev` — displaced by richer content finally getting counted, not by anything wrong with them (see the review doc §0(iv)).

The order-theory and relation-properties near-duplicate clusters flagged in revision 1's digest (`Monotone`/`Antitone`/`StrictMono` family, `Monovary`/`Antivary` family, `Relator.*Unique` family) are all still present and still worth curation attention — unchanged concern, not resolved or worsened by this fix.

Best formalization targets this revision:

- **`Nat.leRec`/`Nat.decreasingInduction`/`Int.leInduction`/`Int.leInductionDown`** — a genuine family of induction principles now visible together for the first time; strong candidates for testing whether a definition-writer can handle dependent `motive`-based recursion correctly.
- **`Int.greatestOfBdd`/`Int.leastOfBdd`** — computable witness extraction under a boundedness hypothesis; rich in existentials and hypothesis binders, good mutant material (drop the boundedness hypothesis, flip the inequality direction).
- **`Nat.binaryRec`** — a foundational recursion principle over binary representations, previously entirely invisible to selection despite being genuinely well-established in Mathlib (raw `mention_count=26` per the audit's own sample).
- **`List.prev`** — worked examples baked into its own docstring, multi-case conditional structure, excellent dossier raw material.
- **`Finset.pi`** — revision 1's own review flagged this as "a new casualty... worth a second look"; now eligible (rank 104), resolving that concern directly.

## Top 40 (rank order)

1. **Int.greatestOfBdd** — a computable version of "there's a greatest value satisfying a bounded, decidable predicate": given an upper bound and a witness the predicate holds somewhere, returns the greatest satisfying value. [docstring]
   Data/Int/LeastGreatest.lean · richness 13: quantifiers/comparisons/hypothesis-heavy · value · new this revision (old_tmc=0 → new_tmc=3)
2. **Nat.leRec** — recursion up from a base point `n`: given a base case and a step from any `k ≥ n` to `k+1`, produces a value at every `m ≥ n`. [docstring]
   Data/Nat/Init.lean · richness 12 · value · was rank 1 (old_tmc=3 → new_tmc=15)
3. **Nat.binaryRec** — a recursion principle for binary (`bit`) representations of naturals: build a case for `0` and a case that extends from `n` to `bit b n`, and get every natural number. [docstring]
   Data/Nat/BinaryRec.lean · richness 11 · value · new this revision (old_tmc=0 → new_tmc=8)
4. **Nat.clog** — the ceiling (round-up) base-`b` logarithm of `n`. [docstring]
   Data/Nat/Log.lean · richness 10 · value · was rank 2 (old_tmc=9 → new_tmc=34)
5. **Int.leastOfBdd** — the least-value dual of rank 1: given a lower bound and a witness, returns the least value satisfying a bounded, decidable predicate. [docstring]
   Data/Int/LeastGreatest.lean · richness 10 · value · new this revision (old_tmc=0 → new_tmc=3)
6. **List.prev** — given a proof `x ∈ l`, returns the element immediately before `x`'s first occurrence in `l`. [docstring]
   Data/List/Cycle.lean · richness 9 · value · new this revision (old_tmc=0 → new_tmc=21)
7. **Finset.strongDownwardInduction** — an induction principle building a value on a finset from values on all larger-or-equal-cardinality supersets, working downward. [docstring]
   Data/Finset/Card.lean · richness 9 · value · new this revision (old_tmc=0 → new_tmc=2)
8. **Equiv.sigmaSigmaSubtypeEq** — a specialization of a nested-sigma equivalence to the case of plain equality constraints (useful for categorical `Hom`-like types). [docstring]
   Logic/Equiv/Basic.lean · richness 9 · bundled · new this revision (old_tmc=0 → new_tmc=2)
9. **List.recNeNil** — a dependent recursion principle for nonempty lists, avoiding the need to handle an impossible empty case. [docstring]
   Data/List/Induction.lean · richness 9 · value · new this revision (old_tmc=0 → new_tmc=2)
10. **Nat.decreasingInduction** — induction downward: if `P(k+1)` implies `P(k)` for all `k < n`, then `P(n)` implies `P(m)` for every `m ≤ n`. [docstring]
    Data/Nat/Init.lean · richness 8 · value · new this revision (old_tmc=0 → new_tmc=5)
11. **Relation.Map** — pushes a relation on `α × β` to a relation on `γ × δ` through a pair of functions `f`, `g`. [docstring]
    Logic/Relation.lean · richness 8 · prop · was rank 3 (old_tmc=17 → new_tmc=17, unchanged — already well-qualified)
12. **Nat.log** — the floor (round-down) base-`b` logarithm of `n`. [docstring]
    Data/Nat/Log.lean · richness 8 · value · was rank 4 (old_tmc=22 → new_tmc=99)
13. **Function.Embedding.setValue** — changes an embedding's value at one point, swapping with whatever point previously mapped there if occupied. [docstring]
    Logic/Embedding/Basic.lean · richness 8 · bundled · new this revision (old_tmc=0 → new_tmc=4)
14. **Equiv.subtypePreimage** — functions agreeing with a fixed function `x₀` on a subtype are equivalent to functions on the complementary subtype. [docstring]
    Logic/Equiv/Basic.lean · richness 8 · bundled · new this revision (old_tmc=0 → new_tmc=2)
15. **Equiv.piEquivPiSubtypeProd** — splits dependent functions on `α` into a product by separating indices satisfying a predicate from those that don't. [docstring]
    Logic/Equiv/Prod.lean · richness 8 · bundled · was rank 5 (old_tmc=4 → new_tmc=5)
16. **Equiv.ofLeftInverse** — if `f` has a left-inverse (when `α` is nonempty), `α` is computably equivalent to `f`'s range. [docstring]
    Logic/Equiv/Set.lean · richness 7 · bundled · new this revision (old_tmc=0 → new_tmc=2)
17. **Int.leInduction** — induction upward on integers from a lower bound `m`. [inferred from signature; docstring only cross-references a sibling lemma]
    Data/Int/Init.lean · richness 8 · value · new this revision (old_tmc=0 → new_tmc=4)
18. **Int.leInductionDown** — induction downward on integers from an upper bound `m`. [inferred from signature; docstring only cross-references a sibling lemma]
    Data/Int/Init.lean · richness 8 · value · new this revision (old_tmc=0 → new_tmc=2)
19. **Relation.Fibration** — `f` is a fibration between two relations if every related pair in the codomain relation lifts to a related pair in the domain relation via `f`. [docstring]
    Logic/Relation.lean · richness 7 · prop · new this revision (old_tmc=1 → new_tmc=11)
20. **Nat.nthRoot** — the `n`th root of a natural number, computed via Newton's method for fast convergence. [docstring]
    Data/Nat/NthRoot/Defs.lean · richness 7 · value · new this revision (old_tmc=0 → new_tmc=15)
21. **Multiset.noncommFoldr** — folds `f` over a multiset given a proof `f` is left-commutative on the multiset's elements. [docstring]
    Data/Finset/NoncommProd.lean · richness 7 · value · new this revision (old_tmc=0 → new_tmc=4)
22. **Function.extend** — extends a function `g` defined along `f` to the whole codomain, using a junk-value function off `f`'s range. [docstring]
    Logic/Function/Basic.lean · richness 6 · value · was eligible (rank unlisted in revision 1's top 10; richness unaffected)
23. **Equiv.piCongrRight** — a family of pointwise equivalences `∀ a, β₁ a ≃ β₂ a` lifts to an equivalence of the dependent-function types. [docstring]
    Logic/Equiv/Basic.lean · richness 7 · bundled · new this revision (old_tmc=1 → new_tmc=2)
24. **Nat.evenOddRec** — a recursion principle splitting on even/odd: from `P 0` and a step extending `P i` to both `P(2i)` and `P(2i+1)`, get `P n` for all `n`. [docstring]
    Data/Nat/EvenOddRec.lean · richness 6 · value · new this revision (old_tmc=0 → new_tmc=3)
25. **Relation.CutExpand** — the relation specifying valid moves in the "hydra game": removing one head and replacing it with a multiset of strictly-`r`-smaller heads. [docstring]
    Logic/Hydra.lean · richness 5 · prop · new this revision (old_tmc=0 → new_tmc=19)
26. **Finset.strongInduction** — builds a value on every finset from values on all its strict subsets, starting from the empty set. [docstring]
    Data/Finset/Card.lean · richness 6 · value · new this revision (old_tmc=0 → new_tmc=2)
27. **Nat.bitCasesOn** — a non-recursive case-split on the binary representation of a natural number (base case for `Nat.binaryRec`-style recursion). [docstring]
    Data/Nat/BinaryRec.lean · richness 6 · value · new this revision (old_tmc=0 → new_tmc=5)
28. **ArithmeticFunction.dirichletInverseFun** — given an inverse of `f 1`, constructs the Dirichlet inverse of an arithmetic function `f`. [docstring]
    NumberTheory/ArithmeticFunction/Defs.lean · richness 6 · value · new this revision (old_tmc=0 → new_tmc=3)
29. **List.nextOr** — returns the element following `x`'s occurrence in a list, or a default if no such element exists. [docstring]
    Data/List/Cycle.lean · richness 6 · value · new this revision (old_tmc=0 → new_tmc=12)
30. **Equiv.sumCompl** — for a predicate `p` on `α`, the sum of `{a // p a}` and its complement is equivalent to `α`. [docstring]
    Logic/Equiv/Sum.lean · richness 6 · bundled · new this revision (old_tmc=0 → new_tmc=6)
31. **Equiv.sumPiEquivProdPi** — dependent functions on a sum-type index are equivalent to pairs of dependent functions on each summand. [docstring]
    Logic/Equiv/Prod.lean · richness 6 · bundled · new this revision (old_tmc=0 → new_tmc=8)
32. **Function.dcomp** — composition of dependent functions, where the type of the composite depends on both the input and the inner function's output. [docstring]
    Logic/Function/Defs.lean · richness 6 · value · new this revision (old_tmc=0 → new_tmc=2)
33. **Composition.embedding** — embeds the `i`-th block of a composition into `Fin n` at its correct position. [docstring]
    Combinatorics/Enumerative/Composition.lean · richness 6 · bundled · new this revision (old_tmc=0 → new_tmc=12)
34. **finSumNatEquiv** — the equivalence between `Fin n ⊕ ℕ` and `ℕ`. [docstring]
    Logic/Equiv/Fin/Basic.lean · richness 6 · bundled · unchanged
35. **DependsOn** — a function depends only on a set `s` if agreeing on `s` forces agreeing outputs. [docstring]
    Logic/Function/DependsOn.lean · richness 5 · prop · unchanged
36. **Function.Semiconj** — `f` semiconjugates `ga` to `gb` if `f ∘ ga = gb ∘ f`. [docstring]
    Logic/Function/Conjugate.lean · richness 5 · prop · unchanged
37. **Finset.Colex.IsInitSeg** — a family of sets is an initial segment of the colexicographic order if it's downward-closed among same-size sets under colex. [docstring]
    Combinatorics/Colex.lean · richness 5 · prop · new this revision (old_tmc=0 → new_tmc=5)
38. **Nat.psub** — partial subtraction: `psub m n = some k` if `m = n + k`, else `none`. [docstring]
    Data/Nat/PSub.lean · richness 5 · value · new this revision (old_tmc=0 → new_tmc=8)
39. **Directed** — a family is directed w.r.t. a relation if some member sits above any pair in the family. [docstring]
    Order/Directed.lean · richness 5 · prop · unchanged
40. **DirectedOn** — a subset is directed if some element of the set sits above any pair in the set. [docstring]
    Order/Directed.lean · richness 5 · prop · unchanged

*(Ranks 41-256 — including the `Monotone`/`Antitone` family, `Xor`, `Function.prod`, `Finset.pi`, and the rest of revision 1's eligible set plus the remaining newly-recovered candidates — are in the review doc's §6 full ranked table, with old/new mention counts for every row.)*

## Worth a second look

- **`Int.leInduction` (17) and `Int.leInductionDown` (18)** — same concern as batch 3 revision 1's digest: docstrings are only cross-references ("See `Int.inductionOn'`..."), not self-contained descriptions. A dossier author will need to read the signature (or `Int.inductionOn'` itself) directly, same as before this revision.
- **The near-duplicate order-theory and relation-uniqueness clusters** (unchanged from revision 1, see that digest's own "worth a second look" section) — still present, still a curation question, not resolved by this revision's fix.
- **`Finset.pi` (rank 104, not in this digest's top 40)** — worth a direct look in the full table given revision 1 specifically flagged it as a concern; now resolved to eligible, but its exact rank and score are only visible in the review doc's §6, not reproduced in this top-40 slice.
