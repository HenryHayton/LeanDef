## VTask.doubleFactorial

### Object

The double factorial of a natural number `n`, written `n!!` in standard mathematical notation, is the product of all positive integers up to `n` that share the same parity as `n`. Concretely, for a positive even number `2k` it equals `2 · 4 · 6 · ··· · (2k)`, and for a positive odd number `2k+1` it equals `1 · 3 · 5 · ··· · (2k+1)`. By convention, `0!! = 1` and `1!! = 1`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.doubleFactorial : ℕ → ℕ
<!-- PINNED-SIGNATURE:END -->


The single argument is the natural number whose double factorial is to be computed.

### Conventions

The double factorial of `0` is defined to be `1` (the empty product convention). The double factorial of `1` is defined to be `1`. These base cases ensure the recursive relation `(n+2)!! = (n+2) · n!!` holds uniformly for all `n ≥ 0`.

### Worked examples

- Claim: `VTask.doubleFactorial 0 = 1` (empty product base case)
  ```lean
  example : VTask.doubleFactorial 0 = 1 := by decide
  ```

- Claim: `VTask.doubleFactorial 1 = 1`
  ```lean
  example : VTask.doubleFactorial 1 = 1 := by decide
  ```

- Claim: `VTask.doubleFactorial 6 = 48` (even case: 2 · 4 · 6 = 48)
  ```lean
  example : VTask.doubleFactorial 6 = 48 := by decide
  ```

- Claim: `VTask.doubleFactorial 7 = 105` (odd case: 1 · 3 · 5 · 7 = 105)
  ```lean
  example : VTask.doubleFactorial 7 = 105 := by decide
  ```

- Claim: The double factorial of any natural number is strictly positive, i.e., `0 < VTask.doubleFactorial n` for all `n`.

- Claim: For all `n`, `(n + 1)! = VTask.doubleFactorial (n + 1) * VTask.doubleFactorial n`, relating the ordinary factorial to a product of two consecutive double factorials.

- Claim: `VTask.doubleFactorial (2 * n) = 2 ^ n * n!` for all `n` (the even double factorial identity).

### Boundaries

- `VTask.doubleFactorial 0 = 1`: zero is treated as an even number with an empty product, yielding 1.
- `VTask.doubleFactorial 1 = 1`: the only odd number at the base of the odd chain.
- `VTask.doubleFactorial 2 = 2`: first nontrivial value, computed as `2 · VTask.doubleFactorial 0 = 2 · 1`.
- The function is always at least 1 (strictly positive) for all natural number inputs.
- The double factorial grows strictly slower than the ordinary factorial; `n!! ≤ n!` for all `n`.

### Not to be confused with

- `Nat.factorial`: the ordinary factorial `n!`, which is the product of ALL positive integers up to `n`, not just those of matching parity; related by `(n+1)! = (n+1)!! · n!!`.
- The notation `n!!` in analysis sometimes refers to iterating the factorial operator (i.e., `(n!)!`), which is an entirely different and much faster-growing function.
- `Nat.ascFactorial` / `Nat.descFactorial`: rising and falling factorial products, which are generalizations in a different direction (shifting the starting point or the step size, not selecting by parity).