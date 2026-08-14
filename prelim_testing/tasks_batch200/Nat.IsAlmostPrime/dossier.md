## Object

`VTask.IsAlmostPrime k n` is the predicate asserting that the natural number `n` is **k-almost prime**: `n` is nonzero and has exactly `k` prime factors when counted with multiplicity. Under this definition, `1` is 0-almost prime (it has no prime factors), every prime `p` is 1-almost prime, products of exactly two primes (e.g., `6 = 2 × 3` or `4 = 2²`) are 2-almost prime, and so on.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsAlmostPrime : (k n : ℕ) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsAlmostPrime : (k n : ℕ) -> Prop`

The first argument `k` is the prescribed number of prime factors (counted with multiplicity) that `n` must have. The second argument `n` is the natural number being tested for membership in the class of k-almost primes.

## Conventions

The value `n = 0` is explicitly excluded: `0` is not considered k-almost prime for any `k`. This is the sole junk-value convention; it prevents `0` from satisfying the predicate despite its prime-factor count being conventionally undefined or infinite.

## Worked examples

- Claim: `VTask.IsAlmostPrime 0 1` holds, because `1` is nonzero and has zero prime factors counted with multiplicity.

- Claim: `VTask.IsAlmostPrime 1 p` holds for any prime `p`, since a prime has exactly one prime factor (itself, with multiplicity one); this is captured by the theorem `Nat.Prime.isAlmostPrime_one`.

- Claim: `VTask.IsAlmostPrime 2 6` holds, because `6 = 2 × 3` is nonzero and has exactly two prime factors counted with multiplicity.

- Claim: `VTask.IsAlmostPrime 2 4` holds, because `4 = 2²` is nonzero and has exactly two prime factors counted with multiplicity (the prime `2` appears twice).

- Claim: `¬ VTask.IsAlmostPrime 1 1` holds, since `1` has zero prime factors, not one.

- Claim: `¬ VTask.IsAlmostPrime 0 0` holds, since `0` is excluded from all k-almost prime classes.

## Boundaries

- **`n = 0`**: Not k-almost prime for any `k`; the nonzero side condition explicitly rules this out.
- **`n = 1`, `k = 0`**: `1` is the unique 0-almost prime; `isAlmostPrime_zero_iff` characterises this class as exactly `{1}`.
- **`k = 1`**: The 1-almost primes are exactly the primes; `isAlmostPrime_one_iff` establishes this equivalence.
- **`k = 2`**: The 2-almost primes (semiprimes) include both products of two distinct primes and squares of primes.
- **Multiplicativity**: If `m` is k-almost prime and `n` is l-almost prime, then `m * n` is (k+l)-almost prime, by `IsAlmostPrime.mul`.

## Not to be confused with

- **`Nat.IsAtMostAlmostPrime l n`**: A weaker predicate asserting that `n` has *at most* `l` prime factors counted with multiplicity, rather than exactly `l`.
- **`Nat.Prime n`**: Primality is exactly 1-almost primality; `IsAlmostPrime 1 n ↔ n.Prime` holds, but `IsAlmostPrime` generalises this to arbitrary factor counts.
- **`Nat.squarefree n`** (or related predicates): Squarefreeness concerns whether prime factors appear with multiplicity greater than one, a different condition from counting the total number of prime factors.