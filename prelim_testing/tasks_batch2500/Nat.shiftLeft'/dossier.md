## Object

`VTask.shiftLeft' b m n` computes the natural number obtained by starting with `m` and performing `n` successive left-shifts, inserting the boolean bit `b` as the least significant bit at each step. Concretely, each step takes the current value, multiplies it by 2, and adds 1 if `b = true` (or 0 if `b = false`). After `n` such steps the result is the natural number whose binary representation is that of `m` followed by `n` copies of the bit `b`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.shiftLeft' : (b : Bool) -> (m : ℕ) -> ℕ → ℕ
<!-- PINNED-SIGNATURE:END -->


VTask.shiftLeft' : (b : Bool) -> (m : ℕ) -> ℕ → ℕ

The first argument `b` is the boolean bit (0 or 1) that is inserted as the least significant bit on each shift step. The second argument `m` is the starting natural number (the value to be shifted). The third argument is the number of left-shift steps to perform.

## Conventions

When the number of steps is zero the function returns `m` unchanged, regardless of `b`. There are no junk-value conventions arising from the Bool or natural-number parameters; the function is total.

## Worked examples

- Claim: `VTask.shiftLeft' false 1 0 = 1` (zero shifts leaves the value alone)
  ```lean
  example : VTask.shiftLeft' false 1 0 = 1 := by decide
  ```

- Claim: `VTask.shiftLeft' false 1 3 = 8` (three left-shifts of 1 with 0-fill: binary 1 → 1000 = 8)
  ```lean
  example : VTask.shiftLeft' false 1 3 = 8 := by decide
  ```

- Claim: `VTask.shiftLeft' true 1 3 = 15` (three left-shifts of 1 with 1-fill: binary 1 → 1111 = 15)
  ```lean
  example : VTask.shiftLeft' true 1 3 = 15 := by decide
  ```

- Claim: `VTask.shiftLeft' true 0 4 = 15` (shifting 0 left 4 times with 1-fill gives 2^4 − 1 = 15)
  ```lean
  example : VTask.shiftLeft' true 0 4 = 15 := by decide
  ```

- Claim: `VTask.shiftLeft' false 5 2 = 20` (two 0-filling shifts of 5: 5 * 4 = 20)
  ```lean
  example : VTask.shiftLeft' false 5 2 = 20 := by decide
  ```

## Boundaries

- **Zero shifts**: `VTask.shiftLeft' b m 0 = m` for all `b` and `m`; the bit `b` is never inserted.
- **Zero base with `b = false`**: repeatedly shifting 0 with 0-fill gives 0 for any number of steps.
- **Zero base with `b = true`**: shifting 0 left `n` times with 1-fill gives `2^n − 1` (a string of `n` ones in binary).
- **`b = false` case**: `VTask.shiftLeft' false m n` coincides with the ordinary left shift `m <<< n`, i.e., `m * 2^n`.
- **`b = true` case**: `VTask.shiftLeft' true m n + 1 = (m + 1) * 2^n`, relating the result to multiplication.
- **Non-zero `m`**: the result is always non-zero when `m ≠ 0`, regardless of `b` or the number of steps.

## Not to be confused with

- `Nat.shiftLeft` (written `m <<< n`): the ordinary left shift, which always fills with 0; equivalent to `VTask.shiftLeft' false m n` but does not accept a fill-bit argument.
- `Nat.shiftRight` (`m >>> n`): shifts bits to the right (divides by powers of 2), the inverse direction.
- `Nat.bit b n`: a single-step operation that prepends bit `b` to `n`; `VTask.shiftLeft'` is the `n`-fold iteration of exactly this operation.