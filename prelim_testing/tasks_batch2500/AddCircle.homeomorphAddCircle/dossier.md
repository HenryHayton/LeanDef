## Object

This is the canonical homeomorphism (continuous bijection with continuous inverse) between two additive circles with possibly different periods `p` and `q` over an ordered field `𝕜` equipped with its order topology. The additive circle with period `r` is the quotient `𝕜 / (r · ℤ)` — the "circle" obtained by identifying points that differ by an integer multiple of `r`. The homeomorphism rescales by the ratio `p⁻¹ · q`, carrying the `p`-periodic circle continuously and bijectively onto the `q`-periodic circle.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.homeomorphAddCircle : {𝕜 : Type u_1} -> [Field 𝕜] -> (p q : 𝕜) -> [LinearOrder 𝕜] -> [IsStrictOrderedRing 𝕜] -> [TopologicalSpace 𝕜] -> [OrderTopology 𝕜] -> (hp : p ≠ 0) -> (hq : q ≠ 0) -> AddCircle p ≃ₜ AddCircle q
<!-- PINNED-SIGNATURE:END -->


VTask.homeomorphAddCircle : {𝕜 : Type u_1} -> [Field 𝕜] -> (p q : 𝕜) -> [LinearOrder 𝕜] -> [IsStrictOrderedRing 𝕜] -> [TopologicalSpace 𝕜] -> [OrderTopology 𝕜] -> (hp : p ≠ 0) -> (hq : q ≠ 0) -> AddCircle p ≃ₜ AddCircle q

The implicit type `𝕜` is the underlying ordered field. `p` is the period of the source additive circle; `q` is the period of the target additive circle. The instance arguments provide the field structure, a compatible linear order, the strict-order-ring axioms, a topological space structure, and the requirement that the topology coincides with the order topology. `hp` is the proof that the source period is nonzero (guaranteeing the source circle is nontrivial and the rescaling ratio is well-defined); `hq` is the corresponding proof for the target period.

## Conventions

There are no junk-value conventions to declare: both `p` and `q` are required to be nonzero by explicit proof arguments, so the definition is never invoked at a degenerate input.

## Worked examples

- Claim: For `p q : ℝ` with `hp : p ≠ 0` and `hq : q ≠ 0`, the forward map sends the class of `x : ℝ` in `AddCircle p` to the class of `x * (p⁻¹ * q)` in `AddCircle q`.

- Claim: For `p q : ℝ` with `hp : p ≠ 0` and `hq : q ≠ 0`, the inverse map sends the class of `x : ℝ` in `AddCircle q` to the class of `x * (q⁻¹ * p)` in `AddCircle p`.

- Claim: When `p = q`, the homeomorphism `VTask.homeomorphAddCircle p p hp hp` has the same underlying equivalence on points as the identity: the image of the class of `x` is again the class of `x` (since `p⁻¹ * p = 1` and `x * 1 = x`).

- Claim: When `p = 1` and `q = 2` in `ℝ`, the class of `0 : ℝ` in `AddCircle 1` maps to the class of `0 * (1⁻¹ * 2) = 0` in `AddCircle 2`.

## Boundaries

- The nonzero hypotheses `hp` and `hq` are essential: they ensure the rescaling factor `p⁻¹ * q` is well-defined in a field. The definition cannot be applied when either period is zero.
- The construction is symmetric in the sense that `(VTask.homeomorphAddCircle p q hp hq).symm = VTask.homeomorphAddCircle q p hq hp` (the inverse rescales by `q⁻¹ * p`).
- When `p = q`, the homeomorphism is the identity homeomorphism on `AddCircle p`.
- The result holds for any ordered field with the order topology, not just `ℝ`; for example, it applies to `ℚ` or other ordered fields with compatible topologies.

## Not to be confused with

- `AddCircle.equivAddCircle`: the underlying set-theoretic (or group-theoretic) equivalence without the bundled continuity data; `VTask.homeomorphAddCircle` is the strictly stronger, topologically richer object.
- `ContinuousMap` between additive circles: a mere continuous function, not necessarily a homeomorphism (no guaranteed continuous inverse).
- `AddCircle p` itself: the single additive circle with a fixed period, not a map between two circles.