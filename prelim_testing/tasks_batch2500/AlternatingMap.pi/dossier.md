## Object

`VTask.pi` constructs a single alternating multilinear map whose codomain is a product (pi) type from a family of alternating multilinear maps sharing the same domain. Given a family `f i` of alternating `R`-multilinear maps from `ι`-tuples of elements of `M` into each `N i`, it produces one alternating map that sends an `ι`-tuple `v` to the function `i ↦ f i v`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pi : {R : Type u_1} -> [Semiring R] -> {M : Type u_2} -> [AddCommMonoid M] -> [Module R M] -> {ι : Type u_7} -> {ι' : Type u_10} -> {N : ι' → Type u_11} -> [(i : ι') → AddCommMonoid (N i)] -> [(i : ι') → Module R (N i)] -> (f : (i : ι') → M [⋀^ι]→ₗ[R] N i) -> M [⋀^ι]→ₗ[R] ((i : ι') → N i)
<!-- PINNED-SIGNATURE:END -->


`{R : Type u_1} -> [Semiring R] -> {M : Type u_2} -> [AddCommMonoid M] -> [Module R M] -> {ι : Type u_7} -> {ι' : Type u_10} -> {N : ι' → Type u_11} -> [(i : ι') → AddCommMonoid (N i)] -> [(i : ι') → Module R (N i)] -> (f : (i : ι') → M [⋀^ι]→ₗ[R] N i) -> M [⋀^ι]→ₗ[R] ((i : ι') → N i)`

`R` is the commutative semiring of scalars. `M` is the shared input module whose `ι`-tuples form the domain. `ι` is the index type for input slots (determining the arity). `ι'` is the index type for the family of maps. `N` assigns to each index `i : ι'` the codomain module for the `i`-th component map. The argument `f` is the family: for each `i : ι'`, `f i` is an alternating `R`-multilinear map from `ι`-tuples in `M` to `N i`.

## Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a total construction that behaves uniformly for all valid inputs, including when `ι'` is empty (in which case the codomain is a trivial unit-like pi type and the resulting map sends everything to the unique element) or when `ι` is empty.

## Worked examples

- Claim: Evaluating `VTask.pi f` at a tuple `v : ι → M` and then projecting to component `i` equals `f i v`. That is, `(VTask.pi f v) i = f i v` for all `i : ι'`.

- Claim: When `ι'` has two elements and `f` assigns one alternating map to each, `VTask.pi f` is the alternating map whose value at `v` is the pair `(f 0 v, f 1 v)`, meaning it simultaneously tracks both components in a product-valued output.

- Claim: If every `f i` maps any tuple with two equal entries to zero (as required by the alternating condition), then `VTask.pi f` also maps any such tuple to the zero function, since each component `(VTask.pi f v) i = f i v = 0`.

## Boundaries

- When `ι'` is the empty type, the pi type `(i : ι') → N i` is a trivial type with a unique element; `VTask.pi` applied to the vacuously empty family yields the unique alternating map into that trivial type.
- When `ι` is the empty type, alternating maps have arity zero and amount to constant maps; `VTask.pi` still applies and packages the family of constants into a single constant map valued in the pi type.
- The construction requires only a `Semiring` on `R` (not commutativity), so it applies in that generality.
- The alternating property (vanishing on tuples with repeated entries) of the result follows componentwise from the alternating property of each `f i`.

## Not to be confused with

- `MultilinearMap.pi`: the analogous construction for multilinear maps without the alternating condition; `VTask.pi` is its alternating refinement.
- `AlternatingMap.compLinearMap`: applies a linear map *after* a single alternating map, rather than combining a family of alternating maps into a product-valued one.
- `LinearMap.pi`: combines a family of linear maps (arity 1) into a product-valued linear map; `VTask.pi` is the higher-arity alternating analogue.