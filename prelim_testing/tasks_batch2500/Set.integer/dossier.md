## VTask.integer

### Object

Given a Dedekind domain `R` with fraction field `K`, and a set `S` of height-one prime ideals (non-zero primes) of `R`, the **`S`-integers of `K`** are the elements of `K` whose valuation at every height-one prime **not** in `S` is at most 1. Equivalently, they are the elements of `K` that are "integral" (have no poles) away from the primes in `S`. This forms an `R`-subalgebra of `K`, lying between `R` itself and `K`. When `S` is empty, the `S`-integers recover the integral closure of `R` in `K` (which equals `R` itself when `R` is integrally closed). When `S` is the whole height-one spectrum, the `S`-integers are all of `K`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.integer : {R : Type u} -> [CommRing R] -> [IsDedekindDomain R] -> (S : Set (IsDedekindDomain.HeightOneSpectrum R)) -> (K : Type v) -> [Field K] -> [Algebra R K] -> [IsFractionRing R K] -> Subalgebra R K
<!-- PINNED-SIGNATURE:END -->


The first argument `R` is the base Dedekind domain (inferred from context). The `CommRing R` and `IsDedekindDomain R` instances supply the ring and Dedekind-domain structures. The argument `S` is a set of height-one prime ideals of `R`; these are the "allowed poles" — primes at which elements of the `S`-integers may have negative valuation. The argument `K` is the ambient field, playing the role of the fraction field. The `Field K`, `Algebra R K`, and `IsFractionRing R K` instances confirm that `K` is indeed a fraction field of `R`. The output is the `R`-subalgebra of `K` consisting of all `S`-integers.

### Conventions

When `S` is empty, every height-one prime lies outside `S`, so membership requires valuation ≤ 1 at every height-one prime; the `S`-integers then coincide with the integral closure of `R` in `K` (equal to `R` itself when `R` is integrally closed, as it is for a Dedekind domain). When `S` is the full height-one spectrum, the condition is vacuous and the `S`-integers equal all of `K` (identified with a subalgebra). The image of `R` under the structure map `algebraMap R K` is always contained in the `S`-integers regardless of `S`, since elements of `R` have valuation ≤ 1 at every height-one prime.

### Worked examples

- Claim: Every element in the image of `algebraMap R K` belongs to `VTask.integer S K` for any set `S` of height-one primes.

- Claim: An element `x : K` is in `VTask.integer S K` if and only if `v.valuation K x ≤ 1` for every height-one prime `v` with `v ∉ S`.

- Claim: When `S` is empty, `VTask.integer S K` is the smallest `R`-subalgebra of `K` consisting of elements integral over `R` (equivalently, it coincides with the integral closure of `R` in `K`).

- Claim: For any `x : VTask.integer S K` and any height-one prime `v` with `v ∉ S`, the valuation `v.valuation K x ≤ 1`.

### Boundaries

- **`S = ∅`**: The `S`-integers are the elements of `K` integral over `R` at all height-one primes — the integral closure of `R` in `K`. For a Dedekind domain, this equals `R` (embedded in `K`).
- **`S` = full height-one spectrum**: The condition `v ∉ S` is never satisfied, so every element of `K` satisfies the membership condition; the `S`-integers equal all of `K`.
- **`S` a finite set of primes**: This recovers the classical notion of `S`-integers studied in algebraic number theory (e.g., integers away from a finite set of rational primes when `R = ℤ`, `K = ℚ`).
- The construction is functorial in `S`: enlarging `S` enlarges the ring of `S`-integers (more poles are allowed).
- Elements of `R` always belong, so `R ⊆ VTask.integer S K ⊆ K` as `R`-algebras.

### Not to be confused with

- **`IsDedekindDomain.HeightOneSpectrum.valuationSubring`**: The valuation subring of a *single* height-one prime `v` — the `S`-integers are the intersection of these subrings over all `v ∉ S`, not a single one.
- **`integralClosure R K`**: The integral closure of `R` in `K` (all elements of `K` integral over `R`) coincides with `VTask.integer ∅ K` only; in general `S`-integers allow poles at primes in `S`.
- **`FractionRing.subalgebra`** or related localizations: The `S`-integers are defined by valuation conditions, not by inverting a multiplicative set; they coincide with certain localizations only in special cases.
