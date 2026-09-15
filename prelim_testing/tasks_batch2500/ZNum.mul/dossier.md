## Object

`VTask.mul` computes the product of two integers represented in the `ZNum` type — a binary numeral representation of integers that uses the constructors `0` (zero), `pos` (positive), and `neg` (negative). The result is again a `ZNum` and agrees with ordinary integer multiplication.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mul : ZNum → ZNum → ZNum
<!-- PINNED-SIGNATURE:END -->


`VTask.mul : ZNum → ZNum → ZNum`

The first argument is the left multiplicand and the second argument is the right multiplicand, both integers given as `ZNum` values.

## Conventions

Multiplication by zero on either side yields `0`: if either argument is the `ZNum` zero constructor, the result is `0` regardless of the other argument. This is a junk-free convention — the representation stays canonical (zero is represented as `0`, not as `pos 0`).

## Worked examples

- Claim: `VTask.mul 0 (ZNum.pos 5) = 0` — multiplying zero by any positive number gives zero.
  ```lean
  example : VTask.mul 0 (ZNum.pos 5) = 0 := by decide
  ```

- Claim: `VTask.mul (ZNum.pos 3) (ZNum.pos 4) = ZNum.pos 12` — the product of two positive `ZNum` values is a positive `ZNum` whose magnitude is the product of the underlying `PosNum` magnitudes.
  ```lean
  example : VTask.mul (ZNum.pos 3) (ZNum.pos 4) = ZNum.pos 12 := by decide
  ```

- Claim: `VTask.mul (ZNum.pos 3) (ZNum.neg 4) = ZNum.neg 12` — a positive times a negative yields a negative.
  ```lean
  example : VTask.mul (ZNum.pos 3) (ZNum.neg 4) = ZNum.neg 12 := by decide
  ```

- Claim: `VTask.mul (ZNum.neg 3) (ZNum.neg 4) = ZNum.pos 12` — a negative times a negative yields a positive.
  ```lean
  example : VTask.mul (ZNum.neg 3) (ZNum.neg 4) = ZNum.pos 12 := by decide
  ```

## Boundaries

- When either argument is `0`, the result is always `0`, regardless of the other argument's sign or magnitude.
- When both arguments are nonzero, the sign of the result follows ordinary sign rules: `pos * pos = pos`, `neg * neg = pos`, `pos * neg = neg`, `neg * pos = neg`.
- The result's underlying `PosNum` magnitude is the product of the two arguments' `PosNum` magnitudes, computed via `PosNum` multiplication.
- The operation is commutative: `VTask.mul a b = VTask.mul b a` for all `ZNum` values.
- Casting the result to `ℤ` agrees with integer multiplication: `((VTask.mul m n : ZNum) : ℤ) = (m : ℤ) * (n : ℤ)`.

## Not to be confused with

- `ZNum.add`: addition of `ZNum` values, not multiplication.
- `Num.mul`: multiplication on the non-negative `Num` type, which has no negative constructor and thus no sign-handling case work.
- `PosNum.mul`: multiplication on strictly positive binary numerals; `VTask.mul` wraps this but additionally handles zero and signs.