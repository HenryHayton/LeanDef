## VTask.arrowCongrEquiv

### Object

Given affine isomorphisms `e₁ : P₁ ≃ᵃ[k] P₂` and `e₂ : P₃ ≃ᵃ[k] P₄`, this is a bijection (an equivalence of types) between the space of affine maps `P₁ →ᵃ[k] P₃` and the space of affine maps `P₂ →ᵃ[k] P₄`. Intuitively, it transports an affine map between one pair of affine spaces to a corresponding affine map between another pair, by conjugating with the given affine isomorphisms: the forward direction sends `f` to `e₂ ∘ f ∘ e₁⁻¹`, and the inverse direction sends `g` to `e₂⁻¹ ∘ g ∘ e₁`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.arrowCongrEquiv : {k : Type u_1} -> {P₁ : Type u_2} -> {P₂ : Type u_3} -> {P₃ : Type u_4} -> {P₄ : Type u_5} -> {V₁ : Type u_6} -> {V₂ : Type u_7} -> {V₃ : Type u_8} -> {V₄ : Type u_9} -> [Ring k] -> [AddCommGroup V₁] -> [AddCommGroup V₂] -> [AddCommGroup V₃] -> [AddCommGroup V₄] -> [Module k V₁] -> [Module k V₂] -> [Module k V₃] -> [Module k V₄] -> [AddTorsor V₁ P₁] -> [AddTorsor V₂ P₂] -> [AddTorsor V₃ P₃] -> [AddTorsor V₄ P₄] -> (e₁ : P₁ ≃ᵃ[k] P₂) -> (e₂ : P₃ ≃ᵃ[k] P₄) -> (P₁ →ᵃ[k] P₃) ≃ (P₂ →ᵃ[k] P₄)
<!-- PINNED-SIGNATURE:END -->


The implicit universe-polymorphic type arguments `k`, `P₁`, `P₂`, `P₃`, `P₄`, `V₁`, `V₂`, `V₃`, `V₄` are the scalar ring, four affine spaces, and their four associated direction vector spaces, respectively. The typeclass arguments supply the ring structure on `k`, abelian group structures on the vector spaces, `k`-module structures on the vector spaces, and torsor structures making each `Pᵢ` an affine space over `Vᵢ`. The first explicit argument `e₁` is an affine isomorphism from `P₁` to `P₂`, used to change the domain of an affine map. The second explicit argument `e₂` is an affine isomorphism from `P₃` to `P₄`, used to change the codomain of an affine map.

### Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a total construction producing a well-defined equivalence for any valid inputs satisfying the typeclass constraints.

### Worked examples

- Claim: For identity affine isomorphisms `e₁ = AffineEquiv.refl k P₁` and `e₂ = AffineEquiv.refl k P₃`, the equivalence `VTask.arrowCongrEquiv e₁ e₂` sends an affine map `f : P₁ →ᵃ[k] P₃` to itself.

- Claim: The forward map of `VTask.arrowCongrEquiv e₁ e₂` applied to `f` equals `e₂.toAffineMap.comp (f.comp e₁.symm.toAffineMap)`, i.e., the conjugate `e₂ ∘ f ∘ e₁⁻¹`.

- Claim: The composition `(VTask.arrowCongrEquiv e₁ e₂).symm.trans (VTask.arrowCongrEquiv e₁ e₂)` is the identity equivalence on `P₁ →ᵃ[k] P₃`, reflecting that the construction is a genuine equivalence of types.

- Claim: If `g : P₂ →ᵃ[k] P₄` is in the range of `VTask.arrowCongrEquiv e₁ e₂`, then `(VTask.arrowCongrEquiv e₁ e₂).symm g` equals `e₂.symm.toAffineMap.comp (g.comp e₁.toAffineMap)`.

### Boundaries

- When `P₁ = P₂` and `e₁ = AffineEquiv.refl k P₁`, the forward map of the equivalence acts only by post-composing with `e₂`, i.e., `f ↦ e₂.toAffineMap.comp f`.
- When `P₃ = P₄` and `e₂ = AffineEquiv.refl k P₃`, the forward map acts only by pre-composing with `e₁⁻¹`, i.e., `f ↦ f.comp e₁.symm.toAffineMap`.
- When both isomorphisms are identities, the equivalence is the identity on the function space.
- The construction works for any ring `k` (not necessarily commutative), since only a `Ring` instance is required rather than `CommRing`.

### Not to be confused with

- `AffineEquiv.arrowCongr`: the affine-map version of the conjugation action, which may return an affine map rather than a bare equivalence of types.
- `AffineEquiv.arrowCongrₗ`: the linear version, producing an equivalence or isomorphism of the linear structure on the function spaces, not just the underlying sets.
- Conjugation by a single affine isomorphism on the domain or codomain alone, rather than simultaneously on both.