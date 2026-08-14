## Object

`VTask.sumAssoc α β γ` is the canonical type-theoretic associativity equivalence for the coproduct (disjoint union) of three types. It witnesses the bijection between `(α ⊕ β) ⊕ γ` (left-associated) and `α ⊕ (β ⊕ γ)` (right-associated), packaging both directions together with proofs that each is the inverse of the other. Concretely, an element tagged as being from `α` (via `inl (inl a)`) or from `β` (via `inl (inr b)`) or from `γ` (via `inr c`) is re-tagged according to the right-associated bracket.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sumAssoc : (α : Type u_9) -> (β : Type u_10) -> (γ : Type u_11) -> (α ⊕ β) ⊕ γ ≃ α ⊕ β ⊕ γ
<!-- PINNED-SIGNATURE:END -->


`VTask.sumAssoc : (α : Type u_9) -> (β : Type u_10) -> (γ : Type u_11) -> (α ⊕ β) ⊕ γ ≃ α ⊕ β ⊕ γ`

The first argument `α` is the leftmost summand type. The second argument `β` is the middle summand type. The third argument `γ` is the rightmost summand type. Together they determine the equivalence between the left-associated and right-associated bracketing of their coproduct.

## Conventions

The notation `α ⊕ β ⊕ γ` on the right-hand side of the equivalence is right-associated by Lean's parsing conventions, meaning it stands for `α ⊕ (β ⊕ γ)`. No junk-value conventions apply since the equivalence is total and every element of the domain type uniquely matches exactly one of three constructor patterns.

## Worked examples

- Claim: Applying `VTask.sumAssoc α β γ` to `inl (inl a)` yields `inl a`.
  (The left-of-left element maps to the leftmost injection in the right-associated form.)

- Claim: Applying `VTask.sumAssoc α β γ` to `inl (inr b)` yields `inr (inl b)`.
  (The left-of-right element maps to the right injection of the left injection in the right-associated form.)

- Claim: Applying `VTask.sumAssoc α β γ` to `inr c` yields `inr (inr c)`.
  (The right element maps to the doubly-right injection in the right-associated form.)

- Claim: The inverse `(VTask.sumAssoc α β γ).symm` applied to `inl a` yields `inl (inl a)`.

- Claim: The inverse `(VTask.sumAssoc α β γ).symm` applied to `inr (inl b)` yields `inl (inr b)`.

- Claim: The inverse `(VTask.sumAssoc α β γ).symm` applied to `inr (inr c)` yields `inr c`.

## Boundaries

- The equivalence is defined for all types `α`, `β`, `γ`, including empty types (`Empty`, `PEmpty`), unit-like types, and any universe level combination. There are no restrictions.
- When any of the three types is empty, the equivalence still holds; the corresponding constructors simply have no inhabitants, and the bijection on the remaining elements is trivially correct.
- The equivalence is its own structural inverse in the sense that `(VTask.sumAssoc α β γ).symm` is exactly the right-to-left direction, which is also a total function.

## Not to be confused with

- `Equiv.sumComm`: the *commutativity* equivalence `α ⊕ β ≃ β ⊕ α`, which swaps the two summands rather than re-associating three.
- `Homeomorph.sumAssoc`: the same re-association but living in the category of topological spaces as a homeomorphism; it has additional continuity data bundled alongside the set-level bijection.
- `Equiv.sumCongr`: an equivalence that applies separate equivalences to the two summands of a binary coproduct, not a re-associating of three summands.