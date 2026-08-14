## VTask.cylinder

### Object

Given a finite subset `U` of an index type `G` and a reference configuration `x : G → A`, the **cylinder set** `VTask.cylinder U x` is the collection of all configurations `y : G → A` that agree with `x` on every index in `U`. That is, it is the set of all functions from `G` to `A` that are "pinned" to match `x` at the finitely many coordinates specified by `U`, with no constraint elsewhere. In symbolic dynamics this is the fundamental notion of specifying finitely many letters in an infinite configuration.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.cylinder : {A : Type u_1} -> {G : Type u_2} -> (U : Finset G) -> (x : G → A) -> Set (G → A)
<!-- PINNED-SIGNATURE:END -->


`{A : Type u_1} -> {G : Type u_2} -> (U : Finset G) -> (x : G → A) -> Set (G → A)`

The type `A` is the **alphabet** — the set of symbols or values that each coordinate can take. The type `G` is the **index set** (or "group of positions") over which configurations are defined. The argument `U` is the **support** of the cylinder: a finite subset of `G` specifying which coordinates are constrained. The argument `x` is the **reference configuration**: a function `G → A` whose values on `U` determine the constraint — every element of the cylinder must agree with `x` at each position in `U`.

### Conventions

When `U` is empty, every configuration satisfies the (vacuous) agreement condition, so the cylinder is the entire set `G → A`. No junk-value convention is needed for inputs outside `U`; the definition is naturally total and the coordinates outside `U` are simply unconstrained.

### Worked examples

- Claim: For `U = ∅`, `VTask.cylinder ∅ x = Set.univ` for any `x : G → A` — the empty support imposes no constraint, so the cylinder is the whole space.

- Claim: For `G = Fin 2`, `A = Bool`, `U = {0, 1}`, and `x` the constant `false` configuration, the cylinder `VTask.cylinder {0, 1} x` consists exactly of those `y : Fin 2 → Bool` with `y 0 = false` and `y 1 = false`.

- Claim: A configuration `y` belongs to `VTask.cylinder U x` if and only if for every index `i ∈ U`, `y i = x i`. (This is a direct unfolding of the membership characterization.)

- Claim: `VTask.cylinder U x` equals the set-theoretic pi `Set.pi (↑U : Set G) (fun i => {x i})`, viewing each constrained coordinate as forced into the singleton `{x i}`.

### Boundaries

- **Empty support (`U = ∅`):** The cylinder is all of `G → A`, since the universal quantifier over an empty set is vacuously true. Every configuration is a member.
- **Full finite support:** When `U` indexes every element of a finite `G`, the cylinder contains exactly the configurations that agree with `x` everywhere, i.e., it is the singleton `{x}`.
- **Single-element support (`U = {i}`):** The cylinder consists of all configurations that match `x` at coordinate `i` and are arbitrary elsewhere; this is the largest nontrivial cylinder over a single coordinate.
- **Topological behaviour:** When `A` carries the discrete topology, each cylinder is clopen (both open and closed). Under a T₁ topology on `A`, cylinders are at least closed. Cylinders over a discrete `A` form a basis for the product topology on `G → A`.
- **Independence of `x` off `U`:** Two reference configurations `x` and `x'` that agree on all of `U` (i.e., `∀ i ∈ U, x i = x' i`) determine the same cylinder set.

### Not to be confused with

- **`Set.pi`:** The set-theoretic product `Set.pi S f` assigns a set `f i` to each index `i ∈ S`; a cylinder is the special case where each `f i` is a singleton `{x i}`, so cylinders are a strictly more special notion.
- **Pattern occurrences / `mulOccursInAt`:** The set of configurations where a pattern `p` occurs at position `g` is also a cylinder (with translated support), but `mulOccursInAt` is the higher-level concept, not the primitive cylinder.
- **Shift-invariant subsets (subshifts):** A subshift is a closed shift-invariant subset of `G → A` defined by forbidden patterns; it is a union of cylinders in general, not a single cylinder.
