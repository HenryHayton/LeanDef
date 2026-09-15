## Object

Given a right-acting semiring `S` whose scalar multiplication on `M` commutes with that of `R`, `VTask.toModuleEnd R M` is the canonical ring homomorphism that sends each element `s : S` to the `R`-linear endomorphism of `M` defined by left multiplication by `s` (i.e., the map `m ↦ s • m`). In other words, it packages the `S`-module structure on `M` into a ring homomorphism from `S` into the endomorphism ring `End_R(M)` of `R`-linear maps `M →ₗ[R] M`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toModuleEnd : (R : Type u_1) -> {S : Type u_3} -> (M : Type u_4) -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> [Semiring S] -> [Module S M] -> [SMulCommClass S R M] -> S →+* Module.End R M
<!-- PINNED-SIGNATURE:END -->


`VTask.toModuleEnd : (R : Type u_1) -> {S : Type u_3} -> (M : Type u_4) -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> [Semiring S] -> [Module S M] -> [SMulCommClass S R M] -> S →+* Module.End R M`

`R` is the base semiring for which we are measuring `R`-linearity; it determines what it means for an endomorphism to be `R`-linear. `S` is the semiring whose elements act on `M` and whose ring structure is being mapped into endomorphisms. `M` is the module on which both `R` and `S` act, serving as the domain and codomain of every endomorphism in the target. The remaining arguments are typeclass witnesses: `Semiring R` and `Semiring S` equip the two types with ring structure; `AddCommMonoid M` and `Module R M` give `M` its additive and `R`-module structures; `Module S M` gives `M` its `S`-module structure; and `SMulCommClass S R M` asserts that the `S`- and `R`-actions on `M` commute, which is exactly what is needed for `s • –` to be `R`-linear.

## Conventions

There are no junk-value or edge conventions to declare: the map is a total ring homomorphism defined on all of `S`, with the zero element of `S` mapping to the zero endomorphism and addition and multiplication in `S` respected by construction.

## Worked examples

- Claim: For any commutative ring `R` viewed as an `R`-module over itself, `VTask.toModuleEnd R R` is the map sending each `r : R` to the endomorphism `m ↦ r • m = r * m`.

- Claim: Applying `VTask.toModuleEnd R M` to the zero element of `S` yields the zero `R`-linear endomorphism of `M` (since `0 • m = 0` for all `m`).

- Claim: Applying `VTask.toModuleEnd R M` to a sum `s + t` equals the pointwise sum of the endomorphisms for `s` and `t` separately, because the map is a ring homomorphism and in particular additive.

- Claim: Applying `VTask.toModuleEnd R M` to a product `s * t` equals the composition of the endomorphism for `s` with the endomorphism for `t`, reflecting multiplicativity of the ring homomorphism.

## Boundaries

- When `S = R` and `M = R` (the free rank-one module), the map `VTask.toModuleEnd R R` recovers scalar multiplication as endomorphisms, and if `R` is commutative it is injective (the endomorphism ring captures all of `R`).
- The `SMulCommClass S R M` hypothesis is essential: without it the map `m ↦ s • m` would not be `R`-linear and the construction would not type-check.
- The map is a ring homomorphism, so it always preserves `1`: the identity element `1 : S` maps to the identity endomorphism `id_M` (since `1 • m = m`).
- The map is not assumed to be injective in general; faithfulness depends on additional hypotheses about the module.

## Not to be confused with

- `DistribMulAction.toModuleEnd`: a strictly weaker version that only yields a monoid homomorphism into `End R M`, not a full ring homomorphism; `VTask.toModuleEnd` extends it by also tracking the additive/ring structure of `S`.
- `LinearMap.toAddMonoidHom`: the forgetful map from an individual `R`-linear map to an additive group homomorphism; this is about a single endomorphism, not a ring homomorphism from `S`.
- `Algebra.toLinearMap`: in the algebra setting, the map sending an algebra element to left multiplication; closely related but requires `R`-algebra structure on `S` rather than just a commuting `S`-module structure.