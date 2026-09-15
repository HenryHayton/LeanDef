## Object

Given a ring isomorphism `e : A ≃+* B` between two commutative semirings, and an ideal `I` of `A` whose image under `e` equals an ideal `J` of `B`, `VTask.equiv h` is the canonical **bijection** (in fact, an equivalence of types) between the set of divided power structures on `I` and the set of divided power structures on `J`. It transports any divided power structure on `I` to one on `J` via `e`, and likewise transports a structure on `J` back to one on `I` via `e⁻¹`, and these two operations are mutually inverse.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.equiv : {A : Type u_1} -> {B : Type u_2} -> [CommSemiring A] -> {I : Ideal A} -> [CommSemiring B] -> {J : Ideal B} -> {e : A ≃+* B} -> (h : Ideal.map e I = J) -> DividedPowers I ≃ DividedPowers J
<!-- PINNED-SIGNATURE:END -->


The implicit arguments fix two commutative semirings `A` and `B` with their respective `CommSemiring` instances, an ideal `I` of `A`, and an ideal `J` of `B`. The explicit argument `e : A ≃+* B` is the ring isomorphism used to identify the two ambient rings. The explicit proof argument `h : Ideal.map e I = J` witnesses that `e` sends `I` exactly onto `J`, which is the necessary compatibility condition for the transfer to be well-defined.

## Conventions

No junk-value or edge-case conventions are declared for this definition: it is a total construction on types with no distinguished default behaviour at boundary inputs.

## Worked examples

- Claim: For the identity ring isomorphism on a commutative semiring `A` with ideal `I`, applying `VTask.equiv` (with the proof that the image of `I` is `I`) sends a divided power structure `dp` on `I` to a divided power structure whose `dpow n a` values agree with those of `dp n a` for all `n` and `a ∈ I`.

- Claim: The forward function of `VTask.equiv h` followed by the inverse function returns the original divided power structure, i.e., `(VTask.equiv h).symm ((VTask.equiv h) dp) = dp` for any divided power structure `dp` on `I`.

- Claim: The inverse of the equivalence produced by `VTask.equiv h` coincides with `VTask.equiv` applied to the symmetric proof `Ideal.map e.symm J = I`.

## Boundaries

- When `A = B` and `e` is the identity ring isomorphism and `I = J`, the equivalence is essentially the identity on divided power structures.
- The construction is entirely determined by `h`; if two proofs `h` and `h'` of `Ideal.map e I = J` are given, they are propositionally equal (since ideal equality is a proposition), so the equivalences they produce are equal.
- The equivalence is an isomorphism of types (a bijection), not merely an injection or surjection: both the forward and backward maps are explicitly provided and verified to be mutual inverses.

## Not to be confused with

- `DividedPowers.ofRingEquiv`: this is the underlying function that sends a divided power structure on `I` to one on `J`; `VTask.equiv` bundles both directions together into a type equivalence.
- `RingEquiv` (ring isomorphism): the input `e` is a ring isomorphism between the ambient rings, whereas `VTask.equiv h` is an equivalence between the corresponding *sets of divided power structures*, which are not rings themselves.
- Transfer lemmas for individual divided power axioms: `VTask.equiv` packages the entire structure as a single bijection, rather than stating that individual axioms are preserved.