## Object

A set `s` in a space `α` is **forward-invariant** under a map `ϕ : τ → α → α` (thought of as a flow or semi-flow parameterised by a "time" type `τ`) if, whenever `t ≥ 0`, every point of `s` that is evolved by `ϕ t` remains inside `s`. In other words, the set cannot be escaped in non-negative time: if you start inside `s` and let the system run forward, you stay inside `s`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsForwardInvariant : {τ : Type u_1} -> {α : Type u_2} -> [Preorder τ] -> [Zero τ] -> (ϕ : τ → α → α) -> (s : Set α) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.IsForwardInvariant : {τ : Type u_1} -> {α : Type u_2} -> [Preorder τ] -> [Zero τ] -> (ϕ : τ → α → α) -> (s : Set α) -> Prop
```

The implicit type `τ` is the "time" parameter type, which must carry a preorder and a distinguished zero element. The implicit type `α` is the phase space. The instance `[Preorder τ]` supplies the ordering used to express the condition `t ≥ 0`, and `[Zero τ]` supplies the reference point `0` ("initial time"). The argument `ϕ` is the flow or evolution operator: `ϕ t x` is the state reached from `x` after time `t`. The argument `s` is the subset of `α` whose forward invariance is being asserted.

## Conventions

No special junk-value or edge conventions are declared for this predicate: it is a universally quantified statement over all `t ≥ 0`, so the case `t = 0` is included but imposes no independent constraint beyond whatever `ϕ 0` does (it need not be the identity unless additional axioms are assumed). The predicate is total and well-defined for any `ϕ` and `s`.

## Worked examples

- Claim: For the constant flow `ϕ t x = x` on any type, every set is forward-invariant under `ϕ`.

- Claim: The empty set is forward-invariant under any flow `ϕ`, because there are no points to map and `MapsTo (ϕ t) ∅ ∅` holds vacuously for every `t`.

- Claim: The full set `Set.univ` is forward-invariant under any flow `ϕ`, because `ϕ t x ∈ Set.univ` for every `x` and every `t ≥ 0`.

- Claim: If `ϕ` is a flow (in the sense of Mathlib's `Flow`) and `x : α`, then `VTask.IsForwardInvariant ϕ (Set.range (fun t => ϕ t x))` holds when `τ` admits the relevant structure, since the forward orbit of `x` is forward-invariant.

## Boundaries

- When `τ` has a preorder in which every element satisfies `t ≥ 0` (e.g. `τ = ℕ` with its natural order), the condition reduces to "for all `t : τ`, `ϕ t` maps `s` into `s`", which is exactly full invariance.
- When `τ = ℤ` with the usual order, `t ≥ 0` excludes negative times, so forward invariance is strictly weaker than full (two-sided) invariance.
- The empty set `∅ ⊆ α` is always forward-invariant (vacuously).
- The whole space `Set.univ` is always forward-invariant.
- Full invariance (`IsInvariant`) implies forward invariance. Conversely, in contexts where `τ` is a canonically ordered additive monoid, forward invariance implies full invariance.

## Not to be confused with

- **`IsInvariant ϕ s`** — asserts that `ϕ t` maps `s` into `s` for *all* `t : τ`, not just those with `t ≥ 0`; this is a strictly stronger condition when negative times are present.
- **`IsBackwardInvariant ϕ s`** — the analogous condition for `t ≤ 0`, requiring the set to be invariant when time runs backward.
- **`forwardOrbit ϕ x`** — this is a *set* (the forward orbit of a single point), not a predicate; it is the canonical example of a forward-invariant set, but the two concepts should not be conflated.