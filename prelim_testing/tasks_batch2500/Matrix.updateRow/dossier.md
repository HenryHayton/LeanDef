## Object

`VTask.updateRow M i b` is the matrix obtained from `M` by replacing its `i`-th row entirely with the function `b`. Every other row of `M` is left unchanged. The result has the same index types and entry type as `M`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.updateRow : {m : Type u_2} -> {n : Type u_3} -> {α : Type v} -> [DecidableEq m] -> (M : Matrix m n α) -> (i : m) -> (b : n → α) -> Matrix m n α
<!-- PINNED-SIGNATURE:END -->


`{m : Type u_2} -> {n : Type u_3} -> {α : Type v} -> [DecidableEq m] -> (M : Matrix m n α) -> (i : m) -> (b : n → α) -> Matrix m n α`

- `m` is the row-index type; it must carry a `DecidableEq` instance so that rows can be compared for equality.
- `n` is the column-index type.
- `α` is the entry type.
- `M` is the original matrix whose rows are being modified.
- `i` is the index of the row to be replaced.
- `b` is the new row, given as a function from column indices to entries.

## Conventions

No special junk-value or edge conventions have been declared for this definition beyond the standard behaviour of `Function.update`: when the row-index type is empty there are no rows to update and the result equals `M`.

## Worked examples

- Claim: The row at index `i` of `VTask.updateRow M i b` equals `b`.
  (For any matrix `M`, index `i`, and replacement row `b`, querying row `i` of the updated matrix returns exactly `b`.)

- Claim: For a row index `j ≠ i`, the row at `j` of `VTask.updateRow M i b` equals the row at `j` of `M`.
  (Rows other than `i` are untouched.)

- Claim: Applying `VTask.updateRow` twice at the same index `i` with rows `b₁` then `b₂` gives the same result as applying it once with `b₂`.
  (The second update overwrites the first.)

- Claim: `VTask.updateRow M i (M i) = M`.
  (Replacing a row with its own existing values is the identity.)

## Boundaries

- If `m` is a type with a single element (a singleton), then every update targets that unique row, so `VTask.updateRow M i b` always equals the constant matrix whose sole row is `b`.
- If `m` is the empty type, the matrix has no rows at all; `VTask.updateRow M i b` is vacuously equal to `M` regardless of `i` and `b`.
- Updating the same row index twice in succession: only the second replacement survives — there is no accumulation.
- The column structure is never altered; `b` must supply a value for every column index in `n`.

## Not to be confused with

- `Matrix.updateColumn`: the analogous operation that replaces a single *column* rather than a row.
- `Function.update`: the underlying point-update on a function; `VTask.updateRow` lifts this to the matrix level, operating on entire rows rather than individual entries.
- Scalar row operations (e.g., multiplying a row by a scalar): those modify a row by an arithmetic operation on the existing entries, whereas `VTask.updateRow` unconditionally replaces the row with an externally supplied function.