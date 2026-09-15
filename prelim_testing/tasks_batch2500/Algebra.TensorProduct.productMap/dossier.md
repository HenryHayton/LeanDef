## Object

Given two `R`-algebra homomorphisms `f : A →ₐ[R] S` and `g : B →ₐ[R] S` with `S` a *commutative* `R`-algebra, `VTask.productMap f g` is the unique `R`-algebra homomorphism from the tensor product `A ⊗[R] B` to `S` that sends a pure tensor `a ⊗ b` to the product `f(a) · g(b)` in `S`. Commutativity of `S` is essential: it ensures that the images of `f` and `g` commute with each other, which is the algebraic prerequisite for the assignment `a ⊗ b ↦ f(a) · g(b)` to extend to a well-defined ring homomorphism on the whole tensor product.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.productMap : {R : Type uR} -> {S : Type uS} -> {A : Type uA} -> {B : Type uB} -> [CommSemiring R] -> [Semiring A] -> [Semiring B] -> [CommSemiring S] -> [Algebra R A] -> [Algebra R B] -> [Algebra R S] -> (f : A →ₐ[R] S) -> (g : B →ₐ[R] S) -> TensorProduct R A B →ₐ[R] S
<!-- PINNED-SIGNATURE:END -->


VTask.productMap : {R : Type uR} -> {S : Type uS} -> {A : Type uA} -> {B : Type uB} -> [CommSemiring R] -> [Semiring A] -> [Semiring B] -> [CommSemiring S] -> [Algebra R A] -> [Algebra R B] -> [Algebra R S] -> (f : A →ₐ[R] S) -> (g : B →ₐ[R] S) -> TensorProduct R A B →ₐ[R] S

`R` is the common base commutative semiring over which all algebras are defined. `A` and `B` are the two `R`-algebras whose tensor product is the domain. `S` is the target commutative `R`-algebra (commutativity here is the key hypothesis that makes the construction work). The argument `f` is an `R`-algebra homomorphism from `A` into `S`, and `g` is an `R`-algebra homomorphism from `B` into `S`. The result is an `R`-algebra homomorphism from `A ⊗[R] B` to `S`.

## Conventions

There are no junk-value or edge-case conventions to declare for this definition: it is a total construction whose inputs are all algebraically well-typed, and no degenerate inputs produce silently discarded or sentinel output.

## Worked examples

- Claim: On a pure tensor `a ⊗ b`, `VTask.productMap f g` evaluates to `f a * g b`.

- Claim: `VTask.productMap f g` composed with the canonical left inclusion `includeLeft : A →ₐ[R] A ⊗[R] B` (sending `a ↦ a ⊗ 1`) recovers `f`; that is, for any `a : A`, `VTask.productMap f g (a ⊗ₜ 1) = f a`.

- Claim: `VTask.productMap f g` composed with the canonical right inclusion `includeRight : B →ₐ[R] A ⊗[R] B` (sending `b ↦ 1 ⊗ b`) recovers `g`; that is, for any `b : B`, `VTask.productMap f g (1 ⊗ₜ b) = g b`.

- Claim: The range (image) of `VTask.productMap f g` as a subalgebra of `S` equals the join (in the lattice of subalgebras) of the range of `f` and the range of `g`.

## Boundaries

- When `A` or `B` is the zero ring (or the `R`-algebra with one element), the tensor product collapses accordingly, and `VTask.productMap` is the unique algebra map out of that trivial tensor product.
- When `f = g` and `A = B`, the map still lands in `S` via `a ⊗ b ↦ f(a) · f(b)`, which is not the same as `f` applied to `a · b` in general (the domain is a tensor product, not `A` itself).
- The commutativity of `S` is a hard requirement: if `S` were merely a semiring, images of `f` and `g` might not commute, and the assignment `a ⊗ b ↦ f(a) · g(b)` would fail to be multiplicative on the tensor product.
- The map is uniquely determined on all of `A ⊗[R] B` by its values on pure tensors, because pure tensors generate the tensor product as an `R`-module.

## Not to be confused with

- `Algebra.TensorProduct.productLeftAlgHom`: the more general version allowing the two base rings to differ; `VTask.productMap` is the special case where both sides share the same base ring `R`.
- `TensorProduct.map f g` (the map `A ⊗[R] B →ₗ[R] S ⊗[R] S` applying `f` and `g` component-wise): that lands in `S ⊗[R] S`, not in `S` itself, and is not an algebra map to `S`.
- `Algebra.TensorProduct.lmul' R`: the multiplication map `S ⊗[R] S →ₐ[R] S`; `VTask.productMap f g` factors as `lmul' R` after `TensorProduct.map f g`, but it is not itself that multiplication map.