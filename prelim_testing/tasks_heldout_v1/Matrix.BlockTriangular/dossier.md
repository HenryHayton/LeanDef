## VTask.BlockTriangular

### Object

A square matrix `M` with rows and columns indexed by a type `m` is *block triangular with respect to a block-labelling function `b`* when every entry `M i j` that lies strictly *below* the block diagonal is zero. More precisely, if the block index of column `j` is strictly less than the block index of row `i` (in the ordering on the block-index type `α`), then `M i j = 0`. In the classical picture, the matrix has a block-upper-triangular shape: grouping rows and columns by their `b`-value, no nonzero entry can appear in a position whose column-block comes earlier (in the ordering on `α`) than its row-block.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.BlockTriangular : {α : Type u_1} -> {m : Type u_3} -> {R : Type v} -> [LT α] -> [Zero R] -> (M : Matrix m m R) -> (b : m → α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.BlockTriangular : {α : Type u_1} -> {m : Type u_3} -> {R : Type v} -> [LT α] -> [Zero R] -> (M : Matrix m m R) -> (b : m → α) -> Prop`

The implicit type `α` is the type used to index (label) the blocks; it must carry a less-than relation `LT α` so that the relative order of block labels is meaningful. The implicit type `m` is the common index type for rows and columns of the square matrix. The implicit type `R` is the entry type, which must have a zero element. The explicit argument `M` is the square matrix being tested. The explicit argument `b` is the block-labelling function that assigns a block index in `α` to each row (equivalently, column) index in `m`; rows and columns with the same `b`-value belong to the same diagonal block.

### Conventions

The predicate does not require `α` to be linearly ordered or even a partial order — only a bare `LT` relation is needed for the statement. Theorems that derive consequences (e.g., determinant formulas) typically strengthen this to a `LinearOrder`. The zero check is the zero of the ring/semiring `R`; there is no convention for a "junk" output since the definition is a `Prop`.

### Worked examples

- Claim: The 2×2 identity matrix over ℤ, with block labelling `b = id : Fin 2 → Fin 2`, satisfies `VTask.BlockTriangular`.

- Claim: The 2×2 matrix `!![0, 1; 0, 0]` over ℤ, with `b = id`, satisfies `VTask.BlockTriangular`, because the only potentially offending entry is position (1, 0), where `b 0 = 0 < 1 = b 1` would need `M 1 0 = 0`, which holds.

- Claim: The 2×2 matrix `!![0, 0; 1, 0]` over ℤ, with `b = id : Fin 2 → Fin 2`, does NOT satisfy `VTask.BlockTriangular`, because `M 1 0 = 1 ≠ 0` yet `b 0 = 0 < 1 = b 1`.

- Claim: Any diagonal matrix (with off-diagonal entries equal to zero) satisfies `VTask.BlockTriangular` for any choice of block-labelling function `b`, since all off-diagonal entries are zero.

### Boundaries

- When the block-labelling function `b` is constant (all indices mapped to the same block label), the condition `b j < b i` is never satisfied, so every matrix vacuously satisfies `VTask.BlockTriangular`. The matrix is treated as a single block.
- When `b` is injective into a linearly ordered `α` (e.g., `b = id` on `Fin n`), the predicate recovers the classical notion of an upper-triangular matrix: every entry strictly below the main diagonal is zero.
- The predicate concerns only the strict inequality `b j < b i`; entries where `b i = b j` (same block) are completely unconstrained and may be nonzero.
- The entry type `R` only needs `Zero R`; no ring or semiring structure is required for the predicate itself.
- Taking the transpose of a block-triangular matrix yields a matrix that is block triangular with respect to the *order-dual* labelling `toDual ∘ b`, i.e., block-lower-triangular in the original order.

### Not to be confused with

- `Matrix.upperTriangular` / upper-triangular matrices: the special case where `m` is linearly ordered and `b = id`; `VTask.BlockTriangular` generalises this to arbitrary block structures.
- `Matrix.BlockDiagonal`: a block-*diagonal* matrix, where additionally the entries between *distinct* diagonal blocks are also zero (both above and below the block diagonal); `VTask.BlockTriangular` only forces the *lower* off-diagonal blocks to be zero.
- `Matrix.toSquareBlock`: a helper that extracts a single diagonal block from a matrix; it is used in the determinant factorisation theorems for `VTask.BlockTriangular`, but is not the same predicate.