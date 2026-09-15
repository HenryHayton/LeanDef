## Object

`VTask.expNegInvGlue` is the real-valued function on ℝ defined by the rule: it equals `exp(−1/x)` for `x > 0`, and equals `0` for `x ≤ 0`. This is a classical smooth (C^∞) bump-like building block used to construct smooth partitions of unity; the key feature is that it transitions from the zero function on the non-positive reals to a positive function on the positive reals in an infinitely differentiable way, even though no Taylor series at `0` can detect the positive-side behavior (the function is not real-analytic at the origin).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.expNegInvGlue : (x : ℝ) -> ℝ
<!-- PINNED-SIGNATURE:END -->


`VTask.expNegInvGlue : (x : ℝ) -> ℝ`

The single argument `x` is the real number at which the function is evaluated.

## Conventions

At the boundary point `x = 0`, the function takes the value `0` (the non-positive branch is used, since `0 ≤ 0`). There is no junk value: the function is total on all of ℝ and its value is determined by the two-branch rule everywhere.

## Worked examples

- Claim: `VTask.expNegInvGlue 0 = 0` (the boundary point returns zero, matching the non-positive branch).

- Claim: `VTask.expNegInvGlue (-3) = 0` (any strictly negative input returns zero).

- Claim: `VTask.expNegInvGlue 1 = Real.exp (-1)` (at `x = 1` the positive branch gives `exp(−1/1) = exp(−1)`).

- Claim: For all `x : ℝ`, `0 ≤ VTask.expNegInvGlue x` (the function is everywhere nonnegative, since `exp` is always positive and the zero branch is nonnegative).

- Claim: For `x > 0`, `VTask.expNegInvGlue x > 0` (strictly positive on the positive reals).

- Claim: `VTask.expNegInvGlue` is `C^∞` (smooth/contDiff of any order `n : ℕ∞`), even though it is not real-analytic at `0`.

## Boundaries

- At `x = 0`: the function equals `0`. The limit from the right also tends to `0` (since `exp(−1/x) → 0` as `x → 0⁺`), so there is no jump; the function is continuous (and in fact smooth) at `0`.
- For `x ≤ 0`: the function is identically `0`, so all derivatives at non-positive points are zero.
- As `x → +∞`: `−1/x → 0`, so `exp(−1/x) → exp(0) = 1`; the function approaches `1` from below but never reaches it on ℝ (it is bounded above by `1`).
- The function is monotone non-decreasing on all of ℝ.
- At `x = 0` specifically, the function is NOT real-analytic (not equal to any convergent power series in a neighborhood), despite being C^∞.

## Not to be confused with

- `Real.exp`: the plain exponential function `x ↦ exp(x)`, which has no two-branch structure and is everywhere positive and real-analytic.
- `Real.smoothTransition`: a related smooth function built from `VTask.expNegInvGlue` that transitions from `0` to `1` on the interval `[0,1]`, used directly as a smooth cutoff.
- A bump function supported on a compact interval: `VTask.expNegInvGlue` is supported on `(0, +∞)` (a half-line), not a compact set, so it is a half-bump rather than a compactly supported bump.