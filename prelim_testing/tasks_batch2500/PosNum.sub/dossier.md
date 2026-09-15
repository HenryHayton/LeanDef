## Object

This is subtraction on strictly positive binary numerals (`PosNum`), with a clamping convention: when the true mathematical difference would be zero or negative (i.e., when `a ≤ b`), the result is defined to be `1` (the smallest `PosNum`) rather than zero or a negative number. When `a > b` the result is the ordinary positive difference `a - b`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sub : (a b : PosNum) -> PosNum
<!-- PINNED-SIGNATURE:END -->


VTask.sub : (a b : PosNum) -> PosNum

The first argument `a` is the minuend (the number being subtracted from). The second argument `b` is the subtrahend (the number being subtracted). Both are strictly positive binary numerals, and the result is likewise a strictly positive binary numeral.

## Conventions

Because `PosNum` cannot represent zero or negative values, the subtraction is clamped: whenever the true integer difference `a - b` would be zero or negative (i.e., `a ≤ b`), the function returns `1` instead of an out-of-range value.

## Worked examples

- Claim: `VTask.sub 5 3 = 2` (ordinary subtraction, `a > b`)
  ```lean
  example : VTask.sub 5 3 = 2 := by decide
  ```

- Claim: `VTask.sub 3 5 = 1` (clamped case, `a < b`)
  ```lean
  example : VTask.sub 3 5 = 1 := by decide
  ```

- Claim: `VTask.sub 4 4 = 1` (equal arguments, difference would be zero, so result is `1`)
  ```lean
  example : VTask.sub 4 4 = 1 := by decide
  ```

- Claim: `VTask.sub 7 1 = 6`
  ```lean
  example : VTask.sub 7 1 = 6 := by decide
  ```

## Boundaries

- When `a = b`: the true difference is zero, which is not representable as a `PosNum`, so the result is `1`.
- When `a < b`: the true difference is negative, which is not representable, so the result is `1`.
- When `a = 1` and `b = 1`: the smallest possible inputs both equal, result is `1`.
- The minimum possible output is always `1`; the function never returns zero.
- The function is not symmetric: `VTask.sub a b` and `VTask.sub b a` generally differ whenever `a ≠ b`.

## Not to be confused with

- `ZNum.sub` / subtraction on `ZNum`: that type includes zero and negative values, so no clamping is needed.
- `Nat.sub`: natural-number monus, which clamps to `0` rather than `1` when the result would be non-positive.
- `PosNum.pred`: computes the predecessor of a single `PosNum`, also with a boundary convention at `1`, but takes only one argument.