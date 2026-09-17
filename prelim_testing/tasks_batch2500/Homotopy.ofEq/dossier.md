## Object

Given an equality `h : f = g` between two chain maps (morphisms of homological complexes) `f, g : C ⟶ D` in a preadditive category, `VTask.ofEq h` produces a **homotopy** from `f` to `g`. Since `f` and `g` are literally the same map, the witness is trivially constructed: the underlying chain-homotopy data (the collection of degree-shifting maps) is identically zero, and all required compatibility equations are satisfied vacuously.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofEq : {ι : Type u_1} -> {V : Type u} -> [CategoryTheory.Category.{v, u} V] -> [CategoryTheory.Preadditive V] -> {c : ComplexShape ι} -> {C D : HomologicalComplex V c} -> {f g : C ⟶ D} -> (h : f = g) -> Homotopy f g
<!-- PINNED-SIGNATURE:END -->


`{ι : Type u_1} -> {V : Type u} -> [CategoryTheory.Category.{v, u} V] -> [CategoryTheory.Preadditive V] -> {c : ComplexShape ι} -> {C D : HomologicalComplex V c} -> {f g : C ⟶ D} -> (h : f = g) -> Homotopy f g`

The index type `ι` parametrises the grading of the complexes. The ambient category `V` is required to be preadditive (so that homotopies, which involve sums of maps, make sense). The complex shape `c` specifies the differentials' degree conventions. `C` and `D` are the source and target homological complexes. `f` and `g` are the two chain maps being related. The explicit argument `h` is the proof that `f` and `g` are equal as chain maps; this equality is what allows the homotopy to be trivially witnessed.

## Conventions

The auxiliary chain-homotopy map (the collection of maps shifting degree) is taken to be the zero morphism in every degree. This is the canonical junk-free choice when no non-trivial homotopy data is needed.

## Worked examples

- Claim: For any chain map `f : C ⟶ D`, applying `VTask.ofEq rfl` yields a homotopy from `f` to `f` whose underlying homotopy maps are all zero.

- Claim: If `f = g` and one constructs `VTask.ofEq h`, the resulting `Homotopy f g` satisfies `(VTask.ofEq h).hom = 0` (i.e., the auxiliary homotopy data is the zero morphism complex).

## Boundaries

- The construction is total: it is defined for any proof of equality `f = g`, including trivial reflexivity `rfl`. There are no restrictions on the shape, the category, or the complexes.
- When `h : f = g` is `rfl`, the result is a homotopy from `f` to itself with zero chain-homotopy data—the simplest possible reflexivity witness for the homotopy relation.
- The zero homotopy maps trivially satisfy the condition that their contributions to boundary terms are zero, so no non-trivial verification is needed.

## Not to be confused with

- `Homotopy.refl`: The reflexivity homotopy for a single chain map `f`, which is `VTask.ofEq rfl`; `VTask.ofEq` generalises this to any equality, not just reflexivity.
- `Homotopy`: The type of chain homotopies itself; `VTask.ofEq` is a *constructor* producing a term of this type, not the type itself.
- Homotopy equivalence of complexes: A much stronger notion asserting the existence of mutually inverse chain maps up to homotopy; `VTask.ofEq` only concerns homotopies between a single pair of equal maps.