## Object

A **submatrix** (or reindexed matrix) is obtained from a matrix `A : Matrix m n α` by selecting and/or reordering its rows and columns via two index-mapping functions. The entry at position `(i, j)` of the resulting matrix equals the entry of `A` at position `(r i, c j)`. This operation subsumes literal submatrix extraction, row/column permutations, row/column repetition, and dimension changes, all expressed uniformly through the reindexing maps.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.submatrix : {l : Type u_1} -> {m : Type u_2} -> {n : Type u_3} -> {o : Type u_4} -> {α : Type v} -> (A : Matrix m n α) -> (r : l → m) -> (c : o → n) -> Matrix l o α
<!-- PINNED-SIGNATURE:END -->


`VTask.submatrix : {l : Type u_1} -> {m : Type u_2} -> {n : Type u_3} -> {o : Type u_4} -> {α : Type v} -> (A : Matrix m n α) -> (r : l → m) -> (c : o → n) -> Matrix l o α`

The type parameters `l`, `m`, `n`, `o` are the index types for the output rows, input rows, input columns, and output columns respectively; `α` is the entry type. `A` is the source matrix whose entries are being reindexed. `r` is the row-reindexing function, mapping each output row index in `l` to a source row index in `m`. `c` is the column-reindexing function, mapping each output column index in `o` to a source column index in `n`.

## Conventions

The reindexing maps `r` and `c` are not required to be injective or surjective; rows or columns may be duplicated, omitted, or reordered arbitrarily. The dimension of the output matrix (governed by `l` and `o`) need not match the dimension of the input matrix (governed by `m` and `n`).

## Worked examples

- Claim: For a 3×3 matrix `A` over integers, the submatrix obtained by the row map `![1, 2] : Fin 2 → Fin 3` and column map `![0, 2] : Fin 2 → Fin 3` picks out the entries at rows 1,2 and columns 0,2.

- Claim: Applying `VTask.submatrix A id id` (using identity maps for both rows and columns) returns a matrix whose `(i, j)` entry equals `A i j`, i.e., it is the same as `A`.

- Claim: If `r : Fin 1 → Fin 3` sends `0 ↦ 2` and `c : Fin 2 → Fin 3` sends `0 ↦ 0`, `1 ↦ 1`, then `(VTask.submatrix A r c) 0 1 = A 2 1`.

- Claim: Composing two submatrix operations is the same as applying a single submatrix with composed index maps: `VTask.submatrix (VTask.submatrix A r c) r' c' = VTask.submatrix A (r ∘ r') (c ∘ c')`.

## Boundaries

- When `r` or `c` is not injective (maps two distinct output indices to the same input index), the corresponding rows or columns of the source matrix are duplicated in the output. No error or degeneracy occurs; the entry formula still holds pointwise.
- When `l` or `o` is an empty type, the result is the unique empty matrix of that type; the formula vacuously holds.
- When `r` and `c` are both bijections (permutations), the submatrix is a simultaneous row and column permutation of `A`.
- The output matrix has exactly `|l|` rows and `|o|` columns regardless of the sizes of `m` and `n`.

## Not to be confused with

- `Matrix.reindex`: Reindexes using *equivalences* rather than arbitrary maps, guaranteeing the result is isomorphic to the original; `VTask.submatrix` allows non-injective or non-surjective maps.
- `Matrix.minor` (in some traditions): A minor is the *determinant* of a square submatrix, whereas `VTask.submatrix` is the submatrix itself (not its determinant).
- `Matrix.updateRow` / `Matrix.updateCol`: These replace a single row or column with new values, rather than reindexing all rows and columns simultaneously.