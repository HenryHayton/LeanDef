## Object

The predecessor function on the type `Num` of binary natural numbers. Given a `Num` value `n`, it returns the largest `Num` that is strictly less than `n`, except at zero where it returns zero (since there is no natural-number predecessor of 0).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pred : Num → Num
<!-- PINNED-SIGNATURE:END -->


The single argument is the `Num` value whose predecessor is to be computed.

## Conventions

Because `Num` represents non-negative integers and zero has no natural predecessor, `VTask.pred 0` is defined to be `0` by convention (a saturating or clamped predecessor rather than a partial function).

## Worked examples

- Claim: `VTask.pred 0 = 0` (the zero case returns zero by convention)
  ```lean
  example : VTask.pred 0 = 0 := by decide
  ```

- Claim: `VTask.pred 1 = 0` (the predecessor of one is zero)
  ```lean
  example : VTask.pred 1 = 0 := by decide
  ```

- Claim: `VTask.pred 5 = 4` (ordinary predecessor for a positive value)
  ```lean
  example : VTask.pred 5 = 4 := by decide
  ```

- Claim: `VTask.pred 8 = 7`
  ```lean
  example : VTask.pred 8 = 7 := by decide
  ```

## Boundaries

- At `n = 0`: the function returns `0` rather than being undefined or returning a sentinel. This is the only point where `VTask.pred n ≠ n - 1` in the usual integer sense.
- For all positive `n`: `VTask.pred n` is the unique `Num` equal to `n - 1` in the natural numbers.
- The function is total on all of `Num`; there are no inputs for which it is undefined.

## Not to be confused with

- `Nat.pred`: the predecessor on `Nat` (unary natural numbers), which similarly sends `0` to `0` but operates on a different type.
- `Int.pred` or integer decrement: these can return negative values, whereas `VTask.pred` always stays within `Num` (non-negative).
- Subtraction `n - 1` on `Num`: conceptually equivalent for positive `n`, but `VTask.pred` is a dedicated, direct predecessor without the overhead of general subtraction.