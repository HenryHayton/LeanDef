## Object

`VTask.augment` constructs a new chain complex (of non-negative degree, indexed by ℕ) from an existing one by inserting a fresh object at degree zero and pushing all original objects up by one degree. Concretely, given a chain complex `C` whose degree-0 object is `C.X 0`, one supplies a target object `X` together with a morphism `f : C.X 0 → X` satisfying the chain-complex identity `d₁₀ ∘ f = 0`. The result is a chain complex whose degree-0 term is `X`, whose degree-`(i+1)` term is the original `C.X i`, whose differential from degree 1 to degree 0 is `f`, and whose higher differentials are inherited from `C` (shifted by one).

This construction is classical in homological algebra: it is the way one appends an augmentation (e.g., the counit of a resolution) to a chain complex without disturbing its internal structure.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.augment : {V : Type u} -> [CategoryTheory.Category.{v, u} V] -> [CategoryTheory.Limits.HasZeroMorphisms V] -> (C : ChainComplex V ℕ) -> {X : V} -> (f : C.X 0 ⟶ X) -> (w : CategoryTheory.CategoryStruct.comp (C.d 1 0) f = 0) -> ChainComplex V ℕ
<!-- PINNED-SIGNATURE:END -->


VTask.augment : {V : Type u} -> [CategoryTheory.Category.{v, u} V] -> [CategoryTheory.Limits.HasZeroMorphisms V] -> (C : ChainComplex V ℕ) -> {X : V} -> (f : C.X 0 ⟶ X) -> (w : CategoryTheory.CategoryStruct.comp (C.d 1 0) f = 0) -> ChainComplex V ℕ

`V` is the ambient category whose objects are the terms of the chain complex (e.g., abelian groups, modules, etc.); its `Category` and `HasZeroMorphisms` instances are provided implicitly. `C` is the original chain complex over `ℕ` that will be shifted up. `X` is the new object to be placed at degree zero; it is inferred implicitly from `f`. `f` is the augmentation morphism, a map from the degree-0 term of `C` to `X`, which becomes the new differential `d₁₀` in the augmented complex. `w` is the proof that composing the original differential `C.d 1 0` with `f` equals zero, guaranteeing that `d ∘ d = 0` holds across the newly introduced degree.

## Conventions

All differentials `d i j` for index pairs `(i, j)` not of the form `(n+1, n)` in a well-formed chain complex are zero by convention; for the augmented complex this is inherited, so in particular `(augment C f w).d 0 _ = 0` and `(augment C f w).d (i+2) 0 = 0`.

## Worked examples

- Claim: The degree-0 object of `VTask.augment C f w` is `X`.
  (Formally: `(VTask.augment C f w).X 0 = X`, which is recorded as `augment_X_zero`.)

- Claim: For any `i : ℕ`, the degree-`(i+1)` object of `VTask.augment C f w` equals `C.X i`.
  (Formally: `(VTask.augment C f w).X (i + 1) = C.X i`, recorded as `augment_X_succ`.)

- Claim: The differential from degree 1 to degree 0 in `VTask.augment C f w` is exactly `f`.
  (Formally: `(VTask.augment C f w).d 1 0 = f`, recorded as `augment_d_one_zero`.)

- Claim: For any `i j : ℕ`, the differential `(VTask.augment C f w).d (i+1) (j+1)` equals `C.d i j`.
  (Formally: `(VTask.augment C f w).d (i + 1) (j + 1) = C.d i j`, recorded as `augment_d_succ_succ`.)

## Boundaries

- If `C` is the zero complex (all objects and morphisms zero), `VTask.augment C 0 (by simp)` produces a complex whose degree-0 term is `X` and all higher terms and all differentials are zero — a valid augmentation.
- The hypothesis `w` is not optional: without `C.d 1 0 ≫ f = 0`, the output would not satisfy `d ∘ d = 0` at the junction between the new differential and the original one.
- The original complex `C` is unmodified; `VTask.augment` produces a brand-new chain complex and does not mutate `C`.
- The truncation of the augmented complex `VTask.augment C f w` is canonically isomorphic to `C` itself (the isomorphism `truncateAugment` has components equal to identity morphisms).
- Conversely, any chain complex can be recovered from the augmentation of its truncation, with the zero-to-zero differential playing the role of `f`.

## Not to be confused with

- `ChainComplex.truncate`: this functor goes in the opposite direction — it removes the degree-0 term of a chain complex, whereas `VTask.augment` adds a new degree-0 term.
- `CochainComplex.augment`: the analogous construction for cochain complexes, where indices flow upward; the degree conventions and differential directions are reversed.
- A suspension or shift functor: those shift the grading uniformly without inserting a new object or requiring a compatibility morphism.