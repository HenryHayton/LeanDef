## VTask.HasOrthogonalRows

### Object

A predicate on a matrix `A` (with entries in a type equipped with multiplication and an additive commutative monoid structure) asserting that every pair of *distinct* rows of `A` is orthogonal to each other. Two rows are orthogonal when their dot product — the sum of entry-wise products — equals zero. A matrix with this property is said to have **orthogonal rows**.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.HasOrthogonalRows : {α : Type u_1} -> {n : Type u_2} -> {m : Type u_3} -> [Mul α] -> [AddCommMonoid α] -> (A : Matrix m n α) -> [Fintype n] -> Prop
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> {n : Type u_2} -> {m : Type u_3} -> [Mul α] -> [AddCommMonoid α] -> (A : Matrix m n α) -> [Fintype n] -> Prop`

The scalar type `α` must support both multiplication and an additive commutative monoid structure so that the dot product of two row vectors can be formed and compared to zero. The type `n` indexes the *columns* of `A` (and must be a `Fintype` so the finite sum in the dot product is well-defined). The type `m` indexes the *rows* of `A`. The matrix `A : Matrix m n α` is the object being tested.

### Conventions

When `m` has at most one element (i.e., the matrix has zero or one rows), the predicate holds vacuously, since there are no two *distinct* rows to test.

### Worked examples

- Claim: The 2×2 identity matrix over ℝ satisfies `VTask.HasOrthogonalRows`, because row 0 is (1,0) and row 1 is (0,1), whose dot product is 0.

- Claim: The 2×2 all-ones matrix over ℝ does **not** satisfy `VTask.HasOrthogonalRows`, because the dot product of row 0 and row 1 is 1·1 + 1·1 = 2 ≠ 0.

- Claim: A matrix `A` satisfies `VTask.HasOrthogonalRows` if and only if `A * Aᵀ` is a diagonal matrix (i.e., has zero off-diagonal entries).

- Claim: If `Aᵀ` satisfies `VTask.HasOrthogonalRows`, then `A` has orthogonal *columns*.

### Boundaries

- If `m` is empty (no rows), the universal quantifier over pairs of distinct rows is vacuously true; every such matrix has orthogonal rows.
- If `m` is a singleton type (exactly one row), there are again no two distinct rows, so the condition is vacuously true.
- If `n` is empty (no columns), every row is the zero vector; dot products are empty sums that equal zero, so the predicate holds.
- The predicate does **not** require rows to be unit vectors (normalised); it only requires mutual orthogonality, not orthonormality.
- The predicate is symmetric in the two row indices: checking that row `i₁` is orthogonal to row `i₂` for all `i₁ ≠ i₂` automatically includes both orderings.

### Not to be confused with

- **`HasOrthogonalCols`**: the analogous predicate asserting that every pair of distinct *columns* is orthogonal; note that `A.HasOrthogonalRows ↔ Aᵀ.HasOrthogonalCols`.
- **Orthogonal matrix** (in the sense `A * Aᵀ = I`): that notion additionally requires the row norms to equal 1 (orthonormality), which `HasOrthogonalRows` alone does not.
- **`IsDiag`**: a predicate on square matrices saying off-diagonal entries are zero; related but applies to matrices directly, not via their row dot products (though `(A * Aᵀ).IsDiag ↔ A.HasOrthogonalRows`).