## Object

`VTask.smulTorsor` constructs a **dilation equivalence** (a bijective map that scales all distances by a fixed positive ratio) from a normed vector space `E` to a normed affine torsor `P` over `E`. Concretely, it is the map `x ↦ k • x +ᵥ c`: scale a vector by the nonzero scalar `k` and then translate by the base point `c` into the torsor. The dilation ratio is the nonnorm `‖k‖₊`. The inverse sends a point `p ∈ P` back to `k⁻¹ • (p -ᵥ c) ∈ E`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.smulTorsor : {𝕜 : Type u_1} -> {E : Type u_2} -> [NormedDivisionRing 𝕜] -> [SeminormedAddCommGroup E] -> [Module 𝕜 E] -> [NormSMulClass 𝕜 E] -> {P : Type u_3} -> [PseudoMetricSpace P] -> [NormedAddTorsor E P] -> (c : P) -> {k : 𝕜} -> (hk : k ≠ 0) -> E ≃ᵈ P
<!-- PINNED-SIGNATURE:END -->


`VTask.smulTorsor : {𝕜 : Type u_1} -> {E : Type u_2} -> [NormedDivisionRing 𝕜] -> [SeminormedAddCommGroup E] -> [Module 𝕜 E] -> [NormSMulClass 𝕜 E] -> {P : Type u_3} -> [PseudoMetricSpace P] -> [NormedAddTorsor E P] -> (c : P) -> {k : 𝕜} -> (hk : k ≠ 0) -> E ≃ᵈ P`

The scalar field `𝕜` must be a normed division ring so that `k` has a multiplicative inverse. `E` is the normed module serving as both the source space and the vector space underlying the torsor. `P` is the normed affine torsor over `E` serving as the target. The explicit argument `c : P` is the **base point**: it is the image of the zero vector `0 ∈ E` under the map. The implicit argument `k : 𝕜` is the **scaling scalar**, and `hk : k ≠ 0` is the proof of nonvanishing required so that `k⁻¹` exists and the map is bijective.

## Conventions

There are no declared junk-value conventions for this definition: it is a total construction on its stated inputs, with the nonzero condition on `k` enforced explicitly by the hypothesis `hk`.

## Worked examples

- Claim: `VTask.smulTorsor c hk` sends `0 : E` to `c : P`, since `k • 0 +ᵥ c = 0 +ᵥ c = c`.

- Claim: The dilation ratio of `VTask.smulTorsor c hk` equals `‖k‖₊`, i.e., `ratio (VTask.smulTorsor c hk) = ‖k‖₊` whenever `x` and `y` are distinct points in `E`.

- Claim: The preimage under `VTask.smulTorsor c hk` of the metric ball in `P` centred at `c` with radius `‖k‖` is the unit ball in `E` centred at `0`; that is, `VTask.smulTorsor c hk ⁻¹' (Metric.ball c ‖k‖) = Metric.ball (0 : E) 1`.

- Claim: For `E = ℝ`, `P = ℝ`, `c = 3`, `k = 2`, the map sends `x` to `2 * x + 3`, so it sends `1` to `5`.

## Boundaries

- The hypothesis `k ≠ 0` is strictly required: if `k = 0` the scaling map would collapse all of `E` to a single point in `P`, failing to be a bijection, so the construction does not apply.
- When `‖k‖ = 1` (for example `k = -1` in a real normed space) the resulting dilation equivalence is in fact an isometric equivalence, since the ratio equals `1`.
- The base point `c` only affects the translation component; changing `c` to another point `c'` yields a different dilation equivalence whose ratio is the same `‖k‖₊` but whose geometric centre is `c'`.
- The construction is valid for any normed division ring `𝕜`, including non-commutative ones such as the quaternions, as long as the module axioms are satisfied.

## Not to be confused with

- `DilationEquiv.smul` (scaling a normed space to itself without a torsor offset; no base-point translation is involved).
- `IsometryEquiv.vaddConst` (translation by a fixed vector in a torsor, which is an isometry with ratio `1`, not a general dilation).
- `AffineMap.smul` (an affine map that scales about a base point but is not packaged as a `DilationEquiv` and does not carry the metric-ratio data).
