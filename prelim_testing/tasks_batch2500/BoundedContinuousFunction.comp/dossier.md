## VTask.comp

### Object

Given a Lipschitz map `G : β → γ` between pseudo-metric spaces and a bounded continuous function `f : α → β` (where `α` is a topological space), `VTask.comp G H f` is the bounded continuous function `α → γ` obtained by composing `f` with `G` in the target, i.e., the function `x ↦ G(f(x))`. The Lipschitz condition on `G` ensures that the composition inherits both continuity (from Lipschitz implies continuous) and boundedness (the Lipschitz constant multiplied by the existing diameter bound gives a new diameter bound).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {α : Type u} -> {β : Type v} -> {γ : Type w} -> [TopologicalSpace α] -> [PseudoMetricSpace β] -> [PseudoMetricSpace γ] -> (G : β → γ) -> {C : NNReal} -> (H : LipschitzWith C G) -> (f : BoundedContinuousFunction α β) -> BoundedContinuousFunction α γ
<!-- PINNED-SIGNATURE:END -->


`VTask.comp : {α : Type u} -> {β : Type v} -> {γ : Type w} -> [TopologicalSpace α] -> [PseudoMetricSpace β] -> [PseudoMetricSpace γ] -> (G : β → γ) -> {C : NNReal} -> (H : LipschitzWith C G) -> (f : BoundedContinuousFunction α β) -> BoundedContinuousFunction α γ`

The implicit type arguments `α`, `β`, `γ` are the domain, intermediate, and codomain types. The topological space instance on `α` and pseudo-metric space instances on `β` and `γ` supply the necessary structure. `G` is the Lipschitz map applied in the target; `C` is its (implicit) Lipschitz constant, and `H` is the proof that `G` is Lipschitz with constant `C`. Finally, `f` is the bounded continuous function from `α` to `β` being composed.

### Conventions

The Lipschitz constant `C` is a non-negative real number (`NNReal`), so no sign condition needs to be asserted separately. The boundedness bound for the composition is derived from `C` and the existing bound on `f`; no junk or default values arise for well-typed inputs.

### Worked examples

- Claim: For any bounded continuous function `f : BoundedContinuousFunction α β`, evaluating `VTask.comp G H f` at a point `a` gives `G (f a)`.

- Claim: When `G` is the identity map on `β` (which is Lipschitz with constant 1), `VTask.comp G H f` is pointwise equal to `f` for every input.

- Claim: If `G : ℝ → ℝ` is multiplication by 2 (Lipschitz with constant 2) and `f : BoundedContinuousFunction α ℝ` has supremum norm at most `M`, then the composition `VTask.comp G H f` has values `2 * f(x)` at each point `x`.

- Claim: The induced map `VTask.comp G H : BoundedContinuousFunction α β → BoundedContinuousFunction α γ` is itself Lipschitz (with the same constant `C`) as a map between the bounded-continuous-function spaces equipped with the sup-norm metric.

### Boundaries

- If `C = 0`, then `G` is a constant map (Lipschitz with constant 0), so the composition is the constant bounded continuous function with that constant value, and the bound on `VTask.comp G H f` is 0.
- The domain `α` need only be a topological space (not a metric space), so the construction works even when `α` has no metric structure.
- If `f` is already the zero function (or any constant), the composition is the corresponding constant function, still a valid bounded continuous function.
- The construction is total: every well-typed triple `(G, H, f)` yields a bounded continuous function; there are no inputs for which the result is undefined.

### Not to be confused with

- `BoundedContinuousFunction.compContinuous`: this composes in the *domain* (precomposing with a continuous map `g : γ → α`), whereas `VTask.comp` composes in the *target* with a Lipschitz map.
- `ContinuousMap.comp`: the analogous composition for plain continuous maps, which does not track boundedness or Lipschitz constants.
- `ContinuousLinearMap.compLeftContinuousBounded`: a version of target-composition restricted to continuous *linear* maps between normed spaces, rather than general Lipschitz maps between pseudo-metric spaces.