## Object

A family of elements of a type `α`, indexed by a sort `ι` and given by a function `f : ι → α`, is **directed** with respect to a binary relation `r` on `α` if for every pair of indices `x` and `y` in `ι` there exists a third index `z` such that both `f x` and `f y` stand in the relation `r` to `f z`. Informally, any two members of the family have a common upper bound (where "upper" is measured by `r`) somewhere else in the family.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Directed : {α : Type u_1} -> {ι : Sort u_3} -> (r : α → α → Prop) -> (f : ι → α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Directed : {α : Type u_1} -> {ι : Sort u_3} -> (r : α → α → Prop) -> (f : ι → α) -> Prop`

The type `α` is the ambient type whose elements the family lives in. The sort `ι` is the index type (or sort) used to parametrise the family. The argument `r` is the binary relation on `α` that serves as the "dominance" or "above" relation (playing the role of `≼`). The argument `f` is the family itself: the function mapping each index to an element of `α`.

## Conventions

There are no declared junk-value or boundary conventions for this definition: it is a universally-quantified proposition, and is simply `False` (vacuously fails or genuinely fails) when the relevant witnesses do not exist, and `True` when they do. No special values are assigned to degenerate inputs.

## Worked examples

- Claim: The constant family `f : ι → α` with `f i = a` for all `i` is directed with respect to any reflexive relation `r`, because every pair trivially has the element `a` itself as a common bound.

- Claim: For `ι = ℕ` and `f = id : ℕ → ℕ`, the family is directed with respect to `(· ≤ ·)`, since for any `x y : ℕ` we can take `z = max x y`, giving `f x ≤ f z` and `f y ≤ f z`.

- Claim: A single-element family `f : Fin 1 → α` (where `f 0 = a`) is directed with respect to any relation `r` that is reflexive at `a`, because the only pair is `(0, 0)` and we can pick `z = 0`.

- Claim: The family `f : Bool → ℕ` given by `f false = 0` and `f true = 1` is directed with respect to `(· ≤ ·)` since for any pair we may take `z = true` and use `0 ≤ 1` and `1 ≤ 1`.

## Boundaries

- When `ι` is an empty type (no indices), the statement `∀ x y, ∃ z, ...` is vacuously true, so every binary relation makes the empty family directed.
- When `r` is the empty relation (always `False`), directedness fails for any family that has at least one element, since no `z` can satisfy the required conditions.
- When `ι` has exactly one element, directedness reduces to: there exists `z` such that `f * ≼ f z` and `f * ≼ f z`, which holds iff `f *` relates to some member of the family under `r` — in particular it holds whenever `r` is reflexive.
- Directedness is not a symmetric condition on `r`: it explicitly asks for upper bounds, not lower bounds.

## Not to be confused with

- `DirectedOn`: the variant where the family is described by a set `S : Set α` rather than an indexed function `f : ι → α`; it asserts that every two elements of `S` have an upper bound in `S`.
- `IsDirected`: a typeclass asserting that an entire type `α` (with a relation `r`) is directed, i.e., every two elements of `α` have a common upper bound in `α` — no indexing family is involved.
- `DirectedSystem`: a stronger structure used in direct limits, requiring the family to be compatible with a directed preorder on the index type via specified transition maps, not just the existence of common upper-bound indices.