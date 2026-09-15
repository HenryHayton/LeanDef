## Object

`VTask.clog b r` is the **integer ceiling logarithm** of `r` with respect to base `b`: the least integer `n` such that `r ≤ b ^ n`. Equivalently, it is the smallest power of the natural number `b` (as an integer exponent) that is still at least as large as `r`. This is the "ceiling" analogue of the integer logarithm, just as `Nat.clog` is the ceiling analogue of `Nat.log` in the natural-number setting.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.clog : {R : Type u_1} -> [Semifield R] -> [LinearOrder R] -> [FloorSemiring R] -> (b : ℕ) -> (r : R) -> ℤ
<!-- PINNED-SIGNATURE:END -->


VTask.clog : {R : Type u_1} -> [Semifield R] -> [LinearOrder R] -> [FloorSemiring R] -> (b : ℕ) -> (r : R) -> ℤ

The type parameter `R` is the ordered semifield in which `r` lives; the three instance arguments supply the algebraic structure (`Semifield`), the ordering (`LinearOrder`), and the ability to take floors and ceilings (`FloorSemiring`). The argument `b` is the base of the logarithm, a natural number. The argument `r` is the value whose ceiling logarithm is being computed.

## Conventions

When the base `b` is 0, the result is defined to be 0 for every `r`, because no meaningful notion of "least power of 0" exists. When the base `b` is 1, the result is also defined to be 0 for every `r`, because all powers of 1 are 1, making a finite ceiling logarithm ill-defined in the usual sense; the convention returns 0. When `r` is 0, the result is 0 regardless of the base. When `r` is 1, the result is 0 regardless of the base, reflecting that `b ^ 0 = 1 ≥ 1`.

## Worked examples

- Claim: `VTask.clog 2 (4 : ℚ) = 2` — in base 2, the least power ≥ 4 is 2² = 4, so the ceiling log is 2.

- Claim: `VTask.clog 2 (5 : ℚ) = 3` — in base 2, 2² = 4 < 5 and 2³ = 8 ≥ 5, so the ceiling log is 3.

- Claim: `VTask.clog 2 (1/4 : ℚ) = -2` — here `r = 1/4 < 1`, so we use the small-side branch; 2^(−2) = 1/4 ≥ 1/4, and 2^(−3) = 1/8 < 1/4, so the ceiling log is −2.

- Claim: `VTask.clog 10 (1 : ℚ) = 0` — any base raised to 0 equals 1, which equals `r`, so the ceiling log is 0.

- Claim: `VTask.clog 0 (42 : ℚ) = 0` — base 0 is a degenerate case; the result is always 0.

- Claim: `VTask.clog 1 (100 : ℚ) = 0` — base 1 is a degenerate case; the result is always 0.

## Boundaries

- **Base 0**: `VTask.clog 0 r = 0` for all `r`, by convention.
- **Base 1**: `VTask.clog 1 r = 0` for all `r`, by convention.
- **r = 0**: `VTask.clog b 0 = 0` for all `b`.
- **r = 1**: `VTask.clog b 1 = 0` for all `b`, since `b ^ 0 = 1 ≥ 1`.
- **r ≥ 1**: the function delegates to the natural-number ceiling logarithm of `⌈r⌉₊`, returning a non-negative integer.
- **0 < r ≤ 1**: the function returns a non-positive integer, computed via the floor of `r⁻¹`.
- **r < 0**: because `R` is a semifield with `FloorSemiring`, negative values have `⌊r⌋₊ = 0` and `⌈r⌉₊ = 0`; the function evaluates to 0 via the boundary conventions.
- The function satisfies the key inequality `r ≤ b ^ (VTask.clog b r)` whenever the base is valid (b ≥ 2) and r > 0.
- The function is related to its floor counterpart by `VTask.clog b r⁻¹ = -(VTask.log b r)`, i.e., inversion of the argument negates and swaps floor/ceiling.

## Not to be confused with

- **`Int.log` (integer floor logarithm)**: the *greatest* integer `n` with `b ^ n ≤ r`, the floor analogue; `VTask.clog` is its ceiling counterpart.
- **`Nat.clog`**: the ceiling logarithm restricted to natural numbers with a natural-number result; `VTask.clog` generalises this to an ordered semifield input and returns an integer, handling values less than 1 via negation.
- **`Real.logb`**: the real-valued logarithm in base `b`; `VTask.clog` is its ceiling rounded to an integer, not the same as rounding `Real.logb` directly (they agree for non-degenerate inputs via `Real.ceil_logb_natCast`).