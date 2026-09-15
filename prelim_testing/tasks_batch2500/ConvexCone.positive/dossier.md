## Object

`VTask.positive R M` is the **positive cone** of an ordered module `M` over an ordered semiring `R`: it is the convex cone whose underlying carrier set consists of all elements `x : M` satisfying `0 ≤ x`. Scalar multiplication by a nonneg element of `R` and addition both preserve nonnegativity, so this set is closed under the two operations required of a convex cone, making it a well-defined `ConvexCone R M`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.positive : (R : Type u_2) -> (M : Type u_4) -> [Semiring R] -> [PartialOrder R] -> [AddCommMonoid M] -> [PartialOrder M] -> [IsOrderedAddMonoid M] -> [Module R M] -> [PosSMulMono R M] -> ConvexCone R M
<!-- PINNED-SIGNATURE:END -->


`(R : Type u_2) -> (M : Type u_4) -> [Semiring R] -> [PartialOrder R] -> [AddCommMonoid M] -> [PartialOrder M] -> [IsOrderedAddMonoid M] -> [Module R M] -> [PosSMulMono R M] -> ConvexCone R M`

The first explicit argument `R` is the scalar ring (required to be an ordered semiring so that nonneg scalars are available). The second explicit argument `M` is the module being ordered (required to carry an additive commutative monoid structure, a compatible partial order, and the module action of `R`). The instance arguments supply the algebraic and order-compatibility laws needed to guarantee closure of the nonneg set under positive scalar multiplication and addition.

## Conventions

No junk-value or edge conventions are declared for this definition: it is a total constructor producing a well-typed `ConvexCone R M` for any choice of `R` and `M` satisfying the stated type-class assumptions, and there are no degenerate inputs to assign special behaviour to.

## Worked examples

- Claim: The carrier of `VTask.positive ℝ ℝ` is the set `{x : ℝ | 0 ≤ x}`, i.e., `Set.Ici 0`.

- Claim: `0` belongs to `VTask.positive R M` for any eligible `R`, `M` (the cone is **pointed**).

- Claim: The strictly-positive cone is contained in (i.e., `≤`) the positive cone, `strictlyPositive R M ≤ VTask.positive R M`.

- Claim: When `M` is an ordered additive commutative **group**, `VTask.positive R M` is **salient** (the cone and its negation meet only at `0`).

## Boundaries

- The zero element `0 : M` always belongs to the positive cone (since `0 ≤ 0`), so the cone is **pointed**.
- Elements satisfying `0 ≤ x` are included regardless of whether the inequality is strict; thus elements with `x = 0` are in the cone and elements with `x < 0` are not.
- In a setting where the order on `M` is trivial (everything compares as equal to `0`), the positive cone becomes all of `M`.
- The scalar `r` used for the `smul_mem` closure only needs `0 ≤ r` in `R` (positivity of `r` as a semiring element), not strict positivity.

## Not to be confused with

- `ConvexCone.strictlyPositive R M` — the strictly positive cone, whose carrier is `{x | 0 < x}`; it is strictly smaller than the positive cone and does not include `0`.
- `PointedCone.positive R E` — a version of the positive cone packaged as a `PointedCone` rather than a `ConvexCone`; its underlying `ConvexCone` coincides with `VTask.positive R E`.
- An arbitrary `ConvexCone R M` — a general convex cone need not arise from an order; the positive cone is the canonical order-theoretic example.