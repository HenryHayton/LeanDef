## VTask.IsMono

### Object

`VTask.IsMono C l` is the proposition that the line `l` is **monochromatic** with respect to the coloring `C`: every point of `l` receives the same color under `C`. Concretely, a `Line α ι` is a combinatorial line in the space `ι → α` of `ι`-tuples over an alphabet `α`, and a coloring is any function `C : (ι → α) → κ` assigning a color in `κ` to each tuple. Monochromaticity means there exists a single color `c` such that every point of the line maps to `c`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsMono : {α : Type u_5} -> {ι : Type u_6} -> {κ : Sort u_7} -> (C : (ι → α) → κ) -> (l : Combinatorics.Line α ι) -> Prop
<!-- PINNED-SIGNATURE:END -->


The first (implicit) argument `α` is the **alphabet** — the type of symbols filling each coordinate. The second implicit argument `ι` is the **index type** — the set of coordinate positions. The third implicit argument `κ` is the **color type** — the codomain of the coloring. The explicit argument `C` is the **coloring function**, assigning a color to each `ι`-tuple over `α`. The explicit argument `l` is the **combinatorial line** whose monochromaticity is being tested.

### Conventions

There are no declared junk-value or edge conventions: `VTask.IsMono` is a well-defined `Prop` for any coloring `C` and any line `l` without restriction, and no special behavior is stipulated at degenerate inputs.

### Worked examples

- Claim: For the constant coloring `C _ = (0 : Fin 2)`, every line is monochromatic (the witness color is `0`).

- Claim: For the identity coloring `C := id` on `Fin 2 → Fin 2` (regarded as a function to some color type isomorphic to `Fin 2 → Fin 2`), a non-constant line is *not* monochromatic, because its two distinct points receive distinct colors.

- Claim: If `α` is a one-element type, then every coloring and every line satisfy `VTask.IsMono C l`, since all points of any line coincide.

- Claim: The Hales–Jewett theorem asserts that for any finite alphabet `α` and finite color type `κ`, there exists a finite index type `ι` such that every coloring `C : (ι → α) → κ` admits some monochromatic line, i.e., some `l` with `VTask.IsMono C l`.

### Boundaries

- When `ι` is empty, a `Line α ι` has a unique point (the empty tuple), and `VTask.IsMono C l` holds trivially since a single-point collection is trivially monochromatic.
- When `κ` is a one-element type, every function `C` is constant, so every line is trivially monochromatic.
- When `α` is a one-element type, every line has only one possible point (all coordinates are identical), so monochromaticity is automatic.
- There is no restriction on `α`, `ι`, or `κ` being finite; the definition is stated for arbitrary types.

### Not to be confused with

- `Combinatorics.Line` itself — the type of combinatorial lines, which `VTask.IsMono` takes as an argument rather than defines.
- A line being *constant* (all coordinates fixed) — a combinatorial line has at least one varying coordinate; monochromaticity concerns the coloring, not the line's internal structure.
- A coloring being *proper* (adjacent points receive different colors) — `VTask.IsMono` is the opposite requirement, that all points share a color.
