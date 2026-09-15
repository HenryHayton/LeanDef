## Object

Given two natural numbers `a` and `b` with prime factorisations `a = ∏ pᵢ^nᵢ` and `b = ∏ pᵢ^mᵢ`, `VTask.factorizationLCMRight a b` is the natural number whose prime factorisation keeps, for each prime `p`, the exponent that `p` has in `b` when that exponent **strictly exceeds** the exponent in `a`, and replaces it with `0` (i.e. that prime does not appear) otherwise. Informally it is the "strictly-b-wins" part of the factorisation of `lcm(a, b)`: together with `factorizationLCMLeft a b` (the "a-wins-or-ties" part), their product equals `lcm a b` whenever both `a` and `b` are non-zero. When either `a` or `b` is `0` the result is `1`, because `lcm(a,0) = lcm(0,b) = 0` has an empty factorisation.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.factorizationLCMRight : (a b : ℕ) -> ℕ
<!-- PINNED-SIGNATURE:END -->


`(a b : ℕ) -> ℕ`

The first argument `a` is the "reference" natural number whose prime exponents serve as the threshold: a prime's exponent from `b` is retained only if it strictly exceeds the corresponding exponent from `a`. The second argument `b` is the natural number from which the surviving prime powers are drawn.

## Conventions

When either `a` or `b` is `0`, the result is `1`. This follows from the convention that `lcm(a, 0) = lcm(0, b) = 0`, whose prime factorisation is treated as the empty product, yielding `1`.

## Worked examples

- Claim: `VTask.factorizationLCMRight 2 2 = 1` — the exponent of 2 in `b = 2` is 1, which is not strictly greater than the exponent 1 in `a = 2`, so the prime 2 contributes nothing, giving the empty product `1`.

- Claim: `VTask.factorizationLCMRight 2 4 = 4` — the exponent of 2 in `b = 4` is 2, which strictly exceeds its exponent 1 in `a = 2`, so we keep `2^2 = 4`.

- Claim: `VTask.factorizationLCMRight 4 2 = 1` — the exponent of 2 in `b = 2` is 1, which is not strictly greater than its exponent 2 in `a = 4`, so nothing is retained; result is `1`.

- Claim: `VTask.factorizationLCMRight 0 6 = 1` — since `a = 0`, `lcm(0, 6) = 0`, whose factorisation is empty; result is `1`.

- Claim: `VTask.factorizationLCMRight 6 10 = 5` — `lcm(6,10) = 30 = 2·3·5`; exponent of 2 in `b=10` is 1, not strictly greater than in `a=6` (also 1); exponent of 3 in `b` is 0, not strictly greater than in `a` (1); exponent of 5 in `b` is 1, strictly greater than in `a` (0), so we keep `5^1 = 5`.

## Boundaries

- If either `a = 0` or `b = 0`, the result is `1` (the empty product convention for `lcm = 0`).
- If `a = b ≠ 0`, every prime exponent in `b` equals the corresponding exponent in `a`, so no prime exponent is strictly greater, and the result is `1`.
- If `b` divides `a` (and both are non-zero), every prime exponent in `b` is at most the corresponding exponent in `a`, so the result is `1`.
- If `a = 1` (and `b ≠ 0`), every prime exponent in `a` is `0`, so every prime exponent in `b` (if positive) strictly exceeds it; the result equals `b`.
- The result is always positive (at least `1`) regardless of inputs.
- `VTask.factorizationLCMRight a b` always divides `b`.
- `VTask.factorizationLCMRight a b` is always coprime to `factorizationLCMLeft a b`, and their product equals `lcm a b` when both inputs are non-zero.

## Not to be confused with

- `factorizationLCMLeft a b`: the complementary factor keeping primes where `a`'s exponent is **≥** `b`'s exponent (ties go to the left factor, not the right); in particular `factorizationLCMLeft 2 2 = 2` while `factorizationLCMRight 2 2 = 1`.
- `Nat.lcm a b`: the full least common multiple, which equals `factorizationLCMLeft a b * factorizationLCMRight a b` (when both are non-zero), not just the "b-strictly-wins" part.
- `Nat.gcd a b`: the greatest common divisor, a different operation that takes the **minimum** of prime exponents rather than selecting based on which is strictly larger.