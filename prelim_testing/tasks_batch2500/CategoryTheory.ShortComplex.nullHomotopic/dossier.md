## Object

Given two short complexes $S_1 = (X_1 \xrightarrow{f_1} X_2 \xrightarrow{g_1} X_3)$ and $S_2 = (X_1' \xrightarrow{f_2} X_2' \xrightarrow{g_2} X_3')$ in a preadditive category, a **null-homotopic morphism** from $S_1$ to $S_2$ is a morphism of short complexes whose three components are each expressed as a sum of terms involving auxiliary "homotopy" maps. In the classical language of chain complexes, a chain map is null-homotopic when it can be written as a boundary—here the analogue for a length-3 complex uses four auxiliary maps (one for each pair of adjacent or equal positions, plus two boundary conditions ensuring the formula yields a genuine morphism of short complexes). The result is a morphism $S_1 \to S_2$ that induces the zero map on homology.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.nullHomotopic : {C : Type u_1} -> [CategoryTheory.Category.{v_1, u_1} C] -> [CategoryTheory.Preadditive C] -> (S₁ S₂ : CategoryTheory.ShortComplex C) -> (h₀ : S₁.X₁ ⟶ S₂.X₁) -> (h₀_f : CategoryTheory.CategoryStruct.comp h₀ S₂.f = 0) -> (h₁ : S₁.X₂ ⟶ S₂.X₁) -> (h₂ : S₁.X₃ ⟶ S₂.X₂) -> (h₃ : S₁.X₃ ⟶ S₂.X₃) -> (g_h₃ : CategoryTheory.CategoryStruct.comp S₁.g h₃ = 0) -> S₁ ⟶ S₂
<!-- PINNED-SIGNATURE:END -->


```
VTask.nullHomotopic : {C : Type u_1} -> [CategoryTheory.Category.{v_1, u_1} C] -> [CategoryTheory.Preadditive C] -> (S₁ S₂ : CategoryTheory.ShortComplex C) -> (h₀ : S₁.X₁ ⟶ S₂.X₁) -> (h₀_f : CategoryTheory.CategoryStruct.comp h₀ S₂.f = 0) -> (h₁ : S₁.X₂ ⟶ S₂.X₁) -> (h₂ : S₁.X₃ ⟶ S₂.X₂) -> (h₃ : S₁.X₃ ⟶ S₂.X₃) -> (g_h₃ : CategoryTheory.CategoryStruct.comp S₁.g h₃ = 0) -> S₁ ⟶ S₂
```

`C` is the ambient preadditive category. `S₁` and `S₂` are the source and target short complexes. `h₀` is the first homotopy datum, a map from $S_1.X_1$ to $S_2.X_1$; `h₀_f` is the condition that $h_0$ followed by $S_2.f$ is zero, needed to ensure the first component formula is a valid morphism of short complexes. `h₁` is the primary homotopy map, going from $S_1.X_2$ back to $S_2.X_1$ (the "backwards" step). `h₂` is the homotopy map from $S_1.X_3$ to $S_2.X_2$. `h₃` is the last homotopy datum, a map from $S_1.X_3$ to $S_2.X_3$; `g_h₃` is the condition that $S_1.g$ followed by $h_3$ is zero, ensuring the third component formula is a valid morphism of short complexes.

## Conventions

There are no junk-value conventions: all arguments are meaningful and the construction is total over its stated inputs; every supplied datum is used in the component formulas and the two proof obligations are genuine mathematical conditions, not mere conventions.

## Worked examples

- Claim: For any null-homotopic morphism built by `VTask.nullHomotopic`, the induced map on homology (left, right, or total) is zero.

- Claim: The first component (τ₁) of the resulting morphism `VTask.nullHomotopic S₁ S₂ h₀ h₀_f h₁ h₂ h₃ g_h₃` equals `h₀ + S₁.f ≫ h₁`.

- Claim: The second component (τ₂) of the resulting morphism equals `h₁ ≫ S₂.f + S₁.g ≫ h₂`.

- Claim: The third component (τ₃) of the resulting morphism equals `h₂ ≫ S₂.g + h₃`.

## Boundaries

- If `h₁`, `h₂` are zero and `h₀`, `h₃` are also zero (and the proof obligations are trivially met), the result is the zero morphism of short complexes.
- The two proof obligations `h₀_f` and `g_h₃` are not optional: they are the precise conditions that make the degree-0 and degree-2 components of the homotopy datum compatible with the boundary maps of $S_2$ and $S_1$ respectively, guaranteeing the output is genuinely a morphism of short complexes (commutes with $f$ and $g$).
- The construction works in any preadditive category—it does not require abelian, exact, or any further structure beyond the preadditive structure and the composition laws.

## Not to be confused with

- `Homotopy.ofNullHomotopic`: the related construction that packages the same data as a homotopy object (rather than just a morphism of short complexes).
- `CategoryTheory.ShortComplex.Homotopy`: the type classifying homotopies between two morphisms of short complexes; a null-homotopic morphism is one that is homotopic to zero via such a homotopy.
- An ordinary chain null-homotopy in homological algebra: while the idea is the same (write the map as a "boundary"), the short-complex version has boundary corrections at both ends (`h₀` and `h₃`) that are absent in the classical infinite-complex setting.
