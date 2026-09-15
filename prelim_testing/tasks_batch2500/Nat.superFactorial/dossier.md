## VTask.superFactorial

### Object

The superfactorial of a natural number `n`, denoted `sf(n)`, is the product of the first `n` factorials:

$$\operatorname{sf}(n) = 0! \cdot 1! \cdot 2! \cdots (n-1)! \cdot n! = \prod_{k=0}^{n} k!$$

Equivalently, it satisfies the recurrence `sf(0) = 1` and `sf(n+1) = (n+1)! · sf(n)` for all `n ≥ 0`. The sequence begins `1, 1, 2, 12, 288, 34560, …`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.superFactorial : ℕ → ℕ
<!-- PINNED-SIGNATURE:END -->


`VTask.superFactorial : ℕ → ℕ`

The single argument is the non-negative integer `n` whose superfactorial is to be computed.

### Conventions

By the empty-product convention, the superfactorial of `0` is defined to be `1`.

### Worked examples

- Claim: `VTask.superFactorial 0 = 1` (empty product)
  ```lean
  example : VTask.superFactorial 0 = 1 := by decide
  ```

- Claim: `VTask.superFactorial 1 = 1` (only factor is `1! = 1`)
  ```lean
  example : VTask.superFactorial 1 = 1 := by decide
  ```

- Claim: `VTask.superFactorial 2 = 2` (product `1! · 2! = 1 · 2 = 2`)
  ```lean
  example : VTask.superFactorial 2 = 2 := by decide
  ```

- Claim: `VTask.superFactorial 3 = 12` (product `1! · 2! · 3! = 1 · 2 · 6 = 12`)
  ```lean
  example : VTask.superFactorial 3 = 12 := by decide
  ```

- Claim: `VTask.superFactorial 4 = 288` (product `1! · 2! · 3! · 4! = 1 · 2 · 6 · 24 = 288`)
  ```lean
  example : VTask.superFactorial 4 = 288 := by decide
  ```

- Claim: `VTask.superFactorial n` equals the product `∏ x ∈ Finset.range (n+1), x!` for every `n`.

- Claim: `VTask.superFactorial n` equals the product `∏ x ∈ Finset.Icc 1 n, x!` for every `n`.

### Boundaries

- At `n = 0`: returns `1` (the empty product, by convention).
- At `n = 1`: returns `1` (since `1! = 1`).
- The function is total on all natural numbers; it grows extremely rapidly, faster than any tower of factorials at a fixed height.
- For even arguments there is a closed-form expression: `sf(2n) = (∏ᵢ (2i+1)!)² · 2ⁿ · n!`.

### Not to be confused with

- `Nat.factorial`: the ordinary factorial `n! = 1 · 2 · ⋯ · n`; the superfactorial is a product of factorials, not of integers.
- `Nat.ascFactorial` / `Nat.descFactorial`: rising and falling factorial (Pochhammer-style products), which are products of consecutive integers, not products of factorials.
- The *Sloane* superfactorial `sf(n) = 1^n · 2^(n−1) · ⋯ · n^1` (an alternative definition sometimes used in combinatorics); the Mathlib definition uses the product-of-factorials convention, not the weighted-product convention.
