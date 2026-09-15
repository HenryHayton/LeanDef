## VTask.mk'

### Object

An affine isometry equivalence between two normed affine spaces over a normed field, constructed from the following data: a bare set-theoretic map between the point spaces, a linear isometry equivalence between the direction vector spaces, and a single base point together with a proof that the map behaves correctly relative to the linear part at that base point. Concretely, an affine isometry equivalence is a bijection between affine spaces that is simultaneously affine (respects the torsor structure) and an isometry (preserves distances), with the inverse also being an isometry.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mk' : {𝕜 : Type u_1} -> {V₁ : Type u_3} -> {V₂ : Type u_5} -> {P₁ : Type u_8} -> {P₂ : Type u_11} -> [NormedField 𝕜] -> [SeminormedAddCommGroup V₁] -> [NormedSpace 𝕜 V₁] -> [PseudoMetricSpace P₁] -> [NormedAddTorsor V₁ P₁] -> [SeminormedAddCommGroup V₂] -> [NormedSpace 𝕜 V₂] -> [PseudoMetricSpace P₂] -> [NormedAddTorsor V₂ P₂] -> (e : P₁ → P₂) -> (e' : V₁ ≃ₗᵢ[𝕜] V₂) -> (p : P₁) -> (h : ∀ (p' : P₁), e p' = e' (p' -ᵥ p) +ᵥ e p) -> P₁ ≃ᵃⁱ[𝕜] P₂
<!-- PINNED-SIGNATURE:END -->


`(e : P₁ → P₂)` is the underlying set-theoretic function between the point spaces that will become the forward map of the equivalence. `(e' : V₁ ≃ₗᵢ[𝕜] V₂)` is the linear isometry equivalence between the corresponding direction (vector) spaces, which serves as the linear part of the affine map. `(p : P₁)` is a chosen base point in the source affine space, used as the reference point to verify the affine condition. `(h : ∀ (p' : P₁), e p' = e' (p' -ᵥ p) +ᵥ e p)` is the proof that for every point `p'` in the source, the image under `e` equals the result of translating the base image `e p` by the linear isometry applied to the displacement from `p` to `p'`; this is exactly the condition that `e` is affine with linear part `e'`.

### Conventions

The affine condition `h` is only required to hold at the single chosen base point `p`, but this is equivalent to full affineness: once the relation `e p' = e' (p' -ᵥ p) +ᵥ e p` holds for all `p'` from one base `p`, the map is globally affine with linear part `e'`.

### Worked examples

- Claim: For any normed field `𝕜` and a linear isometry equivalence `e' : V₁ ≃ₗᵢ[𝕜] V₂`, constructing `VTask.mk' (fun p' => e' (p' -ᵥ p₀) +ᵥ q₀) e' p₀ (fun p' => rfl)` yields an affine isometry equivalence whose coercion to a function equals `fun p' => e' (p' -ᵥ p₀) +ᵥ q₀`.

- Claim: The linear isometry equivalence part of `VTask.mk' e e' p h` is exactly `e'`, i.e., `(VTask.mk' e e' p h).linearIsometryEquiv = e'`.

- Claim: The coercion of `VTask.mk' e e' p h` to a function is definitionally equal to `e`, i.e., `⇑(VTask.mk' e e' p h) = e`.

### Boundaries

- The base point `p` is used only to state and verify the affine condition; the resulting equivalence is independent of the particular choice of `p` in the sense that any `p` producing a valid `h` gives the same affine isometry equivalence (since `e` and `e'` are fixed).
- No topological or measurability conditions beyond those captured by the typeclass assumptions are needed; the construction works in the full generality of normed affine torsors over a normed field.
- The hypothesis `h` must cover all `p' : P₁` (it is universally quantified), not just a neighborhood of `p`.
- If `e` is not actually bijective or not actually isometric, no value of `h` and `e'` can satisfy the hypotheses consistently (since `e'` is a linear isometry equivalence, it forces bijectivity and isometry on `e` automatically).

### Not to be confused with

- `AffineIsometry.mk'`: the analogous constructor for affine isometry *maps* (not equivalences), which does not require or produce an inverse.
- `AffineEquiv.mk'`: the constructor for affine equivalences without the isometry/norm-preserving condition, which takes a `LinearEquiv` rather than a `LinearIsometryEquiv` as its linear part.
- `AffineIsometryEquiv.mk`: a more primitive constructor requiring full bundled data upfront, rather than verifying the affine condition at a single base point.