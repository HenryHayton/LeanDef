## Object

`VTask.Pairwise s r` is the proposition that a binary relation `r` holds between every two *distinct* elements of a set `s`. Concretely, it asserts: for all `x` and `y` belonging to `s`, if `x ≠ y`, then `r x y`. This is the set-indexed analogue of saying "the relation holds pairwise on `s`."

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Pairwise : {α : Type u_1} -> (s : Set α) -> (r : α → α → Prop) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Pairwise : {α : Type u_1} -> (s : Set α) -> (r : α → α → Prop) -> Prop`

The implicit type argument `α` is the ambient type whose elements populate the set. The first explicit argument `s` is the set of elements over which the pairwise condition is required to hold. The second explicit argument `r` is the binary relation that must hold between every two distinct members of `s`.

## Conventions

The distinctness condition `x ≠ y` is built into the statement: reflexive pairs (where `x = y`) are excluded from the obligation, so `VTask.Pairwise s r` places no requirement on `r x x` for any `x ∈ s`. When the relation `r` is reflexive, the distinctness guard is redundant, and `VTask.Pairwise s r` is equivalent to requiring `r a b` for *all* (not just distinct) pairs in `s`.

## Worked examples

- Claim: `VTask.Pairwise ∅ r` holds vacuously for any relation `r`, because there are no elements in the empty set to form pairs from.

- Claim: `VTask.Pairwise {1, 2, 3} (· < ·)` does NOT hold, because `3 < 1` fails even though both belong to the set and `3 ≠ 1`.

- Claim: `VTask.Pairwise {1, 2, 3} (· ≠ ·)` holds, because any two distinct natural numbers in the set are indeed unequal to each other.

- Claim: `VTask.Pairwise (Set.univ : Set Unit) (· = ·)` holds, because `Set.univ` on `Unit` contains only the single element `()`, so there are no two *distinct* elements to check.

- Claim: If `s = {a}` is a singleton, then `VTask.Pairwise s r` holds for any relation `r`, vacuously (no two distinct elements exist).

## Boundaries

- **Empty set**: `VTask.Pairwise ∅ r` is vacuously true for every `r`, since the universal quantifier ranges over an empty domain.
- **Singleton set**: `VTask.Pairwise {a} r` is vacuously true for every `r`, since no two distinct elements are available.
- **Reflexive relations**: When `r` is reflexive, the `x ≠ y` guard is redundant and `VTask.Pairwise s r` becomes equivalent to requiring `r x y` for all `x y ∈ s` without any distinctness side condition.
- **Antisymmetric vs. symmetric relations**: `VTask.Pairwise s r` does NOT require `r y x` to hold whenever `r x y` holds unless `r` itself is symmetric. For asymmetric or non-symmetric relations, both directions are independently checked.
- **Subsets**: If `VTask.Pairwise s r` holds and `t ⊆ s`, then `VTask.Pairwise t r` also holds, since any pair of distinct elements in `t` is also a pair in `s`.

## Not to be confused with

- `Pairwise r` (the global, set-free version): asserts `r i j` for all `i ≠ j` over the *entire* type, not restricted to a set `s`.
- `Set.PairwiseDisjoint s f`: a specialization where `r` is `Disjoint` composed with a function `f`; syntactic sugar for `VTask.Pairwise s (Disjoint on f)`.
- `Finset.Pairwise`: the analogous notion for `Finset` rather than `Set`; uses finite membership instead of set membership, but expresses the same pairwise distinctness condition.
