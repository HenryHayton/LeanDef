## Object

`VTask.symm` constructs the **inverse** of a linear isometry equivalence. Given a semilinear isometric isomorphism `e : E ≃ₛₗᵢ[σ₁₂] E₂` (a bijective linear map between seminormed modules that preserves norms, twisted by a ring homomorphism `σ₁₂`), it produces the inverse map `E₂ ≃ₛₗᵢ[σ₂₁] E`, which is again a linear isometry equivalence twisted by the companion ring homomorphism `σ₂₁` (the compositional inverse of `σ₁₂`).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.symm : {R : Type u_1} -> {R₂ : Type u_2} -> {E : Type u_5} -> {E₂ : Type u_6} -> [Semiring R] -> [Semiring R₂] -> {σ₁₂ : R →+* R₂} -> {σ₂₁ : R₂ →+* R} -> [RingHomInvPair σ₁₂ σ₂₁] -> [RingHomInvPair σ₂₁ σ₁₂] -> [SeminormedAddCommGroup E] -> [SeminormedAddCommGroup E₂] -> [Module R E] -> [Module R₂ E₂] -> (e : E ≃ₛₗᵢ[σ₁₂] E₂) -> E₂ ≃ₛₗᵢ[σ₂₁] E
<!-- PINNED-SIGNATURE:END -->


VTask.symm : {R : Type u_1} -> {R₂ : Type u_2} -> {E : Type u_5} -> {E₂ : Type u_6} -> [Semiring R] -> [Semiring R₂] -> {σ₁₂ : R →+* R₂} -> {σ₂₁ : R₂ →+* R} -> [RingHomInvPair σ₁₂ σ₂₁] -> [RingHomInvPair σ₂₁ σ₁₂] -> [SeminormedAddCommGroup E] -> [SeminormedAddCommGroup E₂] -> [Module R E] -> [Module R₂ E₂] -> (e : E ≃ₛₗᵢ[σ₁₂] E₂) -> E₂ ≃ₛₗᵢ[σ₂₁] E

`R` and `R₂` are the scalar semirings acting on the source and target modules respectively. `E` and `E₂` are the source and target seminormed additive commutative groups, each carrying a module structure over their respective rings. `σ₁₂ : R →+* R₂` is the ring homomorphism twisting the original equivalence, and `σ₂₁ : R₂ →+* R` is its compositional inverse (witnessed by the two `RingHomInvPair` instances, which assert that `σ₂₁ ∘ σ₁₂ = id` and `σ₁₂ ∘ σ₂₁ = id`). The final explicit argument `e` is the linear isometry equivalence whose inverse is to be constructed.

## Conventions

No special junk-value or boundary conventions are declared for this construction: it is a total operation on a well-typed input and every instance of `VTask.symm e` produces a fully valid `LinearIsometryEquiv` in the reverse direction.

## Worked examples

- Claim: For any linear isometry equivalence `e : E ≃ₛₗᵢ[σ₁₂] E₂`, the norm of `VTask.symm e` applied to any vector `y : E₂` equals the norm of `y` (the inverse is also an isometry).

- Claim: For any linear isometry equivalence `e : E ≃ₛₗᵢ[σ₁₂] E₂` and any `x : E`, applying `VTask.symm e` to `e x` returns `x` (left inverse property).

- Claim: For any linear isometry equivalence `e : E ≃ₛₗᵢ[σ₁₂] E₂` and any `y : E₂`, applying `e` to `VTask.symm e y` returns `y` (right inverse property).

- Claim: `VTask.symm (VTask.symm e) = e` for any linear isometry equivalence `e` (the operation is an involution).

## Boundaries

- When `E = E₂` and `σ₁₂ = σ₂₁ = id` (the non-twisted, self-map case), `VTask.symm` still produces the group-theoretic inverse in the automorphism group of linear isometries.
- When `e` is already the identity equivalence, `VTask.symm e` is also the identity equivalence.
- The construction is well-defined for seminormed (not necessarily normed) spaces; in particular, it does not require the norm to be non-degenerate.
- The pair of `RingHomInvPair` instances is essential: without knowing that `σ₁₂` and `σ₂₁` are mutual inverses, the inverse map would not be semilinear with respect to any ring homomorphism.

## Not to be confused with

- `LinearEquiv.symm`: the inverse of a plain linear equivalence, with no norm-preservation requirement or isometry structure bundled.
- `LinearIsometry.symm` (when it exists on an isometric embedding that happens to be surjective): a related but distinct operation that does not bundle the full equivalence data from both sides simultaneously.
- `Isometry.symm` or `IsometryEquiv.symm`: the inverse in the purely metric (non-linear) setting, unaware of the module or ring-homomorphism structure.