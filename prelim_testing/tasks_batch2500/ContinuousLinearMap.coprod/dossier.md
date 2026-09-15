## Object

Given two continuous linear maps `f₁ : M₁ →L[R] M` and `f₂ : M₂ →L[R] M` into a common target module `M`, `VTask.coprod f₁ f₂` is the continuous linear map from the product module `M₁ × M₂` into `M` defined by sending a pair `(x, y)` to `f₁ x + f₂ y`. It is the canonical way to "merge" two continuous linear maps that share the same codomain by feeding them the two components of a product.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.coprod : {R : Type u_1} -> {M : Type u_3} -> {M₁ : Type u_5} -> {M₂ : Type u_6} -> [Semiring R] -> [TopologicalSpace M] -> [TopologicalSpace M₁] -> [TopologicalSpace M₂] -> [AddCommMonoid M] -> [Module R M] -> [ContinuousAdd M] -> [AddCommMonoid M₁] -> [Module R M₁] -> [AddCommMonoid M₂] -> [Module R M₂] -> (f₁ : M₁ →L[R] M) -> (f₂ : M₂ →L[R] M) -> M₁ × M₂ →L[R] M
<!-- PINNED-SIGNATURE:END -->


`VTask.coprod : {R : Type u_1} -> {M : Type u_3} -> {M₁ : Type u_5} -> {M₂ : Type u_6} -> [Semiring R] -> [TopologicalSpace M] -> [TopologicalSpace M₁] -> [TopologicalSpace M₂] -> [AddCommMonoid M] -> [Module R M] -> [ContinuousAdd M] -> [AddCommMonoid M₁] -> [Module R M₁] -> [AddCommMonoid M₂] -> [Module R M₂] -> (f₁ : M₁ →L[R] M) -> (f₂ : M₂ →L[R] M) -> M₁ × M₂ →L[R] M`

The scalar ring `R` is implicit and governs the module structure throughout. `M` is the shared codomain module, which must carry a topological space structure and continuous addition (so that the sum `f₁ x + f₂ y` is itself continuous). `M₁` and `M₂` are the two domain modules, each carrying their own topological space and `R`-module structure. The explicit argument `f₁` is the continuous `R`-linear map applied to the first component of the product pair; `f₂` is the continuous `R`-linear map applied to the second component. The result is the continuous `R`-linear map `(x, y) ↦ f₁ x + f₂ y` on the product `M₁ × M₂`.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total constructor that is well-defined for any two continuous linear maps with a common codomain satisfying the stated type-class assumptions.

## Worked examples

- Claim: When `f₁` and `f₂` are both the identity map on `ℝ` (viewed as a continuous linear map `ℝ →L[ℝ] ℝ`), the coprod sends `(3, 5)` to `8`.

- Claim: When `f₁` is the zero map `M₁ →L[R] M` and `f₂` is any continuous linear map `g : M₂ →L[R] M`, the coprod `VTask.coprod 0 g` sends `(x, y)` to `g y`, because the `f₁` contribution vanishes.

- Claim: The coprod of the two coordinate projections `ContinuousLinearMap.fst` and `ContinuousLinearMap.snd` recovers the identity on `M × M`, in the sense that it sends `(x, y)` to `x + y`.

## Boundaries

- If either `f₁` or `f₂` is the zero continuous linear map, the coprod simply evaluates to the other map applied to the remaining component: `VTask.coprod 0 f₂ (x, y) = f₂ y` and `VTask.coprod f₁ 0 (x, y) = f₁ x`.
- If both maps are zero, the coprod is the zero map on the product.
- The definition requires `ContinuousAdd M` on the codomain. Without this, the pointwise sum of two continuous maps need not be continuous, so the instance requirement is tight.
- The construction is bilinear in `f₁` and `f₂`: scaling or adding maps in either argument is reflected in the resulting coprod.

## Not to be confused with

- `ContinuousLinearMap.prod` — takes maps `f₁ : M →L[R] M₁` and `f₂ : M →L[R] M₂` with a *common domain* and produces a map into the product `M₁ × M₂`; the dual construction to coprod.
- `ContinuousLinearMap.comp` — sequential composition of two continuous linear maps rather than parallel combination with addition.
- `LinearMap.coprod` (the non-topological version) — the purely algebraic coprod of two linear maps, which does not carry or verify continuity.