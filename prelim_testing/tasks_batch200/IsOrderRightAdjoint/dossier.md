## Object

`VTask.IsOrderRightAdjoint f g` is the proposition asserting that `g : β → α` is an *order right adjoint* for `f : α → β`. Concretely, this means: for every element `y` of `β`, the value `g y` is a least upper bound of the set `{x ∈ α | f x ≤ y}`. In other words, `g y` simultaneously (i) lies above every `x` for which `f x ≤ y`, and (ii) is itself the smallest such upper bound. This is a purely order-theoretic notion of adjointness, closely related to (but more elementary than) the categorical concept of an adjoint functor between posets.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsOrderRightAdjoint : {α : Type u_1} -> {β : Type u_2} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> (g : β → α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsOrderRightAdjoint : {α : Type u_1} -> {β : Type u_2} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> (g : β → α) -> Prop`

The type `α` is the source type of `f` (and the target type of `g`), equipped with a preorder. The type `β` is the target type of `f` (and the source type of `g`), also equipped with a preorder. The argument `f` is the "left" function whose fibres over each `y` are the sets whose least upper bounds are sought. The argument `g` is the candidate right adjoint: for each `y : β`, `g y` must be the least upper bound of `{x | f x ≤ y}`.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a universally-quantified `Prop` over all `y : β` with no distinguished edge inputs, and Lean's `IsLUB` handles the full generality including empty fibres.

## Worked examples

- Claim: If `α` is a `CompleteSemilatticeSup` and `f : α → β` is any function, then the function sending `y` to `sSup {x | f x ≤ y}` is an order right adjoint for `f`.

- Claim: If `g₁` and `g₂` are both order right adjoints for the same `f : α → β` and `α` is a partial order, then `g₁ = g₂` (the right adjoint is unique).

- Claim: Any order right adjoint function `g` is monotone: if `y₁ ≤ y₂` in `β`, then `g y₁ ≤ g y₂` in `α`.

- Claim: If `h : VTask.IsOrderRightAdjoint f g` and `e : β ≃o γ` is an order isomorphism, then `VTask.IsOrderRightAdjoint (e ∘ f) (g ∘ e.symm)`.

## Boundaries

- **Empty fibres.** When `{x | f x ≤ y}` is empty for some `y`, the least upper bound condition reduces to requiring that `g y` be the least element of `α` (i.e., a bottom element), since every element trivially upper-bounds the empty set and `g y` must be below all of them. If `α` has no bottom element, then `VTask.IsOrderRightAdjoint f g` may fail to hold for such `f` unless a suitable bottom exists.
- **Preorder vs. partial order.** Over a mere preorder on `α`, right adjoints need not be unique (two different elements can be mutually `≤`-related without being equal). Uniqueness is guaranteed only when `α` is a partial order.
- **Existence.** The predicate says nothing about whether a right adjoint exists; it only characterises what it means *to be* one. In complete sup-semilattices the canonical candidate `y ↦ sSup {x | f x ≤ y}` always satisfies the predicate.

## Not to be confused with

- **`GaloisConnection`**: A Galois connection `l ⊣ u` requires both `l x ≤ y ↔ x ≤ u y`, a symmetric two-sided characterisation; `VTask.IsOrderRightAdjoint` is a one-sided, least-upper-bound formulation that is equivalent but stated differently.
- **`IsLUB`**: The building block predicate used pointwise; `VTask.IsOrderRightAdjoint f g` says `g y` satisfies `IsLUB {x | f x ≤ y}` for *every* `y`, not just a single chosen element.
- **`OrderIso`**: An order isomorphism is a bijective order-preserving map with order-preserving inverse; a right adjoint need be neither injective nor surjective.