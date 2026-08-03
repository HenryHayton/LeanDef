## VTask.choose : ℕ → ℕ → ℕ

### 1. Object

`VTask.choose n k` is the **binomial coefficient** "n choose k", i.e., the number of ways to select an unordered subset of exactly `k` elements from a set of `n` elements. It is a natural-number-valued function defined for all pairs of natural numbers; when `k > n` the value is 0 (there are no such subsets), and in particular `VTask.choose n 0 = 1` for every `n` (there is exactly one empty subset). The values form Pascal's triangle: each interior entry equals the sum of the two entries directly above it.

### 2. Signature

```
VTask.choose : ℕ → ℕ → ℕ
               ↑       ↑
               n       k
```

- `n : ℕ` — the size of the ambient set (non-negative integer).
- `k : ℕ` — the size of the subset to choose (non-negative integer).
- Returns a `ℕ` — the count of k-element subsets of an n-element set.

### 3. Conventions

The function is total on all of `ℕ × ℕ`; no inputs are excluded or undefined. When `k > n`, the convention is that `VTask.choose n k = 0`, reflecting the fact that no k-element subset of an n-element set exists. In particular, `VTask.choose 0 (k+1) = 0` for every `k`. The degenerate case `VTask.choose n 0 = 1` holds for every `n ≥ 0`, including `n = 0`, because there is exactly one empty subset.

### 4. Worked examples

- Claim: VTask.choose 5 2 = 10
  ```lean
  example : VTask.choose 5 2 = 10 := by decide
  ```

- Claim: VTask.choose 0 0 = 1
  ```lean
  example : VTask.choose 0 0 = 1 := by decide
  ```

- Claim: VTask.choose 4 5 = 0 (choosing more elements than the set contains gives 0)
  ```lean
  example : VTask.choose 4 5 = 0 := by decide
  ```

- Claim: VTask.choose 6 3 = VTask.choose 6 3 (Pascal's identity: choose 6 3 = choose 5 2 + choose 5 3 = 10 + 10 = 20)
  ```lean
  example : VTask.choose 6 3 = 20 := by decide
  ```

- Claim: VTask.choose n k = VTask.choose n (n - k) (symmetry) holds for k ≤ n; e.g., choose 7 2 = choose 7 5
  ```lean
  example : VTask.choose 7 2 = VTask.choose 7 5 := by decide
  ```

### 5. Boundaries

- **`k = 0` (any `n`):** `VTask.choose n 0 = 1` for all `n : ℕ`, including `n = 0`. There is exactly one way to choose the empty subset.
- **`n = 0, k ≥ 1`:** `VTask.choose 0 k = 0` for all `k ≥ 1`. No non-empty subset of the empty set exists.
- **`k > n` (general):** `VTask.choose n k = 0`. The recursion unwinds to a `0` base case before `k` reaches `0`.
- **`k = n`:** `VTask.choose n n = 1` for all `n`. There is exactly one way to choose all elements.
- **`k = 1`:** `VTask.choose n 1 = n` for all `n`. One-element subsets correspond bijectively to elements.
- **`n = 1, k = 1`:** `VTask.choose 1 1 = 1`, consistent with both the `k = n` and `k = 1` rules.

### 6. Not to be confused with

- **`VTask.choose n k` vs. the multinomial coefficient:** Multinomial coefficients generalize binomial coefficients to more than two parts; `VTask.choose` is the two-part (binomial) special case only.
- **`Finset.card_powersetCard` (a theorem):** This is the *proof* that `VTask.choose n k` counts k-element subsets of an n-element finset; it is not the function itself.
- **`Nat.descFactorial n k` (falling factorial):** The product `n * (n-1) * … * (n-k+1)`; it equals `VTask.choose n k * k!` but is a different function.
