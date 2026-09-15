## VTask.structureMap

### Object

The *structure map* of the restricted product is the canonical inclusion map that sends a family of elements `x`, where each `x i` lies in the distinguished subset `A i` of `R i`, into the restricted product `Πʳ i, [R i, A i]_[𝓕]`. Because every component `x i` is already in `A i`, the condition required for membership in the restricted product (that `x i ∈ A i` for `𝓕`-almost all `i`) is satisfied trivially and unconditionally. Thus the structure map is an injection from `Π i, A i` (the full product of the subsets) into the restricted product.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.structureMap : {ι : Type u_1} -> (R : ι → Type u_2) -> (A : (i : ι) → Set (R i)) -> (𝓕 : Filter ι) -> (x : (i : ι) → ↑(A i)) -> RestrictedProduct (fun i => R i) (fun i => A i) 𝓕
<!-- PINNED-SIGNATURE:END -->


`VTask.structureMap : {ι : Type u_1} -> (R : ι → Type u_2) -> (A : (i : ι) → Set (R i)) -> (𝓕 : Filter ι) -> (x : (i : ι) → ↑(A i)) -> RestrictedProduct (fun i => R i) (fun i => A i) 𝓕`

The implicit argument `ι` is the index type ranging over the family. The argument `R` assigns to each index `i` the ambient type (e.g. a ring or topological space). The argument `A` assigns to each `i` a distinguished subset of `R i` (the "open compact" or "integral" subsets in typical adèle-ring constructions). The argument `𝓕` is a filter on `ι` encoding the notion of "almost all" indices: an element of the restricted product must lie in `A i` for `𝓕`-almost all `i`. The argument `x` is a dependent function selecting, for each index `i`, a specific element of the subtype `A i`.

### Conventions

There are no junk-value or default-value conventions for this definition: it is a total, well-defined construction on all valid inputs and produces a genuine element of the restricted product rather than relying on any fallback.

### Worked examples

- Claim: For any `x : Π i, A i` and any index `i`, the `i`-th component of `VTask.structureMap R A 𝓕 x` (viewed as an element of `R i`) equals the value of `x i` (viewed as an element of `R i`).

- Claim: The range of `VTask.structureMap R A 𝓕` (as a function to the restricted product) is exactly the set of elements `f` of the restricted product such that `f.1 i ∈ A i` for every `i` — i.e., it picks out those elements of the restricted product whose underlying function lands in `A i` everywhere, not just almost everywhere.

- Claim: `VTask.structureMap R A 𝓕` is an embedding (in the topological sense), so in particular it is injective.

- Claim: When `𝓕` is the cofinite filter, `VTask.structureMap R A cofinite` is an open embedding.

### Boundaries

- When every set `A i` equals the whole type `R i`, the restricted product collapses to the full dependent product, and the structure map becomes the identity (up to the coercion from subtypes).
- The structure map is always injective: two families `x` and `y` in `Π i, A i` map to the same element of the restricted product if and only if they agree at every index.
- The filter `𝓕` plays no role in whether the map is well-defined (the membership condition holds for all indices, hence in particular for almost all), but it does affect the topology and the ambient restricted product that the map targets.
- The image of the structure map is a proper subset of the restricted product whenever there exist elements of the restricted product whose underlying function fails to lie in `A i` for some index `i`.

### Not to be confused with

- The *inclusion* of a single fibre `R i` into the restricted product (sometimes called a partial or diagonal map), which fixes one index and uses a distinguished element elsewhere — the structure map instead specifies all components simultaneously via `Π i, A i`.
- The *coercion* or *underlying function* of a `RestrictedProduct` element back to `Π i, R i`, which goes in the opposite direction.
- The *diagonal map* `Π i, R i → RestrictedProduct`, which would include elements not constrained to lie in `A i`; the structure map's domain is the smaller type `Π i, ↑(A i)`.