## Object

`VTask.roughNumbersUpTo N k` is the finite set of positive integers up to and including `N` that are **not** `k`-smooth. Recall that a positive integer is *`k`-smooth* if every one of its prime factors is at most `k`; a number is *`k`-rough* (the complement notion) if it has at least one prime factor strictly greater than `k`. Thus `VTask.roughNumbersUpTo N k` collects all integers `n` satisfying `1 ≤ n ≤ N` and `n ∉ smoothNumbers k`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.roughNumbersUpTo : (N k : ℕ) -> Finset ℕ
<!-- PINNED-SIGNATURE:END -->


`(N k : ℕ) -> Finset ℕ`

The first argument `N` is the upper bound of the search range; the result contains only positive integers ≤ `N`. The second argument `k` is the smoothness threshold; integers whose prime factors all lie at most `k` are excluded, and only those with a prime factor exceeding `k` are included.

## Conventions

The number 0 is always excluded from the result regardless of `N` and `k`, because the definition explicitly requires `n ≠ 0`; rough numbers are by convention positive. When `k` is 0 or 1 (thresholds below any prime), every positive integer has a prime factor exceeding `k`, so `roughNumbersUpTo N k` coincides with `{1, 2, …, N}` for `N ≥ 1` (with the caveat that 1 has no prime factor at all and in Mathlib 1 is considered 0-smooth / 1-smooth, so whether 1 appears depends on the smoothNumbers convention — see Boundaries).

## Worked examples

- Claim: `5 ∈ VTask.roughNumbersUpTo 10 4` — 5 is a prime greater than 3 (the largest prime ≤ 4), so 5 is not 4-smooth, and 5 ≤ 10.

- Claim: `6 ∉ VTask.roughNumbersUpTo 10 4` — 6 = 2 × 3 has all prime factors ≤ 3 ≤ 4, so 6 is 4-smooth and is excluded.

- Claim: `VTask.roughNumbersUpTo 6 6` does not contain 6 — 6 = 2 × 3, both primes are ≤ 5 ≤ 6, so 6 is 6-smooth and absent.

- Claim: `VTask.roughNumbersUpTo 0 4 = ∅` — there are no positive integers ≤ 0, so the result is empty.

- Claim: `11 ∈ VTask.roughNumbersUpTo 12 6` — 11 is prime and 11 > 6, so 11 is not 6-smooth, and 11 ≤ 12.

## Boundaries

- **`N = 0`**: The range `{0, …, N}` contains only 0, which is excluded by the `n ≠ 0` condition, so the result is the empty finset.
- **`k = 0` or `k = 1`**: In Mathlib, `smoothNumbers 0` and `smoothNumbers 1` include only 1 (since 1 has no prime factors). Therefore `roughNumbersUpTo N 0` and `roughNumbersUpTo N 1` contain all integers from 2 to `N` (none of which are 0-smooth or 1-smooth, because they all have a prime factor > 1).
- **`k ≥ N` (large threshold)**: If `k` is at least as large as every prime ≤ `N`, all positive integers in `[1, N]` are `k`-smooth and the result is empty (or close to empty, depending on primes in range).
- **The number 1**: 1 has no prime factors, so it is vacuously `k`-smooth for every `k`. Consequently 1 never appears in `roughNumbersUpTo N k` for any `N` or `k`.
- **`n = 0`**: 0 is always excluded by the explicit `n ≠ 0` guard, independent of smoothness.

## Not to be confused with

- `Nat.smoothNumbers k` — the complementary notion: the (infinite) set of all `k`-smooth positive integers, without an upper bound.
- `VTask.roughNumbersUpTo N k` with the roles of `N` and `k` swapped — `roughNumbersUpTo k N` is a different (and likely unintended) computation.
- The set of numbers coprime to `k` — coprimality is a different condition from roughness; a number can share no factor with `k` while still being smooth.
