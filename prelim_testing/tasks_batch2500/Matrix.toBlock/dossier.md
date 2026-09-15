## Object

`VTask.toBlock M p q` extracts the submatrix of `M` whose rows are exactly those indices satisfying the predicate `p` and whose columns are exactly those indices satisfying the predicate `q`. The result is a matrix indexed by the subtypes `{a // p a}` and `{a // q a}`, and each entry of the block matrix equals the corresponding entry of the original matrix `M`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toBlock : {m : Type u_2} -> {n : Type u_3} -> {α : Type u_12} -> (M : Matrix m n α) -> (p : m → Prop) -> (q : n → Prop) -> Matrix { a // p a } { a // q a } α
<!-- PINNED-SIGNATURE:END -->


`VTask.toBlock : {m : Type u_2} -> {n : Type u_3} -> {α : Type u_12} -> (M : Matrix m n α) -> (p : m → Prop) -> (q : n → Prop) -> Matrix { a // p a } { a // q a } α`

The implicit argument `m` is the row index type of the original matrix; `n` is the column index type; `α` is the entry type. `M` is the matrix from which the block is extracted. `p` is a predicate on row indices that selects which rows belong to the block. `q` is a predicate on column indices that selects which columns belong to the block.

## Conventions

There are no special junk-value or edge conventions: the function is total and well-defined for any matrix `M` and any predicates `p`, `q`, including the empty predicate (yielding a matrix with an empty index type) or the always-true predicate (yielding a matrix isomorphic to `M` itself).

## Worked examples

- Claim: For the 2×2 identity matrix `M : Matrix (Fin 2) (Fin 2) ℕ` defined by `M i j = if i = j then 1 else 0`, the block selected by `p = (· = 0)` and `q = (· = 0)` has its `(⟨0, rfl⟩, ⟨0, rfl⟩)` entry equal to `M 0 0 = 1`.
  ```lean
  example : (VTask.toBlock (fun i j : Fin 2 => if i = j then 1 else 0)
      (fun i => i = 0) (fun j => j = 0))
      ⟨0, rfl⟩ ⟨0, rfl⟩ = 1 := by decide
  ```

- Claim: For the constant matrix `M : Matrix (Fin 3) (Fin 3) ℕ` with every entry equal to `7`, the block selected by the always-true predicates `p = fun _ => True` and `q = fun _ => True` has every entry equal to `7`.
  ```lean
  example : ∀ (i : {a : Fin 3 // True}) (j : {a : Fin 3 // True}),
      (VTask.toBlock (fun (_ : Fin 3) (_ : Fin 3) => 7)
        (fun _ => True) (fun _ => True)) i j = 7 := by
    intro i j
    simp [VTask.toBlock, Matrix.submatrix]
  ```

- Claim: For a matrix `M : Matrix (Fin 2) (Fin 2) ℕ` and the predicate `p = fun i => i = 1` selecting only the last row, and `q = fun _ => True` selecting all columns, the entry at `(⟨1, rfl⟩, ⟨0, trivial⟩)` equals `M 1 0`.
  ```lean
  example (M : Matrix (Fin 2) (Fin 2) ℕ) :
      (VTask.toBlock M (fun i => i = 1) (fun _ => True))
        ⟨1, rfl⟩ ⟨0, trivial⟩ = M 1 0 := by
    simp [VTask.toBlock, Matrix.submatrix]
  ```

## Boundaries

- If `p` is the always-false predicate, the resulting matrix has an empty row type `{a // False}` and is vacuously a valid matrix with no entries.
- If both `p` and `q` are always-true predicates, the block is isomorphic to `M` itself, with entries in canonical correspondence.
- The function places no restriction on the entry type `α`; it works for any type, whether or not it carries additional algebraic structure.
- There is no requirement that the subtypes `{a // p a}` or `{a // q a}` be finite; the construction is valid for infinite index types as well.

## Not to be confused with

- `Matrix.submatrix`: the more general operation that reindexes rows and columns via arbitrary functions, of which `toBlock` is a special case using subtype coercions.
- `Matrix.BlockDiagonal` / `Matrix.blockDiagonal`: constructs a block-diagonal matrix from a family of matrices, rather than extracting a block from an existing matrix.
- `Matrix.reindex`: reindexes a matrix by equivalences on the row and column types, not by restricting to a subtype.