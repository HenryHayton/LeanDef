## VTask.weightedOrder

### Object

The **weighted order** of a multivariate formal power series `f` over a semiring `R` (in variables indexed by a type `σ`) with respect to a weight function `w : σ → ℕ`. It is the smallest total weight of any monomial that appears with a nonzero coefficient in `f`. The weight of a monomial `X^d` (where `d : σ →₀ ℕ`) is the sum `∑ i, w(i) * d(i)`. If `f` is the zero series (every coefficient is zero), the weighted order is defined to be `⊤` (infinity, the top element of `ℕ∞`); otherwise it is a finite nonnegative integer.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.weightedOrder : {σ : Type u_1} -> {R : Type u_2} -> [Semiring R] -> (w : σ → ℕ) -> (f : MvPowerSeries σ R) -> ℕ∞
<!-- PINNED-SIGNATURE:END -->


The first argument `w : σ → ℕ` assigns a nonneg integer weight to each variable in `σ`. The second argument `f : MvPowerSeries σ R` is the multivariate formal power series whose weighted order is being computed.

### Conventions

When `f` is the zero power series (all coefficients are zero), `VTask.weightedOrder w f` returns `⊤ : ℕ∞`, representing infinity. This is the standard convention that the order of zero is infinite.

### Worked examples

- Claim: For the zero power series over `ℕ`, `VTask.weightedOrder w 0 = ⊤` for any weight function `w`.

- Claim: If `f` is a power series whose lowest-weight nonzero monomial has total `w`-weight equal to `k`, then `VTask.weightedOrder w f = k` (a finite element of `ℕ∞`).

- Claim: For a power series that equals the constant `1` (the unit of the ring), every variable appears with exponent zero in the constant term, so the constant monomial has weight `0`, meaning `VTask.weightedOrder w 1 = 0`.

- Claim: If `w` assigns weight 2 to the single variable and `f` contains as its lowest-degree nonzero monomial the variable itself (degree 1), then `VTask.weightedOrder w f = 2`.

### Boundaries

- **Zero series**: `VTask.weightedOrder w 0 = ⊤`. This is the only case yielding `⊤`.
- **Nonzero series**: the result is always a finite element of `ℕ∞`, equal to the minimum `w`-weighted degree among all monomials with nonzero coefficients.
- **All-zero weights** (`w ≡ 0`): every monomial has weight 0, so any nonzero series has weighted order `0`.
- **Constant nonzero series**: the constant term corresponds to the zero multi-index; its weight is 0, so the weighted order is `0`.
- **The type `σ` is empty** (no variables): the only power series are the scalars, the zero series maps to `⊤`, and any nonzero scalar maps to `0`.

### Not to be confused with

- **`MvPowerSeries.order`** (unweighted order): uses the total degree (sum of exponents) rather than a custom weight; special case of weighted order with `w ≡ 1`.
- **`PowerSeries.order`** (single-variable order): the univariate analogue, returning the index of the first nonzero coefficient.
- **`MvPolynomial.weightedDegree`**: measures the highest weighted degree of a polynomial, not the lowest weighted degree of a power series.