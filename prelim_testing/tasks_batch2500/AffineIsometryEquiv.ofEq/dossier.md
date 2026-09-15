## Object

Given two affine subspaces `s₁` and `s₂` of a normed affine space that are equal as subspaces, `VTask.ofEq` produces a canonical affine isometry equivalence (an isometric bijection that respects the affine structure) from `s₁` to `s₂`. It is the distance-preserving, affine-structure-respecting version of the purely algebraic "reindex by an equality" map: when two subspaces are literally the same object, there is an obvious way to identify them, and this construction packages that identification as a full affine isometry equivalence.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofEq : {𝕜 : Type u_1} -> {V : Type u_2} -> {P : Type u_10} -> [NormedField 𝕜] -> [SeminormedAddCommGroup V] -> [NormedSpace 𝕜 V] -> [PseudoMetricSpace P] -> [NormedAddTorsor V P] -> (s₁ s₂ : AffineSubspace 𝕜 P) -> [Nonempty ↥s₁] -> [Nonempty ↥s₂] -> (h : s₁ = s₂) -> ↥s₁ ≃ᵃⁱ[𝕜] ↥s₂
<!-- PINNED-SIGNATURE:END -->


`VTask.ofEq : {𝕜 : Type u_1} -> {V : Type u_2} -> {P : Type u_10} -> [NormedField 𝕜] -> [SeminormedAddCommGroup V] -> [NormedSpace 𝕜 V] -> [PseudoMetricSpace P] -> [NormedAddTorsor V P] -> (s₁ s₂ : AffineSubspace 𝕜 P) -> [Nonempty ↥s₁] -> [Nonempty ↥s₂] -> (h : s₁ = s₂) -> ↥s₁ ≃ᵃⁱ[𝕜] ↥s₂`

`𝕜` is the scalar field (a normed field, e.g., ℝ or ℂ). `V` is the vector space over `𝕜`, equipped with a seminorm and compatible `𝕜`-module structure. `P` is the affine point space, equipped with a pseudo-metric and a normed affine torsor structure over `V`. `s₁` and `s₂` are the two affine subspaces of `P` being identified; they must each be non-empty (witnessed by the two `Nonempty` instances). `h` is the proof that `s₁` and `s₂` are equal as affine subspaces.

## Conventions

There are no junk-value or edge-case conventions to declare: the function is defined exactly when all hypotheses (including the equality proof `h`) are satisfied, and in that regime it behaves as the identity-like isometry — no degenerate output is assigned outside the stated domain.

## Worked examples

- Claim: For any affine subspace `s` (non-empty) of a normed torsor, `VTask.ofEq s s rfl` is the identity affine isometry equivalence on `s`; in particular it maps every point `x : s` to itself.

- Claim: If `h : s₁ = s₂` is a proof of equality, then the underlying function of `VTask.ofEq s₁ s₂ h` sends a point `p : ↥s₁` to the corresponding point in `↥s₂` obtained by casting along `h`, and the map preserves all pairwise distances.

- Claim: The inverse of `VTask.ofEq s₁ s₂ h` is `VTask.ofEq s₂ s₁ h.symm`.

## Boundaries

- When `h` is `rfl` (i.e., `s₁` and `s₂` are definitionally the same), the resulting equivalence is the identity isometry on `s₁`.
- The `Nonempty` hypotheses are required by the general framework for affine isometry equivalences between subspaces (they ensure the basepoint needed for the affine structure is available); the definition itself does not do anything interesting at those boundaries — it simply requires them to be present.
- Since the map is constructed from an equality, it carries no geometric information beyond the identification: the norm map is trivially the identity on displacement vectors.

## Not to be confused with

- `AffineEquiv.ofEq`: the purely algebraic version, which gives an affine equivalence without the isometry (norm-preserving) guarantee.
- `AffineIsometryEquiv.refl`: the reflexivity isometry `s ≃ᵃⁱ[𝕜] s`, which is the special case `VTask.ofEq s s rfl` but stated directly without going through an equality proof.
- `AffineIsometry.ofEq`: a one-sided (non-invertible) affine isometry constructed from an equality, lacking the equivalence/bijection structure.