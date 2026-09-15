## Object

A set `B` is *exposed* with respect to a set `A` (over a topological vector space `E` with scalar field `𝕜`) if `B` is precisely the set of points in `A` that simultaneously maximize some continuous linear functional `l : E → 𝕜` over all of `A`. In other words, `B` is a "supporting slice" of `A` cut out by an extreme supporting hyperplane. The empty set is declared exposed vacuously (the nonemptiness hypothesis in the definition is not met). Every exposed set is also an extreme set of `A`, but the converse need not hold.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsExposed : (𝕜 : Type u_1) -> {E : Type u_2} -> [TopologicalSpace 𝕜] -> [Semiring 𝕜] -> [Preorder 𝕜] -> [AddCommMonoid E] -> [TopologicalSpace E] -> [Module 𝕜 E] -> (A B : Set E) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsExposed (𝕜 : Type u_1) {E : Type u_2} [TopologicalSpace 𝕜] [Semiring 𝕜] [Preorder 𝕜] [AddCommMonoid E] [TopologicalSpace E] [Module 𝕜 E] (A B : Set E) : Prop`

The scalar field `𝕜` is a topological semiring equipped with a preorder; it plays the role of the codomain of linear functionals and the field of scalars. The ambient space `E` is a topological additive commutative monoid with a compatible `𝕜`-module structure. The argument `A` is the ambient set (the "body") whose exposed faces are being studied. The argument `B` is the candidate exposed face — the set being tested for the exposed-face property relative to `A`.

## Conventions

The empty set is considered exposed with respect to any set `A`; the defining existential is vacuously satisfied because the nonemptiness premise is not met. Thus `VTask.IsExposed 𝕜 A ∅` holds unconditionally.

## Worked examples

- Claim: The empty set is exposed with respect to any set `A` — `VTask.IsExposed 𝕜 A ∅` holds.

- Claim: Every set `A` is exposed with respect to itself — `VTask.IsExposed 𝕜 A A` holds (witnessed by the zero functional).

- Claim: If `B` is exposed in `A` and `A` is convex, then `B` is convex.

- Claim: If `B` is exposed in `A`, then `B ⊆ A`.

- Claim: If `B` is exposed in `A` and `A` is a compact set in a Hausdorff space (with `OrderClosedTopology 𝕜`), then `B` is compact.

- Claim: A singleton `{x}` satisfies `VTask.IsExposed 𝕜 A {x}` if and only if `x` is an exposed point of `A`.

## Boundaries

- **Empty `B`:** `VTask.IsExposed 𝕜 A ∅` holds for any `A` because the condition is stated as an implication with hypothesis `B.Nonempty`, which fails for `∅`.
- **`B = A`:** `A` is always exposed in itself, since the zero functional achieves its maximum everywhere on `A`.
- **Non-exposed extreme sets:** An extreme set need not be exposed. The predicate `VTask.IsExposed` is strictly stronger than `IsExtreme`: every exposed face is extreme, but extreme sets that are not cut out by any supporting hyperplane are not exposed.
- **Antisymmetry:** If `B` is exposed in `A` and simultaneously `A` is exposed in `B`, then `A = B`.
- **Intersection:** A finite nonempty intersection of exposed faces of `A` is again an exposed face of `A` (under an ordered ring assumption).

## Not to be confused with

- `IsExtreme 𝕜 A B` — the weaker notion that `B` is an extreme subset of `A`; every exposed set is extreme, but not vice versa.
- `Set.exposedPoints 𝕜 A` — the set of all exposed *points* (singleton exposed faces) of `A`; related by: `x ∈ A.exposedPoints 𝕜 ↔ VTask.IsExposed 𝕜 A {x}`.
- `ContinuousLinearMap.toExposed l A` — the specific exposed face of `A` cut out by a given functional `l`, which by construction always satisfies `VTask.IsExposed 𝕜 A (l.toExposed A)`.