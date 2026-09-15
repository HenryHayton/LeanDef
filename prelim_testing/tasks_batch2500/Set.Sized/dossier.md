## VTask.Sized

### Object

`VTask.Sized r A` is the property that every finite set belonging to the family `A` has exactly `r` elements. In combinatorics this is called a **uniform** (or **r-uniform**) set family: all members have the same cardinality `r`. The predicate is vacuously true when `A` is empty.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Sized : {α : Type u_1} -> (r : ℕ) -> (A : Set (Finset α)) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.Sized : {α : Type u_1} -> (r : ℕ) -> (A : Set (Finset α)) -> Prop
```

The implicit type parameter `α` is the ground type whose elements populate the finsets. The first explicit argument `r` is the required size (cardinality) that every member of the family must have. The second explicit argument `A` is the family of finite sets (a `Set` of `Finset α`) being tested for uniformity.

### Conventions

When `A` is the empty family (no finsets at all), `VTask.Sized r A` holds for every `r`, because the universal quantification over members is vacuously satisfied.

### Worked examples

**Membership regime**

- Claim: The family `{∅}` (containing only the empty finset) satisfies `VTask.Sized 0 {∅}`, since the empty finset has cardinality 0.

- Claim: If `s : Finset α` has `#s = 3`, then the singleton family `{s}` satisfies `VTask.Sized 3 {s}`.

- Claim: The powerset-card construction `powersetCard r s`, viewed as a set of finsets, satisfies `VTask.Sized r (powersetCard r s)`, because every element of `powersetCard r s` is a finset of size exactly `r`.

- Claim: The family `{{1}, {1,2}}` (over `ℕ`) does **not** satisfy `VTask.Sized 1 {{1}, {1,2}}` because `{1,2}` has cardinality 2, not 1.

**Global structural regime**

- Claim: If `A ⊆ B` and `VTask.Sized r B`, then `VTask.Sized r A` (monotonicity: every subfamily of a uniform family is uniform at the same rank).

- Claim: `VTask.Sized r (A ∪ B)` holds if and only if both `VTask.Sized r A` and `VTask.Sized r B` hold.

- Claim: A family satisfying `VTask.Sized r A` is an antichain with respect to inclusion, because two distinct finsets of the same size cannot be related by strict inclusion.

- Claim: If `VTask.Sized r A` then the shadow `∂ A` satisfies `VTask.Sized (r - 1) (∂ A)`.

### Boundaries

- **Empty family**: `VTask.Sized r ∅` holds for all `r` (vacuous truth).
- **Rank 0**: The only finset of size 0 is `∅`; so `VTask.Sized 0 A` implies `A ⊆ {∅}`, and in fact `A.Subsingleton` holds.
- **Full rank over a `Fintype`**: If `α` is a `Fintype` and `VTask.Sized (Fintype.card α) A`, then `Finset.univ` is the only finset of that size, so `A` is either empty or the singleton `{Finset.univ}`, giving `A.Subsingleton`.
- **Shadow at rank 0**: Because natural-number subtraction is used, taking the shadow of a `VTask.Sized 0 A` family gives `VTask.Sized (0 - 1) = VTask.Sized 0`, which is consistent with the shadow of a family of empty sets being empty.

### Not to be confused with

- **`Finset.card`**: This is the cardinality of a single finset, not a property of a family of finsets.
- **`Set.Finite`**: This asserts that a set (or family) has finitely many elements, unrelated to the sizes of those elements.
- **`IsAntichain`**: While every `VTask.Sized r` family is automatically an antichain under inclusion, `IsAntichain` is a weaker property that does not require all members to have equal size.