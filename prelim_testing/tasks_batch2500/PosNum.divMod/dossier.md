## Object

`VTask.divMod d x` simultaneously computes the quotient and remainder when the positive binary numeral `x` is divided by the positive binary numeral `d`. It returns a pair `(q, r)` where `q = x / d` and `r = x % d`, both expressed as elements of `Num` (the type of non-negative binary numerals, which includes zero).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.divMod : (d : PosNum) -> PosNum → Num × Num
<!-- PINNED-SIGNATURE:END -->


`VTask.divMod : (d : PosNum) -> PosNum → Num × Num`

The first argument `d` is the divisor, a strictly positive binary numeral. The second argument (unnamed in the top-level signature) is the dividend, also a strictly positive binary numeral. The function returns a pair whose first component is the quotient `dividend / divisor` and whose second component is the remainder `dividend % divisor`, both of type `Num`.

## Conventions

Both output components are of type `Num` rather than `PosNum`, allowing the quotient to be zero (when the dividend is smaller than the divisor) and the remainder to be zero (when the divisor divides the dividend exactly). The order of the output pair is `(quotient, remainder)`, i.e., the first component is `x / d` and the second is `x % d`.

## Worked examples

- Claim: `VTask.divMod 3 7` equals `(2, 1)` as `Num` values — dividing 7 by 3 gives quotient 2 and remainder 1.

- Claim: `VTask.divMod 5 5` equals `(1, 0)` — dividing 5 by 5 gives quotient 1 and remainder 0 (exact division).

- Claim: `VTask.divMod 7 3` equals `(0, 3)` — dividing 3 by 7 gives quotient 0 and remainder 3 (dividend smaller than divisor).

- Claim: For all `d n : PosNum`, the natural-number cast of `(VTask.divMod d n).1` equals `(n : ℕ) / (d : ℕ)` and the natural-number cast of `(VTask.divMod d n).2` equals `(n : ℕ) % (d : ℕ)`.

## Boundaries

- **Divisor equals dividend**: When `d = x`, the result is `(1, 0)` — quotient is 1 and remainder is 0.
- **Dividend strictly less than divisor**: The quotient component is `Num.zero` (i.e., 0) and the remainder equals the dividend cast to `Num`.
- **Divisor is 1**: Every positive numeral is divisible by 1, so the remainder is always 0 and the quotient equals the dividend.
- **Both arguments are 1**: `VTask.divMod 1 1` returns `(1, 0)`.
- The remainder always satisfies `0 ≤ r < d` when both are viewed as natural numbers.

## Not to be confused with

- `Num.divMod`: A version of the same operation defined on the larger type `Num` (which includes zero), as opposed to `PosNum` inputs.
- `PosNum.div` / `PosNum.mod`: The individual quotient and remainder operations, which separately compute what `VTask.divMod` computes jointly in a single recursive pass.
- `Int.divMod` or `Nat.divModEquiv`: Division-with-remainder for integers or natural numbers; these operate on a different numeric type hierarchy than binary numerals.