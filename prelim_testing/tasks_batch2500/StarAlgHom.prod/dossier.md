## Object

Given two star algebra homomorphisms `f : A →⋆ₐ[R] B` and `g : A →⋆ₐ[R] C` sharing the same domain `A`, `VTask.prod f g` is the unique star algebra homomorphism from `A` into the product algebra `B × C` whose composition with the first projection gives `f` and whose composition with the second projection gives `g`. In other words, it is the canonical pairing map `a ↦ (f a, g a)`, packaged as a morphism in the category of star `R`-algebras.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prod : {R : Type u_1} -> {A : Type u_2} -> {B : Type u_3} -> {C : Type u_4} -> [CommSemiring R] -> [Semiring A] -> [Algebra R A] -> [Star A] -> [Semiring B] -> [Algebra R B] -> [Star B] -> [Semiring C] -> [Algebra R C] -> [Star C] -> (f : A →⋆ₐ[R] B) -> (g : A →⋆ₐ[R] C) -> A →⋆ₐ[R] B × C
<!-- PINNED-SIGNATURE:END -->


VTask.prod : {R : Type u_1} -> {A : Type u_2} -> {B : Type u_3} -> {C : Type u_4} -> [CommSemiring R] -> [Semiring A] -> [Algebra R A] -> [Star A] -> [Semiring B] -> [Algebra R B] -> [Star B] -> [Semiring C] -> [Algebra R C] -> [Star C] -> (f : A →⋆ₐ[R] B) -> (g : A →⋆ₐ[R] C) -> A →⋆ₐ[R] B × C

The implicit type arguments `R`, `A`, `B`, `C` are the scalar ring and the three algebra types involved. The instance arguments supply the commutative semiring structure on the scalars, semiring and `R`-algebra structures on each of the three algebras, and star operations on each. The explicit argument `f` is the star algebra homomorphism from `A` into the first factor `B`; the explicit argument `g` is the star algebra homomorphism from `A` into the second factor `C`.

## Conventions

No junk-value or boundary conventions are declared: the function is total on all star algebra homomorphisms without restriction.

## Worked examples

- Claim: For any two star algebra homomorphisms `f : A →⋆ₐ[R] B` and `g : A →⋆ₐ[R] C`, the value of `VTask.prod f g` at any element `a : A` is `(f a, g a)`.

- Claim: If `f` and `g` are both the identity star algebra homomorphism on a star `R`-algebra `A` (with `B = C = A`), then `VTask.prod f g` maps every `a : A` to `(a, a)`, the diagonal embedding into `A × A`.

- Claim: The composite of `VTask.prod f g` with the projection `StarAlgHom.fst` (the star algebra homomorphism `B × C →⋆ₐ[R] B` given by the first projection) equals `f`.

- Claim: The composite of `VTask.prod f g` with the projection `StarAlgHom.snd` (the star algebra homomorphism `B × C →⋆ₐ[R] C` given by the second projection) equals `g`.

## Boundaries

- The definition is total: it applies to any pair of star algebra homomorphisms `f`, `g` with the same domain `A` and the same scalar ring `R`, regardless of any additional structure on `B` or `C`.
- The product algebra `B × C` is equipped with the componentwise ring, algebra, and star structures, so the result is a valid star algebra homomorphism exactly because `f` and `g` individually are.
- No special behavior arises when `f = g`: in that case `VTask.prod f f` is the diagonal map `a ↦ (f a, f a)`, not the identity.
- No special behavior arises when `B` or `C` is a trivial (zero) algebra; the construction still produces a valid morphism into the appropriate product.

## Not to be confused with

- `AlgHom.prod`: the analogous pairing construction for plain algebra homomorphisms (without the star-algebra structure), which does not track compatibility with the star operation.
- `StarAlgHom.fst` / `StarAlgHom.snd`: the projection morphisms from a product star algebra onto its factors; these go in the *opposite* direction and are components of a product rather than the pairing.
- `StarAlgHom.prod_map`: a related construction that takes morphisms `f : A →⋆ₐ[R] B` and `g : C →⋆ₐ[R] D` on *different* domains and produces a morphism `A × C →⋆ₐ[R] B × D`, rather than pairing two morphisms from the *same* domain.