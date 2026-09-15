## 1. Object

A set `s` in a module over an ordered semiring is **star-convex at a point `x`** if, for every point `y` in `s`, the entire line segment joining `x` to `y` lies inside `s`. Geometrically, `s` looks like a "star" with `x` as the central vantage point: every ray from `x` toward a member of `s` stays inside `s`.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.StarConvex : (𝕜 : Type u_4) -> {E : Type u_5} -> [Semiring 𝕜] -> [PartialOrder 𝕜] -> [AddCommMonoid E] -> [SMul 𝕜 E] -> (x : E) -> (s : Set E) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.StarConvex : (𝕜 : Type u_4) -> {E : Type u_5} -> [Semiring 𝕜] -> [PartialOrder 𝕜] -> [AddCommMonoid E] -> [SMul 𝕜 E] -> (x : E) -> (s : Set E) -> Prop
```

`𝕜` is the scalar field (an ordered semiring), used to parameterize convex combinations. `E` is the ambient vector space (an additive commutative monoid with a scalar action of `𝕜`). The typeclass arguments supply the necessary algebraic and order structure on `𝕜` and `E`. `x` is the **center** (the distinguished vantage point) at which star-convexity is tested. `s` is the **set** being examined.

## 3. Conventions

The definition is stated for any ordered semiring scalar type and any additive commutative monoid with scalar action; no field or vector-space structure is required. When `s` is empty, the condition is vacuously true for any center `x` (there are no points `y ∈ s` to check). The center `x` need not itself belong to `s` in general; however, whenever `s` is nonempty and `𝕜` satisfies `0 ≤ 1` (i.e., a `ZeroLEOneClass` instance is available), star-convexity at `x` forces `x ∈ s`.

## 4. Worked Examples

- Claim: Every convex set `s` is star-convex at any of its points — if `hs : Convex ℝ s` and `hx : x ∈ s`, then `VTask.StarConvex ℝ x s` holds.

- Claim: The whole space `Set.univ` is `VTask.StarConvex 𝕜 x Set.univ` for every `x`, since any affine combination of `x` with any `y` remains in the universe.

- Claim: If `s` and `t` are both star-convex at `x`, then so is their intersection `s ∩ t` — `VTask.StarConvex 𝕜 x (s ∩ t)` follows from `VTask.StarConvex 𝕜 x s` and `VTask.StarConvex 𝕜 x t`.

- Claim: A balanced set `s ⊆ ℝ`-module is `VTask.StarConvex ℝ 0 s` — star-convex at the origin.

## 5. Boundaries

- **Empty set**: `VTask.StarConvex 𝕜 x ∅` holds vacuously for any `x`, since there are no elements `y ∈ ∅`.
- **Singleton `{x}`**: `VTask.StarConvex 𝕜 x {x}` holds because the only relevant `y` is `x` itself, and `a • x + b • x = (a + b) • x = 1 • x = x` (assuming the scalar action is linear), so the segment from `x` to `x` is just `{x}`.
- **Center not in `s`**: Star-convexity at `x` does not require `x ∈ s` by definition, but when `s` is nonempty and `ZeroLEOneClass 𝕜` holds, membership of `x` is a consequence.
- **Non-convex star-convex sets**: A set can be star-convex at a specific point without being convex overall; star-convexity is strictly weaker than convexity.

## 6. Not to Be Confused With

- **`Convex 𝕜 s`**: Full convexity requires every pair of points in `s` to be a center; star-convexity only demands this of the single fixed point `x`.
- **`IsStarShaped`** (informal): In topology, a star-shaped set has the same geometric meaning, but the Mathlib predicate here is algebraically parameterized by an ordered semiring and works without a norm or topology.
- **`VTask.StarConvex 𝕜 x s` vs `VTask.StarConvex 𝕜 y s`**: Star-convexity is center-dependent; a set may be star-convex at `x` but not at a different point `y ∈ s`.