## Object

A multivariate polynomial over a commutative semiring `R` with variables indexed by `σ` is **weighted homogeneous of weighted degree `m`** with respect to a weight function `w : σ → M` if every monomial that appears in the polynomial (i.e., every monomial with nonzero coefficient) has the same weighted degree `m`. The *weighted degree* of a monomial `x^d` (a finitely-supported exponent vector `d : σ →₀ ℕ`) is the element `∑ i, d(i) • w(i)` in the additive commutative monoid `M`. Thus the polynomial is a finite sum of monomials, all of whose weighted degrees equal the prescribed value `m`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsWeightedHomogeneous : {R : Type u_1} -> {M : Type u_2} -> [CommSemiring R] -> {σ : Type u_3} -> [AddCommMonoid M] -> (w : σ → M) -> (φ : MvPolynomial σ R) -> (m : M) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsWeightedHomogeneous : {R : Type u_1} -> {M : Type u_2} -> [CommSemiring R] -> {σ : Type u_3} -> [AddCommMonoid M] -> (w : σ → M) -> (φ : MvPolynomial σ R) -> (m : M) -> Prop`

`w` is the weight function assigning to each variable index `i : σ` an element `w i : M` that serves as the weight (degree contribution) of that variable. `φ` is the multivariate polynomial over `R` whose weighted homogeneity is being tested. `m` is the required weighted degree that every nonzero monomial of `φ` must have.

## Conventions

The zero polynomial is declared weighted homogeneous of every degree `m`, because it has no nonzero monomials, so the condition `∀ d, coeff d φ ≠ 0 → weight w d = m` is vacuously true.

## Worked examples

- Claim: The variable polynomial `X i` is weighted homogeneous of weighted degree `w i` for any weight function `w` and variable index `i`.

- Claim: The constant polynomial `C r` (for any scalar `r`) is weighted homogeneous of weighted degree `0`, since its only possible nonzero monomial is the constant term whose weighted degree is `∑ i, 0 • w i = 0`.

- Claim: The zero polynomial `(0 : MvPolynomial σ R)` is weighted homogeneous of weighted degree `m` for every `m : M`.

- Claim: The polynomial `1 : MvPolynomial σ R` is weighted homogeneous of weighted degree `0`.

- Claim: For a monomial `monomial d r`, if `weight w d = m`, then `monomial d r` is weighted homogeneous of weighted degree `m`.

- Claim: If `p` is weighted homogeneous of weighted degree `m` with respect to `w`, then `weightedHomogeneousComponent w m p = p` (the component at the same degree recovers `p` entirely).

- Claim: If `p` is weighted homogeneous of weighted degree `m`, then for any `n ≠ m`, the weighted homogeneous component `weightedHomogeneousComponent w n p = 0`.

## Boundaries

- **Empty variable type**: When `σ` is empty (`IsEmpty σ`), every multivariate polynomial is automatically weighted homogeneous of weighted degree `0`, since the only monomial is the empty monomial whose weighted degree is the empty sum, which equals `0`.
- **Zero polynomial**: Vacuously weighted homogeneous of *every* degree `m`, not just one particular `m`. This is exceptional; nonzero polynomials can only be weighted homogeneous of at most one degree (when `M` is cancellative).
- **Scalar multiples**: If `φ` is weighted homogeneous of degree `m` and `r : R` is any scalar, then `r • φ` is also weighted homogeneous of degree `m` (the set of nonzero-coefficient monomials can only shrink).
- **Products**: If `φ` is weighted homogeneous of degree `m` and `ψ` is weighted homogeneous of degree `n`, then `φ * ψ` is weighted homogeneous of degree `m + n`.
- **Sums**: If `φ` and `ψ` are both weighted homogeneous of the same degree `m`, then `φ + ψ` is weighted homogeneous of degree `m`.
- **Partial derivative**: If `φ` is weighted homogeneous of degree `n` and `n' + w i = n`, then `pderiv i φ` is weighted homogeneous of degree `n'` (in the setting where `M` is an `AddCancelCommMonoid`).
- **Weighted total degree zero**: A polynomial `p` is weighted homogeneous of degree `0` if and only if its weighted total degree is `0` (in an `OrderBot` semilattice setting).

## Not to be confused with

- **`MvPolynomial.IsHomogeneous`**: The unweighted version where all variables have weight `1`, so the condition is that all monomials have the same total degree (sum of exponents); this is the special case of `VTask.IsWeightedHomogeneous` with constant weight function `w ≡ 1`.
- **`MvPolynomial.weightedHomogeneousComponent w m φ`**: This is the *projection* of `φ` onto its weighted-degree-`m` component, not a predicate; it is a polynomial, and `φ` satisfies `VTask.IsWeightedHomogeneous w φ m` if and only if this component equals `φ` itself.
- **`MvPolynomial.weightedTotalDegree w φ`**: This is the supremum of all weighted degrees occurring in `φ`, a single element of `M`, whereas `VTask.IsWeightedHomogeneous` asserts that all monomials share exactly one common weighted degree.