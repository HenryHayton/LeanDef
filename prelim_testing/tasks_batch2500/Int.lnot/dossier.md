## 1. Object

`VTask.lnot` is the bitwise NOT (one's complement negation) of an integer. It flips every bit in the two's-complement binary representation of its input. Concretely, for any integer `n`, the result satisfies `VTask.lnot n = -(n + 1)`, which is the classical identity `~n = -n - 1` familiar from most programming languages.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lnot : ℤ → ℤ
<!-- PINNED-SIGNATURE:END -->


`VTask.lnot : ℤ → ℤ`

The single argument is the integer whose bits are to be flipped. It may be any integer — non-negative, negative, or zero — and the result is always an integer of the opposite sign class.

## 3. Conventions

Integers are represented in two's-complement with infinitely many bits, so non-negative integers have an infinite string of leading `0` bits and negative integers have an infinite string of leading `1` bits. Flipping all bits therefore maps every non-negative integer `n` to the negative integer `-(n+1)`, and every negative integer `-(n+1)` back to the non-negative integer `n`.

## 4. Worked Examples

- Claim: `VTask.lnot 0 = -1` (zero, all bits `0`, becomes all bits `1`, i.e. −1)
- Claim: `VTask.lnot (-1) = 0` (−1, all bits `1`, becomes all bits `0`, i.e. 0)
- Claim: `VTask.lnot 4 = -5` (binary `…0000100` flipped gives `…1111011`, the two's-complement representation of −5)
- Claim: `VTask.lnot (-5) = 4` (inverse of the above; `lnot` is an involution)
- Claim: For every integer `n`, `VTask.lnot (VTask.lnot n) = n` (bitwise NOT is its own inverse)
- Claim: For every integer `n` and bit index `k`, `Int.testBit (VTask.lnot n) k = !Int.testBit n k` (each bit is individually flipped)

## 5. Boundaries

- At `n = 0`: `VTask.lnot 0 = -1`. Zero's representation (all `0` bits) flips to all `1` bits, which is −1 in two's complement.
- At `n = -1`: `VTask.lnot (-1) = 0`. The all-`1`-bit pattern flips to the all-`0`-bit pattern.
- The function is total on all of `ℤ` with no undefined inputs.
- The function is an involution: applying it twice returns the original integer.
- The function interchanges the non-negative integers `{0, 1, 2, …}` with the negative integers `{-1, -2, -3, …}` in a perfect bijection.

## 6. Not to be confused with

- `Int.neg` (or unary `-`): arithmetic negation, which maps `n` to `-n`, not to `-(n+1)`.
- `Nat.lnot` (bitwise NOT restricted to natural numbers): because natural numbers have no sign bit, `Nat.lnot` requires a bit-width parameter and produces a finite result, unlike `VTask.lnot` which operates on all integers without a width bound.
- `Bool.not` / `!`: logical (boolean) NOT, which operates on a single truth value rather than flipping all bits of an integer.
