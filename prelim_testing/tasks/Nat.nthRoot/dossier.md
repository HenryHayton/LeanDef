## VTask.nthRoot

### Object

`VTask.nthRoot n a` computes the **floor of the real nth root of a**, i.e., the largest natural number `r` such that `r^n ≤ a`. More precisely, it equals `⌊a^(1/n)⌋₊`, the natural-number floor of `(a : ℝ)^(1/n : ℝ)`. The computation is carried out entirely in natural-number arithmetic (no floating point), using a converging Newton's-method iteration.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.nthRoot : ℕ → ℕ → ℕ
<!-- PINNED-SIGNATURE:END -->


`VTask.nthRoot : ℕ → ℕ → ℕ`

The first argument `n` is the **degree** of the root being taken (e.g., `n = 2` gives a square root, `n = 3` a cube root). The second argument `a` is the **radicand**, the natural number whose nth root is sought.

### Conventions

When the degree `n` is 0, the result is defined to be `1` for every radicand `a`. This is a junk-value convention: `a^(1/0)` is not mathematically meaningful, but the function is kept total by returning `1` (matching the convention that the empty product is 1, or that `⌊a^0⌋₊ = 1`).

### Worked examples

- Claim: `VTask.nthRoot 0 a = 1` for any `a : ℕ`  
  (The 0th-root special case always returns 1.)

- Claim: `VTask.nthRoot 1 7 = 7`  
  (The first root of any number is the number itself.)

- Claim: `VTask.nthRoot 2 9 = 3`  
  (The floor square root of 9 is exactly 3, since 3² = 9.)
  ```lean
  example : VTask.nthRoot 2 9 = 3 := by native_decide
  ```

- Claim: `VTask.nthRoot 2 10 = 3`  
  (The floor square root of 10 is 3, since 3² = 9 ≤ 10 < 16 = 4².)
  ```lean
  example : VTask.nthRoot 2 10 = 3 := by native_decide
  ```

- Claim: `VTask.nthRoot 3 27 = 3`  
  (The floor cube root of 27 is exactly 3.)
  ```lean
  example : VTask.nthRoot 3 27 = 3 := by native_decide
  ```

- Claim: `VTask.nthRoot 3 26 = 2`  
  (26 lies between 2³ = 8 and 3³ = 27, so the floor cube root is 2.)
  ```lean
  example : VTask.nthRoot 3 26 = 2 := by native_decide
  ```

- Claim: `VTask.nthRoot n (a ^ n) = a` for all `n ≠ 0` and `a : ℕ`  
  (The nth root of a perfect nth power is exact.)

### Boundaries

- **`n = 0`**: Returns `1` for every `a`, regardless of `a`. This is a definitional junk-value choice; `a^(1/0)` has no standard mathematical meaning.
- **`n = 1`**: Returns `a` unchanged, since every number is its own first root.
- **`a = 0`, `n ≠ 0`**: Returns `0`, because `0^(1/n) = 0` for positive `n`.
- **`a = 1`**: Returns `1` for any `n`, since `1^(1/n) = 1`.
- **`a = 0`, `n = 0`**: Returns `1` (the `n = 0` junk-value rule takes priority).
- **Perfect nth powers**: `VTask.nthRoot n (a ^ n) = a` for `n ≠ 0`.
- **Floor behaviour**: For non-perfect powers, the result is strictly less than the true real root; specifically, `(VTask.nthRoot n a)^n ≤ a < (VTask.nthRoot n a + 1)^n` whenever `n ≠ 0`.

### Not to be confused with

- **`Nat.sqrt`**: The built-in Mathlib integer square root; a special case (`n = 2`) of `VTask.nthRoot`, but defined and optimised separately.
- **`Real.rpow` / `NNReal.rpow`**: Real-number (possibly irrational) exponentiation giving a real-valued root, not a floored natural number.
- **`Nat.log`**: The discrete natural-number logarithm, which is the "inverse" operation in the exponent rather than the base.