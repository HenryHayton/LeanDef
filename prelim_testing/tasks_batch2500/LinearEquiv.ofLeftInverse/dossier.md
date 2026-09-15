## Object

Given a semilinear map `f : M →ₛₗ[σ₁₂] M₂` and a function `g : M₂ → M` that is a left inverse of `f` (i.e., `g(f(m)) = m` for all `m : M`), `VTask.ofLeftInverse h` is the **semilinear equivalence** between `M` and the range of `f` (as a submodule of `M₂`). The forward direction sends each `m : M` to `f(m)` (viewed as an element of `f.range`), and the inverse direction sends an element of `f.range` back to `M` via `g`.

The existence of a left inverse is equivalent to injectivity, so this construction witnesses the canonical isomorphism `M ≅ f(M)` in the semilinear (twisted-ring-action) setting.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofLeftInverse : {R : Type u_1} -> {R₂ : Type u_3} -> {M : Type u_5} -> {M₂ : Type u_7} -> [Semiring R] -> [Semiring R₂] -> [AddCommMonoid M] -> [AddCommMonoid M₂] -> {module_M : Module R M} -> {module_M₂ : Module R₂ M₂} -> {σ₁₂ : R →+* R₂} -> {σ₂₁ : R₂ →+* R} -> {f : M →ₛₗ[σ₁₂] M₂} -> [RingHomInvPair σ₁₂ σ₂₁] -> [RingHomInvPair σ₂₁ σ₁₂] -> {g : M₂ → M} -> (h : Function.LeftInverse g ⇑f) -> M ≃ₛₗ[σ₁₂] ↥f.range
<!-- PINNED-SIGNATURE:END -->


VTask.ofLeftInverse : {R : Type u_1} -> {R₂ : Type u_3} -> {M : Type u_5} -> {M₂ : Type u_7} -> [Semiring R] -> [Semiring R₂] -> [AddCommMonoid M] -> [AddCommMonoid M₂] -> {module_M : Module R M} -> {module_M₂ : Module R₂ M₂} -> {σ₁₂ : R →+* R₂} -> {σ₂₁ : R₂ →+* R} -> {f : M →ₛₗ[σ₁₂] M₂} -> [RingHomInvPair σ₁₂ σ₂₁] -> [RingHomInvPair σ₂₁ σ₁₂] -> {g : M₂ → M} -> (h : Function.LeftInverse g ⇑f) -> M ≃ₛₗ[σ₁₂] ↥f.range

`R` and `R₂` are the scalar rings acting on the source and target modules, respectively. `M` is the source module over `R`, and `M₂` is the target module over `R₂`. The ring homomorphisms `σ₁₂ : R →+* R₂` and `σ₂₁ : R₂ →+* R` are the scalings maps intertwined by the semilinear structure; the `RingHomInvPair` instances assert that these two ring maps are mutually inverse (up to the relevant composition). The map `f : M →ₛₗ[σ₁₂] M₂` is the semilinear map whose range we consider. The function `g : M₂ → M` is the left inverse (it need not itself be linear). The proof `h : Function.LeftInverse g f` witnesses that `g ∘ f = id` on `M`.

## Conventions

No junk-value or edge-case conventions are declared for this definition: it is a total constructor whose output is completely determined by the data provided, and all arguments are fully constrained by the type signature and the left-inverse hypothesis.

## Worked examples

- Claim: For the identity map `LinearMap.id : M →ₗ[R] M` with left inverse `id`, `VTask.ofLeftInverse` produces an equivalence between `M` and the range of `LinearMap.id`, which equals `⊤`.

- Claim: For an injective linear map `f : M →ₗ[R] M₂` with left inverse `g`, applying the forward direction of `VTask.ofLeftInverse h` to an element `m : M` yields `⟨f m, ⟨m, rfl⟩⟩` as a subtype element of `f.range`.

- Claim: For any `m : M`, the composite of the inverse of `VTask.ofLeftInverse h` followed by its forward direction is the identity on `M`; that is, the left-inverse condition `g (f m) = m` is precisely what makes the overall equivalence well-defined and left-invertible.

- Claim: For any element `x : ↥f.range`, the composite of the forward direction of `VTask.ofLeftInverse h` applied after its inverse is the identity on `f.range`; the right-inverse condition is guaranteed by the fact that every element of `f.range` is of the form `f m'` for some `m' : M`, so `f (g x) = x` in `M₂`.

## Boundaries

- If `g` is a left inverse of `f`, then `f` is necessarily injective, so the map to `f.range` is well-defined and bijective. No extra injectivity proof is needed.
- The function `g` is only required to be a set-theoretic left inverse; it does not need to be linear. However, the resulting structure is still a semilinear equivalence because linearity on the inverse side follows automatically from `f` being linear and `g` being a left inverse.
- The range submodule `f.range` may be a proper submodule of `M₂`, or all of `M₂` if `f` is also surjective. The equivalence always lands in `f.range` regardless.
- When `R = R₂` and `σ₁₂ = σ₂₁ = RingHom.id R`, this reduces to the ordinary linear equivalence between `M` and the range of a linear map with left inverse.
- The `RingHomInvPair` instances are required in both directions (`σ₁₂` composed with `σ₂₁` and vice versa) to ensure the semilinear structure on the equivalence and its inverse are coherent.

## Not to be confused with

- `LinearEquiv.ofInjective`: constructs the same kind of equivalence from an injectivity proof rather than an explicit left inverse; `VTask.ofLeftInverse` is described as a computable alternative to that.
- `LinearMap.rangeRestrict`: the one-directional semilinear map `M →ₛₗ[σ₁₂] f.range` (the forward half of this equivalence, without the inverse).
- `LinearEquiv.ofBijective`: constructs an equivalence between `M` and `M₂` when `f` is both injective and surjective, rather than to the range subtype.