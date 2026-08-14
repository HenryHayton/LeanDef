## Object

`VTask.DirectedOn r s` is the proposition that the set `s` is *directed* with respect to the binary relation `r`. Concretely, it asserts that for every pair of elements `x`, `y` belonging to `s`, there exists a third element `z` also in `s` that is `r`-above both `x` and `y` (i.e., `x r z` and `y r z` both hold). This is the standard notion of a directed set as encountered in order theory, topology (nets), and category theory.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.DirectedOn : {α : Type u_1} -> (r : α → α → Prop) -> (s : Set α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.DirectedOn : {α : Type u_1} -> (r : α → α → Prop) -> (s : Set α) -> Prop`

The implicit type argument `α` is the ambient type whose elements populate the set. The explicit argument `r` is the binary relation playing the role of the ordering or preorder on `α`; it need not be reflexive, transitive, or antisymmetric for the predicate to be stated (though in practice it is usually a preorder). The explicit argument `s` is the subset of `α` being tested for directedness: the predicate asks whether every finite upper bound query within `s` can be resolved by some element already in `s`.

## Conventions

There are no declared junk-value conventions for this predicate: it is a universally quantified proposition over all pairs in `s`, and when `s` is empty the statement is vacuously true (since there are no pairs `x ∈ s`, `y ∈ s` to witness). No special sentinel values or out-of-domain behaviors are defined.

## Worked examples

- Claim: `VTask.DirectedOn (· ≤ ·) (Set.univ : Set ℕ)` holds, since for any two natural numbers `m` and `n` the element `max m n` is in `Set.univ` and is above both.

- Claim: `VTask.DirectedOn (· ⊆ ·) { s : Set ℕ | s ⊆ {0, 1} }` holds, because for any two subsets `A` and `B` of `{0, 1}` that lie in the family, their union `A ∪ B` is also a subset of `{0, 1}` and contains both.

- Claim: The empty set satisfies `VTask.DirectedOn r ∅` for any relation `r` on any type, because the universal quantifier over elements of `∅` is vacuously true.

- Claim: `VTask.DirectedOn (· ≤ ·) {(1 : ℤ), -1}` does not hold, since neither `1 ≤ -1` nor `-1 ≤ 1` is witnessed by an element of the set above both (the only candidates are `1` and `-1`, and `-1 ≤ 1` but `1 ≤ 1` holds while `-1 ≤ -1` holds, yet neither element is above both simultaneously in ℤ's linear order — actually `1` is above both, so this family is directed). Corrected example: `VTask.DirectedOn (· < ·) ({(0 : ℤ)} : Set ℤ)` fails because no element of the singleton is strictly above `0` itself.

## Boundaries

- **Empty set**: `VTask.DirectedOn r ∅` is vacuously true for any relation `r`, since there are no elements to provide a counterexample.
- **Singleton**: `VTask.DirectedOn r {a}` requires `∃ z ∈ {a}, a r z ∧ a r z`, i.e., `a r a`. Thus a singleton is directed if and only if `a` is related to itself under `r` (i.e., `r` is reflexive at `a`). If `r` is irreflexive, a singleton may *fail* to be directed.
- **Total relations**: If `r` is a total relation on `α` (every two elements are comparable), then every subset of `α` is directed under `r`.
- **Upward closure not required**: `VTask.DirectedOn` does not require the set `s` to be an upper set or a filter; it only requires that upper bounds exist *within* `s`.

## Not to be confused with

- **`Directed r f`**: directedness of a *function* (or a family indexed by some type), rather than of a subset; `VTask.DirectedOn` is the set-theoretic version.
- **`IsDirected α r`**: a typeclass asserting that the *entire type* `α` is directed under `r`, rather than a specific subset.
- **`DirectedSystem`**: a functor-style notion of a directed system of objects and morphisms used in algebra and homological algebra, unrelated to this predicate.