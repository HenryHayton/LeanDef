## VTask.pi

### Object

The *pi filter* (product filter) on the dependent product type `(i : ι) → α i`, built from an indexed family of filters `f i` on each factor `α i`. A subset of `(i : ι) → α i` belongs to this filter if and only if it contains a finite-coordinate cylinder: that is, there exist a finite set `I ⊆ ι` and sets `t i ∈ f i` for each `i` such that the restricted cylinder `I.pi t ⊆ s`. Equivalently, it is the coarsest filter making each evaluation map `x ↦ x i` a filter-preserving map from the product filter to `f i`. It generalizes the usual product topology filter construction to an arbitrary (possibly infinite) index type.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pi : {ι : Type u_3} -> {α : ι → Type u_4} -> (f : (i : ι) → Filter (α i)) -> Filter ((i : ι) → α i)
<!-- PINNED-SIGNATURE:END -->


`VTask.pi : {ι : Type u_3} -> {α : ι → Type u_4} -> (f : (i : ι) → Filter (α i)) -> Filter ((i : ι) → α i)`

- `ι` is the index type that parametrises the family of spaces; it is implicit and inferred from context.
- `α` is the type family assigning to each index `i : ι` the type `α i` of the `i`-th factor; it is also implicit.
- `f` is the explicit argument: a dependent function supplying, for each index `i`, a filter on the corresponding factor `α i`.

### Conventions

There are no special junk-value or boundary conventions declared for this definition: when the index type `ι` is empty, the product type `(i : ι) → α i` is a one-element type and `VTask.pi f` reduces to the top filter (the filter of all sets) on that type; this follows from the fact that an infimum over an empty family in the filter lattice is ⊤. When `ι` is nonempty, the filter is genuinely constrained by the factors.

### Worked examples

- Claim: A set `s : Set (Fin 2 → ℝ)` belongs to `VTask.pi (fun i => Filter.atTop)` if and only if there exist a finite `I ⊆ Fin 2` and sets `t i ∈ Filter.atTop` such that `I.pi t ⊆ s`. This is the content of `Filter.mem_pi` applied to the `atTop` family.

- Claim: For a single-index family `f : Unit → Filter ℝ`, the filter `VTask.pi f` on `Unit → ℝ` is isomorphic (via the unique homeomorphism `Unit → ℝ ≃ ℝ`) to `f ()`, since there is only one coordinate and every cylinder is determined entirely by that coordinate.

- Claim: For a finite index type `ι` and filters `f i` on `α i`, the set `Set.univ.pi s` (the full product of sets `s i`) belongs to `VTask.pi f` whenever `s i ∈ f i` for all `i ∈ Set.univ`. This follows from `Filter.pi_mem_pi` with `I = Set.univ` (which is finite when `ι` is finite).

- Claim: If every `f i` is a `NeBot` filter, then the pi filter `VTask.pi f` is also `NeBot`.

### Boundaries

- **Empty index type**: When `ι = PEmpty` or `ι = Fin 0`, the only set of type `Set ((i : ι) → α i)` is `Set.univ` (since the type has exactly one element), and `VTask.pi f = ⊤` (the top filter consisting of all sets). The infimum over an empty family of filters is ⊤ by convention in the filter lattice.
- **Singleton index type**: `VTask.pi f` for `ι = Unit` (or `Fin 1`) is naturally isomorphic to `f ()` via the canonical equivalence between `Unit → α ()` and `α ()`.
- **Infinite index type**: When `ι` is infinite, the pi filter is *strictly coarser* than requiring all coordinates simultaneously. A set belongs to `VTask.pi f` only if it contains a cylinder determined by *finitely many* coordinates, not all of them. This is the key distinction from requiring every projection to reflect the filter.
- **`⊥` in a factor**: If some `f i = ⊥` (the bottom filter), then `VTask.pi f = ⊥` as well, since the infimum drops to bottom.

### Not to be confused with

- `Set.pi I s` — this is a *set* (a cylinder in the product space restricted to indices in `I`), not a filter; it appears as a generating set for `VTask.pi`, but is itself a set-theoretic construction.
- `Filter.prod` — the binary product filter `f ×ˢ g` on `α × β`; this is the special case of `VTask.pi` for a two-element index, but has its own API and notation.
- `nhds` on a product topology — for topological spaces, `VTask.pi (fun i => nhds (x i))` equals `nhds x` in the product topology, but `VTask.pi` is a purely order-theoretic/filter construction that does not presuppose a topology.
