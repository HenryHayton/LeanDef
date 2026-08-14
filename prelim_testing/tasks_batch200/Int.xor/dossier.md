## Object

`VTask.xor` computes the bitwise XOR of two integers. For non-negative integers this coincides with the ordinary bitwise XOR of natural numbers. For negative integers, which are represented in two's-complement (sign-magnitude with an implicit infinite sign extension), the operation is extended so that every bit position — including the implicit sign bits — is XOR-ed. The result is an integer whose two's-complement bit pattern is the bitwise XOR of the two inputs' two's-complement bit patterns.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.xor : ℤ → ℤ → ℤ
<!-- PINNED-SIGNATURE:END -->


VTask.xor : ℤ → ℤ → ℤ

The first argument is the left integer operand. The second argument is the right integer operand. Both arguments range over all integers (positive, negative, or zero); there is no domain restriction.

## Conventions

The function is total on all of ℤ × ℤ; there are no junk-value conventions to declare.

## Worked examples

- Claim: VTask.xor 5 3 = 6 (since 0b101 XOR 0b011 = 0b110)
  ```lean
  example : VTask.xor 5 3 = 6 := by decide
  ```

- Claim: VTask.xor 0 42 = 42 (zero is the identity for XOR)
  ```lean
  example : VTask.xor 0 42 = 42 := by decide
  ```

- Claim: VTask.xor 7 7 = 0 (any integer XOR-ed with itself is zero)
  ```lean
  example : VTask.xor 7 7 = 0 := by decide
  ```

- Claim: VTask.xor (-1) 0 = -1 (−1 in two's complement is all-ones; XOR with 0 leaves it unchanged)
  ```lean
  example : VTask.xor (-1) 0 = -1 := by decide
  ```

- Claim: VTask.xor (-1) (-1) = 0 (all-ones XOR all-ones is zero)
  ```lean
  example : VTask.xor (-1) (-1) = 0 := by decide
  ```

- Claim: VTask.xor (-3) 2 = -1 (casework branch: non-negative XOR negative gives negative)
  ```lean
  example : VTask.xor (-3) 2 = -1 := by decide
  ```

- Claim: VTask.xor (-3) (-5) = 6 (casework branch: negative XOR negative gives non-negative)
  ```lean
  example : VTask.xor (-3) (-5) = 6 := by decide
  ```

## Boundaries

- **Both operands non-negative**: the result is the ordinary natural-number XOR, cast to ℤ, and is non-negative.
- **Exactly one operand negative**: the result is strictly negative (represented as a negative successor).
- **Both operands negative**: the result is non-negative, because the implicit all-ones sign halves cancel.
- **Zero**: `VTask.xor 0 n = n` and `VTask.xor n 0 = n` for all `n : ℤ`.
- **Self-XOR**: `VTask.xor n n = 0` for all `n : ℤ`.
- **−1 (all-ones)**: `VTask.xor (-1) n = -(n + 1)` (bitwise complement), and `VTask.xor (-1) (-1) = 0`.

## Not to be confused with

- `Int.bitwise` — the general bitwise combinator parameterized by an arbitrary Boolean function; `VTask.xor` is specifically the instance obtained by passing the Boolean XOR function.
- `Bool.xor` / `Nat.xor` — the XOR operations on `Bool` and `ℕ` respectively; they do not handle negative integers.
- `Xor` (the propositional connective in `Prop`) — an entirely different object expressing exclusive disjunction of propositions, not a numeric operation.
