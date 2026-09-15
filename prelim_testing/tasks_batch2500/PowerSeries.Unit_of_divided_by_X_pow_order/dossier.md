## Object

`VTask.Unit_of_divided_by_X_pow_order` takes a formal power series `f` over a field `k` and returns an invertible (unit) power series constructed by stripping off the highest power of the indeterminate `X` that divides `f`. Concretely, if `f` is non-zero and has `X`-adic order `n` (meaning `X^n` divides `f` but `X^(n+1)` does not), the result is the unit whose underlying power series is `f / X^n`. This quotient is a unit because its constant term is non-zero (it is not divisible by `X`). If `f = 0`, the function returns the multiplicative identity (the unit `1`) as a junk value.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Unit_of_divided_by_X_pow_order : {k : Type u_2} -> [Field k] -> (f : PowerSeries k) -> (PowerSeries k)ˣ
<!-- PINNED-SIGNATURE:END -->


`VTask.Unit_of_divided_by_X_pow_order : {k : Type u_2} -> [Field k] -> (f : PowerSeries k) -> (PowerSeries k)ˣ`

The implicit type argument `k` is the coefficient field. The `Field k` instance provides the field structure needed to form inverses of non-zero constant terms. The explicit argument `f` is the formal power series being processed.

## Conventions

When `f = 0`, the function has no mathematically meaningful output (zero has no well-defined order, and dividing by `X^∞` is undefined). In this case the function returns the unit `1` as a conventional junk value, making the function total.

## Worked examples

- Claim: For the zero power series over a field, `VTask.Unit_of_divided_by_X_pow_order 0 = 1` (the junk-value branch fires, returning the unit 1).

- Claim: For a non-zero constant power series `f` (order 0), `(VTask.Unit_of_divided_by_X_pow_order f).val = f` (dividing by `X^0 = 1` leaves `f` unchanged, and the result is already a unit because its constant term is non-zero).

- Claim: If `f = X^3 * g` where `g` has non-zero constant term, then `(VTask.Unit_of_divided_by_X_pow_order f).val = g` (the three factors of `X` are divided out, leaving the unit part `g`).

- Claim: For any non-zero power series `f` over a field, `VTask.Unit_of_divided_by_X_pow_order f` is a unit in `PowerSeries k` (this is guaranteed by the return type `(PowerSeries k)ˣ`).

## Boundaries

- **`f = 0`**: Zero has no `X`-adic order (or order is considered infinite). The function returns the unit `1` as a total-function junk value. No assertion about the mathematical content should be inferred from this case.
- **`f` a non-zero constant (order 0)**: The order is `0`, so `X^0 = 1` is divided out and the result's underlying power series is `f` itself. The constant term of `f` must be non-zero for this to be a unit, which it is because `f ≠ 0` has order `0`.
- **`f = X^n` exactly**: The result is the unit `1` (since `X^n / X^n = 1`), viewed as an element of `(PowerSeries k)ˣ`.
- **Non-zero `f` of arbitrary order**: The underlying value of the returned unit always has a non-zero constant term, ensuring invertibility.

## Not to be confused with

- `PowerSeries.order`: The `ℕ∞`-valued order of a power series (the exponent `n` being divided out), not the unit series itself.
- `PowerSeries.divided_by_X_pow_order` (or `divXPowOrder`): The underlying power series `f / X^n` as a bare `PowerSeries k`, not packaged as a unit element.
- `PowerSeries.Units.mk0` or similar unit constructors: Generic ways to wrap an invertible element as a unit, not specific to the `X`-adic structure of power series.