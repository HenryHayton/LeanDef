## Object

`VTask.bit1` is the function on signed binary numerals (`ZNum`) that appends a binary `1` digit to the least-significant end of the numeral, thereby computing `2 * x + 1` for any signed numeral `x`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.bit1 : ZNum → ZNum
<!-- PINNED-SIGNATURE:END -->


`VTask.bit1 : ZNum → ZNum`

The single argument is a signed binary numeral (an element of `ZNum`, which can represent zero, a positive binary numeral, or a negative binary numeral). The result is the signed binary numeral representing `2 * x + 1`.

## Conventions

There are no junk-value conventions: the function is total and is defined by straightforward case analysis on all three constructors of `ZNum` with no edge case treated specially for non-mathematical reasons. The result is always the unique `ZNum` representing `2 * x + 1`.

## Worked examples

- Claim: `VTask.bit1 0 = 1` (appending a `1` to zero yields the numeral `1 = 2*0+1`)

- Claim: `VTask.bit1 (ZNum.pos 1) = ZNum.pos 3` (the positive numeral `1` becomes `3 = 2*1+1`)

- Claim: `VTask.bit1 (ZNum.neg 1) = ZNum.neg 1` (the negative numeral `-1` yields `-1 = 2*(-1)+1`)

- Claim: For any `ZNum` value `n`, casting `VTask.bit1 n` to an `AddGroupWithOne` gives `n + n + 1`.

## Boundaries

- At `x = 0`: the result is `1`, which equals `2 * 0 + 1`. This is consistent with the general formula.
- For positive inputs `pos n`: the result is the positive numeral obtained by appending a `1` bit, always remaining positive.
- For negative inputs `neg n`: the result requires care because `2 * (-n) + 1` can be negative, zero, or positive depending on `n`. In practice, when `n = 1` (representing `-1`), the result is `neg 1` (i.e., `-1`). For larger negative inputs like `neg 2` (representing `-2`), the result is `neg 3` (representing `-3 = 2*(-2)+1`). The result is negative for all negative inputs `n ≤ -1` (since `2n+1 ≤ -1 < 0` for `n ≤ -1`).
- The negation of `VTask.bit1 n` equals `(-n).bitm1`, linking `bit1` and the companion `bitm1` operation.

## Not to be confused with

- `ZNum.bit0`: appends a `0` bit, computing `2 * x` rather than `2 * x + 1`.
- `ZNum.bitm1`: appends a `1` bit on the negative side, computing `2 * x - 1`; it is the negation-dual of `bit1`.
- `PosNum.bit1`: the analogous operation restricted to strictly positive binary numerals, which cannot represent zero or negative values.