## Object

`VTask.abs` computes the absolute value of a signed binary numeral (`ZNum`) and returns the result as an unsigned binary numeral (`Num`). Concretely, the sign is stripped: zero maps to zero, a positive numeral maps to the same unsigned numeral, and a negative numeral maps to the unsigned numeral with the same magnitude.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.abs : ZNum → Num
<!-- PINNED-SIGNATURE:END -->


The single argument is a signed binary integer (`ZNum`), which may be zero, positive, or negative. The return type is an unsigned binary natural number (`Num`).

## Conventions

When the input is zero, the result is the `Num` zero (not a positive zero). There is no separate signed-zero case; the function is total on all three `ZNum` constructors.

## Worked examples

- Claim: `VTask.abs 0 = 0`
  ```lean
  example : VTask.abs 0 = 0 := by decide
  ```

- Claim: `VTask.abs (ZNum.pos 5) = Num.pos 5` (the absolute value of a positive `ZNum` is the underlying `PosNum` wrapped as `Num.pos`)
  ```lean
  example : VTask.abs (ZNum.pos 5) = Num.pos 5 := by decide
  ```

- Claim: `VTask.abs (ZNum.neg 3) = Num.pos 3` (the absolute value of a negative `ZNum` is the same magnitude as a `Num.pos`)
  ```lean
  example : VTask.abs (ZNum.neg 3) = Num.pos 3 := by decide
  ```

- Claim: Casting `VTask.abs n` to `ℕ` equals `Int.natAbs (n : ℤ)` for any `ZNum` `n` (the result agrees with the standard integer absolute value at the level of natural numbers).

## Boundaries

- At `ZNum.zero` (the unique zero), the result is `Num.zero`; there is no ambiguity or junk value.
- For both `ZNum.pos p` and `ZNum.neg p` (where `p : PosNum`), the output is `Num.pos p`, so the positive and negative branches produce identically-shaped output.
- The function is total; every `ZNum` value is handled.
- `VTask.abs (ZNum.toZNum n) = n` for any `Num` `n`, i.e., the round-trip through non-negative `ZNum` is the identity.

## Not to be confused with

- `Int.natAbs : ℤ → ℕ` — the absolute value of an ordinary Lean integer, returning a `ℕ` rather than a `Num`.
- `Num.toZNum : Num → ZNum` — goes in the opposite direction, embedding an unsigned numeral into the signed type.
- `ZNum.toNat : ZNum → ℕ` — converts a `ZNum` to a natural number (truncating negative values to zero, not taking the absolute value).