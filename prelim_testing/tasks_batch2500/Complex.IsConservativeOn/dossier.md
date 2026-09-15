## Object

A function `f : ℂ → E` (with values in a normed complex vector space) is **conservative on** an open subset `U` of the complex plane if the integral of `f` over every axis-aligned rectangle whose boundary lies entirely in `U` is zero. Intuitively, this is a complex-analytic analogue of a path-independent (conservative) vector field: the "rectangular" circulation of `f` vanishes throughout the region.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsConservativeOn : {E : Type u_1} -> [NormedAddCommGroup E] -> [NormedSpace ℂ E] -> (f : ℂ → E) -> (U : Set ℂ) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsConservativeOn : {E : Type u_1} -> [NormedAddCommGroup E] -> [NormedSpace ℂ E] -> (f : ℂ → E) -> (U : Set ℂ) -> Prop`

The implicit type `E` is the target normed complex vector space (e.g., `ℂ` itself, or `ℂⁿ`). The two typeclass arguments equip `E` with a compatible norm and complex scalar multiplication. The explicit argument `f` is the function being tested for conservativity. The explicit argument `U` is the subset of the complex plane over which the rectangular-integral condition must hold.

## Conventions

The condition is stated in terms of a "wedge integral" from one corner to the opposite corner of a rectangle; the requirement that each such integral equal the negation of the integral taken in the reverse direction captures the vanishing of the full rectangular contour integral. No special convention applies to the empty set or to degenerate (zero-area) rectangles: the quantifier ranges over all corner pairs whose induced rectangle is contained in `U`, including degenerate cases where the rectangle collapses to a segment or a point.

## Worked examples

- Claim: Every function that is complex-differentiable (holomorphic) on an open set `U` is conservative on `U`.
  (This follows from `DifferentiableOn.isConservativeOn`.)

- Claim: If `f` is conservative on a larger set `V` and `U ⊆ V`, then `f` is conservative on `U`.
  (This follows from `IsConservativeOn.mono`.)

- Claim: A function `f : ℂ → ℂ` that is continuous everywhere and conservative on `univ` is holomorphic on `univ` (i.e., it is exact on `univ`).
  (This follows from `IsConservativeOn.isExactOn_univ`, a form of Morera's theorem.)

- Claim: If `f` is conservative on an open ball `ball c r`, then the wedge integral from `c` to `w` is a primitive of `f`, i.e., it has derivative `f z` at each point `z` in the ball.
  (This follows from `IsConservativeOn.hasDerivAt_wedgeIntegral`.)

## Boundaries

- **Empty set**: `IsConservativeOn f ∅` holds vacuously, since no rectangle can be contained in the empty set.
- **Degenerate rectangles** (where the two corner points coincide, or share a real or imaginary coordinate): the wedge integral over such a degenerate rectangle is zero regardless of `f`, so degenerate cases contribute no constraint.
- **Non-open sets**: The predicate is well-formed for any subset `U`, not just open sets; however, many consequential theorems (e.g., equivalence with holomorphicity) additionally require `U` to be open.
- **Relation to holomorphicity**: On an open set `U`, conservativity together with continuity is equivalent to complex differentiability (`isConservativeOn_and_continuousOn_iff_isDifferentiableOn`). Without continuity, conservativity alone does not imply holomorphicity.
- **Scalar-valued vs. vector-valued**: The definition applies uniformly to `E`-valued functions for any normed complex vector space `E`, not just complex-scalar functions.

## Not to be confused with

- **`IsExactOn f U`**: A stronger (or related) condition asserting that `f` has a global primitive on `U`; conservativity on a ball implies exactness on that ball, but conservativity on a general domain need not imply a global primitive without topological assumptions.
- **`DifferentiableOn ℂ f U`** (holomorphicity): Implies conservativity, and on an open set the two are equivalent when continuity is also assumed; but conservativity is the weaker, integral-based condition.
- **Real conservativity / path-independence**: In real vector calculus a conservative field has vanishing loop integrals; the complex version here restricts attention specifically to rectangular contours rather than arbitrary closed curves.
