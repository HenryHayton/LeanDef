## Object

`VTask.vecMul v M` computes the **row-vector–matrix product**: given a vector `v` indexed by a finite type `m` and a matrix `M` with row-index type `m` and column-index type `n`, it returns a new vector indexed by `n` whose `j`-th entry is the dot product of `v` with the `j`-th column of `M`. Concretely, the `j`-th output entry equals `∑ i, v i * M i j`. The vector `v` is treated as a **row vector** multiplying `M` on the left.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.vecMul : {m : Type u_2} -> {n : Type u_3} -> {α : Type v} -> [NonUnitalNonAssocSemiring α] -> [Fintype m] -> (v : m → α) -> (M : Matrix m n α) -> n → α
<!-- PINNED-SIGNATURE:END -->


`VTask.vecMul : {m : Type u_2} -> {n : Type u_3} -> {α : Type v} -> [NonUnitalNonAssocSemiring α] -> [Fintype m] -> (v : m → α) -> (M : Matrix m n α) -> n → α`

- `m` is the implicit index type for the rows of `M` and the entries of `v`; it must be a `Fintype` so that finite sums can be computed.
- `n` is the implicit index type for the columns of `M` and the entries of the output vector.
- `α` is the implicit scalar type, which must form a `NonUnitalNonAssocSemiring` (supporting addition and multiplication with their usual identities, but not necessarily a unit element or associativity).
- `v : m → α` is the input row vector, i.e., a function assigning a scalar to each row index.
- `M : Matrix m n α` is the matrix, viewed as a function taking a row index and a column index to a scalar.
- The result is a function `n → α`, the output row vector.

## Conventions

There are no declared junk-value or edge conventions for this definition: it is a total function whose output is fully determined by the semiring and `Fintype` instances on its arguments, and no inputs fall outside its domain or produce conventionally-defined fallback values.

## Worked examples

- Claim: For `v = ![1, 2]` and `M = ![![3, 4], ![5, 6]]` over `ℕ`, `VTask.vecMul v M = ![13, 16]`.
  (Entry 0: `1*3 + 2*5 = 13`; Entry 1: `1*4 + 2*6 = 16`.)
  ```lean
  example : VTask.vecMul ![(1 : ℕ), 2] ![![3, 4], ![5, 6]] = ![13, 16] := by decide
  ```

- Claim: For `v = ![0, 1]` and `M = ![![7, 8], ![9, 10]]` over `ℕ`, `VTask.vecMul v M = ![9, 10]`.
  (Multiplying by the second standard basis vector selects the second row of `M`.)
  ```lean
  example : VTask.vecMul ![(0 : ℕ), 1] ![![7, 8], ![9, 10]] = ![9, 10] := by decide
  ```

- Claim: For the zero vector `v = ![0, 0]` and any matrix `M` over `ℕ`, `VTask.vecMul v M = ![0, 0]`.
  ```lean
  example : VTask.vecMul ![(0 : ℕ), 0] ![![3, 4], ![5, 6]] = ![0, 0] := by decide
  ```

## Boundaries

- **Empty index type `m`:** When `m` is empty (a `Fintype` with no elements), every dot product is an empty sum, which evaluates to `0` in the semiring. Thus `VTask.vecMul v M j = 0` for all `j`, regardless of `M`.
- **Singleton index type:** When `m` has a single element, the dot product reduces to a single multiplication: `VTask.vecMul v M j = v e * M e j` where `e` is the unique element of `m`.
- **Zero matrix:** If `M` is the zero matrix, the result is the zero vector regardless of `v`.
- **Zero vector:** If `v` is identically zero, the result is the zero vector regardless of `M`.
- **`n` need not be finite:** The result type `n → α` is well-defined for any type `n`, even infinite ones, since the computation proceeds column-by-column and no summation over `n` is required.

## Not to be confused with

- **`Matrix.mulVec`**: the **column-vector–matrix product** `M *ᵥ v`, where a matrix `M` multiplies a column vector `v` on the right, producing a vector indexed by the row type of `M`; the roles of rows and columns are swapped relative to `VTask.vecMul`.
- **`Matrix.dotProduct` / `v ⬝ᵥ w`**: the plain dot product of two vectors of the same index type, producing a scalar; `VTask.vecMul` uses dot products internally but its output is a vector, not a scalar.
- **`Matrix.mul` / `A * B`**: full matrix–matrix multiplication; `VTask.vecMul` is the special case where the left factor is a single row vector.
