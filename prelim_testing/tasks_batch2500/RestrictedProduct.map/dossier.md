## Object

`VTask.map` constructs a map between two restricted products over the same index type and filter, given a family of functions on the individual factor types. Concretely, if one has a family of functions `φ i : G i → H i` (one per index `i`) that almost everywhere (with respect to the filter `𝓕`) send the distinguished subsets `C i ⊆ G i` into the distinguished subsets `D i ⊆ H i`, then `VTask.map` lifts this data to a function from the restricted product `∏ʳ i, [G i, C i]_[𝓕]` to the restricted product `∏ʳ i, [H i, D i]_[𝓕]`. The resulting element at each index is simply `φ i` applied to the original element at that index.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {ι : Type u_1} -> {𝓕 : Filter ι} -> {G : ι → Type u_9} -> {H : ι → Type u_10} -> {C : (i : ι) → Set (G i)} -> {D : (i : ι) → Set (H i)} -> (φ : (i : ι) → G i → H i) -> (hφ : ∀ᶠ (i : ι) in 𝓕, Set.MapsTo (φ i) (C i) (D i)) -> (x : RestrictedProduct (fun i => G i) (fun i => C i) 𝓕) -> RestrictedProduct (fun i => H i) (fun i => D i) 𝓕
<!-- PINNED-SIGNATURE:END -->


`VTask.map : {ι : Type u_1} -> {𝓕 : Filter ι} -> {G : ι → Type u_9} -> {H : ι → Type u_10} -> {C : (i : ι) → Set (G i)} -> {D : (i : ι) → Set (H i)} -> (φ : (i : ι) → G i → H i) -> (hφ : ∀ᶠ (i : ι) in 𝓕, Set.MapsTo (φ i) (C i) (D i)) -> (x : RestrictedProduct (fun i => G i) (fun i => C i) 𝓕) -> RestrictedProduct (fun i => H i) (fun i => D i) 𝓕`

The implicit argument `ι` is the common index type. The implicit argument `𝓕` is the filter on the index type that determines which indices are considered "almost all"; together with the subsets `C i` and `D i`, it governs the membership condition for both restricted products. `G` and `H` are the source and target families of types, respectively. `C i` and `D i` are the distinguished subsets of `G i` and `H i` whose membership almost everywhere is required of elements of the corresponding restricted product. The explicit argument `φ` is the family of functions, one function `φ i : G i → H i` for each index `i`. The explicit argument `hφ` is the proof that, for `𝓕`-almost every index `i`, the function `φ i` maps the subset `C i` into `D i`; this is the condition needed to ensure that the image of a valid element of the source restricted product lies in the target restricted product. The explicit argument `x` is the element of the source restricted product to which the map is applied.

## Conventions

There are no junk-value conventions declared for this definition: the function is total on its stated domain, and every valid input produces a meaningful output with no degenerate or undefined cases.

## Worked examples

- Claim: For the identity family of functions (φ i = id), `VTask.map` with the trivially satisfied mapping condition acts as the identity on the restricted product (i.e., `(VTask.map (fun i => id) hφ x) j = x j` for all `j`).

- Claim: If `φ i : G i → H i` satisfies the mapping condition `hφ`, then for any element `x` of the source restricted product and any index `j`, the `j`-th component of `VTask.map φ hφ x` equals `φ j (x j)`.

- Claim: If `φ i` and `ψ i` are two families of functions with appropriate mapping conditions, then applying `VTask.map` for `φ` followed by `VTask.map` for `ψ` yields the same restricted-product element as applying `VTask.map` for the pointwise composition `fun i => ψ i ∘ φ i` (functoriality of the construction).

## Boundaries

- When the filter `𝓕` is the `⊤` filter (every set is large), the condition `hφ` requires that every `φ i` maps `C i` into `D i` without exception.
- When the filter `𝓕` is the cofinite filter, `hφ` only needs to hold for all but finitely many indices, which is the classical adèle-ring setup.
- The function `VTask.map` is defined for all valid inputs; there are no degenerate inputs where the result is undefined or arbitrary.
- If each `φ i` is continuous, then the induced map `VTask.map φ hφ` on restricted products is itself continuous (with respect to the restricted-product topology).

## Not to be confused with

- `RestrictedProduct.mapAlong`: a more general variant that additionally allows changing the index type via a function between index sets, not just mapping fibrewise within a fixed index type.
- `RestrictedProduct.inclusion`: maps a restricted product with a stricter membership condition (a principal filter on a subset) into one with a coarser condition, rather than changing the fibre types.
- `Pi.map`: the ordinary pointwise map on dependent products (Pi types) with no restricted-product membership structure or filter condition.