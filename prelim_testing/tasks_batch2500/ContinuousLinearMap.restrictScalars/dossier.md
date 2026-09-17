## Object

Given a continuous `A`-linear map `f : M₁ →L[A] M₂` between two modules that each carry compatible `R`-module and `A`-module structures, `VTask.restrictScalars R f` reinterprets `f` as a continuous `R`-linear map `M₁ →L[R] M₂`. Conceptually, if `A` is an `R`-algebra (so every `R`-scalar action on a module is determined by the `A`-action), then a map that is linear over the larger ring `A` is automatically linear over the smaller ring `R`; this operation makes that reinterpretation explicit while retaining the continuity of the original map.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.restrictScalars : {A : Type u_1} -> {M₁ : Type u_2} -> {M₂ : Type u_3} -> (R : Type u_4) -> [Semiring A] -> [Semiring R] -> [AddCommMonoid M₁] -> [Module A M₁] -> [Module R M₁] -> [TopologicalSpace M₁] -> [AddCommMonoid M₂] -> [Module A M₂] -> [Module R M₂] -> [TopologicalSpace M₂] -> [LinearMap.CompatibleSMul M₁ M₂ R A] -> (f : M₁ →L[A] M₂) -> M₁ →L[R] M₂
<!-- PINNED-SIGNATURE:END -->


VTask.restrictScalars : {A : Type u_1} -> {M₁ : Type u_2} -> {M₂ : Type u_3} -> (R : Type u_4) -> [Semiring A] -> [Semiring R] -> [AddCommMonoid M₁] -> [Module A M₁] -> [Module R M₁] -> [TopologicalSpace M₁] -> [AddCommMonoid M₂] -> [Module A M₂] -> [Module R M₂] -> [TopologicalSpace M₂] -> [LinearMap.CompatibleSMul M₁ M₂ R A] -> (f : M₁ →L[A] M₂) -> M₁ →L[R] M₂

The explicit argument `R` is the scalar ring to which one is restricting; it is supplied explicitly because it cannot in general be inferred from the other data. The implicit types `A`, `M₁`, `M₂` are the algebra and the source/target modules, inferred from context. The instance arguments provide the semiring structures on `A` and `R`, the additive-commutative-monoid and module structures on `M₁` and `M₂` over both `A` and `R`, the topologies on `M₁` and `M₂`, and the `LinearMap.CompatibleSMul` compatibility condition asserting that the `R`-scalar action is subordinate to the `A`-scalar action in a way that lets `R`-linearity be deduced from `A`-linearity. The argument `f` is the continuous `A`-linear map to be reinterpreted.

## Conventions

The underlying set-function of `VTask.restrictScalars R f` is definitionally equal to the underlying set-function of `f`; no new function is constructed, only the linearity and continuity witnesses are repackaged.

## Worked examples

- Claim: For any continuous `ℂ`-linear map `f : E →L[ℂ] F` between complex Banach spaces (viewed also as real modules), `VTask.restrictScalars ℝ f` is a continuous `ℝ`-linear map with the same underlying function as `f`.

- Claim: For the identity continuous `A`-linear map `ContinuousLinearMap.id A M`, applying `VTask.restrictScalars R` yields the continuous `R`-linear map whose underlying function is still the identity on `M`.

- Claim: If `f : M₁ →L[A] M₂` and `g : M₂ →L[A] M₃` are two composable continuous `A`-linear maps with compatible `R`-module structures, then `VTask.restrictScalars R (g ∘L f)` has the same underlying function as `(VTask.restrictScalars R g) ∘L (VTask.restrictScalars R f)`.

## Boundaries

- When `R = A` (i.e., restricting scalars along the identity algebra map), the result is essentially the same map with the same scalar ring; the `CompatibleSMul` hypothesis becomes trivially satisfied.
- The definition is total: it requires no non-degeneracy conditions on the spaces or the map. In particular it applies even when `M₁` or `M₂` is the zero module.
- If `f` is the zero map, `VTask.restrictScalars R f` is also the zero map (as a continuous `R`-linear map).

## Not to be confused with

- `LinearMap.restrictScalars`: the analogous operation for purely algebraic (not necessarily continuous) linear maps; `VTask.restrictScalars` additionally carries along the continuity proof.
- `ContinuousLinearMap.extendScalars`: the dual operation that extends the scalar ring upward (e.g., from `ℝ` to `ℂ`), rather than restricting it downward.
- `ContinuousLinearMap.restrictDomain` or similar: operations that restrict the *domain module* rather than the *scalar ring*.