## VTask.between

### Object

`VTask.between s t G` is the subgraph of the simple graph `G` on vertex type `V` that retains exactly those edges of `G` whose two endpoints lie on *opposite sides* of the bipartition `(s, t)` — that is, one endpoint in `s` and the other in `t`. Edges both of whose endpoints lie inside `s`, both inside `t`, or neither in `s` nor in `t` are discarded. The result is itself a simple graph on the same vertex type `V`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.between : {V : Type u_1} -> (s t : Set V) -> (G : SimpleGraph V) -> SimpleGraph V
<!-- PINNED-SIGNATURE:END -->


```
VTask.between : {V : Type u_1} -> (s t : Set V) -> (G : SimpleGraph V) -> SimpleGraph V
```

The implicit argument `V` is the shared vertex type. The first explicit argument `s` is one of the two vertex sets forming the bipartition; the second explicit argument `t` is the other vertex set. The third argument `G` is the ambient simple graph whose edges are being filtered.

### Conventions

The sets `s` and `t` need not be disjoint; when a vertex belongs to both, an edge touching it may qualify through either membership. No junk-value convention is imposed on non-disjoint inputs: the adjacency predicate is well-defined for any `s` and `t`.

### Worked examples

- Claim: `VTask.between s t G` is a subgraph of `G`, i.e., `VTask.between s t G ≤ G` for any `s`, `t`, and `G`.

- Claim: The construction is symmetric in `s` and `t`: `VTask.between s t G = VTask.between t s G` for any `s`, `t`, and `G`.

- Claim: If `s` and `t` are disjoint sets of vertices, then `VTask.between s t G` is a bipartite graph (with bipartition `s` and `t`).

- Claim: A pair `(v, w)` is adjacent in `VTask.between s t G` if and only if `G.Adj v w` holds and either (`v ∈ s` and `w ∈ t`) or (`v ∈ t` and `w ∈ s`).

### Boundaries

- **Empty sets**: If `s = ∅` or `t = ∅`, no edge can straddle the bipartition, so `VTask.between s t G` is the edgeless graph on `V` (all adjacencies are `False`).
- **`s = t = V`**: Every edge of `G` satisfies the crossing condition (both endpoints are trivially in `s` and in `t`), so `VTask.between V V G = G`.
- **Non-disjoint `s` and `t`**: The result is still a well-formed simple graph, but it may fail to be bipartite because a vertex in `s ∩ t` can be adjacent to vertices in both `s` and `t`; the bipartiteness theorem requires `Disjoint s t`.
- **`s` and `t` partition `V` (i.e., `t = sᶜ`)**: This is the most natural use case, producing a bipartite spanning subgraph that retains exactly the cut edges between `s` and its complement.

### Not to be confused with

- `SimpleGraph.induce` (or `SimpleGraph.comap`): the induced subgraph on a single set of vertices, which retains all edges *within* that set rather than edges *crossing* between two sets.
- `SimpleGraph.IsBipartiteWith`: a predicate asserting that a graph already has a bipartite structure with a given bipartition; `VTask.between` *constructs* a graph from an ambient one, while `IsBipartiteWith` merely *checks* a property.
- The cut set (edge boundary) of `s`: a set of edges rather than a graph, and often defined for a partition `(s, sᶜ)` only; `VTask.between` packages the same crossing edges as a full `SimpleGraph` value.