## Object

`VTask.bit1` is the operation on binary natural numbers (`Num`) that appends a binary digit `1` to the right (least-significant) end of the number's binary representation. Equivalently, it computes the arithmetic value `2 * n + 1`, mapping every non-negative integer `n` to the next odd number above `2 * n`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.bit1 : Num → Num
<!-- PINNED-SIGNATURE:END -->


VTask.bit1 : Num → Num

The sole argument is the `Num` value (a non-negative binary natural number) to which the bit `1` is appended. The result is a `Num` representing the value `2 * n + 1`.

## Conventions

When the input is the zero element of `Num`, the result is `1` (i.e., the one-bit number `1`), because appending `1` to the empty/zero representation yields the single-bit value `1`.

## Worked examples

- Claim: `VTask.bit1 0 = 1` — appending a 1 to zero yields the number one.
  ```lean
  example : VTask.bit1 0 = 1 := by decide
  ```

- Claim: `VTask.bit1 1 = 3` — the binary representation of 1 is `1`; appending a `1` gives `11` in binary, which equals 3.
  ```lean
  example : VTask.bit1 1 = 3 := by decide
  ```

- Claim: `VTask.bit1 2 = 5` — the binary representation of 2 is `10`; appending a `1` gives `101` in binary, which equals 5.
  ```lean
  example : VTask.bit1 2 = 5 := by decide
  ```

- Claim: `VTask.bit1 5 = 11` — the binary representation of 5 is `101`; appending a `1` gives `1011` in binary, which equals 11.
  ```lean
  example : VTask.bit1 5 = 11 := by decide
  ```

## Boundaries

- **Input `0`**: The special case; since `0` in `Num` has no `pos` representation, the function directly returns `1`.
- **Any `pos n`**: The output is always a `pos` value (never zero), since `2 * n + 1 ≥ 1` for all `n ≥ 0`.
- **Parity**: The output is always odd, because `2 * n + 1` is odd for every `n`.
- The function is total; there are no undefined inputs.

## Not to be confused with

- **`VTask.bit0`**: The analogous operation that appends a `0` bit, computing `2 * n` (always even) rather than `2 * n + 1`.
- **`PosNum.bit1`**: The same operation restricted to the strictly-positive binary numeral type `PosNum`; `VTask.bit1` lifts this to all of `Num` by handling the zero case separately.
- **`Nat.bit1`** (or generic `bit1` in older Mathlib): A generic `bit1` defined as `2 * n + 1` at the `Nat` or semiring level; conceptually the same arithmetic, but operates on a different type.
