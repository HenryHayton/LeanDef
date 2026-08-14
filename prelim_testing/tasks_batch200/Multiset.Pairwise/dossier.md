## Object

`VTask.Pairwise r m` is the proposition that the elements of the multiset `m` can be arranged into a list such that the binary relation `r` holds for every pair of distinct positions in that list (i.e., the list satisfies `List.Pairwise r`). In other words, there is some enumeration of the multiset's elements where every earlier element is related by `r` to every later element.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Pairwise : {α : Type u_1} -> (r : α → α → Prop) -> (m : Multiset α) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.Pairwise : {α : Type u_1} -> (r : α → α → Prop) -> (m : Multiset α) -> Prop
```

The type `α` is the implicit element type of the multiset. The first explicit argument `r` is the binary relation to be checked pairwise among the elements. The second explicit argument `m` is the multiset whose elements are being tested.

## Conventions

The empty multiset vacuously satisfies `VTask.Pairwise r 0` for any relation `r`, since the empty list witnesses the existential with `List.Pairwise r []` holding trivially.

## Worked examples

- Claim: `VTask.Pairwise (· ≠ ·) (0 : Multiset ℕ)` holds, because the empty multiset trivially satisfies pairwise inequality.

- Claim: `VTask.Pairwise (· < ·) ({1, 2, 3} : Multiset ℕ)` holds, witnessed by the list `[1, 2, 3]` on which `<` is pairwise satisfied.

- Claim: `VTask.Pairwise (· ≠ ·) ({1, 1} : Multiset ℕ)` does NOT hold, because any list permutation of `{1, 1}` contains the repeated element `1`, violating pairwise inequality.

- Claim: `VTask.Pairwise (· ≠ ·) s ↔ Multiset.Nodup s` for any multiset `s : Multiset α`, connecting pairwise inequality with the standard no-duplicates predicate.

## Boundaries

- **Empty multiset**: `VTask.Pairwise r 0` is always true, for any `r`.
- **Singleton multiset**: `VTask.Pairwise r {a}` is always true, as a single-element list has no two distinct positions to check.
- **Relation symmetry**: The definition asks for a list witness, so the ordering of the list matters. For a symmetric relation `r`, one can show that if any permutation of `m` satisfies `List.Pairwise r`, then all permutations do, making the predicate independent of the chosen list representative.
- **Non-symmetric relations**: For a non-symmetric `r`, `VTask.Pairwise r m` depends on the existence of at least one ordering of the multiset's elements satisfying `List.Pairwise r`; not every permutation need work.

## Not to be confused with

- `_root_.Pairwise r` (the set/function-indexed version): states that `r i j` holds for all distinct indices `i ≠ j` in some index type, unrelated to multisets.
- `Multiset.Nodup`: the special case `VTask.Pairwise (· ≠ ·)`, which asserts no element appears more than once; `VTask.Pairwise` generalises this to arbitrary relations.
- `List.Pairwise r l`: the list-level predicate requiring `r` between every earlier and later element; `VTask.Pairwise r m` lifts this to multisets by existentially quantifying over list representations of `m`.