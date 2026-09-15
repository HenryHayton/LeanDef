## VTask.toSubgraph

### Object

Given a walk in a simple graph — a sequence of vertices connected step by step by edges — `VTask.toSubgraph` produces the **subgraph of G induced by that walk**: the subgraph whose vertex set is exactly the set of vertices appearing in the walk (the walk's support) and whose edge set is exactly the set of edges traversed by the walk. This is the smallest subgraph of G that contains every vertex visited and every edge used by the walk.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toSubgraph : {V : Type u} -> {G : SimpleGraph V} -> {u v : V} -> G.Walk u v → G.Subgraph
<!-- PINNED-SIGNATURE:END -->


`{V : Type u}` is the type of vertices. `{G : SimpleGraph V}` is the ambient simple graph in which the walk lives. `{u v : V}` are the start and end vertices of the walk. The final argument is the walk itself, a `G.Walk u v`, i.e., a path of edges in G leading from `u` to `v`.

### Conventions

For the trivial (nil) walk at a single vertex `u`, the resulting subgraph is the **singleton subgraph** containing only the vertex `u` and no edges. For a walk obtained by prepending an edge (`cons`), the resulting subgraph is the join (supremum in the subgraph lattice) of the single-edge subgraph for that edge and the subgraph of the rest of the walk.

### Worked examples

- Claim: For any walk `p : G.Walk u v`, both endpoints `u` and `v` are vertices of `VTask.toSubgraph p`.

- Claim: For any walk `p : G.Walk u v`, a vertex `w` belongs to `(VTask.toSubgraph p).verts` if and only if `w` appears in the support (vertex list) of `p`.

- Claim: For any walk `p : G.Walk u v`, the edge set of `VTask.toSubgraph p` equals the edge set of the walk `p` (the multiset/set of edges traversed, regarded as a set of unordered pairs).

- Claim: For walks `p : G.Walk u v` and `q : G.Walk v w`, `VTask.toSubgraph (p.append q) = VTask.toSubgraph p ⊔ VTask.toSubgraph q`.

- Claim: For any walk `p : G.Walk u v`, `VTask.toSubgraph p` is a connected subgraph.

- Claim: For any walk `p : G.Walk u v`, `VTask.toSubgraph p.reverse = VTask.toSubgraph p` (reversing a walk gives the same subgraph).

### Boundaries

- **Nil walk**: A nil walk at vertex `u` produces a subgraph with exactly one vertex (`u`) and no edges.
- **Single-step walk** (`cons h nil` for an adjacency `h : G.Adj u v`): The result is exactly `G.subgraphOfAdj h`, the minimal subgraph containing just the edge `{u, v}`.
- **Repeated vertices/edges**: If the walk revisits a vertex or traverses an edge more than once, the resulting subgraph still records each vertex and each edge only once (subgraphs are sets, not multisets). The vertex set is the support set and the edge set is the edge set of the walk.
- **Non-nil condition**: The equivalence `VTask.toSubgraph p ≤ G'` (for a subgraph `G'`) is equivalent to `p.edgeSet ⊆ G'.edgeSet` precisely when `p` is not nil; for nil walks, the only relevant condition is vertex membership.

### Not to be confused with

- `SimpleGraph.Walk.support`: the raw list of vertices visited by the walk, not a subgraph structure.
- `SimpleGraph.Walk.edgeSet`: the set of edges traversed, without the accompanying vertex-set and subgraph structure.
- `SimpleGraph.induce s`: the induced subgraph on a vertex set `s`, which keeps *all* edges of G between vertices of `s`, not just the edges actually traversed by some particular walk.