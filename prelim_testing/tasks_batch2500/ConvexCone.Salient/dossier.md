## VTask.Salient

### Object

A convex cone is **salient** (also called pointed) if it contains no nonzero element together with its negation. In other words, the cone does not straddle the origin in any direction: there is no nonzero vector `x` such that both `x` and `-x` belong to the cone.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Salient : {R : Type u_2} -> {G : Type u_3} -> [Semiring R] -> [PartialOrder R] -> [AddCommGroup G] -> [SMul R G] -> (C : ConvexCone R G) -> Prop
<!-- PINNED-SIGNATURE:END -->


*(type string inserted automatically)*

`R` is the semiring of scalars, equipped with a partial order, used to scale elements of the cone. `G` is the additive commutative group of ambient vectors, on which `R` acts via scalar multiplication. `C` is the convex cone whose saliency is being tested.

### Conventions

The quantifier ranges only over **nonzero** elements: the zero vector is always in every convex cone, and its negation is also zero, so requiring `-0 ∉ C` would make no cone salient; hence the condition `x ≠ 0` is a built-in guard, not an extra assumption the user must supply.

### Worked examples

- Claim: The trivial cone containing only the zero vector is salient, because there are no nonzero elements to witness a violation.

- Claim: The nonnegative half-line `{r : ℝ | 0 ≤ r}` viewed as a convex cone in `ℝ` is salient, since for any positive `x` the value `-x` is negative and therefore not in the cone.

- Claim: A convex cone `C` is **not** salient if and only if there exists a nonzero `x ∈ C` with `-x ∈ C`; for instance the full real line `ℝ` (as a cone in itself) is not salient because both `1` and `-1` belong to it.

- Claim: If `C` is salient and `x ∈ C` with `x ≠ 0`, then `-x ∉ C`.

### Boundaries

- The zero vector `0` is explicitly excluded from the saliency condition: the property requires `x ≠ 0` before demanding `-x ∉ C`, so the zero vector never causes a cone to fail saliency.
- The trivial (zero) cone `{0}` is vacuously salient.
- A cone equal to an entire subspace (e.g., all of `G`) is never salient for any nontrivial `G`, because every nonzero vector `x` has `-x` also in the subspace.
- The condition is purely about membership; it does not impose any topological or algebraic closedness requirements beyond what the `ConvexCone` type already carries.

### Not to be confused with

- **Pointed cone (in some texts)**: some authors use "pointed" to mean the cone contains no full line, which coincides with saliency here, but other authors use "pointed" only to mean `C ∩ (-C) = {0}` — these are equivalent for convex cones, but the latter phrasing may look different.
- **Proper cone**: a proper cone is salient *and* closed *and* solid (nonempty interior); saliency alone does not imply closedness or full dimensionality.
- `ConvexCone.Pointed`: a convex cone is pointed if `0 ∈ C`, which is a completely separate (and much weaker) condition; do not confuse pointedness with saliency.