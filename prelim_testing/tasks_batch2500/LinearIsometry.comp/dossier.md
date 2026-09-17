## Object

`VTask.comp g f` is the composite of two semilinear isometries: given a semilinear isometry `f : E →ₛₗᵢ[σ₁₂] E₂` and a semilinear isometry `g : E₂ →ₛₗᵢ[σ₂₃] E₃`, their composition is the semilinear isometry `E →ₛₗᵢ[σ₁₃] E₃` that first applies `f` and then applies `g`. The result is simultaneously a semilinear map (linear over the composite ring homomorphism `σ₁₃ = σ₂₃ ∘ σ₁₂`) and an isometry (it preserves norms exactly).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {R : Type u_1} -> {R₂ : Type u_2} -> {R₃ : Type u_3} -> {E : Type u_5} -> {E₂ : Type u_6} -> {E₃ : Type u_7} -> [Semiring R] -> [Semiring R₂] -> [Semiring R₃] -> {σ₁₂ : R →+* R₂} -> {σ₁₃ : R →+* R₃} -> {σ₂₃ : R₂ →+* R₃} -> [RingHomCompTriple σ₁₂ σ₂₃ σ₁₃] -> [SeminormedAddCommGroup E] -> [SeminormedAddCommGroup E₂] -> [SeminormedAddCommGroup E₃] -> [Module R E] -> [Module R₂ E₂] -> [Module R₃ E₃] -> (g : E₂ →ₛₗᵢ[σ₂₃] E₃) -> (f : E →ₛₗᵢ[σ₁₂] E₂) -> E →ₛₗᵢ[σ₁₃] E₃
<!-- PINNED-SIGNATURE:END -->


The implicit universe-polymorphic type arguments `R`, `R₂`, `R₃` are the scalar semirings for the three spaces, each equipped with a `Semiring` instance. The implicit types `E`, `E₂`, `E₃` are the underlying normed vector spaces, each carrying a `SeminormedAddCommGroup` instance and a compatible `Module` structure. The ring homomorphisms `σ₁₂ : R →+* R₂`, `σ₂₃ : R₂ →+* R₃`, and `σ₁₃ : R →+* R₃` are the scalar-action transition maps, and the `RingHomCompTriple` instance asserts that `σ₁₃ = σ₂₃ ∘ σ₁₂`, making composition well-typed. The explicit argument `g` is the outer semilinear isometry applied second (from `E₂` to `E₃`), and `f` is the inner semilinear isometry applied first (from `E` to `E₂`).

## Conventions

No junk-value or degenerate-input conventions are declared: the operation is total and well-defined for all valid pairs of composable semilinear isometries; there are no edge inputs that produce a conventionally-specified junk output.

## Worked examples

- Claim: For any semilinear isometry `f : E →ₛₗᵢ[σ₁₂] E₂`, composing with `g` and then applying to a vector `x` yields `g (f x)`.

- Claim: If `f` and `g` are both norm-preserving (‖f x‖ = ‖x‖ and ‖g y‖ = ‖y‖), then `VTask.comp g f` also satisfies ‖(VTask.comp g f) x‖ = ‖x‖ for all `x`.

- Claim: Composing a semilinear isometry with itself (when domain and codomain and ring homomorphism coincide and `σ` is an endomorphism satisfying the triple condition) yields a semilinear isometry whose underlying linear map is the square of the original.

## Boundaries

- The `RingHomCompTriple σ₁₂ σ₂₃ σ₁₃` typeclass constraint is essential: the composed map is only a valid `σ₁₃`-semilinear map if `σ₁₃` equals the composite `σ₂₃ ∘ σ₁₂` in the appropriate sense. Without this, the composition cannot be formed.
- When all three semirings coincide and all ring homomorphisms are the identity, this reduces to the familiar composition of linear isometries between normed spaces.
- The seminorm condition is preserved exactly (not merely up to a constant): ‖(VTask.comp g f) x‖ = ‖x‖ for all `x`, not just asymptotically.
- The composition of two semilinear isometries is again a semilinear isometry, not merely a bounded or continuous linear map.

## Not to be confused with

- `LinearMap.comp`: Composition of plain linear maps without any norm-preservation requirement; the result is merely linear, not isometric.
- `ContinuousLinearMap.comp`: Composition of continuous (bounded) linear maps; these preserve boundedness but not necessarily norms exactly.
- `LinearIsometryEquiv.trans`: Composition of invertible linear isometries (linear isometric equivalences), which additionally requires both maps to be bijective and furnishes an inverse.