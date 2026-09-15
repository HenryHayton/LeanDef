## Object

Given a multiset of natural numbers all of which are prime, `VTask.ofNatMultiset` produces the corresponding `PrimeMultiset` — a multiset whose elements are the type `Nat.Primes` (natural numbers bundled with their primality proof). It is the canonical way to promote a "flat" `Multiset ℕ` into the richer `PrimeMultiset` type when you already know every element is prime.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofNatMultiset : (v : Multiset ℕ) -> (h : ∀ p ∈ v, Nat.Prime p) -> PrimeMultiset
<!-- PINNED-SIGNATURE:END -->


`(v : Multiset ℕ) -> (h : ∀ p ∈ v, Nat.Prime p) -> PrimeMultiset`

The first argument `v` is the underlying multiset of natural numbers to be promoted. The second argument `h` is a proof that every element appearing in `v` is a prime number; it supplies the primality witness needed to wrap each element into the `Nat.Primes` subtype.

## Conventions

There are no special junk-value or edge-case conventions declared for this definition: when `v` is the empty multiset the hypothesis `h` is vacuously true and the result is the empty `PrimeMultiset`, which is entirely well-behaved and requires no special treatment.

## Worked examples

- Claim: Applying `VTask.ofNatMultiset` to the singleton multiset `{2}` with the proof that 2 is prime yields a `PrimeMultiset` of cardinality 1.

- Claim: Applying `VTask.ofNatMultiset` to the multiset `{2, 3, 5}` (with the corresponding primality proof) yields a `PrimeMultiset` whose underlying `Multiset ℕ` is `{2, 3, 5}`.

- Claim: Applying `VTask.ofNatMultiset` to the empty multiset `0` with the vacuous proof yields the empty `PrimeMultiset` (i.e., `0 : PrimeMultiset`).

## Boundaries

- **Empty multiset**: The hypothesis is vacuously satisfied and the result is the empty `PrimeMultiset`. No special handling is needed.
- **Repeated primes**: Multisets allow multiplicity, so `{2, 2, 3}` is a valid input and produces a `PrimeMultiset` with 2 appearing twice.
- **Non-prime naturals**: The function is only defined (in a meaningful sense) when every element satisfies `Nat.Prime`. The caller must supply the proof `h`; passing a multiset containing a composite or zero is ruled out by the type of `h`.
- **Size preservation**: The cardinality of the resulting `PrimeMultiset` equals the cardinality of `v`; the promotion is bijective on elements.

## Not to be confused with

- `PrimeMultiset.ofList` — constructs a `PrimeMultiset` from a `List` of primes rather than a `Multiset ℕ`.
- `PrimeMultiset.toNatMultiset` (or its coercion) — goes in the opposite direction, converting a `PrimeMultiset` back to a `Multiset ℕ`, i.e., forgets the primality witnesses.
- `Multiset.pmap` — the underlying combinator that lifts a function with a per-element precondition over a multiset; `VTask.ofNatMultiset` is a specific application of that pattern rather than the general tool.