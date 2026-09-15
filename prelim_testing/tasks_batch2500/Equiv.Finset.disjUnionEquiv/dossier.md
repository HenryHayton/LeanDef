## Object

`VTask.disjUnionEquiv` is a canonical bijection (equivalence of types) between the disjoint sum of two finset subtypes and the subtype of their disjoint union. Given two disjoint finite sets `s` and `t` inside a type `α`, every element of `s ⊕ t` (a tagged element that belongs to one set or the other) corresponds uniquely and naturally to an element of `s.disjUnion t h` (an element known to belong to their union), and vice versa.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.disjUnionEquiv : {α : Type u_1} -> [DecidableEq α] -> (s t : Finset α) -> (h : Disjoint s t) -> ↥s ⊕ ↥t ≃ ↥(s.disjUnion t h)
<!-- PINNED-SIGNATURE:END -->


`VTask.disjUnionEquiv : {α : Type u_1} -> [DecidableEq α] -> (s t : Finset α) -> (h : Disjoint s t) -> ↥s ⊕ ↥t ≃ ↥(s.disjUnion t h)`

The implicit type parameter `α` is the ambient type whose elements populate the finsets. The `DecidableEq α` instance is needed for finset operations. The first explicit argument `s` and the second `t` are the two finite sets being combined. The argument `h` is the proof that `s` and `t` are disjoint (i.e., share no common elements), which is required to form their disjoint union. The result is an equivalence whose domain is the coproduct (sum type) of the two subtypes `↥s` and `↥t`, and whose codomain is the subtype `↥(s.disjUnion t h)`.

## Conventions

There are no junk-value conventions to declare: the equivalence is total and every input combination is meaningful. `DecidableEq` is a typeclass argument supplied automatically by instance search in normal usage.

## Worked examples

- Claim: Applying `VTask.disjUnionEquiv` to `Sum.inl x`, where `x : ↥s`, produces the element `⟨x.val, _⟩` in `↥(s.disjUnion t h)` with membership witnessed by `x` being in `s`.

- Claim: Applying `VTask.disjUnionEquiv` to `Sum.inr y`, where `y : ↥t`, produces the element `⟨y.val, _⟩` in `↥(s.disjUnion t h)` with membership witnessed by `y` being in `t`.

- Claim: The inverse `(VTask.disjUnionEquiv s t h).symm`, applied to an element `⟨i, hi'⟩` where `i ∈ s`, returns `Sum.inl ⟨i, _⟩`.

- Claim: The inverse `(VTask.disjUnionEquiv s t h).symm`, applied to an element `⟨i, hi'⟩` where `i ∈ t`, returns `Sum.inr ⟨i, _⟩`.

- Claim: For any disjoint `s t : Finset α` and element `x : ↥s ⊕ ↥t`, the round-trip `(VTask.disjUnionEquiv s t h).symm (VTask.disjUnionEquiv s t h x) = x` holds, confirming the equivalence is a true bijection.

## Boundaries

- If either `s` or `t` is the empty finset, the equivalence still holds. For `s = ∅`, the left injection `Sum.inl` has an empty domain, so the equivalence degenerates to an isomorphism between `↥t` (embedded via `Sum.inr`) and `↥(∅.disjUnion t h)`, which is naturally `↥t`.
- The disjointness hypothesis `h` is essential: the construction `s.disjUnion t h` in Mathlib is only well-typed when `h : Disjoint s t` is supplied, so the equivalence does not exist without it.
- When `s` and `t` are equal (which forces them both to be empty for disjointness to hold), the equivalence is a bijection between the two-sided empty sum and the empty subtype.
- The underlying carrier map sends `Sum.inl ⟨a, ha⟩` to `⟨a, mem_disjUnion.mpr (Or.inl ha)⟩` and `Sum.inr ⟨b, hb⟩` to `⟨b, mem_disjUnion.mpr (Or.inr hb)⟩`; membership proofs may differ propositionally but are equal via proof irrelevance.

## Not to be confused with

- `Finset.disjUnion`: the finset operation itself that produces `s ∪ t` under a disjointness hypothesis; `VTask.disjUnionEquiv` is the *equivalence of types* relating the sum of subtypes to the subtype of that union.
- `Equiv.sumCompl`: an equivalence between `↥s ⊕ ↥sᶜ` and the whole type `α`; it splits on a set and its complement rather than two disjoint finsets.
- `Finset.union_comm` / `Finset.disjUnion_comm`: lemmas about commutativity of the finset union, not about the subtype equivalence.
