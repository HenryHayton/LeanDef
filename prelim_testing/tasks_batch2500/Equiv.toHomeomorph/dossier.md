## VTask.toHomeomorph

### Object

Given a set-theoretic equivalence (bijection) `e : X ≃ Y` between two topological spaces, together with a proof that a subset of `Y` is open if and only if its preimage under `e` is open in `X`, `VTask.toHomeomorph` produces a **homeomorphism** `X ≃ₜ Y` — a bicontinuous bijection between the two spaces. Intuitively, the openness condition ensures that `e` not only moves points bijectively but also respects the topology in both directions, making both `e` and its inverse continuous.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toHomeomorph : {X : Type u_1} -> {Y : Type u_2} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> (e : X ≃ Y) -> (he : ∀ (s : Set Y), IsOpen (⇑e ⁻¹' s) ↔ IsOpen s) -> X ≃ₜ Y
<!-- PINNED-SIGNATURE:END -->


`{X : Type u_1} -> {Y : Type u_2} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> (e : X ≃ Y) -> (he : ∀ (s : Set Y), IsOpen (⇑e ⁻¹' s) ↔ IsOpen s) -> X ≃ₜ Y`

The implicit type arguments `X` and `Y` are the two topological spaces involved. The instance arguments supply the topologies on `X` and `Y` respectively. The argument `e` is the underlying set-theoretic equivalence (bijection) from `X` to `Y`. The argument `he` is a proof that for every subset `s` of `Y`, the subset `s` is open in `Y` if and only if its preimage `e⁻¹(s)` is open in `X`; this encodes precisely that `e` is a homeomorphism.

### Conventions

The resulting homeomorphism `VTask.toHomeomorph e he` has the same underlying equivalence as `e`; that is, it sends the same points to the same points and its inverse sends the same points back. The openness condition `he` is used to derive continuity of both `e` and its inverse, but the underlying bijection is unchanged.

### Worked examples

- Claim: For any topological space `X`, `VTask.toHomeomorph (Equiv.refl X) (fun s => Iff.rfl)` is a homeomorphism from `X` to itself whose underlying map is the identity.

- Claim: If `e : X ≃ Y` is a homeomorphism in the sense that preimages of open sets are open and open sets pull back to open sets, then `VTask.toHomeomorph e he` as a bundled homeomorphism has `(VTask.toHomeomorph e he).toEquiv = e`.

### Boundaries

- The function is defined for any equivalence `e` and any proof `he` of the openness condition; there are no numerical or structural edge cases arising from the types `X` and `Y` themselves (beyond needing topological space instances).
- If `X` or `Y` carries the discrete topology (every set open), then the openness condition `he` is automatically satisfied for any bijection, since every subset of `X` is open.
- If `X` or `Y` carries the indiscrete topology (only ∅ and the whole space are open), the condition `he` becomes a strong constraint: it requires that the bijection send the whole space to the whole space and ∅ to ∅ (which is automatic), so the condition reduces to checking only two sets.
- The construction does not require any compactness, Hausdorff, or other separation/compactness hypotheses; it works for completely arbitrary topological spaces.

### Not to be confused with

- `Homeomorph.mk`: The raw constructor for the `Homeomorph` structure, which requires explicit continuity witnesses for both directions rather than a single openness equivalence condition.
- `Equiv.toHomeomorphOfInducing` (or similar): Constructions that build a homeomorphism from an equivalence satisfying an *inducing* or *embedding* condition, rather than the direct openness-iff characterization used here.
- `IsOpenMap` / `OpenEmbedding`: Related but distinct concepts; an open map sends open sets to open sets (forward direction), whereas `he` is a biconditional about preimages of open sets.