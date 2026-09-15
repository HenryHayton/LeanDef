## 1. Object

The **lineality space** of a pointed cone `C` in a module `E` over an ordered ring `R` is the largest submodule of `E` that is entirely contained in `C`. Concretely, it consists of all vectors `x` such that both `x` and `−x` belong to `C`; equivalently, it is the intersection of `C` with its negation `−C`. Because it is closed under arbitrary scalar multiplication (not just non-negative scaling), it forms a genuine linear subspace rather than merely a sub-cone.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lineal : {R : Type u_1} -> {E : Type u_2} -> [Ring R] -> [LinearOrder R] -> [IsOrderedRing R] -> [AddCommGroup E] -> [Module R E] -> (C : PointedCone R E) -> Submodule R E
<!-- PINNED-SIGNATURE:END -->


VTask.lineal : {R : Type u_1} -> {E : Type u_2} -> [Ring R] -> [LinearOrder R] -> [IsOrderedRing R] -> [AddCommGroup E] -> [Module R E] -> (C : PointedCone R E) -> Submodule R E

`R` is the scalar ring, which must be a linearly ordered ring (so that non-negative scalars are meaningful). `E` is the ambient module over `R` in which the cone lives. `C` is the pointed cone whose lineality space is being computed. The result is a submodule of `E`.

## 3. Conventions

The lineality space is always at least the zero submodule, because every pointed cone contains the origin. No additional junk-value or boundary conventions are declared beyond what the algebraic structure forces.

## 4. Worked examples

- Claim: The lineality space of the non-negative orthant in ℝ² (the cone of vectors with both coordinates ≥ 0) is the zero submodule, since no nonzero vector together with its negation both have non-negative coordinates.

- Claim: For a submodule `S` viewed as a pointed cone `C`, the lineality space `VTask.lineal C` equals `S` itself, because every element `x ∈ S` satisfies both `x ∈ C` and `−x ∈ C`.

- Claim: `VTask.lineal C ≤ C` for every pointed cone `C`; the lineality space is always contained in the cone.

- Claim: `VTask.lineal C` equals the supremum of the set of all submodules `S` satisfying `S ≤ C`; it is the largest submodule inside `C`.

## 5. Boundaries

- When `C` is itself a submodule (viewed as a pointed cone), the lineality space equals `C` entirely.
- When `C` is a strongly pointed (or strictly pointed) cone — one whose lineality space is trivial — `VTask.lineal C` is the zero submodule.
- The lineality space is always a submodule, not merely a sub-cone; in particular it is closed under negation and under scaling by any ring element, positive or negative.
- Since every pointed cone contains `0`, the lineality space is always nonempty (it always contains `0`).

## 6. Not to be confused with

- **The cone `C` itself**: `C` is a `PointedCone`, closed only under non-negative scalings, whereas the lineality space is a proper `Submodule` closed under all scalings.
- **The dual cone or support function**: These encode outward-facing linear inequalities, whereas the lineality space is an internal subspace of directions of full linearity.
- **The recession cone**: The recession cone of a convex set captures directions in which the set extends to infinity; the lineality space is specifically the sub-cone of directions that are linear (both forward and backward) inside `C`.