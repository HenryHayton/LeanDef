## Object

`VTask.comp g f` is the composition of two affine isometries: given an affine isometry `f` from an affine space `P` to an affine space `P₂`, and an affine isometry `g` from `P₂` to a third affine space `P₃`, their composite is the affine isometry from `P` to `P₃` obtained by first applying `f` then `g`. The result preserves both the affine structure (it is an affine map) and distances (it is an isometry, meaning it preserves the norm of difference vectors).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {𝕜 : Type u_1} -> {V : Type u_2} -> {V₂ : Type u_5} -> {V₃ : Type u_6} -> {P : Type u_10} -> {P₂ : Type u_11} -> {P₃ : Type u_12} -> [NormedField 𝕜] -> [SeminormedAddCommGroup V] -> [NormedSpace 𝕜 V] -> [PseudoMetricSpace P] -> [NormedAddTorsor V P] -> [SeminormedAddCommGroup V₂] -> [NormedSpace 𝕜 V₂] -> [PseudoMetricSpace P₂] -> [NormedAddTorsor V₂ P₂] -> [SeminormedAddCommGroup V₃] -> [NormedSpace 𝕜 V₃] -> [PseudoMetricSpace P₃] -> [NormedAddTorsor V₃ P₃] -> (g : P₂ →ᵃⁱ[𝕜] P₃) -> (f : P →ᵃⁱ[𝕜] P₂) -> P →ᵃⁱ[𝕜] P₃
<!-- PINNED-SIGNATURE:END -->


`VTask.comp : {𝕜 : Type u_1} -> {V : Type u_2} -> {V₂ : Type u_5} -> {V₃ : Type u_6} -> {P : Type u_10} -> {P₂ : Type u_11} -> {P₃ : Type u_12} -> [NormedField 𝕜] -> [SeminormedAddCommGroup V] -> [NormedSpace 𝕜 V] -> [PseudoMetricSpace P] -> [NormedAddTorsor V P] -> [SeminormedAddCommGroup V₂] -> [NormedSpace 𝕜 V₂] -> [PseudoMetricSpace P₂] -> [NormedAddTorsor V₂ P₂] -> [SeminormedAddCommGroup V₃] -> [NormedSpace 𝕜 V₃] -> [PseudoMetricSpace P₃] -> [NormedAddTorsor V₃ P₃] -> (g : P₂ →ᵃⁱ[𝕜] P₃) -> (f : P →ᵃⁱ[𝕜] P₂) -> P →ᵃⁱ[𝕜] P₃`

The scalar field `𝕜` is the normed field over which all vector spaces and affine spaces are defined. The types `V`, `V₂`, `V₃` are the model vector spaces (with seminormed additive commutative group and normed `𝕜`-module structure) for the affine spaces `P`, `P₂`, `P₃` respectively; each affine space is equipped with a pseudo-metric compatible with its normed-torsor structure. The argument `g` is the outer affine isometry (applied second), mapping `P₂` to `P₃`. The argument `f` is the inner affine isometry (applied first), mapping `P` to `P₂`. The result is their pointwise composite, an affine isometry from `P` to `P₃`.

## Conventions

There are no junk-value or edge conventions: the function is total and every pair of composable affine isometries yields a well-defined affine isometry. No sentinel or degenerate output is defined.

## Worked examples

- Claim: The underlying affine map of `VTask.comp g f` sends a point `p : P` to `g (f p)`, i.e., it is the pointwise composition `g ∘ f`.

- Claim: `VTask.comp g f` preserves norms: for any vector `v`, the norm of `(VTask.comp g f).linearMap v` equals the norm of `v`. (Follows because `g` and `f` are each norm-preserving, so their composition is too.)

- Claim: Composition of affine isometries is associative: for composable affine isometries `f`, `g`, `h`, the maps `VTask.comp (VTask.comp h g) f` and `VTask.comp h (VTask.comp g f)` agree pointwise.

- Claim: Composing any affine isometry `f : P →ᵃⁱ[𝕜] P₂` on the right with the identity affine isometry on `P` gives an affine isometry that agrees with `f` pointwise.

## Boundaries

- The definition is well-typed only when `f` and `g` are composable, i.e., the codomain type of `f` matches the domain type of `g`; this is enforced statically by the type system.
- The scalar field `𝕜` must be a `NormedField`, but there is no additional restriction beyond being a normed field (in particular, it need not be `ℝ` or `ℂ`).
- Because the underlying spaces are affine spaces modelled on seminormed (rather than normed) vector spaces, the metrics are pseudo-metrics; distinct points can have zero distance. The isometry property still holds with respect to the chosen pseudo-metric structure.
- When `P = P₂ = P₃` and both `f` and `g` are the identity, the composite is also the identity.

## Not to be confused with

- `AffineIsometryEquiv.trans`: composition of affine isometry *equivalences* (invertible affine isometries); `VTask.comp` does not require the maps to be invertible.
- `AffineMap.comp`: composition of plain affine maps without any isometry (norm-preservation) condition; `VTask.comp` additionally guarantees the result is an isometry.
- `Isometry.comp` (metric isometries): composition of abstract distance-preserving maps not necessarily respecting affine structure; `VTask.comp` additionally preserves affine combinations.