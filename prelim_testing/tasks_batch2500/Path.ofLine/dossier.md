## Object

`VTask.ofLine` constructs a `Path x y` — a continuous map from the unit interval `[0,1]` to a topological space `X`, with prescribed start point `x` and end point `y` — by restricting a given continuous function `f : ℝ → X` to the unit interval `[0,1] ⊆ ℝ`. The result is a genuine path object whose underlying function is the restriction of `f`, whose continuity is inherited from the hypothesis that `f` is continuous on `[0,1]`, and whose endpoint conditions are supplied directly.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofLine : {X : Type u_1} -> [TopologicalSpace X] -> {x y : X} -> {f : ℝ → X} -> (hf : ContinuousOn f unitInterval) -> (h₀ : f 0 = x) -> (h₁ : f 1 = y) -> Path x y
<!-- PINNED-SIGNATURE:END -->


`{X : Type u_1} -> [TopologicalSpace X] -> {x y : X} -> {f : ℝ → X} -> (hf : ContinuousOn f unitInterval) -> (h₀ : f 0 = x) -> (h₁ : f 1 = y) -> Path x y`

`X` is the target topological space (implicit), equipped with a topology via the typeclass argument. `x` and `y` are the start and end points of the path (both implicit, inferred from the endpoint proofs). `f` is the real-valued function being restricted (implicit, inferred from `hf`). `hf` is the proof that `f` is continuous on the closed unit interval `[0,1] ⊆ ℝ`. `h₀` is the proof that `f` sends `0` to the start point `x`. `h₁` is the proof that `f` sends `1` to the end point `y`.

## Conventions

The underlying function of the resulting path at a point `t : unitInterval` equals `f` applied to the coercion of `t` to `ℝ`; in other words, the path is literally `f` restricted to `[0,1]` and no extension or reparametrisation takes place.

## Worked examples

- Claim: For the constant function `f = fun _ => x`, `VTask.ofLine` yields a path whose value at every `t` is `x`, since `f 0 = x` and `f 1 = x` and `f` is continuous everywhere.

- Claim: For any existing path `γ : Path x y`, applying `VTask.ofLine` to the extension `γ.extend` (which is continuous on all of `ℝ`) with endpoint proofs `extend_zero γ` and `extend_one γ` recovers exactly `γ`; this is the content of `Path.ofLine_extend`.

- Claim: For every `t : unitInterval`, the value `(VTask.ofLine hf h₀ h₁) t` lies in the image `f '' unitInterval`; this follows immediately from the definition since the path evaluates `f` at the coercion of `t`, and `t` is by definition in `unitInterval`.

## Boundaries

- The function `f` need only be continuous on the closed unit interval; its behaviour outside `[0,1]` is irrelevant and completely ignored by `VTask.ofLine`.
- The endpoint proofs `h₀ : f 0 = x` and `h₁ : f 1 = y` must be provided explicitly; Lean does not infer them from `hf`.
- There is no requirement that `f` be defined or well-behaved at any point outside `[0,1]`; `ContinuousOn f unitInterval` is sufficient.
- When `x = y` and `f` is the constant `x`, the result is a trivial (constant) loop, not distinguished from any other constant path at `x`.

## Not to be confused with

- `Path.extend`: this extends a path `γ : Path x y` (defined on `[0,1]`) to all of `ℝ` by clamping, going in the opposite direction.
- `Path.mk`: the raw constructor for `Path x y`, which requires the underlying function to already be defined on `unitInterval` directly rather than as the restriction of a map on `ℝ`.
- `ContinuousMap.restrict`: a general restriction of a continuous map to a subtype, which does not carry the path endpoint data or produce a `Path` type.