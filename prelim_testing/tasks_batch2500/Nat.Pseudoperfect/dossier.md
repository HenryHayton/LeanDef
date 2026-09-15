## VTask.Pseudoperfect

### Object

A positive natural number `n` is *pseudoperfect* (also called *semiperfect*) if some subset of its proper divisors (i.e., divisors strictly less than `n`) sums exactly to `n`. In other words, `n` can be written as a sum of distinct proper divisors of itself. The requirement that `n` be positive is included so that `0` is excluded by convention.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Pseudoperfect : (n : ℕ) -> Prop
<!-- PINNED-SIGNATURE:END -->


The sole argument `n` is the natural number being tested for pseudoperfectness. The predicate asserts that `n` is positive and that a witnessing subset of proper divisors summing to `n` exists.

### Conventions

The number `0` is explicitly excluded: `VTask.Pseudoperfect 0` is false because positivity is a required conjunct. This is a deliberate junk-value convention to avoid the vacuously true case where the empty-sum subset of `properDivisors 0` (which is empty) would sum to `0`.

### Worked examples

- Claim: `VTask.Pseudoperfect 6` holds, because `6` is perfect (proper divisors `{1, 2, 3}` sum to `6`).
  ```lean
  example : VTask.Pseudoperfect 6 := by decide
  ```

- Claim: `VTask.Pseudoperfect 12` holds, because `12` has proper divisors `{1, 2, 3, 4, 6}` and `2 + 4 + 6 = 12`.
  ```lean
  example : VTask.Pseudoperfect 12 := by decide
  ```

- Claim: `¬ VTask.Pseudoperfect 2` holds, because every prime is not pseudoperfect (its only proper divisor is `1`, which does not sum to `2`).
  ```lean
  example : ¬ VTask.Pseudoperfect 2 := by decide
  ```

- Claim: `¬ VTask.Pseudoperfect 0` holds by the positivity requirement.
  ```lean
  example : ¬ VTask.Pseudoperfect 0 := by decide
  ```

### Boundaries

- **`n = 0`**: Not pseudoperfect; the positivity condition fails outright.
- **`n = 1`**: Not pseudoperfect; `properDivisors 1` is empty, so no nonempty subset exists, and the empty sum `0 ≠ 1`.
- **Primes**: No prime is pseudoperfect; the only proper divisor of a prime `p` is `1`, and `1 ≠ p` for `p ≥ 2`.
- **Perfect numbers**: Every perfect number is pseudoperfect, since the entire set of proper divisors witnesses the condition (the full proper-divisor sum equals `n` by definition of perfect).
- **Abundant numbers**: Many (but not all) abundant numbers are pseudoperfect; a non-pseudoperfect abundant number is called *weird*.

### Not to be confused with

- **`Nat.Perfect`**: A perfect number requires the *entire* set of proper divisors to sum to `n`, whereas pseudoperfect only needs *some* subset; every perfect number is pseudoperfect, but not vice versa (e.g., `12` is pseudoperfect but not perfect).
- **`Nat.Abundant`**: An abundant number has proper-divisor sum *exceeding* `n`; being abundant neither implies nor is implied by being pseudoperfect in general.
- **Weird numbers**: Numbers that are abundant but *not* pseudoperfect; the smallest example is `70`. These are the complement of pseudoperfect within the abundant numbers.