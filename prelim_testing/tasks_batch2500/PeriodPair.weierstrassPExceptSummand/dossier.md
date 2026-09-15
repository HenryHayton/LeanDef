## Object

This function computes a single summand appearing in the coefficient of a power-series expansion of the Weierstrass ℘-function at a point `x` not belonging to the period lattice `L`. Concretely, the coefficient `aᵢ` of `(z − x)ⁱ` in the Laurent/power expansion of `℘(z)` around `x` is an infinite sum over lattice points `l ∈ L`; this function gives the contribution of a specific lattice point `l`, but with the term indexed by `l₀` set to zero (i.e., the `l₀`-th term is omitted from the sum). For `i = 0` the per-lattice-point formula includes a correction term `l⁻²` (the constant part of the Weierstrass normalization), whereas for `i ≥ 1` no such correction appears.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.weierstrassPExceptSummand : (L : PeriodPair) -> (l₀ x : ℂ) -> (i : ℕ) -> (l : ↥L.lattice) -> ℂ
<!-- PINNED-SIGNATURE:END -->


`VTask.weierstrassPExceptSummand : (L : PeriodPair) -> (l₀ x : ℂ) -> (i : ℕ) -> (l : ↥L.lattice) -> ℂ`

`L` is the period pair whose lattice governs the elliptic function. `l₀` is the lattice point whose contribution is to be omitted (zeroed out). `x` is the base-point of the power-series expansion; it is intended to lie outside the lattice. `i` is the index of the coefficient in the expansion, i.e., the power of `(z − x)` whose coefficient is being assembled. `l` is the particular lattice element whose contribution this summand computes.

## Conventions

When the underlying complex number of the lattice element `l` equals `l₀`, the summand is defined to be zero regardless of all other arguments — this is the device by which the `l₀`-th term is "omitted" from the sum. For `i = 0` the summand (when not zeroed) equals `(l − x)^(−2) − l^(−2)`, incorporating the Weierstrass normalization subtraction; for `i ≥ 1` the summand equals `(i + 1) · (l − x)^(−(i+2))` with no subtracted correction.

## Worked examples

- Claim: For any period pair `L`, any `l₀ x : ℂ`, any `i : ℕ`, and any lattice element `l` with `l.1 = l₀`, `VTask.weierstrassPExceptSummand L l₀ x i l = 0`.

- Claim: For a lattice element `l` with `l.1 ≠ l₀` and `i = 0`, the summand equals `(l.1 − x)^(−2 : ℤ) − l.1^(−2 : ℤ)` (one factor for the power expansion term and one subtracted normalization term).

- Claim: For a lattice element `l` with `l.1 ≠ l₀` and `i = 3`, the summand equals `4 · (l.1 − x)^(−5 : ℤ)` (four times the fifth inverse power, with no subtracted correction).

## Boundaries

- When `l.1 = l₀` the output is exactly `0`, regardless of whether `x` is in the lattice, whether `i` is zero or positive, or any other condition.
- At `i = 0` a correction term `−l.1^(−2 : ℤ)` is included; this subtraction is absent for all `i ≥ 1`.
- The function makes sense as a complex number for all inputs; there is no domain restriction enforced inside the function itself (divisions by zero in ℂ are handled by Lean/Mathlib's junk-value convention for `zpow`, which returns `0`).
- If `l.1 = x` (the lattice point coincides with the expansion base-point), then `(l.1 − x)^(−(i+2) : ℤ) = 0^(−(i+2) : ℤ)`, which Mathlib evaluates to `0` by the junk-value convention for non-positive-integer powers of zero.

## Not to be confused with

- `PeriodPair.weierstrassP` (the full Weierstrass ℘-function itself, not a single summand in its series expansion).
- The Eisenstein summand `(l − x)^(−k)` without the `(i+1)` prefactor or the `i = 0` correction (the present function carries both pieces needed for the coefficient `aᵢ`).
- `PeriodPair.coeff_weierstrassPExceptSeries`, which assembles the infinite sum over all `l` of this summand to produce the actual coefficient `aᵢ`.