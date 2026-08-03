## VTask.log

### 1. Object

`VTask.log b n` is the **floor logarithm** of the natural number `n` in base `b`. It returns the largest natural number `k` such that `b^k ≤ n`. Equivalently, it is the unique non-negative integer `k` satisfying `b^k ≤ n < b^(k+1)` whenever `b ≥ 2` and `n ≥ 1`.

### 2. Signature

```
VTask.log : (b n : ℕ) -> ℕ
```

- `b : ℕ` — the base of the logarithm.
- `n : ℕ` — the argument whose logarithm is computed.
- Returns `ℕ` — the largest `k` with `b^k ≤ n`, or `0` in degenerate cases.

### 3. Conventions

When the base satisfies `b ≤ 1` (i.e., `b = 0` or `b = 1`), the function returns `0` for every `n`, since no meaningful iterated division by the base is possible. When `n = 0`, the function returns `0` regardless of the base, because `b^0 = 1 > 0` so no positive power can be ≤ 0 and 0 is the only natural number available. When `n > 0` and `b ≥ 2`, the result is the unique `k` with `b^k ≤ n < b^(k+1)`.

### 4. Worked examples

- Claim: `VTask.log 2 8 = 3` (since `2^3 = 8 ≤ 8 < 16 = 2^4`)
  ```lean
  example : VTask.log 2 8 = 3 := by decide
  ```

- Claim: `VTask.log 2 7 = 2` (since `2^2 = 4 ≤ 7 < 8 = 2^3`)
  ```lean
  example : VTask.log 2 7 = 2 := by decide
  ```

- Claim: `VTask.log 10 999 = 2` (since `10^2 = 100 ≤ 999 < 1000 = 10^3`)
  ```lean
  example : VTask.log 10 999 = 2 := by decide
  ```

- Claim: `VTask.log 1 100 = 0` (base ≤ 1 yields 0 regardless of `n`)
  ```lean
  example : VTask.log 1 100 = 0 := by decide
  ```

- Claim: `VTask.log 2 0 = 0` (`n = 0` always yields 0)
  ```lean
  example : VTask.log 2 0 = 0 := by decide
  ```

### 5. Boundaries

- **`b = 0`**: Returns `0` for all `n`, because `0 ≤ 1` triggers the degenerate branch.
- **`b = 1`**: Returns `0` for all `n`, same reason — `1 ≤ 1` triggers the degenerate branch.
- **`n = 0`**: Returns `0` for all `b`, since there is no natural number `k ≥ 1` with `b^k ≤ 0`.
- **`n = 1`, `b ≥ 2`**: Returns `0`, because `b^0 = 1 ≤ 1 < b = b^1`.
- **`n = b^k` exactly**: Returns `k` exactly — the floor logarithm of a perfect power equals the exponent.
- **Large `n`, `b ≥ 2`**: The result grows without bound, specifically like `⌊logb b n⌋`.

### 6. Not to be confused with

- **`Nat.log2`** — specialized base-2 floor logarithm; equal to `VTask.log 2 n` but may have different definitional behaviour at edge cases.
- **`Real.logb b x`** — the real-valued logarithm in base `b` for real `x`; its natural-number floor `⌊Real.logb b n⌋₊` equals `VTask.log b n` for `b ≥ 2`, `n ≥ 1`, but it is not integer-valued in general.
- **`Int.log b r`** — the integer-valued floor logarithm for a real (or ordered field) argument `r`; coincides with `VTask.log b n` when cast appropriately, but lives in a different type.
