## Object

`VTask.mkContinuousLinear` promotes a `𝕜`-linear map `f` from `F` to the space of alternating multilinear maps `E [⋀^ι]→ₗ[𝕜] G` (which carries no a priori continuity) into a genuine continuous linear map `F →L[𝕜] E [⋀^ι]→L[𝕜] G`, provided one supplies a constant `C` and a norm estimate witnessing that every evaluation is bounded. In other words, it is a constructor that certifies continuity of a linearly-parametrized family of alternating maps by a uniform product-of-norms bound.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mkContinuousLinear : {𝕜 : Type u} -> {E : Type wE} -> {F : Type wF} -> {G : Type wG} -> {ι : Type v} -> [NontriviallyNormedField 𝕜] -> [SeminormedAddCommGroup E] -> [NormedSpace 𝕜 E] -> [SeminormedAddCommGroup F] -> [NormedSpace 𝕜 F] -> [SeminormedAddCommGroup G] -> [NormedSpace 𝕜 G] -> [Fintype ι] -> (f : F →ₗ[𝕜] E [⋀^ι]→ₗ[𝕜] G) -> (C : ℝ) -> (H : ∀ (x : F) (m : ι → E), ‖(f x) m‖ ≤ C * ‖x‖ * ∏ i, ‖m i‖) -> F →L[𝕜] E [⋀^ι]→L[𝕜] G
<!-- PINNED-SIGNATURE:END -->


`VTask.mkContinuousLinear : {𝕜 : Type u} -> {E : Type wE} -> {F : Type wF} -> {G : Type wG} -> {ι : Type v} -> [NontriviallyNormedField 𝕜] -> [SeminormedAddCommGroup E] -> [NormedSpace 𝕜 E] -> [SeminormedAddCommGroup F] -> [NormedSpace 𝕜 F] -> [SeminormedAddCommGroup G] -> [NormedSpace 𝕜 G] -> [Fintype ι] -> (f : F →ₗ[𝕜] E [⋀^ι]→ₗ[𝕜] G) -> (C : ℝ) -> (H : ∀ (x : F) (m : ι → E), ‖(f x) m‖ ≤ C * ‖x‖ * ∏ i, ‖m i‖) -> F →L[𝕜] E [⋀^ι]→L[𝕜] G`

The universe-polymorphic type variables `𝕜`, `E`, `F`, `G`, and `ι` are implicit and inferred from context. The typeclass arguments supply the normed-field structure on the scalar field `𝕜`, the seminormed additive group and `𝕜`-module structures on the three vector spaces `E`, `F`, `G`, and finiteness of the index type `ι` (which governs the arity of the alternating maps). The explicit argument `f` is the underlying `𝕜`-linear map from the domain space `F` into the type of alternating multilinear maps `E [⋀^ι]→ₗ[𝕜] G`; it carries no continuity data on its own. The argument `C` is a real constant serving as an upper bound on operator size. The argument `H` is the pointwise norm estimate: for every vector `x : F` and every tuple `m : ι → E`, the norm of the evaluation `(f x) m` is at most `C` times the norm of `x` times the product of the norms of the components of `m`; this estimate is precisely what ensures the resulting map is continuous.

## Conventions

When the supplied bound `C` is negative, the construction still produces a valid continuous linear map; the operator norm of the result is controlled by `max C 0` rather than by `C` itself, so a negative `C` is treated as `0` for norm-bounding purposes. When `C ≥ 0`, the operator norm of the result is bounded directly by `C`.

## Worked examples

- Claim: For any linear map `f : F →ₗ[𝕜] E [⋀^ι]→ₗ[𝕜] G` with bound `C ≥ 0` and hypothesis `H`, the operator norm of `VTask.mkContinuousLinear f C H` is at most `C`.

- Claim: For any linear map `f : F →ₗ[𝕜] E [⋀^ι]→ₗ[𝕜] G` with arbitrary real constant `C` (possibly negative) and hypothesis `H`, the operator norm of `VTask.mkContinuousLinear f C H` is at most `max C 0`.

- Claim: Applying `VTask.mkContinuousLinear f C H` to a vector `x : F` and then evaluating the resulting continuous alternating map at a tuple `m : ι → E` gives the same value as `(f x) m`.

## Boundaries

- If `C < 0`, the norm bound in `H` forces `‖(f x) m‖ ≤ C * ‖x‖ * ∏ i, ‖m i‖ ≤ 0`, so every evaluation is zero, yet the construction is still well-defined; the operator norm is bounded by `max C 0 = 0`.
- If `ι` is the empty type, the product `∏ i, ‖m i‖` is the empty product, equal to `1`, so the bound reduces to `‖(f x) m‖ ≤ C * ‖x‖`, i.e., the alternating map in the image is a single scalar multiple of `x`.
- The bound `H` is used only to certify continuity; the actual map values are entirely determined by `f`. The constructed map evaluates identically to `f` at all points.
- `C = 0` is a valid input; the estimate then forces all evaluations to zero, and the operator norm of the result is `0`.

## Not to be confused with

- `AlternatingMap.mkContinuous`: promotes a single alternating linear map (not a linear family) to a continuous alternating map, given a pointwise bound `‖f m‖ ≤ C * ∏ i, ‖m i‖`; there is no `F`-linear parameter.
- `ContinuousLinearMap.mkContinuous` (or `LinearMap.mkContinuous`): promotes a plain `𝕜`-linear map between normed spaces to a continuous one, with no alternating-map structure involved.
- `VTask.mkContinuousLinear` applied after precomposing with `ContinuousAlternatingMap.toAlternatingMapLinear`: this is the standard idiom for lifting a map defined on algebraic alternating maps to one on continuous alternating maps, but the two steps should not be confused with the single-step constructor itself.