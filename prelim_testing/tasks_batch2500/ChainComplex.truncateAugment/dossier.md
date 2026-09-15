## VTask.truncateAugment

### Object

Given a chain complex `C` indexed by natural numbers in an additive category `V`, an object `X`, a morphism `f : C₀ → X` from the zeroth term, and a proof that the composite `d₁₀ ≫ f = 0` (so that augmenting is well-formed), `VTask.truncateAugment` produces a canonical isomorphism between the truncation of the augmented complex back to `C`. Concretely, augmenting `C` by `f` appends `X` at degree −1 (reindexed to degree 0 in the augmented complex), and then truncating forgets that appended object, recovering something isomorphic to `C`. All components of both the forward and inverse morphism in this isomorphism are identity maps, so the isomorphism is essentially the identity at every degree.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.truncateAugment : {V : Type u} -> [CategoryTheory.Category.{v, u} V] -> [CategoryTheory.Limits.HasZeroMorphisms V] -> (C : ChainComplex V ℕ) -> {X : V} -> (f : C.X 0 ⟶ X) -> (w : CategoryTheory.CategoryStruct.comp (C.d 1 0) f = 0) -> ChainComplex.truncate.obj (C.augment f w) ≅ C
<!-- PINNED-SIGNATURE:END -->


The implicit argument `V` is the ambient additive category; the two instance arguments supply that `V` is a category and that it has zero morphisms. The explicit argument `C` is the chain complex being augmented; `X` is the object being attached at the new bottom degree; `f` is the augmentation map from degree 0 of `C` to `X`; and `w` is the witness that composing the differential `d : C₁ → C₀` with `f` is the zero morphism, which is the compatibility condition required for augmentation.

### Conventions

All component morphisms of the forward map (hom) are the identity morphism at each natural-number degree. All component morphisms of the inverse map (inv) are likewise the identity morphism at each natural-number degree.

### Worked examples

- Claim: For any chain complex `C`, augmentation data `f`, `w`, the forward component at degree `i` is the identity: `(VTask.truncateAugment C f w).hom.f i = 𝟙 (C.X i)`.

- Claim: For any chain complex `C`, augmentation data `f`, `w`, the inverse component at degree `i` is the identity: `(VTask.truncateAugment C f w).inv.f i = 𝟙 ((ChainComplex.truncate.obj (ChainComplex.augment C f w)).X i)`.

- Claim: The isomorphism `VTask.truncateAugment C f w` witnesses that `ChainComplex.truncate.obj (ChainComplex.augment C f w)` and `C` are isomorphic as chain complexes in `V`.

### Boundaries

- The construction is total: it applies to any chain complex over any category with zero morphisms, as long as the augmentation witness `w` is provided.
- When `i = 0`, the component maps are still identity morphisms; there is no special boundary behaviour at the lowest degree.
- The isomorphism is not merely an isomorphism of graded objects but a genuine isomorphism of chain complexes, meaning the component identities are compatible with all differentials.

### Not to be confused with

- `ChainComplex.augment`: The operation that *creates* an augmented chain complex from `C`, `f`, and `w`; `VTask.truncateAugment` goes the other direction, showing truncation undoes augmentation.
- `ChainComplex.truncate`: The functor that strips the zeroth (bottom) degree from an augmented complex; `VTask.truncateAugment` is the canonical isomorphism relating the result of applying this functor to an augmented complex back to the original.
- `CochainComplex.truncateAugment`: The analogous statement for cochain complexes indexed by natural numbers; the directions of differentials differ.