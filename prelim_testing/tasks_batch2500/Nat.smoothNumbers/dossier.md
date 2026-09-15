## VTask.smoothNumbers

### Object

`VTask.smoothNumbers n` is the set of positive natural numbers that are *n-smooth*: a positive natural number `m` belongs to this set if and only if every prime factor of `m` is strictly less than `n`. Equivalently, these are the nonzero natural numbers whose prime factorization uses only primes from the set `{2, 3, 5, …, p}` where `p` is the largest prime below `n`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.smoothNumbers : (n : ℕ) -> Set ℕ
<!-- PINNED-SIGNATURE:END -->


```
VTask.smoothNumbers : (n : ℕ) -> Set ℕ
```

The single argument `n` is the smoothness bound: a natural number belongs to the set precisely when all of its prime factors are strictly less than `n`.

### Conventions

Zero is excluded from every smooth-numbers set: membership requires the number to be nonzero, so `0 ∉ VTask.smoothNumbers n` for every `n`. The special case `VTask.smoothNumbers 0` equals the singleton `{1}`, because `1` is the only positive natural number with no prime factors at all, and the vacuous condition on prime factors is trivially satisfied.

### Worked examples

- Claim: `12 ∈ VTask.smoothNumbers 5` because the prime factors of 12 are 2 and 3, both strictly less than 5.

- Claim: `15 ∉ VTask.smoothNumbers 5` because 5 is a prime factor of 15 and 5 is not strictly less than 5.

- Claim: `1 ∈ VTask.smoothNumbers 0` — the number 1 has no prime factors, so the condition is vacuously satisfied and `VTask.smoothNumbers 0 = {1}`.

- Claim: `0 ∉ VTask.smoothNumbers 7` — zero is excluded by the nonzero requirement regardless of the smoothness bound.

- Claim: `6 ∈ VTask.smoothNumbers 4` because the prime factors of 6 are 2 and 3, both strictly less than 4.

### Boundaries

- **`n = 0`:** The set `VTask.smoothNumbers 0` equals `{1}`. Only 1 qualifies, since it is the unique positive natural number with no prime factors.
- **`n = 1`:** No prime is less than 1, so any nonzero number with at least one prime factor is excluded. Again only `1` (which has no prime factors) belongs to `VTask.smoothNumbers 1`, making it equal to `{1}` as well.
- **`n = 2`:** The only prime less than 2 is… none, so again the set equals `{1}`.
- **`n = 3`:** Only powers of 2 (which are nonzero) belong, since the sole prime less than 3 is 2.
- **`m = 0`:** Zero is never a member of `VTask.smoothNumbers n` for any `n`, because membership requires `m ≠ 0`.
- **`n` composite vs. prime:** Passing a composite value `N` gives the same set as passing `N+1` when `N` is not prime (`VTask.smoothNumbers_succ`), so the set changes only at prime values of `n`.
- **Monotonicity:** `VTask.smoothNumbers n ⊆ VTask.smoothNumbers (n+1)` — a larger bound admits more numbers.

### Not to be confused with

- **`smoothNumbersUpTo N k`** — a *finite* set of numbers that are both at most `N` and `k`-smooth; this is a finset, not the infinite set of all smooth numbers.
- **`factoredNumbers S`** — the generalization where the allowed prime factors come from an arbitrary finset `S` rather than the initial segment `{p | p < n}`.
- **`Nat.primeFactors m`** — the finset of prime factors of a fixed number `m`, as opposed to the set of all numbers whose prime factors lie below a bound.