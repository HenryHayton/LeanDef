## Object

`VTask.toNonUnitalStarSubalgebra` converts a non-unital subalgebra (over a commutative semiring `R`, inside a non-unital semiring `A` with a star operation) into a non-unital star subalgebra, by supplying a proof that the subalgebra is closed under the star involution. The resulting object carries exactly the same underlying set and algebraic structure as the original subalgebra, but is additionally equipped with the star-closure data that promotes it to a star subalgebra.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toNonUnitalStarSubalgebra : {R : Type u} -> {A : Type v} -> [CommSemiring R] -> [NonUnitalSemiring A] -> [Module R A] -> [Star A] -> (s : NonUnitalSubalgebra R A) -> (h_star : ∀ x ∈ s, star x ∈ s) -> NonUnitalStarSubalgebra R A
<!-- PINNED-SIGNATURE:END -->


`VTask.toNonUnitalStarSubalgebra : {R : Type u} -> {A : Type v} -> [CommSemiring R] -> [NonUnitalSemiring A] -> [Module R A] -> [Star A] -> (s : NonUnitalSubalgebra R A) -> (h_star : ∀ x ∈ s, star x ∈ s) -> NonUnitalStarSubalgebra R A`

The implicit type `R` is the commutative semiring of scalars. The implicit type `A` is the ambient non-unital semiring equipped with the scalar `R`-module structure and a star involution. The argument `s` is the non-unital subalgebra to be promoted. The argument `h_star` is the proof witnessing that `s` is closed under the star operation: for every element `x` belonging to `s`, its star `star x` also belongs to `s`.

## Conventions

No junk-value or edge conventions have been declared for this definition, since it is a total constructor requiring explicit arguments and produces a fully-specified algebraic structure whenever called.

## Worked examples

- Claim: For any non-unital subalgebra `s` and closure proof `h`, the carrier of `VTask.toNonUnitalStarSubalgebra s h` equals the carrier of `s` (the underlying sets coincide).

- Claim: Every element `x` of a non-unital subalgebra `s` that is also in the non-unital star subalgebra produced by `VTask.toNonUnitalStarSubalgebra s h` satisfies `star x ∈ VTask.toNonUnitalStarSubalgebra s h`, because `h` witnesses star-closure of `s`.

- Claim: If `s` is a non-unital subalgebra closed under `star`, the ring-theoretic operations (addition, scalar multiplication, multiplication) on `VTask.toNonUnitalStarSubalgebra s h` are inherited from those of `s` without change.

## Boundaries

- The function is total: it is defined for any non-unital subalgebra `s` and any proof `h_star`, with no restrictions on the types or the content of `s`.
- If `s` is already the entire ambient algebra `A`, then `VTask.toNonUnitalStarSubalgebra s h` is a non-unital star subalgebra with carrier equal to all of `A`.
- The construction does not add any new elements to `s`; the underlying carrier set is identical before and after the promotion.
- The `h_star` argument is mandatory; there is no automatic inference of star-closure, so the caller must supply it explicitly.

## Not to be confused with

- `NonUnitalStarSubalgebra` (the type itself): this is the target type, not the constructor that produces values of that type from a plain subalgebra.
- A unital star subalgebra (`StarSubalgebra`): that structure additionally requires a unit element and lives over a unital ring, whereas this construction is strictly non-unital.
- The forgetful direction `NonUnitalStarSubalgebra.toNonUnitalSubalgebra`: that map discards the star data and goes the opposite way, from a star subalgebra to a plain subalgebra.