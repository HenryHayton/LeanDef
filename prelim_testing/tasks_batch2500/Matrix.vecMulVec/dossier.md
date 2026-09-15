## Object

`VTask.vecMulVec w v` is the **outer product** (or rank-1 matrix) formed from two vectors `w` and `v`. It is the matrix whose `(i, j)`-entry is the product of the `i`-th component of `w` with the `j`-th component of `v`. Concretely, if `w : m → α` and `v : n → α`, then the result is the `m × n` matrix `M` with `M i j = w i * v j`. This is the direct analogue of the outer product `w vᵀ` familiar from linear algebra (with `w` a column vector and `v` a row vector).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.vecMulVec : {m : Type u_2} -> {n : Type u_3} -> {α : Type v} -> [Mul α] -> (w : m → α) -> (v : n → α) -> Matrix m n α
<!-- PINNED-SIGNATURE:END -->


`VTask.vecMulVec : {m : Type u_2} -> {n : Type u_3} -> {α : Type v} -> [Mul α] -> (w : m → α) -> (v : n → α) -> Matrix m n α`

The implicit type arguments `m` and `n` are the index types for the rows and columns of the resulting matrix, respectively; `α` is the entry type. The typeclass `[Mul α]` supplies the binary multiplication used to form each entry. The explicit argument `w : m → α` is the "column" vector, whose values index the rows; `v : n → α` is the "row" vector, whose values index the columns. The result is a `Matrix m n α`.

## Conventions

There are no declared junk-value or edge-case conventions for this definition: it is total and well-defined for all inputs, including empty index types, zero vectors, and non-commutative multiplications. The multiplication is always taken in the order `w i * v j` (left factor from `w`, right factor from `v`), which matters when `α` is non-commutative.

## Worked examples

- Claim: `VTask.vecMulVec (fun i : Fin 2 => (i : ℕ) + 1) (fun j : Fin 3 => (j : ℕ) + 1) 1 2 = 6`
  ```lean
  example : VTask.vecMulVec (fun i : Fin 2 => (i : ℕ) + 1) (fun j : Fin 3 => (j : ℕ) + 1) 1 2 = 6 := by decide
  ```

- Claim: For `w = ![1, 2]` and `v = ![3, 4]`, `VTask.vecMulVec w v 0 1 = 4` (first entry of `w` times second entry of `v`).
  ```lean
  example : VTask.vecMulVec (![1, 2] : Fin 2 → ℕ) (![3, 4] : Fin 2 → ℕ) 0 1 = 4 := by decide
  ```

- Claim: `VTask.vecMulVec (fun _ : Fin 1 => 5) (fun _ : Fin 1 => 7) 0 0 = 35`
  ```lean
  example : VTask.vecMulVec (fun _ : Fin 1 => (5 : ℕ)) (fun _ : Fin 1 => 7) 0 0 = 35 := by decide
  ```

- Claim: For any vectors `w : m → α` and `v : n → α`, every entry `(i, j)` of `VTask.vecMulVec w v` equals `w i * v j`.

## Boundaries

- **Empty index types**: If `m` or `n` is an empty type (e.g., `Fin 0`), the resulting matrix has no entries, but the definition is still valid and produces the unique empty matrix.
- **Non-commutative multiplication**: The entry order is always `w i * v j`; if `α` is non-commutative, swapping `w` and `v` (even with transposition) may give a different result.
- **Zero vectors**: If all entries of `w` (or `v`) are zero (in a suitable algebraic structure), every entry of the result is zero, giving the zero matrix.
- **Scalar case (`m = n = Fin 1`)**: The result is a `1 × 1` matrix whose sole entry is `w 0 * v 0`, i.e., the product of two scalars.

## Not to be confused with

- **`Matrix.dotProduct` (inner product)**: Takes two vectors of the same index type and returns a scalar (sum of componentwise products), not a matrix.
- **`Matrix.mulVec` / `Matrix.vecMul`**: These multiply a matrix by a vector to produce a vector, not an outer product of two vectors.
- **`Matrix.replicateRow` / `Matrix.replicateCol`**: These replicate a single vector across all rows or columns; `VTask.vecMulVec` is their *pointwise product* (for a unique replication index), not either one alone.