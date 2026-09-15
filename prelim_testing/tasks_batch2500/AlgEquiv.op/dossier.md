## Object

`VTask.op` is a canonical equivalence (a bijection with explicit inverse) between the type of algebra isomorphisms from `A` to `B` over a commutative semiring `R`, and the type of algebra isomorphisms from the opposite algebra `Aᵐᵒᵖ` to the opposite algebra `Bᵐᵒᵖ` over the same base ring `R`. Concretely, it says that an algebra iso between two algebras exists if and only if the same is true for their opposites, and the correspondence is natural and involutive. This is the action of the opposite-algebra functor on isomorphisms in the category of `R`-algebras.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.op : {R : Type u_1} -> {A : Type u_3} -> {B : Type u_4} -> [CommSemiring R] -> [Semiring A] -> [Semiring B] -> [Algebra R A] -> [Algebra R B] -> (A ≃ₐ[R] B) ≃ Aᵐᵒᵖ ≃ₐ[R] Bᵐᵒᵖ
<!-- PINNED-SIGNATURE:END -->


VTask.op : {R : Type u_1} -> {A : Type u_3} -> {B : Type u_4} -> [CommSemiring R] -> [Semiring A] -> [Semiring B] -> [Algebra R A] -> [Algebra R B] -> (A ≃ₐ[R] B) ≃ Aᵐᵒᵖ ≃ₐ[R] Bᵐᵒᵖ

`R` is the commutative base semiring over which both algebras are defined. `A` and `B` are the source and target `R`-algebras, each equipped with a semiring structure and an `R`-algebra structure. The `CommSemiring`, `Semiring`, and `Algebra` arguments are the requisite typeclass instances. The output is a type-level equivalence (with an explicit inverse) between the set of `R`-algebra isomorphisms `A ≃ₐ[R] B` and the set of `R`-algebra isomorphisms `Aᵐᵒᵖ ≃ₐ[R] Bᵐᵒᵖ`.

## Conventions

No special junk-value or boundary conventions are declared for this definition: `VTask.op` is a total construction on a globally defined type of equivalences, and every input produces a valid output with no degenerate cases.

## Worked examples

- Claim: For the identity algebra isomorphism `AlgEquiv.refl : A ≃ₐ[R] A`, applying `VTask.op` forward yields a map whose underlying function sends `MulOpposite.op a` to `MulOpposite.op a` for all `a`.

- Claim: `VTask.op` is an equivalence, meaning its forward and inverse functions are mutual inverses: for any `f : A ≃ₐ[R] B`, applying `VTask.op.toFun` then `VTask.op.invFun` recovers `f`.

- Claim: For any `f : A ≃ₐ[R] B`, the algebra isomorphism `VTask.op f` commutes with the `R`-algebra structure on the opposite algebras, i.e., it is genuinely an `R`-algebra map `Aᵐᵒᵖ →ₐ[R] Bᵐᵒᵖ`.

- Claim: `VTask.op` applied to a composite of two algebra isos corresponds to composing their opposite-algebra counterparts in the same order (functoriality).

## Boundaries

- The construction is defined for semirings (not necessarily rings), so it applies in the broadest standard algebraic setting without requiring additive inverses.
- When `A = B`, `VTask.op` restricts to an equivalence on the automorphism group `A ≃ₐ[R] A`, sending automorphisms to automorphisms of `Aᵐᵒᵖ`.
- The equivalence is involutive in the sense that applying the opposite construction twice (passing to `Aᵐᵒᵖᵐᵒᵖ`) recovers the original iso up to the canonical identification `Aᵐᵒᵖᵐᵒᵖ ≅ A`.
- There is no restriction on commutativity of `A` or `B`; the construction is meaningful and non-trivial precisely when the algebras are non-commutative.

## Not to be confused with

- `RingEquiv.op`: The analogous construction for plain ring isomorphisms, without the algebra (base-ring scalar) structure — `VTask.op` additionally preserves and uses the `R`-algebra homomorphism condition.
- `MulOpposite.opEquiv`: The canonical set-level equivalence `A ≃ Aᵐᵒᵖ` given by `op`/`unop`; this is not an algebra isomorphism between `A` and `Aᵐᵒᵖ` but merely a type equivalence.
- The forgetful map from `A ≃ₐ[R] B` to `A ≃ B`: passing to the underlying equivalence of types, which discards all algebraic structure and is unrelated to the opposite construction.