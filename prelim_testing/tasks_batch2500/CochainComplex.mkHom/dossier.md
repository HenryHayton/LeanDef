## Object

`VTask.mkHom P Q zero one one_zero_comm succ` is a chain map (morphism of cochain complexes) from a ℕ-indexed cochain complex `P` to another ℕ-indexed cochain complex `Q` in an additive category `V`. It is constructed inductively: the components in degrees 0 and 1 are supplied directly, and every component in degree `n + 2` is produced by a user-supplied step function that receives the components in degrees `n` and `n + 1` together with the proof that those two components form a commutative square. The resulting morphism respects all the differential squares, i.e., it is a genuine morphism in the category of cochain complexes.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mkHom : {V : Type u} -> [CategoryTheory.Category.{v, u} V] -> [CategoryTheory.Limits.HasZeroMorphisms V] -> (P Q : CochainComplex V ℕ) -> (zero : P.X 0 ⟶ Q.X 0) -> (one : P.X 1 ⟶ Q.X 1) -> (one_zero_comm : CategoryTheory.CategoryStruct.comp zero (Q.d 0 1) = CategoryTheory.CategoryStruct.comp (P.d 0 1) one) -> (succ :
    (n : ℕ) →
      (p :
          (f : P.X n ⟶ Q.X n) ×'
            (f' : P.X (n + 1) ⟶ Q.X (n + 1)) ×'
              CategoryTheory.CategoryStruct.comp f (Q.d n (n + 1)) =
                CategoryTheory.CategoryStruct.comp (P.d n (n + 1)) f') →
        (f'' : P.X (n + 2) ⟶ Q.X (n + 2)) ×'
          CategoryTheory.CategoryStruct.comp p.snd.fst (Q.d (n + 1) (n + 2)) =
            CategoryTheory.CategoryStruct.comp (P.d (n + 1) (n + 2)) f'') -> P ⟶ Q
<!-- PINNED-SIGNATURE:END -->


VTask.mkHom : {V : Type u} -> [CategoryTheory.Category.{v, u} V] -> [CategoryTheory.Limits.HasZeroMorphisms V] -> (P Q : CochainComplex V ℕ) -> (zero : P.X 0 ⟶ Q.X 0) -> (one : P.X 1 ⟶ Q.X 1) -> (one_zero_comm : CategoryTheory.CategoryStruct.comp zero (Q.d 0 1) = CategoryTheory.CategoryStruct.comp (P.d 0 1) one) -> (succ : ...) -> P ⟶ Q

- `V` is the ambient additive category in which the complexes live.
- The `Category` and `HasZeroMorphisms` instances equip `V` with the categorical structure and zero morphisms needed to talk about cochain complexes.
- `P` and `Q` are the source and target ℕ-indexed cochain complexes.
- `zero` is the component of the chain map in degree 0, a morphism from `P.X 0` to `Q.X 0`.
- `one` is the component in degree 1, a morphism from `P.X 1` to `Q.X 1`.
- `one_zero_comm` is the proof that `zero` and `one` form a commutative square with the differentials `P.d 0 1` and `Q.d 0 1`, i.e., `zero ≫ Q.d 0 1 = P.d 0 1 ≫ one`.
- `succ` is the inductive step: given a natural number `n` and a package consisting of the component in degree `n`, the component in degree `n + 1`, and the commutativity proof for the square between them, it produces the component in degree `n + 2` together with the proof that it forms a commutative square with the component in degree `n + 1`.

## Conventions

The differential of a cochain complex between non-consecutive (or equal) indices is zero by convention in Mathlib, so the commutativity condition is vacuous outside of consecutive degrees; the constructor only requires commutativity for consecutive pairs `(n, n+1)`.

## Worked examples

- Claim: The degree-0 component of `VTask.mkHom P Q zero one h succ` equals `zero`.
  (Follows from `mkHom_f_0`: the degree-0 component is exactly the supplied `zero` morphism.)

- Claim: The degree-1 component of `VTask.mkHom P Q zero one h succ` equals `one`.
  (Follows from `mkHom_f_1`: the degree-1 component is exactly the supplied `one` morphism.)

- Claim: The degree-`(n+2)` component of `VTask.mkHom P Q zero one h succ` equals the first projection of `succ n ⟨f_n, f_{n+1}, comm_n⟩`, where `f_n`, `f_{n+1}` are the degree-`n` and degree-`(n+1)` components of the resulting chain map and `comm_n` is the commutativity proof between them.
  (Follows from `mkHom_f_succ_succ`: the inductive step `succ` is applied to the previous two components.)

- Claim: The morphism `VTask.mkHom P Q zero one h succ` is a valid chain map, meaning for every `n` the square `f n ≫ Q.d n (n+1) = P.d n (n+1) ≫ f (n+1)` commutes.
  (This is guaranteed by construction: each component comes paired with its commutativity proof.)

## Boundaries

- If `P` and `Q` are zero complexes (all objects are zero), then every morphism is zero and the constructor simply packages the zero morphisms; it still produces a valid chain map.
- The inductive step `succ` must be defined for every `n : ℕ`, so there is no finite truncation: the constructor works for the full ℕ-indexed complex.
- The constructor does not require the complexes to be bounded or to satisfy any finiteness condition.
- When the category `V` is abelian or has additional structure, the resulting chain map is still just a chain map at this level of generality; any exactness or other properties must be proved separately.

## Not to be confused with

- `HomologicalComplex.Hom` (the type of chain maps between homological complexes in general): `VTask.mkHom` is a *constructor* for an element of that type, not the type itself.
- `ChainComplex.mkHom` (a similar constructor for ℕ-indexed *chain* complexes, where the grading goes downward): this constructor targets *cochain* complexes where the grading goes upward.
- `CochainComplex.mk` (a constructor for cochain complexes themselves from inductive data): that builds the complex as an object, while `VTask.mkHom` builds a morphism between two already-given complexes.