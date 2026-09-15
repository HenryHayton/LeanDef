## Object

`VTask.mkContinuousLinear` constructs a continuous linear map from a normed space `G` to the space of continuous multilinear maps `ContinuousMultilinearMap 𝕜 E G'`, starting from a linear map `f : G →ₗ[𝕜] MultilinearMap 𝕜 E G'` whose values are (a priori only algebraically) multilinear, together with a uniform norm bound witnessing that the combined linear-multilinear evaluation is jointly controlled. The output is a genuine element of `G →L[𝕜] ContinuousMultilinearMap 𝕜 E G'`, meaning both the multilinear part (for each fixed linear input) and the linear part (varying the linear input) are continuous.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mkContinuousLinear : {𝕜 : Type u} -> {ι : Type v} -> {E : ι → Type wE} -> {G : Type wG} -> {G' : Type wG'} -> [NontriviallyNormedField 𝕜] -> [(i : ι) → SeminormedAddCommGroup (E i)] -> [(i : ι) → NormedSpace 𝕜 (E i)] -> [SeminormedAddCommGroup G] -> [NormedSpace 𝕜 G] -> [SeminormedAddCommGroup G'] -> [NormedSpace 𝕜 G'] -> [Fintype ι] -> (f : G →ₗ[𝕜] MultilinearMap 𝕜 E G') -> (C : ℝ) -> (H : ∀ (x : G) (m : (i : ι) → E i), ‖(f x) m‖ ≤ C * ‖x‖ * ∏ i, ‖m i‖) -> G →L[𝕜] ContinuousMultilinearMap 𝕜 E G'
<!-- PINNED-SIGNATURE:END -->


`VTask.mkContinuousLinear : {𝕜 : Type u} -> {ι : Type v} -> {E : ι → Type wE} -> {G : Type wG} -> {G' : Type wG'} -> [NontriviallyNormedField 𝕜] -> [(i : ι) → SeminormedAddCommGroup (E i)] -> [(i : ι) → NormedSpace 𝕜 (E i)] -> [SeminormedAddCommGroup G] -> [SeminormedAddCommGroup G'] -> [NormedSpace 𝕜 G] -> [NormedSpace 𝕜 G'] -> [Fintype ι] -> (f : G →ₗ[𝕜] MultilinearMap 𝕜 E G') -> (C : ℝ) -> (H : ∀ (x : G) (m : (i : ι) → E i), ‖(f x) m‖ ≤ C * ‖x‖ * ∏ i, ‖m i‖) -> G →L[𝕜] ContinuousMultilinearMap 𝕜 E G'`

The scalar field `𝕜` is a nontrivially normed field (e.g., `ℝ` or `ℂ`). The index type `ι` (finite via `Fintype ι`) parameterises the family of input spaces `E i` for the multilinear part. `G` is the domain of the linear part, and `G'` is the common target space. All spaces carry compatible seminormed structures over `𝕜`.

The explicit argument `f` is a linear map from `G` into the space of (algebraic, not yet continuous) multilinear maps from the family `E` to `G'`. The argument `C` is a real constant serving as the uniform norm bound. The argument `H` is the proof that for every linear input `x : G` and every multilinear input family `m : (i : ι) → E i`, the norm of the evaluation `(f x) m` is bounded by `C * ‖x‖ * ∏ i, ‖m i‖`; this combined estimate is exactly what is needed to promote `f` to a continuous linear map into the continuous multilinear maps.

## Conventions

When the supplied constant `C` is negative, the construction still succeeds; the effective operator-norm bound used internally is `max C 0`, so the negativity of `C` does not cause any inconsistency — the bound `max C 0` replaces it. No restriction on the sign of `C` is imposed by the definition itself.

## Worked examples

- Claim: For any linear map `f : G →ₗ[𝕜] MultilinearMap 𝕜 E G'` satisfying the bound with constant `C ≥ 0`, the norm of the resulting continuous linear map satisfies `‖VTask.mkContinuousLinear f C H‖ ≤ C`.

- Claim: For any `C : ℝ` (possibly negative), the norm of `VTask.mkContinuousLinear f C H` satisfies `‖VTask.mkContinuousLinear f C H‖ ≤ max C 0`.

- Claim: The underlying function of `VTask.mkContinuousLinear f C H`, when applied to `x : G`, equals the continuous multilinear map obtained by restricting `f x` using the bound `H x`; in particular, evaluating it at any `m` gives the same value as `(f x) m`.

## Boundaries

- If `C < 0`: the bound `H` forces `‖(f x) m‖ ≤ C * ‖x‖ * ∏ i, ‖m i‖`, which (since norms are non-negative) implies `f x = 0` for all `x`. The construction still produces a well-typed output; its norm is bounded by `max C 0 = 0`.
- If `C = 0`: the bound asserts that `f` is identically zero, and the output is the zero continuous linear map with norm `0`.
- If `ι` is empty (no multilinear inputs): the product `∏ i, ‖m i‖` is the empty product, equal to `1`, so the bound becomes `‖(f x) m‖ ≤ C * ‖x‖`. The construction still applies without modification.
- The definition is total: it imposes no domain restriction beyond the typeclass assumptions and the proof `H`.

## Not to be confused with

- `MultilinearMap.mkContinuous`: promotes a single *multilinear* map (not parameterised by a linear input) to a continuous multilinear map using a bound of the form `‖f m‖ ≤ C * ∏ i, ‖m i‖`; there is no linear variable `x` in the estimate.
- `LinearMap.mkContinuous`: promotes a single *linear* map to a continuous linear map using a bound `‖f x‖ ≤ C * ‖x‖`; the output space is not a space of multilinear maps.
- `VTask.mkContinuousMultilinear` (the multilinear analogue): constructs a continuous multilinear map from a multilinear map into multilinear maps, using a bound over all multilinear inputs without a separate linear variable.