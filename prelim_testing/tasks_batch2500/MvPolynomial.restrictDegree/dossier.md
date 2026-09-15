## VTask.restrictDegree

### Object

For a commutative semiring `R` and a type of variable indices `σ`, `VTask.restrictDegree σ R m` is the sub-`R`-module of the multivariate polynomial ring `MvPolynomial σ R` consisting of exactly those polynomials in which every variable appears with exponent at most `m`. Concretely, a polynomial `p` belongs to this submodule if and only if, for every monomial (a finitely-supported function `n : σ → ℕ`) appearing with a nonzero coefficient in `p`, and for every variable index `i : σ`, the exponent `n i ≤ m`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.restrictDegree : (σ : Type u) -> (R : Type v) -> [CommSemiring R] -> (m : ℕ) -> Submodule R (MvPolynomial σ R)
<!-- PINNED-SIGNATURE:END -->


The first argument `σ` is the type whose elements name the indeterminates of the polynomial ring. The second argument `R` is the coefficient ring, which must carry a `CommSemiring` structure (supplied implicitly). The third argument `m : ℕ` is the uniform upper bound imposed on the degree of every individual variable in any monomial; every exponent in every monomial of an admissible polynomial must be at most `m`.

### Conventions

When `m = 0` the only polynomials satisfying the degree condition are those supported on the zero monomial (i.e., the constant polynomials), so the submodule coincides with the image of the constant embedding `R → MvPolynomial σ R`. The bound is inclusive: exponent exactly equal to `m` is permitted.

### Worked examples

- Claim: The constant polynomial `1 : MvPolynomial (Fin 2) ℤ` belongs to `VTask.restrictDegree (Fin 2) ℤ 0`, because all its monomial exponents are 0 ≤ 0.

- Claim: The monomial `X 0 * X 1 : MvPolynomial (Fin 2) ℤ` (corresponding to the exponent vector `[1,1]`) belongs to `VTask.restrictDegree (Fin 2) ℤ 1`, since each variable exponent is 1 ≤ 1.

- Claim: The polynomial `X 0 ^ 2 : MvPolynomial (Fin 1) ℤ` does **not** belong to `VTask.restrictDegree (Fin 1) ℤ 1`, because variable 0 appears with exponent 2 > 1.

- Claim: `VTask.restrictDegree σ R m` is a submodule of `MvPolynomial σ R` for any `σ`, `R`, and `m`, hence is closed under addition and scalar multiplication by `R`.

- Claim: For `m₁ ≤ m₂`, every polynomial in `VTask.restrictDegree σ R m₁` also belongs to `VTask.restrictDegree σ R m₂` (monotonicity in `m`).

### Boundaries

- **`m = 0`**: The submodule consists precisely of the constant polynomials (those supported only on the zero monomial). This is a copy of `R` inside `MvPolynomial σ R`.
- **`σ = Empty` (no variables)**: Every polynomial over an empty variable type is a constant, and every monomial exponent condition is vacuously true, so the submodule is all of `MvPolynomial Empty R` for any `m`.
- **`σ` infinite**: The definition is still valid; the degree bound applies to each variable's exponent in each monomial individually. The submodule may or may not be a finitely generated `R`-module depending on whether `σ` is finite.
- **`m` unbounded growth**: As `m → ∞`, the union of the submodules `VTask.restrictDegree σ R m` (over all `m`) is all of `MvPolynomial σ R`, since every polynomial has finitely many monomials each with finite exponents.

### Not to be confused with

- **`MvPolynomial.restrictTotalDegree`** (if it exists): a submodule bounding the *total* degree (sum of all exponents in a monomial) rather than bounding each variable's exponent individually.
- **`Polynomial.degreeLE`**: the analogous construction for univariate polynomials, bounding the degree of a single-variable polynomial; `VTask.restrictDegree` generalises this to many variables with a uniform per-variable bound.
- **`MvPolynomial.restrictSupport`**: the more general primitive that restricts to polynomials whose monomial support lies in a given set of exponent vectors; `VTask.restrictDegree` is the special case where that set is `{n | ∀ i, n i ≤ m}`.