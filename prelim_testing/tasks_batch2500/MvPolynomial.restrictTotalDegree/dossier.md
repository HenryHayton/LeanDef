## VTask.restrictTotalDegree

### Object

Given a type of variables σ, a commutative semiring R of coefficients, and a natural number m, `VTask.restrictTotalDegree σ R m` is the R-submodule of the multivariate polynomial ring `MvPolynomial σ R` consisting of exactly those polynomials whose **total degree** is at most m. The total degree of a polynomial is the maximum, over all monomials appearing with nonzero coefficient, of the sum of all variable exponents in that monomial.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.restrictTotalDegree : (σ : Type u) -> (R : Type v) -> [CommSemiring R] -> (m : ℕ) -> Submodule R (MvPolynomial σ R)
<!-- PINNED-SIGNATURE:END -->


The first argument `σ` is the type indexing the set of variables. The second argument `R` is the coefficient type, which must carry a commutative semiring structure. The natural number `m` is the degree bound: every polynomial in the resulting submodule has total degree ≤ m.

### Conventions

The zero polynomial is conventionally assigned total degree −∞ (or treated as having total degree below any natural number), so the zero polynomial belongs to `VTask.restrictTotalDegree σ R m` for every m. The submodule for m = 0 consists precisely of the constant polynomials (including zero).

### Worked examples

- Claim: The constant polynomial `(3 : MvPolynomial (Fin 2) ℕ)` belongs to `VTask.restrictTotalDegree (Fin 2) ℕ 0`, since it has total degree 0.

- Claim: The monomial `X 0 * X 1` in `MvPolynomial (Fin 2) ℤ` belongs to `VTask.restrictTotalDegree (Fin 2) ℤ 2` because its total degree is 1 + 1 = 2 ≤ 2.

- Claim: The monomial `X 0 ^ 3` in `MvPolynomial (Fin 1) ℕ` does **not** belong to `VTask.restrictTotalDegree (Fin 1) ℕ 2`, since its total degree is 3 > 2.

- Claim: `VTask.restrictTotalDegree σ R m` is a submodule of `VTask.restrictTotalDegree σ R (m + 1)` for any m, since total degree ≤ m implies total degree ≤ m + 1.

### Boundaries

- **m = 0**: The submodule contains exactly the constant polynomials (elements of R embedded into `MvPolynomial σ R`), since the only monomials of total degree 0 are the empty monomial.
- **Zero polynomial**: The zero polynomial, having no nonzero terms, belongs to the submodule for every value of m.
- **Empty variable type (σ = Empty or Fin 0)**: Every polynomial in `MvPolynomial (Fin 0) R` is a constant, so the submodule equals the entire ring for all m ≥ 0.
- **Sums and scalar multiples**: The submodule is closed under addition and scalar multiplication; in particular, the sum of two polynomials each of total degree ≤ m also has total degree ≤ m.

### Not to be confused with

- **`MvPolynomial.totalDegree`**: This is a function returning the total degree of a single polynomial as a natural number, not the submodule of polynomials bounded by a given degree.
- **`VTask.restrictDegree` (degree in a single variable)**: A submodule bounding the degree in one specific variable, rather than the sum of all variable exponents.
- **Homogeneous components**: The submodule of polynomials of total degree *exactly* m (a direct summand), which is strictly smaller than `VTask.restrictTotalDegree σ R m` for m ≥ 1.