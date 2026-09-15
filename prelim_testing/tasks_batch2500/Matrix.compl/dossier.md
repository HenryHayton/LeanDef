## VTask.compl

### Object

For a square matrix `A` over a type `α` with distinguished elements `0` and `1`, `A.compl` is the matrix whose `(i, j)` entry is `0` when `i = j` (the diagonal is identically zero), `1` when `i ≠ j` and `A i j = 0` (the two vertices are not connected in the original graph), and `0` when `i ≠ j` and `A i j ≠ 0` (the two vertices are connected in the original graph). In graph-theoretic terms, if `A` is the adjacency matrix of a simple graph on vertex set `V`, then `A.compl` is the adjacency matrix of its complement graph: an edge is present in the complement precisely when it is absent in the original, with no self-loops.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.compl : {α : Type u_1} -> {V : Type u_2} -> [Zero α] -> [One α] -> [DecidableEq α] -> [DecidableEq V] -> (A : Matrix V V α) -> Matrix V V α
<!-- PINNED-SIGNATURE:END -->


`VTask.compl : {α : Type u_1} -> {V : Type u_2} -> [Zero α] -> [One α] -> [DecidableEq α] -> [DecidableEq V] -> (A : Matrix V V α) -> Matrix V V α`

The implicit type `α` is the entry type of the matrix, which must have a zero element and a one element (supplied by the `Zero α` and `One α` instances). Decidable equality on `α` is needed to test whether an entry equals zero, and decidable equality on `V` is needed to test whether two vertex indices are equal. The explicit argument `A` is the input square matrix — typically an adjacency matrix of a simple graph — whose complement matrix is being formed.

### Conventions

All diagonal entries of `A.compl` are `0`, regardless of the diagonal of `A`. Off-diagonal entries of `A.compl` are `1` when the corresponding entry of `A` is `0`, and `0` otherwise; in particular, if an off-diagonal entry of `A` is any nonzero value (not just `1`), the complement records `0` at that position.

### Worked examples

- Claim: For the 3×3 zero matrix over `ℕ`, `(0 : Matrix (Fin 3) (Fin 3) ℕ).compl 0 1 = 1` (off-diagonal entry of the zero matrix complements to 1).
  ```lean
  example : (0 : Matrix (Fin 3) (Fin 3) ℕ).compl 0 1 = 1 := by decide
  ```

- Claim: For the 3×3 zero matrix over `ℕ`, `(0 : Matrix (Fin 3) (Fin 3) ℕ).compl 0 0 = 0` (diagonal entry is always 0).
  ```lean
  example : (0 : Matrix (Fin 3) (Fin 3) ℕ).compl 0 0 = 0 := by decide
  ```

- Claim: For a 2×2 all-ones matrix `J` over `ℕ` (where `J i j = 1` for all `i j`), the complement `J.compl` is the zero matrix, since every entry is either on the diagonal (set to 0) or a nonzero entry off the diagonal (set to 0).
  ```lean
  example : (Matrix.of (fun _ _ => (1 : ℕ)) : Matrix (Fin 2) (Fin 2) ℕ).compl = 0 := by decide
  ```

- Claim: Every entry of `A.compl` is either `0` or `1` — the complement matrix always has values in `{0, 1}`, matching the `compl_apply` theorem.

- Claim: If `A` is a symmetric adjacency matrix, then `A.compl` is also symmetric, since the zero-test `A i j = 0` is symmetric whenever `A` is symmetric.

### Boundaries

- **Diagonal**: The diagonal of `A.compl` is uniformly `0`, no matter what values appear on the diagonal of `A`. This enforces the convention that graphs have no self-loops.
- **Non-binary inputs**: If `A` contains off-diagonal entries that are neither `0` nor `1` (e.g., `2`), those entries are treated as "present edges" (nonzero), so the complement records `0` there. The output always lies in `{0, 1}`.
- **1×1 matrices**: On a single-vertex type, the only entry is the diagonal `(0, 0)`, which `A.compl` sets to `0`; the complement of any single-vertex graph is the empty graph.
- **Empty vertex type**: When `V` is uninhabited, `A.compl` is vacuously the empty matrix.
- **Involution on adjacency matrices**: Applying `compl` twice to a genuine adjacency matrix (symmetric, zero diagonal, entries in `{0, 1}`) recovers the original matrix.

### Not to be confused with

- **`Matrix.adjMatrix`**: converts a `SimpleGraph` to a `{0,1}`-valued matrix; `VTask.compl` works the other direction, transforming a matrix into the complement's adjacency matrix.
- **The Schur complement** (`Matrix.schur_complement_eq₁₁`): an algebraic construction for block matrices involving matrix inverses — entirely unrelated to graph complementation.
- **`SimpleGraph.compl`** (or `SimpleGraph.complement`): the complement operation on the `SimpleGraph` type itself, which operates on the graph structure rather than on its matrix representation.