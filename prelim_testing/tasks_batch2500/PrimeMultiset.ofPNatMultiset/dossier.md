## VTask.ofPNatMultiset

### Object

A coercion that takes a multiset of positive natural numbers (`ℕ+`) together with a proof that every element of that multiset is prime, and produces the corresponding `PrimeMultiset` — that is, a multiset whose elements are provably prime positive naturals. It is essentially a validated repackaging: given that the `ℕ+` multiset already satisfies the primality requirement, the function witnesses that it may be treated as a `PrimeMultiset` without changing the underlying collection.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofPNatMultiset : (v : Multiset ℕ+) -> (h : ∀ p ∈ v, p.Prime) -> PrimeMultiset
<!-- PINNED-SIGNATURE:END -->


The first argument `v` is the multiset of positive natural numbers to be recast. The second argument `h` is a proof that every element `p` belonging to `v` is prime (in the `ℕ+` sense, i.e., `p.Prime`). Together they provide everything needed to view `v` as a legitimate `PrimeMultiset`.

### Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a total function whose domain is all pairs `(v, h)` where `h` is a valid primality proof for all elements of `v`, and the result is fully determined by those two inputs.

### Worked examples

- Claim: Applying `VTask.ofPNatMultiset` to the empty multiset (with the vacuously true primality proof) yields the empty `PrimeMultiset`.

- Claim: If `v = {2, 3, 5}` as a multiset of `ℕ+` elements and `h` witnesses that each is prime, then `VTask.ofPNatMultiset v h` is a `PrimeMultiset` of cardinality 3.

- Claim: The cardinality of `VTask.ofPNatMultiset v h` equals the cardinality of `v` for any valid pair `(v, h)`; no elements are added or removed during the conversion.

- Claim: For a singleton multiset `v = {p}` where `p : ℕ+` is prime and `h` attests to that, `VTask.ofPNatMultiset v h` contains exactly one element, namely the prime corresponding to `p`.

### Boundaries

- **Empty multiset**: When `v = 0` (the empty multiset), the hypothesis `h` holds vacuously, and the result is the empty `PrimeMultiset`. This is a well-defined and well-behaved edge case.
- **Singleton**: A single prime `p` yields a singleton `PrimeMultiset`; a single non-prime would be ruled out by the type of `h` (the proof obligation cannot be discharged).
- **Non-prime elements**: Non-prime elements cannot appear in the input in any well-typed invocation, because `h` must be provided for every element. The function is thus total on its domain but the domain itself enforces primality.
- **Multiplicity**: Elements may appear with multiplicity greater than one (e.g., `{2, 2, 3}`), and this multiplicity is preserved exactly in the resulting `PrimeMultiset`.

### Not to be confused with

- `PrimeMultiset.ofNatMultiset`: A similar coercion but starting from a `Multiset ℕ` (ordinary natural numbers) rather than `Multiset ℕ+` (positive naturals), requiring primality proofs in the `ℕ` sense.
- `PrimeMultiset.toPNatMultiset` (or its inverse): Goes in the opposite direction, producing a `Multiset ℕ+` from a `PrimeMultiset`, rather than constructing a `PrimeMultiset` from a `Multiset ℕ+`.
- `Multiset.pmap`: The underlying mapping function used to attach primality proofs element-wise; `VTask.ofPNatMultiset` is a specific application of `pmap` to the `PNat.Prime` predicate, not the general pmap operation itself.
