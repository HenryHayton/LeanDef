## Object

A cochain of degree `n` between two cochain complexes `F` and `G` (indexed by `ℤ`) is a family of morphisms: for every pair of integers `(p, q)` satisfying `p + n = q`, there is a morphism `F.X p ⟶ G.X q`. The definition `VTask.v` extracts that single morphism component from the cochain, given the source index `p`, the target index `q`, and the proof that these indices are correctly offset by `n`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.v : {C : Type u} -> [CategoryTheory.Category.{v, u} C] -> [CategoryTheory.Preadditive C] -> {F G : CochainComplex C ℤ} -> {n : ℤ} -> (γ : CochainComplex.HomComplex.Cochain F G n) -> (p q : ℤ) -> (hpq : p + n = q) -> F.X p ⟶ G.X q
<!-- PINNED-SIGNATURE:END -->


`VTask.v : {C : Type u} -> [CategoryTheory.Category.{v, u} C] -> [CategoryTheory.Preadditive C] -> {F G : CochainComplex C ℤ} -> {n : ℤ} -> (γ : CochainComplex.HomComplex.Cochain F G n) -> (p q : ℤ) -> (hpq : p + n = q) -> F.X p ⟶ G.X q`

- `C` is the ambient preadditive category whose objects form the coefficients of the complexes.
- `F` and `G` are cochain complexes over `C` indexed by the integers.
- `n` is the degree of the cochain `γ`, meaning `γ` shifts indices by `n`.
- `γ` is the cochain being evaluated; it is a degree-`n` cochain from `F` to `G`.
- `p` is the source integer index (selecting the object `F.X p` in `F`).
- `q` is the target integer index (selecting the object `G.X q` in `G`).
- `hpq` is the proof that `p + n = q`, certifying that the pair `(p, q)` is a valid index pair for a degree-`n` cochain.

The result is the specific morphism `F.X p ⟶ G.X q` that `γ` assigns to this pair.

## Conventions

The domain of `VTask.v` is unrestricted: every integer pair `(p, q)` and every valid proof `hpq : p + n = q` is accepted, and the function is total. There are no junk-value conventions declared, since the proof `hpq` structurally guarantees that the requested component exists.

## Worked examples

- Claim: For the zero cochain of degree `n`, the value `VTask.v 0 p q hpq` is the zero morphism `0 : F.X p ⟶ G.X q`.

- Claim: If `γ` and `δ` are two degree-`n` cochains, then `VTask.v (γ + δ) p q hpq = VTask.v γ p q hpq + VTask.v δ p q hpq` — that is, extracting a component is additive in the cochain argument.

- Claim: For the identity cochain of degree `0` on a complex `F`, the value at `(p, p, rfl)` is the identity morphism `𝟙 (F.X p)`.

## Boundaries

- When `n = 0`, the condition `hpq : p + 0 = q` forces `q = p`, so each component lives on the diagonal: `F.X p ⟶ G.X p`.
- When `n = 1`, only pairs with `q = p + 1` are valid index pairs, and `VTask.v γ p (p+1) (by ring)` extracts the morphism at that pair.
- The proof `hpq` is used purely as a key to select the component; if two proofs `h` and `h'` satisfy `p + n = q`, they are equal (since `ℤ` equality of integers is a proposition), and `VTask.v γ p q h = VTask.v γ p q h'` holds by proof irrelevance.
- The function is defined for all integers, including negative indices, with no exceptional behaviour.

## Not to be confused with

- `CochainComplex.HomComplex.Cochain`: the full cochain itself (the entire family of morphisms), not a single extracted component.
- `CochainComplex.Hom`: a chain map between complexes, which is a degree-`0` cochain that also commutes with the differentials; `VTask.v` works for cochains of any degree, not just chain maps.
- Evaluation of a natural transformation at an object: although superficially similar (picking out one component), `VTask.v` specifically concerns `ℤ`-indexed cochain complexes and enforces the offset condition `p + n = q`.