## VTask.completeBipartiteGraph

### Object

The complete bipartite graph on two vertex types `V` and `W` is the simple graph whose vertex set is the disjoint union `V ⊕ W`, and in which two vertices are adjacent if and only if one vertex comes from the `V`-side (tagged `inl`) and the other comes from the `W`-side (tagged `inr`). In other words, every vertex on the left is connected to every vertex on the right, and there are no edges within either side. Every bipartite graph embeds as a subgraph of such a graph.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.completeBipartiteGraph : (V : Type u_1) -> (W : Type u_2) -> SimpleGraph (V ⊕ W)
<!-- PINNED-SIGNATURE:END -->


`(V : Type u_1) -> (W : Type u_2) -> SimpleGraph (V ⊕ W)`

The first argument `V` is the type whose elements form the left side of the bipartition. The second argument `W` is the type whose elements form the right side of the bipartition. The result is a `SimpleGraph` on the coproduct type `V ⊕ W`, with edges running precisely between the two sides.

### Conventions

There are no special junk-value or edge conventions for this definition: it is a total construction defined for any two types, including empty types, singleton types, and infinite types. When one or both sides are empty, the resulting graph simply has no edges.

### Worked examples

- Claim: In `VTask.completeBipartiteGraph Bool Bool`, the vertex `Sum.inl true` is adjacent to `Sum.inr false` (one is on the left, the other on the right).

- Claim: In `VTask.completeBipartiteGraph Bool Bool`, the vertex `Sum.inl true` is NOT adjacent to `Sum.inl false` (both are on the left side, so no edge exists).

- Claim: In `VTask.completeBipartiteGraph Bool Bool`, the vertex `Sum.inr true` is adjacent to `Sum.inl false` (right-to-left adjacency is symmetric with left-to-right).

- Claim: When `V` or `W` is the empty type `Empty`, `VTask.completeBipartiteGraph Empty Bool` has no edges, since there are no vertices on the left side.

- Claim: The chromatic number of `VTask.completeBipartiteGraph V W` is 2 when both `V` and `W` are nonempty, since the two-coloring given by the bipartition is optimal.

- Claim: The number of edges in `VTask.completeBipartiteGraph W₁ W₂` equals `ENat.card W₁ * ENat.card W₂`, reflecting the fact that every left vertex is connected to every right vertex.

### Boundaries

- If `V` is empty (`V = Empty`), no vertex of the form `Sum.inl v` exists, so there are no edges at all in `VTask.completeBipartiteGraph Empty W`.
- If `W` is empty, symmetrically, there are no edges in `VTask.completeBipartiteGraph V Empty`.
- If both `V` and `W` are empty, the graph has no vertices and no edges.
- The graph is always triangle-free: any three-vertex set must include at least two vertices from the same side, which are not adjacent.
- Adjacency is symmetric: `Sum.inl v` adjacent to `Sum.inr w` if and only if `Sum.inr w` adjacent to `Sum.inl v`.
- No vertex is adjacent to itself (the graph is a simple graph), since a vertex cannot simultaneously be `inl` and `inr`.

### Not to be confused with

- `SimpleGraph.completeGraph V`: the complete graph on a single vertex type `V`, where every distinct pair of vertices is adjacent — not bipartite unless `V` has at most one vertex.
- `SimpleGraph.bipartiteDoubleCover G`: a derived construction that is always a subgraph of `VTask.completeBipartiteGraph V V`, but is built from an existing graph `G` rather than from two separate types.
- A bipartite graph in general: any graph admitting a two-coloring is bipartite, but `VTask.completeBipartiteGraph V W` is specifically the *complete* bipartite graph, meaning it contains the maximum possible number of edges between its two sides.