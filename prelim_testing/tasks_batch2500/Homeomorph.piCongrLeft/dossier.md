## VTask.piCongrLeft

### Object

Given a bijection `e : ι ≃ ι'` between two index types, and a family of topological spaces `Y` indexed by `ι'`, there is a natural algebraic isomorphism between the dependent product `Π i : ι, Y (e i)` and the dependent product `Π j : ι', Y j` — one simply re-indexes using `e`. `VTask.piCongrLeft` promotes this set-theoretic bijection to a **homeomorphism**: both the forward map (re-indexing) and its inverse are continuous, making the two product spaces not only algebraically but topologically identical.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.piCongrLeft : {ι : Type u_7} -> {ι' : Type u_8} -> {Y : ι' → Type u_9} -> [(j : ι') → TopologicalSpace (Y j)] -> (e : ι ≃ ι') -> ((i : ι) → Y (e i)) ≃ₜ ((j : ι') → Y j)
<!-- PINNED-SIGNATURE:END -->


`VTask.piCongrLeft : {ι : Type u_7} -> {ι' : Type u_8} -> {Y : ι' → Type u_9} -> [(j : ι') → TopologicalSpace (Y j)] -> (e : ι ≃ ι') -> ((i : ι) → Y (e i)) ≃ₜ ((j : ι') → Y j)`

- `ι` and `ι'` are the source and target index types (implicit).
- `Y` is the type family over `ι'` whose fibers form the spaces being compared (implicit).
- The instance argument `[∀ j, TopologicalSpace (Y j)]` equips each fiber `Y j` with its topology so that the product topologies on both sides are defined.
- `e : ι ≃ ι'` is the bijection used to re-index: it determines both the forward and backward maps of the homeomorphism.

The result is a homeomorphism `(∀ i, Y (e i)) ≃ₜ (∀ j, Y j)` where the forward map sends a tuple `x` to the tuple `fun j ↦ x (e.symm j)`, and the inverse sends a tuple `y` to `fun i ↦ y (e i)`, both being continuous with respect to the product topologies.

### Conventions

There are no junk-value or edge conventions to declare: the definition is total and well-defined for every equivalence `e`, including the identity equivalence, empty index types, and singleton index types.

### Worked examples

- Claim: When `e` is the identity equivalence `Equiv.refl ι`, `VTask.piCongrLeft e` equals the identity homeomorphism on `∀ i, X i`.

- Claim: The inverse of `VTask.piCongrLeft e` acts by pre-composing with `e`: for a tuple `y : ∀ j, Y j`, `(VTask.piCongrLeft e).symm y = fun i ↦ y (e i)`.

- Claim: For a tuple `x : ∀ i, Y (e i)` and any index `i : ι`, evaluating the forward map at `e i` recovers `x i`: `(VTask.piCongrLeft e x) (e i) = x i`.

### Boundaries

- **Empty index type**: When `ι` and `ι'` are both empty (the unique equivalence between them being `Equiv.refl`), both product types have a single element (the empty tuple) and the homeomorphism is trivially the unique map between them.
- **Identity equivalence**: `VTask.piCongrLeft (Equiv.refl ι)` is definitionally the identity homeomorphism (and provably equal to it, as stated in `piCongrLeft_refl`).
- **Singleton index type**: For `ι ≅ ι' ≅ PUnit`, both products are homeomorphic to the single fiber, and `VTask.piCongrLeft` witnesses this.
- **Non-trivial topology**: The homeomorphism respects the product topology on both sides exactly; it is not merely a bijection of the underlying sets.

### Not to be confused with

- `Equiv.piCongrLeft`: the underlying set-theoretic equivalence between `Π i, Y (e i)` and `Π j, Y j`, with no topology.
- `Homeomorph.piCongrRight`: the homeomorphism `Π i, X i ≃ₜ Π i, Y i` obtained from a fiberwise homeomorphism `∀ i, X i ≃ₜ Y i`, rather than from re-indexing.
- `Homeomorph.piCongr`: combines both re-indexing and fiberwise homeomorphisms simultaneously, subsuming both `piCongrLeft` and `piCongrRight`.
