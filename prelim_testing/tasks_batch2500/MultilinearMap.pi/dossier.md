## Object

Given a family of multilinear maps `f i : MultilinearMap R M₁ (M' i)` indexed by `i : ι'`, all sharing the same domain `M₁` (a family of modules over a common index `ι`), `VTask.pi f` is the single multilinear map whose codomain is the product space `∀ i : ι', M' i`, obtained by evaluating each component map independently: the output at a tuple `m` is the function `i ↦ f i m`.

In classical language: if you have a family of multilinear maps to different codomains, you can assemble them into one multilinear map to the Cartesian product by running each map in parallel on the same input.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pi : {R : Type uR} -> {ι : Type uι} -> {M₁ : ι → Type v₁} -> [Semiring R] -> [(i : ι) → AddCommMonoid (M₁ i)] -> [(i : ι) → Module R (M₁ i)] -> {ι' : Type u_1} -> {M' : ι' → Type u_2} -> [(i : ι') → AddCommMonoid (M' i)] -> [(i : ι') → Module R (M' i)] -> (f : (i : ι') → MultilinearMap R M₁ (M' i)) -> MultilinearMap R M₁ ((i : ι') → M' i)
<!-- PINNED-SIGNATURE:END -->


`VTask.pi : {R : Type uR} -> {ι : Type uι} -> {M₁ : ι → Type v₁} -> [Semiring R] -> [(i : ι) → AddCommMonoid (M₁ i)] -> [(i : ι) → Module R (M₁ i)] -> {ι' : Type u_1} -> {M' : ι' → Type u_2} -> [(i : ι') → AddCommMonoid (M' i)] -> [(i : ι') → Module R (M' i)] -> (f : (i : ι') → MultilinearMap R M₁ (M' i)) -> MultilinearMap R M₁ ((i : ι') → M' i)`

`R` is the commutative semiring of scalars. `ι` is the index type ranging over the domain factors, and `M₁` is the family of modules constituting the domain of all maps in the family. `ι'` is the index type for the family itself, and `M'` assigns to each `i : ι'` the codomain module of the `i`-th map. The argument `f` is the family of multilinear maps being combined: each `f i` is a multilinear map from the shared domain `M₁` to the module `M' i`.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total, structurally straightforward constructor that is well-defined for any valid family `f`, including the empty family when `ι'` is an empty type.

## Worked examples

- Claim: For any tuple `m : ∀ i : ι, M₁ i` and any index `j : ι'`, applying `VTask.pi f` to `m` and then projecting to component `j` equals `f j m`.

- Claim: When `ι'` is the two-element type `Fin 2` and `f 0`, `f 1` are two multilinear maps to modules `M' 0` and `M' 1` respectively, `VTask.pi f` is a single multilinear map whose value at any input `m` is the pair `(f 0 m, f 1 m)` in `M' 0 × M' 1` (interpreted as a dependent function `∀ i : Fin 2, M' i`).

- Claim: When `ι'` is empty (no component maps), `VTask.pi f` is the unique multilinear map to `∀ i : ι', M' i` (a one-element type), sending every input to the unique element.

- Claim: `VTask.pi f` is multilinear: for any position `k : ι`, any update to the `k`-th coordinate by an addition or scalar multiplication is reflected componentwise in each `f i`, since each `f i` is itself multilinear.

## Boundaries

- When the indexing type `ι'` is the empty type, the family `f` is vacuous and `VTask.pi f` maps every input to the unique element of the empty product type `∀ i : ι', M' i`, which is a one-element (terminal) type.
- When `ι` is a singleton, each multilinear map in the family reduces to a linear map, and `VTask.pi f` is the corresponding linear map to the product.
- The construction is valid for any semiring `R`, including non-commutative semirings; no commutativity of `R` is required.
- The domain index type `ι` may itself be empty, in which case each `f i` is a "nullary" multilinear map (a constant), and `VTask.pi f` is similarly a nullary multilinear map whose unique value is assembled from the constants.

## Not to be confused with

- `MultilinearMap.compLinearMap`: this precomposes a single multilinear map with linear maps on the domain, rather than assembling a family into a product codomain.
- `LinearMap.pi`: the analogous construction for *linear* (not multilinear) maps, assembling a family of linear maps into one map to a product; `VTask.pi` is its multilinear analogue.
- `ContinuousMultilinearMap.pi`: a topological variant of the same construction for continuous multilinear maps; `VTask.pi` carries no topology.
