## Object

`VTask.ofNormedAddCommGroup` packages a continuous function `f : α → β`, where `β` is a seminormed additive commutative group, together with a uniform norm bound into a *bounded continuous function* — an element of the type `α →ᵇ β` that simultaneously records continuity and the boundedness of the map in the metric sense.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofNormedAddCommGroup : {α : Type u} -> {β : Type v} -> [TopologicalSpace α] -> [SeminormedAddCommGroup β] -> (f : α → β) -> (Hf : Continuous f) -> (C : ℝ) -> (H : ∀ (x : α), ‖f x‖ ≤ C) -> BoundedContinuousFunction α β
<!-- PINNED-SIGNATURE:END -->


`{α : Type u} -> {β : Type v} -> [TopologicalSpace α] -> [SeminormedAddCommGroup β] -> (f : α → β) -> (Hf : Continuous f) -> (C : ℝ) -> (H : ∀ (x : α), ‖f x‖ ≤ C) -> BoundedContinuousFunction α β`

The implicit type `α` is the domain; it carries a topology supplied by the `TopologicalSpace` instance. The implicit type `β` is the codomain; it carries both a topology and a norm supplied by the `SeminormedAddCommGroup` instance. The argument `f` is the underlying function to be packaged. The argument `Hf` is a proof that `f` is continuous with respect to the topologies on `α` and `β`. The argument `C` is a proposed uniform upper bound for the norm of the function's values — it need not be tight or non-negative, only a valid bound. The argument `H` is a proof that `‖f x‖ ≤ C` holds for every point `x` in `α`, witnessing that `f` is uniformly bounded in norm.

## Conventions

The bound `C` supplied by the caller is not required to be non-negative; any real number larger than all `‖f x‖` is acceptable, and the construction is still valid. The coercion of the resulting `BoundedContinuousFunction` back to a plain function recovers exactly `f`, with no modification to values.

## Worked examples

- Claim: When `f : ℝ → ℝ` is the zero function, `VTask.ofNormedAddCommGroup f (continuous_const) 0 (fun x => le_refl 0)` produces a bounded continuous function whose underlying map is identically zero.

- Claim: When `f : ℝ → ℝ` is the constant function `fun _ => 1`, providing `C = 1` and the proof `fun x => le_refl 1`, the resulting bounded continuous function has norm at most `1`.

- Claim: The coercion of `VTask.ofNormedAddCommGroup f Hf C H` to a function `α → β` equals `f` definitionally for any admissible inputs.

## Boundaries

- If `C` is negative but no `x` satisfies `‖f x‖ ≤ C` in practice, then `H` cannot be proved and the construction cannot be applied; however, the constructor itself places no syntactic restriction on `C` being non-negative.
- The norm bound stored internally in the resulting `BoundedContinuousFunction` may be larger than `C`; specifically the internal bound is at most `2 * C` (or a similar constant multiple), but the coercion to function is unchanged.
- The domain `α` need not be compact, non-empty, or metrizable; any topological space is accepted.
- The seminorm on `β` may degenerate (i.e., `‖x‖ = 0` for non-zero `x`); the construction remains valid.

## Not to be confused with

- `BoundedContinuousFunction.ofNormedAddCommGroupDiscrete`: a variant for domains with the discrete topology that does not require an explicit continuity proof `Hf`, since every function is continuous there.
- `ContinuousMap.mk`: constructs a plain continuous map without bundling a boundedness witness; the result is not a `BoundedContinuousFunction`.
- `BoundedContinuousFunction.mkOfBound`: an alternative constructor that works with a bound on the metric distance between values, rather than a pointwise norm bound.