## VTask.weierstrassPSeries

### Object

For a lattice period pair `L` and a complex base-point `x`, this is the formal power series (with complex coefficients, in a single complex variable) whose coefficients encode the Taylor expansion of the Weierstrass elliptic function ℘ around `x`. Concretely, its zeroth coefficient is the value ℘(x) itself, and for every positive integer `i` the `i`-th coefficient is `(i+1)` times the sum-of-inverse-powers function evaluated at `x` with exponent `i+2`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.weierstrassPSeries : (L : PeriodPair) -> (x : ℂ) -> FormalMultilinearSeries ℂ ℂ ℂ
<!-- PINNED-SIGNATURE:END -->


`L` is the period pair (a pair of complex numbers that are linearly independent over the reals, generating the lattice for the elliptic function). `x` is the base-point in the complex plane around which the power series is expanded.

### Conventions

The series is indexed starting at `i = 0`. The zeroth term carries the value of ℘ at `x` as a constant (degree-0) coefficient. For every index `i ≥ 1`, the coefficient is `(i+1)` times the sum over non-zero lattice translates of `(z - ω)^{-(i+2)}` evaluated at `z = x`. No junk-value convention is required because the formula is total and well-defined for every non-negative integer index.

### Worked examples

- Claim: The zeroth coefficient of `VTask.weierstrassPSeries L x` (as a scalar) equals the value of the Weierstrass ℘ function at `x`.

- Claim: For index `i = 1`, the coefficient of `VTask.weierstrassPSeries L x` equals `2 * L.sumInvPow x 3`, reflecting the formula `(1 + 1) * L.sumInvPow x (1 + 2)`.

- Claim: For index `i = 2`, the coefficient of `VTask.weierstrassPSeries L x` equals `3 * L.sumInvPow x 4`, reflecting the formula `(2 + 1) * L.sumInvPow x (2 + 2)`.

### Boundaries

- At `i = 0` the formula takes the special branch: the coefficient is ℘(x), not `1 * L.sumInvPow x 2`. The two branches are genuinely different at `i = 0` since `sumInvPow` at exponent 2 is not the same as the ℘-value (℘ involves a Eisenstein-type correction).
- When `x` is a lattice point (i.e., `x ∈ L`), the Weierstrass ℘ function has a pole, so the individual coefficients may be undefined or divergent; the formal series is still syntactically constructed but may not converge.
- The series is defined for every `x : ℂ` and every index `i : ℕ` without exception; no domain restriction is imposed.

### Not to be confused with

- `PeriodPair.sumInvPow`: the auxiliary building block — a sum of inverse powers over lattice translates — that appears inside each non-zero coefficient of this series, but is not itself a power series.
- `PeriodPair.weierstrassP` (℘ itself): the elliptic function whose Taylor expansion this series represents; the series is the expansion *of* ℘, not ℘ itself.
- A `FormalMultilinearSeries` with non-scalar entries: this series uses scalar (degree-1 multilinear) terms via `ofScalars`, so each term is determined by a single complex number, not a general multilinear map.