## VTask.A

### Object

Given a function `f : ℝ → F`, a candidate derivative value `L : F`, a scale `r : ℝ`, and an error tolerance `ε : ℝ`, the set `VTask.A f L r ε` is a subset of the real line consisting of all base-points `x` near which `f` is well approximated at scale `r` by the linear map `h ↦ h • L`, up to relative error `ε`. Concretely, `x` belongs to this set if there exists a scale `r'` slightly smaller than `r` (in the half-open interval `(r/2, r]`) such that for every pair of points `y, z` in the right interval `[x, x + r']`, the deviation `‖f(z) − f(y) − (z − y) • L‖` is at most `ε * r`. The use of a sub-scale `r'` strictly above `r/2` (rather than `r` itself) is a technical device ensuring the set is open on the right in a suitable sense.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.A : {F : Type u_1} -> [NormedAddCommGroup F] -> [NormedSpace ℝ F] -> (f : ℝ → F) -> (L : F) -> (r ε : ℝ) -> Set ℝ
<!-- PINNED-SIGNATURE:END -->


VTask.A : {F : Type u_1} -> [NormedAddCommGroup F] -> [NormedSpace ℝ F] -> (f : ℝ → F) -> (L : F) -> (r ε : ℝ) -> Set ℝ

`F` is the target normed vector space over `ℝ`. The instance arguments supply the norm and the real scalar structure on `F`. The argument `f` is the function being studied. The argument `L` is the proposed derivative value — the vector in `F` playing the role of the slope of `f` at scale `r`. The argument `r` is the spatial scale at which the approximation is being assessed. The argument `ε` is the dimensionless error tolerance: the approximation error `‖f(z) − f(y) − (z − y) • L‖` must be at most `ε` times the scale `r`.

### Conventions

When `ε ≤ 0`, the error bound `ε * r` is non-positive, so membership requires the approximation error to be at most a non-positive number; for typical nonzero `f` this makes the set empty, but the definition places no special junk-value rule here — it is simply what the formula gives. When `r ≤ 0`, the interval `(r/2, r]` is empty, so there is no witness `r'` and the set is empty. The definition is stated for all real `r` and `ε` without restriction.

### Worked examples

- Claim: If `f` is the zero function on `ℝ → ℝ` and `L = 0`, then every `x : ℝ` belongs to `VTask.A f 0 r ε` for any `r > 0` and `ε ≥ 0`, because all approximation errors are zero.

- Claim: If `f(t) = t` (the identity on `ℝ`) and `L = 1`, then for any `r > 0` and any `ε ≥ 0`, every `x : ℝ` lies in `VTask.A f 1 r ε`, because `f(z) − f(y) − (z − y) • 1 = 0` for all `y, z`.

- Claim: For any `r > 0` and `ε₁ ≤ ε₂`, the set `VTask.A f L r ε₁` is a subset of `VTask.A f L r ε₂` (monotonicity in the error tolerance).

- Claim: If `r ≤ 0`, then `VTask.A f L r ε = ∅` for any `f`, `L`, `ε`, because the interval `Ioc (r/2) r` is empty and no witness `r'` exists.

### Boundaries

- When `r ≤ 0`: the interval `(r/2, r]` is empty, so no scale `r'` can be found; the set is empty.
- When `ε < 0`: the bound `ε * r` (for `r > 0`) is negative, so no pair `(y, z)` can satisfy the norm inequality unless the approximation error is exactly zero; the set may be empty for generic `f`.
- The right-openness tweak (using `r' ∈ (r/2, r]` rather than insisting on `r` itself) ensures that membership at a point propagates to a right neighbourhood of that point, making `VTask.A f L r ε` a member of the right-neighbourhood filter at each of its points.
- If `f` is differentiable from the right at `x` with right derivative `L`, then for any `ε > 0` there exists `R > 0` such that `x ∈ VTask.A f L r ε` for all `r ∈ (0, R)`.
- Two candidate derivative vectors `L₁` and `L₂` that both place `x` in their respective sets at the same scale satisfy `‖L₁ − L₂‖ ≤ 4ε`, so the approximating vector is essentially unique for small `ε`.

### Not to be confused with

- The set `D f K` used in the same measurability argument: that is a derived object built by intersecting and unioning the `A`-sets, capturing points where the right derivative of `f` lies in a closed set `K`.
- The standard definition of differentiability or the derivative itself: `VTask.A f L r ε` is a quantitative, scale-localised approximation set, not a statement about limits.
- `Ioc (r/2) r` (the interval used inside the definition): that is a subset of the real line, whereas `VTask.A f L r ε` is a subset of the domain of `f`.