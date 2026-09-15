## VTask.A

### Object

For a natural number `n`, `VTask.A n` is the **Cartan matrix of type Aₙ₋₁**, the `n × n` integer matrix associated with the Dynkin diagram of the special linear Lie algebra `sl(n)` (equivalently, the root system of type Aₙ₋₁ when `n ≥ 2`). Its rows and columns are indexed by `Fin n`. The matrix encodes the inner-product data among the simple roots of the root system: diagonal entries are all 2 (the self-pairing of each simple root with itself), entries for adjacent indices in the natural linear order are −1 (reflecting the single bond between consecutive nodes of the Aₙ₋₁ Dynkin diagram), and all other entries are 0.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.A : (n : ℕ) -> Matrix (Fin n) (Fin n) ℤ
<!-- PINNED-SIGNATURE:END -->


`(n : ℕ) -> Matrix (Fin n) (Fin n) ℤ`

The sole argument `n` is the **size** of the matrix, i.e., the number of rows (and columns). The resulting Cartan matrix has rank `n − 1` as a root system and corresponds to the Lie type Aₙ₋₁; thus `n = 2` gives the rank-1 system A₁, `n = 3` gives A₂, etc.

### Conventions

The matrix size parameter is `n`, not the rank: the Cartan matrix of type Aₙ₋₁ is returned as an `n × n` matrix, so the rank of the system is one less than the argument. At `n = 0` the matrix is the unique `0 × 0` empty matrix (the vacuous Cartan matrix). At `n = 1` the matrix is the `1 × 1` matrix `!![2]`, corresponding to the trivial rank-0 root system (or, by convention, the degenerate single-node Dynkin diagram).

### Worked examples

- Claim: `VTask.A 1 = !![2]`
  ```lean
  example : VTask.A 1 = !![2] := by decide
  ```

- Claim: `VTask.A 2 = !![ 2, -1; -1,  2]`
  ```lean
  example : VTask.A 2 = !![ 2, -1; -1,  2] := by decide
  ```

- Claim: `VTask.A 3 = !![ 2, -1,  0; -1,  2, -1;  0, -1,  2]`
  ```lean
  example : VTask.A 3 = !![ 2, -1,  0; -1,  2, -1;  0, -1,  2] := by decide
  ```

- Claim: `VTask.A n` is symmetric (i.e., equal to its own transpose) for every `n`.

- Claim: `VTask.A n` is simply laced (all off-diagonal entries are 0 or −1) for every `n`.

- Claim: For any `i ≠ j : Fin n`, the entry `VTask.A n i j ≤ 0`.

### Boundaries

- **`n = 0`**: The matrix is the `0 × 0` empty matrix; all matrix statements hold vacuously.
- **`n = 1`**: The matrix is `!![2]`, a single diagonal entry. There are no off-diagonal entries, so the Dynkin diagram has one node with no edges — this is the degenerate (rank-0) case.
- **`n = 2`**: Gives the standard A₁ Cartan matrix `!![2, -1; -1, 2]` (rank 1), the smallest non-trivial case. Note the docstring convention: the Lie-theoretic rank is `n − 1`.
- **Diagonal entries**: Always exactly 2, for every `n` and every index `i : Fin n`.
- **Adjacent off-diagonal entries** (indices differing by exactly 1 in the natural order): Always exactly −1.
- **Non-adjacent off-diagonal entries**: Always exactly 0.

### Not to be confused with

- **`VTask.B`, `VTask.C`, `VTask.D`**: Cartan matrices of the other classical Lie types (Bₙ, Cₙ, Dₙ); they share the tridiagonal backbone with `VTask.A` but differ in specific boundary entries.
- **The identity matrix or the "all-twos" diagonal matrix**: `VTask.A n` has −1 entries flanking the diagonal, not a pure diagonal matrix.
- **The adjacency matrix of the path graph Aₙ₋₁**: The adjacency matrix of the path graph has 0 on the diagonal and 1 for adjacent pairs; `VTask.A n` replaces the 0-diagonal with 2 and the 1-adjacencies with −1.