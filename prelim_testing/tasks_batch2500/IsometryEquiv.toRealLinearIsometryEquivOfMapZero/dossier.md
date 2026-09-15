## Object

This construction embodies the **Mazur–Ulam theorem**: given an isometric bijection (isometry equivalence) between two real normed vector spaces that fixes the origin, the map is automatically ℝ-linear and an isometry. The result is packaged as a *linear isometry equivalence* over ℝ, i.e., a structure carrying both the algebraic proof that the map is an ℝ-linear isomorphism and the metric proof that it preserves norms.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toRealLinearIsometryEquivOfMapZero : {E : Type u_1} -> {F : Type u_3} -> [NormedAddCommGroup E] -> [NormedSpace ℝ E] -> [NormedAddCommGroup F] -> [NormedSpace ℝ F] -> (f : E ≃ᵢ F) -> (h0 : f 0 = 0) -> E ≃ₗᵢ[ℝ] F
<!-- PINNED-SIGNATURE:END -->


`VTask.toRealLinearIsometryEquivOfMapZero : {E : Type u_1} -> {F : Type u_3} -> [NormedAddCommGroup E] -> [NormedSpace ℝ E] -> [NormedAddCommGroup F] -> [NormedSpace ℝ F] -> (f : E ≃ᵢ F) -> (h0 : f 0 = 0) -> E ≃ₗᵢ[ℝ] F`

The implicit type arguments `E` and `F` are the source and target real normed vector spaces, each equipped with their normed-additive-commutative-group and real-normed-space instances via typeclass arguments. The explicit argument `f` is the isometric bijection (an isometry equivalence `E ≃ᵢ F`) to be linearised. The explicit argument `h0` is the proof that `f` maps the origin of `E` to the origin of `F`, which is the hypothesis required by the Mazur–Ulam theorem to promote `f` to a linear map.

## Conventions

No special junk-value or edge conventions are declared: the function is total on its stated inputs and the output is fully determined by `f` and `h0`. When the two spaces are the same and `f` is the identity isometry, the result is the identity linear isometry equivalence.

## Worked examples

- Claim: Applying `VTask.toRealLinearIsometryEquivOfMapZero` to the identity isometry on ℝ (with the trivial `h0 : id 0 = 0`) gives a linear isometry equivalence whose underlying function is the identity.

- Claim: For any isometry equivalence `f : E ≃ᵢ F` with `f 0 = 0`, the coercion of `VTask.toRealLinearIsometryEquivOfMapZero f h0` to a bare function equals `f` itself, i.e., `⇑(VTask.toRealLinearIsometryEquivOfMapZero f h0) = ⇑f`.

- Claim: For any `f : E ≃ᵢ F` with `f 0 = 0` and any `x : E`, the norm is preserved: `‖(VTask.toRealLinearIsometryEquivOfMapZero f h0) x‖ = ‖x‖`.

- Claim: The inverse of `VTask.toRealLinearIsometryEquivOfMapZero f h0` has its underlying function equal to `f.symm`, matching the inverse of the original isometry equivalence.

## Boundaries

- The hypothesis `h0 : f 0 = 0` is essential; without it the Mazur–Ulam theorem cannot promote `f` to a linear map, and the construction is not defined.
- For finite-dimensional spaces, the conclusion is not surprising, but the theorem holds for arbitrary (possibly infinite-dimensional) real normed spaces.
- If `f` already happens to be the identity on its carrier type, the resulting linear isometry equivalence is still constructed through the full Mazur–Ulam machinery; no special shortcut case is exposed.
- The construction is specific to normed spaces over **ℝ**; there is no analogous statement for complex normed spaces in general (isometries of complex spaces need not be ℂ-linear).

## Not to be confused with

- `IsometryEquiv` (`E ≃ᵢ F`): the raw isometric bijection that is the *input* to this construction, carrying no linearity data.
- `LinearIsometryEquiv` (`E ≃ₗᵢ[ℝ] F`): the type of the *output*; the construction here is the process of producing one from an origin-preserving isometry equivalence.
- The affine version of Mazur–Ulam, which upgrades an arbitrary (not necessarily origin-preserving) isometry equivalence to an affine isometry equivalence — a distinct result that does not require `f 0 = 0`.