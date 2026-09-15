## Object

The **line graph** of a simple graph $G$ is the simple graph whose vertex set is the edge set of $G$, and in which two vertices (i.e., two edges of $G$) are adjacent if and only if they are distinct and share at least one common endpoint in $G$.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lineGraph : {V : Type u_1} -> (G : SimpleGraph V) -> SimpleGraph ↑G.edgeSet
<!-- PINNED-SIGNATURE:END -->


`VTask.lineGraph : {V : Type u_1} -> (G : SimpleGraph V) -> SimpleGraph ↑G.edgeSet`

The implicit argument `V` is the vertex type of the original graph. The explicit argument `G` is the simple graph whose line graph is being constructed. The result is a `SimpleGraph` whose vertex type is the subtype `↑G.edgeSet`, i.e., elements of the edge set of `G` (each edge being an element of `Sym2 V` that belongs to `G`).

## Conventions

No special junk-value conventions are declared: the construction is total and well-defined for any simple graph `G`, including the empty graph (which yields an edgeless line graph on an empty vertex set) and graphs with isolated vertices (which contribute no vertices to the line graph).

## Worked examples

- Claim: For the complete graph on three vertices `K₃`, two edges sharing a vertex are adjacent in its line graph.

- Claim: Two edges `e₁` and `e₂` of `G` are adjacent in `VTask.lineGraph G` if and only if they are distinct and there exists a vertex `v` belonging to both `e₁` and `e₂` (viewed as elements of `Sym2 V`).

- Claim: If `G ⊑ G'` (i.e., `G` is contained as a subgraph in `G'`), then `VTask.lineGraph G ⊑ VTask.lineGraph G'`.

- Claim: For a graph `G` with no edges, `VTask.lineGraph G` has an empty vertex set and no adjacencies.

## Boundaries

- **Empty graph**: If `G` has no edges, then `G.edgeSet` is empty, and `VTask.lineGraph G` is a simple graph on an empty type — it has no vertices and no adjacencies.
- **Single-edge graph**: If `G` has exactly one edge, then `VTask.lineGraph G` has exactly one vertex and no adjacencies (a single vertex cannot be adjacent to itself, since the graph is simple and the definition requires the two edge-vertices to be distinct).
- **Star graph**: In the star graph $K_{1,n}$, all $n$ edges share the central vertex, so every pair of edges is adjacent in the line graph — giving a complete graph $K_n$ as the line graph.
- **Path graph**: In a path $P_n$, consecutive edges share an endpoint, while non-consecutive edges do not, so the line graph of $P_n$ is again a path $P_{n-1}$.
- **Self-loops**: Because `G` is a `SimpleGraph`, it has no self-loops, so the irreflexivity of adjacency in the line graph is automatically consistent with the `SimpleGraph` structure.

## Not to be confused with

- **`SimpleGraph.edgeSet`**: The bare edge set of `G` as a `Set (Sym2 V)`, which is merely the vertex type of `VTask.lineGraph G`, not itself a graph.
- **`SimpleGraph.incidenceSet`**: The set of edges incident to a particular vertex of `G`; this describes a local neighbourhood in `G`, not the global line graph construction.
- **Subdivision graph**: Another derived graph construction where edges are replaced by paths; distinct from the line graph, which replaces edges by vertices and encodes shared endpoints as adjacency.