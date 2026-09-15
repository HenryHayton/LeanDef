## 1. Object

A set `s` in a type `α` is **bounded** with respect to a binary relation `r` if there exists a single element `a : α` (called an upper bound, or witness) such that every element of `s` relates to `a` via `r`. In other words, `s` is contained in the set of all elements that `r`-precede `a`. This is a purely relational notion of boundedness: `a` need not itself belong to `s`, and `r` need not be a preorder or have any special properties.

The term "final" alludes to the order-theoretic usage where one says a set is "finally" or "eventually" bounded when it has a cofinal bound in the given direction.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Bounded : {α : Type u} -> (r : α → α → Prop) -> (s : Set α) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.Bounded : {α : Type u} -> (r : α → α → Prop) -> (s : Set α) -> Prop
```

The implicit type argument `α` is the ambient type whose elements populate the set and serve as the potential witness. The first explicit argument `r` is the binary relation on `α` that determines the direction of boundedness: an element `b` of `s` is considered "bounded by `a`" when `r b a` holds. The second explicit argument `s` is the set whose boundedness is being asserted.

## 3. Conventions

The definition is total: it is meaningful for every relation `r` and every set `s`, including the empty set and the full universe. No junk-value conventions are required.

## 4. Worked examples

- Claim: The set `{n : ℕ | n < 5}` is bounded with respect to `(· ≤ ·)`, witnessed by `5`.

- Claim: The empty set `(∅ : Set ℕ)` is bounded with respect to any relation, since the existential is vacuously satisfied by any witness.

- Claim: For any element `a : α` and relation `r`, the set `{b | r b a}` (the set of all elements that `r`-precede `a`) is bounded with respect to `r`, witnessed by `a` itself.

- Claim: The interval `Iio a` (the strict downward ray below `a` in a preorder) is bounded with respect to `(· < ·)`, witnessed by `a`.

- Claim: If `s ⊆ t` and `t` is bounded with respect to `r`, then `s` is also bounded with respect to `r`.

## 5. Boundaries

- **Empty set**: `∅` is always `VTask.Bounded r ∅` for any relation `r`, because the existential `∃ a, ∀ b ∈ ∅, r b a` is trivially satisfied — the inner universal is vacuously true for any choice of `a`.
- **Whole type (`Set.univ`)**: `VTask.Bounded r Set.univ` holds if and only if the entire type `α` has an element `a` such that every element of `α` relates to `a` via `r`. For a strict linear order on `ℕ` this fails (there is no largest natural number), but it holds for a type with a top element.
- **Singleton sets**: A singleton `{b}` is always `VTask.Bounded r {b}` when there exists any `a` with `r b a`; in particular it fails if `b` has no `r`-successor at all.
- **Relation strengthening**: If `r ≤ r'` pointwise (i.e., `r b a → r' b a` for all `b, a`) and `s` is bounded for `r`, it is also bounded for `r'`.

## 6. Not to be confused with

- **`Bornology.IsBounded`**: A bornological notion of boundedness defined via a bornology structure on a topological or metric space; unrelated to any fixed binary relation.
- **`Set.Nonempty` + order-boundedness**: In a lattice or preorder, one sometimes speaks of a set having an upper bound in the order-theoretic sense; `VTask.Bounded (· ≤ ·) s` coincides with this when `r` is `(· ≤ ·)`, but the definition here works for arbitrary relations with no order axioms.
- **`BddAbove` / `BddBelow`**: Mathlib's `BddAbove s` asserts `(upperBounds s).Nonempty` in a preorder, which is equivalent to `VTask.Bounded (· ≤ ·) s` but is phrased differently and tied to the `Preorder` typeclass.