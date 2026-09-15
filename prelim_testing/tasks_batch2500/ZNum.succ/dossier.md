## Object

`VTask.succ` computes the successor of a signed binary integer (`ZNum`), i.e., the unique element that is exactly 1 greater than the input. It is the binary-number analogue of the usual integer successor function `n ↦ n + 1`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.succ : ZNum → ZNum
<!-- PINNED-SIGNATURE:END -->


`VTask.succ : ZNum → ZNum`

The single argument is any signed binary integer (`ZNum`), which may be zero, a positive binary numeral, or a negative binary numeral.

## Conventions

There are no junk-value or out-of-domain conventions: `VTask.succ` is a total function defined for every `ZNum`, including zero and all negative values.

## Worked examples

- Claim: `VTask.succ 0 = 1` (the successor of zero is one)
- Claim: `VTask.succ 3 = 4` (the successor of a positive `ZNum` increments it by one)
- Claim: `VTask.succ (-1) = 0` (the successor of −1 is zero, crossing the sign boundary)
- Claim: `VTask.succ (-3) = -2` (the successor of a negative `ZNum` moves it one step toward zero)
- Claim: For every `ZNum` `n`, casting `VTask.succ n` to any `AddGroupWithOne` equals the cast of `n` plus 1 (i.e., `(VTask.succ n : α) = n + 1`)

## Boundaries

- At `0`: `VTask.succ 0 = 1`, moving from the zero constructor to the `pos` constructor.
- At `neg 1` (i.e., the `ZNum` value −1): the result is `0`, since the underlying positive numeral's predecessor is empty/zero, so the result lands back on the zero constructor.
- For all `pos a`: the result stays in the `pos` constructor, using `PosNum.succ` to increment the underlying positive numeral.
- For `neg a` with `a > 1`: the result is a negative `ZNum` one step closer to zero, obtained by taking the predecessor of the positive numeral `a`.
- The function is total with no undefined cases.

## Not to be confused with

- `ZNum.pred`: the predecessor function (decreases by 1 rather than increasing), the inverse of `VTask.succ`.
- `PosNum.succ`: the successor function for strictly *positive* binary numerals only; it does not handle zero or negative values.
- `Nat.succ` / `Num.succ`: successor for natural-number types, which have no negative values and thus no sign-crossing behavior.