## VTask.ofLinearIsometry

### Object

This construction promotes a linear isometry `f : E →ₛₗᵢ[σ₁₂] E₂` to a full linear isometric equivalence `E ≃ₛₗᵢ[σ₁₂] E₂`, given explicit evidence that a companion linear map `g : E₂ →ₛₗ[σ₂₁] E` is a two-sided inverse of `f`. In short: if a (semilinear) isometry has an inverse, the pair can be bundled into an isometric equivalence, with `f` serving as the forward direction and `g` as the backward direction.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofLinearIsometry : {R : Type u_1} -> {R₂ : Type u_2} -> {E : Type u_5} -> {E₂ : Type u_6} -> [Semiring R] -> [Semiring R₂] -> {σ₁₂ : R →+* R₂} -> {σ₂₁ : R₂ →+* R} -> [RingHomInvPair σ₁₂ σ₂₁] -> [RingHomInvPair σ₂₁ σ₁₂] -> [SeminormedAddCommGroup E] -> [SeminormedAddCommGroup E₂] -> [Module R E] -> [Module R₂ E₂] -> (f : E →ₛₗᵢ[σ₁₂] E₂) -> (g : E₂ →ₛₗ[σ₂₁] E) -> (h₁ : f.toLinearMap ∘ₛₗ g = LinearMap.id) -> (h₂ : g ∘ₛₗ f.toLinearMap = LinearMap.id) -> E ≃ₛₗᵢ[σ₁₂] E₂
<!-- PINNED-SIGNATURE:END -->


The implicit arguments fix the algebraic and metric structure: two semirings `R` and `R₂`, two seminormed additive commutative groups `E` and `E₂` carrying compatible module structures, and a pair of mutually inverse ring homomorphisms `σ₁₂ : R →+* R₂` and `σ₂₁ : R₂ →+* R` (the `RingHomInvPair` instances certify that each is a two-sided inverse of the other).

The four explicit arguments are:
- `f`: the semilinear isometry from `E` to `E₂` with respect to `σ₁₂`; this will be the underlying forward map of the resulting equivalence.
- `g`: a semilinear map from `E₂` back to `E` with respect to `σ₂₁`; this is the proposed inverse.
- `h₁`: a proof that composing `f` after `g` yields the identity on `E₂`, i.e., `f ∘ g = id`.
- `h₂`: a proof that composing `g` after `f` yields the identity on `E`, i.e., `g ∘ f = id`.

### Conventions

The coercion of the resulting equivalence to a plain function agrees exactly with the coercion of `f`; no additional data beyond `f` and `g` is stored in the norm component. The `.symm` of the resulting equivalence coerces to `g` as a plain function.

### Worked examples

- Claim: For the identity linear isometry `id : E →ₛₗᵢ[RingHom.id R] E` with inverse also being the identity linear map, `VTask.ofLinearIsometry` produces an equivalence whose forward coercion equals the identity function on `E`.

- Claim: If `f : E →ₛₗᵢ[σ₁₂] E₂` and `g : E₂ →ₛₗ[σ₂₁] E` satisfy `f ∘ g = id` and `g ∘ f = id`, then for any `x : E`, the norm of `(VTask.ofLinearIsometry f g h₁ h₂) x` equals the norm of `x`, since `f` is an isometry.

- Claim: The `.symm` of `VTask.ofLinearIsometry f g h₁ h₂`, when coerced to a function `E₂ → E`, equals `g` as a function.

### Boundaries

- The construction is total on its inputs: there are no restrictions on `f`, `g`, `h₁`, or `h₂` beyond their stated types and the typeclass assumptions. In particular, the semirings and modules may be trivial, the spaces may be zero-dimensional, or `E` and `E₂` may be equal.
- When `E` or `E₂` is the zero module, the only map is the zero map, and the proofs `h₁` and `h₂` are trivially satisfied; the construction still yields a valid equivalence.
- The two inverse conditions `h₁` and `h₂` must both be supplied; neither alone is sufficient (semilinear maps between modules over different rings do not generally satisfy a one-sided-inverse-implies-bijective argument).

### Not to be confused with

- `LinearIsometryEquiv.mk` / direct structure construction: builds an isometric equivalence from lower-level fields without requiring a companion inverse map to be passed explicitly.
- `LinearEquiv.ofLinear`: the pure algebraic analogue that produces a linear equivalence from a linear map and its inverse, but carries no norm/isometry data.
- A `LinearIsometry` (`E →ₛₗᵢ[σ₁₂] E₂`): a one-way isometric map with no built-in inverse; `VTask.ofLinearIsometry` is the bridge that upgrades it to a two-way equivalence once an inverse is known.