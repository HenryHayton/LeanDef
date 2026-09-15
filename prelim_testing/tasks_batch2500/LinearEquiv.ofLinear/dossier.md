## VTask.ofLinear

### Object

Given a semilinear map `f : M →ₛₗ[σ₁₂] M₂` and a semilinear map `g : M₂ →ₛₗ[σ₂₁] M` in the opposite direction, together with proofs that they compose to the respective identity maps, `VTask.ofLinear` packages these data into a single semilinear equivalence `M ≃ₛₗ[σ₁₂] M₂`. Informally, it certifies that a semilinear map is an isomorphism by providing its explicit inverse.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofLinear : {R : Type u_1} -> {R₂ : Type u_2} -> {M : Type u_5} -> {M₂ : Type u_7} -> [Semiring R] -> [Semiring R₂] -> [AddCommMonoid M] -> [AddCommMonoid M₂] -> {module_M : Module R M} -> {module_M₂ : Module R₂ M₂} -> {σ₁₂ : R →+* R₂} -> {σ₂₁ : R₂ →+* R} -> {re₁₂ : RingHomInvPair σ₁₂ σ₂₁} -> {re₂₁ : RingHomInvPair σ₂₁ σ₁₂} -> (f : M →ₛₗ[σ₁₂] M₂) -> (g : M₂ →ₛₗ[σ₂₁] M) -> (h₁ : f ∘ₛₗ g = LinearMap.id) -> (h₂ : g ∘ₛₗ f = LinearMap.id) -> M ≃ₛₗ[σ₁₂] M₂
<!-- PINNED-SIGNATURE:END -->


`VTask.ofLinear : {R : Type u_1} -> {R₂ : Type u_2} -> {M : Type u_5} -> {M₂ : Type u_7} -> [Semiring R] -> [Semiring R₂] -> [AddCommMonoid M] -> [AddCommMonoid M₂] -> {module_M : Module R M} -> {module_M₂ : Module R₂ M₂} -> {σ₁₂ : R →+* R₂} -> {σ₂₁ : R₂ →+* R} -> {re₁₂ : RingHomInvPair σ₁₂ σ₂₁} -> {re₂₁ : RingHomInvPair σ₂₁ σ₁₂} -> (f : M →ₛₗ[σ₁₂] M₂) -> (g : M₂ →ₛₗ[σ₂₁] M) -> (h₁ : f ∘ₛₗ g = LinearMap.id) -> (h₂ : g ∘ₛₗ f = LinearMap.id) -> M ≃ₛₗ[σ₁₂] M₂`

The implicit type arguments `R` and `R₂` are the two (semi)rings acting on the modules. The implicit types `M` and `M₂` are the source and target modules. The instance arguments provide the semiring and module structures. The implicit arguments `σ₁₂ : R →+* R₂` and `σ₂₁ : R₂ →+* R` are the ring homomorphisms relating the two scalings; `re₁₂` and `re₂₁` are the proofs that `σ₁₂` and `σ₂₁` are inverses of each other (the `RingHomInvPair` hypotheses). The explicit argument `f` is the forward semilinear map from `M` to `M₂`. The explicit argument `g` is the proposed inverse semilinear map from `M₂` back to `M`. The proof `h₁` asserts that `f` composed with `g` equals the identity on `M₂`. The proof `h₂` asserts that `g` composed with `f` equals the identity on `M`.

### Conventions

There are no junk-value or edge conventions to declare: the definition is total and every input is meaningful by hypothesis.

### Worked examples

- Claim: For the identity linear map `LinearMap.id` on a module `M`, applying `VTask.ofLinear LinearMap.id LinearMap.id rfl rfl` to any element `x` gives back `x`.

- Claim: The forward direction of the equivalence produced by `VTask.ofLinear f g h₁ h₂` acts exactly as `f`: for every `x : M`, `(VTask.ofLinear f g h₁ h₂) x = f x`.

- Claim: The inverse (`.symm`) of the equivalence produced by `VTask.ofLinear f g h₁ h₂` acts exactly as `g`: for every `y : M₂`, `(VTask.ofLinear f g h₁ h₂).symm y = g y`.

### Boundaries

- The definition is total: it requires explicit proof obligations (`h₁` and `h₂`), so there is no degenerate or junk case; the output is always a valid semilinear equivalence.
- The two proofs `h₁` and `h₂` play symmetric but distinct roles: `h₁` witnesses right-inversion (`f ∘ g = id`, so `g` is a right inverse of `f`) and `h₂` witnesses left-inversion (`g ∘ f = id`, so `g` is a left inverse of `f`). Both are needed to establish a genuine two-sided inverse.
- When both `σ₁₂` and `σ₂₁` are the identity ring homomorphism (i.e., `R = R₂` and both maps are `R`-linear), this specialises to the ordinary (non-semilinear) linear equivalence constructor.
- The coercion of the resulting equivalence back to a linear map recovers exactly `f`, and its `.symm` coercion recovers exactly `g`.

### Not to be confused with

- `LinearEquiv.symm`: the operation that reverses an *already-constructed* linear equivalence; `VTask.ofLinear` *constructs* the equivalence from scratch.
- `LinearMap.inverse`: a function that tries to build a set-theoretic inverse from a bijection hypothesis, without bundling it as a `LinearEquiv`.
- `Equiv.ofBijective`: constructs a plain (non-linear) equivalence from a bijection proof, with no linearity structure on the inverse.