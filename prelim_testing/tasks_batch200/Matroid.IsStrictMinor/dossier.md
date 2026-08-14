## VTask.IsStrictMinor

### Object

A matroid `N` is a **strict minor** of a matroid `M` if `N` is a minor of `M` but `M` is not a minor of `N`; equivalently, `N` can be obtained from `M` by deleting and/or contracting subsets of the ground set that are not both simultaneously empty (so the operation is genuinely non-trivial, making `N` strictly smaller than `M`). This is the strict analogue of the minor relation, forming the strict part of the partial order on matroids induced by the minor (≤m) relation.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsStrictMinor : {α : Type u_1} -> (N M : Matroid α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsStrictMinor : {α : Type u_1} -> (N M : Matroid α) -> Prop`

The implicit type argument `α` is the common element type of both matroids. The first explicit argument `N` is the candidate strict minor — the matroid being tested for strict subordinacy. The second explicit argument `M` is the ambient matroid — the one from which `N` would be derived by deletion and contraction.

### Conventions

The notation `N <m M` is used throughout Mathlib as an infix abbreviation for `VTask.IsStrictMinor N M`, mirroring the standard `<` symbol for strict orders. The relation is irreflexive (no matroid is a strict minor of itself) and transitive, and it coincides with the strict part of the matroid minor partial order, so `N <m M` is equivalent to `N ≤m M ∧ N ≠ M`.

### Worked examples

- Claim: If `N <m M`, then the ground set of `N` is a strict subset of the ground set of `M` (i.e., `N.E ⊂ M.E`).

- Claim: If `N <m M`, then `N ≠ M`.

- Claim: If `N <m M` and `M <m M'`, then `N <m M'` (transitivity).

- Claim: If `N <m M`, then `N ≤m M` (every strict minor is in particular a minor).

- Claim: No matroid `M` satisfies `M <m M` (irreflexivity follows from `¬ (M ≤m M ∧ ¬ M ≤m M)`).

### Boundaries

- **Irreflexivity**: `VTask.IsStrictMinor M M` is always false, because the minor relation is a partial order (reflexive), so one cannot have both `M ≤m M` and `¬ M ≤m M` simultaneously.
- **Ground-set shrinkage**: Whenever `N <m M`, the ground set of `N` is a *proper* subset of the ground set of `M`. In particular `N` and `M` cannot have equal ground sets unless their rank functions also differ in the appropriate way — but the ground set always strictly shrinks.
- **Asymmetry**: If `N <m M`, then `M <m N` is false, since the minor relation is antisymmetric.
- **Relation to equality**: `N <m M` implies `N ≠ M`; conversely, `N ≤m M` and `N ≠ M` together imply `N <m M`.

### Not to be confused with

- **`Matroid.IsMinor` (`N ≤m M`)**: The non-strict minor relation; allows `N = M` (i.e., deletion and contraction of empty sets). `VTask.IsStrictMinor` adds the requirement that the minor is proper.
- **`N < M` (the strict order on `Matroid α`)**: This is definitionally equal to `VTask.IsStrictMinor N M` (as recorded by `lt_eq_isStrictMinor`), but one may encounter it written as a strict inequality rather than using the `<m` notation.
- **`N.E ⊂ M.E` (strict subset of ground sets)**: A necessary consequence of `N <m M`, but not sufficient — matroids with the same ground set can still be related by `<m` if one is obtained from the other by a non-trivial contraction followed by deletion that returns to the same carrier set.