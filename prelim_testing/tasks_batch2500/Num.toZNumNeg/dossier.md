## Object

`VTask.toZNumNeg` converts a natural number `x` of type `Num` into its negation `-x` as an element of type `ZNum`, the type of binary-represented integers. Where `Num` represents non-negative integers (zero or a positive binary numeral), this function produces the non-positive counterpart in `ZNum`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toZNumNeg : Num → ZNum
<!-- PINNED-SIGNATURE:END -->


`VTask.toZNumNeg : Num → ZNum`

The sole argument is a non-negative binary numeral (`Num`) to be negated and embedded into the signed binary integer type `ZNum`.

## Conventions

When the input is zero (`0 : Num`), the result is zero (`0 : ZNum`), reflecting that negating zero yields zero. When the input is a positive numeral `pos a`, the result is the negative element `ZNum.neg a`, representing the strictly negative integer `-a`.

## Worked examples

- Claim: `VTask.toZNumNeg 0 = 0`
  ```lean
  example : VTask.toZNumNeg 0 = 0 := by decide
  ```

- Claim: `VTask.toZNumNeg (Num.pos 1) = ZNum.neg 1`
  ```lean
  example : VTask.toZNumNeg (Num.pos 1) = ZNum.neg 1 := by decide
  ```

- Claim: `VTask.toZNumNeg (Num.pos 3) = ZNum.neg 3`
  ```lean
  example : VTask.toZNumNeg (Num.pos 3) = ZNum.neg 3 := by decide
  ```

## Boundaries

- At `0 : Num`, the result is `0 : ZNum` (not `ZNum.neg` applied to anything), since zero is its own negation and `ZNum` has a dedicated zero constructor.
- For any strictly positive `Num` value `pos a`, the result is the `ZNum.neg a` constructor, which is always strictly negative. There is no positive or zero `ZNum` output for a nonzero input.
- The function is total: every `Num` value has a well-defined image in `ZNum`.

## Not to be confused with

- `Num.toZNum`: embeds a `Num` into `ZNum` as a non-negative value (identity on the non-negative part), rather than negating it.
- `ZNum.neg`: a constructor of the `ZNum` type representing a strictly negative binary integer, used inside `toZNumNeg` but not itself a conversion function.
- `Int.negSucc`: a constructor in Lean's `Int` type for negative integers, unrelated to the binary `ZNum`/`Num` representation used here.