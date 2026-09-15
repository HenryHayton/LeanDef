## Object

This constructor produces a bialgebra isomorphism (a bialgebra equivalence) `A ≃ₐc[R] B` from a pair of bialgebra homomorphisms that are mutually inverse. A *bialgebra isomorphism* over a commutative semiring `R` is a bijective `R`-linear map between two `R`-bialgebras that simultaneously preserves the algebra structure (multiplication and unit) and the coalgebra structure (comultiplication and counit), with the inverse map also preserving both structures. `VTask.ofBialgHom` packages this data into the isomorphism type, relieving the user from having to supply the full equivalence structure directly.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofBialgHom : {R : Type u} -> {A : Type v} -> {B : Type w} -> [CommSemiring R] -> [Semiring A] -> [Semiring B] -> [Algebra R A] -> [Algebra R B] -> [CoalgebraStruct R A] -> [CoalgebraStruct R B] -> (f : A →ₐc[R] B) -> (g : B →ₐc[R] A) -> (h₁ : f.comp g = BialgHom.id R B) -> (h₂ : g.comp f = BialgHom.id R A) -> A ≃ₐc[R] B
<!-- PINNED-SIGNATURE:END -->


VTask.ofBialgHom : {R : Type u} -> {A : Type v} -> {B : Type w} -> [CommSemiring R] -> [Semiring A] -> [Semiring B] -> [Algebra R A] -> [Algebra R B] -> [CoalgebraStruct R A] -> [CoalgebraStruct R B] -> (f : A →ₐc[R] B) -> (g : B →ₐc[R] A) -> (h₁ : f.comp g = BialgHom.id R B) -> (h₂ : g.comp f = BialgHom.id R A) -> A ≃ₐc[R] B

`R` is the base commutative semiring over which the bialgebras are defined. `A` and `B` are the source and target bialgebra types, respectively, equipped with semiring, algebra, and coalgebra structures via the instance arguments. `f` is the forward bialgebra homomorphism from `A` to `B`. `g` is the proposed inverse, a bialgebra homomorphism from `B` back to `A`. `h₁` is the proof that composing `f` after `g` yields the identity on `B` (i.e., `g` is a right inverse of `f`). `h₂` is the proof that composing `g` after `f` yields the identity on `A` (i.e., `g` is a left inverse of `f`).

## Conventions

There are no junk-value or default-output conventions to record: the constructor is only defined when all four explicit arguments are supplied, and the result is fully determined by them without any case-splitting on degenerate inputs.

## Worked examples

- Claim: The underlying function of `VTask.ofBialgHom f g h₁ h₂` equals `f` as a bialgebra homomorphism — that is, coercing the resulting isomorphism to a morphism recovers `f`.

- Claim: The inverse of `VTask.ofBialgHom f g h₁ h₂` is `VTask.ofBialgHom g f h₂ h₁` — swapping the roles of `f` and `g` (and exchanging the two inverse proofs) yields the symmetric isomorphism.

- Claim: For any bialgebra `A` over `R`, applying `VTask.ofBialgHom` to `BialgHom.id R A`, `BialgHom.id R A`, and the two trivial identity proofs produces a bialgebra isomorphism `A ≃ₐc[R] A` whose forward map is the identity.

## Boundaries

- Both `h₁` and `h₂` must be supplied; neither alone suffices. An injective-but-not-surjective (or surjective-but-not-injective) bialgebra map cannot be fed to this constructor without the matching one-sided inverse.
- When `A = B` and `f = g = BialgHom.id R A`, the two conditions `h₁` and `h₂` are the same proof obligation, and the result is the identity bialgebra isomorphism.
- The constructor does not check compatibility of `R`, `A`, `B` beyond what the type system enforces; if the instance arguments are satisfied, the constructor applies unconditionally.
- The result's coercion to a function is definitionally equal to `f`, and its inverse's coercion is definitionally equal to `g`.

## Not to be confused with

- `BialgHom` (`A →ₐc[R] B`): a bialgebra *homomorphism* (not necessarily invertible); `VTask.ofBialgHom` lifts a pair of mutually inverse homomorphisms into the stronger isomorphism type.
- `AlgEquiv.ofAlgHom`: the analogous constructor for algebra isomorphisms, which ignores the coalgebra structure entirely.
- `CoalgEquiv.ofCoalgHom` (if it exists): the analogous constructor for coalgebra isomorphisms, which ignores the algebra structure; `VTask.ofBialgHom` requires both structures to be preserved simultaneously.