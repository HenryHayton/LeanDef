## Object

`VTask.toSpanSingleton` constructs, from a unit-norm vector `v` in a normed space `E` over a nontrivially normed field `𝕜`, the canonical linear isometry that embeds the field `𝕜` into `E` by sending each scalar `c` to the scalar multiple `c • v`. Because `v` has norm 1, multiplying by any scalar `c` scales the norm exactly by `‖c‖`, so this map is isometric (i.e., it is a norm-preserving linear map).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toSpanSingleton : (𝕜 : Type u_1) -> (E : Type u_4) -> [SeminormedAddCommGroup E] -> [NontriviallyNormedField 𝕜] -> [NormedSpace 𝕜 E] -> {v : E} -> (hv : ‖v‖ = 1) -> 𝕜 →ₗᵢ[𝕜] E
<!-- PINNED-SIGNATURE:END -->


VTask.toSpanSingleton : (𝕜 : Type u_1) -> (E : Type u_4) -> [SeminormedAddCommGroup E] -> [NontriviallyNormedField 𝕜] -> [NormedSpace 𝕜 E] -> {v : E} -> (hv : ‖v‖ = 1) -> 𝕜 →ₗᵢ[𝕜] E

The first explicit argument `𝕜` is the scalar field (e.g., `ℝ` or `ℂ`). The second explicit argument `E` is the normed space in which the unit vector lives. The instance arguments supply the seminormed group structure on `E`, the nontrivially normed field structure on `𝕜`, and the compatible normed-space module structure. The implicit argument `v : E` is the unit vector serving as the "direction" of the embedding. The proof argument `hv : ‖v‖ = 1` witnesses that `v` is indeed a unit vector.

## Conventions

The map is only well-defined (and isometric) when the vector `v` satisfies `‖v‖ = 1`; this is enforced by requiring an explicit proof `hv`. If one were to imagine supplying a zero vector or a non-unit vector, the isometry property would fail, so no such junk-value convention is declared.

## Worked examples

- Claim: For `𝕜 = ℝ`, `E = ℝ`, and `v = 1` (with `‖1‖ = 1`), the map `VTask.toSpanSingleton ℝ ℝ (by norm_num : ‖(1 : ℝ)‖ = 1)` sends any scalar `c : ℝ` to `c • 1 = c`, so it is the identity on `ℝ`.

- Claim: For `𝕜 = ℝ`, `E = ℝ²` (i.e., `Fin 2 → ℝ`), and `v` the standard basis vector `e₀` (which has norm 1), the map `VTask.toSpanSingleton ℝ (Fin 2 → ℝ) hv` sends `c : ℝ` to the vector `c • e₀`, and satisfies `‖VTask.toSpanSingleton ℝ (Fin 2 → ℝ) hv c‖ = ‖c‖` for all `c`.

- Claim: The map `VTask.toSpanSingleton 𝕜 E hv` is injective, since a linear isometry is always injective (it preserves norms, so its kernel is trivial).

- Claim: The image of `VTask.toSpanSingleton 𝕜 E hv` is exactly the one-dimensional subspace `𝕜 • {v}` (the span of `v` in `E`).

## Boundaries

- The proof obligation `hv : ‖v‖ = 1` is the only constraint; the map is defined for any such unit vector in any normed space over a nontrivially normed field.
- When `𝕜 = E` (one-dimensional case) and `v = 1`, the map is an isometric isomorphism of `𝕜` with itself.
- The map is `𝕜`-linear by construction and hence in particular additive; it commutes with scalar multiplication by any element of `𝕜`.
- The nontrivial norm on `𝕜` (the `NontriviallyNormedField` hypothesis) is essential: it ensures there exist elements of `𝕜` with `‖c‖ ≠ 0`, which is needed for injectivity and for the isometry property to be non-degenerate.

## Not to be confused with

- `LinearMap.toSpanSingleton 𝕜 E v` — the underlying `𝕜`-linear map sending `c` to `c • v`, but without any norm/isometry structure; `VTask.toSpanSingleton` wraps this with the isometry proof.
- `Submodule.span 𝕜 {v}` — the submodule spanned by `v` as a set-theoretic object, not a map from `𝕜`.
- A general linear isometry `E →ₗᵢ[𝕜] F` between two normed spaces — this construction is the specific one arising from multiplication by a unit vector, not an arbitrary linear isometry.