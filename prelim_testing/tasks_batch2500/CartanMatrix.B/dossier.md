## Object

`VTask.B n` is the Cartan matrix of the simple Lie algebra of type Bₙ (corresponding to the odd orthogonal Lie algebra so(2n+1)). It is an n×n integer matrix encoding the inner-product data between simple roots of the root system Bₙ. Its rows and columns are indexed by the n simple roots, and its entries record twice the cosine of the angle between (appropriately normalised) root pairs. For n = 1 it coincides with the A₁ Cartan matrix, and for n ≥ 2 it is the unique indecomposable Cartan matrix of type B.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.B : (n : ℕ) -> Matrix (Fin n) (Fin n) ℤ
<!-- PINNED-SIGNATURE:END -->


`(n : ℕ) -> Matrix (Fin n) (Fin n) ℤ`

The single argument `n` is the rank of the root system, i.e., the number of simple roots. The result is an n×n matrix whose rows and columns are both indexed by `Fin n`.

## Conventions

When `n = 0` the matrix is the unique 0×0 matrix (the empty matrix), which is a valid but degenerate case not corresponding to any Lie algebra. The diagonal entries are always 2. For adjacent simple roots where the longer root comes after the shorter one (i.e., when `j = i + 1` and `j = n − 1`, the last node), the entry `(i, j)` is −2, reflecting the asymmetry of the Bₙ Dynkin diagram at the end node. All other off-diagonal entries are either −1 (for adjacent pairs not at the distinguished end) or 0 (for non-adjacent pairs).

## Worked examples

- Claim: `VTask.B 2` equals the 2×2 matrix with rows `[2, −2]` and `[−1, 2]`, confirming the asymmetry characteristic of B₂.
  ```lean
  example : VTask.B 2 = !![2, -2; -1, 2] := by decide
  ```

- Claim: For `VTask.B 3`, the diagonal entries are all 2: `VTask.B 3 0 0 = 2`, `VTask.B 3 1 1 = 2`, `VTask.B 3 2 2 = 2`.
  ```lean
  example : VTask.B 3 0 0 = 2 ∧ VTask.B 3 1 1 = 2 ∧ VTask.B 3 2 2 = 2 := by decide
  ```

- Claim: For `VTask.B 3`, the entry at position (1, 2) (adjacent pair at the long-short boundary) is −2: `VTask.B 3 1 2 = -2`.
  ```lean
  example : VTask.B 3 1 2 = -2 := by decide
  ```

- Claim: For `VTask.B 3`, the entry at position (0, 1) (adjacent interior pair) is −1: `VTask.B 3 0 1 = -1`.
  ```lean
  example : VTask.B 3 0 1 = -1 := by decide
  ```

- Claim: For `VTask.B 3`, the entry at position (0, 2) (non-adjacent pair) is 0: `VTask.B 3 0 2 = 0`.
  ```lean
  example : VTask.B 3 0 2 = 0 := by decide
  ```

- Claim: `VTask.B 1` equals `VTask.A 1` (the rank-1 Cartan matrix, which is `[[2]]`).

## Boundaries

- **n = 0**: The result is the empty 0×0 matrix, a junk value since there is no Lie algebra of type B₀.
- **n = 1**: The matrix is `[[2]]`, the 1×1 Cartan matrix, which coincides with the A₁ Cartan matrix. There is no asymmetry because there is only one node.
- **n = 2**: The first genuinely B-type matrix; B₂ is isomorphic to C₂ as a root system but the matrix here uses the B-convention, with the −2 entry in position (0,1) (upper right).
- **General n ≥ 2**: The matrix is not symmetric — the entry `(n−2, n−1)` is −2 while `(n−1, n−2)` is −1 — reflecting that the last simple root is shorter than the others.

## Not to be confused with

- **`VTask.A n`**: The Cartan matrix of type Aₙ (corresponding to sl(n+1)); it is symmetric with all off-diagonal entries equal to −1 or 0, with no −2 off-diagonal entries.
- **`VTask.C n`**: The Cartan matrix of type Cₙ; it has the same Dynkin diagram shape as Bₙ but with the asymmetry reversed — the −2 entry appears in the lower-left rather than the upper-right.
- **`VTask.D n`**: The Cartan matrix of type Dₙ; it is fully symmetric and has a branching structure at the second-to-last node rather than a long-short edge.