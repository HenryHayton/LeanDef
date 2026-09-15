## Object

Given an algebra homomorphism `f : A →ₐ[R] B` whose image is commutative (in the sense that `f x` and `f y` commute for all `x, y : A`), `VTask.fromOpposite f hf` is the induced algebra homomorphism from the opposite algebra `Aᵐᵒᵖ` to `B`. It acts by first "unflipping" an element of `Aᵐᵒᵖ` to recover the underlying element of `A`, then applying `f`. The commutativity hypothesis is precisely what ensures multiplication in `Aᵐᵒᵖ` (which reverses factors) is respected: since `f(yx) = f(y)f(x)` must equal `f(x)f(y)` for the map to be multiplicative on `Aᵐᵒᵖ`, commutativity of the image is exactly the right condition.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.fromOpposite : {R : Type u_1} -> {A : Type u_3} -> {B : Type u_4} -> [CommSemiring R] -> [Semiring A] -> [Semiring B] -> [Algebra R A] -> [Algebra R B] -> (f : A →ₐ[R] B) -> (hf : ∀ (x y : A), Commute (f x) (f y)) -> Aᵐᵒᵖ →ₐ[R] B
<!-- PINNED-SIGNATURE:END -->


`VTask.fromOpposite : {R : Type u_1} -> {A : Type u_3} -> {B : Type u_4} -> [CommSemiring R] -> [Semiring A] -> [Semiring B] -> [Algebra R A] -> [Algebra R B] -> (f : A →ₐ[R] B) -> (hf : ∀ (x y : A), Commute (f x) (f y)) -> Aᵐᵒᵖ →ₐ[R] B`

The implicit type parameters are: `R` is the commutative base semiring over which all algebras are defined; `A` is the source algebra (whose opposite is used as the domain); `B` is the target algebra. The instance arguments supply the semiring and algebra structures on `R`, `A`, and `B`. The first explicit argument `f` is the original algebra homomorphism from `A` to `B`. The second explicit argument `hf` is a proof that the image of `f` is commutative, i.e., that `f x` and `f y` commute (as elements of `B`) for every pair `x, y : A`.

## Conventions

There are no declared junk-value or edge-case conventions for this definition: it is a total construction on well-typed inputs, and there are no degenerate inputs that force a fallback value.

## Worked examples

- Claim: For any `R`-algebra homomorphism `f : A →ₐ[R] B` with commuting image and any `a : A`, applying `VTask.fromOpposite f hf` to `MulOpposite.op a` yields `f a`.

- Claim: The underlying ring homomorphism of `VTask.fromOpposite f hf` coincides with the ring homomorphism from `Aᵐᵒᵖ` to `B` induced by `f`'s underlying ring homomorphism; concretely, `(VTask.fromOpposite f hf : Aᵐᵒᵖ →+* B) = (f : A →+* B).fromOpposite hf`.

- Claim: The underlying linear map of `VTask.fromOpposite f hf` equals `f`'s linear map composed with the canonical linear equivalence `Aᵐᵒᵖ ≃ₗ[R] A`; concretely, `(VTask.fromOpposite f hf).toLinearMap = f.toLinearMap ∘ₗ (opLinearEquiv R (M := A)).symm`.

## Boundaries

- When `B` is commutative, the hypothesis `hf` is trivially satisfied for any `f`, so every algebra map `A →ₐ[R] B` with commutative target lifts to a map out of `Aᵐᵒᵖ`.
- When `A` itself is commutative, `Aᵐᵒᵖ` is canonically isomorphic to `A`, and `VTask.fromOpposite f hf` essentially recovers `f` under this identification.
- The commutativity hypothesis `hf` concerns elements of `B` (the image), not of `A` itself; `A` need not be commutative.
- If `f` is the zero map (into the zero algebra or a trivial target), `hf` holds vacuously and the construction is well-defined.

## Not to be confused with

- `MulOpposite.opAlgEquiv`: the canonical algebra isomorphism `A ≃ₐ[R] Aᵐᵒᵖ` when `A` is commutative; `VTask.fromOpposite` goes the other direction and requires a commutativity hypothesis rather than assuming `A` is commutative.
- `RingHom.fromOpposite`: the analogous construction for plain ring homomorphisms (without the `R`-algebra scalar compatibility); `VTask.fromOpposite` additionally preserves the algebra (i.e., `R`-scalar) structure.
- An algebra homomorphism `Aᵐᵒᵖ →ₐ[R] Bᵐᵒᵖ` induced by `f`; that goes between opposite algebras, whereas `VTask.fromOpposite f hf` maps into `B` itself, not its opposite.