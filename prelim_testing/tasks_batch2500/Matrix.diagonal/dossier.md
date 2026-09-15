## Object

`VTask.diagonal d` is the square matrix over an index type `n` and coefficient type `α` whose `(i, j)` entry equals `d i` when `i = j` (on the main diagonal) and `0` otherwise (off the diagonal). It is the standard diagonal matrix construction: place the values given by the function `d` along the main diagonal and fill every off-diagonal position with the zero element.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.diagonal : {n : Type u_3} -> {α : Type v} -> [DecidableEq n] -> [Zero α] -> (d : n → α) -> Matrix n n α
<!-- PINNED-SIGNATURE:END -->


`VTask.diagonal : {n : Type u_3} -> {α : Type v} -> [DecidableEq n] -> [Zero α] -> (d : n → α) -> Matrix n n α`

The implicit type argument `n` is the index type used for both rows and columns, making the result a square matrix. The implicit type argument `α` is the type of matrix entries. The `DecidableEq n` instance is needed to decide, for any pair of indices, whether they are equal or not. The `Zero α` instance provides the zero value placed in off-diagonal positions. The explicit argument `d : n → α` is the function specifying the diagonal entries: the value at index `i` is placed in position `(i, i)`.

## Conventions

When the index type `n` is empty (has no elements), the resulting matrix is the unique empty square matrix, which is vacuously consistent with all diagonal/off-diagonal conditions. There are no junk values for this definition beyond this edge case, which is handled uniformly by the universal quantification over `n`.

## Worked examples

- Claim: For `d : Fin 3 → ℕ` defined by `d i = i.val + 1`, the diagonal matrix has entry `(diagonal d) ⟨1, _⟩ ⟨1, _⟩ = 2`.

- Claim: For `d : Fin 2 → ℤ` defined by `d 0 = 5` and `d 1 = 7`, the off-diagonal entries `(diagonal d) 0 1` and `(diagonal d) 1 0` are both `0`.

- Claim: `VTask.diagonal (fun _ : Fin 3 => (1 : ℤ))` is the 3×3 matrix with `1`s on the diagonal and `0`s elsewhere (i.e., the identity matrix over ℤ).
  ```lean
  example : VTask.diagonal (fun _ : Fin 3 => (1 : ℤ)) = 1 := by decide
  ```

- Claim: `VTask.diagonal (fun i : Fin 2 => (i.val : ℕ))` has `(diagonal d) 0 0 = 0`, `(diagonal d) 1 1 = 1`, and `(diagonal d) 0 1 = 0`.
  ```lean
  example : VTask.diagonal (fun i : Fin 2 => (i.val : ℕ)) 0 1 = 0 := by decide
  ```

## Boundaries

- **Empty index type**: If `n` is uninhabited (e.g., `Fin 0`), then `diagonal d` is the unique `0 × 0` matrix. Both the on-diagonal and off-diagonal conditions are vacuously satisfied.
- **Singleton index type**: If `n` has exactly one element, the matrix is `1 × 1` and consists solely of `d` applied to that element; there are no off-diagonal positions.
- **Zero diagonal function**: If `d` is the constant zero function, then `diagonal d` is the zero matrix, since both diagonal entries (which equal `d i = 0`) and off-diagonal entries are `0`.
- **Equality decidability**: The construction requires `DecidableEq n` to place values correctly; without it, the casework on `i = j` cannot be carried out computationally.

## Not to be confused with

- `Matrix.diag`: The inverse operation — given a matrix, `diag A` extracts its diagonal as a function `n → α`; `VTask.diagonal` goes the other direction, from a function to a matrix.
- `Matrix.blockDiagonal`: Places entire sub-matrices along the diagonal of a larger matrix, rather than scalar values at each diagonal position.
- `Matrix.one` (the identity matrix): For semirings with `One`, the identity matrix corresponds to `diagonal (fun _ => 1)`, but `VTask.diagonal` is a more general construction that does not require a ring structure.