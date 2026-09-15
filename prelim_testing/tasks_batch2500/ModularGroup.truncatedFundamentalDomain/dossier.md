## VTask.truncatedFundamentalDomain

### Object

The *truncated fundamental domain* at height `y` is the subset of the complex upper half-plane consisting of those points that belong to the standard (Ford–Klein) fundamental domain for the action of SL(2,ℤ) on the upper half-plane AND whose imaginary part is at most `y`. Geometrically, one takes the classical fundamental domain — the region satisfying |Re(τ)| ≤ 1/2 and |τ| ≥ 1 — and cuts it off from above by the horizontal line Im(τ) = y. When y is large, the truncated domain approximates the full fundamental domain; when y is small (e.g., y < √3/2), the set may be empty.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.truncatedFundamentalDomain : (y : ℝ) -> Set UpperHalfPlane
<!-- PINNED-SIGNATURE:END -->


`VTask.truncatedFundamentalDomain : (y : ℝ) -> Set UpperHalfPlane`

The single argument `y` is the cutoff height: only points of the upper half-plane whose imaginary part does not exceed `y` are retained. It is a real number and is not required to be positive or to exceed any particular threshold.

### Conventions

There are no special junk-value conventions to declare: the definition is total over all real `y`, and for any value of `y` it simply returns the (possibly empty) set of upper-half-plane points satisfying both the standard-fundamental-domain membership condition and the imaginary-part bound. No sentinel or default value is needed.

### Worked examples

- Claim: The point `τ = i` (i.e., Re = 0, Im = 1) belongs to `VTask.truncatedFundamentalDomain 2`, because `i` lies in the standard fundamental domain (|Re(i)| = 0 ≤ 1/2, |i| = 1 ≥ 1) and Im(i) = 1 ≤ 2.

- Claim: The point `τ = i` does NOT belong to `VTask.truncatedFundamentalDomain 0.5`, because even though `i` is in the standard fundamental domain, Im(i) = 1 > 0.5, so the height condition is violated.

- Claim: For any `y < 0`, the set `VTask.truncatedFundamentalDomain y` is empty, since every point of the upper half-plane has positive imaginary part and thus Im(τ) > 0 > y is false — wait, actually Im(τ) > 0 means the condition Im(τ) ≤ y with y < 0 can never be satisfied, so the set is empty.

- Claim: `VTask.truncatedFundamentalDomain y₁ ⊆ VTask.truncatedFundamentalDomain y₂` whenever `y₁ ≤ y₂`, since any point satisfying Im(τ) ≤ y₁ automatically satisfies Im(τ) ≤ y₂.

### Boundaries

- **y < 0**: The set is empty; no point of the upper half-plane has non-positive imaginary part.
- **0 < y < √3/2 (approximately 0.866)**: The height bound cuts below the lowest points of the standard fundamental domain (whose minimum imaginary part is √3/2), so the set is empty.
- **y = √3/2**: Only the two corner points of the fundamental domain at imaginary part exactly √3/2 can be in the set (the points e^{iπ/3} and e^{2iπ/3}).
- **y → +∞**: The truncated domain converges (in an appropriate sense) to the full standard fundamental domain.
- **y is negative infinity (conceptually)**: The set is empty for all sufficiently negative y.

### Not to be confused with

- **The standard fundamental domain `𝒟`** (without truncation): this is the full, unbounded version; the truncated variant adds the additional constraint Im(τ) ≤ y.
- **A fundamental domain truncated from below**: one could instead require Im(τ) ≥ y (a *Siegel set*-style lower truncation); this definition truncates from *above*.
- **`Set.Iic` applied to the imaginary part**: the truncated fundamental domain is an intersection, not merely the preimage of (-∞, y] under Im; membership in the standard fundamental domain is also required.