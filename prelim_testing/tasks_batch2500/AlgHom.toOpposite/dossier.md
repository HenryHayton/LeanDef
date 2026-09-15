## Object

Given an `R`-algebra homomorphism `f : A →ₐ[R] B` whose image is commutative (in the sense that `f x` and `f y` commute for every pair of elements `x, y ∈ A`), `VTask.toOpposite` produces a new `R`-algebra homomorphism `A →ₐ[R] Bᵐᵒᵖ`, where `Bᵐᵒᵖ` is the opposite algebra of `B`. The key point is that the commutativity hypothesis makes it possible to view the same underlying map as a homomorphism into the opposite ring, since in `Bᵐᵒᵖ` multiplication is reversed and commutativity of the image makes the reversal transparent.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toOpposite : {R : Type u_1} -> {A : Type u_3} -> {B : Type u_4} -> [CommSemiring R] -> [Semiring A] -> [Semiring B] -> [Algebra R A] -> [Algebra R B] -> (f : A →ₐ[R] B) -> (hf : ∀ (x y : A), Commute (f x) (f y)) -> A →ₐ[R] Bᵐᵒᵖ
<!-- PINNED-SIGNATURE:END -->


`VTask.toOpposite : {R : Type u_1} -> {A : Type u_3} -> {B : Type u_4} -> [CommSemiring R] -> [Semiring A] -> [Semiring B] -> [Algebra R A] -> [Algebra R B] -> (f : A →ₐ[R] B) -> (hf : ∀ (x y : A), Commute (f x) (f y)) -> A →ₐ[R] Bᵐᵒᵖ`

The scalar base ring `R` is a commutative semiring. `A` and `B` are semirings equipped with `R`-algebra structures. The argument `f` is the source `R`-algebra homomorphism from `A` to `B`. The argument `hf` is the commutativity witness: a proof that for every `x, y : A`, the elements `f x` and `f y` commute in `B` (i.e., `f x * f y = f y * f x`). The output is an `R`-algebra homomorphism from `A` to the opposite algebra `Bᵐᵒᵖ`.

## Conventions

The underlying function of the resulting homomorphism is the composition of `f` with the canonical embedding `op : B → Bᵐᵒᵖ`; no new map data is introduced beyond the original `f`.

## Worked examples

- Claim: For any commutative `R`-algebra `B` and any algebra homomorphism `f : A →ₐ[R] B`, the commutativity condition `∀ x y, Commute (f x) (f y)` is automatically satisfied, and `VTask.toOpposite f hf` exists as an `R`-algebra homomorphism `A →ₐ[R] Bᵐᵒᵖ`.

- Claim: The underlying ring homomorphism of `VTask.toOpposite f hf` coincides with the ring-homomorphism-level `toOpposite` applied to `f`'s underlying ring homomorphism: `(VTask.toOpposite f hf : A →+* Bᵐᵒᵖ) = (f : A →+* B).toOpposite hf`.

- Claim: The underlying linear map of `VTask.toOpposite f hf` equals the composition of the canonical `R`-linear equivalence `opLinearEquiv R : B ≃ₗ[R] Bᵐᵒᵖ` with the linear map of `f`: `(VTask.toOpposite f hf).toLinearMap = (opLinearEquiv R) ∘ₗ f.toLinearMap`.

## Boundaries

- The commutativity hypothesis `hf` is essential: without it the naïve assignment `op ∘ f` would not respect the reversed multiplication in `Bᵐᵒᵖ`. When `B` is commutative every algebra map satisfies the hypothesis trivially.
- When `A = B` and `f` is the identity, `hf` amounts to requiring that `B` is commutative in order to use this construction.
- The construction is valid for semirings (no additive-inverse/negation requirement), matching the generality of the underlying `Semiring` and `CommSemiring` classes.

## Not to be confused with

- `RingHom.toOpposite`: the analogous construction at the level of ring homomorphisms alone, without the `R`-algebra scalar-action compatibility.
- `AlgEquiv.toOpposite` or similar: an algebra *isomorphism* to the opposite; `VTask.toOpposite` produces only a homomorphism, not an equivalence.
- The identity map on `Bᵐᵒᵖ`: `op : B → Bᵐᵒᵖ` is just a type-level re-labelling and is not itself an algebra homomorphism in the same sense (it reverses multiplication).