## VTask.transfer

### Object

Given a walk `p` in a simple graph `G` from vertex `u` to vertex `v`, and a second simple graph `H` on the same vertex type, `VTask.transfer p H h` produces the "same" walk reinterpreted as a walk in `H`. The walk visits exactly the same sequence of vertices and uses exactly the same sequence of edges — only the ambient graph changes from `G` to `H`. The proof obligation `h` witnesses that every edge appearing in `p` is also an edge of `H`, making the reinterpretation valid.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.transfer : {V : Type u} -> {G : SimpleGraph V} -> {u v : V} -> (p : G.Walk u v) -> (H : SimpleGraph V) -> (h : ∀ e ∈ p.edges, e ∈ H.edgeSet) -> H.Walk u v
<!-- PINNED-SIGNATURE:END -->


`VTask.transfer : {V : Type u} -> {G : SimpleGraph V} -> {u v : V} -> (p : G.Walk u v) -> (H : SimpleGraph V) -> (h : ∀ e ∈ p.edges, e ∈ H.edgeSet) -> H.Walk u v`

The implicit type `V` is the common vertex type shared by both graphs. The implicit graph `G` is the source graph in which `p` originally lives. The implicit vertices `u` and `v` are the start and end points of the walk. The argument `p` is the walk in `G` to be transferred. The argument `H` is the target simple graph, also on vertex type `V`, into which the walk will be reinterpreted. The argument `h` is a proof that every edge in the edge list of `p` belongs to the edge set of `H`, ensuring that each step of `p` is a valid adjacency in `H`.

### Conventions

There are no special junk-value or boundary conventions beyond the standard behavior: when `p` is the empty (nil) walk, the result is the nil walk in `H`; the function is total and well-defined on all valid inputs.

### Worked examples

- Claim: Transferring a nil walk from any graph `G` to any graph `H` (with trivially satisfied edge condition) yields the nil walk in `H`, and in particular has length 0.

- Claim: The edge list of the transferred walk equals the edge list of the original walk — that is, `(p.transfer H h).edges = p.edges` for any valid `p`, `H`, and `h`.

- Claim: The support (sequence of visited vertices) of the transferred walk equals the support of the original walk — that is, `(p.transfer H h).support = p.support`.

- Claim: If a walk `p` in `G` is a path (no repeated vertices), then `p.transfer H h` is also a path in `H`.

- Claim: Transferring `p` back to `G` itself (using the canonical proof that `p`'s edges lie in `G`) returns a walk definitionally equal to `p` — that is, `p.transfer G p.edges_subset_edgeSet = p`.

### Boundaries

- **Nil walk**: When `p` is the nil walk at a vertex `u`, the transfer is the nil walk at `u` in `H`. The hypothesis `h` is vacuously satisfied since the nil walk has no edges.
- **Single-step walk**: For a walk consisting of one edge `(u, v)`, the hypothesis `h` must supply proof that the single symmetric pair `s(u, v)` belongs to `H.edgeSet`; the result is the one-step walk in `H`.
- **Same graph**: Transferring `p` to its own graph `G` is the identity on walks.
- **Subgraph containment**: If `G ≤ H` (as simple graphs, meaning every edge of `G` is an edge of `H`), then the hypothesis `h` can always be satisfied, and the transfer coincides with the canonical map induced by the subgraph inclusion.
- **Composition**: Transferring a walk that was already transferred is equivalent to transferring the original walk directly to the final target, and the edges of the twice-transferred walk equal those of the original.

### Not to be confused with

- `SimpleGraph.Walk.map`: Maps a walk along a graph homomorphism, potentially changing both the vertex type and the graph; `VTask.transfer` keeps the vertex type and vertex sequence fixed, only changing the ambient graph.
- `SimpleGraph.Subgraph.spanningCoe`: Reinterprets a subgraph as a spanning subgraph, operating at the graph level rather than the walk level.
- `SimpleGraph.Walk.toSubgraph`: Converts a walk into the subgraph whose edges are exactly those of the walk, which is a different direction of the same intuition.