## Object

`VTask.sigma` assembles a single continuous map out of a topological disjoint union (sigma type) from a family of continuous maps, one for each index. Concretely, given an index type `I`, a family of topological spaces `X i` indexed by `I`, a target topological space `A`, and a continuous map `f i : X i → A` for each `i`, it produces a continuous map `(Σ i, X i) → A` that sends a pair `⟨i, x⟩` to `f i x`. The sigma type `Σ i, X i` carries the disjoint-union topology (the coproduct topology), so the assembled map is automatically continuous.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sigma : {I : Type u_5} -> {A : Type u_6} -> {X : I → Type u_7} -> [TopologicalSpace A] -> [(i : I) → TopologicalSpace (X i)] -> (f : (i : I) → C(X i, A)) -> C((i : I) × X i, A)
<!-- PINNED-SIGNATURE:END -->


`VTask.sigma : {I : Type u_5} -> {A : Type u_6} -> {X : I → Type u_7} -> [TopologicalSpace A] -> [(i : I) → TopologicalSpace (X i)] -> (f : (i : I) → C(X i, A)) -> C((i : I) × X i, A)`

- `I` is the index type whose elements label the individual summands of the disjoint union.
- `A` is the common target topological space into which every component map maps.
- `X` is the family of topological spaces forming the summands, one for each index `i : I`.
- The `TopologicalSpace A` instance supplies the topology on the target.
- The `(i : I) → TopologicalSpace (X i)` instance supplies a topology on each summand.
- `f` is the family of continuous maps: for each index `i`, `f i` is a continuous map from `X i` to `A`.

The output is a continuous map from the sigma type (disjoint union) `(i : I) × X i` to `A`.

## Conventions

There are no junk-value or edge-case conventions to declare: the definition is a total construction with no degenerate inputs requiring special treatment. Every well-typed input yields a well-defined continuous map.

## Worked examples

- Claim: For the family sending every point of `Bool` to `0 : ℤ` and every point of `ℕ` to `0 : ℤ`, the assembled map sends any `⟨i, x⟩` to `0`.

- Claim: If `I = Unit`, `X () = ℝ`, `A = ℝ`, and `f ()` is the identity continuous map, then `VTask.sigma f ⟨(), r⟩ = r` for all `r : ℝ`.

- Claim: For a two-element index type `I = Fin 2`, with `X 0 = X 1 = ℝ` and `f i` the continuous map sending every real to `(i : ℝ)`, the assembled continuous map sends `⟨0, r⟩` to `0` and `⟨1, r⟩` to `1` for any `r : ℝ`.

## Boundaries

- When `I` is empty (`IsEmpty I`), the sigma type `Σ i, X i` is itself empty, and `VTask.sigma f` is the unique continuous map from the empty space to `A`; the family `f` is vacuously given and the result is well-defined.
- When `I` is a singleton (`I = Unit`), the disjoint union reduces to a single summand `X ()`, and `VTask.sigma f` is essentially just `f ()`.
- When some `X i` is empty, those summands contribute no points; the assembled map is only defined on the non-empty summands.
- The construction does not require `I` to be finite or discrete; it works for any index type.

## Not to be confused with

- `ContinuousMap.comp`: that composes two continuous maps in sequence, whereas `VTask.sigma` assembles a single map from a family indexed by a type.
- `Sigma.uncurry` for plain functions (without continuity): the analogous operation on bare functions that forgets topological structure.
- `ContinuousMap.pi`: the dual construction that assembles a continuous map *into* a product type `Π i, X i` from a family of components, rather than out of a coproduct.