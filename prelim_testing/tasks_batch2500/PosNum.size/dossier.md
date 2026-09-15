## Object

`VTask.size` computes the number of bits required to represent a positive binary numeral, returned as a `PosNum`. Concretely, it counts how many binary digits the numeral has when written in standard binary notation (i.e., ⌊log₂ n⌋ + 1 for a positive integer n).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.size : PosNum → PosNum
<!-- PINNED-SIGNATURE:END -->


VTask.size : PosNum → PosNum

The sole argument is the positive binary numeral whose bit-length is to be computed. The result is itself a `PosNum` giving that bit-length.

## Conventions

There are no junk-value conventions: `VTask.size` is a total function defined on all `PosNum` values, and the output is always a valid `PosNum` (at least 1, since every positive numeral has at least one bit).

## Worked examples

- Claim: `VTask.size 1 = 1` (the numeral 1 in binary is a single bit)
  ```lean
  example : VTask.size 1 = 1 := by decide
  ```

- Claim: `VTask.size (PosNum.bit0 1) = 2` (the numeral 2 in binary is `10`, which has 2 bits)
  ```lean
  example : VTask.size (PosNum.bit0 1) = 2 := by decide
  ```

- Claim: `VTask.size (PosNum.bit1 (PosNum.bit0 1)) = 3` (the numeral 5 in binary is `101`, which has 3 bits)
  ```lean
  example : VTask.size (PosNum.bit1 (PosNum.bit0 1)) = 3 := by decide
  ```

- Claim: For any `PosNum` `n`, `(VTask.size n : ℕ) = Nat.size (n : ℕ)`, i.e., the `PosNum` bit-count agrees with `Nat.size` after coercion.

## Boundaries

- The smallest input is `1` (the `PosNum` representing the integer 1), and `VTask.size 1 = 1`. There is no zero in `PosNum`, so the output is always at least 1.
- For a `k`-bit numeral (i.e., a `PosNum` in the range [2^(k−1), 2^k − 1]), `VTask.size` returns the `PosNum` equal to `k`.
- The function is structurally recursive on the `PosNum` constructors and terminates for every well-formed input.

## Not to be confused with

- `PosNum.natSize`: a related function that returns a plain `ℕ` rather than a `PosNum`; it equals `(VTask.size n : ℕ)` for all `n`.
- `Nat.size`: the corresponding function on natural numbers, which counts bits in the same way but operates on `ℕ` and returns `ℕ`; it equals `(VTask.size n : ℕ)` after coercing a `PosNum` to `ℕ`.
- `Num.size`: a size function defined on `Num` (which includes zero), not on the strictly-positive `PosNum` type.