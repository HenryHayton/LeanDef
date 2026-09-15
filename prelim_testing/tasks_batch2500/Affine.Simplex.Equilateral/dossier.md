## Object

A simplex is *equilateral* if every pair of distinct vertices is the same distance apart. Equivalently, there exists a single real number `r` such that the distance between any two distinct vertices of the simplex equals `r`. This generalises the familiar notion of an equilateral triangle to simplices of any dimension.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Equilateral : {R : Type u_1} -> {V : Type u_2} -> {P : Type u_3} -> [Ring R] -> [SeminormedAddCommGroup V] -> [PseudoMetricSpace P] -> [Module R V] -> [NormedAddTorsor V P] -> {n : ℕ} -> (s : Affine.Simplex R P n) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Equilateral : {R : Type u_1} -> {V : Type u_2} -> {P : Type u_3} -> [Ring R] -> [SeminormedAddCommGroup V] -> [PseudoMetricSpace P] -> [Module R V] -> [NormedAddTorsor V P] -> {n : ℕ} -> (s : Affine.Simplex R P n) -> Prop`

The implicit type `R` is the scalar ring; `V` is the normed vector space of translations; `P` is the (pseudo-)metric space of points. The natural number `n` determines the dimension of the simplex (so the simplex has `n + 1` vertices). The explicit argument `s` is the affine simplex whose equilaterality is being tested.

## Conventions

The common edge length `r` is existentially quantified and is allowed to be zero; a degenerate simplex where all vertices coincide is technically equilateral with `r = 0`. The predicate is stated for any `Ring R` and `PseudoMetricSpace P`, so it makes sense even when the metric is only a pseudometric and distances can fail to separate points.

## Worked examples

- Claim: For a 1-simplex (line segment) in ℝ, the simplex whose two vertices are 0 and 1 satisfies `VTask.Equilateral` with common length 1.

- Claim: Every regular simplex satisfies `VTask.Equilateral`; that is, if `s.Regular` holds then `VTask.Equilateral s` holds.

- Claim: For any equilateral simplex `s : Affine.Simplex ℝ P n` with `n ≥ 2` and distinct indices `i₁ i₂ i₃`, the angle `∠ (s.points i₁) (s.points i₂) (s.points i₃) = π / 3`.

- Claim: If `VTask.Equilateral s` holds then for any two pairs of distinct vertex indices `(i₁, i₂)` and `(i₃, i₄)`, the distances `dist (s.points i₁) (s.points i₂)` and `dist (s.points i₃) (s.points i₄)` are equal.

## Boundaries

- **0-simplex (single vertex):** There are no pairs of distinct vertices, so the condition `∀ i j, i ≠ j → dist ... = r` is vacuously true for any `r`; every 0-simplex is trivially equilateral.
- **Degenerate simplex (all vertices coincide):** The common distance is 0, so the predicate holds with `r = 0`.
- **1-simplex (edge):** There is exactly one pair of distinct vertices; the condition reduces to naming the single edge length as `r`, so every 1-simplex is equilateral.
- **Higher dimensions:** For `n ≥ 2`, the condition is genuinely non-trivial: all `(n+1)n/2` pairwise distances must agree.

## Not to be confused with

- **`Affine.Simplex.Regular`**: A regular simplex is both equilateral *and* equiangular (all angles equal); equilateral alone does not imply regularity in general normed spaces.
- **`Affine.Simplex.AcuteAngled`**: A weaker consequence of equilaterality over ℝ; an equilateral simplex is always acute-angled, but acute-angled simplices need not be equilateral.
- **Isosceles or isometric conditions**: Being equilateral is about all *edge lengths* being equal, not about all vertex-to-centroid distances or face areas being equal.