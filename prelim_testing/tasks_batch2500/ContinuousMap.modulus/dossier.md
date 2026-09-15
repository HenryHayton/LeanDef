## Object

Given a continuous map `f` between compact pseudo-metric spaces and a positive real number `ε`, `VTask.modulus f ε h` is a specific positive real number `δ` such that whenever two points of the domain are within distance `δ` of each other, their images under `f` are within distance `ε` of each other. In other words, it is an arbitrarily (but definitively) chosen modulus of uniform continuity for `f` at tolerance `ε`. Its existence is guaranteed by the fact that every continuous map from a compact pseudo-metric space to a pseudo-metric space is uniformly continuous.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.modulus : {α : Type u_1} -> {β : Type u_2} -> [PseudoMetricSpace α] -> [CompactSpace α] -> [PseudoMetricSpace β] -> (f : C(α, β)) -> (ε : ℝ) -> (h : 0 < ε) -> ℝ
<!-- PINNED-SIGNATURE:END -->


The first implicit argument is the domain type `α`, which must carry the structure of a compact pseudo-metric space. The second implicit argument is the codomain type `β`, which must carry the structure of a pseudo-metric space. The argument `f` is the continuous map whose uniform continuity is being witnessed. The argument `ε` is the prescribed output tolerance — a real number representing the maximum allowable distance between image points. The argument `h` is a proof that `ε` is strictly positive, ensuring the tolerance is meaningful.

## Conventions

The value `VTask.modulus f ε h` is a classically chosen real number; its exact value is not determined by any constructive rule, only by the existence of a uniform continuity witness. The result is always strictly positive, because any valid modulus of uniform continuity must be positive. The choice is fixed (deterministic in any given logical environment) but opaque: one should not assume any specific numerical value for the result beyond what can be proved from the uniform continuity specification it satisfies.

## Worked examples

- Claim: For any compact pseudo-metric space `α`, any pseudo-metric space `β`, any continuous map `f : C(α, β)`, and any `ε > 0`, the chosen modulus `VTask.modulus f ε h` is strictly positive.

- Claim: For any compact pseudo-metric space `α`, any pseudo-metric space `β`, any `f : C(α, β)`, and `ε > 0` with proof `h`, and any two points `x y : α` satisfying `dist x y < VTask.modulus f ε h`, we have `dist (f x) (f y) < ε`.

## Boundaries

The argument `ε` must be strictly positive (enforced by the proof `h : 0 < ε`); there is no meaningful notion of a modulus of uniform continuity for a non-positive tolerance. The compactness of the domain `α` is essential: without it, uniform continuity is not guaranteed for all continuous functions, and the existence of the modulus cannot be asserted in general. If `α` is empty or a singleton, the modulus is still well-defined (and any positive real would serve), but the chosen value remains opaque. The definition produces a real number, not a natural number or rational approximation.

## Not to be confused with

- The modulus of continuity at a point (a local notion), which only controls behavior near a single point rather than uniformly across all of `α`.
- The modulus of continuity as a function of `ε` (the supremal `δ` for a given `ε`), which is the canonical/optimal choice rather than an arbitrary classical choice.
- `dist`-based bounds obtained directly from `UniformContinuous` or `Metric.uniformContinuous_iff`, which provide existential witnesses rather than a fixed chosen value.