## VTask.map

### Object

Given two chain complexes `K`, `K'` (indexed by natural numbers, going downward) and two cochain complexes `L`, `L'` (indexed by natural numbers, going upward), together with "connect data" `h` and `h'` that each splice a chain complex and a cochain complex into a single ℤ-indexed cochain complex, and given morphisms `fK : K ⟶ K'` and `fL : L ⟶ L'` that are compatible at the gluing point, `VTask.map` produces the induced morphism of ℤ-indexed cochain complexes from `h.cochainComplex` to `h'.cochainComplex`. In other words, it expresses the functoriality of the "connect" construction: morphisms on the two halves that agree at the seam assemble into a morphism of the combined complexes.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {C : Type u} -> [CategoryTheory.Category.{v, u} C] -> [CategoryTheory.Limits.HasZeroMorphisms C] -> {K K' : ChainComplex C ℕ} -> {L L' : CochainComplex C ℕ} -> (h : CochainComplex.ConnectData K L) -> (h' : CochainComplex.ConnectData K' L') -> (fK : K ⟶ K') -> (fL : L ⟶ L') -> (f_comm : CategoryTheory.CategoryStruct.comp (fK.f 0) h'.d₀ = CategoryTheory.CategoryStruct.comp h.d₀ (fL.f 0)) -> h.cochainComplex ⟶ h'.cochainComplex
<!-- PINNED-SIGNATURE:END -->


`{C : Type u} -> [CategoryTheory.Category.{v, u} C] -> [CategoryTheory.Limits.HasZeroMorphisms C] -> {K K' : ChainComplex C ℕ} -> {L L' : CochainComplex C ℕ} -> (h : CochainComplex.ConnectData K L) -> (h' : CochainComplex.ConnectData K' L') -> (fK : K ⟶ K') -> (fL : L ⟶ L') -> (f_comm : CategoryTheory.CategoryStruct.comp (fK.f 0) h'.d₀ = CategoryTheory.CategoryStruct.comp h.d₀ (fL.f 0)) -> h.cochainComplex ⟶ h'.cochainComplex`

`C` is the ambient additive category (with zero morphisms) in which all complexes live. `K` and `K'` are the chain-complex halves (covering non-positive integer degrees) of the source and target connected complexes, respectively. `L` and `L'` are the cochain-complex halves (covering positive integer degrees). `h` is the connect datum that glues `K` and `L` into one ℤ-indexed cochain complex, and `h'` glues `K'` and `L'` analogously; both carry the single connecting differential `d₀` from degree 0 to degree 1 across the seam. `fK` is a morphism of chain complexes from `K` to `K'`; `fL` is a morphism of cochain complexes from `L` to `L'`. `f_comm` is the commutativity condition asserting that the two ways of crossing the seam agree: applying `fK` at degree 0 then `h'.d₀`, or applying `h.d₀` then `fL` at degree 0, produce the same map. The output is a morphism of ℤ-indexed cochain complexes from the connected complex built from `(K, L, h)` to the one built from `(K', L', h')`.

### Conventions

At non-negative integer degrees `n` (written `ofNat n` in the ℤ indexing) the component of the output morphism is `fL.f n`, the degree-`n` component of the cochain complex morphism `fL`. At strictly negative integer degrees `-(n+1)` (written `negSucc n`) the component is `fK.f n`, the degree-`n` component of the chain complex morphism `fK`. The commutativity of the output morphism with differentials at the seam degree (between `negSucc 0` and `ofNat 0`) follows from the hypothesis `f_comm`.

### Worked examples

- Claim: For any compatible pair `(fK, fL)`, the degree-2 component (a positive degree) of `VTask.map h h' fK fL f_comm` equals `fL.f 2`.

- Claim: For any compatible pair `(fK, fL)`, the degree corresponding to `negSucc 3` (i.e., degree −4) of `VTask.map h h' fK fL f_comm` equals `fK.f 3`.

- Claim: The composite `VTask.map h h' fK fL p ≫ VTask.map h' h'' fK' fL' q` equals `VTask.map h h'' (fK ≫ fK') (fL ≫ fL') _`, i.e., `VTask.map` is compatible with composition (functoriality). This is recorded as `CochainComplex.ConnectData.map_comp_map`.

### Boundaries

- The seam degree (`ofNat 0` on the cochain side and `negSucc 0` on the chain side) is the only point where the two halves interact; commutativity there requires the explicit hypothesis `f_comm` and does not follow automatically from `fK` and `fL` alone.
- When `fK` and `fL` are both identity morphisms and `h = h'`, the result is the identity morphism on `h.cochainComplex`, reflecting the identity law of the functor.
- The construction is symmetric in the following sense: swapping which morphism lives on the chain side versus the cochain side and changing `f_comm` accordingly yields the same combined morphism.
- There is no restriction on the category `C` beyond having zero morphisms; the construction works in any such category.

### Not to be confused with

- `CochainComplex.ConnectData.cochainComplex`: this is the *object*-level construction producing the ℤ-indexed cochain complex from connect data, whereas `VTask.map` is the *morphism*-level (functoriality) construction.
- `homologyMap` applied to `VTask.map h h' fK fL f_comm`: that gives the induced map on homology groups and is a further derived construction, not the morphism of complexes itself.
- A direct product or coproduct of the two complexes: the connect construction is a *splice* along a single connecting differential, not a product.