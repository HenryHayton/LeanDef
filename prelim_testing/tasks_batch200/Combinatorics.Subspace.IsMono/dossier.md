## VTask.IsMono

### Object

Given a coloring `C` that assigns a color (an element of `κ`) to every function `ι → α`, and a combinatorial subspace `l` of `ι → α` (a structured family of such functions parametrized by `η → α`), `VTask.IsMono C l` is the proposition that the subspace `l` is **monochromatic** with respect to `C`: every point of `l` receives the same color. In other words, `C` is constant on the image of `l`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsMono : {η : Type u_5} -> {α : Type u_6} -> {ι : Type u_7} -> {κ : Type u_8} -> (C : (ι → α) → κ) -> (l : Combinatorics.Subspace η α ι) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsMono : {η : Type u_5} -> {α : Type u_6} -> {ι : Type u_7} -> {κ : Type u_8} -> (C : (ι → α) → κ) -> (l : Combinatorics.Subspace η α ι) -> Prop`

The four implicit type arguments `η`, `α`, `ι`, `κ` are, respectively: the type indexing the "wildcard" positions within the subspace, the alphabet (set of colors for coordinate values), the index type for functions in the ambient space, and the type of colors assigned by `C`. The explicit argument `C` is the coloring function, assigning a color in `κ` to each function `ι → α`. The explicit argument `l` is the combinatorial subspace whose monochromaticity is being asserted.

### Conventions

There are no declared junk-value or edge-case conventions for this definition: it is a universally quantified Prop over an existential, and is simply `False`-like (vacuously there is no witnessing color) when the subspace has no points — but no special convention governs that boundary; it is handled by ordinary logic.

### Worked examples

- Claim: The constant subspace mapping every point to the same function `f₀ : ι → α` is monochromatic under any coloring `C`, since `C` takes the single value `C f₀` on all points of the subspace.

- Claim: If `l` is a combinatorial subspace and `C` is a coloring that assigns the same color `c₀` to every function in the ambient space `ι → α`, then `VTask.IsMono C l` holds (witnessed by `c₀`).

- Claim: The Hales–Jewett theorem guarantees that for any finite alphabet `α`, any finite color set `κ`, and any finite wildcard type `η`, there exists a large enough index type `ι` such that every coloring `C : (ι → α) → κ` admits some combinatorial subspace `l` with `VTask.IsMono C l`.

- Claim: If `l.IsMono C` holds and `eη`, `eα`, `eι` are type equivalences, then the reindexed subspace `l.reindex eη eα eι` is monochromatic under the appropriately conjugated coloring.

### Boundaries

- When the subspace `l` is such that it has exactly one point (e.g., a constant subspace), `VTask.IsMono C l` is trivially true for any `C`, since the single color value witnesses monochromaticity.
- The definition makes sense even when `κ` has only one element; in that case, `VTask.IsMono C l` holds for every subspace `l` and every coloring `C`.
- If `η` is an empty type, the subspace `l` degenerates (it has only one point — the function with no wildcard coordinates), and monochromaticity is again trivially satisfied.
- There is no restriction on `α`, `ι`, `η`, or `κ` being finite; the definition is stated in full generality, though the main theorems (Hales–Jewett) require finiteness.

### Not to be confused with

- `Combinatorics.Subspace` itself: that is the type of combinatorial subspaces, not a proposition about colorings.
- A subspace being a **line** (a combinatorial line): a combinatorial line is a special case of a combinatorial subspace where `η` is a one-element type; `IsMono` applies to subspaces of any wildcard type `η`.
- A coloring being **proper** or **valid**: `IsMono` asserts that all points in the subspace have the *same* color, which is the opposite of a proper coloring requirement (which would demand adjacent points have *different* colors).
