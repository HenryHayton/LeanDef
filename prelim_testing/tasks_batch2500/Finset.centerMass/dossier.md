## VTask.centerMass

### Object

The weighted center of mass (barycenter) of a finite collection of points in a module over a field. Given a finite index set, a weight function assigning a scalar to each index, and a point function assigning a vector to each index, the center of mass is the vector obtained by scaling the weighted sum of the points by the reciprocal of the total weight. This generalizes the usual notion of a weighted average: if the weights are nonnegative and sum to 1, the result is a convex combination of the points, but the definition imposes neither constraint.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.centerMass : {R : Type u_1} -> {E : Type u_3} -> {ι : Type u_5} -> [Field R] -> [AddCommGroup E] -> [Module R E] -> (t : Finset ι) -> (w : ι → R) -> (z : ι → E) -> E
<!-- PINNED-SIGNATURE:END -->


`VTask.centerMass : {R : Type u_1} -> {E : Type u_3} -> {ι : Type u_5} -> [Field R] -> [AddCommGroup E] -> [Module R E] -> (t : Finset ι) -> (w : ι → R) -> (z : ι → E) -> E`

The implicit type `R` is the scalar field of weights; `E` is the ambient module (vector space) in which the points live; `ι` is the type used to index the collection of points. The first explicit argument `t` is the finite index set determining which points and weights participate in the computation. The second explicit argument `w` is the weight function, assigning a scalar in `R` to each index; only the values at indices in `t` are used. The third explicit argument `z` is the point function, assigning a vector in `E` to each index; again only values at indices in `t` matter. The return value is the center of mass, an element of `E`.

### Conventions

When the total weight `∑ i ∈ t, w i` is zero, the reciprocal of zero in the field `R` is zero (by the junk-value convention for `Field.inv`), so `VTask.centerMass t w z` evaluates to the zero vector of `E` in that degenerate case. No nonnegativity of weights is required and the weights need not sum to 1; the definition is formally valid for arbitrary weight functions.

### Worked examples

- Claim: For the two-point set `{0, 1}` in `ℚ` with equal weights `w i = 1` and points `z 0 = 0`, `z 1 = 4`, the center of mass is `2`.
  The total weight is `1 + 1 = 2`, the weighted sum is `1 * 0 + 1 * 4 = 4`, and the center of mass is `(1/2) * 4 = 2`.

- Claim: For the singleton set `{0}` with weight `w 0 = 3` and point `z 0 = v`, the center of mass equals `v`.
  The total weight is `3`, the weighted sum is `3 * v`, and `(1/3) * (3 * v) = v`.

- Claim: For any finite set `t` and weight function `w` with `∑ i ∈ t, w i = 0`, `VTask.centerMass t w z = 0`.
  The reciprocal of `0` in a field is `0`, so the result is `0 • (∑ i ∈ t, w i • z i) = 0`.

- Claim: For the three-point set `{0, 1, 2}` with weights `1, 1, 1` and points `z i = i` (in `ℚ`), the center of mass is `1`.
  Total weight `3`, weighted sum `0 + 1 + 2 = 3`, center of mass `(1/3) * 3 = 1`.

### Boundaries

- **Empty index set**: When `t = ∅`, both the weighted sum and the total weight are `0`. The reciprocal of `0` is `0`, so `VTask.centerMass ∅ w z = 0` (the zero vector) regardless of `w` and `z`.
- **Zero total weight with nonzero points**: When the weights cancel (e.g., `w 0 = 1, w 1 = -1` with equal magnitudes), the total weight is `0`, and the result is again the zero vector by the junk-value convention.
- **Singleton set**: `VTask.centerMass {i} w z = z i`, since `(w i)⁻¹ * (w i * z i) = z i` when `w i ≠ 0`; when `w i = 0`, the result is `0`.
- **Unit total weight**: When `∑ i ∈ t, w i = 1`, the center of mass is exactly `∑ i ∈ t, w i • z i`, the plain weighted sum.
- **Negative or non-probability weights**: Permitted; the formula is purely algebraic.

### Not to be confused with

- **`Finset.sum` (plain weighted sum)**: Computes `∑ i ∈ t, w i • z i` without dividing by the total weight; equals `VTask.centerMass` only when the total weight is 1.
- **Affine combination / convex combination**: A convex combination requires `w i ≥ 0` and `∑ w i = 1`; `VTask.centerMass` imposes neither condition and is the underlying algebraic operation.
- **`Finset.average` or arithmetic mean**: The arithmetic mean is the special case where all weights are equal; `VTask.centerMass` with uniform weights `w i = 1` recovers the arithmetic mean (when `|t| ≠ 0` in the field).