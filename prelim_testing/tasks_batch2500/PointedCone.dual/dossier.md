## VTask.dual

### Object

Given a bilinear pairing `p : M →ₗ[R] N →ₗ[R] R` and a subset `s ⊆ M`, the **dual cone** of `s` with respect to `p` is the collection of all points `y ∈ N` such that `0 ≤ p(x, y)` for every `x ∈ s`. This set is automatically a pointed cone in `N`: it contains zero and is closed under addition and scaling by nonneg elements of `R`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.dual : {R : Type u_1} -> [CommSemiring R] -> [PartialOrder R] -> [IsOrderedRing R] -> {M : Type u_2} -> [AddCommMonoid M] -> [Module R M] -> {N : Type u_3} -> [AddCommMonoid N] -> [Module R N] -> (p : M →ₗ[R] N →ₗ[R] R) -> (s : Set M) -> PointedCone R N
<!-- PINNED-SIGNATURE:END -->


```
VTask.dual : {R : Type u_1} -> [CommSemiring R] -> [PartialOrder R] -> [IsOrderedRing R] -> {M : Type u_2} -> [AddCommMonoid M] -> [Module R M] -> {N : Type u_3} -> [AddCommMonoid N] -> [Module R N] -> (p : M →ₗ[R] N →ₗ[R] R) -> (s : Set M) -> PointedCone R N
```

`R` is the ordered commutative semiring (in practice a linearly ordered field or ring) that serves as the scalar and value type. `M` is the left module housing the input set; `N` is the right module in which the dual cone lives. `p` is the bilinear pairing between `M` and `N` with values in `R`, given as a curried `R`-linear map. `s` is the subset of `M` whose dual cone is being formed.

### Conventions

No special junk-value or edge-case conventions are formally declared for this construction; its behaviour on every input follows directly from the universal-quantification definition.

### Worked examples

- Claim: The zero vector of `N` belongs to `VTask.dual p s` for every pairing `p` and every set `s`, because `p x 0 = 0 ≥ 0` for all `x`.

- Claim: When `s = ∅`, `VTask.dual p ∅` equals the whole ambient cone (all of `N` with the cone structure), because the condition `∀ x ∈ ∅, 0 ≤ p x y` is vacuously satisfied by every `y`.

- Claim: `VTask.dual p` is antitone: if `s ⊆ t` then `VTask.dual p t ≤ VTask.dual p s`, since a `y` that passes the test for all `x ∈ t` certainly passes it for all `x ∈ s ⊆ t`.

- Claim: For a union, `VTask.dual p (s ∪ t) = VTask.dual p s ⊓ VTask.dual p t`, because `y` must satisfy the nonnegativity condition for every point in both `s` and `t`.

- Claim: Any `y ∈ VTask.dual p s` satisfies `0 ≤ p x y` for every `x ∈ s` — this is exactly the membership characterisation.

### Boundaries

- **Empty set**: `VTask.dual p ∅` is the universal pointed cone (the whole of `N` carries the trivially satisfied condition), giving the top element in the lattice of pointed cones.
- **Singleton**: `VTask.dual p {x}` consists of all `y` with `0 ≤ p x y`, a closed half-space through the origin defined by the linear functional `p x`.
- **Injective pairing flip**: When `p.flip` is injective, `VTask.dual p Set.univ` collapses to the zero cone `{0}`.
- **Double dual**: There is always an inclusion `s ⊆ VTask.dual p.flip (VTask.dual p s)` (the double-dual inclusion), but equality does not hold in general without finite-generation or reflexivity hypotheses.
- **Hull invariance**: Taking the conic hull of `s` before dualizing does not change the result: `VTask.dual p (hull R s) = VTask.dual p s`.

### Not to be confused with

- **`PointedCone.comap`**: pulls a cone back along a linear map; dual cones can be expressed via comap but are conceptually about bilinear pairings, not just preimages.
- **`Module.Dual` / linear functionals**: the dual cone is a subset of `N`, not a space of functionals; one must supply a pairing `p` to bridge `N` to the scalar-valued dual.
- **`ConvexCone.dual`**: a parallel construction on `ConvexCone` rather than `PointedCone`; the pointed version automatically includes the vertex `0`.
