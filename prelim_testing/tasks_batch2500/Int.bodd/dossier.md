## VTask.bodd

### Object

`VTask.bodd` is a function that tests whether an integer is odd, returning `true` if the integer is odd and `false` if it is even. It extends the usual notion of parity from the natural numbers to all integers, respecting the fact that negative integers also have well-defined parity.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.bodd : ℤ → Bool
<!-- PINNED-SIGNATURE:END -->


The single argument is an arbitrary integer whose parity is to be determined.

### Conventions

Parity of negative integers agrees with parity of their absolute values: a negative integer is odd if and only if its absolute value (as a natural number) is odd. Concretely, `-(n+1)` is odd precisely when `n` is even, and even precisely when `n` is odd.

### Worked examples

- Claim: `VTask.bodd 0 = false` (zero is even)
  ```lean
  example : VTask.bodd 0 = false := by decide
  ```

- Claim: `VTask.bodd 1 = true` (one is odd)
  ```lean
  example : VTask.bodd 1 = true := by decide
  ```

- Claim: `VTask.bodd (-3) = true` (negative three is odd)
  ```lean
  example : VTask.bodd (-3) = true := by decide
  ```

- Claim: `VTask.bodd (-4) = false` (negative four is even)
  ```lean
  example : VTask.bodd (-4) = false := by decide
  ```

- Claim: `VTask.bodd (m + n) = xor (VTask.bodd m) (VTask.bodd n)` for all integers `m n` (parity of a sum is the XOR of parities)

- Claim: `VTask.bodd (-n) = VTask.bodd n` for all integers `n` (negation preserves parity)

### Boundaries

- At `0`: returns `false`, consistent with zero being even.
- At `1`: returns `true`, consistent with one being odd.
- At `-1`: returns `true`; a negSucc integer `-[0+1]` has the negated parity of `0`, and since `Nat.bodd 0 = false`, `not false = true`, so `-1` is correctly identified as odd.
- The function is total on all of `ℤ` with no exceptional inputs.
- Parity is invariant under negation: `VTask.bodd (-n) = VTask.bodd n` for all `n : ℤ`.

### Not to be confused with

- `Nat.bodd`: the analogous parity test for natural numbers only; `VTask.bodd` extends this to all integers.
- `Int.even` / `Even`: a `Prop`-valued predicate asserting that an integer is even; `VTask.bodd` instead returns a `Bool` value directly and tests for *odd*ness, not evenness.
- `Int.div2`: the companion function that returns the integer divided by 2 (floored), paired with `VTask.bodd` in the decomposition `bit (bodd n) (div2 n) = n`.