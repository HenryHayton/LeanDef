## VTask.codRestrict

### Object

Given a continuous linear map `f : M₁ →SL[σ₁₂] M₂` whose image is entirely contained in a submodule `p` of `M₂`, `VTask.codRestrict f p h` is the continuous linear map `M₁ →SL[σ₁₂] ↥p` obtained by viewing the same underlying function as a map into `p` (rather than into the larger module `M₂`). In other words, it is the codomain-restriction of `f` to the subspace `p`, carrying along both the linearity and the continuity of `f`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.codRestrict : {R₁ : Type u_1} -> {R₂ : Type u_2} -> [Semiring R₁] -> [Semiring R₂] -> {σ₁₂ : R₁ →+* R₂} -> {M₁ : Type u_4} -> {M₂ : Type u_5} -> [TopologicalSpace M₁] -> [AddCommMonoid M₁] -> [Module R₁ M₁] -> [TopologicalSpace M₂] -> [AddCommMonoid M₂] -> [Module R₂ M₂] -> (f : M₁ →SL[σ₁₂] M₂) -> (p : Submodule R₂ M₂) -> (h : ∀ (x : M₁), f x ∈ p) -> M₁ →SL[σ₁₂] ↥p
<!-- PINNED-SIGNATURE:END -->


VTask.codRestrict : {R₁ : Type u_1} -> {R₂ : Type u_2} -> [Semiring R₁] -> [Semiring R₂] -> {σ₁₂ : R₁ →+* R₂} -> {M₁ : Type u_4} -> {M₂ : Type u_5} -> [TopologicalSpace M₁] -> [AddCommMonoid M₁] -> [Module R₁ M₁] -> [TopologicalSpace M₂] -> [AddCommMonoid M₂] -> [Module R₂ M₂] -> (f : M₁ →SL[σ₁₂] M₂) -> (p : Submodule R₂ M₂) -> (h : ∀ (x : M₁), f x ∈ p) -> M₁ →SL[σ₁₂] ↥p

The ring scalars `R₁` and `R₂` are the coefficient rings for the domain and codomain modules respectively, related by the ring homomorphism `σ₁₂`. The topological module `M₁` is the domain and `M₂` is the ambient codomain module. The argument `f` is the original continuous linear (σ₁₂-semilinear) map whose codomain is being restricted. The argument `p` is the target submodule of `M₂` into which the image of `f` must fall. The argument `h` is the proof that every element in the image of `f` belongs to `p`, i.e., the membership certificate that makes the restriction well-typed.

### Conventions

No special junk-value or edge conventions are declared for this definition: the construction is well-typed precisely when the membership proof `h` is supplied, and there are no implicit out-of-domain inputs that would require a default return value.

### Worked examples

- Claim: For any continuous linear map `f : M₁ →SL[σ₁₂] M₂` and submodule `p` with `h : ∀ x, f x ∈ p`, the underlying function of `VTask.codRestrict f p h` (coerced back to `M₂`) agrees pointwise with `f` itself.

- Claim: The kernel of `VTask.codRestrict f p h` (viewed as a semilinear map into `p`) equals the kernel of the original map `f` (viewed as a semilinear map into `M₂`).

- Claim: If `g : M₂ →SL[σ₂₃] M₃` is another continuous linear map, then `g.domRestrict p ∘SL VTask.codRestrict f p h` equals `g ∘SL f` as maps `M₁ → M₃`.

### Boundaries

- When `p` is the entire module `M₂` (i.e., `p = ⊤`), the result is essentially the same map as `f`, but with codomain type `↥(⊤ : Submodule R₂ M₂)` rather than `M₂`; the values are the same up to the canonical isomorphism.
- When `f` is the zero map, every value lies in any submodule (including `⊥`), so the membership proof `h` is trivially satisfied and the restriction to `⊥` yields the zero map into the trivial submodule.
- The construction does not require any topological or algebraic property stronger than continuity of `f` and the submodule structure of `p`; in particular, `p` need not be closed, open, or have any extra topological property.
- The coercion `(VTask.codRestrict f p h x : M₂)` recovers exactly `f x`, so no information about the values is lost.

### Not to be confused with

- `ContinuousLinearMap.domRestrict`: restricts the *domain* of a continuous linear map to a submodule, rather than the codomain.
- `ContinuousLinearMap.restrict`: simultaneously restricts both the domain and the codomain to submodules, requiring a combined membership condition.
- `LinearMap.codRestrict`: the purely algebraic (non-topological) codomain restriction of a linear map, which does not carry or verify continuity.
