## Object

For a commutative Artinian ring `R`, every prime ideal is maximal and every maximal ideal is prime. This equivalence makes that bijection explicit and canonical: it is a type equivalence between the prime spectrum of `R` (the type of prime ideals of `R`) and the maximal spectrum of `R` (the type of maximal ideals of `R`), sending each prime ideal to itself viewed as a maximal ideal, and vice versa.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.primeSpectrumEquivMaximalSpectrum : {R : Type u_1} -> [CommRing R] -> [IsArtinianRing R] -> PrimeSpectrum R ≃ MaximalSpectrum R
<!-- PINNED-SIGNATURE:END -->


`VTask.primeSpectrumEquivMaximalSpectrum : {R : Type u_1} -> [CommRing R] -> [IsArtinianRing R] -> PrimeSpectrum R ≃ MaximalSpectrum R`

The implicit type argument `R` is the commutative ring over which both spectra are formed. The `CommRing R` instance supplies the ring structure. The `IsArtinianRing R` instance is the crucial hypothesis: it is the Artinian condition that forces every prime ideal to be maximal (and every maximal ideal to be prime), making the bijection possible. There are no explicit term arguments; the equivalence itself is the output.

## Conventions

The forward and backward maps are both the identity on underlying ideals: both directions of the equivalence act as the identity function on the set-theoretic ideal, merely retagging the proof that the ideal is prime (resp. maximal) into a proof that it is maximal (resp. prime). There are no junk values because the equivalence is defined on every element of both types without restriction.

## Worked examples

- Claim: For `R = ZMod 6` (which is Artinian), the forward map of `VTask.primeSpectrumEquivMaximalSpectrum` sends a prime ideal `I` to a maximal ideal with the same underlying ideal.

- Claim: For any Artinian commutative ring `R` and prime ideal `I : PrimeSpectrum R`, the underlying ideal of `(VTask.primeSpectrumEquivMaximalSpectrum I)` equals `I.asIdeal`.

- Claim: The equivalence `VTask.primeSpectrumEquivMaximalSpectrum` for an Artinian ring is an equivalence of types, so its composition with its inverse is the identity on `PrimeSpectrum R`.

## Boundaries

- The Artinian hypothesis is essential: without it, prime ideals need not be maximal (e.g., in `ℤ` the zero ideal is prime but not maximal). The definition is simply not available without `IsArtinianRing R`.
- The equivalence is canonical in the sense that it does not make any arbitrary choices: both maps are determined uniquely by the underlying ideal.
- For a field (a trivially Artinian ring), both the prime spectrum and the maximal spectrum contain exactly one element (the zero ideal), and the equivalence is the unique bijection between two singletons.
- For the zero ring, both spectra are empty and the equivalence is the unique bijection between two empty types.

## Not to be confused with

- `PrimeSpectrum R` alone: the type of prime ideals without any claim of equivalence with maximal ideals; this makes sense for any commutative ring, not just Artinian ones.
- `MaximalSpectrum R` alone: the type of maximal ideals without any equivalence; again defined for any commutative ring.
- The theorem `isPrime_iff_isMaximal` (or similar): a bare propositional statement that a specific ideal is prime iff it is maximal in an Artinian ring, as opposed to the bundled type equivalence between the two spectrum types that `VTask.primeSpectrumEquivMaximalSpectrum` provides.