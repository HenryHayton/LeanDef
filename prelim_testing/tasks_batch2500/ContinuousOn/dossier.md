## Object

A predicate asserting that a function between topological spaces is continuous when restricted to a given subset. Concretely, the function must be continuous at each point of the subset, where continuity is measured relative to the subspace topology induced by that same subset (i.e., only considering limits along sequences or nets that stay within the subset).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ContinuousOn : {X : Type u_1} -> {Y : Type u_2} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> (f : X → Y) -> (s : Set X) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.ContinuousOn : {X : Type u_1} -> {Y : Type u_2} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> (f : X → Y) -> (s : Set X) -> Prop`

The implicit type arguments `X` and `Y` are the domain and codomain types, respectively. The topological space instances supply the topologies on `X` and `Y`. The explicit argument `f` is the function whose continuity is being assessed. The argument `s` is the subset of `X` on which continuity is required.

## Conventions

No special junk-value or boundary conventions are declared for this predicate: it is a universally quantified statement over `s`, so when `s` is empty the predicate holds vacuously (there are no points to check), and no distinguished default value needs to be assigned.

## Worked examples

- Claim: `VTask.ContinuousOn id s` holds for any topological space `X` and any subset `s : Set X`, because the identity function is continuous everywhere.

- Claim: `VTask.ContinuousOn (fun _ => c) s` holds for any constant function (with value `c : Y`) and any subset `s`, because a constant function is continuous at every point within any set.

- Claim: If `f : X → Y` is globally continuous (i.e., `Continuous f` holds), then `VTask.ContinuousOn f s` holds for every subset `s : Set X`.

- Claim: `VTask.ContinuousOn f ∅` holds for any function `f`, because the universal quantification over the empty set is vacuously true.

## Boundaries

- **Empty set**: When `s = ∅`, the predicate is vacuously true for every function `f`, since there are no points in `s` at which to check continuity.
- **Full space**: When `s = Set.univ`, the predicate asserts continuity at every point with respect to the full topology, which is equivalent to global continuity of `f`.
- **Singleton set**: When `s = {x₀}`, the predicate holds if and only if `f` is continuous at `x₀` within `{x₀}`. Because the only net in a singleton stays at `x₀`, the filter condition is trivially satisfied, so the predicate holds for every function.
- **Restriction vs. global continuity**: `VTask.ContinuousOn f s` is strictly weaker than `Continuous f`; a function can be continuous on a proper subset without being globally continuous.

## Not to be confused with

- **`Continuous f`**: Global continuity of `f` on all of `X`; this is strictly stronger than `VTask.ContinuousOn f s` for proper subsets `s`.
- **`ContinuousWithinAt f s x`**: The pointwise version — continuity of `f` at a single point `x` within `s`. `VTask.ContinuousOn f s` is exactly the assertion that `ContinuousWithinAt f s x` holds for every `x ∈ s`.
- **`ContinuousAt f x`**: Continuity at a point `x` with respect to the full ambient topology of `X`, not just the subspace topology of `s`. It is stronger than `ContinuousWithinAt f s x` when `s` is not a neighbourhood of `x`.