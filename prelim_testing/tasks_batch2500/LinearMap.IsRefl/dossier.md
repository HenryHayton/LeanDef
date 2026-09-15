## VTask.IsRefl

### Object

A sesquilinear map `B : M₁ →ₛₗ[I₁] M₁ →ₛₗ[I₂] M` is called **reflexive** if, whenever `B x y = 0`, it follows that `B y x = 0`. In other words, the vanishing of `B` at an ordered pair `(x, y)` is a symmetric condition: `B x y = 0` and `B y x = 0` always hold or fail together. This generalises the classical notion of reflexivity for bilinear or sesquilinear forms (such as symmetric, skew-symmetric, or Hermitian forms), which all satisfy this property.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsRefl : {R : Type u_1} -> {R₁ : Type u_2} -> {M : Type u_5} -> {M₁ : Type u_6} -> [CommSemiring R] -> [AddCommMonoid M] -> [Module R M] -> [CommSemiring R₁] -> [AddCommMonoid M₁] -> [Module R₁ M₁] -> {I₁ I₂ : R₁ →+* R} -> (B : M₁ →ₛₗ[I₁] M₁ →ₛₗ[I₂] M) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsRefl : {R : Type u_1} -> {R₁ : Type u_2} -> {M : Type u_5} -> {M₁ : Type u_6} -> [CommSemiring R] -> [AddCommMonoid M] -> [Module R M] -> [CommSemiring R₁] -> [AddCommMonoid M₁] -> [Module R₁ M₁] -> {I₁ I₂ : R₁ →+* R} -> (B : M₁ →ₛₗ[I₁] M₁ →ₛₗ[I₂] M) -> Prop`

`R` is the target scalar ring and `R₁` is the source scalar ring for the sesquilinear map; both are commutative semirings. `M` is the codomain module (over `R`) and `M₁` is the domain module (over `R₁`). `I₁` and `I₂` are the two ring homomorphisms `R₁ →+* R` that govern how scalars are twisted in each argument of the sesquilinear map. The principal argument `B` is the sesquilinear map whose reflexivity is being asserted.

### Conventions

There are no declared junk-value or edge-case conventions for this definition: `IsRefl` is a `Prop` defined by a universal quantifier over all elements of the module, and it carries no distinguished behaviour at degenerate inputs beyond the logical content of the universal statement itself.

### Worked examples

- Claim: The zero sesquilinear map (sending every pair to 0) is reflexive, because `B x y = 0` is always true and so is `B y x = 0`.

- Claim: For a symmetric bilinear form `B` over a commutative ring satisfying `B x y = B y x` for all `x y`, `IsRefl B` holds, since `B x y = 0` directly gives `B y x = B x y = 0`.

- Claim: If `B` is reflexive and nondegenerate (in the sense of `LinearMap.Nondegenerate`), then `B` has the separating-left property: for every nonzero `x`, there exists `y` such that `B x y ≠ 0`. This follows from the theorem `IsRefl.nondegenerate_iff_separatingLeft`.

- Claim: If `B` is reflexive and `W` is a submodule disjoint from its own orthogonal complement with respect to `B`, then the restriction of `B` to `W × W` is nondegenerate.

### Boundaries

- The zero map trivially satisfies reflexivity: `B x y = 0` is vacuously satisfied for all `x y`, and `B y x = 0` holds as well, so the universal implication is true.
- Reflexivity does not imply symmetry; a form can be reflexive without satisfying `B x y = B y x`. Alternating (skew-symmetric) forms, for which `B x x = 0` implies `B y x = -B x y`, are reflexive.
- The definition is stated for sesquilinear maps with potentially different ring homomorphisms `I₁` and `I₂` in the two arguments; in the bilinear case both are the identity.
- There is no constraint on the codomain `M` beyond being an `R`-module; in particular `M` need not be `R` itself.

### Not to be confused with

- `Module.IsReflexive`: reflexivity of a *module* (the natural map from a module to its double dual is an isomorphism), entirely unrelated to reflexivity of a bilinear form.
- `LinearMap.IsSymm`: a bilinear form is symmetric if `B x y = B y x` for all `x y`; this is strictly stronger than reflexivity.
- `LinearMap.IsAlt`: a bilinear form is alternating if `B x x = 0` for all `x`; this implies reflexivity (over fields of characteristic ≠ 2) but is a different condition.