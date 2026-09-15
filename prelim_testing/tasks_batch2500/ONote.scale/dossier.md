## Object

`VTask.scale x o` computes the ordinal notation representing `ω^x · o`, i.e., it multiplies the ordinal denoted by `o` on the left by the ordinal `ω^x`. Concretely, it scales every exponent appearing in the Cantor-normal-form expansion of `o` by adding `x` to each leading exponent.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.scale : (x : ONote) -> ONote → ONote
<!-- PINNED-SIGNATURE:END -->


The first argument `x` is the exponent: the result represents multiplication by `ω^x`. The second argument `o` is the ordinal notation being scaled; it is the "multiplicand" whose Cantor-normal-form exponents are all shifted up by `x`.

## Conventions

When `o` is the notation for zero (`0`), the result is the notation for zero (`0`), consistent with `ω^x · 0 = 0` for any ordinal `x`.

## Worked examples

- Claim: Scaling the notation for `0` by any `x` yields `0`. For instance, `VTask.scale x 0 = 0` for all `x : ONote`.

- Claim: Scaling the notation for `ω^e` (represented as `oadd e 1 0`) by `x` yields `oadd (x + e) 1 0`, i.e., the notation for `ω^(x+e)`. For example, scaling `ω^0 = 1` (notation `oadd 0 1 0`) by `x` gives `oadd x 1 0`, the notation for `ω^x`.

- Claim: If `o = oadd e₁ n₁ (oadd e₂ n₂ 0)` (a two-term Cantor normal form `ω^e₁·n₁ + ω^e₂·n₂`), then `VTask.scale x o = oadd (x+e₁) n₁ (oadd (x+e₂) n₂ 0)`, the notation for `ω^(x+e₁)·n₁ + ω^(x+e₂)·n₂`.

- Claim: `VTask.scale` distributes over addition in the sense that `ω^x · (a + b) = ω^x · a + ω^x · b`, so scaling each summand independently and concatenating gives the same result as scaling the whole sum.

## Boundaries

- When `o = 0` (the zero notation), `VTask.scale x o = 0` regardless of `x`, since `ω^x · 0 = 0`.
- When `x = 0` (the zero notation, representing the ordinal 0), `ω^0 = 1`, so `VTask.scale 0 o` should yield a notation for `1 · o = o`. Since `0 + e = e` holds in `ONote`, the exponents are unchanged and the result is structurally identical to `o`.
- The function is defined for all `ONote` inputs without restriction; it does not require `o` or `x` to be in normal form, though preservation of normal form is a meaningful property when inputs are well-formed.
- The natural-number coefficients `n` in each `oadd` term are passed through unchanged; only the exponent part of each term is shifted by `x`.

## Not to be confused with

- `ONote.mul`: full ordinal multiplication `a * b` in `ONote`, not just left-multiplication by a pure power of `ω`.
- `ONote.opow` (or `ONote.pow`): ordinal exponentiation `ω^x` as a standalone value, rather than using `ω^x` as a scaling factor.
- Simply adding `x` to `o` as a notation (`ONote.add`): `VTask.scale` shifts all exponents in `o` by `x`, which is multiplication, not addition.