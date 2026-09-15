## Object

A pointed cone `C` in `N` (over an ordered commutative ring `R`) is **dually finitely generated** (DualFG) if it can be expressed as the dual of some *finite* set of vectors in `M`. Geometrically, this means `C` is an intersection of finitely many closed halfspaces defined by the pairing `p`, i.e., `C` is an H-cone (halfspace-representable cone). This is the dual notion to being finitely generated (FG, or V-cone), where the cone is the non-negative span of finitely many generators.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.DualFG : {R : Type u_1} -> {M : Type u_2} -> {N : Type u_3} -> [CommRing R] -> [PartialOrder R] -> [IsOrderedRing R] -> [AddCommGroup M] -> [Module R M] -> [AddCommGroup N] -> [Module R N] -> (p : M →ₗ[R] N →ₗ[R] R) -> (C : PointedCone R N) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.DualFG (p : M →ₗ[R] N →ₗ[R] R) (C : PointedCone R N) : Prop`

The bilinear pairing `p` is the linear map from `M` to the `R`-linear functionals on `N`; it specifies which halfspaces are available and how vectors in `M` define inequalities on `N`. The pointed cone `C` is the object under examination — the cone in `N` that we are asking to be dually finitely generated with respect to `p`.

## Conventions

The pairing `p` is held fixed throughout: DualFG is always stated relative to a particular bilinear pairing between `M` and `N`. There are no junk-value conventions declared for this definition; the proposition is simply `False`-valued (i.e., not provable) for cones that genuinely are not dually finitely generated, and no special sentinel behavior is assigned to degenerate inputs.

## Worked examples

- Claim: For any finset `s : Finset M`, the cone `dual p s` satisfies `VTask.DualFG p (dual p s)` — the dual of a finite set is always dually finitely generated.

- Claim: If `C` and `D` are both DualFG with respect to `p`, then their intersection `C ⊓ D` is also DualFG with respect to `p`. This follows because the union of the two witnessing finsets provides a finset whose dual equals the intersection of the two cones.

- Claim: If `C : PointedCone R M` is finitely generated (FG), then `dual p C` is DualFG with respect to `p`. Concretely, the finite generators of `C` serve as the finite witness for DualFG of its dual.

- Claim: Every DualFG cone `C` with respect to `p` is also DualFG with respect to the identity pairing `.id`, since there is a coercion that allows reinterpreting the witness.

## Boundaries

- The empty finset is a valid witness: its dual is typically the entire ambient cone (all of `N` paired non-negatively with nothing is everything), so the top element of the pointed cone lattice is DualFG.
- A single-element finset gives a single halfspace; thus any half-space cone (defined by one linear inequality) is DualFG.
- The property is preserved under finite intersections (`⊓`) but not in general under unions or spans.
- If `C` is DualFG, the double-dual identity `dual p (dual p.flip C) = C` holds, reflecting the finitely-generated/H-cone duality theorem.
- The definition requires only *existence* of a witnessing finset; it is not constructive.

## Not to be confused with

- `PointedCone.FG` (finitely generated, V-cone): that property says `C` is the non-negative span of finitely many vectors, whereas DualFG says `C` is the intersection of finitely many halfspaces.
- `PointedCone.dual` (the dual operator): this maps a set or cone to its dual cone; DualFG is a *property* of a cone asserting it lies in the image of this operator applied to some finite set.
- `Finset.dual` vs `PointedCone.dual`: the witness for DualFG is a `Finset M`, but the dual operator can also be applied to arbitrary subsets or cones; DualFG specifically requires a finite set as witness.