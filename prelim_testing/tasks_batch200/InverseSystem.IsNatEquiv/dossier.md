## Object

`VTask.IsNatEquiv` is the predicate asserting that a family of equivalences between the types `F j` and the "partial product" types `piLT X j` (indexed over a subset `s` of a preordered index set `ι`) forms a **natural transformation** with respect to the transition maps. Concretely, it says that for any two indices `k ≤ j` both lying in `s`, applying first the transition map `f` (going from `F j` to `F k`) and then the equivalence at `k` gives the same result as applying the equivalence at `j` first and then the canonical projection `piLTProj` from the product-below-`j` to the product-below-`k`. In other words, the equivalences intertwine the structure maps on the `F`-side with the canonical structure maps on the `piLT`-side.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsNatEquiv : {ι : Type u_1} -> [Preorder ι] -> {F : ι → Type u_4} -> {X : ι → Type u_5} -> (f : ⦃i j : ι⦄ → i ≤ j → F j → F i) -> {s : Set ι} -> (equiv : (j : ↑s) → F ↑j ≃ InverseSystem.piLT X ↑j) -> Prop
<!-- PINNED-SIGNATURE:END -->


The type string is inserted automatically above.

- `ι` is the type of indices, equipped with a preorder.
- `F` is a family of types over `ι`, the domain side of the equivalences.
- `X` is a family of types over `ι` that parametrises the codomain `piLT X j` (the product of `X i` over indices `i` strictly less than `j`).
- `f` is the family of transition maps: given `i ≤ j`, it provides a map `F j → F i`, making `F` into an inverse system.
- `s` is the subset of `ι` over which the equivalences are defined.
- `equiv` is the family of equivalences: for each index `j` in `s`, it provides an equivalence `F j ≃ piLT X j`.

## Conventions

No junk-value conventions are declared: the predicate is simply `False` (unsatisfied) for any input that fails the naturality square, and `True` (satisfied) for any input where all naturality squares commute. There are no implicit default or junk values to specify because the definition is a universally quantified `Prop` over a possibly empty domain.

## Worked examples

- Claim: If `s` is empty then `VTask.IsNatEquiv f equiv` holds vacuously for any `equiv`, because the universal quantification ranges over an empty set.

- Claim: For the canonical equivalences `piEquivLim` constructed from a limiting cone of an inverse system, `VTask.IsNatEquiv f (piEquivLim nat equivLim hi)` holds whenever the components of `equivLim x` are given by the transition maps, i.e., whenever `(equivLim x).1 l = f l.2.le x` for all `x` and `l`.

- Claim: If `VTask.IsNatEquiv f equiv` already holds, and a new equivalence `piEquivSucc equiv e hi` is built by extending `equiv` at a successor index using `e` satisfying `(e x).1 = f (le_succ i) x`, then `VTask.IsNatEquiv f (piEquivSucc equiv e hi)` also holds.

## Boundaries

- When `s` is a singleton `{j}`, there are no pairs `k ≤ j` with both in `s` and `k ≠ j` (unless `k = j`), so the condition is either vacuous or reduces to the single reflexive case where `h : j ≤ j`; in the reflexive case it requires that the equivalence commutes with the identity transition.
- The predicate is defined for any preorder on `ι`, not just a linear or well-founded order, so the naturality condition must hold for all comparable pairs in `s`, not just adjacent ones.
- Because the quantification is over all `k ≤ j` in `s` (not just immediate predecessors), transitivity of the condition is built into the statement: satisfying it for adjacent pairs in a well-founded setting implies it for all pairs, but the predicate directly requires all pairs.

## Not to be confused with

- `InverseSystem` (a typeclass asserting that the transition maps `f` themselves satisfy a functoriality/cocycle condition): `VTask.IsNatEquiv` instead concerns the equivalences `equiv`, not the maps `f` directly.
- `Equiv.trans` or pointwise equality of equivalences: `VTask.IsNatEquiv` is a commutativity/naturality square condition between two different equivalences mediated by structure maps, not a statement about a single equivalence.
- `piLT` itself (the partial product type `∏ i < j, X i`): `VTask.IsNatEquiv` uses `piLT` as the codomain but is a predicate on the family `equiv`, not a definition of the type itself.