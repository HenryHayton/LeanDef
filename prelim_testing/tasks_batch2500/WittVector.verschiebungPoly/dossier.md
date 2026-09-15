## VTask.verschiebungPoly

### Object

The `n`th Verschiebung polynomial is an element of the ring of multivariate polynomials over the integers with natural-number indices for variables. Specifically, the 0th polynomial is the zero polynomial, and for every positive integer `n`, the `n`th polynomial is the single free variable indexed by `n − 1`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.verschiebungPoly : (n : ℕ) -> MvPolynomial ℕ ℤ
<!-- PINNED-SIGNATURE:END -->


The single argument `n : ℕ` selects which Verschiebung polynomial to return: `n = 0` gives the zero polynomial, and `n > 0` gives the monomial equal to the variable `X(n−1)`.

### Conventions

The 0th Verschiebung polynomial is defined to be the zero polynomial (the additive identity), serving as the natural base case for the otherwise variable-returning family.

### Worked examples

- Claim: `VTask.verschiebungPoly 0 = 0` — the 0th Verschiebung polynomial is the zero polynomial.

- Claim: `VTask.verschiebungPoly 1 = MvPolynomial.X 0` — the 1st Verschiebung polynomial is the variable X(0).

- Claim: `VTask.verschiebungPoly 3 = MvPolynomial.X 2` — the 3rd Verschiebung polynomial is the variable X(2).

- Claim: `VTask.verschiebungPoly 5 = MvPolynomial.X 4` — the 5th Verschiebung polynomial is the variable X(4).

### Boundaries

- At `n = 0`, the result is the zero polynomial, not a variable. This is the only index for which no variable is produced.
- For all `n ≥ 1`, the result is exactly the generator `X (n − 1)`, a monomial with coefficient 1 and no other terms.
- There is no upper boundary: the function is total on all natural numbers.

### Not to be confused with

- `MvPolynomial.X k`: The variable indexed by `k` directly; `verschiebungPoly` shifts the index by one and handles the `n = 0` case separately.
- Witt vector ghost polynomials or Frobenius polynomials: related families used in Witt vector arithmetic, but with different (typically more complex) formulas involving sums and powers.
- `verschiebungFun` (the Verschiebung map on Witt vectors): the ring map whose components these polynomials describe, not the polynomials themselves.