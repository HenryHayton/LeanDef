## Object

`VTask.blockDiagonal M` assembles a family of matrices `M`, indexed by a type `o`, into a single large block-diagonal matrix. Concretely, it places the matrix `M k` as the `k`-th diagonal block, and fills all off-diagonal positions with zero. The result has row index type `m × o` and column index type `n × o`: a pair `(i, k)` selects row `i` within block `k`, and similarly for columns.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.blockDiagonal : {m : Type u_2} -> {n : Type u_3} -> {o : Type u_4} -> {α : Type u_12} -> [DecidableEq o] -> [Zero α] -> (M : o → Matrix m n α) -> Matrix (m × o) (n × o) α
<!-- PINNED-SIGNATURE:END -->


`VTask.blockDiagonal : {m : Type u_2} -> {n : Type u_3} -> {o : Type u_4} -> {α : Type u_12} -> [DecidableEq o] -> [Zero α] -> (M : o → Matrix m n α) -> Matrix (m × o) (n × o) α`

The implicit types `m`, `n`, and `o` are the row-index type, column-index type, and block-index type of the family, respectively. `α` is the scalar type of the matrices. The `DecidableEq o` instance is needed to decide, for any two block indices, whether they are equal (to determine if an entry falls on or off the diagonal). The `Zero α` instance supplies the zero scalar used to fill off-diagonal blocks. The explicit argument `M` is the family of matrices being assembled: for each block index `k : o`, `M k` is an `m`-by-`n` matrix that will appear as the `k`-th diagonal block.

## Conventions

Off-diagonal entries (those at row `(i, k)` and column `(j, k')` with `k ≠ k'`) are set to `0`, the zero of the scalar type `α`. There is no junk value for the on-diagonal case; the entry at `(i, k)` and `(j, k)` is exactly `M k i j`.

## Worked examples

- Claim: For a family `M : Fin 2 → Matrix (Fin 2) (Fin 2) ℤ`, the entry at row `(0, 0)` and column `(1, 0)` equals `M 0 0 1` (same block, on-diagonal block entry).

- Claim: For any family `M : Fin 2 → Matrix (Fin 2) (Fin 2) ℤ`, the entry at row `(0, 0)` and column `(1, 1)` equals `0` (different block indices, so off-diagonal).

- Claim: `VTask.blockDiagonal` is injective: if two families produce the same block-diagonal matrix, then the families are equal.

- Claim: For the constant family `fun (_ : Fin 3) => B`, the block-diagonal matrix has three copies of `B` along the diagonal and zeros elsewhere.

## Boundaries

- When `o` is empty (a type with no inhabitants), the result is a matrix with row type `m × o` and column type `n × o`, both of which are also empty, so the matrix is vacuously the unique such matrix.
- When `o` has exactly one element, the result is essentially the single matrix `M` (up to the trivial product with a one-element type), with no off-diagonal blocks.
- When `m` or `n` is empty, each block `M k` is an empty matrix, and the entire result is likewise an empty matrix.
- The zero scalar used for off-diagonal entries is determined solely by the `Zero α` instance; no ring structure is assumed.

## Not to be confused with

- `Matrix.blockDiagonal'`: the heterogeneous variant where each block may have a different size (indexed by dependent types); use that when block dimensions vary.
- `Matrix.diagonal`: places a vector of scalars on the diagonal of a square matrix; `VTask.blockDiagonal` generalises this to blocks of matrices rather than scalar entries.
- `Matrix.fromBlocks`: assembles a fixed 2×2 arrangement of four matrix blocks into one matrix; `VTask.blockDiagonal` handles an arbitrary indexed family of same-sized diagonal blocks.