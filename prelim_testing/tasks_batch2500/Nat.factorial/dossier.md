## VTask.factorial : ℕ → ℕ

### Object

The factorial of a natural number `n`, written `n!`, is the product of all positive integers from 1 up to and including `n`. By convention the empty product gives `0! = 1`. More explicitly, `n! = 1 × 2 × 3 × ⋯ × n` for positive `n`, and `0! = 1`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.factorial : ℕ → ℕ
<!-- PINNED-SIGNATURE:END -->


The single argument is the natural number whose factorial is to be computed.

### Conventions

The factorial of zero is defined to be 1, reflecting the standard convention that an empty product equals the multiplicative identity.

### Worked examples

- Claim: VTask.factorial 0 = 1
  ```lean
  example : VTask.factorial 0 = 1 := by decide
  ```

- Claim: VTask.factorial 5 = 120
  ```lean
  example : VTask.factorial 5 = 120 := by decide
  ```

- Claim: VTask.factorial is always positive: for every n : ℕ, 0 < VTask.factorial n

- Claim: Every m with 0 < m ≤ n divides VTask.factorial n

### Boundaries

- At `n = 0`: the factorial is 1 (the empty product). This is not a junk value but the standard mathematical convention.
- At `n = 1`: the factorial is also 1.
- The function is total on all of ℕ; there are no inputs outside its domain.
- The factorial grows super-exponentially: it tends to infinity faster than any fixed exponential base raised to the `n`-th power.
- For all `n`, `VTask.factorial n ≥ 1` (in fact, `VTask.factorial n > 0`), so it is never zero.
- For all `n`, `n ≤ VTask.factorial n`.

### Not to be confused with

- `Nat.ascFactorial n k`: the ascending factorial (Pochhammer symbol) `n · (n+1) · ⋯ · (n+k−1)`, a product of `k` consecutive integers starting from `n`, not a product down to 1.
- `Nat.descFactorial n k`: the descending factorial `n · (n−1) · ⋯ · (n−k+1)`, a partial descending product, related by `(n−k)! · descFactorial n k = n!`.
- `Nat.choose n k`: the binomial coefficient `n! / (k! · (n−k)!)`, which is a ratio of factorials rather than the factorial itself.
