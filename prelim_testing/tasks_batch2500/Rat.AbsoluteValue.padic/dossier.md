## Object

The p-adic absolute value on the rationals, promoted to a bundled `AbsoluteValue ℚ ℝ`. For a prime `p` and a rational number `x`, the p-adic absolute value is defined by writing `x = p^n · (a/b)` where neither `a` nor `b` is divisible by `p`, and setting `|x|_p = p^{-n}`; one sets `|0|_p = 0`. This gives a non-archimedean absolute value on `ℚ` satisfying the ultrametric inequality `|x + y|_p ≤ max(|x|_p, |y|_p)` (which in particular implies the ordinary triangle inequality).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.padic : (p : ℕ) -> [Fact (Nat.Prime p)] -> AbsoluteValue ℚ ℝ
<!-- PINNED-SIGNATURE:END -->


`VTask.padic : (p : ℕ) -> [Fact (Nat.Prime p)] -> AbsoluteValue ℚ ℝ`

The first argument `p` is the prime number whose p-adic absolute value is being constructed. The instance argument `[Fact (Nat.Prime p)]` is the proof, packaged in the `Fact` typeclass wrapper, that `p` is indeed a prime natural number; this ensures the construction is only invoked for genuine primes.

## Conventions

The value at zero is `0`: `VTask.padic p 0 = 0`, consistent with the convention that any absolute value sends `0` to `0`.

## Worked examples

- Claim: For `p = 2`, the 2-adic absolute value of `4` (which is `2^2`) equals `1/4`, since `4 = 2^2` has 2-adic valuation `2` and `|4|_2 = 2^{-2} = 1/4`.

- Claim: For `p = 3`, the 3-adic absolute value of `1/9 = 3^{-2}` is `9`, since the 3-adic valuation of `1/9` is `-2` and `|1/9|_3 = 3^2 = 9`.

- Claim: For any prime `p` and any integer `n : ℤ`, `VTask.padic p n ≤ 1`, because integers have non-negative p-adic valuation.

- Claim: The 5-adic absolute value satisfies the ultrametric inequality: `VTask.padic 5 (x + y) ≤ max (VTask.padic 5 x) (VTask.padic 5 y)` for all `x y : ℚ`.

- Claim: By Ostrowski's theorem, every nontrivial absolute value on `ℚ` is equivalent either to the usual real absolute value or to `VTask.padic p` for a unique prime `p`.

## Boundaries

- At `x = 0`: `VTask.padic p 0 = 0` (required by the `AbsoluteValue` axioms).
- At `x = 1`: `VTask.padic p 1 = 1` for any prime `p`, since `1` has zero p-adic valuation.
- At `x = p` (the prime itself cast to `ℚ`): `VTask.padic p p = 1/p`, since the p-adic valuation of `p` is `1`.
- At `x = p^n` for large `n`: `VTask.padic p (p^n) = p^{-n}`, which tends to `0` as `n → ∞`, demonstrating that high powers of `p` are "small" p-adically.
- For integers not divisible by `p`: `VTask.padic p x = 1`.
- The result lies in `ℝ` (via the coercion of the rational-valued padicNorm to the reals), so it is always a non-negative real number.

## Not to be confused with

- `padicNorm p x`: the rational-valued p-adic norm (returning a value in `ℚ`), not bundled as an `AbsoluteValue` structure; `VTask.padic p` is the real-valued bundled version.
- The real absolute value on `ℚ` (the archimedean counterpart in Ostrowski's theorem): unlike `VTask.padic p`, it satisfies `|n| → ∞` for integers `n → ∞`.
- `Padic p` (the completion of `ℚ` with respect to the p-adic metric): that is a new number field, not an absolute value on `ℚ` itself.