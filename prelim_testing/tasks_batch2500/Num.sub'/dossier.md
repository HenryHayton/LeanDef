## Object

`VTask.sub'` computes the exact integer difference of two non-negative binary numerals, returning a signed binary integer (`ZNum`) that can represent zero, a positive, or a negative result. Unlike truncated subtraction, no information is lost: if the second argument exceeds the first, the result is the appropriate negative integer.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sub' : Num → Num → ZNum
<!-- PINNED-SIGNATURE:END -->


`VTask.sub' : Num → Num → ZNum`

The first argument is the minuend — the `Num` from which the second is subtracted. The second argument is the subtrahend — the `Num` being subtracted from the first.

## Conventions

No special junk-value or out-of-domain conventions are declared: the function is total on all pairs of `Num` values and every case produces a mathematically meaningful signed result.

## Worked Examples

- Claim: `VTask.sub' 0 0 = 0`
  ```lean
  example : VTask.sub' 0 0 = 0 := by decide
  ```

- Claim: `VTask.sub' (Num.pos 3) 0 = ZNum.pos 3` (subtracting zero from a positive numeral gives the corresponding positive `ZNum`)
  ```lean
  example : VTask.sub' (Num.pos 3) 0 = ZNum.pos 3 := by decide
  ```

- Claim: `VTask.sub' 0 (Num.pos 5) = ZNum.neg 5` (subtracting a positive from zero yields a negative `ZNum`)
  ```lean
  example : VTask.sub' 0 (Num.pos 5) = ZNum.neg 5 := by decide
  ```

- Claim: `VTask.sub' (Num.pos 7) (Num.pos 3) = ZNum.pos 4`
  ```lean
  example : VTask.sub' (Num.pos 7) (Num.pos 3) = ZNum.pos 4 := by decide
  ```

- Claim: `VTask.sub' (Num.pos 3) (Num.pos 7) = ZNum.neg 4` (result is negative when the subtrahend is larger)
  ```lean
  example : VTask.sub' (Num.pos 3) (Num.pos 7) = ZNum.neg 4 := by decide
  ```

## Boundaries

- When both arguments are zero, the result is `ZNum` zero.
- When the second argument is zero and the first is positive, the result is the positive `ZNum` counterpart of the first argument — no arithmetic is performed.
- When the first argument is zero and the second is positive, the result is the negation of the second argument as a `ZNum`.
- When both arguments are positive `Num`s, the result is the signed difference, which can be positive, negative, or zero depending on their relative magnitude.
- The function is semantically faithful: for any ring (or `AddGroupWithOne`) into which `Num` and `ZNum` cast, casting `VTask.sub' m n` gives the same result as casting `m` minus casting `n`.

## Not to be confused with

- `Num.sub` (or truncated subtraction on `Num`): returns a `Num`, clamping to zero when the result would be negative, losing sign information.
- `ZNum.sub`: subtraction defined directly on `ZNum` operands, not on `Num` operands.
- `PosNum.sub'`: the underlying signed subtraction for strictly positive binary numerals; `VTask.sub'` delegates to this in the two-positive case but handles the zero cases itself.