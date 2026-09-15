## Object

`VTask.C n` is the Cartan matrix of type Cₙ, the integer square matrix of size n×n encoding the root-system data of the symplectic Lie algebra sp(2n). Its diagonal entries are all 2 (as required of any Cartan matrix), its immediate super-diagonal entries are −1, its immediate sub-diagonal entries are −1 except in the last row where the entry just below the diagonal is −2, and all remaining entries are 0. The asymmetry in the last row reflects the one short simple root of the Cₙ root system.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.C : (n : ℕ) -> Matrix (Fin n) (Fin n) ℤ
<!-- PINNED-SIGNATURE:END -->


`(n : ℕ) -> Matrix (Fin n) (Fin n) ℤ`

The single argument `n` is the rank of the root system, i.e., the number of simple roots; the resulting matrix is n×n with integer entries indexed by `Fin n`.

## Conventions

At rank 0 the matrix is the unique 0×0 empty matrix (vacuously satisfying all row/column conditions). At rank 1 the resulting 1×1 matrix `[[2]]` coincides with the Cartan matrix of type A₁, since a single-node diagram has no off-diagonal entries to distinguish the two types.

## Worked examples

- Claim: `VTask.C 2` equals the 2×2 matrix with rows [2, −1] and [−2, 2].
  ```lean
  example : VTask.C 2 = !![2, -1; -2, 2] := by decide
  ```

- Claim: The diagonal entry `VTask.C n i i = 2` for any rank `n` and any index `i : Fin n`.

- Claim: The super-diagonal entry `VTask.C 3 ⟨0, by omega⟩ ⟨1, by omega⟩ = -1`.
  ```lean
  example : VTask.C 3 ⟨0, by omega⟩ ⟨1, by omega⟩ = -1 := by decide
  ```

- Claim: The sub-diagonal entry in the last row of `VTask.C 3` is −2, i.e., `VTask.C 3 ⟨2, by omega⟩ ⟨1, by omega⟩ = -2`.
  ```lean
  example : VTask.C 3 ⟨2, by omega⟩ ⟨1, by omega⟩ = -2 := by decide
  ```

- Claim: `VTask.C 1 = VTask.C 1` in the sense that rank-1 type-C equals the rank-1 type-A Cartan matrix (both are `[[2]]`).

## Boundaries

- **n = 0**: The matrix is the 0×0 empty matrix over ℤ; there are no indices to evaluate.
- **n = 1**: The only entry is the diagonal `(0,0)` entry equal to 2; there are no off-diagonal entries, so the sub-diagonal −2 rule never applies, and the matrix coincides with the A₁ Cartan matrix.
- **Last-row sub-diagonal**: For any n ≥ 2, the entry at row n−1 (the last row) and column n−2 is −2 (not −1), distinguishing type C from type B and type A.
- **All off-diagonal entries are ≤ 0**: No off-diagonal entry is positive, consistent with the general requirement for Cartan matrices.
- **Non-symmetry**: For n ≥ 2 the matrix is not symmetric (the (n−1, n−2) entry is −2 while the (n−2, n−1) entry is −1), in contrast to type-A Cartan matrices.

## Not to be confused with

- **Type-B Cartan matrix (`VTask.B n`)**: Also has a distinguished entry of −2 near the last row, but the asymmetry appears in the super-diagonal (first row or column) rather than the sub-diagonal last row.
- **Type-A Cartan matrix (`VTask.A n`)**: Fully symmetric tridiagonal Cartan matrix with all off-diagonal nonzero entries equal to −1; coincides with `VTask.C 1` only at rank 1.
- **The symplectic group generator matrix**: `VTask.C n` is an integer combinatorial matrix (Cartan matrix), not the standard skew-symmetric matrix J used to define the symplectic form on ℝ²ⁿ.