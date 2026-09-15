## Object

`VTask.ofNatList` converts a list of natural numbers, all of which are prime, into a `PrimeMultiset` — the multiset of prime numbers (with multiplicity) used in Mathlib's development of unique factorisation. The resulting `PrimeMultiset` carries exactly the same elements as the input list, viewed as a bag (multiset) of primes, with no ordering information retained.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofNatList : (l : List ℕ) -> (h : ∀ p ∈ l, Nat.Prime p) -> PrimeMultiset
<!-- PINNED-SIGNATURE:END -->


```
VTask.ofNatList : (l : List ℕ) -> (h : ∀ p ∈ l, Nat.Prime p) -> PrimeMultiset
```

The first argument is the list of natural numbers to be promoted. The second argument is a proof that every element of that list is a prime number; it acts as a certificate licensing the embedding of each element into the type of primes.

## Conventions

There are no junk-value or boundary conventions of special note for this definition: the function is total over all lists satisfying the primality hypothesis, and it simply carries the list (treated as an unordered bag) faithfully into `PrimeMultiset`.

## Worked examples

- Claim: `VTask.ofNatList [] (by simp)` equals the empty `PrimeMultiset`.

- Claim: `VTask.ofNatList [2, 3, 2] h` (with appropriate `h`) is a `PrimeMultiset` in which the prime `2` appears with multiplicity 2 and the prime `3` appears with multiplicity 1.

- Claim: `VTask.ofNatList [5] h` (with `h` proving `5` is prime) is a `PrimeMultiset` whose underlying multiset has cardinality 1 and contains the prime `5`.

- Claim: For any list `l` with primality proof `h`, the cardinality of `VTask.ofNatList l h` as a multiset equals the length of `l`.

## Boundaries

- When `l = []`, the result is the empty `PrimeMultiset`, and the primality hypothesis is vacuously satisfied by any proof.
- Duplicate entries in `l` are preserved: if a prime `p` appears `k` times in `l`, it appears with multiplicity `k` in the resulting `PrimeMultiset`.
- The list order is forgotten: `VTask.ofNatList [2, 3] h` and `VTask.ofNatList [3, 2] h` produce the same `PrimeMultiset`.
- The primality hypothesis must cover every element; a list containing a composite or `0` or `1` cannot legally be supplied, as no valid proof `h` exists for it.

## Not to be confused with

- `PrimeMultiset.ofNatMultiset`: the analogous constructor for `Multiset ℕ` rather than `List ℕ`; `VTask.ofNatList` is defined by coercing through this.
- `Multiset.ofList`: coerces a `List α` to `Multiset α` without any primality requirement or promotion to `PrimeMultiset`.
- `Nat.factors`: produces a `List ℕ` of prime factors of a number, which can then be fed into `VTask.ofNatList`, but is a distinct operation (factorisation rather than packaging).