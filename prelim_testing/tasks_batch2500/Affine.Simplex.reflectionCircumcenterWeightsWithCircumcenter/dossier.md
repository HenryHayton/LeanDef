## VTask.reflectionCircumcenterWeightsWithCircumcenter

### Object

This function produces a weight system — a real-valued function on the index type `PointsWithCircumcenterIndex n` — that encodes the affine combination expressing the reflection of the circumcenter of an n-simplex across the affine span of one of its edges (a pair of vertices). Concretely, the weight system assigns weight 1 to each of the two distinguished vertex indices i₁ and i₂, weight 0 to all other vertex indices, and weight −1 to the circumcenter index. When the two indices are distinct, these weights sum to 1, making the combination a valid affine combination, and the resulting affine combination of the simplex's points-with-circumcenter structure yields the reflection of the circumcenter in the edge spanned by those two vertices.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.reflectionCircumcenterWeightsWithCircumcenter : {n : ℕ} -> (i₁ i₂ : Fin (n + 1)) -> Affine.Simplex.PointsWithCircumcenterIndex n → ℝ
<!-- PINNED-SIGNATURE:END -->


The implicit argument `n` is the dimension of the simplex (so the simplex has n + 1 vertices). The arguments `i₁` and `i₂` are the two vertex indices (elements of `Fin (n + 1)`) whose span defines the edge — equivalently, the mirror line — across which the circumcenter is reflected. The final argument is an element of the index type `PointsWithCircumcenterIndex n`, which ranges over the n + 1 vertex positions (via `pointIndex`) and the circumcenter position (via `circumcenterIndex`); the function returns the real weight assigned to that index.

### Conventions

The definition is stated without an explicit distinctness hypothesis, but it is only geometrically meaningful (and the weights only sum to 1) when `i₁ ≠ i₂`. When `i₁ = i₂`, the weights still evaluate but yield a sum of 1 only if one counts the coincident index once, which in the Finset sum context means the sum equals 1 only under the non-coincidence condition — callers are responsible for ensuring `i₁ ≠ i₂` before using the affine combination result.

### Worked examples

- Claim: For any `n` and any vertex index `i`, if `i = i₁` then `VTask.reflectionCircumcenterWeightsWithCircumcenter i₁ i₂ (pointIndex i) = 1` (the two selected vertices get weight 1).

- Claim: For any `n`, `i₁`, `i₂`, the weight at the circumcenter index is −1: `VTask.reflectionCircumcenterWeightsWithCircumcenter i₁ i₂ circumcenterIndex = -1`.

- Claim: For a vertex index `i` that equals neither `i₁` nor `i₂`, the weight is 0: `VTask.reflectionCircumcenterWeightsWithCircumcenter i₁ i₂ (pointIndex i) = 0` whenever `i ≠ i₁` and `i ≠ i₂`.

- Claim: When `i₁ ≠ i₂`, the weights sum to 1: `∑ idx, VTask.reflectionCircumcenterWeightsWithCircumcenter i₁ i₂ idx = 1`.

### Boundaries

- **`i₁ = i₂` (degenerate edge):** The function still evaluates — the coincident vertex gets weight 1 (counted once in the weight function despite appearing in both branches of the disjunction, which collapse), and all other vertices get 0, with the circumcenter getting −1. The total sum equals 1 − 1 = 0, not 1, so the result does **not** form a valid affine combination. The reflection interpretation breaks down entirely in this case.
- **`n = 0` (0-simplex, a single point):** There is only one vertex index (`i₁` and `i₂` must both be `0 : Fin 1`), so the non-coincidence condition `i₁ ≠ i₂` cannot be satisfied; the edge-reflection is undefined in any geometric sense.
- **Large `n`:** For vertices `i` with `i ≠ i₁` and `i ≠ i₂`, the weight is exactly 0; only two of the n + 1 vertex weights are nonzero.

### Not to be confused with

- **`circumcenterWeightsWithCircumcenter`**: The analogous weight function for expressing the circumcenter itself (not its reflection) as an affine combination, which assigns equal weights to all vertices and weight 1 to the circumcenter index.
- **`pointsWithCircumcenter`**: The function mapping `PointsWithCircumcenterIndex n` to actual points in the ambient Euclidean space; this dossier's object assigns *weights* to those indices, not points.
- **`reflection (affineSpan ℝ ...)` applied directly**: The geometric reflection map itself, which acts on points; this weight function is the *coordinate description* of that reflection's output, not the reflection operator.