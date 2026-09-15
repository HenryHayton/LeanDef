## Object

The *inclusion map* for restricted products: given two filters `𝓕 ≤ 𝓖` on an index type `ι`, every element of the restricted product `Πʳ i, [R i, A i]_[𝓖]` — whose underlying tuple belongs to `A i` for `𝓖`-almost all indices — is automatically an element of the coarser restricted product `Πʳ i, [R i, A i]_[𝓕]`, since every set that is large with respect to `𝓖` is also large with respect to the smaller filter `𝓕`. The map `VTask.inclusion` realises this canonical injection: it sends an element of the `𝓖`-restricted product to the same underlying tuple viewed as an element of the `𝓕`-restricted product.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.inclusion : {ι : Type u_1} -> (R : ι → Type u_2) -> (A : (i : ι) → Set (R i)) -> {𝓕 𝓖 : Filter ι} -> (h : 𝓕 ≤ 𝓖) -> (x : RestrictedProduct (fun i => R i) (fun i => A i) 𝓖) -> RestrictedProduct (fun i => R i) (fun i => A i) 𝓕
<!-- PINNED-SIGNATURE:END -->


`VTask.inclusion : {ι : Type u_1} -> (R : ι → Type u_2) -> (A : (i : ι) → Set (R i)) -> {𝓕 𝓖 : Filter ι} -> (h : 𝓕 ≤ 𝓖) -> (x : RestrictedProduct (fun i => R i) (fun i => A i) 𝓖) -> RestrictedProduct (fun i => R i) (fun i => A i) 𝓕`

The argument `R` is the family of types indexed by `ι` from which the product is built. The argument `A` assigns to each index `i` a distinguished subset `A i` of `R i`; membership in this subset for almost all indices is the restricted-product condition. The argument `h` is the proof that the filter `𝓕` is coarser than (i.e., contained in or equal to) `𝓖`; it is precisely this inequality that makes the inclusion well-defined. The argument `x` is the element of the `𝓖`-restricted product being mapped.

## Conventions

The map acts pointwise on the underlying tuple: evaluating `VTask.inclusion R A h x` at any index `i` yields the same value as evaluating `x` at `i`. There are no junk values because the function is total; every input produces a well-typed output.

## Worked examples

- Claim: Applying `VTask.inclusion R A h x` at any index `i` gives the same value as `x i`.

  (This follows directly from the `inclusion_apply` lemma: for all valid arguments, `VTask.inclusion R A h x i = x i`.)

- Claim: When `𝓕 = 𝓖` and `h` is the reflexivity proof `le_refl 𝓕`, the map `VTask.inclusion R A h` equals the identity function on the restricted product.

  (This is the content of `inclusion_eq_id`: `VTask.inclusion R A (le_refl 𝓕) = id`.)

- Claim: The range of `VTask.inclusion R A h` (for `h : 𝓕 ≤ 𝓖`) consists exactly of those elements `x` of the `𝓕`-restricted product satisfying `∀ᶠ i in 𝓖, x i ∈ A i`.

  (This characterises exactly which elements of the larger restricted product lie in the image of the inclusion.)

- Claim: The map `VTask.inclusion R A h` is continuous for any `h : 𝓕 ≤ 𝓖`, when the restricted products carry their natural topologies.

## Boundaries

- When `𝓕 = 𝓖` (equal filters, `h` is `le_refl`), the inclusion is the identity map.
- When `𝓖 = ⊤` (the principal filter of all sets, or the discrete filter), every tuple satisfies the `A`-condition for `𝓖`-almost all indices trivially, so the inclusion from `Πʳ i, [R i, A i]_[⊤]` into any restricted product is an embedding.
- When `𝓖` is the principal filter of a finite set `S` (so `cofinite ≤ 𝓟 S` fails), the inclusion may not be an open embedding; open embedding holds exactly when `cofinite ≤ 𝓟 S`.
- The inclusion is always injective (it does not change the underlying tuple), and it is always continuous.

## Not to be confused with

- `RestrictedProduct` itself — that is the *type* of restricted product elements; `VTask.inclusion` is the *map* between two such types.
- The coercion `DFunLike.coe` from a restricted product to the full product type `Π i, R i` — that forgets the filter condition entirely, whereas `VTask.inclusion` changes the filter but keeps the element inside a restricted product.
- Direct product inclusions such as `Pi.map` — those change the individual component types or component maps, while `VTask.inclusion` keeps all components fixed and only relaxes the almost-everywhere condition.