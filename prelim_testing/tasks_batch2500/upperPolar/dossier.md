## Object

Given a binary relation `r` between two types `α` and `β`, and a set `s` of elements of `α`, the **upper polar** of `s` is the set of all elements `b : β` such that `r a b` holds for every `a` in `s`. In other words, it collects every `β`-element that is related (via `r`) to *all* members of `s` simultaneously. This construction is one half of the Galois connection that underlies formal concept analysis.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.upperPolar : {α : Type u_2} -> {β : Type u_3} -> (r : α → β → Prop) -> (s : Set α) -> Set β
<!-- PINNED-SIGNATURE:END -->


`VTask.upperPolar : {α : Type u_2} -> {β : Type u_3} -> (r : α → β → Prop) -> (s : Set α) -> Set β`

The first implicit argument is the source type `α`; the second implicit argument is the target type `β`. The explicit argument `r` is the binary relation from `α` to `β` that specifies when an `α`-element and a `β`-element are "compatible". The argument `s` is the subset of `α` whose upper polar is being computed. The result is the subset of `β` consisting of all elements compatible with every element of `s`.

## Conventions

When `s` is the empty set, every `β`-element trivially satisfies the universal condition, so the upper polar of `∅` is all of `β` (i.e., `Set.univ`). No other junk-value conventions are declared.

## Worked examples

- Claim: An element `b` belongs to `VTask.upperPolar r s` if and only if `r a b` holds for every `a ∈ s`.

- Claim: `VTask.upperPolar r ∅ = Set.univ` — when the input set is empty, the upper polar is the entire target type.

- Claim: For a singleton set `{a}`, `b ∈ VTask.upperPolar r {a}` if and only if `r a b` holds directly.

- Claim: `VTask.upperPolar r` is antitone: if `s₁ ⊆ s₂` then `VTask.upperPolar r s₂ ⊆ VTask.upperPolar r s₁`. Enlarging the set of constraints can only shrink (or keep equal) the set of elements satisfying all of them.

- Claim: For any set `s : Set α`, the set `s` is contained in `lowerPolar r (VTask.upperPolar r s)` — applying the lower polar to the upper polar recovers at least the original set.

## Boundaries

- **Empty input set**: `VTask.upperPolar r ∅ = Set.univ`. The vacuous universal quantifier is satisfied by every element, so the polar is the whole type.
- **Antitonicity**: Adding more elements to `s` imposes more conditions, so the upper polar can only shrink. In particular `VTask.upperPolar r` is antitone as a function on `Set α`.
- **Galois connection**: `t ⊆ VTask.upperPolar r s` if and only if `s ⊆ lowerPolar r t`. This adjunction means the upper polar and lower polar form a Galois connection between `Set α` and `Set β`.
- **Closure operator**: Applying lower polar then upper polar (or vice versa) yields a closure operator; every set is contained in its double polar.
- **Swapped relation**: The upper polar of `s` along `r` equals the lower polar of `s` along the swapped relation `swap r`.

## Not to be confused with

- **`lowerPolar r t`**: The *lower* polar, which takes a set `t : Set β` and returns the set of all `a : α` related by `r` to every element of `t` — the direction of the relation and the ambient type are reversed.
- **The concept intent/extent**: `IsIntent r t` and `IsExtent r s` assert that a set is *already* fixed by the double-polar operation; the upper polar itself is just the single application that maps `s` to a subset of `β`.
- **The image of a relation**: `Relation.image r s` collects all `b` related to *some* element of `s`, whereas the upper polar collects `b` related to *all* elements of `s`.