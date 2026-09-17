## Object

Given a square matrix `A` over a commutative ring `α` indexed by a finite type `n`, a vector `b : n → α`, and an index `i : n`, `VTask.cramerMap A b i` is the determinant of the matrix obtained from `A` by replacing column `i` with the entries of `b`. Varying `i` over all indices gives the vector that Cramer's rule associates with the pair `(A, b)`: if the system `A * x = b` has a unique solution `x`, then this vector equals `A.det • x`; if not, the output is still well-defined as a determinant, but its interpretation as a solution-related quantity may not hold.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.cramerMap : {n : Type v} -> {α : Type w} -> [DecidableEq n] -> [Fintype n] -> [CommRing α] -> (A : Matrix n n α) -> (b : n → α) -> (i : n) -> α
<!-- PINNED-SIGNATURE:END -->


The first implicit argument `n` is the finite index type shared by the rows and columns of the matrix and by the vector. The second implicit argument `α` is the commutative ring in which all entries and the determinant live. The `DecidableEq` and `Fintype` instances are required on `n` to form the matrix and compute its determinant, and the `CommRing` instance is required on `α`. The explicit argument `A` is the square matrix whose column will be substituted. The argument `b` is the replacement column, given as a function from indices to ring elements. The argument `i` selects which column of `A` is replaced by `b` before taking the determinant.

## Conventions

The function is total: it is defined for every commutative ring and every finite index type, including the degenerate case where `n` is empty (i.e., a 0×0 matrix), in which case the determinant equals the multiplicative identity `1` of the ring.

## Worked examples

- Claim: For the 1×1 matrix with single entry `5 : ℤ` and replacement column `b _ = 3`, `VTask.cramerMap A b` at the unique index equals `3`.
  ```lean
  example : VTask.cramerMap !![( 5 : ℤ)] (fun _ => 3) 0 = 3 := by decide
  ```

- Claim: For the 2×2 identity matrix over `ℤ` with `b = ![7, 11]`, replacing column `0` gives determinant `7` (the `(0,0)`-entry of the replacement column, since the other column of the identity contributes a factor of 1).
  ```lean
  example : VTask.cramerMap (!![( 1 : ℤ), 0; 0, 1]) (![7, 11]) 0 = 7 := by decide
  ```

- Claim: For the 2×2 matrix `A = !![2, 1; 1, 3]` over `ℤ` and `b = ![5, 4]`, `VTask.cramerMap A b 0` equals `det !![5, 1; 4, 3] = 11`.
  ```lean
  example : VTask.cramerMap (!![( 2 : ℤ), 1; 1, 3]) (![5, 4]) 0 = 11 := by decide
  ```

## Boundaries

- **Empty index type:** When `n` is the empty type (a 0×0 matrix), the determinant of any 0×0 matrix is `1`, so `VTask.cramerMap A b i` cannot be evaluated (there is no `i : n`); the function vacuously has no values.
- **Singular matrix:** When `A` is singular (i.e., `A.det = 0`), the output `VTask.cramerMap A b i` is still a well-defined determinant value, but the Cramer's rule identity `A.det • x = cramerMap A b` degenerates to `0 = cramerMap A b` only when `b` is in the image of `A`; otherwise the formula does not directly yield a solution.
- **Ring with zero divisors:** The formula is valid in any commutative ring, but the interpretation of `cramerMap A b` as `A.det • x` for a solution `x` requires that `A.det` is not a zero divisor to recover `x` uniquely.
- **Non-invertible ring:** Works in any commutative ring, not just fields; the output is always a ring element.

## Not to be confused with

- **`Matrix.det`**: The determinant of the original matrix `A` itself, without any column substitution.
- **`Matrix.updateCol`**: The intermediate matrix obtained after replacing column `i` of `A` with `b`; `VTask.cramerMap` goes one step further and takes the determinant of that matrix.
- **Cramer's rule solution `x`**: The actual solution vector to `A * x = b`; `VTask.cramerMap A b` is `A.det • x`, not `x` itself, and requires dividing by `A.det` (possible only when `A.det` is invertible) to recover `x`.