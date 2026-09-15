## Object

The binary operation of multiplication on the type `Num` of binary natural numbers. Given two `Num` values, it returns their product as a `Num`, consistent with ordinary natural-number multiplication under the canonical embedding `Num → ℕ`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mul : Num → Num → Num
<!-- PINNED-SIGNATURE:END -->


`VTask.mul : Num → Num → Num`

The first argument is the left multiplicand and the second is the right multiplicand, both non-negative binary numerals of type `Num`.

## Conventions

Multiplying `0` on the left by any `Num` value yields `0` (zero is absorbing on the left). Multiplying any `Num` value by `0` on the right likewise yields `0` (zero is absorbing on the right). When both arguments are positive (represented as `pos a` and `pos b` for `PosNum` values `a` and `b`), the result is the positive numeral `pos (a * b)`.

## Worked examples

- Claim: `VTask.mul 0 5 = 0`
  ```lean
  example : VTask.mul 0 5 = 0 := by decide
  ```

- Claim: `VTask.mul 3 0 = 0`
  ```lean
  example : VTask.mul 3 0 = 0 := by decide
  ```

- Claim: `VTask.mul 3 4 = 12`
  ```lean
  example : VTask.mul 3 4 = 12 := by decide
  ```

- Claim: The cast of `VTask.mul m n` to `ℕ` equals the product of the casts of `m` and `n`; that is, `((VTask.mul m n : Num) : ℕ) = (m : ℕ) * (n : ℕ)` for all `m n : Num`.

## Boundaries

- If either argument is `0`, the result is always `0` regardless of the other argument, so `0` is an absorbing element (annihilator) for multiplication.
- When both arguments are positive, the multiplication is delegated to `PosNum` multiplication, so there is no overflow or wrapping; the result is always the exact binary representation of the arithmetic product.
- The operation is total: it is defined for every pair of `Num` values with no preconditions.

## Not to be confused with

- `PosNum.mul`: multiplication restricted to strictly positive binary numerals; it does not handle the zero case and cannot return zero.
- `ZNum.mul`: multiplication on signed binary numerals, which additionally handles negative values.
- `Nat.mul`: multiplication on `ℕ`; while numerically equivalent under the canonical embedding, it operates on a different type.