## Object

Given two composable continuous semilinear maps — one from a topological module `M₁` to `M₂` (with ring homomorphism `σ₁₂ : R₁ →+* R₂`) and one from `M₂` to `M₃` (with ring homomorphism `σ₂₃ : R₂ →+* R₃`) — `VTask.comp g f` produces their composite, a continuous semilinear map from `M₁` to `M₃` with the composed ring homomorphism `σ₁₃ : R₁ →+* R₃`. The composite map sends each element `x : M₁` to `g(f(x))`, and the result carries both the semilinear-map structure (compatibility with ring scalars) and the continuity guarantee inherited from `f` and `g`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {R₁ : Type u_1} -> {R₂ : Type u_2} -> {R₃ : Type u_3} -> [Semiring R₁] -> [Semiring R₂] -> [Semiring R₃] -> {σ₁₂ : R₁ →+* R₂} -> {σ₂₃ : R₂ →+* R₃} -> {σ₁₃ : R₁ →+* R₃} -> {M₁ : Type u_4} -> [TopologicalSpace M₁] -> [AddCommMonoid M₁] -> {M₂ : Type u_6} -> [TopologicalSpace M₂] -> [AddCommMonoid M₂] -> {M₃ : Type u_7} -> [TopologicalSpace M₃] -> [AddCommMonoid M₃] -> [Module R₁ M₁] -> [Module R₂ M₂] -> [Module R₃ M₃] -> [RingHomCompTriple σ₁₂ σ₂₃ σ₁₃] -> (g : M₂ →SL[σ₂₃] M₃) -> (f : M₁ →SL[σ₁₂] M₂) -> M₁ →SL[σ₁₃] M₃
<!-- PINNED-SIGNATURE:END -->


The implicit type arguments `R₁`, `R₂`, `R₃` are the three scalar semirings, equipped with their respective `Semiring` instances. The implicit maps `σ₁₂`, `σ₂₃`, `σ₁₃` are the ring homomorphisms between the scalars, with `σ₁₃` required to equal the composition `σ₂₃ ∘ σ₁₂` (enforced by the `RingHomCompTriple` instance). The implicit types `M₁`, `M₂`, `M₃` are the three topological modules, each equipped with a `TopologicalSpace`, an `AddCommMonoid`, and the appropriate `Module` instance. The explicit argument `g : M₂ →SL[σ₂₃] M₃` is the outer (post-composition) continuous semilinear map, and `f : M₁ →SL[σ₁₂] M₂` is the inner (pre-composition) continuous semilinear map. The result is the composed continuous semilinear map `M₁ →SL[σ₁₃] M₃`.

## Conventions

The arguments are in "function-application order": `g` is listed before `f`, matching mathematical notation `g ∘ f`, so the map applied first is the second explicit argument. When the ring homomorphisms are all identity maps (i.e., the maps are continuous linear maps over the same ring), the composition reduces to ordinary composition of continuous linear maps.

## Worked examples

- Claim: For continuous linear maps `f g : ℝ →L[ℝ] ℝ`, the composition `VTask.comp g f` applied to a point `x` equals `g (f x)`.

- Claim: Composing any continuous linear map `f : M₁ →SL[σ₁₂] M₂` with the identity continuous linear map on `M₂` on the left yields a map that agrees pointwise with `f`.

- Claim: Composition is associative: for composable continuous semilinear maps `h`, `g`, `f`, `VTask.comp (VTask.comp h g) f` and `VTask.comp h (VTask.comp g f)` agree pointwise.

## Boundaries

The `RingHomCompTriple σ₁₂ σ₂₃ σ₁₃` instance is a typeclass witness that `σ₁₃ = σ₂₃ ∘ σ₁₂`; Lean finds this automatically in standard cases (e.g., all homomorphisms are identity maps, or they form a recognized triple). If the ring homomorphisms do not compose correctly, the instance will not be found and the definition cannot be applied. Continuity of the composition is guaranteed whenever both `f` and `g` are continuous, which is always the case since the inputs are required to be `ContinuousSemilinearMap`s. There are no junk values; every valid pair of composable inputs yields a valid continuous semilinear map.

## Not to be confused with

- The underlying semilinear map composition (without continuity): this only composes the algebraic maps and does not carry a continuity proof.
- Scalar multiplication by a ring homomorphism applied to a single map: that changes scalars but does not combine two maps.
- Function composition `Function.comp`: that operates on bare functions with no linear or continuity structure.