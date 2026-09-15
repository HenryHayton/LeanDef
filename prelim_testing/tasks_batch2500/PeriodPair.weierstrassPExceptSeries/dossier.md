## Object

Given a period pair `L` (determining an elliptic lattice), a base point `l₀` in the complex plane, and an expansion point `x`, `VTask.weierstrassPExceptSeries L l₀ x` is the formal power series (in the single complex variable `z - x`) whose sum recovers the value of the "Weierstrass ℘ function with the `l₀`-term removed" (written `℘[L - l₀]`) near `x`. In more classical terms: the Weierstrass ℘-function attached to `L` is a meromorphic doubly-periodic function; omitting the lattice translate at `l₀` yields a holomorphic function on a neighbourhood of `x` (provided `x` avoids the remaining poles), and this object is precisely the Taylor series of that holomorphic function centred at `x`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.weierstrassPExceptSeries : (L : PeriodPair) -> (l₀ x : ℂ) -> FormalMultilinearSeries ℂ ℂ ℂ
<!-- PINNED-SIGNATURE:END -->


VTask.weierstrassPExceptSeries : (L : PeriodPair) -> (l₀ x : ℂ) -> FormalMultilinearSeries ℂ ℂ ℂ

`L` is the period pair (equivalently, the lattice `Λ ⊂ ℂ`) that determines the elliptic curve. `l₀` is the single lattice element whose corresponding pole is "removed" from the usual ℘-function; it is an arbitrary complex number and the series reflects whether or not `l₀` actually belongs to the lattice. `x` is the centre of the Taylor expansion, the point at which the series is based.

## Conventions

The zeroth coefficient (index `i = 0`) of the series at the point `x` is defined to be the value `℘[L - l₀] x` itself, i.e., the constant term is the evaluation of the removed-pole ℘-function at the centre. For indices `i ≥ 1`, the coefficient carries the derivative information encoding the Taylor expansion and includes a correction term that subtracts the contribution of `l₀` itself when `l₀ ∈ L.lattice`; if `l₀ ∉ L.lattice`, no such correction is applied and the series coincides with the full Weierstrass ℘ power series.

## Worked examples

- Claim: When `l₀` does not belong to `L.lattice`, `VTask.weierstrassPExceptSeries L l₀` equals the ordinary Weierstrass ℘ power series `L.weierstrassPSeries`.

- Claim: The series `VTask.weierstrassPExceptSeries L l₀ x` converges to `℘[L - l₀] z` whenever every non-`l₀` lattice point `l` satisfies `‖z - x‖ < ‖l - x‖`, i.e., `z` is closer to `x` than to any remaining pole.

- Claim: The coefficient at index `0` of `VTask.weierstrassPExceptSeries L l₀ x` equals `℘[L - l₀] x`.

- Claim: `VTask.weierstrassPExceptSeries L l₀ x` is the unique formal power series for which `HasFPowerSeriesOnBall ℘[L - l₀] (VTask.weierstrassPExceptSeries L l₀ x) x r` holds for every sufficiently small `r > 0` with the closed ball of radius `r` around `x` free of poles of `℘[L - l₀]`.

## Boundaries

- If `l₀ ∉ L.lattice`, the removal has no effect on the function's poles, and the resulting series is the same as the power series of the full (unmodified) Weierstrass ℘-function at `x`.
- If `x` itself is a pole of `℘[L - l₀]` (i.e., `x ∈ L.lattice` and `x ≠ l₀`, so `x` is a pole that was not removed), the zeroth coefficient at `x` becomes infinite; the formal series is still defined as a `FormalMultilinearSeries` object, but it does not converge and does not represent an analytic function near `x`.
- If `l₀ ∈ L.lattice` and `x = l₀`, then the removed pole is exactly the centre, the function `℘[L - l₀]` is holomorphic at `l₀`, and the series is valid with the `l₀`-correction term active in all coefficients `i ≥ 1`.
- The series is always total and well-typed for every complex `L`, `l₀`, `x`; there is no domain restriction.

## Not to be confused with

- `PeriodPair.weierstrassPSeries`: the power series of the full, unmodified Weierstrass ℘-function at a point; this coincides with `VTask.weierstrassPExceptSeries` only when `l₀ ∉ L.lattice`.
- `PeriodPair.weierstrassPExcept` (the function `℘[L - l₀]` itself): the meromorphic function of which this series is the Taylor expansion; the series and the function are distinct mathematical objects.
- `PeriodPair.sumInvPow`: the tsum appearing in the higher-degree coefficients; it is an ingredient of the series' coefficients, not the series itself.