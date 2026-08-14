## Object

`VTask.land` computes the bitwise AND of two integers. For each bit position `k`, the `k`-th bit of the result is 1 if and only if the `k`-th bit of both inputs is 1. The integers are treated in their two's-complement binary representation, extended to infinite width (negative integers have infinitely many 1-bits above their magnitude).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.land : ℤ → ℤ → ℤ
<!-- PINNED-SIGNATURE:END -->


`VTask.land : ℤ → ℤ → ℤ`

The first argument is the left operand integer; the second argument is the right operand integer. Both are arbitrary integers and there are no sign restrictions.

## Conventions

The function handles all four sign combinations (non-negative/non-negative, non-negative/negative, negative/non-negative, negative/negative) by appealing to the two's-complement infinite-precision model: a non-negative integer `n` has its natural binary expansion with leading zeros, while a negative integer `-[k+1]` (i.e., `-(k+1)`) has the bit pattern of `k` bitwise-complemented, viewed as infinitely extended with leading ones. There are no junk values: the function is total on all of ℤ × ℤ.

## Worked examples

- Claim: `VTask.land 6 5 = 4` (both non-negative: 6 = 0b110, 5 = 0b101, AND = 0b100 = 4)
  ```lean
  example : VTask.land 6 5 = 4 := by native_decide
  ```

- Claim: `VTask.land 12 15 = 12` (both non-negative: 12 = 0b1100, 15 = 0b1111, AND = 0b1100 = 12)
  ```lean
  example : VTask.land 12 15 = 12 := by native_decide
  ```

- Claim: `VTask.land (-2) (-3) = -4` (both negative: in two's complement, -2 = ...11111110, -3 = ...11111101, AND = ...11111100 = -4)
  ```lean
  example : VTask.land (-2) (-3) = -4 := by native_decide
  ```

- Claim: `VTask.land 0 0 = 0` (AND of zero with zero is zero)
  ```lean
  example : VTask.land 0 0 = 0 := by native_decide
  ```

## Boundaries

- `VTask.land n 0 = 0` and `VTask.land 0 n = 0` for any `n : ℤ`, since zero has no set bits.
- `VTask.land n (-1) = n` for any `n : ℤ`, since −1 in two's complement has all bits set.
- `VTask.land n n = n` for any `n : ℤ` (idempotence).
- For two negative inputs `-[m+1]` and `-[n+1]`, the result is `-(m ||| n + 1)`, which is always negative.
- For a non-negative and a negative input, the result is always non-negative (since the infinite leading ones of the negative number are masked off by the leading zeros of the non-negative number).

## Not to be confused with

- `VTask.lor` (bitwise OR of two integers): returns a 1-bit wherever *either* operand has a 1-bit, not just both.
- `VTask.lxor` (bitwise XOR of two integers): returns a 1-bit wherever the two operands *differ*, not where both are 1.
- `Nat.land` (bitwise AND restricted to natural numbers): only defined for `ℕ`, so it does not handle negative integers or the two's-complement sign conventions.