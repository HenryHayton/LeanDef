## VTask.Flat

### Object

A convex cone in a module over a semiring is called **flat** if it contains some nonzero vector together with its additive inverse (negative). Geometrically, this means the cone contains an entire line through the origin, not just a ray. A cone that fails to be flat is called salient (or pointed in some terminologies).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Flat : {R : Type u_2} -> {G : Type u_3} -> [Semiring R] -> [PartialOrder R] -> [AddCommGroup G] -> [SMul R G] -> (C : ConvexCone R G) -> Prop
<!-- PINNED-SIGNATURE:END -->


The implicit arguments fix the algebraic context: `R` is the scalar semiring (equipped with a partial order), `G` is the additive commutative group on which `R` acts. The single explicit argument `C` is the convex cone whose flatness is being tested.

### Conventions

No special junk-value or boundary conventions are declared for this predicate: the existential is meaningful for every convex cone in every valid algebraic context, and no degenerate input requires a special-case output convention.

### Worked examples

- Claim: The whole space, viewed as a convex cone over the reals in `ℝ`, is flat, since it contains every vector and its negative.

- Claim: A flat cone is always pointed (contains the zero vector), so `VTask.Flat C → C.Pointed`.

- Claim: Flatness is monotone: if `C₁ ≤ C₂` (as convex cones) and `C₁` is flat, then `C₂` is flat, because the witnessing vector and its negative both belong to the larger cone.

- Claim: A convex cone `C` is salient if and only if it is not flat, i.e., `C.Salient ↔ ¬ VTask.Flat C`.

### Boundaries

- The zero cone (containing only `0`) is **not** flat, because the definition requires the witnessing vector to be nonzero.
- Any cone containing a nonzero element `x` and also `-x` is immediately flat, regardless of what other elements it contains.
- A ray (a half-line from the origin) that does not contain the opposite ray is not flat; adding the opposite ray makes it flat.
- Every flat cone is in particular pointed (contains `0`), but the converse fails: a pointed cone need not be flat.

### Not to be confused with

- `ConvexCone.Pointed`: a cone is pointed if it contains `0`; every flat cone is pointed, but a pointed cone need not be flat.
- `ConvexCone.Salient`: the negation of flatness; a cone is salient precisely when it contains no nonzero vector together with its negative.
- `ConvexCone.Blunt`: a cone that does not contain `0`; this is an orthogonal condition to flatness (a blunt cone cannot be flat since flatness implies pointedness).