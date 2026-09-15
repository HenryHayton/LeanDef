## Object

A generalized loop (`GenLoop`) is a continuous map from the N-dimensional unit cube `I^N = (N → [0,1])` into a topological space `X` that sends the entire boundary of the cube to a fixed basepoint `x`. `VTask.copy` produces a new `GenLoop` whose underlying map is a given function `g`, under the guarantee that `g` equals the coercion of an existing `GenLoop` `f`. This is a bookkeeping device: the resulting element of `GenLoop N X x` is equal to `f` as a `GenLoop`, but its coercion is definitionally equal to `g`, which can be useful when rewriting along definitional equalities in proofs.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {N : Type u_1} -> {X : Type u_2} -> [TopologicalSpace X] -> {x : X} -> (f : ↑(GenLoop N X x)) -> (g : (N → ↑unitInterval) → X) -> (h : g = ⇑f) -> ↑(GenLoop N X x)
<!-- PINNED-SIGNATURE:END -->


`VTask.copy : {N : Type u_1} -> {X : Type u_2} -> [TopologicalSpace X] -> {x : X} -> (f : ↑(GenLoop N X x)) -> (g : (N → ↑unitInterval) → X) -> (h : g = ⇑f) -> ↑(GenLoop N X x)`

- `N` is the index type parametrising the cube's dimensions (implicit).
- `X` is the topological space in which the loop lives (implicit), equipped with a `TopologicalSpace` instance.
- `x` is the basepoint in `X` to which the boundary of the cube is sent (implicit).
- `f` is the original generalized loop being copied.
- `g` is the new underlying function from the unit cube to `X` that will be used in place of `f`'s coercion.
- `h` is the proof that `g` equals the coercion of `f`, ensuring that `g` inherits all the required properties (continuity and the boundary condition).

## Conventions

There are no junk-value or edge conventions declared for this definition: the function is total and well-defined whenever the three arguments `f`, `g`, and `h` are provided — the proof `h` completely constrains the admissible inputs so no degenerate case arises.

## Worked examples

- Claim: For any `GenLoop f`, calling `VTask.copy f (⇑f) rfl` yields a `GenLoop` whose coercion is exactly `⇑f` (i.e., `coe_copy` holds: `⇑(VTask.copy f g h) = g`).

- Claim: For any `GenLoop f`, `VTask.copy f (⇑f) rfl` is equal to `f` as a `GenLoop` (i.e., `copy_eq` holds: `VTask.copy f (⇑f) rfl = f`).

- Claim: If `g` and `h : g = ⇑f` are given, then the result `VTask.copy f g h` is a valid member of `GenLoop N X x`, meaning its underlying map sends the boundary of the cube to the basepoint `x`.

## Boundaries

- The only admissible input for `g` (given `f`) is a function propositionally equal to `⇑f`; the proof `h` enforces this and there is no case where `g` could differ from `f`'s coercion.
- When `g = ⇑f` and `h = rfl`, the copy is trivially equal to `f` and its coercion is definitionally `⇑f`.
- The definition is total: as long as `h : g = ⇑f` is provided, the result is always a well-formed `GenLoop`.

## Not to be confused with

- `GenLoop` itself: the subtype of maps `I^N → X` sending the boundary to `x`; `VTask.copy` merely constructs a new such element, it is not the type definition.
- Homotopy of generalized loops: `VTask.copy` does not produce a homotopy between `f` and anything; it is a strict equality of `GenLoop` values.
- `ContinuousMap.copy` or similar coercion-fixing lemmas: analogous constructions exist for plain continuous maps, but `VTask.copy` additionally enforces the basepoint boundary condition specific to `GenLoop`.