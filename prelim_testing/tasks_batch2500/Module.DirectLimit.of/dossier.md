## Object

`VTask.of` is the canonical inclusion (injection into the colimit) of a single component module into the direct limit of a directed system of modules. Given a directed system of `R`-modules `G i` indexed by a preordered type `ι`, with transition maps `f i j hij : G i →ₗ[R] G j` for `i ≤ j`, the direct limit `Module.DirectLimit G f` is the colimit of this system. For each index `i`, `VTask.of R ι G f i` is an `R`-linear map from `G i` into this colimit that is compatible with all transition maps: applying `of` at index `j` after a transition map `f i j hij` gives the same element as applying `of` at index `i`. This map plays the role of the universal cocone leg in the colimit construction.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.of : (R : Type u_1) -> [Semiring R] -> (ι : Type u_2) -> [Preorder ι] -> (G : ι → Type u_3) -> [(i : ι) → AddCommMonoid (G i)] -> [(i : ι) → Module R (G i)] -> (f : (i j : ι) → i ≤ j → G i →ₗ[R] G j) -> [DecidableEq ι] -> (i : ι) -> G i →ₗ[R] Module.DirectLimit G f
<!-- PINNED-SIGNATURE:END -->


`VTask.of (R : Type u_1) [Semiring R] (ι : Type u_2) [Preorder ι] (G : ι → Type u_3) [(i : ι) → AddCommMonoid (G i)] [(i : ι) → Module R (G i)] (f : (i j : ι) → i ≤ j → G i →ₗ[R] G j) [DecidableEq ι] (i : ι) : G i →ₗ[R] Module.DirectLimit G f`

- `R` is the commutative semiring of scalars shared across the entire directed system.
- `ι` is the index type, equipped with a preorder that determines which transitions exist.
- `G` is the family of modules, one for each index `i : ι`.
- The `AddCommMonoid` and `Module` instances equip each `G i` with its additive and scalar-multiplication structure.
- `f` is the family of transition maps: for each `i ≤ j`, a linear map `G i →ₗ[R] G j` expressing how the system is directed.
- The `DecidableEq ι` instance is a technical requirement for constructing the underlying direct sum.
- `i` is the specific index whose component `G i` is being mapped into the direct limit.

The output is an `R`-linear map from `G i` into `Module.DirectLimit G f`.

## Conventions

There are no junk-value or boundary conventions declared: the map `VTask.of R ι G f i` is defined for every choice of ring `R`, preordered index type `ι`, module family `G`, transition maps `f`, and index `i`, with no degenerate regimes producing special sentinel outputs.

## Worked examples

- Claim: For any element `x : G i`, applying `VTask.of` and then the lift linear map `F` recovers `F.comp (VTask.of R ι G f i)` applied to `x`; in particular `lift_comp_of` states that any linear map out of the direct limit is recovered from its composites with the canonical inclusions.

- Claim: For indices `i ≤ j` and any element `x : G i`, the image of the transitioned element `f i j hij x` under `VTask.of R ι G f j` equals the image of `x` under `VTask.of R ι G f i`; that is, `VTask.of R ι G f j (f i j hij x) = VTask.of R ι G f i x`.

- Claim: When the index type is nonempty and directed, every element `z : Module.DirectLimit G f` is in the image of some `VTask.of R ι G f i`; that is, there exist `i` and `x` such that `VTask.of R ι G f i x = z`.

- Claim: If `VTask.of R ι G f i x = 0` in the direct limit, then there exists an index `j` with `i ≤ j` such that the transition map sends `x` to zero: `f i j hij x = 0` in `G j`.

## Boundaries

- When the index type `ι` is empty (no indices at all), the direct limit itself is the trivial module, and there are no components from which to map — the map `VTask.of` simply has no instances to be called.
- When the transition maps `f` are all identity maps (e.g., a constant system), `VTask.of R ι G f i` is still well-defined; the direct limit collapses to (a quotient of) the direct sum.
- The map `VTask.of R ι G f i` need not be injective in general: injectivity holds if and only if there is no index `j ≥ i` at which the transition map `f i j hij` kills the element. This is precisely the content of the `of.zero_exact` theorem.
- Even for a non-directed preorder, `VTask.of` is defined; the colimit construction still makes sense, though the universal property characterizing it as a filtered colimit requires directedness.

## Not to be confused with

- `DirectSum.lof R ι G i`: the canonical inclusion of `G i` into the *direct sum* (coproduct), not the direct limit (colimit); the direct limit further identifies elements related by transition maps.
- `Module.DirectLimit.lift`: the universal map *out* of the direct limit into another module, dual in role to `VTask.of` which maps *into* the direct limit.
- The quotient map `Quot.mk` used internally in the construction: `VTask.of` is the mathematically meaningful cocone leg, while `Quot.mk` is an implementation artifact of the quotient construction.