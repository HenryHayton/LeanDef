## Object

A set `s` of points in a space `α` is **invariant** under a parameterised family of maps `ϕ : τ → α → α` if, for every parameter value `t` in `τ`, the map `ϕ t` sends every point of `s` back into `s`. In other words, `s` is closed under every member of the family: no point in `s` can be moved outside `s` by any `ϕ t`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsInvariant : {τ : Type u_1} -> {α : Type u_2} -> (ϕ : τ → α → α) -> (s : Set α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsInvariant : {τ : Type u_1} -> {α : Type u_2} -> (ϕ : τ → α → α) -> (s : Set α) -> Prop`

The type `τ` is the **parameter type** (e.g. a time variable or an index set); `α` is the **state space** whose subsets we study. The argument `ϕ` is the parameterised family of self-maps on `α` — for each `t : τ`, `ϕ t : α → α` is one member of the family. The argument `s` is the candidate **invariant set**, the subset of `α` whose invariance is being asserted.

## Conventions

No junk-value or edge conventions are declared for this definition: it is a universally quantified proposition that is well-formed for every choice of types, family, and set, including the empty set and the full set `Set.univ`, so no special boundary conventions are needed.

## Worked examples

- Claim: The empty set is invariant under every parameterised family `ϕ : τ → α → α`, because there are no points in it to map outside itself.

- Claim: The full set `Set.univ` is invariant under every parameterised family `ϕ : τ → α → α`, because every map sends points into `Set.univ` trivially.

- Claim: If `ϕ : ℕ → ℝ → ℝ` is the constant-zero family `ϕ t x = 0`, then the singleton `{0}` is invariant under `ϕ`, since `ϕ t 0 = 0 ∈ {0}` for all `t`.

- Claim: For a flow `ϕ` on a space `α`, the forward orbit `orbit ϕ x` starting at any point `x` is invariant under `ϕ`.

## Boundaries

- **Empty set**: `VTask.IsInvariant ϕ ∅` holds trivially for every `ϕ`, since the premise of `MapsTo (ϕ t) ∅ ∅` is vacuously true — there are no points to map.
- **Full set**: `VTask.IsInvariant ϕ Set.univ` holds trivially for every `ϕ`, since any point's image lands in `Set.univ`.
- **Single parameter value**: If `τ` is a one-element type, invariance reduces to a single `MapsTo` condition.
- **Relationship to forward invariance**: In a preorder with a zero element, invariance implies forward invariance. Under a canonically ordered additive monoid structure, the converse also holds.

## Not to be confused with

- **`VTask.IsForwardInvariant`**: requires the set to be mapped into itself only for *non-negative* (or *future*) parameters; strictly weaker than `VTask.IsInvariant` in general ordered settings.
- **`MulAction.IsInvariantBlock`**: a block-theoretic notion for group actions on sets, where the set is either mapped to itself or to a disjoint translate; a different invariance concept from the pointwise map-into condition here.
- **Fixed sets**: A set could be called *fixed* if every `ϕ t` fixes each individual point of `s` (i.e. `ϕ t x = x` for all `x ∈ s`); that is strictly stronger than `VTask.IsInvariant`, which only requires `ϕ t x ∈ s`.
