## Object

The **formal derivative** of a polynomial over a semiring `R` is the polynomial obtained by applying the classical power-rule coefficient-by-coefficient: if `p = a₀ + a₁X + a₂X² + … + aₙXⁿ`, then `VTask.derivative p = a₁ + 2a₂X + … + naₙXⁿ⁻¹`. No notion of limits or analysis is involved; the operation is purely algebraic and is defined for polynomials over any semiring (including ℕ, ℤ, ℤ/nℤ, etc.).

The result is packaged as an `R`-linear map `R[X] →ₗ[R] R[X]`, capturing the fact that differentiation is additive and `R`-homogeneous.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.derivative : {R : Type u} -> [Semiring R] -> Polynomial R →ₗ[R] Polynomial R
<!-- PINNED-SIGNATURE:END -->


`VTask.derivative : {R : Type u} -> [Semiring R] -> Polynomial R →ₗ[R] Polynomial R`

The implicit type argument `R` is the coefficient semiring. The `Semiring R` instance supplies the ring operations used to form products `n · aₙ` (where `n : ℕ` is cast into `R`). The map itself takes a polynomial over `R` and returns its formal derivative, again a polynomial over `R`.

## Conventions

Because the natural-number subtraction `n - 1` in the coefficient formula is used for the exponent, the constant term (exponent 0) contributes `a₀ · 0 · X^(0-1) = 0`; there is no junk term from the subtraction underflow.

When `R` has characteristic `p > 0`, the coefficient `n · aₙ` becomes zero for all `n` divisible by `p`, so the formal derivative of `Xᵖ` is `0`; this is expected algebraic behaviour, not a special convention.

## Worked examples

- Claim: The formal derivative of the zero polynomial is zero: `VTask.derivative 0 = 0`.

- Claim: The formal derivative of a constant polynomial `C r` is `0` for any `r : R`.

- Claim: The formal derivative of `X ^ 3` over `ℤ` is `3 * X ^ 2` (i.e., `C 3 * X ^ 2`).

- Claim: The formal derivative of `X ^ 2 + X + 1` over `ℤ` equals `2 * X + 1`.

- Claim: The formal derivative satisfies the product rule: for polynomials `p q : R[X]` over a commutative semiring, `VTask.derivative (p * q) = VTask.derivative p * q + p * VTask.derivative q`.

- Claim: Iterating `VTask.derivative` `n + 1` times applied to `X ^ n` over `ℚ` yields `n!` (the factorial as a scalar).

## Boundaries

- **Zero polynomial**: `VTask.derivative 0 = 0`. The empty sum is zero.
- **Constant polynomial**: `VTask.derivative (C r) = 0` for any `r : R`, since the sole term has exponent 0, contributing coefficient `r * 0 = 0`.
- **Linear polynomial**: `VTask.derivative (C r * X) = C r`; the degree drops by one as expected.
- **Characteristic-p behaviour**: Over `ZMod p`, the monomial `X ^ p` has formal derivative `0` because the coefficient `p` vanishes in the ring. Entire polynomials of the form `f(Xᵖ)` lie in the kernel.
- **Degree**: For a nonzero polynomial of degree `n ≥ 1`, the formal derivative has degree `n - 1` (provided the leading coefficient times `n` is nonzero in `R`). For a nonzero constant, the derivative is `0` and has no well-defined positive degree.
- **Semiring, not ring**: The definition works over any semiring; no additive inverses are needed because the power rule only uses multiplication and the natural cast `↑n : R`.

## Not to be confused with

- **`Polynomial.eval` composed with a derivative**: `VTask.derivative p` is a polynomial object; evaluating it at a point gives a ring element, but the derivative itself is not an element of `R`.
- **`PowerSeries.derivative`**: The analogous formal derivative for formal power series in `R⟦X⟧`; it agrees with `VTask.derivative` on the polynomial truncations but lives in a different type.
- **`Polynomial.HasDerivAt` / analytic derivative**: The analytic (limit-based) derivative of a polynomial function `R → R` when `R = ℝ` or `ℝ`; it coincides numerically with the formal derivative but is a different object defined via analysis rather than pure algebra.