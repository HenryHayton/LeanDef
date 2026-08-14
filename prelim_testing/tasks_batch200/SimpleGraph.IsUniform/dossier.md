## 1. Object

A pair of finite vertex sets `s` and `t` in a simple graph `G` is called **ε-uniform** (equivalently, **ε-regular** in the sense of Szemerédi) with parameter `ε` in an ordered field `𝕜` if the following holds: for every pair of subsets `s' ⊆ s` and `t' ⊆ t` whose sizes are at least an `ε`-fraction of `|s|` and `|t|` respectively, the edge density between `s'` and `t'` differs from the global edge density between `s` and `t` by less than `ε`. Intuitively, the edges between `s` and `t` are distributed as uniformly as in a random bipartite graph: no large enough sub-pair witnesses a significantly different density.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsUniform : {α : Type u_1} -> {𝕜 : Type u_2} -> [Field 𝕜] -> [LinearOrder 𝕜] -> (G : SimpleGraph α) -> [DecidableRel G.Adj] -> (ε : 𝕜) -> (s t : Finset α) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.IsUniform : {α : Type u_1} -> {𝕜 : Type u_2} -> [Field 𝕜] -> [LinearOrder 𝕜] -> (G : SimpleGraph α) -> [DecidableRel G.Adj] -> (ε : 𝕜) -> (s t : Finset α) -> Prop
```

`α` is the type of graph vertices. `𝕜` is the ordered field in which densities and the uniformity parameter are measured (typically `ℚ` or `ℝ`). `G` is the simple graph under consideration. `ε` is the uniformity parameter: smaller values demand a stricter (more uniform) distribution of edges. `s` and `t` are the two finite sets of vertices whose inter-pair edge distribution is being tested. The result is a proposition stating that `s` and `t` form an `ε`-uniform pair in `G`.

## 3. Conventions

No junk-value or boundary conventions are formally declared for this definition. The definition is a universally quantified proposition, and when `ε ≤ 0` it is vacuously true (no subset can satisfy the size threshold `|s| * ε ≤ |s'|` with `|s'|` a non-negative natural number cast to `𝕜` when `ε ≤ 0` combined with any non-trivial `s`). Conversely, any proof of `VTask.IsUniform G ε s t` for a non-trivial pair implies `0 < ε`.

## 4. Worked Examples

- Claim: If `G` is the empty graph on a vertex type `α`, `s` and `t` are disjoint finsets, and `ε = 1`, then `VTask.IsUniform G 1 s t` holds because the edge density between any subsets is 0, so the absolute difference is 0 < 1.

- Claim: If `G.IsUniform ε s t` holds, then `0 < ε`. That is, a non-vacuous uniformity condition forces `ε` to be positive.

- Claim: For `ε₁ ≤ ε₂`, if `G.IsUniform ε₁ s t` then `G.IsUniform ε₂ s t`, since a larger `ε₂` both loosens the size threshold on subsets and relaxes the density-difference bound.

- Claim: `¬ G.IsUniform ε s t` if and only if there exist subsets `s' ⊆ s` and `t' ⊆ t` with `|s| * ε ≤ |s'|`, `|t| * ε ≤ |t'|`, and `|edgeDensity(s', t') − edgeDensity(s, t)| ≥ ε`.

## 5. Boundaries

- When `ε ≤ 0`: The size-threshold conditions `|s| * ε ≤ |s'|` and `|t| * ε ≤ |t'|` are satisfied by every subset (since cardinalities cast to `𝕜` are non-negative), so the property is in principle non-vacuous for this reason; however `ε ≤ 0` combined with the strict inequality `|density difference| < ε` becomes impossible since absolute values are non-negative, making the proposition false unless there are no large enough subsets — in practice the definition is only meaningful and useful for `0 < ε < 1`.
- When `s` or `t` is empty: The only subset is the empty set, and edge density among empty sets is 0, so the absolute difference is 0. The condition `|s| * ε ≤ |s'|` with `|s| = 0` forces `0 ≤ 0` which holds, but `|s'| = 0` too, so density is trivially 0 and the gap is 0. The property holds for any positive `ε`.
- When `ε ≥ 1`: The property can still be stated, but since edge densities lie in `[0, 1]` the absolute difference is at most 1, so the requirement `< ε` may be easier to satisfy.

## 6. Not to be Confused With

- `Finpartition.IsUniform G ε`: uniformity of an entire equipartition of the vertex set (Szemerédi regularity), which aggregates pairwise `IsUniform` conditions over parts of a partition — not a single pair.
- `G.edgeDensity s t`: the raw numerical edge density of the pair, which is one of the inputs to the `IsUniform` condition, not the condition itself.
- `G.nonuniformWitness ε s t`: the explicit subset of `s` witnessing a failure of `ε`-uniformity when the pair is not uniform — this is a Finset, not a Prop.