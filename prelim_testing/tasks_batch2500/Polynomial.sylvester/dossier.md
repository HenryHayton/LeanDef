## 1. Object

The **Sylvester matrix** of two polynomials `f` and `g`, with respect to parameters `m` and `n`, is the classical `(m+n) × (m+n)` matrix whose determinant yields the resultant of the two polynomials. Its columns are arranged in two groups: the first `m` columns contain shifted copies of the coefficients of `g` (read from top to bottom in successive diagonal strips), and the last `n` columns contain shifted copies of the coefficients of `f` in the same fashion. More precisely, the `j`-th column (0-indexed) of the first group places `g`'s coefficient `g_k` at row `j + k`, and the `j`-th column of the second group places `f`'s coefficient `f_k` at row `j + k`; all other entries are zero.

Importantly, `m` and `n` are free natural-number parameters and need not equal the actual degrees of `f` and `g`; the matrix is well-defined for any values of `m` and `n`.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sylvester : {R : Type u_1} -> [Semiring R] -> (f g : Polynomial R) -> (m n : ℕ) -> Matrix (Fin (m + n)) (Fin (m + n)) R
<!-- PINNED-SIGNATURE:END -->


`VTask.sylvester : {R : Type u_1} -> [Semiring R] -> (f g : Polynomial R) -> (m n : ℕ) -> Matrix (Fin (m + n)) (Fin (m + n)) R`

- `R` is the coefficient ring, which is required to be a semiring (so it need not have subtraction or a multiplicative inverse).
- `f` is the first polynomial; its coefficients fill the rightmost `n` columns of the matrix.
- `g` is the second polynomial; its coefficients fill the leftmost `m` columns of the matrix.
- `m` is the parameter that controls how many columns are devoted to `g` and also (together with `n`) fixes the matrix dimension; it is intended to be at least the degree of `f` but this is not enforced.
- `n` is the parameter that controls how many columns are devoted to `f` and also contributes to the matrix dimension; it is intended to be at least the degree of `g` but this is not enforced.

## 3. Conventions

When `m` or `n` is zero the corresponding block of columns vanishes entirely and the matrix degenerates to a smaller square block filled by the other polynomial's coefficient strips; this is still a valid `(m+n) × (m+n)` matrix. When both `m` and `n` are zero the result is a `0 × 0` (empty) matrix. Entries outside the shifted coefficient band — i.e., rows not in the interval `[j, j+n]` (for `g`-columns) or `[j, j+m]` (for `f`-columns) — are defined to be the zero element of `R`. If `m` or `n` exceeds the actual degree of the corresponding polynomial, the extra rows will contain zero coefficients (since `Polynomial.coeff` returns 0 beyond the degree), so the construction remains consistent and simply pads with zeros.

## 4. Worked examples

- Claim: For `f = X` and `g = X` over `ℤ` with `m = 1`, `n = 1`, the Sylvester matrix is the 2×2 identity (since both polynomials are monic of degree 1, and the Sylvester matrix becomes `[[g₀, 0], [g₁, f₀], [0, f₁]]` truncated to 2×2 with `g₀ = 0, g₁ = 1, f₀ = 0, f₁ = 1`; the (0,0) entry is `g.coeff(0-0) = g.coeff 0 = 0` if `0 ∈ [0,1]`, so entry (0,0) = `g.coeff 0 = 0`; entry (1,0) = `g.coeff 1 = 1`; entry (0,1) = `f.coeff 0 = 0`; entry (1,1) = `f.coeff 1 = 1`; so the matrix is `!![0, 0; 1, 1]` and its determinant is 0, which matches `resultant(X, X) = 0`).

- Claim: For the constant polynomial `f = C 2` and `g = C 3` over `ℤ` with `m = 1`, `n = 1`, the Sylvester matrix `VTask.sylvester f g 1 1` is a 2×2 matrix; entry (0,0) is `g.coeff 0 = 3`, entry (1,0) is `g.coeff 1 = 0`, entry (0,1) is `f.coeff 0 = 2`, entry (1,1) is `f.coeff 1 = 0`, giving `!![3, 2; 0, 0]` with determinant 0 — consistent with both polynomials being constant (degree 0, not degree 1).

- Claim: Swapping `f` and `g` and also swapping `m` and `n` produces a matrix that, after reindexing, equals the original Sylvester matrix. That is, `VTask.sylvester f g m n` and `VTask.sylvester g f n m` are related by a canonical permutation of rows and columns (`sylvester_comm`).

- Claim: Applying a semiring homomorphism `φ : R →+* S` entry-wise to `VTask.sylvester f g m n` gives the same result as computing `VTask.sylvester (f.map φ) (g.map φ) m n` (`sylvester_map_map`).

## 5. Boundaries

- **`m = 0`**: The first block of columns (for `g`) is empty. The resulting `n × n` matrix contains only the `f`-coefficient strips across all `n` columns.
- **`n = 0`**: The second block of columns (for `f`) is empty. The resulting `m × m` matrix contains only the `g`-coefficient strips across all `m` columns.
- **`m = 0` and `n = 0`**: The matrix has size `0 × 0`; it is the unique empty matrix.
- **Degree of `f` less than `n`**: The `f`-coefficient columns are padded with zeros above the degree, since `Polynomial.coeff f k = 0` for `k > natDegree f`.
- **Degree of `g` less than `m`**: Similarly, the `g`-coefficient columns are padded with zeros.
- **Row/column boundary**: Entry `(i, j)` is nonzero only when `i` lies in the interval `[j, j+n]` (for `j < m`) or `[j - m, j - m + m] = [j-m, j]` (for `j ≥ m`), so the matrix is banded.

## 6. Not to be confused with

- **`Polynomial.resultant`** — the scalar determinant of the Sylvester matrix; `VTask.sylvester` is the matrix itself, not its determinant.
- **`sylvesterMap`** — the linear map between polynomial degree-bounded spaces whose matrix representation (in the standard basis) equals `VTask.sylvester`; `VTask.sylvester` is the concrete matrix, while `sylvesterMap` is the abstract linear map.
- **`sylvesterDeriv`** — a related but distinct matrix formed from a single polynomial `f` and its formal derivative, used in discriminant computations; not the same as the two-polynomial Sylvester matrix.