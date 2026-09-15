## VTask.IsHomeomorphicTrivialFiberBundle

### Object

A predicate asserting that a given surjection `proj : Z → B` makes `Z` a **trivial fiber bundle** with fiber `F` over the base `B`, in the sense that `Z` is homeomorphic to the Cartesian product `B × F` via a homeomorphism that intertwines `proj` with the first-coordinate projection `Prod.fst : B × F → B`. In other words, the bundle `proj : Z → B` is isomorphic, as a bundle over `B`, to the trivially-foliated product `B × F`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsHomeomorphicTrivialFiberBundle : {B : Type u_1} -> (F : Type u_2) -> {Z : Type u_3} -> [TopologicalSpace B] -> [TopologicalSpace F] -> [TopologicalSpace Z] -> (proj : Z → B) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsHomeomorphicTrivialFiberBundle : {B : Type u_1} -> (F : Type u_2) -> {Z : Type u_3} -> [TopologicalSpace B] -> [TopologicalSpace F] -> [TopologicalSpace Z] -> (proj : Z → B) -> Prop`

`B` is the base space of the bundle, supplied implicitly. `F` is the fiber type, supplied explicitly; it carries the topology of a typical fiber. `Z` is the total space of the bundle, supplied implicitly. The three topology instance arguments equip `B`, `F`, and `Z` with their respective topological structures. `proj` is the bundle projection — the map from the total space `Z` to the base `B` whose fibers one wants to identify with `F`.

### Conventions

The fiber type `F` appears as an explicit argument even though the topology on it is provided by an implicit instance; this is because the fiber determines the _type_ of the homeomorphism witness and must be fixed before the proposition can be stated. The base `B` and total space `Z` are implicit because they are typically inferred from `proj`. There are no junk-value conventions: the proposition is simply `False` (has no proof) for any `proj` that genuinely fails to be a trivial fiber bundle; no special convention is needed for degenerate inputs.

### Worked examples

- Claim: `VTask.IsHomeomorphicTrivialFiberBundle F (Prod.fst : B × F → B)` holds for any topological spaces `B` and `F` — the identity homeomorphism witnesses that the product projection is trivially a fiber bundle.

- Claim: `VTask.IsHomeomorphicTrivialFiberBundle ℝ Complex.re` holds — the real part map `ℝe : ℂ → ℝ` makes the complex plane a trivial real line bundle over `ℝ`, with the homeomorphism `ℂ ≃ₜ ℝ × ℝ` sending `re` to `Prod.fst`.

- Claim: `VTask.IsHomeomorphicTrivialFiberBundle ℝ Complex.im` holds — the imaginary part map `ℂ → ℝ` similarly makes `ℂ` a trivial fiber bundle over `ℝ`.

- Claim: If `h : VTask.IsHomeomorphicTrivialFiberBundle F proj` and `F` is nonempty, then `proj` is surjective.

- Claim: If `h : VTask.IsHomeomorphicTrivialFiberBundle F proj`, then `proj` is continuous and is an open map.

### Boundaries

- When `F` is the empty type, there are no points in any fiber. The homeomorphism `Z ≃ₜ B × F ≅ ∅` would force `Z` to be empty, so the property can only hold if `Z` (and hence the domain of `proj`) is empty. In this degenerate case surjectivity of `proj` fails if `B` is nonempty.
- When `F` is a singleton (one-point space), the property reduces to `Z` being homeomorphic to `B` via `proj` itself, since `B × {*} ≅ B`.
- The property is purely topological: it requires an actual _homeomorphism_, not merely a continuous bijection, to `B × F` over `B`. A continuous bijection that is not a homeomorphism does not suffice.
- The homeomorphism required is global (over all of `B`); local trivialisations are a weaker notion handled by `IsFiberBundle` / `FiberBundle`, not by this predicate.

### Not to be confused with

- `FiberBundle` / `IsFiberBundle`: a fiber bundle that is only **locally** trivial over `B`; `VTask.IsHomeomorphicTrivialFiberBundle` is the strictly stronger **global** triviality.
- `VTask.IsHomeomorphicTrivialFiberBundle F Prod.snd`: this is also true but uses the _second_ coordinate of a swapped product `F × B → B` as the projection, not the standard `Prod.fst`.
- A mere continuous surjection `proj : Z → B` with homeomorphic fibers: this does not imply global triviality, which additionally requires the homeomorphism to be compatible with the base projection.