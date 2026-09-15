## Object

`VTask.gcdA x y` is the first Bézout coefficient for the pair of integers `x` and `y`: the integer `a` such that `gcd(x, y) = x · a + y · b` for some companion integer `b` (given by `gcdB x y`). It is the "x-multiplier" in the extended Euclidean algorithm applied to `x` and `y`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.gcdA : ℤ → ℤ → ℤ
<!-- PINNED-SIGNATURE:END -->


VTask.gcdA : ℤ → ℤ → ℤ

The first argument is the integer `x` whose coefficient `a` is being computed. The second argument is the integer `y`, the other input to the extended GCD. Both arguments are arbitrary integers (any sign, zero included).

## Conventions

The Bézout coefficient `a` is not uniquely determined by `x` and `y` alone; a specific canonical choice is made following the convention inherited from the natural-number extended GCD, extended to negative inputs by negating the coefficient when the first argument is negative. No special junk value is needed since the function is total over all integers.

## Worked examples

- Claim: `VTask.gcdA 6 10 = 2`, reflecting the identity `gcd(6,10) = 2 = 6·2 + 10·(−1)`.

- Claim: For `x = 3` and `y = 5`, `VTask.gcdA 3 5` is the integer `a` satisfying `gcd(3,5) = 1 = 3·a + 5·b` for companion `b = VTask.gcdB 3 5`.

- Claim: For negative first argument, `VTask.gcdA (-6) 10 = -2`, since negating the first argument negates the coefficient: `gcd(6,10) = gcd(-6,10) = 2 = (-6)·(-2) + 10·(-1)`.

- Claim: `VTask.gcdA 0 5 = 0`, since `gcd(0,5) = 5 = 0·0 + 5·1`, so the first Bézout coefficient is `0`.

## Boundaries

- When `x = 0`: `gcd(0, y) = |y|`, and the identity becomes `|y| = 0 · a + y · b`, so `a` is conventionally `0`.
- When `y = 0`: `gcd(x, 0) = |x|`, and the identity becomes `|x| = x · a + 0 · b`, so `a` is conventionally `1` for positive `x` and `−1` for negative `x`.
- When both are `0`: `gcd(0, 0) = 0`, and `a = 0` by convention.
- When `x` is negative, the coefficient is the negation of the coefficient that would be obtained for `|x|`.
- The defining property is always: `(gcd x y : ℤ) = x * gcdA x y + y * gcdB x y`.

## Not to be confused with

- `VTask.gcdB x y`: the companion second Bézout coefficient `b` in the same identity; `gcdA` is specifically the coefficient of `x`, not `y`.
- `Int.gcd x y`: the non-negative GCD value itself, not one of its Bézout coefficients.
- `Nat.gcdA m n`: the natural-number version of the same coefficient; `VTask.gcdA` extends this to integers by handling sign of the first argument.