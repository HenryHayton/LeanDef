## Object

`VTask.piMap` constructs a single continuous `R`-linear map from the product space `(∀ i, φ i)` to the product space `(∀ i, ψ i)` by acting on each coordinate `i` independently via the supplied continuous linear map `f i : φ i →L[R] ψ i`. Concretely, if `x : ∀ i, φ i`, then the resulting map sends `x` to the function `i ↦ f i (x i)`, which is exactly `Pi.map (fun i ↦ f i)`. When the index type `ι` is finite this is the block-diagonal continuous linear map between the indexed products.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.piMap : {R : Type u_1} -> [Semiring R] -> {ι : Type u_4} -> {φ : ι → Type u_5} -> [(i : ι) → TopologicalSpace (φ i)] -> [(i : ι) → AddCommMonoid (φ i)] -> [(i : ι) → Module R (φ i)] -> {ψ : ι → Type u_6} -> [(i : ι) → TopologicalSpace (ψ i)] -> [(i : ι) → AddCommMonoid (ψ i)] -> [(i : ι) → Module R (ψ i)] -> (f : (i : ι) → φ i →L[R] ψ i) -> ((i : ι) → φ i) →L[R] (i : ι) → ψ i
<!-- PINNED-SIGNATURE:END -->


The definition is parameterised by:
- A semiring `R` that serves as the scalar ring for all modules involved.
- An index type `ι` whose elements label the coordinates.
- A family `φ : ι → Type` of source modules, each carrying a topology, additive commutative monoid structure, and `R`-module structure.
- A family `ψ : ι → Type` of target modules, similarly equipped.
- The key explicit argument `f` is a family of continuous `R`-linear maps — one per index `i` — mapping the `i`-th source module `φ i` to the `i`-th target module `ψ i`.

The result is the single continuous `R`-linear map from the dependent product `(∀ i, φ i)` to the dependent product `(∀ i, ψ i)` that applies `f i` coordinatewise.

## Conventions

No junk-value or edge-case conventions are declared for this definition: it is a total construction that is well-defined for any family `f` of continuous linear maps, including the empty family (when `ι` is uninhabited), in which case both domain and codomain are trivial and the map is the unique such continuous linear map.

## Worked examples

- Claim: Applying `VTask.piMap f` to a point `x : ∀ i, φ i` yields the function `i ↦ f i (x i)`, i.e., `⇑(VTask.piMap f) x = fun i ↦ f i (x i)` — this follows because the underlying function equals `Pi.map (fun i ↦ f i)`.

- Claim: When `R = ℝ`, `ι = Fin 2`, `φ i = ℝ`, `ψ i = ℝ`, and `f i = ContinuousLinearMap.id ℝ ℝ` for all `i`, the map `VTask.piMap f` sends every `x : Fin 2 → ℝ` to itself, i.e., it is the identity on `Fin 2 → ℝ`.

- Claim: `VTask.piMap (fun i ↦ g i ∘L f i) = VTask.piMap g ∘L VTask.piMap f` for composable families `f` and `g`, expressing that the construction is functorial (respects composition coordinatewise).

- Claim: `VTask.piMap (fun i ↦ ContinuousLinearMap.id R (φ i)) = ContinuousLinearMap.id R (∀ i, φ i)`, expressing that the block-diagonal of identity maps is the identity.

## Boundaries

- When `ι` is the empty type, both `(∀ i, φ i)` and `(∀ i, ψ i)` are singleton types and the resulting continuous linear map is the unique continuous linear map between them, regardless of `f`.
- When `ι` has exactly one element, `VTask.piMap f` is (up to the canonical isomorphism) just the single continuous linear map `f` for that element.
- The definition requires no finiteness assumption on `ι`; it is valid for infinite index types as long as the product topologies and module structures are present.
- Continuity of the output map is guaranteed by the continuity of each `f i` together with the product topology, so no additional continuity hypotheses are needed beyond those already bundled in each `f i`.

## Not to be confused with

- `ContinuousLinearMap.pi` — builds a continuous linear map *into* a product `(∀ i, φ i)` from a family of maps each landing in one coordinate, rather than acting *on* a product coordinatewise.
- `LinearMap.piMap` (the unbundled linear-algebraic version) — the same coordinatewise action but without continuity data or the topological structure.
- `Pi.map` (the bare function-level construction) — applies a family of functions coordinatewise with no linearity or continuity structure bundled.