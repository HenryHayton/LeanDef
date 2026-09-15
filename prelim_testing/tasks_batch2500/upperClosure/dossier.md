## Object

Given a preordered set and a subset `s`, `VTask.upperClosure s` is the smallest upper set (upward-closed set) that contains `s`. Concretely, its carrier is the set of all elements `x` for which there exists some `a ∈ s` with `a ≤ x`. It is the "upward shadow" of `s` in the preorder.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.upperClosure : {α : Type u_1} -> [Preorder α] -> (s : Set α) -> UpperSet α
<!-- PINNED-SIGNATURE:END -->


`VTask.upperClosure : {α : Type u_1} -> [Preorder α] -> (s : Set α) -> UpperSet α`

The implicit type parameter `α` is the ambient preordered type. The `Preorder α` instance supplies the ordering relation. The explicit argument `s` is the seed set whose upward closure is being formed.

## Conventions

No special junk-value conventions are declared: the function is total and well-defined for every subset of every preordered type, including the empty set and the full set.

## Worked examples

- Claim: Every element of `s` belongs to `VTask.upperClosure s` (the seed is contained in its own upper closure).

- Claim: For a singleton `{a}` in a preorder, the carrier of `VTask.upperClosure {a}` equals the set of all elements `x` with `a ≤ x`, i.e., it coincides with the principal upper set `UpperSet.Ici a`.

- Claim: If `s` is already an upper set, then `VTask.upperClosure s` (as a set) equals `s` itself — the operation is idempotent on upper sets.

- Claim: For the natural numbers with the usual order, the upper closure of `{3, 7}` contains 10 (since `7 ≤ 10`) but does not contain 2 (since neither 3 nor 7 is ≤ 2).

## Boundaries

- **Empty set**: `VTask.upperClosure ∅` is the empty upper set, since no element `a ∈ ∅` can witness `a ≤ x` for any `x`.
- **Full set**: `VTask.upperClosure Set.univ` is the full upper set (all of `α`), since every `x` has a witness `a = x ∈ Set.univ` with `a ≤ x` by reflexivity.
- **Preorders with non-trivial equivalences**: In a preorder that is not a partial order, `a ≤ b` and `b ≤ a` with `a ≠ b` can both hold; the upper closure still works correctly and includes both `a` and `b` if either is in `s`.
- **Idempotence**: Applying the construction twice does not enlarge the result; the upper closure of an upper set is that set itself.

## Not to be confused with

- `UpperSet.Ici a` — the principal upper set above a single element `a`; `VTask.upperClosure {a}` equals this, but `VTask.upperClosure` handles arbitrary sets.
- `lowerClosure s` — the dual construction producing the smallest *lower* set (downward-closed set) containing `s`.
- `IsUpperSet s` — a predicate asserting that a plain `Set α` is already upward-closed, not the closure operator itself.