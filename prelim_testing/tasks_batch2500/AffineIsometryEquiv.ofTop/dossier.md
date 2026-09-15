## Object

`VTask.ofTop` produces a canonical isometric affine equivalence (an affine isometry equivalence) between an affine subspace `s₁` of a normed affine space `P` and the whole space `P` itself, given a proof that `s₁` equals the top subspace `⊤` (i.e., all of `P`). Concretely, it is the identity map viewed as a distance-preserving affine bijection from the coerced type `↥s₁` to `P`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofTop : {𝕜 : Type u_1} -> {V : Type u_2} -> {P : Type u_10} -> [NormedField 𝕜] -> [SeminormedAddCommGroup V] -> [NormedSpace 𝕜 V] -> [PseudoMetricSpace P] -> [NormedAddTorsor V P] -> (s₁ : AffineSubspace 𝕜 P) -> [Nonempty ↥s₁] -> (h : s₁ = ⊤) -> ↥s₁ ≃ᵃⁱ[𝕜] P
<!-- PINNED-SIGNATURE:END -->


`VTask.ofTop : {𝕜 : Type u_1} -> {V : Type u_2} -> {P : Type u_10} -> [NormedField 𝕜] -> [SeminormedAddCommGroup V] -> [NormedSpace 𝕜 V] -> [PseudoMetricSpace P] -> [NormedAddTorsor V P] -> (s₁ : AffineSubspace 𝕜 P) -> [Nonempty ↥s₁] -> (h : s₁ = ⊤) -> ↥s₁ ≃ᵃⁱ[𝕜] P`

The scalar field `𝕜` is a normed field providing the affine structure's scalars. The type `V` is the normed vector space of translations, and `P` is the normed affine (pseudo-metric) space acted on by `V`. The argument `s₁` is the affine subspace being promoted to the whole space. The `Nonempty` instance on `↥s₁` confirms the subspace has at least one point, which is needed to form the equivalence. The argument `h` is the proof that `s₁` equals `⊤`, i.e., the entire space `P`.

## Conventions

There are no junk-value conventions declared for this definition: it is a total function on its stated domain — it is only defined when a proof `h : s₁ = ⊤` is supplied, so no out-of-domain inputs arise.

## Worked examples

- Claim: For `s₁ = ⊤` in a normed affine space, `VTask.ofTop s₁ h` applied to any element `x : ↥s₁` yields a point in `P` whose underlying value equals the coercion of `x`.

- Claim: The underlying affine map of `VTask.ofTop s₁ h` is bijective (since it is an equivalence), and its norm map sends every vector to a vector of the same norm, confirming it is an isometry.

- Claim: For any normed field `𝕜`, normed space `V`, and normed additive torsor `P`, if `h : (⊤ : AffineSubspace 𝕜 P) = ⊤`, then `VTask.ofTop ⊤ h` is an isometric affine equivalence from `↥(⊤ : AffineSubspace 𝕜 P)` to `P`.

## Boundaries

- The proof `h : s₁ = ⊤` is required; without it, the function cannot be called. There is no fallback or default for subspaces that do not equal `⊤`.
- The `Nonempty ↥s₁` instance is required. Since `s₁ = ⊤` and any affine space is inhabited, in practice this instance is always available when `h` holds, but it must be supplied explicitly to the type class system.
- When `s₁ = ⊤`, every element of `P` belongs to `s₁`, so the equivalence is a bijection over all of `P`; there is no restriction to a proper subset.
- The isometry property means distances and norms of difference vectors are preserved exactly, not just up to a constant.

## Not to be confused with

- `AffineSubspace.topEquiv`: the canonical affine equivalence between `↥(⊤ : AffineSubspace 𝕜 P)` and `P`, which is purely an affine equivalence without the isometry/norm-preserving structure bundled in.
- `AffineIsometryEquiv.refl`: the identity isometric affine equivalence on a space with itself, which does not involve a subspace coercion at all.
- `AffineEquiv.ofEq`: a plain affine (not necessarily isometric) equivalence between two equal affine subspaces, which `VTask.ofTop` builds upon internally but which lacks the norm-preservation guarantee.