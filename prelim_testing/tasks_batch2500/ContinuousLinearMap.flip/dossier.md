## VTask.flip

### Object

Given a continuous bilinear map `f : E →SL[σ₁₃] F →SL[σ₂₃] G` (that is, a continuous linear map from `E` to the space of continuous linear maps from `F` to `G`, with the respective ring homomorphisms controlling scalar action), `VTask.flip f` is the continuous bilinear map obtained by swapping the two arguments: it is the map `F →SL[σ₂₃] E →SL[σ₁₃] G` that sends `y` to the continuous linear map `x ↦ f x y`. In other words, `(VTask.flip f) y x = f x y` for all `x : E` and `y : F`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.flip : {𝕜 : Type u_1} -> {𝕜₂ : Type u_2} -> {𝕜₃ : Type u_3} -> {E : Type u_4} -> {F : Type u_6} -> {G : Type u_8} -> [SeminormedAddCommGroup E] -> [SeminormedAddCommGroup F] -> [SeminormedAddCommGroup G] -> [NontriviallyNormedField 𝕜] -> [NontriviallyNormedField 𝕜₂] -> [NontriviallyNormedField 𝕜₃] -> [NormedSpace 𝕜 E] -> [NormedSpace 𝕜₂ F] -> [NormedSpace 𝕜₃ G] -> {σ₂₃ : 𝕜₂ →+* 𝕜₃} -> {σ₁₃ : 𝕜 →+* 𝕜₃} -> [RingHomIsometric σ₂₃] -> [RingHomIsometric σ₁₃] -> (f : E →SL[σ₁₃] F →SL[σ₂₃] G) -> F →SL[σ₂₃] E →SL[σ₁₃] G
<!-- PINNED-SIGNATURE:END -->


The implicit universe-polymorphic type arguments `𝕜`, `𝕜₂`, `𝕜₃` are scalar fields for the three spaces involved, each required to be nontrivially normed fields. The types `E`, `F`, `G` are the domain, intermediate, and codomain normed spaces, respectively, each equipped with a seminormed additive commutative group structure and a normed space structure over the appropriate field. The ring homomorphisms `σ₁₃ : 𝕜 →+* 𝕜₃` and `σ₂₃ : 𝕜₂ →+* 𝕜₃` encode the scalar compatibility between the fields; both are required to be isometric ring homomorphisms. The explicit argument `f` is the continuous bilinear map (in curried form) whose arguments are to be swapped.

### Conventions

No special junk-value or boundary conventions are declared for this definition: the operation is total over all continuous bilinear maps of the given type, and every instance of `VTask.flip f` is a fully legitimate continuous linear map.

### Worked examples

- Claim: For any continuous bilinear map `f : E →SL[σ₁₃] F →SL[σ₂₃] G`, applying `VTask.flip f` to `y` and then to `x` recovers `f x y`.

- Claim: The operator norm of `VTask.flip f` equals the operator norm of `f`, i.e., `‖VTask.flip f‖ = ‖f‖`.

- Claim: `VTask.flip (VTask.flip f)` and `f` agree as functions, i.e., applying double-flip recovers the original map pointwise.

### Boundaries

- When `f` is the zero map, `VTask.flip f` is also the zero map (since `f x y = 0` for all `x, y` implies `(VTask.flip f) y x = 0`).
- The operation is an involution on continuous bilinear maps: flipping twice returns a map that is pointwise equal to the original.
- The operator norm is preserved: `‖VTask.flip f‖ = ‖f‖`, so flipping is an isometry at the level of normed spaces of bilinear maps.
- Linearity and continuity in each argument are preserved by the flip, so `VTask.flip f` is indeed a valid element of `F →SL[σ₂₃] E →SL[σ₁₃] G`.

### Not to be confused with

- `ContinuousLinearMap.flipL`: the version of the same flip operation that is packaged as a `LinearIsometryEquiv`, providing the full isometric equivalence structure rather than just a single flipped map.
- `LinearMap.flip`: the analogous argument-swapping for plain (not necessarily continuous) linear maps, without any norm or continuity data.
- Function.swap / `flip` in the general function sense: those operate on arbitrary functions `α → β → γ` without any linearity or continuity requirements.