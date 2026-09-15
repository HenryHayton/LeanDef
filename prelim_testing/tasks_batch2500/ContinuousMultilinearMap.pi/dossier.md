## Object

`VTask.pi` constructs a single continuous multilinear map whose codomain is a product (dependent-function) type `∀ i, M' i`, by packaging together a family of continuous multilinear maps, one for each index `i : ι'`, all sharing the same domain. Concretely, if for every index `i` you have a continuous multilinear map `f i : M₁ →[R] M' i` (abbreviating the multilinear structure), then `VTask.pi f` is the continuous multilinear map that sends an input tuple `m` to the function `i ↦ f i m`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pi : {R : Type u} -> {ι : Type v} -> {M₁ : ι → Type w₁} -> [Semiring R] -> [(i : ι) → AddCommMonoid (M₁ i)] -> [(i : ι) → Module R (M₁ i)] -> [(i : ι) → TopologicalSpace (M₁ i)] -> {ι' : Type u_1} -> {M' : ι' → Type u_2} -> [(i : ι') → AddCommMonoid (M' i)] -> [(i : ι') → TopologicalSpace (M' i)] -> [(i : ι') → Module R (M' i)] -> (f : (i : ι') → ContinuousMultilinearMap R M₁ (M' i)) -> ContinuousMultilinearMap R M₁ ((i : ι') → M' i)
<!-- PINNED-SIGNATURE:END -->


`VTask.pi : {R : Type u} -> {ι : Type v} -> {M₁ : ι → Type w₁} -> [Semiring R] -> [(i : ι) → AddCommMonoid (M₁ i)] -> [(i : ι) → Module R (M₁ i)] -> [(i : ι) → TopologicalSpace (M₁ i)] -> {ι' : Type u_1} -> {M' : ι' → Type u_2} -> [(i : ι') → AddCommMonoid (M' i)] -> [(i : ι') → TopologicalSpace (M' i)] -> [(i : ι') → Module R (M' i)] -> (f : (i : ι') → ContinuousMultilinearMap R M₁ (M' i)) -> ContinuousMultilinearMap R M₁ ((i : ι') → M' i)`

- `R` is the commutative semiring of scalars shared by all maps.
- `ι` is the index type for the domain family; the domain of each map in the family is the product `∀ i : ι, M₁ i`.
- `M₁` is the family of modules forming the multilinear domain.
- The instance arguments `[Semiring R]`, `[AddCommMonoid (M₁ i)]`, `[Module R (M₁ i)]`, `[TopologicalSpace (M₁ i)]` equip the domain with its algebraic and topological structure.
- `ι'` is the index type for the codomain family; each component of the output lives in a separate module.
- `M'` is the family of codomain modules, one for each `i : ι'`.
- The instance arguments `[AddCommMonoid (M' i)]`, `[TopologicalSpace (M' i)]`, `[Module R (M' i)]` equip each codomain component with its structure.
- `f` is the family of continuous multilinear maps being combined; `f i` maps the shared domain into the `i`-th codomain component `M' i`.

The result is the unique continuous multilinear map whose `i`-th component, for every `i : ι'`, equals `f i`.

## Conventions

There are no special junk-value or edge conventions for this definition: it is genuinely total and its behavior on every input is determined by the pointwise evaluation rule `(VTask.pi f) m i = f i m`.

## Worked examples

- Claim: For a family `f : ∀ i : ι', ContinuousMultilinearMap R M₁ (M' i)` and any input tuple `m : ∀ i, M₁ i`, evaluating `VTask.pi f m` at index `j` yields exactly `f j m`. (This is the `pi_apply` lemma.)

- Claim: When `ι'` has a single element (e.g., `ι' = Unit`) and `f : Unit → ContinuousMultilinearMap R M₁ (M' ())`, the map `VTask.pi f` is the continuous multilinear map sending `m` to the constant function at `f () m`.

- Claim: The underlying function (coercion) of `VTask.pi f` equals the function `fun m j => f j m`. (This is the `coe_pi` lemma.)

- Claim: In the normed setting, the operator norm of `VTask.pi f` equals the norm of the family `f` (viewed in the appropriate normed space), i.e., `‖VTask.pi f‖ = ‖f‖`.

## Boundaries

- When `ι'` is empty (`ι' = Empty` or an uninhabited type), `VTask.pi f` is the continuous multilinear map into the trivial one-point type `∀ i : Empty, M' i ≅ Unit`; the family `f` is vacuously empty, and the result is the unique such map.
- When `ι'` has exactly one element, `VTask.pi f` is essentially the same as `f` of that single element, up to the identification of `∀ _ : Unit, M' ()` with `M' ()`.
- The definition is total: no restrictions are placed on `ι`, `ι'`, or the modules beyond the stated typeclasses.
- Continuity of the output map is guaranteed automatically from the continuity of each component `f i`.

## Not to be confused with

- `MultilinearMap.pi`: the purely algebraic (non-topological) analogue that bundles a family of multilinear maps; `VTask.pi` adds and verifies joint continuity.
- `ContinuousLinearMap.pi`: the linear (not multilinear) version that combines a family of continuous linear maps into a product-valued continuous linear map; the domain there is a single module, not a product.
- `ContinuousMultilinearMap.piFieldEquiv`: a specific linear equivalence relating a scalar-field-valued iterated multilinear map to a function-type-valued one; this is an isomorphism, not the general pi-construction.
