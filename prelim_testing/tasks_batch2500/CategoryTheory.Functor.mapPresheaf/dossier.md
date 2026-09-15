## VTask.mapPresheaf

### Object

Given a functor `F` from a category `C` to a category `D`, `VTask.mapPresheaf F` is the induced functor from the category of `C`-valued presheaved spaces to the category of `D`-valued presheaved spaces. It acts by leaving the underlying topological space (carrier) unchanged and post-composing every presheaf with `F`. On morphisms, it leaves the underlying continuous map (base) unchanged and applies `F` to the sheaf-theoretic comparison maps via whiskering.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mapPresheaf : {C : Type u_1} -> [CategoryTheory.Category.{v_1, u_1} C] -> {D : Type u_2} -> [CategoryTheory.Category.{v_2, u_2} D] -> (F : CategoryTheory.Functor C D) -> CategoryTheory.Functor (AlgebraicGeometry.PresheafedSpace C) (AlgebraicGeometry.PresheafedSpace D)
<!-- PINNED-SIGNATURE:END -->


`{C : Type u_1} -> [CategoryTheory.Category.{v_1, u_1} C] -> {D : Type u_2} -> [CategoryTheory.Category.{v_2, u_2} D] -> (F : CategoryTheory.Functor C D) -> CategoryTheory.Functor (AlgebraicGeometry.PresheafedSpace C) (AlgebraicGeometry.PresheafedSpace D)`

The implicit type parameters `C` and `D` are the source and target categories of the functor, with their accompanying `Category` structure instances inferred automatically. The explicit argument `F` is the functor between these two categories that determines how presheaf values are transformed.

### Conventions

There are no junk-value or boundary conventions to record: `VTask.mapPresheaf` is a total construction defined for any functor `F : C ⥤ D` between any two categories, with no special casing at degenerate inputs.

### Worked examples

- Claim: For any presheaved space `X : PresheafedSpace C` and functor `F : C ⥤ D`, the underlying topological carrier of `(VTask.mapPresheaf F).obj X` equals that of `X`.

- Claim: For any presheaved space `X : PresheafedSpace C` and functor `F : C ⥤ D`, the presheaf of `(VTask.mapPresheaf F).obj X` equals `X.presheaf ⋙ F`, i.e., the original presheaf followed by `F`.

- Claim: For any morphism `f : X ⟶ Y` in `PresheafedSpace C` and functor `F : C ⥤ D`, the base (underlying continuous map) of `(VTask.mapPresheaf F).map f` equals `f.base`.

- Claim: For any morphism `f : X ⟶ Y` in `PresheafedSpace C` and functor `F : C ⥤ D`, the sheaf comparison component `c` of `(VTask.mapPresheaf F).map f` equals the right-whiskering of `f.c` by `F`.

### Boundaries

- When `F` is the identity functor on `C`, `VTask.mapPresheaf F` is isomorphic (in fact definitionally close) to the identity functor on `PresheafedSpace C`, since post-composing a presheaf with the identity functor leaves it unchanged.
- When `F` is a composition `G ⋙ H`, `VTask.mapPresheaf (G ⋙ H)` produces the same result as composing `VTask.mapPresheaf G` followed by `VTask.mapPresheaf H`, by associativity of functor composition.
- The construction is entirely well-defined for the zero-object situation or for the empty topological space; no special behaviour arises.

### Not to be confused with

- `AlgebraicGeometry.PresheafedSpace.map`: This refers to the action of a continuous map on a single presheaved space (a morphism in `PresheafedSpace`), not the functorial lift of a categorical functor on presheaf values.
- `CategoryTheory.Functor.mapCone` / `CategoryTheory.Functor.mapDiagram`: Other "map-a-functor" constructions in category theory that transform diagrams or cones rather than presheaved spaces.
- `AlgebraicGeometry.SheafedSpace.mapPresheaf` (or ringed-space analogues): Analogous constructions for sheaved or ringed spaces that carry additional compatibility conditions beyond what is required for presheaved spaces.