## Object

Given a family of continuous linear equivalences `f i : E i ≃L[𝕜] E₁ i` (one for each index `i`), `VTask.continuousMultilinearMapCongrLeft F f` is the **continuous linear equivalence** between the space of continuous multilinear maps `ContinuousMultilinearMap 𝕜 E₁ F` (taking inputs from the family `E₁`) and the space `ContinuousMultilinearMap 𝕜 E F` (taking inputs from the family `E`), obtained by pre-composing every continuous multilinear map with the family `f`. Concretely, a multilinear map `g : Π i, E₁ i → F` is sent to the multilinear map `(x₁, …, xₙ) ↦ g(f 1 x₁, …, f n xₙ)`, and the inverse direction uses the pointwise inverses `(f i).symm`. This construction is not merely a bijection of sets: it is a linear, continuous, open map between the two function spaces, i.e., a genuine isomorphism in the category of topological vector spaces.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.continuousMultilinearMapCongrLeft : {𝕜 : Type u_1} -> {ι : Type u_2} -> {E : ι → Type u_3} -> {E₁ : ι → Type u_4} -> (F : Type u_5) -> [NormedField 𝕜] -> [(i : ι) → TopologicalSpace (E i)] -> [(i : ι) → AddCommGroup (E i)] -> [(i : ι) → Module 𝕜 (E i)] -> [(i : ι) → TopologicalSpace (E₁ i)] -> [(i : ι) → AddCommGroup (E₁ i)] -> [(i : ι) → Module 𝕜 (E₁ i)] -> [AddCommGroup F] -> [Module 𝕜 F] -> [TopologicalSpace F] -> [IsTopologicalAddGroup F] -> [ContinuousConstSMul 𝕜 F] -> (f : (i : ι) → E i ≃L[𝕜] E₁ i) -> ContinuousMultilinearMap 𝕜 E₁ F ≃L[𝕜] ContinuousMultilinearMap 𝕜 E F
<!-- PINNED-SIGNATURE:END -->


`VTask.continuousMultilinearMapCongrLeft : {𝕜 : Type u_1} -> {ι : Type u_2} -> {E : ι → Type u_3} -> {E₁ : ι → Type u_4} -> (F : Type u_5) -> ...`

- **`𝕜`** (implicit): the scalar field, required to be a normed field.
- **`ι`** (implicit): the index type parametrising the family of input spaces.
- **`E`** (implicit): the first family of topological `𝕜`-modules, one for each index `i ∈ ι`; these are the input spaces of the *output* side of the equivalence.
- **`E₁`** (implicit): the second family of topological `𝕜`-modules, one for each index `i ∈ ι`; these are the input spaces of the *input* side of the equivalence.
- **`F`** (explicit): the common codomain, a topological `𝕜`-module with a topological additive group structure and continuous scalar multiplication; it appears on both sides of the equivalence.
- **`f`** (explicit): the family of continuous linear equivalences, one per index, `f i : E i ≃L[𝕜] E₁ i`; these are used to pre-compose (change of variables) in the multilinear maps. The forward direction of the main equivalence pre-composes with `f i`, and the inverse pre-composes with `(f i).symm`.

All remaining arguments are typeclass instances providing the required algebraic and topological structure on `E i`, `E₁ i`, and `F`.

## Conventions

No special junk-value or boundary conventions are declared for this definition: the construction is total and well-defined for any valid inputs satisfying the typeclass constraints, and no degenerate regime (such as an empty index type `ι`) requires a special convention.

## Worked examples

- Claim: When `ι` is a one-element type and `f` is the identity equivalence on each component, `VTask.continuousMultilinearMapCongrLeft F f` sends a continuous multilinear map `g` to itself (up to the canonical identification of `E i` with `E₁ i`).

- Claim: When `ι = Fin 2`, `E i = ℝ`, `E₁ i = ℝ`, and `f i` is the negation equivalence `x ↦ −x` (which is indeed a continuous linear equivalence), the image of a continuous bilinear map `B` under `VTask.continuousMultilinearMapCongrLeft ℝ f` is the map `(x, y) ↦ B(−x, −y) = B(x, y)` (since `B` is multilinear and two sign flips cancel). Thus the equivalence sends `B` to itself in this case.

- Claim: Composing `VTask.continuousMultilinearMapCongrLeft F f` with its inverse (i.e., applying it and then applying the inverse equivalence) returns the original continuous multilinear map, reflecting that the left and right inverses are genuinely inverse to each other.

## Boundaries

- **Empty index type `ι = ∅` (or `ι = Fin 0`)**: The spaces `ContinuousMultilinearMap 𝕜 E F` and `ContinuousMultilinearMap 𝕜 E₁ F` both reduce to the space of continuous "nullary" multilinear maps (essentially constant maps determined by their value at the unique empty tuple). The equivalence is still well-defined and is essentially the identity.
- **Single index `ι = Fin 1` or a singleton type**: The continuous multilinear maps reduce to continuous linear maps, and the equivalence reduces to pre-composition with the single given continuous linear equivalence `f 0`.
- **`f i` being the identity equivalence for all `i`**: The resulting continuous linear equivalence is the identity on the space of continuous multilinear maps.
- The construction requires `F` to carry both a topological additive group structure (`IsTopologicalAddGroup`) and continuous constant scalar multiplication (`ContinuousConstSMul 𝕜 F`); without these, the linearity and continuity of the resulting equivalence on the function space cannot be established.

## Not to be confused with

- **`ContinuousMultilinearMap.compContinuousLinearMapL`**: The unbundled (or partially bundled) version that produces only the forward linear map of the pre-composition operation, without packaging the full continuous linear equivalence structure; `VTask.continuousMultilinearMapCongrLeft` wraps this into a two-sided invertible equivalence.
- **`continuousMultilinearMapCongrRight`** (hypothetical): A change-of-codomain operation (post-composition) rather than a change-of-domain operation (pre-composition); the present definition acts on the *input* family of spaces, not the output space `F`.
- **`ContinuousLinearEquiv.arrowCongrEquiv`** or similar: Linear equivalences between spaces of *linear* (not multilinear) maps induced by domain/codomain equivalences; those apply only to the single-input (linear) case, whereas `VTask.continuousMultilinearMapCongrLeft` handles the genuinely multilinear (multi-input) setting.
