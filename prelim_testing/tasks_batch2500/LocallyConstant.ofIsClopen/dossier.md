## VTask.ofIsClopen

### Object

Given a topological space `X` and a clopen subset `U ⊆ X`, this is the locally constant function `X → Fin 2` that sends every point of `U` to `0` and every point of the complement `Uᶜ` to `1`. It is the characteristic (indicator) function of `U` valued in the two-element set `{0, 1}`, packaged together with the proof that it is locally constant — a consequence of `U` being both open and closed.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofIsClopen : {X : Type u_5} -> [TopologicalSpace X] -> {U : Set X} -> [(x : X) → Decidable (x ∈ U)] -> (hU : IsClopen U) -> LocallyConstant X (Fin 2)
<!-- PINNED-SIGNATURE:END -->


The implicit argument `X` is the underlying topological space. The instance `[TopologicalSpace X]` supplies the topology. The implicit argument `U` is the clopen subset of `X` whose characteristic function is being constructed. The instance `[∀ x, Decidable (x ∈ U)]` provides the decidability of membership in `U` needed to define the indicator function computably. The explicit argument `hU : IsClopen U` is the proof that `U` is simultaneously open and closed in `X`.

### Conventions

Points in `U` map to `0 : Fin 2`, while points outside `U` (i.e., in `Uᶜ`) map to `1 : Fin 2`. This is the opposite of the usual {0,1}-indicator convention (where membership gives 1), and the choice is fixed by the definition.

### Worked examples

- Claim: For the clopen set `U = Set.univ` in any topological space, `VTask.ofIsClopen hU` sends every point to `0`.

- Claim: For the clopen set `U = ∅` in any topological space, `VTask.ofIsClopen hU` sends every point to `1`.

- Claim: The fiber over `0` of `VTask.ofIsClopen hU` equals `U` (i.e., `VTask.ofIsClopen hU ⁻¹' {0} = U`).

- Claim: The fiber over `1` of `VTask.ofIsClopen hU` equals `Uᶜ` (i.e., `VTask.ofIsClopen hU ⁻¹' {1} = Uᶜ`).

### Boundaries

- When `U = Set.univ`, the function is the constant `0` map, which is trivially locally constant.
- When `U = ∅`, the function is the constant `1` map, which is trivially locally constant.
- The construction is well-typed for any `IsClopen U`, including degenerate cases such as a discrete or indiscrete topology, as long as membership in `U` is decidable.
- Since `Fin 2` has exactly two elements, every locally constant function `X → Fin 2` arises in this way from a clopen set.

### Not to be confused with

- The ordinary indicator function `Set.indicator`: that is a function to a general monoid (typically `ℕ` or `ℝ`) and is not packaged as a `LocallyConstant`, nor does it require clopenness.
- `LocallyConstant.const`: that constructs a globally constant locally constant function with a fixed value, not a two-valued characteristic function of a subset.
- `ContinuousMap.ofIsClopen` (if it existed): `VTask.ofIsClopen` produces a `LocallyConstant`, which carries strictly more structure than a mere continuous map.