## VTask.mkContinuous

### Object

Given an alternating multilinear map `f : E [⋀^ι]→ₗ[𝕜] F` (a map that is linear in each of finitely many arguments indexed by `ι` and vanishes whenever two arguments coincide) together with a real constant `C` and a proof that the norm of `f` on any input tuple is bounded above by `C` times the product of the norms of the inputs, `VTask.mkContinuous` produces the corresponding **continuous** alternating map `E [⋀^ι]→L[𝕜] F`. The underlying algebraic map is identical; the constructor merely packages the boundedness hypothesis into a continuity certificate, upgrading the type to carry the topological data.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mkContinuous : {𝕜 : Type u} -> {E : Type wE} -> {F : Type wF} -> {ι : Type v} -> [NontriviallyNormedField 𝕜] -> [SeminormedAddCommGroup E] -> [NormedSpace 𝕜 E] -> [SeminormedAddCommGroup F] -> [NormedSpace 𝕜 F] -> [Fintype ι] -> (f : E [⋀^ι]→ₗ[𝕜] F) -> (C : ℝ) -> (H : ∀ (m : ι → E), ‖f m‖ ≤ C * ∏ i, ‖m i‖) -> E [⋀^ι]→L[𝕜] F
<!-- PINNED-SIGNATURE:END -->


`VTask.mkContinuous : {𝕜 : Type u} -> {E : Type wE} -> {F : Type wF} -> {ι : Type v} -> [NontriviallyNormedField 𝕜] -> [SeminormedAddCommGroup E] -> [NormedSpace 𝕜 E] -> [SeminormedAddCommGroup F] -> [NormedSpace 𝕜 F] -> [Fintype ι] -> (f : E [⋀^ι]→ₗ[𝕜] F) -> (C : ℝ) -> (H : ∀ (m : ι → E), ‖f m‖ ≤ C * ∏ i, ‖m i‖) -> E [⋀^ι]→L[𝕜] F`

The scalar field `𝕜` must be a nontrivially normed field; `E` and `F` are seminormed additive commutative groups carrying `𝕜`-module (normed space) structures; `ι` is a finite index type used to label the arguments of the alternating map. The argument `f` is the alternating multilinear map to be promoted. The argument `C` is the proposed bound constant: any real number (including negative values) is accepted, though only non-negative choices yield sharp operator-norm estimates. The argument `H` is the proof obligation that, for every tuple `m : ι → E`, the output norm satisfies `‖f m‖ ≤ C * ∏ i, ‖m i‖`.

### Conventions

The constant `C` is allowed to be negative: if `C < 0` the hypothesis `H` forces `f` to be identically zero (since norms are non-negative), and the construction still type-checks without restriction. When `C` is not assumed non-negative, the operator norm of the resulting map is bounded by `max C 0` rather than `C` itself.

### Worked examples

- Claim: Applying `VTask.mkContinuous` to the zero alternating map with `C = 0` and the trivial bound yields a continuous alternating map whose underlying function is still the zero map.

- Claim: For a continuous alternating map `g : E [⋀^ι]→L[𝕜] F` promoted from its underlying alternating map `f` via `VTask.mkContinuous f C H`, the value at any tuple `m` satisfies `‖VTask.mkContinuous f C H m‖ ≤ C * ∏ i, ‖m i‖` (directly from `H`).

- Claim: When `C ≥ 0`, the operator norm of `VTask.mkContinuous f C H` is at most `C`; that is, `‖VTask.mkContinuous f C H‖ ≤ C`.

- Claim: For any `C : ℝ` (possibly negative), `‖VTask.mkContinuous f C H‖ ≤ max C 0`.

### Boundaries

- **Negative `C`:** The hypothesis `H` with a negative `C` is consistent only when `f` is the zero map (since `‖f m‖ ≥ 0`). The construction is still valid; the operator norm bound `max C 0 = 0` correctly reflects this.
- **Empty index type `ι`:** When `ι` is empty (Fintype with zero elements), the product `∏ i, ‖m i‖` is the empty product, equal to `1`, so the bound reduces to `‖f m‖ ≤ C` for the single input tuple (the unique map from the empty type). The result is a continuous alternating map on zero arguments.
- **`C = 0`:** Forces `f` to be identically zero on all inputs; the resulting operator norm is `0`.
- **Non-sharp `C`:** Using a `C` larger than the optimal bound is permitted; the norm estimate `‖VTask.mkContinuous f C H‖ ≤ C` will still hold and be valid, just not tight.

### Not to be confused with

- `ContinuousMultilinearMap.mkContinuous`: the analogous constructor for (not necessarily alternating) continuous multilinear maps; does not enforce the alternating (antisymmetry/vanishing on repeated inputs) condition.
- `AlternatingMap.mkContinuousLinear`: promotes a linear map into alternating maps `F →ₗ[𝕜] E [⋀^ι]→ₗ[𝕜] G` to a continuous linear map, requiring a two-factor norm bound involving both a linear and a multilinear component.
- `AlternatingMap.mkContinuousAlternating`: promotes an alternating-map-valued alternating map (a bilinear alternating construction), with a product-of-two-products norm bound, to a continuous version.
