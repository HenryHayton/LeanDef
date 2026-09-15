## VTask.nullHomotopicMap

### Object

Given two homological complexes `C` and `D` (over a preadditive category `V`, with the same index shape `c`), and a doubly-indexed family of morphisms `hom i j : C.X i ⟶ D.X j` (one for every pair of indices), `VTask.nullHomotopicMap hom` is the chain map `C ⟶ D` whose component at degree `i` is the sum of two terms:

- the **forward part**: `hom i k₂ ≫ D.d k₂ i`, using the unique `k₂` with `c.Rel k₂ i` (the differential of `D` going into degree `i`), and
- the **backward part**: `C.d i k₀ ≫ hom k₀ i`, using the unique `k₀` with `c.Rel i k₀` (the differential of `C` going out of degree `i`).

This is precisely the chain map that would witness a null-homotopy if `hom` were the homotopy datum: a map of the form `d ∘ h + h ∘ d`. In particular, any map of this form is chain-homotopic to zero, and the zero map between any two complexes arises this way (by taking all `hom i j = 0`). The construction is well-defined as a chain map (i.e., it commutes with the differentials) regardless of whether the family `hom` satisfies any vanishing conditions outside the relevant indices.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.nullHomotopicMap : {ι : Type u_1} -> {V : Type u} -> [CategoryTheory.Category.{v, u} V] -> [CategoryTheory.Preadditive V] -> {c : ComplexShape ι} -> {C D : HomologicalComplex V c} -> (hom : (i j : ι) → C.X i ⟶ D.X j) -> C ⟶ D
<!-- PINNED-SIGNATURE:END -->


`VTask.nullHomotopicMap : {ι : Type u_1} -> {V : Type u} -> [CategoryTheory.Category.{v, u} V] -> [CategoryTheory.Preadditive V] -> {c : ComplexShape ι} -> {C D : HomologicalComplex V c} -> (hom : (i j : ι) → C.X i ⟶ D.X j) -> C ⟶ D`

- `ι` is the type of degree indices used to label the components of the complexes.
- `V` is the underlying preadditive category in which all objects and morphisms live.
- The `Category` instance equips `V` with its categorical structure (composition, identities).
- The `Preadditive` instance equips each hom-set in `V` with an abelian group structure compatible with composition, which is needed so that the component maps can be formed as sums.
- `c` is the complex shape, specifying which pairs of degrees are linked by differentials and in which direction.
- `C` and `D` are the source and target homological complexes over `V` with shape `c`.
- `hom` is the doubly-indexed family of morphisms: for every pair of indices `i` and `j`, it provides a morphism from the `i`-th object of `C` to the `j`-th object of `D`. Only the values `hom i k₂` where `c.Rel k₂ i` and `hom k₀ i` where `c.Rel i k₀` actually contribute to the resulting chain map; all other values are silently ignored.

### Conventions

When an index `k₀` has no predecessor under `c.Rel` (i.e., `c.Rel k₀ l` holds for no `l`) and no successor (i.e., `c.Rel l k₀` holds for no `l`), the component of the null-homotopic map at `k₀` is zero, regardless of the values of `hom`. The values of `hom i j` for pairs `(i, j)` where neither `c.Rel j i` nor `c.Rel i j` holds are completely ignored and do not affect the resulting chain map.

### Worked examples

- Claim: At a degree `k₁` that is in the interior of the complex (with `c.Rel k₂ k₁` and `c.Rel k₁ k₀`), the component of `VTask.nullHomotopicMap hom` at `k₁` equals `C.d k₁ k₀ ≫ hom k₀ k₁ + hom k₁ k₂ ≫ D.d k₂ k₁`.

- Claim: At a degree `k₀` that is a left boundary (there exists `k₁` with `c.Rel k₁ k₀`, but no `l` satisfies `c.Rel k₀ l`), the component equals `hom k₀ k₁ ≫ D.d k₁ k₀` (only the forward/dNext part survives).

- Claim: At a degree `k₁` that is a right boundary (there exists `k₀` with `c.Rel k₁ k₀`, but no `l` satisfies `c.Rel l k₁`), the component equals `C.d k₁ k₀ ≫ hom k₀ k₁` (only the backward/prevD part survives).

- Claim: At an isolated degree `k₀` (no `l` with `c.Rel k₀ l`, and no `l` with `c.Rel l k₀`), the component of `VTask.nullHomotopicMap hom` at `k₀` is `0`.

- Claim: Post-composing a null-homotopic map with a chain map `g : D ⟶ E` gives the null-homotopic map for the family `fun i j => hom i j ≫ g.f j`; that is, `VTask.nullHomotopicMap hom ≫ g = VTask.nullHomotopicMap (fun i j => hom i j ≫ g.f j)`.

- Claim: Pre-composing a chain map `f : C ⟶ D` with a null-homotopic map gives `f ≫ VTask.nullHomotopicMap hom = VTask.nullHomotopicMap (fun i j => f.f i ≫ hom i j)`.

### Boundaries

- If every index is isolated (no differential relations in `c`), then `VTask.nullHomotopicMap hom` is the zero chain map for every family `hom`, since both the forward and backward parts vanish everywhere.
- At a left-boundary degree (no outgoing differentials from that degree in `C`), the backward contribution vanishes and only the forward part `hom k₀ k₁ ≫ D.d k₁ k₀` appears.
- At a right-boundary degree (no incoming differentials into that degree in `D`), the forward contribution vanishes and only the backward part `C.d k₁ k₀ ≫ hom k₀ k₁` appears.
- The family `hom` is allowed to be entirely arbitrary (no zero conditions required outside relevant indices); extra values are simply ignored.
- Taking `hom i j = 0` for all `i j` yields the zero chain map.

### Not to be confused with

- `Homotopy.nullHomotopicMap'`: A variant that requires `hom` to be defined only on pairs `(i, j)` with `c.Rel j i`, supplying the same chain map but from a restricted datum.
- `Homotopy`: The structure recording a homotopy between two chain maps, which uses the same `hom` datum but additionally carries the chain maps being related and a proof that their difference equals the null-homotopic map.
- A null-homotopy *witness*: `VTask.nullHomotopicMap hom` is itself a chain map (an element of `C ⟶ D`), not a proof that some other map is null-homotopic; it is the map that *would be* the homotopy-to-zero if it happened to equal some given map.
