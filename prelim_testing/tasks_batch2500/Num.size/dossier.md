## Object

`VTask.size` computes the number of bits needed to represent a non-negative binary numeral (`Num`). For a positive numeral whose highest set bit has position *k* (counting from 1 at the least-significant end), the result is *k*. Concretely, a positive integer *n* satisfies `size n = ⌊log₂ n⌋ + 1`. The special case `size 0 = 0` reflects the convention that zero requires zero bits.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.size : Num → Num
<!-- PINNED-SIGNATURE:END -->


VTask.size : Num → Num

The single argument is the non-negative binary numeral whose bit-length is to be measured.

## Conventions

The number zero is assigned a size of zero, rather than one (which might be argued on representation grounds). This is a junk-value / boundary convention: the function is otherwise the standard bit-length (floor of log base 2, plus 1) for positive inputs.

## Worked examples

- Claim: `VTask.size 0 = 0` — zero requires zero bits by convention.
  ```lean
  example : VTask.size 0 = 0 := by decide
  ```

- Claim: `VTask.size 1 = 1` — the numeral 1 is represented by a single bit.
  ```lean
  example : VTask.size 1 = 1 := by decide
  ```

- Claim: `VTask.size 4 = 3` — the numeral 4 = 0b100 requires 3 bits.
  ```lean
  example : VTask.size 4 = 3 := by decide
  ```

- Claim: `VTask.size 7 = 3` — the numeral 7 = 0b111 requires 3 bits.
  ```lean
  example : VTask.size 7 = 3 := by decide
  ```

- Claim: `VTask.size 8 = 4` — the numeral 8 = 0b1000 requires 4 bits.
  ```lean
  example : VTask.size 8 = 4 := by decide
  ```

## Boundaries

- **Zero**: `size 0 = 0`. This is the only numeral for which the result is zero; every positive numeral has size at least 1.
- **Powers of two**: `size (2^k) = k + 1`, since `2^k` has exactly `k+1` bits.
- **One below a power of two**: `size (2^k - 1) = k`, since `2^k - 1` has `k` bits all set.
- The function is monotone on positive numerals: if `m ≤ n` and both are positive, then `size m ≤ size n` (though not strictly).

## Not to be confused with

- `Nat.log 2 n` — this is the floor of the base-2 logarithm, which equals `VTask.size n - 1` for positive `n`, and differs at zero (`Nat.log 2 0 = 0` as well, but the off-by-one means they diverge for positive values).
- `PosNum.size` — the analogous function on the strictly-positive numeral type `PosNum`; `VTask.size` lifts it to `Num` by adding the zero case.
- Bit-count (popcount) — counts the number of *set* bits, not the position of the highest set bit.