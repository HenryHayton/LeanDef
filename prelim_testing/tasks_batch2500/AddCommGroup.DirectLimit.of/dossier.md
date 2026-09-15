## VTask.of

### Object
`VTask.of` is the canonical additive monoid homomorphism that embeds a single component `G i` of a directed system into the colimit (direct limit) of that system. Given a directed system of abelian groups indexed by a preordered type, it picks out the copy of `G i` sitting inside the direct limit, sending each element `x : G i` to its equivalence class in the direct limit. These maps are the universal "insertion" maps that together witness the universal property of the direct limit.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.of : {ι : Type u_2} -> [Preorder ι] -> (G : ι → Type u_3) -> [(i : ι) → AddCommMonoid (G i)] -> (f : (i j : ι) → i ≤ j → G i →+ G j) -> [DecidableEq ι] -> (i : ι) -> G i →+ AddCommGroup.DirectLimit G f
<!-- PINNED-SIGNATURE:END -->


`{ι : Type u_2} -> [Preorder ι] -> (G : ι → Type u_3) -> [(i : ι) → AddCommMonoid (G i)] -> (f : (i j : ι) → i ≤ j → G i →+ G j) -> [DecidableEq ι] -> (i : ι) -> G i →+ AddCommGroup.DirectLimit G f`

- `ι` is the index type, which serves as the directed poset whose elements label the components of the system.
- The `Preorder ι` instance supplies the partial order on `ι` used to specify when one index is "below" another.
- `G` is the functor: for each index `i`, `G i` is an abelian group (here required as an `AddCommMonoid`, with the `AddCommGroup` structure on the direct limit understood separately).
- The `AddCommMonoid (G i)` instances provide the additive structure on every component.
- `f` is the system of transition maps: for each `i ≤ j`, `f i j _` is an additive monoid homomorphism `G i →+ G j`, required to satisfy the compatibility conditions of a directed system (these are not enforced by the type but are the intended invariant).
- `DecidableEq ι` is required for the internal construction of the direct limit.
- `i` is the specific index of the component being embedded — the source of the canonical map.

### Conventions

No junk-value or degenerate-input conventions have been declared for this definition; it is a well-defined additive monoid homomorphism for every admissible choice of inputs.

### Worked examples

- Claim: For the trivial directed system over a single-element index type with `G ⋆ = ℤ` and the identity transition map, `VTask.of G f ⋆` sends every `x : ℤ` to its canonical image in the direct limit.

- Claim: For a directed system indexed by `ℕ` with `G n = ℤ` and all transition maps equal to the identity, `VTask.of G f 0` followed by `VTask.of G f 1` are related by the fact that for `x : G 0`, the image of `f 0 1 h x` under `VTask.of G f 1` equals the image of `x` under `VTask.of G f 0` — reflecting the commutativity of the canonical maps with the transition maps.

### Boundaries

- If the preorder on `ι` has no comparabilities (i.e., is a discrete/antichain order), the transition maps `f i j h` are only defined when `i = j` (where `h : i ≤ j` forces `i = j`). The canonical map `VTask.of G f i` is still well-defined; it simply embeds `G i` into the direct limit where no two distinct components are identified.
- When `ι` is empty, the direct limit is the trivial group and `VTask.of` vacuously has no instantiations.
- The map is generally not surjective (the direct limit can receive elements from many components), but it is injective whenever the transition maps are all injective (injectivity of the canonical maps is a standard fact about direct limits of injective systems).
- The zero element of `G i` is always mapped to the zero element of the direct limit, as `VTask.of G f i` is an additive monoid homomorphism.

### Not to be confused with

- `AddCommGroup.DirectLimit` itself — that is the colimit object (a type), whereas `VTask.of` is the insertion map *into* that object.
- The transition map `f i j h : G i →+ G j` — that goes between components of the system, not into the direct limit.
- `Module.DirectLimit.of` — the analogous construction for modules over a ring; `VTask.of` is its additive-group specialization and wraps it, but lives in the `AddCommGroup` namespace and returns an `AddMonoidHom` rather than a `LinearMap`.
