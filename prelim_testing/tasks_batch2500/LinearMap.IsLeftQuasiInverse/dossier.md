## Object

`VTask.IsLeftQuasiInverse u v` is the proposition that the linear map `u : V →ₗ[K] V₂` is a **left quasi-inverse** of the linear map `v : V₂ →ₗ[K] V`. Concretely, this means that the composition `u ∘ v` (first apply `v`, then `u`) is equivalent to the identity map on `V₂`, where two linear maps are *equivalent* when their difference has image (range) that is a noetherian `K`-module — equivalently, when their difference has finitely generated range in the case that `K` is a noetherian ring (e.g., a field). This is a strictly weaker condition than `u ∘ v` being literally equal to the identity; the two maps are only required to agree up to a map whose image is "small" in the noetherian sense.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsLeftQuasiInverse : {K : Type u_1} -> {V : Type u_2} -> {V₂ : Type u_4} -> [CommRing K] -> [AddCommGroup V] -> [Module K V] -> [AddCommGroup V₂] -> [Module K V₂] -> (u : V →ₗ[K] V₂) -> (v : V₂ →ₗ[K] V) -> Prop
<!-- PINNED-SIGNATURE:END -->


VTask.IsLeftQuasiInverse : {K : Type u_1} -> {V : Type u_2} -> {V₂ : Type u_4} -> [CommRing K] -> [AddCommGroup V] -> [Module K V] -> [AddCommGroup V₂] -> [Module K V₂] -> (u : V →ₗ[K] V₂) -> (v : V₂ →ₗ[K] V) -> Prop

`K` is the commutative scalar ring. `V` is the source module of `v` and the target module of `u`. `V₂` is the target module of `v` and the source module of `u`. The instance arguments supply the ring and module structures on `K`, `V`, and `V₂`. The argument `u` is the candidate left quasi-inverse — the map being tested for the quasi-inverse property. The argument `v` is the map of which `u` is the purported left quasi-inverse.

## Conventions

There are no declared junk-value or edge conventions for this definition: it is a `Prop`-valued predicate on a pair of linear maps with no distinguished degenerate inputs requiring special treatment.

## Worked examples

- Claim: For any linear map `v : V₂ →ₗ[K] V`, the identity map `LinearMap.id` on `V₂` is a left quasi-inverse of itself composed with the zero map only when their composition is equivalent to the identity; in particular, if `u = LinearMap.id` and `v = LinearMap.id` (both are the identity), then `VTask.IsLeftQuasiInverse LinearMap.id LinearMap.id` holds, since `id ∘ id = id ≈ id`.

- Claim: If `u` is a left quasi-inverse of `v` and `u'` is equivalent to `u` modulo a noetherian-range difference, and `v'` is equivalent to `v` modulo a noetherian-range difference, then `VTask.IsLeftQuasiInverse u' v'` also holds — the property is stable under the equivalence relation on linear maps.

- Claim: `VTask.IsLeftQuasiInverse u v` holds if and only if `v` is a right quasi-inverse of `u` (i.e., `v.IsRightQuasiInverse u`), showing the left/right quasi-inverse relation is symmetric in the sense of swapping the two maps.

- Claim: If `u'` is a left quasi-inverse of `u` and `v'` is a left quasi-inverse of `v`, then `u' ∘ v'` is a left quasi-inverse of `v ∘ u` — the property is closed under composition in the appropriate sense.

## Boundaries

- When `u ∘ v` is exactly equal to `LinearMap.id` (not merely equivalent), the condition is satisfied, since exact equality implies equivalence modulo noetherian-range maps (the difference is the zero map, which has zero range, a noetherian module).
- The condition is *not* symmetric in `u` and `v` as stated: `VTask.IsLeftQuasiInverse u v` says `u ∘ v ≈ id`, while swapping would say `v ∘ u ≈ id`. These are different propositions (left vs. right quasi-inverse).
- If `K` is a noetherian ring (in particular, a field), "noetherian range" is the same as "finitely generated range", making the equivalence relation easier to check concretely.
- The definition is stated for modules over a commutative ring `K`; it does not apply directly to non-commutative scalar rings.

## Not to be confused with

- `LinearMap.IsRightQuasiInverse u v`: asserts `v ∘ u ≈ id` (roles of left and right are swapped); this is equivalent to `VTask.IsLeftQuasiInverse v u`.
- The classical notion of a left inverse (retraction): requires `u ∘ v = id` exactly, with no "noetherian-range" slack.
- The equivalence relation `≈` on linear maps itself (which compares two maps modulo noetherian-range differences): the quasi-inverse condition uses this relation but is a property of a *pair* of maps, not a direct comparison of two maps.