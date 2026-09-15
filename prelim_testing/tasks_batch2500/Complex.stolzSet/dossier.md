## VTask.stolzSet

### Object

The Stolz set for a real parameter `M` is a subset of the complex plane consisting of all complex numbers `z` that simultaneously satisfy two conditions: (1) `z` lies strictly inside the open unit disc (i.e., `|z| < 1`), and (2) the distance from `z` to the point `1` is strictly less than `M` times the quantity `(1 − |z|)`. Geometrically, for `M > 1` the set is a roughly teardrop-shaped region with its cusp pointing toward `1` on the unit circle. As `M` increases the region expands and fills out more and more of the open unit disc. For `M ≤ 1` the set is empty. These sets arise naturally in the study of Abel-type convergence theorems for power series.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.stolzSet : (M : ℝ) -> Set ℂ
<!-- PINNED-SIGNATURE:END -->


`VTask.stolzSet : (M : ℝ) -> Set ℂ`

The single argument `M` is a real number that controls the aperture (or 'width') of the teardrop region near the boundary point `1`. Larger values of `M` yield larger sets that approach the full open unit disc; values of `M` at most `1` yield the empty set.

### Conventions

When `M ≤ 1` the defining angular condition `‖1 − z‖ < M * (1 − ‖z‖)` cannot be satisfied for any `z` with `‖z‖ < 1` (since `‖1 − z‖ ≥ 1 − ‖z‖ > 0` by the reverse triangle inequality), so the set is empty by convention (or rather, by the mathematics). No special junk-value convention is imposed beyond the definitions: the formula is applied uniformly for all real `M` including negative values, and for `M ≤ 0` the condition `M * (1 − ‖z‖) > 0` is never satisfied, so the set is again empty.

### Worked examples

- Claim: The point `0 : ℂ` belongs to `VTask.stolzSet M` for any real `M > 2`, since `‖0‖ = 0 < 1` and `‖1 − 0‖ = 1 < M * (1 − 0) = M`.

- Claim: `VTask.stolzSet M = ∅` whenever `M ≤ 1`, because for any `z` with `‖z‖ < 1` the reverse triangle inequality gives `‖1 − z‖ ≥ 1 − ‖z‖ ≥ M * (1 − ‖z‖)` when `M ≤ 1`.

- Claim: The point `z = (1/2 : ℂ)` lies in `VTask.stolzSet 3`, since `‖1/2‖ = 1/2 < 1` and `‖1 − 1/2‖ = 1/2 < 3 * (1 − 1/2) = 3/2`.

- Claim: For any `M : ℝ`, every element of `VTask.stolzSet M` lies strictly inside the open unit disc.

### Boundaries

- **`M ≤ 1`**: The set is empty. The reverse triangle inequality prevents the angular condition from being met.
- **`M = 1`**: Still empty (same reason; the inequality is strict).
- **`M > 1`**: The set is nonempty; it contains points near `1` on the real axis and expands as `M` grows.
- **`M → ∞`**: The Stolz set fills out the entire open unit disc in the limit (in the sense that the filter `𝓝[stolzSet M] 1` becomes finer).
- **`M ≤ 0`**: The right-hand side `M * (1 − ‖z‖)` is non-positive for `‖z‖ < 1`, so the condition can never be met; the set is empty.
- **Boundary of the unit disc (`‖z‖ = 1`)**: By condition (1) the boundary is excluded; only the open disc is considered.
- **The point `z = 1`**: Not in the set (it has `‖z‖ = 1`, violating condition (1)), and it serves only as the cusp/tip of the region from outside.

### Not to be confused with

- **`Complex.stolzCone`**: A different, angular cone-shaped region in the complex plane near `1`, defined via the real and imaginary parts of `z`; every Stolz cone is contained in some Stolz set but the two families are not identical.
- **The Stolz–Cesàro theorem**: An unrelated result in real analysis about limits of sequences; shares the name 'Stolz' but is entirely distinct.
- **`Metric.ball 0 1` or the open unit disc as a set**: The Stolz set is always a strict subset of the open unit disc (for finite `M`), cut further by the angular condition near `1`.
