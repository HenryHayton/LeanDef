## Object

`VTask.codRestrict` takes a non-unital star algebra homomorphism `f : A → B` (given in the form of a morphism class `F`) whose image is known to land inside a non-unital star subalgebra `S` of `B`, and produces a new non-unital star algebra homomorphism from `A` into `S` itself (as a type). In other words, it restricts the codomain of `f` from all of `B` to the subtype `↥S`, packaging the membership proof into the morphism's type.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.codRestrict : {F : Type v'} -> {R : Type u} -> {A : Type v} -> {B : Type w} -> [CommSemiring R] -> [NonUnitalNonAssocSemiring A] -> [Module R A] -> [Star A] -> [NonUnitalNonAssocSemiring B] -> [Module R B] -> [Star B] -> [FunLike F A B] -> [NonUnitalAlgHomClass F R A B] -> [StarHomClass F A B] -> (f : F) -> (S : NonUnitalStarSubalgebra R B) -> (hf : ∀ (x : A), f x ∈ S) -> A →⋆ₙₐ[R] ↥S
<!-- PINNED-SIGNATURE:END -->


`VTask.codRestrict : {F : Type v'} -> {R : Type u} -> {A : Type v} -> {B : Type w} -> [CommSemiring R] -> [NonUnitalNonAssocSemiring A] -> [Module R A] -> [Star A] -> [NonUnitalNonAssocSemiring B] -> [Module R B] -> [Star B] -> [FunLike F A B] -> [NonUnitalAlgHomClass F R A B] -> [StarHomClass F A B] -> (f : F) -> (S : NonUnitalStarSubalgebra R B) -> (hf : ∀ (x : A), f x ∈ S) -> A →⋆ₙₐ[R] ↥S`

The type parameters `R`, `A`, `B` are, respectively, the scalar semiring, the domain non-unital star algebra, and the ambient codomain non-unital star algebra. The class parameter `F` is the type of the concrete morphism being restricted, which must be simultaneously a non-unital algebra homomorphism and a star homomorphism. The explicit argument `f` is the morphism whose codomain is to be restricted. The argument `S` is the non-unital star subalgebra of `B` to which we wish to restrict. The argument `hf` is the proof that every element of `A` maps under `f` into `S`, which is the key hypothesis ensuring the restriction is well-defined.

## Conventions

No junk-value or edge-case conventions are declared: the definition is total and well-defined whenever the hypothesis `hf` is supplied, and there are no boundary inputs that require special treatment.

## Worked examples

- Claim: For any `f : A →⋆ₙₐ[R] B` and subalgebra `S` with `hf : ∀ x, f x ∈ S`, the underlying element `↑(VTask.codRestrict f S hf x)` equals `f x` for every `x : A`.

- Claim: The composition of the canonical inclusion `NonUnitalStarSubalgebraClass.subtype S` with `VTask.codRestrict f S hf` equals `f` as a morphism `A →⋆ₙₐ[R] B`.

- Claim: `VTask.codRestrict f S hf` is injective if and only if `f` itself is injective.

## Boundaries

- The definition requires `hf : ∀ x, f x ∈ S`; without this proof there is no way to form the restricted morphism, since elements of `↥S` carry a membership witness in their type.
- When `S` is all of `B` (i.e., `S = ⊤`), `VTask.codRestrict f ⊤ (fun x => mem_top)` produces a morphism into `↥⊤`, which is isomorphic to `B` but not definitionally equal to `f`.
- The coercion `↑(VTask.codRestrict f S hf x) = f x` holds definitionally, so the restricted morphism and the original agree on all values once the subtype coercion is applied.
- Injectivity is preserved and reflected: `VTask.codRestrict f S hf` is injective exactly when `f` is injective, since the coercion to `B` is injective.

## Not to be confused with

- `NonUnitalStarAlgHom.restrict` (domain restriction): restricts the *domain* of a star algebra homomorphism to a sub-object, rather than the codomain.
- `NonUnitalAlgHom.codRestrict`: the analogous codomain restriction for non-unital algebra homomorphisms that do *not* carry a star structure; this version does not ensure compatibility with the star operation.
- `StarAlgHom.codRestrict`: the unital analogue, which works with unital star algebra homomorphisms and unital star subalgebras, requiring a unit-preserving condition.