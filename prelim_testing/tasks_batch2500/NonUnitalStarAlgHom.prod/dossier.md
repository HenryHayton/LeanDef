## VTask.prod

### Object

Given two non-unital star algebra homomorphisms `f : A →⋆ₙₐ[R] B` and `g : A →⋆ₙₐ[R] C` sharing the same domain `A`, this construction produces a single non-unital star algebra homomorphism `A →⋆ₙₐ[R] B × C` whose action on any element `a : A` is the pair `(f a, g a)`. In other words, it is the canonical pairing (product) of two morphisms into the product type, equipped with all the required homomorphism structure.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prod : {R : Type u_1} -> {A : Type u_2} -> {B : Type u_3} -> {C : Type u_4} -> [Monoid R] -> [NonUnitalNonAssocSemiring A] -> [DistribMulAction R A] -> [Star A] -> [NonUnitalNonAssocSemiring B] -> [DistribMulAction R B] -> [Star B] -> [NonUnitalNonAssocSemiring C] -> [DistribMulAction R C] -> [Star C] -> (f : A →⋆ₙₐ[R] B) -> (g : A →⋆ₙₐ[R] C) -> A →⋆ₙₐ[R] B × C
<!-- PINNED-SIGNATURE:END -->


The implicit type arguments `R`, `A`, `B`, `C` are the scalar semiring and the three non-unital star algebras involved, with their associated typeclass instances (monoid, semiring, distributing scalar action, and star operation). The argument `f` is the first component morphism, mapping from `A` to `B`; the argument `g` is the second component morphism, mapping from `A` to `C`.

### Conventions

No junk-value or edge conventions are declared for this construction: it is a total function on well-typed inputs and every output is a fully valid non-unital star algebra homomorphism.

### Worked Examples

- Claim: For any `a : A`, applying `VTask.prod f g` to `a` yields `(f a, g a)`.

- Claim: `VTask.prod f g` respects the star operation, i.e., `(VTask.prod f g) (star a) = star ((VTask.prod f g) a)` for all `a`.

- Claim: The first projection recovers `f`, meaning `(VTask.prod f g).toFun a` has first component equal to `f a` for all `a`.

- Claim: The second projection recovers `g`, meaning `(VTask.prod f g).toFun a` has second component equal to `g a` for all `a`.

### Boundaries

- When `B` and `C` are the same type, `VTask.prod f g` still produces a morphism into `B × B`; there is no degenerate collapse.
- If `f = g`, the result is the diagonal morphism sending each `a` to `(f a, f a)`.
- The construction does not require `B` or `C` to be unital, associative, or commutative; any non-unital star `R`-algebra suffices.
- The product type `B × C` is automatically equipped with componentwise star and semiring structure, so no additional hypotheses are needed beyond those already present.

### Not to be confused with

- The product *type* or *algebra* `B × C` itself, which is the codomain here but not the same as this morphism-pairing construction.
- `NonUnitalStarAlgHom.comp`, which composes two morphisms in sequence rather than pairing them side by side.
- The unital analogue `StarAlgHom.prod`, which requires unital algebra structure on all objects involved.