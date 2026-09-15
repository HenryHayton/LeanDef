## Object

Given two coalgebra morphisms `f : A →ₗc[R] B` and `g : B →ₗc[R] A` that are inverses of each other (in the sense that `f ∘ g = id` and `g ∘ f = id` as coalgebra maps), `VTask.ofCoalgHom` packages them together into a coalgebra isomorphism `A ≃ₗc[R] B`. In other words, it promotes a pair of mutually inverse coalgebra homomorphisms into a single invertible coalgebra equivalence.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofCoalgHom : {R : Type u_1} -> {A : Type u_2} -> {B : Type u_3} -> [CommSemiring R] -> [AddCommMonoid A] -> [AddCommMonoid B] -> [Module R A] -> [Module R B] -> [CoalgebraStruct R A] -> [CoalgebraStruct R B] -> (f : A →ₗc[R] B) -> (g : B →ₗc[R] A) -> (h₁ : f.comp g = CoalgHom.id R B) -> (h₂ : g.comp f = CoalgHom.id R A) -> A ≃ₗc[R] B
<!-- PINNED-SIGNATURE:END -->


`VTask.ofCoalgHom : {R : Type u_1} -> {A : Type u_2} -> {B : Type u_3} -> [CommSemiring R] -> [AddCommMonoid A] -> [AddCommMonoid B] -> [Module R A] -> [Module R B] -> [CoalgebraStruct R A] -> [CoalgebraStruct R B] -> (f : A →ₗc[R] B) -> (g : B →ₗc[R] A) -> (h₁ : f.comp g = CoalgHom.id R B) -> (h₂ : g.comp f = CoalgHom.id R A) -> A ≃ₗc[R] B`

The implicit type arguments `R`, `A`, and `B` are the coefficient semiring and the two coalgebra types being related. The typeclass arguments supply the commutative semiring structure on `R`, the additive commutative monoid and module structures on `A` and `B`, and the coalgebra structures on `A` and `B` over `R`. The argument `f` is the forward coalgebra homomorphism from `A` to `B`. The argument `g` is the proposed inverse, a coalgebra homomorphism from `B` back to `A`. The argument `h₁` is the proof that composing `f` after `g` yields the identity on `B`, i.e., `f ∘ g = id_B` as coalgebra maps. The argument `h₂` is the proof that composing `g` after `f` yields the identity on `A`, i.e., `g ∘ f = id_A` as coalgebra maps.

## Conventions

No junk-value or boundary conventions are declared: the constructor is a total function on well-typed inputs and every argument is a genuine mathematical datum (morphisms plus proofs of their being mutual inverses), so there are no degenerate or undefined input regimes to document.

## Worked examples

- Claim: The underlying forward map of `VTask.ofCoalgHom f g h₁ h₂` is equal to `f` as a coalgebra homomorphism.

- Claim: The inverse equivalence `(VTask.ofCoalgHom f g h₁ h₂).symm` equals `VTask.ofCoalgHom g f h₂ h₁`.

- Claim: For any coalgebra isomorphism `e : A ≃ₗc[R] B`, one can recover it via `VTask.ofCoalgHom` applied to `e` (viewed as a homomorphism) and its inverse, since the resulting equivalence has the same underlying map.

## Boundaries

- The construction requires *both* direction proofs: supplying only one of `h₁` or `h₂` does not suffice to build the isomorphism, even though bijectivity on the underlying sets would follow from either one alone in many classical settings.
- If `f` or `g` is the identity map on `A = B` and both `h₁` and `h₂` are proofs of `id ∘ id = id`, the result is simply the identity coalgebra equivalence on `A`.
- Because the construction is definitionally equal to `f` on the forward direction and to `g` on the reverse direction, no data is lost or gained relative to the original morphisms.

## Not to be confused with

- `CoalgHom` (`A →ₗc[R] B`): a coalgebra homomorphism without an inverse; `VTask.ofCoalgHom` upgrades a morphism-with-inverse pair into the stronger isomorphism type.
- `LinearEquiv.ofLinear`: the analogous constructor for linear equivalences ignoring the coalgebra (comultiplication/counit) structure; `VTask.ofCoalgHom` additionally requires and preserves the coalgebra structure.
- `CoalgEquiv.symm`: the operation that swaps the two directions of an *already-constructed* coalgebra isomorphism, rather than building one from scratch from two separate morphisms.