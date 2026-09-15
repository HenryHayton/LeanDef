## Object

`VTask.comp f g` is the composition of two ⋆-algebra homomorphisms, producing a new ⋆-algebra homomorphism. Given a ⋆-algebra homomorphism `g : A →⋆ₐ[R] B` and another `f : B →⋆ₐ[R] C`, their composition is the map that first applies `g` and then applies `f`, yielding a ⋆-algebra homomorphism `A →⋆ₐ[R] C`. This composition respects all the structure: it is `R`-linear, multiplicative, unital, and compatible with the star involution.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {R : Type u_2} -> {A : Type u_3} -> {B : Type u_4} -> {C : Type u_5} -> [CommSemiring R] -> [Semiring A] -> [Algebra R A] -> [Star A] -> [Semiring B] -> [Algebra R B] -> [Star B] -> [Semiring C] -> [Algebra R C] -> [Star C] -> (f : B →⋆ₐ[R] C) -> (g : A →⋆ₐ[R] B) -> A →⋆ₐ[R] C
<!-- PINNED-SIGNATURE:END -->


The implicit type arguments `R`, `A`, `B`, `C` are the scalar commutative semiring and the three ⋆-algebras over `R`. The typeclass arguments supply the semiring, algebra, and star structures on `A`, `B`, and `C`. The first explicit argument `f` is the outer ⋆-algebra homomorphism (from `B` to `C`); the second explicit argument `g` is the inner ⋆-algebra homomorphism (from `A` to `B`). The result is the composite ⋆-algebra homomorphism from `A` to `C` sending each element `a` to `f(g(a))`.

## Conventions

No special junk-value or edge conventions are declared for this definition: it is a total construction that is well-defined for all valid inputs, with no boundary regime requiring a conventional choice.

## Worked examples

- Claim: `VTask.comp id g = g` for any ⋆-algebra homomorphism `g : A →⋆ₐ[R] B`, where `id` is the identity ⋆-algebra homomorphism on `B`.

- Claim: `VTask.comp f id = f` for any ⋆-algebra homomorphism `f : B →⋆ₐ[R] C`, where `id` is the identity ⋆-algebra homomorphism on `B`.

- Claim: Composing three ⋆-algebra homomorphisms is associative: `VTask.comp (VTask.comp h f) g = VTask.comp h (VTask.comp f g)` for compatible `h`, `f`, `g`.

- Claim: For ⋆-algebra homomorphisms `f : B →⋆ₐ[R] C` and `g : A →⋆ₐ[R] B`, the underlying function of `VTask.comp f g` is the function composition of the underlying functions of `f` and `g`, i.e., `(VTask.comp f g) a = f (g a)` for all `a : A`.

## Boundaries

- When either `f` or `g` is the identity ⋆-algebra homomorphism, the composition reduces to the other map.
- When `A = B = C` and both morphisms are the zero map (in a context where that is a ⋆-algebra homomorphism), the composition is again the zero map.
- The construction is well-defined even when the algebras are trivial (zero rings), producing the unique homomorphism in that case.
- There is no partial definition or undefined case: the composition of any two composable ⋆-algebra homomorphisms is always a valid ⋆-algebra homomorphism.

## Not to be confused with

- `AlgHom.comp`: composition of plain algebra homomorphisms (without the star structure), which does not require or preserve the star involution.
- `StarHom.comp`: composition of star homomorphisms on a single algebraic structure without the algebra (R-linear) structure.
- Function composition `Function.comp`: operates on bare functions and carries none of the algebra or star-algebra homomorphism structure.