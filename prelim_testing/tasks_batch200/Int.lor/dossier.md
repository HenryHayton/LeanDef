## VTask.lor

### Object

`VTask.lor` computes the bitwise OR of two integers. Given two integers `m` and `n`, it returns the unique integer whose two's-complement binary representation has a `1` bit in position `k` if and only if at least one of `m` or `n` has a `1` bit in position `k`. This extends the familiar bitwise OR on non-negative integers to all of ℤ via two's-complement arithmetic, where negative integers are treated as having infinitely many leading `1` bits.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lor : ℤ → ℤ → ℤ
<!-- PINNED-SIGNATURE:END -->


The first argument is the left operand of the bitwise OR; the second argument is the right operand. Both are arbitrary integers (positive, negative, or zero), and the result is an integer.

### Conventions

Negative integers are handled via two's-complement: a negative integer is treated as having an infinite sequence of leading `1` bits. As a consequence, for example, `VTask.lor (-1) n = -1` for all integers `n`, since `-1` has all bits set. The operation is total on all of ℤ with no junk values.

### Worked examples

- Claim: `VTask.lor 6 3 = 7` (both non-negative: `0b110 ||| 0b011 = 0b111`)
  ```lean
  example : VTask.lor 6 3 = 7 := by decide
  ```

- Claim: `VTask.lor 5 5 = 5` (idempotence: OR of a value with itself)
  ```lean
  example : VTask.lor 5 5 = 5 := by decide
  ```

- Claim: `VTask.lor (-4) 3 = -1` (negative with positive: in two's-complement, `-4 = ...11111100` and `3 = ...00000011`, so their OR is `...11111111 = -1`)

- Claim: `VTask.lor (-3) (-5) = -1` (two negatives: `-3 = ...11111101`, `-5 = ...11111011`, OR = `...11111111 = -1`)

- Claim: `VTask.lor 0 n = n` for any integer `n` (0 is the identity element)

### Boundaries

- When both arguments are zero, the result is zero.
- When either argument is `-1` (all bits set in two's-complement), the result is always `-1`, regardless of the other argument.
- When one argument is `0`, the result equals the other argument exactly.
- For two negative inputs `-[m+1]` and `-[n+1]` (in the internal representation), the result is again negative, specifically `-[m &&& n + 1]`, meaning the OR of two negatives is always negative.
- For one non-negative and one negative input, the result is always negative (or zero only in degenerate cases not achievable with these types).

### Not to be confused with

- `VTask.land` (bitwise AND of two integers): selects bits where *both* operands have a `1`, rather than *at least one*.
- `VTask.lxor` (bitwise XOR of two integers): selects bits where the two operands *differ*, rather than where at least one is `1`.
- Logical OR (`||` on `Bool` or `∨` on `Prop`): those operate on truth values, not on the bit-patterns of integer representations.