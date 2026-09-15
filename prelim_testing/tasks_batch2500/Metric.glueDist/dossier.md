## Object

`VTask.glueDist` defines a **predistance function** on the disjoint union `X ⊕ Y` of two metric spaces, controlled by a parameter `ε`. It is constructed so that identified points — a point `Φ p` in `X` and its counterpart `Ψ p` in `Y` — are declared to be at distance exactly `ε` from one another (when they are the sole representatives in `Z`). Within each summand the predistance agrees with the original metric, while the cross-summand distance between a point `x ∈ X` and a point `y ∈ Y` is the infimum over all mediating points `p ∈ Z` of `dist(x, Φ p) + dist(y, Ψ p)`, plus the offset `ε`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.glueDist : {X : Type u} -> {Y : Type v} -> {Z : Type w} -> [MetricSpace X] -> [MetricSpace Y] -> (Φ : Z → X) -> (Ψ : Z → Y) -> (ε : ℝ) -> X ⊕ Y → X ⊕ Y → ℝ
<!-- PINNED-SIGNATURE:END -->


`VTask.glueDist : {X : Type u} -> {Y : Type v} -> {Z : Type w} -> [MetricSpace X] -> [MetricSpace Y] -> (Φ : Z → X) -> (Ψ : Z → Y) -> (ε : ℝ) -> X ⊕ Y → X ⊕ Y → ℝ`

`X` and `Y` are the two metric spaces being glued; `Z` is the parameter type that indexes the identified pairs. `Φ` is the embedding of `Z` into `X`, specifying which points of `X` are to be identified. `Ψ` is the embedding of `Z` into `Y`, specifying the corresponding points of `Y`. `ε` is the real number that becomes the declared distance between each glued pair `(Φ p, Ψ p)`. The final two arguments are the two points of `X ⊕ Y` whose predistance is being computed.

## Conventions

There is no junk-value convention to declare: the function is defined on all inputs without restriction, and every case (both summands the same, or opposite summands) yields a well-defined real number for any choice of `Φ`, `Ψ`, and `ε`.

## Worked examples

- Claim: For any `x y : X`, `VTask.glueDist Φ Ψ ε (.inl x) (.inl y) = dist x y` (the predistance of two left-summand points is their original metric distance, regardless of `Φ`, `Ψ`, and `ε`).

- Claim: For any `x y : Y`, `VTask.glueDist Φ Ψ ε (.inr x) (.inr y) = dist x y` (the predistance of two right-summand points is their original metric distance).

- Claim: When `Z` is a singleton with `p : Z`, `Φ p = x₀ ∈ X`, and `Ψ p = y₀ ∈ Y`, we have `VTask.glueDist Φ Ψ ε (.inl x₀) (.inr y₀) = ε`, because the infimum `⨅ p, dist x₀ (Φ p) + dist y₀ (Ψ p)` evaluates to `0 + 0 = 0`, giving `0 + ε = ε`. (This is exactly `glueDist_glued_points`.)

- Claim: For any `x : X` and `y : Y`, `VTask.glueDist Φ Ψ ε (.inl x) (.inr y) = VTask.glueDist Φ Ψ ε (.inr y) (.inl x)` (the function is symmetric across summands).

## Boundaries

- **`Z` empty**: When `Z` is empty, the infimum `⨅ p, dist x (Φ p) + dist y (Ψ p)` ranges over an empty index set; in Mathlib this conventionally evaluates to `⊤` (i.e., `+∞` for a bounded infimum in `ℝ`, but formally `0` if no instances exist). In practice, `glueDist` is primarily used when `Z` is nonempty.
- **`ε ≤ 0`**: The function is total and still computes for any real `ε`. However, key metric properties (such as `glueDist_eq_zero` implying equality) require `ε > 0`. With `ε ≤ 0` the result may fail to be a genuine metric.
- **Symmetry**: `VTask.glueDist Φ Ψ ε x y = VTask.glueDist Φ Ψ ε y x` holds unconditionally (for all four combinations of `inl`/`inr`).
- **Self-distance**: `VTask.glueDist Φ Ψ ε x x = 0` for all `x : X ⊕ Y`.
- **Lower bound**: For any `x : X` and `y : Y`, `ε ≤ VTask.glueDist Φ Ψ ε (.inl x) (.inr y)`, since the infimum of non-negative sums is non-negative.

## Not to be confused with

- `Metric.Sum.dist` — the standard metric on `X ⊕ Y` (disjoint union) in Mathlib, which is a special case of `VTask.glueDist` with `Z = Unit`, `ε = 1`, and both maps constant.
- `Metric.glueSpaceDist` or the gluing of metric spaces along isometric embeddings — a higher-level construction that uses `glueDist` internally but works with isometries and produces a genuine metric space quotient.
- `EMetric.glueDist` — any extended-metric (ℝ≥0∞-valued) analogue; the present function is strictly real-valued and does not take values in `ℝ≥0∞`.
