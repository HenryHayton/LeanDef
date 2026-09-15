## Object

`VTask.ofZNum` converts a signed binary numeral (`ZNum`) to an unsigned binary numeral (`Num`). Because `Num` is a type of non-negative numerals, negative inputs cannot be represented and are mapped to zero. Positive inputs are converted faithfully by stripping the sign.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofZNum : ZNum → Num
<!-- PINNED-SIGNATURE:END -->


The sole argument is the signed integer (of type `ZNum`) to be converted. It may be zero, a positive binary numeral, or a negative binary numeral.

## Conventions

When the input `ZNum` is negative, the function returns `0` (the zero element of `Num`) rather than signalling an error or producing an option. This is a total, junk-value convention: the "natural" domain is non-negative integers, but the function is defined for all `ZNum` inputs.

## Worked examples

- Claim: `VTask.ofZNum (ZNum.pos 3) = Num.pos 3` — a positive `ZNum` wrapping the positive numeral `3` maps to the corresponding `Num`.

- Claim: `VTask.ofZNum 0 = 0` — the zero `ZNum` maps to the zero `Num`.

- Claim: `VTask.ofZNum (-5) = 0` — any negative `ZNum` maps to `0` in `Num`.

- Claim: `VTask.ofZNum (ZNum.pos 1) = 1` — the positive `ZNum` for one maps to `Num` one.

## Boundaries

- **`ZNum.pos p` (positive input):** returns `Num.pos p`, preserving the underlying positive numeral exactly.
- **`ZNum.zero` (zero input):** returns `0`; zero is not a `ZNum.pos`, so it falls to the catch-all case.
- **Any negative `ZNum` (e.g., `ZNum.neg p`):** returns `0`; the function is total and silently saturates at zero rather than wrapping or erroring.

## Not to be confused with

- `ZNum.toInt` — converts a `ZNum` to a Lean `Int`, preserving negative values rather than clamping them.
- `Num.toZNum` — goes in the opposite direction, embedding an unsigned `Num` into the signed `ZNum` type.
- A hypothetical `ofZNum : ZNum → Option Num` — the docstring mentions `Option Num` as a description, but the actual return type is `Num` (not `Option Num`); there is no `none`/`some` wrapping.