## Object

`VTask.bitwise f m n` is the integer obtained by applying the boolean function `f` independently to each corresponding bit position in the two's-complement binary representations of the integers `m` and `n`. Concretely, the bit at position `k` in the result is `f (bit k of m) (bit k of n)`. Because integers are represented in two's complement with an infinite sign extension, every bit position is well-defined: a non-negative integer has `false` (0) bits beyond its most-significant 1, while a negative integer has `true` (1) bits beyond its most-significant 0.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.bitwise : (f : Bool → Bool → Bool) -> ℤ → ℤ → ℤ
<!-- PINNED-SIGNATURE:END -->


`VTask.bitwise : (f : Bool → Bool → Bool) -> ℤ → ℤ → ℤ`

The first argument `f` is the pointwise boolean operation to be applied at each bit position. The second argument is the left operand integer whose bits serve as the first input to `f`. The third argument is the right operand integer whose bits serve as the second input to `f`.

## Conventions

Negative integers are represented in two's complement with infinite sign extension: a negative integer has infinitely many `true` (1) bits beyond its finite bit pattern, while a non-negative integer has infinitely many `false` (0) bits. This convention ensures that `VTask.bitwise f m n` is always a well-defined integer, even when `f false false ≠ false` (which would make a non-negative result impossible to represent finitely). When `f false false = true`, applying `VTask.bitwise f` to two non-negative integers yields a negative integer.

## Worked examples

- Claim: For every bit position `k`, `testBit (VTask.bitwise f m n) k = f (testBit m k) (testBit n k)` — i.e., the result's bits are exactly the pointwise application of `f`.

- Claim: `VTask.bitwise and = Int.land` — applying `VTask.bitwise` with boolean `and` recovers the standard integer bitwise AND.

- Claim: `VTask.bitwise or = Int.lor` — applying `VTask.bitwise` with boolean `or` recovers the standard integer bitwise OR.

- Claim: `VTask.bitwise xor = Int.xor` — applying `VTask.bitwise` with boolean `xor` recovers the standard integer bitwise XOR.

- Claim: For non-negative integers `m n : ℕ`, `VTask.bitwise f (↑m : ℤ) (↑n : ℤ)` agrees with the natural-number bitwise operation `natBitwise f m n` — the non-negative branch introduces no sign correction.

- Claim: For a non-negative `m : ℕ` and a negative integer `-[n+1]`, `VTask.bitwise f (↑m : ℤ) (-[n+1])` applies `f` with the bits of `n+1` complemented, reflecting the two's-complement representation of the negative argument.

## Boundaries

- When `f false false = true`, two non-negative integers can produce a negative result, because infinitely many upper bit positions yield `true`. This is well-defined: the result is a negative integer in two's complement.
- When `f false false = false` and both inputs are non-negative, the result is non-negative (only finitely many bits can be `true`).
- `VTask.bitwise f 0 0 = 0` when `f false false = false`, and `VTask.bitwise f 0 0 = -1` when `f false false = true` (all bits `true` corresponds to −1 in two's complement).
- The function is total: it is defined for all integers and all boolean functions `f`, with no domain restriction.

## Not to be confused with

- `Int.land` / `Int.lor` / `Int.xor`: these are the specific named bitwise operations; `VTask.bitwise` is their common generalisation parametrised by an arbitrary boolean function.
- `Nat.bitwise`: the analogous operation on natural numbers, which does not handle negative integers or two's-complement sign extension.
- `Int.testBit`: this retrieves a single bit from one integer, whereas `VTask.bitwise` combines corresponding bits of two integers into a new integer.