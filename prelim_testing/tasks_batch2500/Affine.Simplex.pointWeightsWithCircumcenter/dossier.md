## Object

`VTask.pointWeightsWithCircumcenter i` is a weight function on the index type `PointsWithCircumcenterIndex n`, which labels the n+1 vertices of an n-simplex together with its circumcenter. The weight function places weight 1 on the vertex indexed by `i`, weight 0 on every other vertex, and weight 0 on the circumcenter index. It is the barycentric weight vector that picks out a single vertex of the simplex when forming an affine combination over the extended point set that includes the circumcenter.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pointWeightsWithCircumcenter : {n : ℕ} -> (i : Fin (n + 1)) -> Affine.Simplex.PointsWithCircumcenterIndex n → ℝ
<!-- PINNED-SIGNATURE:END -->


`{n : ℕ} -> (i : Fin (n + 1)) -> Affine.Simplex.PointsWithCircumcenterIndex n → ℝ`

The implicit argument `n` is the dimension of the simplex (so the simplex has n+1 vertices). The explicit argument `i` is the index, ranging over `Fin (n + 1)`, of the particular vertex whose weight is being isolated. The final argument is a `PointsWithCircumcenterIndex n` value — either a vertex index `pointIndex j` for some `j : Fin (n + 1)`, or the special `circumcenterIndex` — and the function returns the real-valued weight assigned to that index entry.

## Conventions

The weight assigned to `circumcenterIndex` is always 0, regardless of `i`; the circumcenter plays no role in expressing a bare vertex as an affine combination. The weight assigned to `pointIndex j` is 1 if `j = i` and 0 otherwise, using decidable equality on `Fin (n + 1)`. No junk values arise because the function is total and well-defined on both constructors of `PointsWithCircumcenterIndex n`.

## Worked examples

- Claim: For any `n` and vertex index `i`, `VTask.pointWeightsWithCircumcenter i (pointIndex i) = 1` — the weight at the selected vertex is 1.

- Claim: For distinct `i j : Fin (n + 1)` with `i ≠ j`, `VTask.pointWeightsWithCircumcenter i (pointIndex j) = 0` — the weight at any other vertex is 0.

- Claim: `VTask.pointWeightsWithCircumcenter i circumcenterIndex = 0` — the circumcenter always receives weight 0.

- Claim: The weights sum to 1: `∑ j, VTask.pointWeightsWithCircumcenter i j = 1` for every valid `i`.

- Claim: Using these weights in an affine combination over `s.pointsWithCircumcenter` recovers exactly `s.points i`.

## Boundaries

- When `n = 0` there is exactly one vertex (`i : Fin 1` forces `i = 0`), and `PointsWithCircumcenterIndex 0` has two elements: `pointIndex 0` and `circumcenterIndex`. The weight vector is `{pointIndex 0 ↦ 1, circumcenterIndex ↦ 0}`, which is the only possible non-trivial case.
- The equality check `j = i` uses the standard decidable equality on `Fin (n + 1)`, so there is no ambiguity at the boundary between equal and unequal indices.
- All weights are integers (0 or 1) embedded in ℝ; no floating-point or continuity concerns arise.

## Not to be confused with

- `Affine.Simplex.circumcenterWeightsWithCircumcenter`: the analogous weight function that gives weight 1 to the `circumcenterIndex` and 0 to all vertices, used to express the circumcenter itself as an affine combination.
- `Affine.Simplex.pointsWithCircumcenter`: the function that maps `PointsWithCircumcenterIndex n` to actual points in the ambient space (vertices and circumcenter), of which `VTask.pointWeightsWithCircumcenter` supplies the coefficients.
- Barycentric coordinates of a general point: unlike general barycentric coordinate maps, this function is not computing coordinates of an arbitrary point but simply selecting a basis vertex via a 0-1 weight vector.