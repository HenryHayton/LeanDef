## Object

`VTask.natSize` computes the number of bits required to represent a non-negative binary numeral (`Num`) as a natural number. Equivalently, for a positive integer `n`, it returns ⌊log₂ n⌋ + 1, the length of the binary representation of `n`. The special case `natSize 0 = 0` is chosen by convention.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.natSize : Num → ℕ
<!-- PINNED-SIGNATURE:END -->


`VTask.natSize : Num → ℕ`

The sole argument is a `Num` value — a non-negative binary numeral, either zero or a positive binary number (`PosNum`). The result is a natural number giving the bit-width of that numeral.

## Conventions

The bit-size of zero is defined to be `0`, even though one might argue zero requires one bit to write down. This is a deliberate junk-value / boundary convention.

## Worked examples

- Claim: `VTask.natSize 0 = 0` (zero is represented as needing zero bits)
  ```lean
  example : VTask.natSize 0 = 0 := by decide
  ```

- Claim: `VTask.natSize 1 = 1` (the number 1 needs one bit)
  ```lean
  example : VTask.natSize 1 = 1 := by decide
  ```

- Claim: `VTask.natSize 4 = 3` (the number 4 = 100₂ needs three bits)
  ```lean
  example : VTask.natSize 4 = 3 := by decide
  ```

- Claim: `VTask.natSize 7 = 3` (the number 7 = 111₂ needs three bits)
  ```lean
  example : VTask.natSize 7 = 3 := by decide
  ```

- Claim: `VTask.natSize 8 = 4` (the number 8 = 1000₂ needs four bits)
  ```lean
  example : VTask.natSize 8 = 4 := by decide
  ```

## Boundaries

- At `0`: returns `0` by definition, not `1`. This is the only case where the result differs from ⌊log₂ n⌋ + 1.
- At `1`: returns `1`, consistent with the single-bit binary representation `1₂`.
- At powers of two `2^k`: returns `k + 1`, since `2^k` in binary is `1` followed by `k` zeros.
- At `2^k - 1` (all-ones patterns): also returns `k`, since these numbers have exactly `k` bits.

## Not to be confused with

- `PosNum.natSize`: the analogous function on strictly positive binary numerals; `VTask.natSize` delegates to it for nonzero inputs and handles the `0` case separately.
- `Num.log2` or similar logarithm functions: those may return ⌊log₂ n⌋ (one less than the bit-width for positive `n`) and may have different conventions at zero.
- `Nat.log 2 n`: the base-2 logarithm on natural numbers, which equals `VTask.natSize n - 1` for positive `n` and is also `0` at `0`, but differs in off-by-one from `VTask.natSize`.