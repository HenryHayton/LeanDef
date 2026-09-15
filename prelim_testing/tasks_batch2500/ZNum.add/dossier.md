## Object

`VTask.add` is the binary addition operation on `ZNum`, the type of binary-numeral representations of integers (including zero, positive binary numerals, and negative binary numerals). Given two `ZNum` values, it returns their integer sum, also represented as a `ZNum`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.add : ZNum → ZNum → ZNum
<!-- PINNED-SIGNATURE:END -->


`VTask.add : ZNum → ZNum → ZNum`

The first argument is the left addend and the second argument is the right addend, both integers represented in the `ZNum` binary numeral system. The result is their sum in the same system.

## Conventions

There are no junk-value or partiality conventions: `VTask.add` is a total function defined for all pairs of `ZNum` values, and every output is a canonical `ZNum` representative of the mathematical sum.

## Worked Examples

- Claim: `VTask.add 0 (ZNum.pos 3) = ZNum.pos 3` (zero is a left identity)
  ```lean
  example : VTask.add 0 (ZNum.pos 3) = ZNum.pos 3 := by decide
  ```

- Claim: `VTask.add (ZNum.pos 5) 0 = ZNum.pos 5` (zero is a right identity)
  ```lean
  example : VTask.add (ZNum.pos 5) 0 = ZNum.pos 5 := by decide
  ```

- Claim: `VTask.add (ZNum.pos 3) (ZNum.pos 4) = ZNum.pos 7` (positive plus positive)
  ```lean
  example : VTask.add (ZNum.pos 3) (ZNum.pos 4) = ZNum.pos 7 := by decide
  ```

- Claim: `VTask.add (ZNum.neg 5) (ZNum.neg 3) = ZNum.neg 8` (negative plus negative)
  ```lean
  example : VTask.add (ZNum.neg 5) (ZNum.neg 3) = ZNum.neg 8 := by decide
  ```

- Claim: `VTask.add (ZNum.pos 5) (ZNum.neg 3) = ZNum.pos 2` (positive plus negative with positive result)
  ```lean
  example : VTask.add (ZNum.pos 5) (ZNum.neg 3) = ZNum.pos 2 := by decide
  ```

- Claim: `VTask.add (ZNum.neg 5) (ZNum.pos 3) = ZNum.neg 2` (negative plus positive with negative result)
  ```lean
  example : VTask.add (ZNum.neg 5) (ZNum.pos 3) = ZNum.neg 2 := by decide
  ```

- Claim: `VTask.add (ZNum.pos 3) (ZNum.neg 3) = 0` (additive inverses sum to zero)
  ```lean
  example : VTask.add (ZNum.pos 3) (ZNum.neg 3) = 0 := by decide
  ```

## Boundaries

- When either argument is `ZNum.zero` (i.e., `0`), the result is exactly the other argument, with no normalization step needed.
- When a positive and a negative numeral of equal magnitude are added, the result is `ZNum.zero`.
- When a positive and a negative numeral are added, the operation delegates to a subtraction-of-positive-numerals helper (`sub'`) which produces the correctly signed `ZNum` result, so the output is always in canonical form.
- The operation is commutative and associative, consistent with integer addition.

## Not to be confused with

- `ZNum.mul`: the multiplication operation on `ZNum`, not addition.
- `Num.add`: addition on `Num`, the type of non-negative binary numerals only, which does not handle negative numbers.
- `PosNum.add`: addition on `PosNum`, the type of strictly positive binary numerals, which neither handles zero nor negative numbers.
