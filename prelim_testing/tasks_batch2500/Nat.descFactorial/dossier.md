## Object

The descending factorial (also called the falling factorial or Pochhammer symbol in one specialization) of a natural number `n` taken `k` steps: the product `n · (n−1) · (n−2) · ⋯ · (n−k+1)`, which equals `n! / (n−k)!` whenever `k ≤ n`. When `k = 0` the empty product is 1. When `k > n` the result is 0 (natural-number subtraction makes the first factor that reaches 0 collapse the entire product).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.descFactorial : (n : ℕ) -> ℕ → ℕ
<!-- PINNED-SIGNATURE:END -->


`VTask.descFactorial : (n : ℕ) -> ℕ → ℕ`

The first argument `n` is the starting value from which the descending product begins. The second argument `k` is the number of consecutive descending factors to multiply together.

## Conventions

When `k > n`, natural-number subtraction causes one of the factors in the product to be 0, so `VTask.descFactorial n k = 0` for all `k > n`. There is no junk value in the traditional sense; this is the mathematically natural extension of the falling factorial to all natural numbers.

## Worked examples

- Claim: `VTask.descFactorial 5 0 = 1` (empty product)
  ```lean
  example : VTask.descFactorial 5 0 = 1 := by decide
  ```

- Claim: `VTask.descFactorial 5 3 = 60` (since 5 · 4 · 3 = 60)
  ```lean
  example : VTask.descFactorial 5 3 = 60 := by decide
  ```

- Claim: `VTask.descFactorial 4 4 = 24` (equals 4! since k = n)
  ```lean
  example : VTask.descFactorial 4 4 = 24 := by decide
  ```

- Claim: `VTask.descFactorial 3 5 = 0` (k > n, so the product hits zero)
  ```lean
  example : VTask.descFactorial 3 5 = 0 := by decide
  ```

- Claim: For any `n : ℕ` with `k ≤ n`, `(n - k)! * VTask.descFactorial n k = n!` — the fundamental identity relating the descending factorial to the ordinary factorial.

- Claim: `VTask.descFactorial n k ≤ n ^ k` for all `n k : ℕ` — the descending factorial is bounded above by the corresponding power.

## Boundaries

- **`k = 0`**: The result is always 1 regardless of `n`, reflecting the empty product convention.
- **`k = n`**: The result equals `n!`, since `n · (n−1) · ⋯ · 1 = n!`.
- **`k > n`**: The result is 0. Specifically, `VTask.descFactorial n k = 0 ↔ n < k`.
- **`n = 0, k ≥ 1`**: The result is 0, since the very first factor `0 - 0 = 0`.
- **`n = 0, k = 0`**: The result is 1 (base case).

## Not to be confused with

- **Ascending factorial (`ascFactorial`)**: multiplies `n · (n+1) · (n+2) · ⋯`, going upward rather than downward; related by `VTask.descFactorial (n+k) k = ascFactorial (n+1) k`.
- **`descPochhammer`**: a polynomial generalization of the same product, defined over a commutative ring, strictly more general than `VTask.descFactorial` which is specialized to natural numbers.
- **`Nat.factorial`**: computes `n! = n · (n−1) · ⋯ · 1`, which equals `VTask.descFactorial n n`; confusing the two ignores the role of the second argument `k`.