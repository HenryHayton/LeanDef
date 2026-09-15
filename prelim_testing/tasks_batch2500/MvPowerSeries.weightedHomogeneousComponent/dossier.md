## VTask.weightedHomogeneousComponent

### Object

Given a weight function `w : σ → ℕ` assigning a non-negative integer weight to each variable, and a target degree `p : ℕ`, the **weighted homogeneous component of degree `p`** of a multivariate power series `f` is the power series obtained by retaining exactly those monomials of `f` whose total `w`-weighted degree equals `p`, and replacing all other coefficients by zero. The result is an `R`-linear map from multivariate power series to multivariate power series.

More precisely, if `d : σ →₀ ℕ` is a multi-index (exponent vector), its `w`-weighted degree is `weight w d = ∑ i, w(i) * d(i)`. The component keeps the coefficient of `d` in `f` unchanged when `weight w d = p`, and sets it to zero otherwise.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.weightedHomogeneousComponent : {σ : Type u_1} -> {R : Type u_2} -> [Semiring R] -> (w : σ → ℕ) -> (p : ℕ) -> MvPowerSeries σ R →ₗ[R] MvPowerSeries σ R
<!-- PINNED-SIGNATURE:END -->


`VTask.weightedHomogeneousComponent : {σ : Type u_1} -> {R : Type u_2} -> [Semiring R] -> (w : σ → ℕ) -> (p : ℕ) -> MvPowerSeries σ R →ₗ[R] MvPowerSeries σ R`

The implicit type `σ` is the index type for the variables of the power series. The implicit type `R` is the coefficient semiring, which is required to satisfy the `Semiring` typeclass. The argument `w` is the weight function, assigning a natural-number weight to each variable. The argument `p` is the target weighted degree; only monomials of exactly this weighted degree are retained. The output is an `R`-linear map sending each power series to its `p`-th weighted homogeneous component.

### Conventions

The coefficient of a multi-index `d` in the output is exactly `coeff d f` when `weight w d = p`, and is exactly `0` otherwise. There are no junk values in the classical sense: the function is total over all `p : ℕ`, and when `p` is strictly less than the weighted order of `f`, the output is the zero power series.

### Worked examples

- Claim: For any power series `f` and multi-index `d`, if `weight w d ≠ p`, then the coefficient of `d` in `VTask.weightedHomogeneousComponent w p f` is `0`.

- Claim: For any power series `f` and multi-index `d`, if `weight w d = p`, then the coefficient of `d` in `VTask.weightedHomogeneousComponent w p f` equals the coefficient of `d` in `f`.

- Claim: The output of `VTask.weightedHomogeneousComponent w p f` is always a weighted-homogeneous power series of degree `p` (i.e., `IsWeightedHomogeneous w (VTask.weightedHomogeneousComponent w p f) p` holds).

- Claim: If `p` is strictly less than the weighted order of `f`, then `VTask.weightedHomogeneousComponent w p f = 0`.

- Claim: A power series `f` is weighted-homogeneous of degree `p` if and only if `f = VTask.weightedHomogeneousComponent w p f`.

### Boundaries

- When `p = 0`, the component retains precisely those monomials for which every variable with nonzero weight appears with exponent zero (i.e., monomials of total weight zero), and zeros out all others.
- If the weight function `w` is identically zero, then every multi-index has `weight w d = 0`, so `VTask.weightedHomogeneousComponent w 0 f = f` and `VTask.weightedHomogeneousComponent w p f = 0` for all `p > 0`.
- If `f = 0`, then all components are zero regardless of `p`.
- If `p` equals the weighted order of `f` (the least degree with a nonzero coefficient), the component is guaranteed to be nonzero.
- The map is `R`-linear: it preserves addition and scalar multiplication by elements of `R`.

### Not to be confused with

- `MvPowerSeries.weightedOrder`: This is the minimum weighted degree for which `f` has a nonzero coefficient — a scalar, not a power series.
- `MvPolynomial.weightedHomogeneousComponent`: The analogous projection for multivariate *polynomials* (finite support); the power series version handles potentially infinite formal sums.
- `MvPowerSeries.IsWeightedHomogeneous`: A predicate asserting that a power series *is* weighted-homogeneous of a given degree, rather than a map extracting the homogeneous part.