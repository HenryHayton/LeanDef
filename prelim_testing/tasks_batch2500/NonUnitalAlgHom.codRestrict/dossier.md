## Object

`VTask.codRestrict` takes a non-unital algebra homomorphism `f : A → B` (presented via its type-class abstraction) together with a non-unital sub-algebra `S` of `B` and a proof that every element of the image of `f` lies in `S`, and produces a new non-unital `R`-algebra homomorphism `A →ₙₐ[R] S` that agrees with `f` pointwise but has its codomain tightened to `S`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.codRestrict : {F : Type v'} -> {R : Type u} -> {A : Type v} -> {B : Type w} -> [CommSemiring R] -> [NonUnitalNonAssocSemiring A] -> [Module R A] -> [NonUnitalNonAssocSemiring B] -> [Module R B] -> [FunLike F A B] -> [NonUnitalAlgHomClass F R A B] -> (f : F) -> (S : NonUnitalSubalgebra R B) -> (hf : ∀ (x : A), f x ∈ S) -> A →ₙₐ[R] ↥S
<!-- PINNED-SIGNATURE:END -->


`VTask.codRestrict : {F : Type v'} -> {R : Type u} -> {A : Type v} -> {B : Type w} -> [CommSemiring R] -> [NonUnitalNonAssocSemiring A] -> [Module R A] -> [NonUnitalNonAssocSemiring B] -> [Module R B] -> [FunLike F A B] -> [NonUnitalAlgHomClass F R A B] -> (f : F) -> (S : NonUnitalSubalgebra R B) -> (hf : ∀ (x : A), f x ∈ S) -> A →ₙₐ[R] ↥S`

The implicit type arguments `F`, `R`, `A`, `B` are, respectively, the type of the morphism being restricted, the scalar semiring, the domain algebra, and the codomain algebra. The instance arguments supply the algebraic and module structures on these types, as well as the evidence that `F` is a valid type of non-unital `R`-algebra homomorphisms from `A` to `B`. The explicit argument `f` is the non-unital algebra homomorphism whose codomain is to be restricted. The argument `S` is the target non-unital sub-algebra of `B` into which `f` is being restricted. The argument `hf` is the membership proof that `f` maps every element of `A` into `S`.

## Conventions

There are no junk-value or edge-case conventions for this definition: it is a total construction whose inputs are fully constrained by the type system and the explicit membership proof `hf`, so no special sentinel or boundary conventions are declared.

## Worked examples

- Claim: For any `f : A →ₙₐ[R] B`, non-unital sub-algebra `S`, and proof `hf` that the image lies in `S`, the underlying element satisfies `↑(VTask.codRestrict f S hf x) = f x` for every `x : A`.

- Claim: Composing the canonical inclusion (subtype map) of `S` into `B` with `VTask.codRestrict f S hf` recovers `f` as a non-unital algebra homomorphism `A →ₙₐ[R] B`.

- Claim: `VTask.codRestrict f S hf` is injective as a function if and only if `f` itself is injective.

## Boundaries

- If `f` already maps into all of `B` (i.e., `S = ⊤`), the construction still applies; the result is a morphism into the whole algebra, which canonically identifies with `f`.
- The membership proof `hf` is required to cover all of `A`; there is no partial restriction. Supplying a proof for a strict subset of `A` is not possible at this type.
- The construction does not require `f` to be surjective onto `S`; `S` may be strictly larger than the image of `f`.
- When `A` is the zero ring or `f` is the zero homomorphism, the image of every element is `0`, and any sub-algebra containing `0` provides a valid `S` and `hf`.

## Not to be confused with

- `NonUnitalAlgHom.restrict` (domain restriction): restricts the *domain* of a non-unital algebra homomorphism to a sub-algebra of `A`, rather than the codomain.
- `AlgHom.codRestrict`: the unital analogue, which works with unital algebra homomorphisms and unital sub-algebras; this version explicitly handles the non-unital setting.
- `NonUnitalSubalgebraClass.subtype S`: the canonical *inclusion* homomorphism from `S` into `B`, which is the right inverse to codomain restriction rather than codomain restriction itself.