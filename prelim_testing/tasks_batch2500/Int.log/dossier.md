## Object

`VTask.log b r` is the **integer-valued floor logarithm**: the greatest integer `n` such that `b ^ n ≤ r`. It extends the natural-number floor logarithm (`Nat.log`) to all elements of a linearly ordered semifield, including values strictly between 0 and 1, by returning negative integers in that regime. For base 0 or 1, and for `r = 0`, the value is defined to be 0 by convention.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.log : {R : Type u_1} -> [Semifield R] -> [LinearOrder R] -> [FloorSemiring R] -> (b : ℕ) -> (r : R) -> ℤ
<!-- PINNED-SIGNATURE:END -->


`VTask.log : {R : Type u_1} -> [Semifield R] -> [LinearOrder R] -> [FloorSemiring R] -> (b : ℕ) -> (r : R) -> ℤ`

The type `R` is an implicit linearly ordered semifield equipped with a floor operation (e.g., the real numbers or the rationals). The argument `b` is the **base** of the logarithm, a natural number. The argument `r` is the **value** whose floor logarithm is computed.

## Conventions

When the base `b` is 0 or 1, the result is 0 for every `r`, rather than being undefined; this is a junk-value convention that keeps the function total. When `r = 0`, the result is also 0. For `r` in the range `(0, 1)`, the function returns a non-positive integer (specifically, the negation of a natural-number ceiling logarithm of `r⁻¹`).

## Worked examples

- Claim: For `r : ℝ` with `r = 8`, `VTask.log 2 r = 3` because `2^3 = 8 ≤ 8` and `2^4 = 16 > 8`.

- Claim: For `r : ℝ` with `r = 1/8`, `VTask.log 2 r = -3` because `2^(-3) = 1/8 ≤ 1/8` and `2^(-2) = 1/4 > 1/8`.

- Claim: For any `r : ℝ`, `VTask.log 1 r = 0`, since base 1 always yields 0.

- Claim: For any `r : ℝ`, `VTask.log 0 r = 0`, since base 0 always yields 0.

- Claim: `VTask.log 10 (1 : ℝ) = 0` because `10^0 = 1 ≤ 1` and `10^1 = 10 > 1`.

- Claim: For `r : ℝ` with `r = 100`, `VTask.log 10 r = 2` because `10^2 = 100 ≤ 100` and `10^3 > 100`.

## Boundaries

- **`r = 0`**: The result is 0, by convention (junk value), even though a true logarithm of 0 is undefined.
- **`r = 1`**: The result is 0 for any base, since `b^0 = 1 ≤ 1`.
- **`b = 0` or `b = 1`**: The result is always 0 regardless of `r`.
- **`0 < r < 1`**: The result is a non-positive integer, equal to the negation of `Nat.clog b ⌈r⁻¹⌉₊`.
- **`r ≥ 1`**: The result is a non-negative integer equal to `Nat.log b ⌊r⌋₊`.
- The function is **total** on all of `R`; no domain restriction is imposed.

## Not to be confused with

- `Nat.log b n`: the floor logarithm for natural numbers only; `VTask.log` generalises this to any linearly ordered semifield with a floor.
- `VTask.clog` (i.e., `Int.clog`): the *ceiling* integer logarithm, the least `n` such that `r ≤ b ^ n`; it rounds up instead of down.
- `Real.logb b r`: the real-valued (not integer-valued) logarithm base `b`; its floor coincides with `VTask.log b r` for non-negative reals.
