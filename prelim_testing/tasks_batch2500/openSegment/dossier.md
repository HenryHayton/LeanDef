## VTask.openSegment

### Object

The open segment between two points `x` and `y` in a module `E` over an ordered semiring `𝕜` is the set of all strict convex combinations of `x` and `y`. Concretely, it consists of every point of the form `a • x + b • y` where `a` and `b` are *strictly positive* elements of `𝕜` that sum to `1`. Unlike the closed segment, the endpoints themselves are excluded whenever the semiring structure forces `a` or `b` to be zero — but note the important caveat that if `x = y` the open segment always equals `{x}`, because any strictly positive `a` and `b` with `a + b = 1` still yield `a • x + b • x = x`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.openSegment : (𝕜 : Type u_1) -> {E : Type u_2} -> [Semiring 𝕜] -> [PartialOrder 𝕜] -> [AddCommMonoid E] -> [SMul 𝕜 E] -> (x y : E) -> Set E
<!-- PINNED-SIGNATURE:END -->


`(𝕜 : Type u_1) -> {E : Type u_2} -> [Semiring 𝕜] -> [PartialOrder 𝕜] -> [AddCommMonoid E] -> [SMul 𝕜 E] -> (x y : E) -> Set E`

The explicit type argument `𝕜` is the ordered semiring of scalars used to form convex combinations; it determines what "strictly positive" and "sums to 1" mean. The implicit type `E` is the ambient vector space (or module) in which the segment lives. The two explicit point arguments `x` and `y` are the endpoints: `x` is the left endpoint and `y` is the right endpoint of the open segment.

### Conventions

When both endpoints coincide (`x = y`), the open segment `VTask.openSegment 𝕜 x x` equals the singleton `{x}` rather than the empty set. This holds whenever the base semiring `𝕜` contains at least one element `t` strictly between `0` and `1` (so that `a = t` and `b = 1 - t` are both strictly positive and sum to `1`), which is the case for typical scalar fields such as `ℝ` or `ℚ`.

### Worked examples

- Claim: A point `z` belongs to `VTask.openSegment ℝ x y` if and only if there exist real numbers `a > 0` and `b > 0` with `a + b = 1` and `a • x + b • y = z`.

- Claim: For `x y : ℝ`, the midpoint `(x + y) / 2` belongs to `VTask.openSegment ℝ x y` whenever `x ≠ y`, witnessed by `a = 1/2` and `b = 1/2`.

- Claim: `VTask.openSegment ℝ (0 : ℝ) 1` is the open interval `(0, 1)` in `ℝ`, i.e., `VTask.openSegment ℝ (0 : ℝ) 1 = Set.Ioo 0 1`.

- Claim: `VTask.openSegment ℝ (x : ℝ) x = {x}` for any real number `x`, because `(1/2) • x + (1/2) • x = x` with `1/2 > 0` and `1/2 + 1/2 = 1`.

- Claim: The open segment is symmetric: for all `x y : E`, `VTask.openSegment 𝕜 x y = VTask.openSegment 𝕜 y x`, since any witnessing pair `(a, b)` for one direction gives `(b, a)` for the other.

### Boundaries

- **Equal endpoints**: `VTask.openSegment 𝕜 x x = {x}` (not `∅`) whenever `𝕜` has an element strictly between `0` and `1`, such as `1/2` in `ℝ`. This is the most important non-obvious edge case.
- **No strict positivity**: If the ordered semiring `𝕜` has no element strictly between `0` and `1` (for example, `𝕜 = ℕ` or any semiring where `0` and `1` are adjacent in the order), then `VTask.openSegment 𝕜 x y` may be empty for `x ≠ y`, since no `a, b > 0` with `a + b = 1` can exist.
- **Endpoints not members**: For `x ≠ y` over `ℝ` (or any linearly ordered field), neither `x` nor `y` belongs to `VTask.openSegment 𝕜 x y`, distinguishing it from the closed segment.
- **Contained in any convex set containing both endpoints**: If a convex set `s` contains both `x` and `y`, then `VTask.openSegment 𝕜 x y ⊆ s`.

### Not to be confused with

- **`segment 𝕜 x y`** (the closed segment): includes both endpoints `x` and `y`, using `0 ≤ a`, `0 ≤ b` instead of strict positivity.
- **`Set.Ioo x y`** (open interval in a linear order): a purely order-theoretic notion on a linearly ordered type, not involving scalar combinations; coincides with the open segment for `ℝ` but is a different definition in general.
- **`interior (segment 𝕜 x y)`** (topological interior of the closed segment): topologically equivalent to the open segment for `x ≠ y` in normed spaces, but requires a topological structure that `VTask.openSegment` does not.
