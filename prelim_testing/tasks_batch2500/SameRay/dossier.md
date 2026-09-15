## Object

Two vectors `v₁` and `v₂` in a module over a strictly ordered commutative semiring are said to lie on the **same ray** if they point in the same direction from the origin (or at least do not point in opposite directions), with zero vectors treated as compatible with every direction. Concretely, the relation holds when at least one of the two vectors is zero, or when there exist strictly positive scalars `r₁` and `r₂` such that scaling `v₁` by `r₁` yields the same vector as scaling `v₂` by `r₂`. Over a field of real numbers, this is equivalent to saying one vector is a nonnegative scalar multiple of the other.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.SameRay : (R : Type u_1) -> [CommSemiring R] -> [PartialOrder R] -> [IsStrictOrderedRing R] -> {M : Type u_2} -> [AddCommMonoid M] -> [Module R M] -> (v₁ v₂ : M) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.SameRay : (R : Type u_1) -> [CommSemiring R] -> [PartialOrder R] -> [IsStrictOrderedRing R] -> {M : Type u_2} -> [AddCommMonoid M] -> [Module R M] -> (v₁ v₂ : M) -> Prop`

The first explicit argument `R` is the scalar ring, which must be a commutative semiring equipped with a compatible strict total order (making it a strictly ordered ring). The implicit argument `M` is the module in which the vectors live, required to be an additive commutative monoid with an `R`-module structure. The arguments `v₁` and `v₂` are the two vectors in `M` whose directional compatibility is being tested.

## Conventions

The zero vector is conventionally regarded as lying on the same ray as every vector: any pair `(0, w)` or `(v, 0)` satisfies the relation regardless of the nonzero argument. This avoids excluding zero from the relation and keeps it reflexive at the origin.

## Worked examples

- Claim: For real vectors, `(2 : ℝ) • (1, 0)` and `(3 : ℝ) • (1, 0)` are on the same ray, witnessed by taking `r₁ = 3`, `r₂ = 2`.

- Claim: The zero vector `(0 : ℝ × ℝ)` is on the same ray as any vector `v : ℝ × ℝ`, because the first disjunct `v₁ = 0` is satisfied.

- Claim: `VTask.SameRay ℝ v₁ v₂` is a reflexive relation: every vector is on the same ray as itself, since we can take `r₁ = r₂ = 1` (both strictly positive) to obtain `1 • v = 1 • v`.

- Claim: Over `ℝ`, if `VTask.SameRay ℝ x y` and `‖x‖ = ‖y‖` with both `x y : E` (normed space), then `x = y`.

## Boundaries

- If both `v₁` and `v₂` are zero, the relation holds trivially (the first disjunct suffices).
- If exactly one is zero, the relation still holds via the first or second disjunct.
- The scalars `r₁`, `r₂` witnessing the relation must be **strictly** positive; zero scalars are not admitted as witnesses in the existential clause. This prevents two nonzero opposite vectors from being mistakenly identified as same-ray.
- Over `ℝ`, `v` and `-v` for a nonzero `v` do **not** satisfy the relation (no positive multiples can make them equal).
- The relation is symmetric and reflexive but not antisymmetric in general (it does not force equality).

## Not to be confused with

- `Module.Ray`: the quotient type that packages an equivalence class of nonzero vectors under the same-ray relation, rather than a bare proposition about two vectors.
- Linear independence / proportionality over a field: two vectors being proportional (one a scalar multiple of the other) is a weaker notion that allows negative scalars and does not distinguish direction.
- `Collinear`: three or more points being collinear in an affine space is a related but distinct geometric notion that does not track directional orientation.