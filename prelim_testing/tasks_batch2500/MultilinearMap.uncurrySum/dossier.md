## Object

`VTask.uncurrySum` takes a "doubly curried" multilinear map — one that is multilinear in the left-index variables and whose values are themselves multilinear maps in the right-index variables — and flattens it into a single multilinear map indexed by the disjoint union type `ι ⊕ ι'`. Concretely, given modules `N(Sum.inl i)` for `i : ι` and `N(Sum.inr i')` for `i' : ι'`, it converts a multilinear map from the `ι`-family to the space of multilinear maps from the `ι'`-family into `M₂`, yielding a single multilinear map on the full `ι ⊕ ι'`-indexed family with values in `M₂`. This is the "uncurrying" direction of the canonical isomorphism between these two formulations.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.uncurrySum : {R : Type uR} -> {ι : Type uι} -> {ι' : Type uι'} -> {M₂ : Type v₂} -> [CommSemiring R] -> [AddCommMonoid M₂] -> [Module R M₂] -> {N : ι ⊕ ι' → Type u_1} -> [(i : ι ⊕ ι') → AddCommMonoid (N i)] -> [(i : ι ⊕ ι') → Module R (N i)] -> (g : MultilinearMap R (fun i => N (Sum.inl i)) (MultilinearMap R (fun i => N (Sum.inr i)) M₂)) -> MultilinearMap R N M₂
<!-- PINNED-SIGNATURE:END -->


VTask.uncurrySum : {R : Type uR} -> {ι : Type uι} -> {ι' : Type uι'} -> {M₂ : Type v₂} -> [CommSemiring R] -> [AddCommMonoid M₂] -> [Module R M₂] -> {N : ι ⊕ ι' → Type u_1} -> [(i : ι ⊕ ι') → AddCommMonoid (N i)] -> [(i : ι ⊕ ι') → Module R (N i)] -> (g : MultilinearMap R (fun i => N (Sum.inl i)) (MultilinearMap R (fun i => N (Sum.inr i)) M₂)) -> MultilinearMap R N M₂

`R` is the commutative semiring of scalars. `ι` is the index type for the left (inner) family of modules, and `ι'` is the index type for the right (outer) family. `M₂` is the target module. `N` is the family of modules indexed by `ι ⊕ ι'`, so `N (Sum.inl i)` is the `i`-th left module and `N (Sum.inr i')` is the `i'`-th right module. The argument `g` is the curried multilinear map: it is multilinear in the left-indexed variables `N (Sum.inl i)` and produces, for each such input, a multilinear map in the right-indexed variables `N (Sum.inr i')` with values in `M₂`.

## Conventions

The resulting multilinear map evaluates at a vector `u : (i : ι ⊕ ι') → N i` by splitting `u` along the sum: it applies `g` to the restriction `fun i ↦ u (Sum.inl i)` and then applies the resulting multilinear map to the restriction `fun i' ↦ u (Sum.inr i')`. There are no junk-value conventions: the construction is total and well-defined for all inputs in its domain.

## Worked examples

- Claim: For any multilinear map `f : MultilinearMap R N M₂` over a sum-indexed family, applying `VTask.uncurrySum` to `currySum f` recovers `f` exactly (the round-trip `uncurrySum ∘ currySum = id`).

- Claim: For any curried map `g`, applying `currySum` to `VTask.uncurrySum g` recovers `g` (the round-trip `currySum ∘ uncurrySum = id`).

- Claim: `VTask.uncurrySum` is additive: `VTask.uncurrySum (g₁ + g₂) = VTask.uncurrySum g₁ + VTask.uncurrySum g₂`.

- Claim: `VTask.uncurrySum` is compatible with scalar multiplication: for any scalar `r`, `VTask.uncurrySum (r • g) = r • VTask.uncurrySum g`.

## Boundaries

- When `ι` is empty (`ι = Empty` or `Fin 0`), `g` is a multilinear map on an empty family, which is effectively a constant element of the space of multilinear maps on the `ι'`-family. The result of `VTask.uncurrySum g` is then a multilinear map depending only on the `ι'`-indexed variables.
- When `ι'` is empty, symmetrically, `g` takes values in a multilinear map on an empty family (effectively a scalar), and the result depends only on the `ι`-indexed variables.
- When both index types are empty, the result is a constant multilinear map (a zero-linear map).
- The construction is an isomorphism: it has a two-sided inverse given by `currySum`, and together they form the linear equivalence `currySumEquiv`.

## Not to be confused with

- `MultilinearMap.currySum`: the inverse operation, which takes a multilinear map on `ι ⊕ ι'` and produces the curried version (multilinear in left variables, valued in multilinear maps in right variables).
- `MultilinearMap.currySumEquiv`: the bundled linear equivalence packaging both `currySum` and `uncurrySum` as an invertible linear map, as opposed to the bare map construction here.
- Ordinary function uncurrying (`Function.uncurry`): that operates on functions `A → B → C` becoming `A × B → C`, not on multilinear maps over sum-indexed module families.