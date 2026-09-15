## Object

`VTask.compRightL` constructs, from a function `f : α → ι`, a continuous linear map that sends any tuple `v : (i : ι) → φ i` (indexed by `ι`) to the reindexed tuple `(i : α) ↦ v (f i)` (indexed by `α`). In other words, it is the operation of "pre-composing with `f`" on the right: it pulls a `ι`-indexed family of values back along `f` to produce an `α`-indexed family. This is a continuous linear map between product (Pi) types equipped with their product topology and module structure.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.compRightL : (R : Type u_1) -> [Semiring R] -> {ι : Type u_4} -> (φ : ι → Type u_5) -> [(i : ι) → TopologicalSpace (φ i)] -> [(i : ι) → AddCommMonoid (φ i)] -> [(i : ι) → Module R (φ i)] -> {α : Type u_6} -> (f : α → ι) -> ((i : ι) → φ i) →L[R] (i : α) → φ (f i)
<!-- PINNED-SIGNATURE:END -->


`VTask.compRightL : (R : Type u_1) -> [Semiring R] -> {ι : Type u_4} -> (φ : ι → Type u_5) -> [(i : ι) → TopologicalSpace (φ i)] -> [(i : ι) → AddCommMonoid (φ i)] -> [(i : ι) → Module R (φ i)] -> {α : Type u_6} -> (f : α → ι) -> ((i : ι) → φ i) →L[R] (i : α) → φ (f i)`

The first explicit argument `R` is the scalar semiring over which the continuous linear map is defined. The type family `φ` assigns to each element of the index type `ι` the type of the corresponding component; it determines both the domain and the codomain. The argument `f : α → ι` is the reindexing function: it specifies how the smaller (or differently-shaped) index type `α` maps into `ι`, thereby controlling which components of a `ι`-tuple are selected (and in what order) in the output `α`-tuple.

## Conventions

There are no declared junk-value or edge conventions for this definition: it is a total construction that applies for any function `f : α → ι` without restriction, and produces a well-defined continuous linear map in all cases.

## Worked examples

- Claim: When `f` is the identity on `ι`, `VTask.compRightL R φ (id : ι → ι)` maps any tuple `v` to itself.

- Claim: For `ι = Fin 3`, `α = Fin 2`, and `f i = ⟨i.val, ...⟩` (an embedding of `Fin 2` into `Fin 3`), applying `VTask.compRightL R φ f` to a tuple `v : (i : Fin 3) → φ i` yields the two-component tuple `![v 0, v 1]`.

- Claim: When `f = Subtype.val` for some predicate `p : ι → Prop`, `VTask.compRightL R φ (Subtype.val)` applied to `v : (i : ι) → φ i` gives the restriction of `v` to the subtype, forgetting all components outside the subtype.

- Claim: `VTask.compRightL R φ f` is a linear map, so it satisfies `VTask.compRightL R φ f (u + v) = VTask.compRightL R φ f u + VTask.compRightL R φ f v` for all `u v`.

## Boundaries

- If `α` is empty (`α = PEmpty` or `α = Fin 0`), then `f` is the unique function from the empty type, and the resulting continuous linear map sends every `ι`-tuple to the unique empty tuple; this is well-defined.
- If `f` is not injective, multiple indices in `α` may map to the same index in `ι`, causing the same component of the input tuple to appear multiple times in the output; this is perfectly valid.
- If `f` is surjective onto `ι`, then every component of the input is used at least once.
- If `α = ι` and `f = id`, the map is essentially the identity (as a continuous linear map).
- The map is always continuous because it is a projection/restriction on product spaces, which are continuous by the universal property of the product topology.

## Not to be confused with

- The analogous left-composition map, which instead post-composes fiberwise linear maps rather than reindexing the product.
- `LinearMap.pi` or `ContinuousLinearMap.pi`, which construct a map *into* a product type by assembling component maps, rather than reindexing an existing product.
- The projection `ContinuousLinearMap.proj`, which selects a single component `v i` from a product, rather than pulling back along an arbitrary function `f`.