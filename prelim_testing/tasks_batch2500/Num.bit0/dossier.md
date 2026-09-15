## Object

`VTask.bit0` is the function on binary natural numbers (`Num`) that appends a binary digit `0` to the right end of the binary representation of its argument. Equivalently, it multiplies the argument by 2: if the argument represents the value *n*, the result represents *2n*.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.bit0 : Num → Num
<!-- PINNED-SIGNATURE:END -->


`VTask.bit0 : Num → Num`

The single argument is a non-negative integer in binary (`Num`) whose binary representation is to be left-shifted by one place (i.e., doubled) by appending a `0` bit at the least-significant position.

## Conventions

When the input is zero (`0 : Num`), the result is also zero (`0 : Num`), since zero with a trailing `0` appended is still zero in the canonical binary representation (there is no canonical non-zero `Num` for the value 0).

## Worked examples

- Claim: `VTask.bit0 0 = 0` — appending a `0` to zero yields zero.
  ```lean
  example : VTask.bit0 0 = 0 := by decide
  ```

- Claim: `VTask.bit0 1 = 2` — appending a `0` to the binary representation of 1 (which is `1`) yields `10` in binary, i.e., 2.
  ```lean
  example : VTask.bit0 1 = 2 := by decide
  ```

- Claim: `VTask.bit0 3 = 6` — appending a `0` to `11` in binary yields `110`, i.e., 6.
  ```lean
  example : VTask.bit0 3 = 6 := by decide
  ```

- Claim: `VTask.bit0 5 = 10` — appending a `0` to `101` in binary yields `1010`, i.e., 10.
  ```lean
  example : VTask.bit0 5 = 10 := by decide
  ```

## Boundaries

- **Input is zero**: `VTask.bit0 0 = 0`. The canonical representation of `Num` does not allow a leading-zero form like `pos 0`, so doubling zero stays zero.
- **Input is positive**: For any positive `n`, `VTask.bit0 n` is always even and strictly positive; it is never zero.
- **The function is total**: it is defined for every value of `Num` with no preconditions.

## Not to be confused with

- `VTask.bit1 : Num → Num` — appends a `1` bit instead of a `0`, yielding the odd number `2n + 1`.
- `PosNum.bit0 : PosNum → PosNum` — the same bit-appending operation but restricted to the strictly-positive binary number type `PosNum`; `VTask.bit0` lifts this to all of `Num` by handling the zero case separately.
- Left-shift or multiplication by 2 on `Nat` — conceptually the same operation but on a different type; `VTask.bit0` operates structurally on the binary representation inside `Num`.
