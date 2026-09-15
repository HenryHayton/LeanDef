## Object

Given a binary relation `r` between a set `α` and a set `β`, and a subset `t` of `β`, the **lower polar** of `t` along `r` is the collection of all elements `a` of `α` that `r`-relate to *every* element of `t`. In the language of formal concept analysis, it is the "extent" counterpart to `t`: the largest set of objects that share all attributes in `t`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lowerPolar : {α : Type u_2} -> {β : Type u_3} -> (r : α → β → Prop) -> (t : Set β) -> Set α
<!-- PINNED-SIGNATURE:END -->


`VTask.lowerPolar : {α : Type u_2} -> {β : Type u_3} -> (r : α → β → Prop) -> (t : Set β) -> Set α`

The first (explicit) argument `r` is the binary relation, with elements of `α` on the left and elements of `β` on the right. The second explicit argument `t` is the subset of `β` whose lower polar is to be computed. The result is a subset of `α`.

## Conventions

The operation is total: it is defined for every relation and every subset of `β`, including the empty set. No junk-value conventions are needed beyond observing that the lower polar of the empty set is the entire set `α` (every element of `α` vacuously relates to all elements of `∅`).

## Worked examples

- Claim: For any relation `r`, the lower polar of the empty set equals the whole type `α`.

- Claim: An element `a : α` belongs to `VTask.lowerPolar r {b}` if and only if `r a b` holds.

- Claim: If `t₁ ⊆ t₂` then `VTask.lowerPolar r t₂ ⊆ VTask.lowerPolar r t₁` (the operation is antitone in `t`).

- Claim: For the relation `r : ℕ → ℕ → Prop` defined by `r a b ↔ a ≤ b`, the lower polar of `{3, 5}` is `{a | a ≤ 3}`, i.e., all natural numbers that are ≤ both 3 and 5.

## Boundaries

- **Empty set**: `VTask.lowerPolar r ∅ = Set.univ`. Every element of `α` vacuously satisfies the condition of relating to all members of the empty set.
- **Singleton**: `a ∈ VTask.lowerPolar r {b} ↔ r a b`. Membership in the lower polar of a singleton reduces to a single relation test.
- **Antitonicity**: Enlarging `t` can only shrink (or leave unchanged) the lower polar; the map `t ↦ VTask.lowerPolar r t` is antitone.
- **Closure**: Any set `s ⊆ α` is contained in `VTask.lowerPolar r (VTask.upperPolar r s)`, and applying the two polars in succession is a closure-like (idempotent on closed sets) operation.
- **Swap symmetry**: Swapping the arguments of `r` turns the lower polar into the upper polar and vice versa.

## Not to be confused with

- `VTask.upperPolar`: the *dual* operation — given a subset `s` of `α`, it collects all `b ∈ β` that every element of `s` relates to; the roles of `α` and `β` are exchanged.
- The *annihilator* in linear algebra: superficially similar (collecting objects that "kill" everything in a given set), but defined algebraically via bilinear forms rather than an arbitrary relation.
- The *orthogonal complement* in lattice theory: also uses a polar-style construction, but typically requires a symmetric or self-dual setup rather than a directed relation between two distinct types.