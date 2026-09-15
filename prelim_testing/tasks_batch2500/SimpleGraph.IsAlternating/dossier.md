## VTask.IsAlternating

### Object

Given two simple graphs `G` and `G'` on the same vertex type, `VTask.IsAlternating G G'` expresses that `G` is an *alternating graph with respect to `G'`*: along every pair of distinct edges of `G` incident to a common vertex, exactly one of those two edges belongs to `G'`. In other words, at every vertex the edges of `G` alternate between being in `G'` and not being in `G'`. This forces each vertex to have degree at most 2 in `G` (otherwise a consistent alternating assignment would be impossible), and the property is the key structural ingredient used to combine two matchings via symmetric difference to obtain a new perfect matching.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsAlternating : {V : Type u_1} -> (G G' : SimpleGraph V) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.IsAlternating : {V : Type u_1} -> (G G' : SimpleGraph V) -> Prop
```

The vertex type `V` is implicit and is inferred from the graphs. The first explicit argument `G` is the graph whose edges are being classified as alternating; it is the graph that must have the alternating edge pattern. The second explicit argument `G'` is the reference graph — membership or non-membership of `G'` alternates along edges of `G`.

### Conventions

No junk-value or default-output conventions are declared for this definition: it is a universally quantified `Prop` with no inputs outside its stated domain, so there are no boundary inputs requiring a conventional junk value.

### Worked examples

- Claim: If `G'` is a perfect matching and `G` is the symmetric difference of two perfect matchings `M` and `M'`, then `G.IsAlternating M.spanningCoe` holds.

- Claim: If `G.IsAlternating G'` and `G'' ≤ G`, then `G''.IsAlternating G'` holds (the property is monotone in the first argument under subgraph inclusion).

- Claim: The empty graph (with no edges) satisfies `IsAlternating G'` for any `G'`, because the universal quantifier over edges of the empty graph is vacuously true.

### Boundaries

- When `G` has no edges at all, `VTask.IsAlternating G G'` holds vacuously for any `G'`, since there are no pairs of distinct neighbors to constrain.
- When every vertex of `G` has degree at most 1 (e.g., `G` is itself a matching), `VTask.IsAlternating G G'` holds vacuously as well, because no vertex can have two distinct neighbors in `G`.
- The property is not symmetric in its two arguments: `G.IsAlternating G'` and `G'.IsAlternating G` are independent statements.
- If some vertex has degree 3 or more in `G`, it is impossible for `G.IsAlternating G'` to hold, because among three distinct edges at a vertex one cannot alternate between two truth values consistently.

### Not to be confused with

- `SimpleGraph.IsCycles`: a related property asserting that every connected component of a graph is a cycle; often used alongside `IsAlternating` in matching arguments but is a different structural condition.
- `SimpleGraph.Subgraph.IsAlternating` (lattice-level): the `symmDiff` for subgraphs derived from the lattice structure also affects which vertices are included; `VTask.IsAlternating` deliberately works at the `SimpleGraph` level to avoid this.
- An alternating *path* or *walk* with respect to a matching: that is a path-level notion where edges alternate between being in and outside a matching, whereas `VTask.IsAlternating` is a global graph-level property about every local pair of incident edges.