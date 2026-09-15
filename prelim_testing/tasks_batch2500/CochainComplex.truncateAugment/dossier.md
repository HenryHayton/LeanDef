## Object

`VTask.truncateAugment` produces a canonical isomorphism of cochain complexes (indexed by ℕ) between two naturally associated objects: the truncation of an augmented cochain complex, and the original cochain complex before augmentation. Concretely, given a cochain complex `C` and an augmentation morphism `f : X → C.X 0` satisfying the cocycle condition, one can form an augmented complex by prepending `X` in degree −1 (or, in the ℕ-indexed setting, by shifting degrees up by 1 and placing `X` in degree 0). Truncating this augmented complex—dropping the degree-0 term `X`—recovers a complex isomorphic to `C`, and this isomorphism has identity maps at every degree.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.truncateAugment : {V : Type u} -> [CategoryTheory.Category.{v, u} V] -> [CategoryTheory.Limits.HasZeroMorphisms V] -> (C : CochainComplex V ℕ) -> {X : V} -> (f : X ⟶ C.X 0) -> (w : CategoryTheory.CategoryStruct.comp f (C.d 0 1) = 0) -> CochainComplex.truncate.obj (C.augment f w) ≅ C
<!-- PINNED-SIGNATURE:END -->


`VTask.truncateAugment : {V : Type u} -> [CategoryTheory.Category.{v, u} V] -> [CategoryTheory.Limits.HasZeroMorphisms V] -> (C : CochainComplex V ℕ) -> {X : V} -> (f : X ⟶ C.X 0) -> (w : CategoryTheory.CategoryStruct.comp f (C.d 0 1) = 0) -> CochainComplex.truncate.obj (C.augment f w) ≅ C`

- `V` is the ambient additive category (an implicit universe-polymorphic type equipped with a category structure and zero morphisms).
- `C` is the cochain complex over `V` indexed by natural numbers that we begin with.
- `X` is an implicit object of `V` that serves as the augmenting object placed in degree 0 of the augmented complex.
- `f` is the augmentation morphism from `X` to the degree-0 term of `C`, i.e., a morphism `X → C.X 0`.
- `w` is the proof that `f` composed with the first differential `C.d 0 1` is zero, ensuring that augmenting with `f` yields a valid cochain complex.

The output is a natural isomorphism of cochain complexes `truncate.obj (C.augment f w) ≅ C`.

## Conventions

Both the forward (`hom`) and backward (`inv`) components of the isomorphism are given by identity morphisms at every natural number index `i`; there are no nontrivial maps involved.

## Worked examples

- Claim: For any valid augmented cochain complex, the forward component `(VTask.truncateAugment C f w).hom.f i` equals the identity morphism `𝟙 (C.X i)` at every degree `i : ℕ`.

- Claim: For any valid augmented cochain complex, the backward component `(VTask.truncateAugment C f w).inv.f i` equals the identity morphism on `(CochainComplex.truncate.obj (C.augment f w)).X i` at every degree `i : ℕ`.

- Claim: The isomorphism `VTask.truncateAugment C f w` is its own inverse in the sense that `hom` followed by `inv` and `inv` followed by `hom` are both the identity chain map, since both components are identities.

## Boundaries

- The condition `w : f ≫ C.d 0 1 = 0` is essential; without it, `C.augment f w` is not defined as a valid cochain complex, and the truncation would not be meaningful.
- The isomorphism is entirely trivial at the level of individual objects and morphisms: every component is an identity. The nontrivial content is the proof that these identity maps constitute a valid chain map (i.e., commute with the differentials).
- Because ℕ-indexed cochain complexes are used, there is no negative-degree term; the augmenting object `X` occupies degree 0 of the augmented complex, and degree-0 of the original complex `C` appears in degree 1 of the augmented complex. After truncation, degrees are renumbered back so that `C.X i` corresponds to `(truncate.obj (C.augment f w)).X i`.

## Not to be confused with

- `CochainComplex.augment`: the operation that *creates* the augmented cochain complex from `C`, `f`, and `w`; `VTask.truncateAugment` goes in the opposite direction by recovering `C` after truncation.
- `CochainComplex.truncate`: the functor that drops the degree-0 term of a cochain complex; `VTask.truncateAugment` is a specific natural isomorphism relating the output of this functor (applied to an augmented complex) back to the original complex.
- `CochainComplex.augmentTruncate`: the companion isomorphism that augmenting the truncation of a cochain complex is isomorphic to the original complex, which goes in the other direction of the adjunction between augmentation and truncation.
