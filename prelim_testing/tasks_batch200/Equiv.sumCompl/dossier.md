## Object

`VTask.sumCompl p` is a canonical equivalence (bijection) between the disjoint union `{ a // p a } ⊕ { a // ¬ p a }` and the type `α` itself. Informally: every element of `α` either satisfies the predicate `p` or its negation, and these two cases are mutually exclusive and exhaustive, so the coproduct of the two corresponding subtypes is in natural bijection with `α`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sumCompl : {α : Type u_9} -> (p : α → Prop) -> [DecidablePred p] -> { a // p a } ⊕ { a // ¬p a } ≃ α
<!-- PINNED-SIGNATURE:END -->


`VTask.sumCompl : {α : Type u_9} -> (p : α → Prop) -> [DecidablePred p] -> { a // p a } ⊕ { a // ¬p a } ≃ α`

The type parameter `α` is the ambient type whose elements are being partitioned. The argument `p` is the predicate that splits `α` into two complementary subtypes: elements satisfying `p` and elements not satisfying `p`. The instance `[DecidablePred p]` provides the computational evidence needed to decide, for any given element of `α`, which side of the partition it belongs to.

## Conventions

The forward direction of the equivalence (from the sum type to `α`) simply forgets the subtype witness: both `Sum.inl ⟨a, h⟩` and `Sum.inr ⟨a, h⟩` map to the underlying element `a`. The inverse direction sends an element `a : α` to `Sum.inl ⟨a, h⟩` when `p a` holds (with `h : p a`) and to `Sum.inr ⟨a, h⟩` when `¬ p a` holds (with `h : ¬ p a`), using the decidability instance to make this choice computationally.

## Worked examples

- Claim: Applying `VTask.sumCompl` to `Sum.inl x` (where `x : { a // p a }`) returns `x.val`.

- Claim: Applying `VTask.sumCompl` to `Sum.inr x` (where `x : { a // ¬ p a }`) returns `x.val`.

- Claim: The inverse of `VTask.sumCompl (fun n : Fin 4 => n.val < 2)` applied to `⟨3, by decide⟩` is `Sum.inr ⟨⟨3, by decide⟩, by decide⟩`.

- Claim: The inverse of `VTask.sumCompl (fun n : Fin 4 => n.val < 2)` applied to `⟨1, by decide⟩` is `Sum.inl ⟨⟨1, by decide⟩, by decide⟩`.

## Boundaries

- When `α` is empty, both subtypes `{ a // p a }` and `{ a // ¬ p a }` are empty, so their sum is also empty, and the equivalence holds trivially.
- When `p` is always true (i.e., `∀ a, p a`), the subtype `{ a // ¬ p a }` is empty and the equivalence reduces to a bijection from `{ a // p a }` to `α`.
- When `p` is always false (i.e., `∀ a, ¬ p a`), the subtype `{ a // p a }` is empty and the equivalence reduces to a bijection from `{ a // ¬ p a }` to `α`.
- The equivalence is definitionally well-behaved: the round-trip in both directions is the identity.

## Not to be confused with

- `subtypeOrEquiv`: a more general equivalence for sums of subtypes `{ x // p x }` and `{ x // q x }` where `p` and `q` need not be complementary predicates.
- `Equiv.Set.sumCompl`: the set-theoretic analogue, stated for sets `s` and `sᶜ` in `Set α` rather than for predicates and their negations at the type level.
- `Equiv.sumCongr`: combines two independent equivalences on summand types, but does not merge a disjoint union into a base type.