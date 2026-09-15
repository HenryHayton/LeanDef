## Object

`VTask.map` constructs the tensor product of two algebra homomorphisms. Given an `S`-algebra map `f : A →ₐ[S] C` and an `R`-algebra map `g : B →ₐ[R] D`, it produces an `S`-algebra homomorphism `A ⊗[R] B →ₐ[S] C ⊗[R] D` that sends a pure tensor `a ⊗ b` to `f(a) ⊗ g(b)` and extends linearly to all of the tensor product.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {R : Type uR} -> {S : Type uS} -> {A : Type uA} -> {B : Type uB} -> {C : Type uC} -> {D : Type uD} -> [CommSemiring R] -> [CommSemiring S] -> [Algebra R S] -> [Semiring A] -> [Algebra R A] -> [Algebra S A] -> [IsScalarTower R S A] -> [Semiring B] -> [Algebra R B] -> [Semiring C] -> [Algebra R C] -> [Algebra S C] -> [IsScalarTower R S C] -> [Semiring D] -> [Algebra R D] -> (f : A →ₐ[S] C) -> (g : B →ₐ[R] D) -> TensorProduct R A B →ₐ[S] TensorProduct R C D
<!-- PINNED-SIGNATURE:END -->


`VTask.map : {R : Type uR} -> {S : Type uS} -> {A : Type uA} -> {B : Type uB} -> {C : Type uC} -> {D : Type uD} -> [CommSemiring R] -> [CommSemiring S] -> [Algebra R S] -> [Semiring A] -> [Algebra R A] -> [Algebra S A] -> [IsScalarTower R S A] -> [Semiring B] -> [Algebra R B] -> [Semiring C] -> [Algebra R C] -> [Algebra S C] -> [IsScalarTower R S C] -> [Semiring D] -> [Algebra R D] -> (f : A →ₐ[S] C) -> (g : B →ₐ[R] D) -> TensorProduct R A B →ₐ[S] TensorProduct R C D`

The implicit type arguments `R`, `S`, `A`, `B`, `C`, `D` are the underlying ring and algebra types. `R` is the base commutative semiring over which the tensor products are formed; `S` is a commutative semiring that is also an `R`-algebra, serving as the scalar ring for the `S`-algebra structures on `A` and `C`. The typeclass assumptions ensure that `A` and `C` are `R`-algebras and `S`-algebras compatibly (scalar tower `R → S → A` and `R → S → C`), that `B` is an `R`-algebra, and that `D` is an `R`-algebra.

The first explicit argument `f : A →ₐ[S] C` is an `S`-algebra homomorphism from `A` to `C`.

The second explicit argument `g : B →ₐ[R] D` is an `R`-algebra homomorphism from `B` to `D`.

The result is the induced `S`-algebra homomorphism from the tensor product `A ⊗[R] B` to `C ⊗[R] D`.

## Conventions

There are no special junk-value or edge-case conventions declared for this definition: it is a total function on its explicit inputs and the output is fully determined by functoriality of the tensor product construction.

## Worked examples

- Claim: When `f` is the identity on `A` and `g` is the identity on `B`, `VTask.map f g` acts as the identity on `A ⊗[R] B`; that is, for any pure tensor `a ⊗ b`, the result is `a ⊗ b`.

- Claim: For composable pairs `f₁ : A →ₐ[S] C`, `f₂ : C →ₐ[S] E` and `g₁ : B →ₐ[R] D`, `g₂ : D →ₐ[R] F`, the composition `VTask.map (f₂.comp f₁) (g₂.comp g₁)` equals `(VTask.map f₂ g₂).comp (VTask.map f₁ g₁)` as algebra homomorphisms (functoriality in both arguments).

- Claim: On a pure tensor `a ⊗ₜ b` in `A ⊗[R] B`, the homomorphism `VTask.map f g` evaluates to `f a ⊗ₜ g b` in `C ⊗[R] D`.

## Boundaries

- When `f` is the identity `S`-algebra map on `A` and `g` is the identity `R`-algebra map on `B`, `VTask.map f g` is the identity `S`-algebra homomorphism on `A ⊗[R] B`.
- The map respects multiplication: it sends `(a₁ ⊗ b₁) * (a₂ ⊗ b₂)` to `(f a₁ * f a₂) ⊗ (g b₁ * g b₂)`, consistent with the algebra structure on tensor products.
- The map sends the unit `1 ⊗ 1` in `A ⊗[R] B` to `1 ⊗ 1` in `C ⊗[R] D`, since algebra homomorphisms preserve units.
- The `S`-linearity of `f` and the `R`-linearity of `g` are exactly what is needed to make the result well-defined as an `S`-algebra map on the tensor product; relaxing either condition would break the construction.

## Not to be confused with

- `TensorProduct.map` (the linear-map version): that construction operates on plain `R`-linear maps and produces an `R`-linear map between tensor products, without the algebra-homomorphism or `S`-module structure.
- `AlgebraTensorModule.map`: the underlying linear-map level construction used internally; it lacks the multiplicative (algebra homomorphism) conclusion that `VTask.map` provides.
- `AlgHom.comp`: composition of two algebra homomorphisms in sequence, rather than their tensor product side-by-side.