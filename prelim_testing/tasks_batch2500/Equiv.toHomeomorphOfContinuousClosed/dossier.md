## Object

Given a set-theoretic bijection `e : X ≃ Y` between two topological spaces, together with a proof that the underlying function is continuous and a proof that it is a closed map (i.e., sends closed sets to closed sets), `VTask.toHomeomorphOfContinuousClosed` produces a homeomorphism `X ≃ₜ Y` — a bicontinuous bijection — whose underlying function agrees with `e`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toHomeomorphOfContinuousClosed : {X : Type u_1} -> {Y : Type u_2} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> (e : X ≃ Y) -> (h₁ : Continuous ⇑e) -> (h₂ : IsClosedMap ⇑e) -> X ≃ₜ Y
<!-- PINNED-SIGNATURE:END -->


`{X : Type u_1} -> {Y : Type u_2} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> (e : X ≃ Y) -> (h₁ : Continuous ⇑e) -> (h₂ : IsClosedMap ⇑e) -> X ≃ₜ Y`

The implicit type arguments `X` and `Y` are the source and target types. The implicit topological-space instances equip each type with its topology. The argument `e` is the underlying equivalence (bijection with explicit inverse). The argument `h₁` is the proof that the forward function of `e` is continuous. The argument `h₂` is the proof that the forward function of `e` is a closed map.

## Conventions

The resulting homeomorphism's underlying function (and its `toEquiv`) is definitionally equal to the original equivalence `e`; no new map is fabricated.

## Worked examples

- Claim: For the identity equivalence `Equiv.refl X`, with the trivial continuity and closed-map proofs, `VTask.toHomeomorphOfContinuousClosed (Equiv.refl X) continuous_id (fun s hs => hs)` produces a homeomorphism whose underlying equivalence is `Equiv.refl X`.

- Claim: If `e : X ≃ Y` is continuous and sends closed sets to closed sets, then the homeomorphism `h := VTask.toHomeomorphOfContinuousClosed e h₁ h₂` satisfies `h.toFun = e.toFun` (the forward functions agree).

- Claim: If `e : X ≃ Y` is continuous and is a closed map, then the inverse of the resulting homeomorphism is also continuous (this is the defining content of being a homeomorphism, and is guaranteed by the construction).

- Claim: The composition of the homeomorphism produced from `e` with the homeomorphism produced from the inverse equivalence `e.symm` (given appropriate hypotheses) is the identity homeomorphism on `X`.

## Boundaries

- The construction is total: it requires no restrictions on the topological spaces beyond being topological spaces. Any continuous closed bijection qualifies.
- If `e` is continuous but not a closed map, the construction cannot be invoked — the argument `h₂ : IsClosedMap ⇑e` would be unprovable. No fallback or partial result is produced.
- The docstring mentions "open" but the actual hypothesis used is `IsClosedMap`; the two conditions are equivalent for bijections between topological spaces (a bijection is an open map if and only if it is a closed map), so either characterization leads to the same conclusion.
- Continuity of the inverse is not assumed; it is derived automatically from the fact that a continuous bijection that is also a closed map is a topological embedding, and hence a homeomorphism.

## Not to be confused with

- `Equiv.toHomeomorphOfIsInducing`: a related constructor that builds a homeomorphism from an equivalence and an inducing-map hypothesis, rather than from continuity + closed-map hypotheses directly.
- `Homeomorph.ofContinuousOpen` (or an analogous constructor using `IsOpenMap`): uses the open-map condition instead of the closed-map condition; both are valid routes to a homeomorphism from a continuous bijection, but are separate lemmas.
- `IsClosedEmbedding.homeomorph`: constructs a homeomorphism from a closed embedding onto its image, which is a strictly stronger hypothesis than what is needed here (surjectivity is already encoded in `e`).