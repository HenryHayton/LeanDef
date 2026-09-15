## VTask.centroidWeightsWithCircumcenter

### Object

Given a finite set `fs` of vertex indices of an `n`-simplex, this function produces a real-valued weight function on the extended index type that records both the `n+1` vertices and the circumcenter of the simplex. The weight assigned to vertex index `i` is `1/|fs|` if `i` belongs to `fs`, and `0` otherwise; the weight assigned to the circumcenter index is always `0`. When used as the coefficient vector in an affine combination over the augmented point set (vertices plus circumcenter), the result is exactly the centroid of the sub-collection of vertices indexed by `fs`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.centroidWeightsWithCircumcenter : {n : ℕ} -> (fs : Finset (Fin (n + 1))) -> Affine.Simplex.PointsWithCircumcenterIndex n → ℝ
<!-- PINNED-SIGNATURE:END -->


`{n : ℕ} -> (fs : Finset (Fin (n + 1))) -> Affine.Simplex.PointsWithCircumcenterIndex n → ℝ`

The implicit argument `n` is the dimension of the ambient simplex (which has `n + 1` vertices). The explicit argument `fs` is the finite set of vertex indices whose centroid is desired; it is a subset of `Fin (n + 1)`. The return type is a weight function on `PointsWithCircumcenterIndex n`, the two-constructor type whose terms are either a vertex index `pointIndex i` for `i : Fin (n + 1)` or the special term `circumcenterIndex`.

### Conventions

When `fs` is empty the weight at every index is `0` (since `(0 : ℝ)⁻¹ = 0` in Mathlib's real-number division), so the sum of weights is `0` rather than `1`; the resulting affine combination is not a proper affine combination and does not represent a centroid in the usual sense.

### Worked examples

- Claim: For any `n` and any `i : Fin (n + 1)` with `i ∈ fs`, `VTask.centroidWeightsWithCircumcenter fs (pointIndex i) = (↑(Finset.card fs))⁻¹`.

- Claim: For any `n` and any `i : Fin (n + 1)` with `i ∉ fs`, `VTask.centroidWeightsWithCircumcenter fs (pointIndex i) = 0`.

- Claim: For any `n` and any `fs`, `VTask.centroidWeightsWithCircumcenter fs circumcenterIndex = 0`.

- Claim: When `fs = Finset.univ` (all vertices of a 2-simplex), the weight at each vertex index is `1/3`, and `∑ i, VTask.centroidWeightsWithCircumcenter Finset.univ i = 1`.

- Claim: When `fs` is the singleton `{j}`, the weight at `pointIndex j` is `1` and at `pointIndex i` (for `i ≠ j`) is `0`, so the affine combination recovers vertex `j` itself.

### Boundaries

- **Empty `fs`**: Every weight is `0`; the sum of weights is `0`, not `1`. The function is still well-defined by the convention `(0 : ℝ)⁻¹ = 0`.
- **Nonempty `fs`**: The weights sum to `1` (theorem `sum_centroidWeightsWithCircumcenter`), making them valid affine-combination coefficients.
- **Circumcenter slot**: Always receives weight `0` regardless of `fs`, so the circumcenter never contributes to the resulting affine combination.
- **Full vertex set (`fs = Finset.univ`)**: Each vertex weight equals `1/(n+1)`, giving the barycenter (centroid) of all vertices.

### Not to be confused with

- `Affine.Simplex.circumcenterWeightsWithCircumcenter`: assigns weight `1` to the circumcenter index and `0` to all vertex indices, producing the circumcenter rather than a vertex centroid.
- `Affine.Simplex.mongePointWeightsWithCircumcenter`: a related but different weight function used to express the Monge point via the same augmented point set.
- `Finset.centroid`: the direct affine-geometric centroid of a finite set of points, not expressed as weights over the augmented `PointsWithCircumcenterIndex` type.