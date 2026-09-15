## VTask.induce

### Object

Given a graph `G` (with vertex type `α` and edge type `β`) and a set `X` of vertices, `VTask.induce G X` is the **induced subgraph** of `G` on `X`: the graph whose vertex set is exactly `X`, and whose edges are precisely those edges of `G` whose both endpoints lie in `X`. No edge is added or removed except by the membership of its endpoints in `X`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.induce : {α : Type u_1} -> {β : Type u_2} -> (G : Graph α β) -> (X : Set α) -> Graph α β
<!-- PINNED-SIGNATURE:END -->


The first argument `G` is the ambient graph from which the induced subgraph is carved out. The second argument `X` is the set of vertices that define the induced subgraph; it need not be a subset of `V(G)`, though the interesting case is when it is.

### Conventions

The set `X` is used as-is as the vertex set of the result, even if `X` contains vertices that are not in `V(G)`. In that case the excess vertices in `X \ V(G)` are isolated (no edge of `G` can have an endpoint outside `V(G)`), and the induced subgraph is a subgraph of `G` only when `X ⊆ V(G)`.

### Worked examples

- Claim: For any graph `G`, inducing on the full vertex set `V(G)` recovers `G` itself, i.e., `G.induce V(G) = G`.

- Claim: The edge set of `G.induce X` consists exactly of those edges `e` of `G` for which both endpoints of `e` belong to `X`, i.e., `E(G.induce X) = {e | ∃ x y, G.IsLink e x y ∧ x ∈ X ∧ y ∈ X}`.

- Claim: If `X ⊆ V(G)`, then `G.induce X ≤ G` (the induced subgraph is a subgraph of `G` in the ordering on graphs).

- Claim: If `X` is disjoint from `V(G)`, then `G.induce X` has vertex set `X` and no edges at all.

### Boundaries

- **Empty set:** `G.induce ∅` has no vertices and no edges; it is the empty graph on `α` and `β`.
- **Full vertex set:** `G.induce V(G) = G` — inducing on all vertices is the identity.
- **Overshoot (X ⊄ V(G)):** The definition still produces a well-formed graph, but the induced subgraph is not necessarily a subgraph of `G` in the graph-order sense; `G.induce X ≤ G` holds if and only if `X ⊆ V(G)`.
- **Singleton set:** `G.induce {v}` has a single vertex `v` and no edges (since every edge needs two endpoints, and in a simple-enough setting both would need to be `v`, which is excluded by the link axioms).

### Not to be confused with

- **Graph deletion `G.deleteVertices S`**: removes a set `S` of vertices and their incident edges, whereas `VTask.induce G X` *keeps* exactly the vertices in `X`. The two are complementary: `G.induce X` corresponds to `G.deleteVertices (V(G) \ X)` when `X ⊆ V(G)`.
- **Spanning subgraph**: a spanning subgraph keeps all vertices of `G` but may remove edges; `VTask.induce G X` typically changes the vertex set.
- **Graph.Subgraph.induce**: a related construction in the `Subgraph` API that induces within a fixed subgraph structure, returning a `Subgraph` object rather than a `Graph`.
