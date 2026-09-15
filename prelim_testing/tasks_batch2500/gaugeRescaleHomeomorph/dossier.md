## VTask.gaugeRescaleHomeomorph

### Object

This is a self-homeomorphism of a real topological vector space `E`, constructed from two sets `s` and `t` that are each convex, contain a neighbourhood of the origin, and are von Neumann bounded. The map rescales each point by the ratio of the Minkowski gauge (Minkowski functional) of `s` to that of `t`, sending `s`-level sets to `t`-level sets in a continuous, bijective, and continuously invertible fashion. In particular it carries the interior of `s` homeomorphically onto the interior of `t`, and the closure of `s` homeomorphically onto the closure of `t`. Since both sets are equivalent via this rescaling, the construction shows that any two such "balanced convex bodies" in `E` are topologically the same.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.gaugeRescaleHomeomorph : {E : Type u_1} -> [AddCommGroup E] -> [Module ℝ E] -> [TopologicalSpace E] -> [IsTopologicalAddGroup E] -> [ContinuousSMul ℝ E] -> [T1Space E] -> (s t : Set E) -> (hsc : Convex ℝ s) -> (hs₀ : s ∈ nhds 0) -> (hsb : Bornology.IsVonNBounded ℝ s) -> (htc : Convex ℝ t) -> (ht₀ : t ∈ nhds 0) -> (htb : Bornology.IsVonNBounded ℝ t) -> E ≃ₜ E
<!-- PINNED-SIGNATURE:END -->


`{E : Type u_1} -> [AddCommGroup E] -> [Module ℝ E] -> [TopologicalSpace E] -> [IsTopologicalAddGroup E] -> [ContinuousSMul ℝ E] -> [T1Space E] -> (s t : Set E) -> (hsc : Convex ℝ s) -> (hs₀ : s ∈ nhds 0) -> (hsb : Bornology.IsVonNBounded ℝ s) -> (htc : Convex ℝ t) -> (ht₀ : t ∈ nhds 0) -> (htb : Bornology.IsVonNBounded ℝ t) -> E ≃ₜ E`

The implicit type class arguments supply the algebraic and topological structure on the ambient space `E`: it is a real vector space equipped with a compatible topological group structure, continuous scalar multiplication, and the T1 separation axiom.

The argument `s` is the *source* convex body: the set whose gauge functional is used in the numerator of the rescaling ratio. The argument `t` is the *target* convex body.

`hsc` witnesses that `s` is convex over the reals. `hs₀` witnesses that `s` is a neighbourhood of the origin (equivalently, `0 ∈ interior s`). `hsb` witnesses that `s` is von Neumann bounded, i.e., every neighbourhood of 0 absorbs `s`.

Analogously, `htc`, `ht₀`, and `htb` are the same three hypotheses for the target set `t`.

The return type `E ≃ₜ E` is a homeomorphism from `E` to itself (a self-homeomorphism of the underlying topological space).

### Conventions

There are no junk-value conventions to declare: the definition is total over its stated domain — every combination of inputs satisfying the explicitly required hypotheses (convexity, neighbourhood of 0, and von Neumann boundedness for each of `s` and `t`) yields a well-defined homeomorphism. No distinguished behaviour is defined outside that domain.

### Worked examples

- Claim: The image of the closure of `s` under `VTask.gaugeRescaleHomeomorph s t hsc hs₀ hsb htc ht₀ htb` equals the closure of `t`.

- Claim: The image of the interior of `s` under `VTask.gaugeRescaleHomeomorph s t hsc hs₀ hsb htc ht₀ htb` equals the interior of `t`.

- Claim: When `s = t` (with the same hypotheses), `VTask.gaugeRescaleHomeomorph s s hsc hs₀ hsb hsc hs₀ hsb` maps every point in the interior of `s` to itself, because the gauge ratio is identically 1 on the interior.

- Claim: In `ℝ` with `s = Set.Ioo (-1) 1` and `t = Set.Ioo (-2) 2` (both convex, 0-neighbourhoods, and bounded), `VTask.gaugeRescaleHomeomorph s t ...` sends any `x : ℝ` to `2 * x`, reflecting the doubling of the gauge ratio.

### Boundaries

- At the origin `0 : E`, the gauge of any absorbing set vanishes, so the rescaling map sends `0` to `0`; the homeomorphism fixes the origin.
- For points on the *boundary* of `s` (gauge value 1), the map sends them to points on the boundary of `t`.
- The hypotheses `hs₀` and `ht₀` (neighbourhoods of 0) are essential: without them the Minkowski gauge might be identically 0 on a large set and the map would fail to be injective.
- The von Neumann boundedness conditions `hsb` and `htb` ensure the gauges are continuous and everywhere finite and positive away from 0, which is what guarantees the inverse is also continuous.
- If `E` is finite-dimensional, every convex body with 0 in its interior is automatically von Neumann bounded, so `hsb`/`htb` are automatic; in infinite dimensions they must be checked.

### Not to be confused with

- `gaugeRescaleEquiv` — the underlying set-theoretic equivalence (bijection) between `E` and itself from which this homeomorphism is built; it lacks the bundled continuity data.
- The gauge (Minkowski functional) `gauge s` itself — a real-valued function on `E`, not a self-map of `E`.
- Linear isomorphisms between `E` and itself — `VTask.gaugeRescaleHomeomorph` is generally not linear; it is a nonlinear, radially defined rescaling.
