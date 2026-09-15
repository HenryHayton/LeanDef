## Object

Given a function `f : X → Y` and a topology on `Y`, the **induced topology** on `X` is the topology whose open sets are exactly the preimages under `f` of open sets in `Y`. It is the coarsest (smallest) topology on `X` that makes `f` continuous: any topology on `X` making `f` continuous must be at least as fine as the induced topology.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.induced : {X : Type u_1} -> {Y : Type u_2} -> (f : X → Y) -> (t : TopologicalSpace Y) -> TopologicalSpace X
<!-- PINNED-SIGNATURE:END -->


`VTask.induced : {X : Type u_1} -> {Y : Type u_2} -> (f : X → Y) -> (t : TopologicalSpace Y) -> TopologicalSpace X`

The type variables `X` and `Y` are the domain and codomain types, inferred implicitly. The argument `f` is the function along which the topology is pulled back; it determines which subsets of `X` count as open. The argument `t` is the topology on `Y` from which open sets are drawn; a subset `U ⊆ Y` is open in the sense of `t`, and its preimage `f⁻¹(U)` is then declared open in `X`.

## Conventions

The construction is total and well-defined for every function and every topology on the codomain; there are no junk-value conventions to declare.

## Worked examples

- Claim: If `f : X → Y` is any function and `t` is the discrete topology on `Y`, then every subset of `X` is open in `VTask.induced f t`, because every subset of `Y` is open and every subset of `X` arises as a preimage.

- Claim: For the inclusion `f : ℝ → ℝ²` sending `x` to `(x, 0)`, the induced topology on `ℝ` is the standard Euclidean topology on `ℝ`, because open balls in `ℝ²` pull back to open intervals in `ℝ`.

- Claim: The neighborhood filter of a point `x : X` in `VTask.induced f t` equals the comap of `f` applied to the neighborhood filter of `f x` in `t`; symbolically `𝓝 x = comap f (𝓝 (f x))`.

- Claim: For any two topologies `t₁` and `t₂` on `Y` with `t₁ ≤ t₂`, we have `VTask.induced f t₁ ≤ VTask.induced f t₂`, i.e., the induced topology is monotone in the topology on `Y`.

- Claim: Composing inductions: `VTask.induced (g ∘ f) t = VTask.induced f (VTask.induced g t)` for composable functions `f : X → Y` and `g : Y → Z` and a topology `t` on `Z`.

## Boundaries

- If `f` is the constant function (sending everything to a single point `y₀`), the induced topology on `X` is the indiscrete topology: the only open sets are `∅` and `X`, since only `∅` and `Y` are preimages of open sets whose preimage covers extremes.
- If `f` is surjective, the induced topology is still well-defined but need not equal any familiar topology unless additional structure is present.
- If `t` is the indiscrete topology on `Y` (only `∅` and `Y` are open), then `VTask.induced f t` is also indiscrete on `X`, since the only preimages are `∅` and `X`.
- If `f` is a homeomorphism (a continuous bijection with continuous inverse), then `VTask.induced f t` coincides with the topology on the domain, reflecting the fact that homeomorphisms preserve the full topological structure.
- The whole space `X` is always open in `VTask.induced f t` (it is the preimage of `Y`), and the empty set is always open (it is the preimage of `∅`), so the axioms are automatically satisfied.

## Not to be confused with

- `TopologicalSpace.coinduced`: the **coinduced** (quotient/pushforward) topology going the other direction — the finest topology on `Y` making `f` continuous, constructed from images rather than preimages.
- `TopologicalSpace.inf`: the infimum of two topologies on the same type, which also produces a coarser topology but is not defined via a single pullback function.
- `UniformSpace.comap`: the analogous pullback for uniform spaces; its underlying topology equals `VTask.induced f` applied to the underlying topology of the uniform space, but the two objects live in different categories.