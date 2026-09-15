## VTask.Rel

### Object

Given a partition `P` of a subset `s` of a type `α`, `VTask.Rel P a b` is the binary relation on `α` that holds for two elements `a` and `b` precisely when they belong to the same part (block) of `P`. In classical terms, it is the equivalence relation whose equivalence classes are exactly the parts of `P`, extended to all of `α` by declaring any two elements outside `s` — or a pair with one member outside `s` — to be unrelated.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Rel : {α : Type u_1} -> {s : Set α} -> (P : Partition s) -> (a b : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> {s : Set α} -> (P : Partition s) -> (a b : α) -> Prop`

The implicit type parameter `α` is the ambient type. The implicit set `s ⊆ α` is the domain being partitioned. The explicit argument `P` is the partition of `s` whose blocks define the relation. The arguments `a` and `b` are the two elements of `α` whose relatedness is being asserted.

### Conventions

When at least one of `a` or `b` lies outside `s`, the relation `VTask.Rel P a b` is always false; the relation is thus irreflexive (and vacuously everything else) outside `s`. Reflexivity `VTask.Rel P a a` holds exactly when `a ∈ s`.

### Worked examples

- Claim: For the discrete partition of a two-element set `{0, 1}` where `{0}` and `{1}` are separate blocks, the elements `0` and `1` are NOT related, but `0` is related to itself.

- Claim: If `P` is any partition of `s` and `P.Rel P a b` holds, then both `a` and `b` are members of `s`.

- Claim: `VTask.Rel P x y` is symmetric: `P.Rel x y ↔ P.Rel y x`.

- Claim: `VTask.Rel P x x ↔ x ∈ s` — reflexivity holds exactly for elements in the partitioned set.

- Claim: If `P.Rel x y` and `P.Rel y z`, then `P.Rel x z` (transitivity).

### Boundaries

- **Elements outside `s`:** For any `a ∉ s`, `VTask.Rel P a a` is false. More generally, if either argument is outside `s`, the relation is false, because no part of `P` can contain an element not in `s`.
- **Elements inside `s`:** Every `a ∈ s` belongs to exactly one part of `P`, so `VTask.Rel P a a` is true, and `VTask.Rel P a b` is true iff `a` and `b` lie in the same block.
- **Coarser vs. finer partitions:** `VTask.Rel P ≤ VTask.Rel Q` (as relations) if and only if `P ≤ Q` as partitions (i.e., `P` is a refinement of `Q`).

### Not to be confused with

- **`Setoid.r` / `Equivalence`:** A setoid relation on `α` is reflexive everywhere; `VTask.Rel P` is only reflexive on `s`, making it a partial equivalence relation rather than a full one.
- **`Partition.partOf`:** `partOf` returns the actual block (as a `Set α`) containing a given element; `VTask.Rel` is the derived boolean-valued (Prop-valued) co-membership predicate, not the block itself.
- **`Set.EqOn`:** `Set.EqOn f g s` compares function values on a set, whereas `VTask.Rel P` compares elements of `α` for block-membership within a partition.