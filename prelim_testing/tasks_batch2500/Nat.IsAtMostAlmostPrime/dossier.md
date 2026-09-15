## Object

`VTask.IsAtMostAlmostPrime k n` is the proposition that a positive natural number `n` has **at most `k` prime factors**, counted with multiplicity (i.e., its big-Omega value `Ω(n)` is no greater than `k`). Equivalently, `n` is a nonzero natural number that can be written as a product of at most `k` primes (not necessarily distinct). This generalises the notion of an almost-prime: where an almost-prime has *exactly* `k` prime factors, this predicate allows any count from 0 up to `k`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsAtMostAlmostPrime : (k n : ℕ) -> Prop
<!-- PINNED-SIGNATURE:END -->


`(k n : ℕ) -> Prop`

The first argument `k` is the upper bound on the number of prime factors (counted with multiplicity). The second argument `n` is the natural number being tested.

## Conventions

The predicate explicitly requires `n ≠ 0`; the value `n = 0` is excluded even though `Ω(0)` might be treated as 0 in some conventions, so `VTask.IsAtMostAlmostPrime k 0` is always false regardless of `k`.

## Worked examples

- Claim: `VTask.IsAtMostAlmostPrime 3 12` holds, because 12 = 2 × 2 × 3 has Ω(12) = 3 ≤ 3 and 12 ≠ 0.

- Claim: `VTask.IsAtMostAlmostPrime 1 7` holds, because 7 is prime so Ω(7) = 1 ≤ 1 and 7 ≠ 0.

- Claim: `VTask.IsAtMostAlmostPrime 2 8` does not hold, because 8 = 2³ has Ω(8) = 3 > 2.

- Claim: `VTask.IsAtMostAlmostPrime 0 0` does not hold, because 0 is excluded by the nonzero requirement.

- Claim: `VTask.IsAtMostAlmostPrime 0 1` holds, because 1 has no prime factors (Ω(1) = 0 ≤ 0) and 1 ≠ 0.

## Boundaries

- **n = 0**: Always false, by the explicit nonzero condition.
- **n = 1**: `VTask.IsAtMostAlmostPrime k 1` holds for every `k ≥ 0`, since Ω(1) = 0.
- **k = 0**: Only `n = 1` satisfies `VTask.IsAtMostAlmostPrime 0 n`, since Ω(n) = 0 implies n = 1 for positive n.
- **Monotonicity in k**: If `VTask.IsAtMostAlmostPrime k n` holds and `k ≤ l`, then `VTask.IsAtMostAlmostPrime l n` also holds.
- **Closure under multiplication**: If `VTask.IsAtMostAlmostPrime k m` and `VTask.IsAtMostAlmostPrime l n`, then `VTask.IsAtMostAlmostPrime (k + l) (m * n)` holds.

## Not to be confused with

- **`Nat.IsAlmostPrime k n`**: The exact version — requires Ω(n) = k rather than Ω(n) ≤ k.
- **`Nat.Prime n`**: Asserts n is prime (Ω(n) = 1); a strict special case, not an upper-bound condition.
- **`Nat.ArithmeticFunction.omega n` (ω, small-omega)**: Counts *distinct* prime factors without multiplicity, unlike the big-Omega used here.