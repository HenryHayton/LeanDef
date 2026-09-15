## Object

`VTask.mulNat o n` computes the ordinal notation (an element of `ONote`) representing the product of an ordinal `o` (given in Cantor normal form notation) with a natural number `n`. Semantically, if `o` represents an ordinal `α` and `n` is a natural number, then `VTask.mulNat o n` represents the ordinal `α · n`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mulNat : ONote → ℕ → ONote
<!-- PINNED-SIGNATURE:END -->


VTask.mulNat : ONote → ℕ → ONote

The first argument is the ordinal notation term (an `ONote` value in Cantor normal form) to be multiplied. The second argument is the natural number multiplier.

## Conventions

When the first argument is the zero ordinal notation `0`, the result is `0` regardless of the natural number, reflecting that `0 · n = 0` for all `n`. When the second argument is the natural number `0`, the result is `0` regardless of the ordinal notation, reflecting that `α · 0 = 0` for all ordinals `α`. These two zero cases are treated as junk-value conventions in the sense that no special output is invented — both are the unique canonical zero ordinal notation.

## Worked examples

- Claim: `VTask.mulNat 0 5 = 0` — multiplying the zero ordinal by any natural number yields zero.
  ```lean
  example : VTask.mulNat 0 5 = 0 := by decide
  ```

- Claim: `VTask.mulNat (ONote.oadd 0 1 0) 3 = ONote.oadd 0 3 0` — the ordinal notation for `1` (which is `oadd 0 1 0`, representing `ω^0 · 1 = 1`) multiplied by `3` gives the notation for `3` (which is `oadd 0 3 0`, representing `ω^0 · 3 = 3`).
  ```lean
  example : VTask.mulNat (ONote.oadd 0 1 0) 3 = ONote.oadd 0 3 0 := by decide
  ```

- Claim: `VTask.mulNat (ONote.oadd 1 1 0) 4 = ONote.oadd 1 4 0` — the notation for `ω` multiplied by `4` yields the notation for `ω · 4`.
  ```lean
  example : VTask.mulNat (ONote.oadd 1 1 0) 4 = ONote.oadd 1 4 0 := by decide
  ```

- Claim: `VTask.mulNat (ONote.oadd 0 2 0) 0 = 0` — multiplying any ordinal notation by zero gives zero.
  ```lean
  example : VTask.mulNat (ONote.oadd 0 2 0) 0 = 0 := by decide
  ```

## Boundaries

- If the ordinal notation argument is `0` (the zero ordinal), the result is always `0`, even if the natural number is very large.
- If the natural number argument is `0`, the result is always `0`, even for large ordinals.
- For a non-zero ordinal `oadd e n a` multiplied by a positive natural number `m+1`, the leading exponent `e` is preserved unchanged, the leading coefficient `n` is multiplied by `m+1` (using positive natural number arithmetic), and the lower-order tail `a` is also preserved unchanged. This reflects that ordinal multiplication by a finite number only scales the leading coefficient of the top Cantor normal form term and retains the tail.
- The result is always a valid `ONote`; in particular, if the input has the normal form property (`NF`), so does the output.

## Not to be confused with

- `ONote.mul` (or `ONote` multiplication via `HMul`): full ordinal-by-ordinal multiplication in `ONote`, of which `VTask.mulNat` is the special case where the right factor is a natural number.
- `ONote.ofNat`: converts a natural number to its ordinal notation, but does not perform multiplication.
- `ONote.scale`: multiplies an ordinal notation on the left by a power-of-ω factor, not by a natural number coefficient.