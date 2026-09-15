## VTask.VanishingDiam

### Object

Given a *scheme* — a function assigning to each finite sequence of symbols a subset of a metric space — `VTask.VanishingDiam A` is the proposition that the scheme has **vanishing diameter**: for every infinite branch (an infinite sequence of symbols), the extended diameter of the sets produced by truncating that branch to its first `n` terms tends to zero as `n → ∞`. Intuitively, as one travels deeper along any branch of the scheme tree, the associated sets shrink to arbitrarily small size.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.VanishingDiam : {β : Type u_1} -> {α : Type u_2} -> (A : List β → Set α) -> [PseudoMetricSpace α] -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.VanishingDiam : {β : Type u_1} -> {α : Type u_2} -> (A : List β → Set α) -> [PseudoMetricSpace α] -> Prop`

The implicit type `β` is the **alphabet** (or branching type): finite sequences of `β` serve as addresses in the scheme tree. The implicit type `α` is the **ambient space**, which must carry a pseudo-metric structure (provided by the instance argument). The explicit argument `A` is the **scheme itself**: a function from finite lists of `β` to subsets of `α`. The pseudo-metric space instance supplies the notion of diameter used in the condition.

### Conventions

There are no declared junk-value or edge conventions for this definition: the proposition is stated uniformly for all infinite branches and all finite prefixes, so no special case is designated a fallback or default output.

### Worked examples

- Claim: For the constant scheme `A l = Set.univ` on a nontrivial pseudo-metric space with infinite diameter, `VTask.VanishingDiam A` fails because the diameters are always infinite and do not tend to 0.

- Claim: For a scheme on `ℝ` defined by `A l = Set.Icc 0 (2 : ℝ) ^ (-(List.length l : ℝ))` (a closed interval whose radius shrinks geometrically with depth), `VTask.VanishingDiam A` holds, since the extended diameter of `A l` is `2^(-n)` when `l` has length `n`, and `2^(-n) → 0`.

- Claim: The trivial scheme `A l = ∅` satisfies `VTask.VanishingDiam A`, since the extended diameter of the empty set is `0` for every finite prefix, and the constant sequence `0` trivially converges to `0`.

### Boundaries

- **Empty sets along branches**: If `A (res x n)` is empty for all sufficiently large `n` along some branch `x`, the diameter is `0` from that point onward, which is consistent with (in fact, ensures) convergence to `0`.
- **n = 0 prefix**: At depth `0`, the prefix `res x 0` is the empty list, so `A []` is the set assigned to the root of the scheme. Its diameter may be large or even infinite without violating `VanishingDiam`, as long as the diameters converge to `0` as `n → ∞`.
- **Non-decreasing sets**: If a scheme happens to produce sets that are not nested or that grow along some branch, `VanishingDiam` can still hold provided the diameters still tend to zero; the condition is purely metric, not topological or set-theoretic.
- **Pseudo-metric vs. metric**: The extended diameter is used (`Metric.ediam`, taking values in `ℝ≥0∞`), so the condition is well-posed even when sets have infinite diameter; those branches simply do not satisfy convergence to `0` unless diameters eventually become finite and small.

### Not to be confused with

- **`Metric.diam` convergence**: `VanishingDiam` uses *extended* diameter (`ediam`, valued in `ℝ≥0∞`) rather than the real-valued `diam`; sets of infinite diameter contribute `⊤` rather than `0`, so the conditions differ on unbounded sets.
- **Vanishing intersection / singleton intersection**: A scheme may have vanishing diameter without having nonempty or singleton intersections along branches; `VanishingDiam` says nothing directly about whether `⋂ n, A (res x n)` is empty, a singleton, or larger.
- **Closedness or completeness conditions on the scheme**: Other scheme properties (e.g., that sets are closed, or that the space is complete) are separate hypotheses often combined with `VanishingDiam` to conclude that branches have a unique limit point.
