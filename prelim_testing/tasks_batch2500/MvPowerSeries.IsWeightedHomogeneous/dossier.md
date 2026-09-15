## VTask.IsWeightedHomogeneous

### Object

A multivariate power series `f` over a commutative semiring `R` (in variables indexed by a type `σ`) is *weighted homogeneous of degree `p`* with respect to a weight function `w : σ → ℕ` if every monomial that appears in `f` with a nonzero coefficient has the same `w`-weighted total degree, namely `p`. The weighted degree of a monomial `X^d` (where `d : σ →₀ ℕ` is a finitely-supported exponent vector) is defined as `weight w d = ∑ᵢ w(i) · d(i)`. So the predicate asserts that `f` is supported entirely on the single `w`-degree level `p`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsWeightedHomogeneous : {σ : Type u_1} -> {R : Type u_2} -> [Semiring R] -> (w : σ → ℕ) -> (f : MvPowerSeries σ R) -> (p : ℕ) -> Prop
<!-- PINNED-SIGNATURE:END -->


The implicit argument `σ` is the index type for the variables; `R` is the coefficient semiring. The argument `w` is the weight function assigning a natural-number weight to each variable. The argument `f` is the multivariate power series being tested. The argument `p` is the claimed weighted degree: every nonzero coefficient of `f` must lie on a monomial whose `w`-weighted degree equals exactly `p`.

### Conventions

The zero power series is weighted homogeneous of every degree `p`, because it has no nonzero coefficients and the condition is vacuously satisfied.

### Worked examples

- Claim: The zero power series `(0 : MvPowerSeries σ R)` is `VTask.IsWeightedHomogeneous w 0` for any weight `w` and any degree `p`.

- Claim: If `f` is `VTask.IsWeightedHomogeneous w p` and `g` is `VTask.IsWeightedHomogeneous w p`, then `f + g` is `VTask.IsWeightedHomogeneous w p`.

- Claim: If `f` is `VTask.IsWeightedHomogeneous w p` and `g` is `VTask.IsWeightedHomogeneous w q`, then `f * g` is `VTask.IsWeightedHomogeneous w (p + q)`.

- Claim: For any power series `f`, the `p`-th weighted homogeneous component of `f` (i.e., the projection onto the degree-`p` part) is `VTask.IsWeightedHomogeneous w p`.

- Claim: `f` is `VTask.IsWeightedHomogeneous w p` if and only if `f` equals its own `p`-th weighted homogeneous component.

### Boundaries

- **Zero series**: The zero power series satisfies `VTask.IsWeightedHomogeneous w p` for *every* `p ∈ ℕ`, because the condition quantifies over nonzero coefficients and there are none. This is the canonical junk-value convention.
- **Coefficient outside declared degree is zero**: If `f` is weighted homogeneous of degree `p` and `d` is a monomial with `weight w d ≠ p`, then `f.coeff d = 0` (the contrapositive of the definition).
- **Variable weight zero**: If some variable `i` has `w i = 0`, then monomials with arbitrary powers of `i` all have the same weighted degree, so a weighted-homogeneous series may contain infinitely many distinct monomials all at the same weighted degree level.
- **Degree uniqueness**: A nonzero series can be weighted homogeneous of at most one degree, since having two distinct degrees would force two different values of `p` for the same nonzero coefficient, which is impossible.

### Not to be confused with

- **`MvPolynomial.IsWeightedHomogeneous`**: The analogous predicate for multivariate *polynomials* (finitely-supported formal sums), not power series; the present definition applies to the full power-series ring which may have infinitely many nonzero coefficients.
- **`MvPowerSeries.weightedHomogeneousComponent`**: This is the *projection* (a linear map) extracting the degree-`p` part of any power series; the present object is the *predicate* asserting that a series equals its own projection at `p`.
- **Standard total-degree homogeneity**: The special case where `w` is the constant function `1` (every variable has weight 1) recovers the usual notion of homogeneity by total degree, but `VTask.IsWeightedHomogeneous` handles arbitrary non-uniform weights.