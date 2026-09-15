## VTask.minFac

### Object

`VTask.minFac n` returns the smallest prime factor of the natural number `n`, with two special conventions for degenerate inputs: the value at `n = 0` is `2`, and the value at `n = 1` is `1` (a junk value, since 1 has no prime factors).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.minFac : (n : ℕ) -> ℕ
<!-- PINNED-SIGNATURE:END -->


```
VTask.minFac : (n : ℕ) -> ℕ
```

The single argument `n` is the natural number whose smallest prime factor is sought.

### Conventions

For `n = 0`, the function returns `2`. This is a junk value because 0 has no smallest prime factor in the usual mathematical sense, but 2 is a consistent and convenient sentinel (it divides 0). For `n = 1`, the function returns `1`. Again this is a junk value; 1 has no prime factors, so there is no true smallest prime factor, and `1` is the chosen sentinel. For every `n ≥ 2`, the function returns the genuine smallest prime factor of `n`.

### Worked examples

- Claim: `VTask.minFac 0 = 2` (the junk-value case for 0)
  ```lean
  example : VTask.minFac 0 = 2 := by native_decide
  ```

- Claim: `VTask.minFac 1 = 1` (the special junk-value case)

- Claim: `VTask.minFac 2 = 2` (2 is prime, so its smallest prime factor is itself)
  ```lean
  example : VTask.minFac 2 = 2 := by native_decide
  ```

- Claim: `VTask.minFac 15 = 3` (15 = 3 × 5, so the smallest prime factor is 3)

- Claim: `VTask.minFac 49 = 7` (49 = 7², so the smallest prime factor is 7)

- Claim: `VTask.minFac 12 = 2` (12 is even, so 2 is its smallest prime factor)
  ```lean
  example : VTask.minFac 12 = 2 := by native_decide
  ```

### Boundaries

- **`n = 0`**: Returns `2`. Zero is divisible by every positive integer, including 2, so 2 is a natural sentinel. Note `2 ∣ 0` holds in the natural numbers.
- **`n = 1`**: Returns `1`. This is a junk/sentinel value; `1` is not prime, and 1 has no prime factors. The fact `VTask.minFac n = 1 ↔ n = 1` characterises this case exactly.
- **`n = 2`**: Returns `2` (the smallest and only prime factor of 2).
- **`n` prime**: Returns `n` itself.
- **`n` even, `n ≥ 2`**: Returns `2`.
- **`n` odd composite**: Returns the smallest odd prime dividing `n`; the search starts from 3.
- For all `n ≠ 1`, `VTask.minFac n` is prime and divides `n`.
- For all `n > 0`, `VTask.minFac n ≤ n`.
- For all `n`, `VTask.minFac n > 0`.

### Not to be confused with

- **`Nat.factors n`**: Returns the full list of prime factors of `n` with multiplicity, not just the smallest one.
- **`Nat.minFacAux n k`**: An internal helper that searches for the smallest factor of `n` starting from a given odd candidate `k`; not meant to be called directly.
- **`Nat.sqrt n`**: Computes the integer square root of `n`; sometimes confused with `minFac` because primality testing via `minFac` involves comparing against `sqrt`.