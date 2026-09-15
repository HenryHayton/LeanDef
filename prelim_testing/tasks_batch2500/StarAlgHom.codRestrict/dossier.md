## VTask.codRestrict

### Object

Given a star algebra homomorphism `f : A →⋆ₐ[R] B` and a star subalgebra `S` of `B` that contains the entire image of `f`, `VTask.codRestrict f S hf` is the star algebra homomorphism `A →⋆ₐ[R] S` obtained by viewing `f` as landing in `S` rather than in the larger ambient algebra `B`. It is the same map as `f` on underlying elements, but with codomain tightened to `S`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.codRestrict : {R : Type u_2} -> {A : Type u_3} -> {B : Type u_4} -> [CommSemiring R] -> [StarRing R] -> [Semiring A] -> [Algebra R A] -> [StarRing A] -> [Semiring B] -> [Algebra R B] -> [StarRing B] -> [StarModule R B] -> (f : A →⋆ₐ[R] B) -> (S : StarSubalgebra R B) -> (hf : ∀ (x : A), f x ∈ S) -> A →⋆ₐ[R] ↥S
<!-- PINNED-SIGNATURE:END -->


`{R : Type u_2} -> {A : Type u_3} -> {B : Type u_4} -> [CommSemiring R] -> [StarRing R] -> [Semiring A] -> [Algebra R A] -> [StarRing A] -> [Semiring B] -> [Algebra R B] -> [StarRing B] -> [StarModule R B] -> (f : A →⋆ₐ[R] B) -> (S : StarSubalgebra R B) -> (hf : ∀ (x : A), f x ∈ S) -> A →⋆ₐ[R] ↥S`

`R` is the commutative semiring of scalars over which everything is an algebra. `A` is the source star `R`-algebra. `B` is the target star `R`-algebra containing `S`. The argument `f` is the star algebra homomorphism whose codomain is to be restricted. The argument `S` is the star subalgebra of `B` to which the codomain is restricted. The argument `hf` is the proof that every element in the image of `f` lies in `S`, justifying the restriction.

### Conventions

There are no junk-value or edge-case conventions declared for this construction: the function is well-defined whenever its explicit arguments are supplied, and no inputs are outside the natural domain.

### Worked examples

- Claim: For any `f : A →⋆ₐ[R] B`, `S`, and proof `hf`, the coercion of `VTask.codRestrict f S hf x` back to `B` equals `f x` for every `x : A`.

- Claim: The composition of the canonical inclusion `S.subtype` with `VTask.codRestrict f S hf` is equal to `f` as a map `A →⋆ₐ[R] B`.

- Claim: `VTask.codRestrict f S hf` is injective if and only if `f` itself is injective.

### Boundaries

- If `S = ⊤` (the top star subalgebra, equal to all of `B`), then `VTask.codRestrict f ⊤ hf` is essentially the same as `f` up to the identification of `↥⊤` with `B`.
- The proof `hf` must cover every element of `A`; there is no partial restriction. If only a subset of `A` mapped into `S`, the construction would not type-check.
- The resulting map is a genuine star `R`-algebra homomorphism into `S`; in particular it respects the star operation, the algebra scalar action of `R`, and the ring structure of `S`.
- When `f` is surjective onto `S` (i.e., every element of `S` is in the image of `f`), the restricted map `VTask.codRestrict f S hf` is a surjective star algebra homomorphism onto `S`.

### Not to be confused with

- `StarAlgHom.restrict` (domain restriction): restricts the *source* algebra to a star subalgebra, whereas `VTask.codRestrict` restricts the *codomain*.
- `NonUnitalStarAlgHom.codRestrict`: the analogous codomain restriction for *non-unital* star algebra homomorphisms; the present definition requires unitality.
- `AlgHom.codRestrict`: the codomain restriction for plain (non-star) algebra homomorphisms; `VTask.codRestrict` additionally verifies compatibility with the star operation.
