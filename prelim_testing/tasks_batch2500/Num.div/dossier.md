## Object

This is Euclidean (floor) division on the type `Num` of binary natural numbers, extended to a total function by declaring that division by zero yields zero. The result of `VTask.div x d` is the largest natural number `q` such that `q * d ≤ x`, except when `d = 0`, in which case the result is defined to be `0`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.div : Num → Num → Num
<!-- PINNED-SIGNATURE:END -->


VTask.div : Num → Num → Num

The first argument is the dividend — the number being divided. The second argument is the divisor — the number by which the dividend is divided.

## Conventions

Division by zero is given the junk value `0`: for any `Num` value `x`, `VTask.div x 0 = 0`. This makes the operation total on all of `Num × Num`.

## Worked examples

- Claim: VTask.div 0 5 = 0 (zero divided by anything is zero)
  ```lean
  example : VTask.div 0 5 = 0 := by decide
  ```

- Claim: VTask.div 7 2 = 3 (ordinary floor division)
  ```lean
  example : VTask.div 7 2 = 3 := by decide
  ```

- Claim: VTask.div 10 0 = 0 (division by zero yields zero)
  ```lean
  example : VTask.div 10 0 = 0 := by decide
  ```

- Claim: VTask.div 9 3 = 3 (exact division)
  ```lean
  example : VTask.div 9 3 = 3 := by decide
  ```

## Boundaries

- `VTask.div 0 0 = 0`: both the zero-dividend and the zero-divisor rules agree here, and the result is `0`.
- `VTask.div n 0 = 0` for all `n`: division by zero is always `0`, regardless of the dividend.
- `VTask.div 0 d = 0` for all `d`: zero divided by anything is zero.
- The operation agrees with `Nat` floor division when both arguments are cast to `ℕ`: `(VTask.div n d : ℕ) = (n : ℕ) / (d : ℕ)` for all `n d : Num`.

## Not to be confused with

- `Num.mod`: the companion modulo operation, giving the remainder rather than the quotient.
- `ZNum.div`: division on the signed binary integer type `ZNum`, which handles negative values and uses truncation toward zero.
- `PosNum.div'`: the underlying division on strictly positive binary numerals; `VTask.div` wraps this with zero-case handling.
