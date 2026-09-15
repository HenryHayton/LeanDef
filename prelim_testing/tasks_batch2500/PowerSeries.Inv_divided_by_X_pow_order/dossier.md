## VTask.Inv_divided_by_X_pow_order

### Object

Given a non-zero formal power series `f` over a field `k`, let `ord` denote the order (X-adic valuation) of `f`, i.e., the largest non-negative integer such that `X^ord` divides `f`. The quotient `f / X^ord` is then a power series whose constant coefficient is non-zero, hence a unit in the ring of power series over a field. `VTask.Inv_divided_by_X_pow_order hf` is the multiplicative inverse of that unit quotient: it is the unique power series `g` satisfying `(f / X^ord) * g = 1` in `k⟦X⟧`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Inv_divided_by_X_pow_order : {k : Type u_2} -> [Field k] -> {f : PowerSeries k} -> (hf : f ≠ 0) -> PowerSeries k
<!-- PINNED-SIGNATURE:END -->


The implicit argument `k` is the coefficient field. The instance argument provides the field structure on `k`. The implicit argument `f` is the ambient formal power series. The explicit argument `hf` is a proof that `f` is not the zero power series; this non-vanishing condition is required to guarantee that `f / X^ord` has a non-zero constant term and is therefore invertible.

### Conventions

The domain of `VTask.Inv_divided_by_X_pow_order` is all non-zero formal power series over a field; there is no additional restriction. When `f` is a unit (i.e., its constant term is already non-zero, so `ord f = 0`), the output coincides with the ordinary power-series inverse of `f`.

### Worked examples

- Claim: For `f = 1` (the constant power series 1) over `ℚ`, `VTask.Inv_divided_by_X_pow_order hf = 1`, since `ord(1) = 0` and the inverse of `1 / X^0 = 1` is `1`.

- Claim: For `f = X` over `ℚ`, `ord(f) = 1` and `f / X^1 = 1`, so `VTask.Inv_divided_by_X_pow_order hf = 1`.

- Claim: For `f = 2 * X^3` over `ℚ`, `ord(f) = 3` and `f / X^3 = 2` (the constant series with value 2), so `VTask.Inv_divided_by_X_pow_order hf` equals the constant power series `1/2`.

- Claim: For any non-zero `f`, the product `(f / X^(order f)) * VTask.Inv_divided_by_X_pow_order hf = 1` in `k⟦X⟧`.

### Boundaries

- The argument `hf : f ≠ 0` is essential: the zero power series has no well-defined order and its quotient by any power of `X` would not have an invertible constant term.
- When `f` already has a non-zero constant term (`order f = 0`), `f / X^0 = f`, so `VTask.Inv_divided_by_X_pow_order hf` is just the standard power-series inverse of `f`.
- The result is always a power series with non-zero constant term (it is a unit in `k⟦X⟧`), regardless of how many leading zero coefficients `f` had.
- This definition does NOT invert `f` itself; it inverts only the unit part `f / X^(order f)`. In particular, multiplying `f` by `VTask.Inv_divided_by_X_pow_order hf` gives `X^(order f)`, not `1`.

### Not to be confused with

- `PowerSeries.invOfUnit`: inverts a power series given an explicit proof that its constant coefficient is a unit — `VTask.Inv_divided_by_X_pow_order` automates the extraction of that unit by first stripping powers of `X`.
- `Unit_divided_by_X_pow_order`: packages `f / X^(order f)` together with `VTask.Inv_divided_by_X_pow_order hf` into a `Units` term; `VTask.Inv_divided_by_X_pow_order` is only the inverse component.
- The inverse of `f` itself: `VTask.Inv_divided_by_X_pow_order hf` is NOT the power-series inverse of `f` (which does not exist when `order f > 0`); it is the inverse of the unit obtained after removing the `X^ord` factor.
