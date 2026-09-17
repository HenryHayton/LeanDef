## Object

`VTask.prod f g` is the **diagonal product** of two non-unital `R`-algebra homomorphisms `f : A →ₙₐ[R] B` and `g : A →ₙₐ[R] C` sharing the same domain `A`. It is the unique non-unital `R`-algebra homomorphism `A →ₙₐ[R] B × C` whose composition with the projection onto `B` recovers `f`, and whose composition with the projection onto `C` recovers `g`. Concretely, it sends each element `a : A` to the pair `(f a, g a)` in the product `B × C`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prod : {R : Type u} -> [Monoid R] -> {A : Type v} -> {B : Type w} -> {C : Type w₁} -> [NonUnitalNonAssocSemiring A] -> [DistribMulAction R A] -> [NonUnitalNonAssocSemiring B] -> [NonUnitalNonAssocSemiring C] -> [DistribMulAction R B] -> [DistribMulAction R C] -> (f : A →ₙₐ[R] B) -> (g : A →ₙₐ[R] C) -> A →ₙₐ[R] B × C
<!-- PINNED-SIGNATURE:END -->


`VTask.prod : {R : Type u} -> [Monoid R] -> {A : Type v} -> {B : Type w} -> {C : Type w₁} -> [NonUnitalNonAssocSemiring A] -> [DistribMulAction R A] -> [NonUnitalNonAssocSemiring B] -> [NonUnitalNonAssocSemiring C] -> [DistribMulAction R B] -> [DistribMulAction R C] -> (f : A →ₙₐ[R] B) -> (g : A →ₙₐ[R] C) -> A →ₙₐ[R] B × C`

The scalar ring `R` (with a `Monoid` structure) controls the `R`-action present throughout. `A` is the common source non-unital, non-associative semiring on which the action of `R` is a `DistribMulAction`. `B` and `C` are the two target non-unital, non-associative semirings, each also carrying a compatible `DistribMulAction` of `R`. The argument `f` is the first component morphism, landing in `B`; the argument `g` is the second component morphism, landing in `C`. The result is a morphism from `A` into the product semiring `B × C`.

## Conventions

No special junk-value or edge conventions are declared: the construction is total and well-defined for all valid inputs.

## Worked examples

- Claim: For the zero non-unital algebra homomorphism `0 : A →ₙₐ[R] B` and `0 : A →ₙₐ[R] C`, `VTask.prod 0 0` evaluated at any element `a` yields `(0, 0)`.

- Claim: If `f : A →ₙₐ[R] B` and `g : A →ₙₐ[R] C`, then applying `VTask.prod f g` to an element `a : A` gives `(f a, g a)` in `B × C`.

- Claim: If `f₁, f₂ : A →ₙₐ[R] B` and `g₁, g₂ : A →ₙₐ[R] C`, then `VTask.prod (f₁ + f₂) (g₁ + g₂) = VTask.prod f₁ g₁ + VTask.prod f₂ g₂` (where addition of morphisms is pointwise), reflecting that the pairing is bilinear over the pointwise structure on hom-sets.

## Boundaries

- When `B = C` and `f = g`, `VTask.prod f f` is the diagonal morphism `a ↦ (f a, f a)`; it is not in general the same as the identity unless `B = A` and `f` is the identity.
- When `A` is the zero ring (or the only element is `0`), the resulting morphism sends every element to `(0, 0)`, which is consistent with `map_zero`.
- The construction produces a morphism into the **product** `B × C`, not into a direct sum or tensor product; the ring structure on `B × C` is componentwise.
- There is no requirement that the individual morphisms `f` or `g` be injective, surjective, or unital; the result enjoys the same non-unital, non-associative level of generality.

## Not to be confused with

- `NonUnitalAlgHom.fst` / `NonUnitalAlgHom.snd`: these are the canonical projection morphisms `B × C →ₙₐ[R] B` and `B × C →ₙₐ[R] C`, going in the opposite direction from `VTask.prod`.
- `NonUnitalAlgHom.coprod`: the coproduct (co-pairing) construction for morphisms out of a coproduct (direct sum), rather than into a product.
- `Prod.map` on functions: a function-level operation pairing two maps with *different* domains, while `VTask.prod` requires both morphisms to share the **same** domain `A`.