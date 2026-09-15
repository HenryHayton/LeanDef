## Object

Given a family of continuous linear maps `f i : M →L[R] φ i` (one for each index `i` in an index type `ι`), `VTask.pi f` is the single continuous linear map `M →L[R] (∀ i, φ i)` that sends each element `m : M` to the tuple whose `i`-th component is `f i m`. This is the universal "diagonal" or "product" construction: the unique continuous linear map into a product of modules whose composition with each projection recovers the original components.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pi : {R : Type u_1} -> [Semiring R] -> {M : Type u_2} -> [TopologicalSpace M] -> [AddCommMonoid M] -> [Module R M] -> {ι : Type u_4} -> {φ : ι → Type u_5} -> [(i : ι) → TopologicalSpace (φ i)] -> [(i : ι) → AddCommMonoid (φ i)] -> [(i : ι) → Module R (φ i)] -> (f : (i : ι) → M →L[R] φ i) -> M →L[R] (i : ι) → φ i
<!-- PINNED-SIGNATURE:END -->


`VTask.pi : {R : Type u_1} -> [Semiring R] -> {M : Type u_2} -> [TopologicalSpace M] -> [AddCommMonoid M] -> [Module R M] -> {ι : Type u_4} -> {φ : ι → Type u_5} -> [(i : ι) → TopologicalSpace (φ i)] -> [(i : ι) → AddCommMonoid (φ i)] -> [(i : ι) → Module R (φ i)] -> (f : (i : ι) → M →L[R] φ i) -> M →L[R] (i : ι) → φ i`

The scalar semiring `R` governs linearity throughout. The domain module `M` is a topological `R`-module serving as the common source for all maps in the family. The index type `ι` parametrises the family; it can be any type, including infinite ones. The family `φ : ι → Type` assigns to each index a target type, each equipped with the structure of a topological `R`-module. The explicit argument `f` is the family of continuous linear maps, one per index, all sharing the same domain `M`.

## Conventions

There are no junk-value or out-of-domain conventions to declare: `VTask.pi` is defined for all valid inputs without any restriction, and every case is meaningful.

## Worked examples

- Claim: Evaluating `VTask.pi f` at a point `m : M` and then projecting to index `i` yields `f i m`. Formally, `VTask.pi f m i = f i m` for all `f`, `m`, `i`.

- Claim: When all component maps are zero, `VTask.pi (fun _ => 0) = 0` as continuous linear maps.

- Claim: Composing the `i`-th projection with `VTask.pi f` recovers `f i`, i.e., `proj i ∘L VTask.pi f = f i`.

- Claim: Applying `VTask.pi` to the family of projections `proj i : (∀ i, φ i) →L[R] φ i` yields the identity on `∀ i, φ i`.

## Boundaries

- When the index type `ι` is empty (`ι = Empty` or `ι = Fin 0`), the construction still makes sense and produces the unique continuous linear map into the trivial product type, which is the zero map.
- When `ι` has a single element, `VTask.pi f` is essentially the same (up to isomorphism) as `f` itself composed with the obvious identification.
- When `ι` is infinite, the target carries the product topology (pointwise convergence), and continuity of `VTask.pi f` is inherited from continuity of each `f i`.
- If the family `f` is constant — all components are the same map `g` — then `VTask.pi (fun _ => g)` sends each `m` to the constant tuple `fun _ => g m`.

## Not to be confused with

- `ContinuousLinearMap.piMap`: maps a family of continuous linear maps `φ i →L[R] ψ i` to a single continuous linear map `(∀ i, φ i) →L[R] (∀ i, ψ i)`, acting component-wise on a product-to-product rather than a single-module-to-product.
- `LinearMap.pi`: the purely algebraic (non-topological) analogue, which does not require or verify continuity of the resulting map.
- `ContinuousLinearMap.prod`: the binary version pairing two maps `M →L[R] N` and `M →L[R] P` into `M →L[R] N × P`, which is the special case of `VTask.pi` for a two-element index but presented as a separate constructor.