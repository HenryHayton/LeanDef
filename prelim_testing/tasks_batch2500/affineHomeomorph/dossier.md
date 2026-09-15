## Object

`VTask.affineHomeomorph a b h` is the homeomorphism from a topological field `𝕜` to itself given by the affine map `x ↦ a * x + b`, packaged as a topological equivalence (a bicontinuous bijection with explicit continuous inverse). The inverse map sends `y` to `(y - b) / a`. The non-vanishing hypothesis on `a` is precisely what makes this map invertible.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.affineHomeomorph : {𝕜 : Type u_2} -> [Field 𝕜] -> [TopologicalSpace 𝕜] -> [IsTopologicalRing 𝕜] -> (a b : 𝕜) -> (h : a ≠ 0) -> 𝕜 ≃ₜ 𝕜
<!-- PINNED-SIGNATURE:END -->


The implicit type argument `𝕜` is a topological field (equipped with a `Field` instance, a `TopologicalSpace` instance, and an `IsTopologicalRing` instance ensuring the ring operations are continuous). The argument `a` is the multiplicative slope of the affine map; it must be nonzero, as witnessed by the proof `h : a ≠ 0`. The argument `b` is the additive translation (the intercept). The result is a homeomorphism — a bundled bicontinuous bijection — from `𝕜` to itself.

## Conventions

The non-zero hypothesis `h : a ≠ 0` is a required explicit proof argument (not inferred); callers must supply it directly. There are no junk-value conventions because the definition is not total in `a`: the non-zero condition is enforced by the type signature itself.

## Worked examples

- Claim: For `𝕜 = ℝ`, `a = 2`, `b = 3`, the forward map sends `1` to `5`.
  (Apply the definition: `2 * 1 + 3 = 5`.)

- Claim: For `𝕜 = ℝ`, `a = 2`, `b = 3`, the inverse map sends `5` to `1`.
  (Apply the inverse: `(5 - 3) / 2 = 1`.)

- Claim: For `𝕜 = ℝ`, `a = -1`, `b = 0`, the map `x ↦ -x` is a homeomorphism. This corresponds to `VTask.affineHomeomorph (-1) 0 (by norm_num)`, whose forward function evaluates to `-1 * x + 0 = -x` and whose inverse evaluates to `(y - 0) / (-1) = -y`.

- Claim: For any nonzero `a` and any `b`, the composition of the forward and inverse functions of `VTask.affineHomeomorph a b h` is the identity, i.e., `(y - b) / a` composed with `x ↦ a * x + b` gives back `x`.

## Boundaries

- The case `a = 0` is excluded by the hypothesis `h : a ≠ 0`. If `a` were zero, the map `x ↦ 0 * x + b = b` would be constant, hence not injective and not a homeomorphism.
- The translation `b` may be any element of `𝕜`, including zero (which gives the homothety `x ↦ a * x`).
- When `a = 1` and `b = 0`, the homeomorphism is the identity on `𝕜`.
- When `a = 1`, the map is pure translation by `b`.

## Not to be confused with

- `ContinuousLinearEquiv` (a continuous linear equivalence): the affine homeomorphism is linear only when `b = 0`; for general `b` it is affine but not linear.
- A plain `Homeomorph` constructed from some other map on `𝕜`: this specific homeomorphism is the *affine* one `x ↦ a * x + b` and should not be confused with, e.g., inversion or other self-homeomorphisms of `𝕜`.
- `AffineMap` (an affine map without topology): `VTask.affineHomeomorph` is the full topological package, carrying both continuity and a continuous inverse, not merely the algebraic structure.