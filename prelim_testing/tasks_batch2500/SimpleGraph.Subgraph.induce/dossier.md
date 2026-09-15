## VTask.induce

### Object

Given a subgraph `G'` of a simple graph `G` on vertex type `V`, and a set `s` of vertices of `G`, `VTask.induce G' s` is the subgraph of `G` whose vertex set is exactly `s` and whose edges are precisely those edges of `G'` whose both endpoints lie in `s`. In other words, it is the subgraph obtained by restricting `G'` to the vertices in `s` — keeping an edge if and only if both of its endpoints are in `s` and the edge already belongs to `G'`.

The typical intended use is when `s ⊆ G'.verts`, in which case this gives the standard graph-theoretic notion of an induced subgraph (of `G'`) on vertex set `s`. However, the definition is total: any set `s` may be supplied, and if `s` is not a subset of `G'.verts`, the result is still well-defined — vertices in `s` but not in `G'.verts` simply have no incident edges in the result.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.induce : {V : Type u} -> {G : SimpleGraph V} -> (G' : G.Subgraph) -> (s : Set V) -> G.Subgraph
<!-- PINNED-SIGNATURE:END -->


`VTask.induce : {V : Type u} -> {G : SimpleGraph V} -> (G' : G.Subgraph) -> (s : Set V) -> G.Subgraph`

The implicit argument `V` is the type of vertices of the ambient graph. The implicit argument `G` is the ambient simple graph. The explicit argument `G'` is the subgraph from which edges are to be induced — only edges already present in `G'` can appear in the result. The explicit argument `s` is the new vertex set of the induced subgraph; edges are kept precisely when both endpoints belong to `s`.

### Conventions

There are no junk-value conventions to declare: the definition is total in all its arguments and produces a well-defined subgraph for every choice of `G'` and `s`. In particular, if `s` is not contained in `G'.verts`, the result is still a valid subgraph (it simply has no edges involving vertices outside `G'.verts`, since `G'` itself has no such edges).

### Worked examples

- Claim: The vertex set of `VTask.induce G' s` is exactly `s`.

- Claim: An edge `{u, v}` belongs to `VTask.induce G' s` if and only if `u ∈ s`, `v ∈ s`, and `G'.Adj u v`.

- Claim: Inducing a subgraph on its own vertex set returns the subgraph unchanged: `VTask.induce G' G'.verts = G'`.

- Claim: If `G' ≤ G''` (as subgraphs), then `VTask.induce G' s ≤ VTask.induce G'' s` for any set `s`.

- Claim: Inducing on a union of sets is at least as large as the join of the two separate induced subgraphs: `VTask.induce G' s ⊔ VTask.induce G' s' ≤ VTask.induce G' (s ∪ s')`.

- Claim: For any simple graph `G` and set `s`, the induced subgraph `G.induce s` (as a simple graph on the subtype) corresponds, as a spanning coe, to the subgraph induced from the top subgraph `⊤` of `G` on `s`.

### Boundaries

- **`s` not contained in `G'.verts`:** The definition is still valid. Vertices in `s \ G'.verts` become isolated vertices in the result, since `G'` has no edges touching vertices outside `G'.verts`.
- **`s = ∅`:** The result is the empty subgraph (no vertices, no edges).
- **`s = G'.verts`:** The result equals `G'` itself (the theorem `induce_self_verts`).
- **`G' = ⊤` (the full subgraph of `G`):** Inducing the top subgraph on `s` yields the subgraph of `G` with vertex set `s` and all edges of `G` between vertices of `s`; this relates directly to `SimpleGraph.induce` on the simple-graph side.
- **`s` a superset of `G'.verts`:** Extra vertices in `s \ G'.verts` become isolated; no new edges are added beyond those of `G'`.
- **Monotonicity:** The induced subgraph is monotone in both arguments: larger `s` (under inclusion) yields a larger subgraph, and a larger `G'` (under the subgraph order) also yields a larger result.

### Not to be confused with

- `SimpleGraph.induce`: The operation on simple graphs (not subgraphs) that restricts a `SimpleGraph V` to a vertex-type subtype; `VTask.induce` works at the level of `Subgraph` objects and does not change the ambient vertex type.
- `SimpleGraph.Subgraph.restrict` or subgraph coercion: The `coe` of `VTask.induce G' s` is a simple graph on the subtype `s`, which is related to but distinct from `VTask.induce G' s` itself as a `G.Subgraph`.
- `SimpleGraph.Subgraph.spanningCoe`: The spanning coe of a subgraph retains all vertices of `G` but only the edges of the subgraph; this is different from restricting to `s` via `VTask.induce`.
