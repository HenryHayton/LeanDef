## Object

`VTask.sumCompl p` is a canonical equivalence (bijection) between the disjoint sum (coproduct) of the subtype `{ a // p a }` (elements satisfying `p`) and the complementary subtype `{ a // ¬ p a }` (elements not satisfying `p`), on one side, and the full type `α` on the other side. Informally, it witnesses the fact that every element of `α` either satisfies the predicate or does not, and these two cases are disjoint and exhaustive — so the disjoint union of the two subtypes is in bijection with `α` itself.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sumCompl : {α : Type u_9} -> (p : α → Prop) -> [DecidablePred p] -> { a // p a } ⊕ { a // ¬p a } ≃ α
<!-- PINNED-SIGNATURE:END -->


`VTask.sumCompl : {α : Type u_9} -> (p : α → Prop) -> [DecidablePred p] -> { a // p a } ⊕ { a // ¬p a } ≃ α`

The implicit argument `α` is the ambient type whose elements are being classified. The argument `p` is the decidable predicate on `α` that partitions it into two complementary subtypes. The instance argument `[DecidablePred p]` provides the means to decide, for any given element `a : α`, whether `p a` holds or not; this is required to define the inverse map.

## Conventions

The forward direction of the equivalence maps a tagged element `Sum.inl ⟨a, ha⟩` (an element satisfying `p`) or `Sum.inr ⟨a, ha⟩` (an element not satisfying `p`) to the underlying element `a : α` in both cases, simply forgetting the tag and proof. The inverse direction maps an element `a : α` to `Sum.inl ⟨a, h⟩` if `p a` holds (with `h : p a`), and to `Sum.inr ⟨a, h⟩` if `¬ p a` (with `h : ¬ p a`), using decidability to branch.

## Worked examples

- Claim: Applying `VTask.sumCompl` to `Sum.inl x` (where `x : { a // p a }`) returns the underlying value `↑x : α`.

- Claim: Applying `VTask.sumCompl` to `Sum.inr y` (where `y : { a // ¬ p a }`) returns the underlying value `↑y : α`.

- Claim: For the predicate `p = (· < 3)` on `Fin 5`, the inverse of `VTask.sumCompl p` applied to `(3 : Fin 5)` sends it into the right (`Sum.inr`) component, since `¬ (3 < 3)`.

- Claim: For the predicate `p = (· < 3)` on `Fin 5`, the inverse of `VTask.sumCompl p` applied to `(2 : Fin 5)` sends it into the left (`Sum.inl`) component, since `2 < 3`.

- Claim: `VTask.sumCompl` is an equivalence, so applying it and then its inverse yields the identity on `{ a // p a } ⊕ { a // ¬p a }`.

## Boundaries

- If `α` is the empty type, both subtypes are empty, the sum is empty, and the equivalence is the unique (vacuous) bijection between two empty types.
- If `p` is the always-true predicate, then `{ a // p a } ≅ α` and `{ a // ¬ p a }` is empty; the sum still bijects with `α`, with every element landing in the left (`inl`) component under the inverse.
- If `p` is the always-false predicate, the situation is symmetric: `{ a // p a }` is empty and every element maps to the right (`inr`) component under the inverse.
- The `DecidablePred p` instance is needed only for the inverse direction; the forward map is unconditionally defined.

## Not to be confused with

- `subtypeOrEquiv`: a more general equivalence for pairs of predicates `p`, `q` that are complementary (`IsCompl`), rather than always taking `q = ¬ p`.
- `Equiv.Set.sumCompl`: the set-theoretic analogue, which states that the disjoint union of a set `s` and its set-complement `sᶜ` is equivalent to the whole type, phrased using set membership rather than subtype predicates.
- `Equiv.sumCongr`: a different construction that maps a sum type to another sum type by applying separate equivalences to each summand, with no complementation involved.