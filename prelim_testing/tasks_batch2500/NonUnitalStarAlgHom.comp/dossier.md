## Object

`VTask.comp` constructs the composition of two non-unital ⋆-algebra homomorphisms as a new non-unital ⋆-algebra homomorphism. Given morphisms `f : B →⋆ₙₐ[R] C` and `g : A →⋆ₙₐ[R] B`, it produces the composite map `f ∘ g : A →⋆ₙₐ[R] C`, verifying that this composite preserves the R-module scalar action, the non-unital ring (additive and multiplicative) structure, and the star (involution) operation.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {R : Type u_1} -> {A : Type u_2} -> {B : Type u_3} -> {C : Type u_4} -> [Monoid R] -> [NonUnitalNonAssocSemiring A] -> [DistribMulAction R A] -> [Star A] -> [NonUnitalNonAssocSemiring B] -> [DistribMulAction R B] -> [Star B] -> [NonUnitalNonAssocSemiring C] -> [DistribMulAction R C] -> [Star C] -> (f : B →⋆ₙₐ[R] C) -> (g : A →⋆ₙₐ[R] B) -> A →⋆ₙₐ[R] C
<!-- PINNED-SIGNATURE:END -->


The implicit type arguments `R`, `A`, `B`, `C` are the scalar semiring and the three non-unital ⋆-algebras involved; their required algebraic structures (monoid on `R`; non-unital non-associative semiring, distributing scalar action, and star on each of `A`, `B`, `C`) are provided as typeclass instances. The explicit argument `f` is the outer morphism from `B` to `C`; `g` is the inner morphism from `A` to `B`. The output is the composite non-unital ⋆-algebra homomorphism from `A` to `C`.

## Conventions

No junk-value or edge-case conventions are declared for this definition: it is a total construction on bundled morphisms and every valid pair of composable non-unital ⋆-algebra homomorphisms yields a well-formed result.

## Worked examples

- Claim: For any non-unital ⋆-algebra `A` over `R` and identity-like homomorphism `id_A` and any `f : A →⋆ₙₐ[R] B`, the underlying function of `VTask.comp f id_A` equals `f ∘ id_A` pointwise.

- Claim: Composition is associative: for composable morphisms `f`, `g`, `h`, applying `VTask.comp (VTask.comp f g) h` and `VTask.comp f (VTask.comp g h)` to any element `a` gives the same result.

- Claim: For `f : B →⋆ₙₐ[R] C` and `g : A →⋆ₙₐ[R] B`, the composite `VTask.comp f g` applied to `a * b` equals `f (g (a * b))`, which equals `f (g a) * f (g b)` since both `g` and `f` preserve multiplication.

## Boundaries

- The definition is total: it applies to any pair of composable non-unital ⋆-algebra homomorphisms with matching intermediate algebra.
- There is no requirement that `A`, `B`, or `C` be unital; the construction works in the purely non-unital setting.
- There is no associativity or commutativity requirement on the underlying rings; `NonUnitalNonAssocSemiring` suffices.
- The star operation on each algebra is not required to be involutive or to satisfy any additional axiom beyond what the `Star` typeclass provides; preservation of star is nonetheless verified for the composite.

## Not to be confused with

- The composition of plain non-unital algebra homomorphisms (without star), which does not require or preserve the star involution.
- The composition of unital ⋆-algebra homomorphisms (`A →⋆ₐ[R] B`), which additionally requires unitality and preserves the multiplicative identity.
- Function composition `Function.comp`, which is a bare function-level operation and carries none of the algebraic homomorphism structure or bundled proofs.