## VTask.circumcenterWeightsWithCircumcenter

### Object

A weight function on the augmented index type `PointsWithCircumcenterIndex n` that encodes the circumcenter of an `n`-simplex as an affine combination of its vertices together with the circumcenter itself. It assigns weight 1 to the circumcenter index and weight 0 to every vertex index. This is the "trivial" barycentric-style representation of the circumcenter: the circumcenter is simply itself, expressed as a weighted sum where only the circumcenter term contributes.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.circumcenterWeightsWithCircumcenter : (n : ℕ) -> Affine.Simplex.PointsWithCircumcenterIndex n → ℝ
<!-- PINNED-SIGNATURE:END -->


`VTask.circumcenterWeightsWithCircumcenter : (n : ℕ) -> Affine.Simplex.PointsWithCircumcenterIndex n → ℝ`

The first argument `n` is the dimension parameter of the simplex (a natural number), determining the range of vertex indices. The second argument is an index in the augmented point set `PointsWithCircumcenterIndex n`, which consists of the `n+1` vertex indices (each of the form `pointIndex i`) together with one distinguished circumcenter index (`circumcenterIndex`); the function returns the real-valued weight assigned to that index.

### Conventions

Every vertex index (`pointIndex i` for any valid `i`) receives weight exactly 0. The circumcenter index (`circumcenterIndex`) receives weight exactly 1. There are no other cases: the two constructors cover the entire type.

### Worked examples

- Claim: For any `n`, `VTask.circumcenterWeightsWithCircumcenter n circumcenterIndex = 1`

- Claim: For any `n` and any vertex index `i : Fin (n + 1)`, `VTask.circumcenterWeightsWithCircumcenter n (pointIndex i) = 0`

- Claim: For `n = 2`, the weight at `circumcenterIndex` is 1 and the weight at each of the three vertex indices (`pointIndex ⟨0, _⟩`, `pointIndex ⟨1, _⟩`, `pointIndex ⟨2, _⟩`) is 0, so the weights sum to 1.

- Claim: The function is non-negative everywhere: for any `n` and any `idx : PointsWithCircumcenterIndex n`, `0 ≤ VTask.circumcenterWeightsWithCircumcenter n idx`.

### Boundaries

- When `n = 0` the simplex is a single point (a 0-simplex). There is exactly one vertex index (`pointIndex ⟨0, _⟩`) and one circumcenter index. The weight function still returns 0 at the vertex and 1 at the circumcenter.
- The function is total: it is defined for every natural number `n` and every element of `PointsWithCircumcenterIndex n` without restriction.
- The weights sum to 1 (only the circumcenter index contributes, with weight 1), consistent with the requirement that the weighted combination is an affine combination.

### Not to be confused with

- `Affine.Simplex.circumcenterWeights`: the circumcenter weights expressed purely over the vertex indices of the simplex (without the augmented circumcenter index), giving the actual barycentric coefficients of the circumcenter with respect to the vertices.
- `VTask.pointsWithCircumcenter`: the function that maps `PointsWithCircumcenterIndex n` to the actual points in the ambient affine space (vertices plus circumcenter), as opposed to the weights assigned to those points.
- Weight functions for other distinguished centers (e.g., centroid weights), which assign equal nonzero weight `1/(n+1)` to each vertex index and 0 to the circumcenter index.