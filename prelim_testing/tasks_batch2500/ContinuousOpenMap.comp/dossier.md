## Object

`VTask.comp f g` is the composite of two continuous open maps. Given continuous open maps `g : α →CO β` and `f : β →CO γ`, their composition is the function `f ∘ g : α → γ`, packaged as a continuous open map from `α` to `γ`. It is the categorical composition in the category of topological spaces and continuous open maps.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {α : Type u_2} -> {β : Type u_3} -> {γ : Type u_4} -> [TopologicalSpace α] -> [TopologicalSpace β] -> [TopologicalSpace γ] -> (f : β →CO γ) -> (g : α →CO β) -> α →CO γ
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_2} -> {β : Type u_3} -> {γ : Type u_4} -> [TopologicalSpace α] -> [TopologicalSpace β] -> [TopologicalSpace γ] -> (f : β →CO γ) -> (g : α →CO β) -> α →CO γ`

The type arguments `α`, `β`, `γ` are the source, intermediate, and target topological spaces, respectively; they are inferred implicitly. The three `TopologicalSpace` instances supply the topologies on those spaces and are found automatically. The first explicit argument `f` is the outer continuous open map (from `β` to `γ`); the second explicit argument `g` is the inner continuous open map (from `α` to `β`). The result is the composite continuous open map from `α` to `γ`.

## Conventions

No special junk-value or edge-case conventions are declared: the definition is total and its behaviour is entirely determined by the standard composition of functions, with no boundary or default cases.

## Worked examples

- Claim: For any continuous open maps `g : α →CO β` and `f : β →CO γ`, the underlying function of `VTask.comp f g` at a point `x : α` equals `f (g x)`.

- Claim: If `f` and `g` are both the identity continuous open map on a space `α`, then `VTask.comp f g` is also the identity continuous open map, i.e., it sends every point to itself.

- Claim: For continuous open maps `h : γ →CO δ`, `f : β →CO γ`, `g : α →CO β`, the composites `VTask.comp (VTask.comp h f) g` and `VTask.comp h (VTask.comp f g)` agree as functions on all points of `α` (associativity of composition).

## Boundaries

- When either `f` or `g` is a constant map (if such a map happens to be open, e.g., on certain spaces), the composite is the corresponding constant map.
- The composition of identity maps yields an identity map.
- The openness of the composite is guaranteed by the fact that both maps individually preserve open sets: the image of an open set under `g` is open in `β`, and then its image under `f` is open in `γ`.
- The definition is total: it is defined for all valid continuous open maps `f` and `g` with matching intermediate type `β`.

## Not to be confused with

- `ContinuousMap.comp`: composition of merely continuous maps (not required to be open), yielding a `ContinuousMap` rather than a `ContinuousOpenMap`.
- `OpenEmbedding.comp` or `IsOpenMap.comp`: results about composing the *property* of being an open map at the level of bare functions, rather than constructing a bundled `ContinuousOpenMap`.
- `ContinuousLinearMap.comp`: composition of continuous linear maps in a linear-algebraic setting, which carries additional algebraic structure beyond topology.