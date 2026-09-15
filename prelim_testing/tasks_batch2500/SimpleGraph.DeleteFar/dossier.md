## VTask.DeleteFar

### Object

A simple graph `G` is said to be **`r`-delete-far** from a graph property `p` if one must delete at least `r` edges from `G` in order to obtain a graph satisfying `p`. In other words, no matter which set of fewer than `r` edges you remove from `G`, the resulting graph fails to have property `p`. This notion formalizes how "robust" the violation of `p` is in `G`: a large value of `r` means `G` is deeply far from satisfying `p`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.DeleteFar : {V : Type u_1} -> (G : SimpleGraph V) -> {𝕜 : Type u_2} -> [Ring 𝕜] -> [PartialOrder 𝕜] -> [Fintype ↑G.edgeSet] -> (p : SimpleGraph V → Prop) -> (r : 𝕜) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.DeleteFar : {V : Type u_1} -> (G : SimpleGraph V) -> {𝕜 : Type u_2} -> [Ring 𝕜] -> [PartialOrder 𝕜] -> [Fintype ↑G.edgeSet] -> (p : SimpleGraph V → Prop) -> (r : 𝕜) -> Prop`

`V` is the vertex type of the graph. `G` is the simple graph under consideration. `𝕜` is the ordered ring in which the threshold `r` lives (typically `ℕ`, `ℤ`, or `ℝ`). The `Ring` and `PartialOrder` instances give `𝕜` its algebraic and comparison structure. The `Fintype` instance asserts that the edge set of `G` is finite, which is needed to count edges. `p` is the graph property (a predicate on simple graphs over `V`) that `G` is far from. `r` is the threshold: `G` must be `r`-delete-far, meaning at least `r` edge deletions are required to reach a graph satisfying `p`.

### Conventions

When `r ≤ 0` (or `r = 0` for natural-number-valued thresholds), the condition `VTask.DeleteFar G p r` is vacuously satisfied whenever `p` can be achieved by deleting any edges at all, since the size of any edge set is nonnegative — there are no genuinely junk values declared for this definition.

### Worked examples

- Claim: If `G.DeleteFar p r₂` holds and `r₁ ≤ r₂`, then `G.DeleteFar p r₁` holds (monotonicity: being `r₂`-delete-far implies being `r₁`-delete-far for any smaller threshold `r₁`).

- Claim: If `G.DeleteFar p r` and the empty graph `⊥` satisfies `p`, then `r` is at most the total number of edges of `G` (since deleting all edges yields `⊥`, the entire edge set witnesses the deletion cost, which is `#G.edgeFinset`).

- Claim: `G.DeleteFar p r` is equivalent to saying that for every subgraph `H ≤ G` (with decidable adjacency), if `p H` then `r ≤ #G.edgeFinset - #H.edgeFinset`; that is, the number of edges that must be removed from `G` to reach `H` is at least `r`.

### Boundaries

- When `r = 0`, the definition asserts that for every subset `s` of edges, if deleting `s` yields a graph with property `p`, then `0 ≤ #s`. This is always true (edge counts are nonneg), so `G.DeleteFar p 0` holds whenever `p` is achievable at all by edge deletion — the condition is trivially satisfied at threshold zero.
- When `G` has no edges (i.e., `G = ⊥`), the only subset of its edge set is the empty set, and deleting it leaves `⊥`. So `G.DeleteFar p r` holds iff either `¬ p ⊥` (no deletion achieves `p`) or `r ≤ 0`.
- When `p` is the property of being the empty graph `⊥`, the definition says that to reduce `G` to the empty graph, one must delete all edges, so `G.DeleteFar (· = ⊥) r` holds iff `r ≤ #G.edgeFinset`.
- If `p` holds of `G` itself (so the empty deletion suffices), then `G.DeleteFar p r` forces `r ≤ 0`, since the empty deletion set has cardinality `0`.

### Not to be confused with

- **`SimpleGraph.deleteEdges`**: the operation of removing a specific set of edges from a graph; `DeleteFar` is a property about how many edges must be deleted, not the act of deletion itself.
- **`SimpleGraph.FarFromTriangleFree`** (or analogous named instances): these are specific instantiations of `DeleteFar` for concrete properties like triangle-freeness; `DeleteFar` is the general parameterized version.
- **Edge connectivity or robustness**: edge connectivity counts the minimum edges whose removal disconnects the graph; `DeleteFar` counts the minimum edges to remove to achieve an arbitrary property `p`, which need not be connectivity-related.
