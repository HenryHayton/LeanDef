## VTask.divisors

### 1. Object

`VTask.divisors n` is the finite set of all positive divisors of the natural number `n`. For example, the divisors of 12 are {1, 2, 3, 4, 6, 12}. By convention, the divisors of 0 form the empty set.

### 2. Signature

```
VTask.divisors : (n : ℕ) -> Finset ℕ
```

- `n : ℕ` — the natural number whose divisors are sought.
- Returns a `Finset ℕ` containing exactly the positive natural numbers that divide `n`.

### 3. Conventions

The divisors of 0 are defined to be the empty finset `∅`; this is a junk-value convention adopted because every natural number divides 0, which would make a "genuine" answer infinite and thus not a `Finset`.

### 4. Worked examples

- Claim: The divisors of 1 are exactly {1}.
- Claim: The divisors of a prime `p` are exactly {1, p}.
- Claim: The divisors of 12 are {1, 2, 3, 4, 6, 12}.
- Claim: The divisors of 0 are the empty finset.
- Claim: A natural number `d` belongs to `VTask.divisors n` if and only if `d` is a positive divisor of `n` (i.e., `d ∣ n` and `0 < d`).
- Claim: The function `VTask.divisors` is injective: distinct natural numbers have distinct divisor sets.

### 5. Boundaries

- **`n = 0`**: Returns `∅`. This is a deliberate convention, not a mathematical statement that 0 has no divisors; rather, the set of divisors of 0 would be infinite, so it is defined to be empty.
- **`n = 1`**: Returns `{1}`, the singleton containing only 1, since 1 is the sole positive divisor of 1.
- **Prime `p`**: Returns `{1, p}`, a two-element set.
- **`d ∈ VTask.divisors n` characterisation**: A natural number `d` is a member of `VTask.divisors n` if and only if `d ∣ n` and `1 ≤ d` (equivalently, `0 < d`). In particular, 0 is never a member of any divisor set.
- **Multiplicativity**: For positive `m` and `n`, the divisors of `m * n` equal the `Finset`-product of the divisors of `m` and the divisors of `n`.

### 6. Not to be confused with

- **`Nat.divisorsAntidiagonal n`**: returns pairs `(a, b)` with `a * b = n`, rather than individual divisors.
- **`Nat.factors n`**: returns the multiset of prime factors of `n` (with repetition), not the set of all positive divisors.
- **`Nat.properDivisors n`**: the set of divisors of `n` strictly less than `n`; it excludes `n` itself, unlike `VTask.divisors`.
