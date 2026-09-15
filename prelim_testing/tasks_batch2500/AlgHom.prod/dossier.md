## VTask.prod

### Object

Given two algebra homomorphisms `f : A →ₐ[R] B` and `g : A →ₐ[R] C` over a commutative semiring `R`, `VTask.prod f g` is the unique algebra homomorphism `A →ₐ[R] B × C` whose composition with the first projection `B × C → B` equals `f` and whose composition with the second projection `B × C → C` equals `g`. Concretely, it sends each element `a : A` to the pair `(f a, g a)` in the product `R`-algebra `B × C`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prod : {R : Type u_1} -> {A : Type u_2} -> {B : Type u_3} -> {C : Type u_4} -> [CommSemiring R] -> [Semiring A] -> [Algebra R A] -> [Semiring B] -> [Algebra R B] -> [Semiring C] -> [Algebra R C] -> (f : A →ₐ[R] B) -> (g : A →ₐ[R] C) -> A →ₐ[R] B × C
<!-- PINNED-SIGNATURE:END -->


`VTask.prod : {R : Type u_1} -> {A : Type u_2} -> {B : Type u_3} -> {C : Type u_4} -> [CommSemiring R] -> [Semiring A] -> [Algebra R A] -> [Semiring B] -> [Algebra R B] -> [Semiring C] -> [Algebra R C] -> (f : A →ₐ[R] B) -> (g : A →ₐ[R] C) -> A →ₐ[R] B × C`

The implicit type arguments `R`, `A`, `B`, `C` are the scalar base ring and the three algebra types involved. The instance arguments supply the required semiring and `R`-algebra structures on each type. The first explicit argument `f` is the algebra homomorphism from `A` to `B` that will be the first component of the product morphism; the second explicit argument `g` is the algebra homomorphism from `A` to `C` that will be the second component.

### Conventions

No junk-value or edge conventions are declared for this definition: it is a total construction over well-typed inputs, and there are no degenerate or boundary cases that assign a conventional default value.

### Worked examples

- Claim: For any element `a : A`, applying `VTask.prod f g` to `a` yields the pair `(f a, g a)` in `B × C`.
  (The result morphism sends `a` to `(f a, g a)` by definition of the product construction.)

- Claim: `VTask.prod f g` preserves the algebra map: for any scalar `r : R`, `(VTask.prod f g) (algebraMap R A r) = algebraMap R (B × C) r`. This follows because both `f` and `g` individually satisfy the `commutes` condition, and the algebra map on the product `B × C` is defined componentwise.

- Claim: When `f` is the identity algebra homomorphism `AlgHom.id R A` and `g` is also `AlgHom.id R A`, `VTask.prod (AlgHom.id R A) (AlgHom.id R A)` sends every `a : A` to `(a, a)` in `A × A`.

- Claim: `VTask.prod f g` composed with the first-component projection algebra homomorphism recovers `f`, and composed with the second-component projection recovers `g`.

### Boundaries

- If `B` or `C` is the zero ring (or a trivially structured semiring), the construction still applies; the product morphism simply maps everything to the unique element or the trivial image.
- The construction is fully symmetric in `B` and `C`: swapping the roles of `f` and `g` produces the composition of `VTask.prod g f` with the swap isomorphism `B × C ≅ C × B`.
- When `A` itself is a product algebra `A₁ × A₂`, the universal property of the product still applies component-by-component; there is nothing special about the source being a product.
- The `R`-algebra structure on `B × C` used by this construction is the standard componentwise one, so the `commutes` condition is verified componentwise.

### Not to be confused with

- `AlgHom.fst` / `AlgHom.snd`: these are the *projection* morphisms `B × C →ₐ[R] B` and `B × C →ₐ[R] C`, going in the opposite direction from `VTask.prod f g`.
- `RingHom.prod`: the analogous construction for plain ring homomorphisms, without the `R`-algebra (scalar compatibility) structure.
- `AlgHom.prodMap` (if it exists): a morphism `A × B →ₐ[R] C × D` built from two morphisms on *different* source algebras, as opposed to `VTask.prod` which fans out from a single source.
