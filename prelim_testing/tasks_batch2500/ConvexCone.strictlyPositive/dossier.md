## Object

`VTask.strictlyPositive R M` is the convex cone in the ordered module `M` over the ordered semiring `R` consisting of all elements strictly greater than zero. Concretely, an element `x : M` belongs to this cone if and only if `0 < x`. This is the "open positive cone" or "cone of strictly positive elements" in `M`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.strictlyPositive : (R : Type u_2) -> (M : Type u_4) -> [Semiring R] -> [PartialOrder R] -> [AddCommGroup M] -> [PartialOrder M] -> [IsOrderedAddMonoid M] -> [Module R M] -> [PosSMulStrictMono R M] -> ConvexCone R M
<!-- PINNED-SIGNATURE:END -->


The first argument `R` is the ordered semiring of scalars. The second argument `M` is the ordered `R`-module in which the cone lives. The remaining arguments are typeclass witnesses: a semiring structure and a partial order on `R`; an additive commutative group structure, a partial order, and an ordered-additive-monoid structure on `M`; an `R`-module structure on `M`; and a `PosSMulStrictMono` instance ensuring that scaling by strictly positive scalars preserves strict positivity.

## Conventions

The name uses `strictlyPositive` (rather than the shorter `pos`) deliberately, because the term "positive cone" is established mathematical terminology meaning the cone of *non-negative* elements; see `ConvexCone.positive`. Mathlib's usual `pos`/`nonneg` naming convention is intentionally departed from here to avoid collision with that established usage.

## Worked examples

- Claim: The element `(1 : ℝ)` belongs to `VTask.strictlyPositive ℝ ℝ` because `0 < 1`.

- Claim: The element `(0 : ℝ)` does **not** belong to `VTask.strictlyPositive ℝ ℝ` because `¬ (0 < 0)`.

- Claim: For any `r : ℝ` with `0 < r` and any `x : ℝ` with `0 < x`, the scalar multiple `r • x` belongs to `VTask.strictlyPositive ℝ ℝ`.

- Claim: If `x y : ℝ` both satisfy `0 < x` and `0 < y`, then `x + y` belongs to `VTask.strictlyPositive ℝ ℝ`.

## Boundaries

- The zero element is **excluded**: `0` does not belong to `VTask.strictlyPositive R M` since the carrier is the open ray `Set.Ioi 0`, not the closed ray `Set.Ici 0`.
- Scalar multiplication requires the scalar to be strictly positive (`0 < r`): multiplying by zero or a negative scalar need not preserve membership, and the cone's `smul_mem'` axiom is only guaranteed for positive scalars.
- The cone is not a subgroup of `M` in general (it is not closed under negation), which is expected for a cone of strictly positive elements.
- When `M` has no elements strictly greater than zero (e.g., a trivial ordered module), the resulting cone has empty carrier.

## Not to be confused with

- `ConvexCone.positive R M`: the cone of *non-negative* elements (`0 ≤ x`), which includes zero and is more commonly called the "positive cone" in mathematical literature.
- `ConvexCone.pointed`: a property saying a cone contains zero, which `VTask.strictlyPositive` does **not** satisfy.
- `Set.Ioi 0`: the underlying carrier set; `VTask.strictlyPositive R M` bundles this with the full `ConvexCone` structure (scalar-multiplication and addition closure).