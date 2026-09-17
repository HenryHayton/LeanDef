## Object

`VTask.ProbablePrime n b` is the proposition that the natural number `n` passes the **Fermat primality test** with respect to base `b`. Concretely, it asserts that `n` divides `b^(n-1) - 1` (arithmetic in ℕ, so subtraction is truncated). Every genuine prime `p` satisfies this for any base `b` coprime to `p` (Fermat's little theorem), but composite numbers can satisfy it too — those are called **Fermat pseudoprimes** to base `b`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ProbablePrime : (n b : ℕ) -> Prop
<!-- PINNED-SIGNATURE:END -->


VTask.ProbablePrime : (n b : ℕ) -> Prop

The first argument `n` is the number being tested for primality. The second argument `b` is the base used in the Fermat test.

## Conventions

Because subtraction is truncated in ℕ, `b^(n-1) - 1` equals `0` when `b^(n-1) = 0` or `b^(n-1) ≤ 1`; in particular, every `n` divides `0`, so edge cases propagate freely. Specifically: every natural number `n` is a probable prime to base `0` (since `0^(n-1) = 0` for `n ≥ 1`, and `0^0 = 1` so `0-1 = 0` for `n = 0`, all yielding divisibility of `n` into `0`). Similarly, every `n` is a probable prime to base `1` (since `1^(n-1) = 1`, and `1 - 1 = 0` in ℕ). Furthermore, `n = 0` and `n = 1` are probable primes to every base (since `0 ∣ 0` and `1 ∣ k` for all `k`).

## Worked examples

- Claim: `VTask.ProbablePrime 5 2` holds — 5 is a probable prime to base 2 (5 divides 2^4 - 1 = 15).
  ```lean
  example : VTask.ProbablePrime 5 2 := by decide
  ```

- Claim: `VTask.ProbablePrime 341 2` holds — 341 = 11 × 31 is the smallest Fermat pseudoprime to base 2 (341 divides 2^340 - 1).
  ```lean
  example : VTask.ProbablePrime 341 2 := by decide
  ```

- Claim: `VTask.ProbablePrime 6 2` does not hold — 6 does not divide 2^5 - 1 = 31.
  ```lean
  example : ¬ VTask.ProbablePrime 6 2 := by decide
  ```

- Claim: `VTask.ProbablePrime 100 1` holds — every `n` is a probable prime to base 1.
  ```lean
  example : VTask.ProbablePrime 100 1 := by decide
  ```

- Claim: `VTask.ProbablePrime 1 37` holds — 1 is a probable prime to every base.
  ```lean
  example : VTask.ProbablePrime 1 37 := by decide
  ```

## Boundaries

- **`n = 0`**: `0 ∣ b^(0-1) - 1 = b^0 - 1 = 1 - 1 = 0` in ℕ (since `0^0 = 1` by convention, and `1 - 1 = 0`), so `VTask.ProbablePrime 0 b` holds for all `b` (as `0 ∣ 0`).
- **`n = 1`**: `1 ∣ k` for every `k`, so `VTask.ProbablePrime 1 b` holds for all `b`.
- **`b = 0`**: For `n ≥ 2`, `0^(n-1) = 0`, so `b^(n-1) - 1 = 0 - 1 = 0` in ℕ; hence `n ∣ 0` holds. For `n = 0` or `n = 1` the same applies as above. So `VTask.ProbablePrime n 0` holds for all `n`.
- **`b = 1`**: `1^(n-1) = 1` and `1 - 1 = 0` in ℕ, so `n ∣ 0` holds for all `n`. Thus `VTask.ProbablePrime n 1` holds for all `n`.
- **Coprimality**: When `n ≥ 1` and `b ≥ 1`, `VTask.ProbablePrime n b` implies `n` and `b` are coprime.
- **Modular arithmetic equivalence**: For `b ≥ 1`, `VTask.ProbablePrime n b` is equivalent to `b^(n-1) ≡ 1 [MOD n]`.

## Not to be confused with

- **`Nat.Prime`**: The proposition that `n` is a genuine prime; probable primality is a necessary (but not sufficient) condition for many bases, and `VTask.ProbablePrime` admits composite numbers (pseudoprimes).
- **`Nat.IsCoprime`** / **`Nat.Coprime`**: Coprimality of `n` and `b` is a *consequence* of probable primality (when both are ≥ 1), not the same notion.
- **Miller–Rabin witness**: A stronger primality test; `VTask.ProbablePrime` is the weaker Fermat test only, which does not detect Carmichael numbers.