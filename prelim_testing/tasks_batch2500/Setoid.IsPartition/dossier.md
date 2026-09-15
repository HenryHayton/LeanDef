## VTask.IsPartition

### Object

`VTask.IsPartition c` is a proposition asserting that the collection `c` of subsets of a type `α` forms a **partition** of `α`. Concretely, this means two things hold simultaneously: (1) the empty set is not one of the pieces (every piece is nonempty), and (2) every element `a : α` belongs to exactly one piece in `c` (existence and uniqueness of the piece containing `a`).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsPartition : {α : Type u_1} -> (c : Set (Set α)) -> Prop
<!-- PINNED-SIGNATURE:END -->


The single argument `c` is a collection (a set of sets) of subsets of the ambient type `α`. It is the candidate partition whose pieces are to be verified: one checks whether those pieces are pairwise disjoint, cover all of `α`, and none of them is empty.

### Conventions

The type parameter `α` is implicit and inferred from the element type of `c`. There are no junk-value conventions declared for this definition: the predicate is a straightforward `Prop` that is simply false when the conditions are not met, so no special out-of-domain behavior needs to be specified.

### Worked examples

- Claim: The collection `{{0,1}, {2}}` is a partition of `Fin 3` (each element belongs to exactly one piece and no piece is empty).

- Claim: The collection of equivalence classes of any setoid on `α` satisfies `VTask.IsPartition`, i.e., `VTask.IsPartition r.classes` holds for any `Setoid α`.

- Claim: The collection `{∅, {0}}` is **not** a partition of `Fin 2`, because the empty set is a member of the collection.

- Claim: If `VTask.IsPartition c` holds, then the union `⋃₀ c` equals `Set.univ`, meaning the pieces cover all of `α`.

- Claim: If `VTask.IsPartition c` holds, then the pieces in `c` are pairwise disjoint: distinct pieces have empty intersection.

### Boundaries

- The empty collection `∅ : Set (Set α)` does **not** satisfy `VTask.IsPartition` when `α` is nonempty, because no element of `α` can belong to any piece (the unique-membership condition fails). For the empty type `α = Empty`, the empty collection vacuously satisfies the unique-membership condition, and it trivially avoids containing `∅`, so `VTask.IsPartition (∅ : Set (Set Empty))` holds.
- A collection containing the empty set never satisfies `VTask.IsPartition`, regardless of the other pieces.
- A collection consisting of a single piece `{Set.univ}` satisfies `VTask.IsPartition` if and only if `α` is nonempty (otherwise `Set.univ = ∅` would be that single piece, and `∅ ∉ c` would fail).
- Overlapping pieces never satisfy `VTask.IsPartition`: if two distinct sets in `c` share an element, the uniqueness condition for that element fails.

### Not to be confused with

- `Set.PairwiseDisjoint`: asserts only that the pieces in a collection are pairwise disjoint, without requiring that they cover `α` or that they are all nonempty.
- `Finpartition`: a finitely-indexed partition structure in Mathlib, carrying combinatorial data; `VTask.IsPartition` is a bare `Prop` on an arbitrary `Set (Set α)` without finiteness assumptions.
- `Setoid` (an equivalence relation on `α`): while every setoid induces a partition via its equivalence classes, `VTask.IsPartition` lives at the level of the collection of classes, not the relation itself.