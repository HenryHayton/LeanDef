## Object

`VTask.Pairwise R s` is the proposition that the sequence `s` is *pairwise related* by `R`: for every pair of positions `i < j`, if position `i` holds value `x` and position `j` holds value `y`, then `R x y` holds. Informally, every element appearing earlier in the sequence is `R`-related to every element appearing later. This generalises classical list-pairwise-disjointness, strict sortedness, and distinctness to the setting of potentially-infinite lazy sequences (`Seq`).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Pairwise : {α : Type u} -> (R : α → α → Prop) -> (s : Stream'.Seq α) -> Prop
<!-- PINNED-SIGNATURE:END -->


The first argument `R` is the binary relation on elements of type `α` that must hold between every earlier–later pair. The second argument `s` is the lazy sequence (a `Stream'.Seq`) whose elements are being tested.

## Conventions

For positions `i` and `j` where `s.get? i` or `s.get? j` returns `none` (i.e. the sequence has terminated before that index), the universal quantification over the corresponding element is vacuously true, so those index pairs impose no constraint. In particular, the empty sequence and any single-element sequence trivially satisfy `VTask.Pairwise R` for every `R`.

## Worked examples

- Claim: `VTask.Pairwise R nil` holds for every relation `R` and every type, because there are no elements to relate.

- Claim: For the sequence `[1, 2, 3]` (finite), `VTask.Pairwise (· < ·) [1, 2, 3]` holds, since `1 < 2`, `1 < 3`, and `2 < 3`.

- Claim: `VTask.Pairwise (· < ·) [1, 3, 2]` does **not** hold, because position 1 holds `3` and position 2 holds `2`, but `¬ (3 < 2)`.

- Claim: `VTask.Pairwise (· ≠ ·) s` asserts that `s` contains no duplicate elements (every element at an earlier index differs from every element at a later index).

- Claim: If `VTask.Pairwise R s` holds, then `VTask.Pairwise R s.tail` also holds (the property is inherited by the tail of the sequence).

## Boundaries

- **Empty sequence (`nil`)**: `VTask.Pairwise R nil` is always true; there are no index pairs `i < j` with elements present.
- **Singleton sequence `cons hd nil`**: Always satisfies `VTask.Pairwise R` for any `R`, since there is no pair of distinct filled positions.
- **Infinite sequences**: The definition quantifies over all natural-number indices, so for an infinite sequence `VTask.Pairwise R s` is a genuinely infinite conjunction; it cannot in general be decided by finite computation.
- **Asymmetric relations**: `VTask.Pairwise R` is *not* symmetric in the elements — it only requires `R x y` when `x`'s index is strictly smaller than `y`'s, not vice versa. So `VTask.Pairwise (· < ·)` asserts strict increase, not merely that all pairs are comparable.
- **Dropping a prefix**: If `VTask.Pairwise R s` holds, then for any `n`, `VTask.Pairwise R (s.drop n)` holds as well.

## Not to be confused with

- `List.Pairwise`: the analogous predicate for finite `List`s; `VTask.Pairwise` extends this notion to the lazy `Seq` type, which can be infinite.
- `Stream'.Seq.Sorted` or similar order predicates: sortedness for sequences is a special case of `VTask.Pairwise (· ≤ ·)` or `VTask.Pairwise (· < ·)`, but `VTask.Pairwise` is strictly more general (works for any `R`).
- A *pointwise* property: `VTask.Pairwise R s` is about *pairs* of elements at different positions, not a property of each element individually.