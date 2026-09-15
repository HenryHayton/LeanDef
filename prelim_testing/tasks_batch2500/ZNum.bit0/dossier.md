## 1. Object

Given a signed binary numeral `n` (of type `ZNum`, which represents integers in a binary positional format), `VTask.bit0 n` is the numeral obtained by appending a binary digit `0` on the right end of `n`'s binary representation. Concretely, this doubles the value: `VTask.bit0 n = n + n = 2 * n`.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.bit0 : ZNum → ZNum
<!-- PINNED-SIGNATURE:END -->


`VTask.bit0 : ZNum → ZNum`

The single argument is the signed binary numeral to be doubled by appending a `0` bit to its binary representation.

## 3. Conventions

When the argument is the zero numeral `0`, the result is `0` (appending a zero bit to zero leaves zero, consistent with `2 * 0 = 0`). The sign of the result always matches the sign of the input: positive inputs give positive outputs and negative inputs give negative outputs.

## 4. Worked examples

- Claim: `VTask.bit0 0 = 0` — doubling zero gives zero.
  ```lean
  example : VTask.bit0 0 = 0 := by decide
  ```

- Claim: `VTask.bit0 (pos 1) = pos 2` — doubling the positive numeral 1 yields the positive numeral 2 (binary `10`).
  ```lean
  example : VTask.bit0 (ZNum.pos 1) = ZNum.pos 2 := by decide
  ```

- Claim: `VTask.bit0 (neg 3) = neg 6` — doubling the negative numeral −3 yields −6.
  ```lean
  example : VTask.bit0 (ZNum.neg 3) = ZNum.neg 6 := by decide
  ```

- Claim: For every `n : ZNum`, casting `VTask.bit0 n` to any `AddGroupWithOne` equals `n + n`.

## 5. Boundaries

- At `n = 0`: the result is exactly `0`, not `pos 0` or `neg 0` (neither of which are valid `ZNum` constructors — `ZNum` has a dedicated `0` constructor).
- For positive `n = pos p`: the result is `pos (PosNum.bit0 p)`, keeping the positive sign.
- For negative `n = neg p`: the result is `neg (PosNum.bit0 p)`, keeping the negative sign. The magnitude is doubled symmetrically with the positive case.
- The function is total on all `ZNum` values; there are no undefined or junk-value cases.

## 6. Not to be confused with

- `VTask.bit1` — appends a `1` bit instead of `0`, computing `n + n + 1` rather than `n + n`.
- `PosNum.bit0` — the analogous operation on strictly positive binary numerals only (no zero or negative case).
- `Num.bit0` — the analogous operation on non-negative binary numerals (`Num` has zero but no negative values).