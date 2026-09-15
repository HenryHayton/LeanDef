## VTask.IsVertexCover

### Object

A *vertex cover* of a simple graph is a set of vertices such that every edge of the graph has at least one of its two endpoints belonging to that set. Equivalently, no edge is entirely contained in the complement of the set. This is a classical combinatorial notion: a vertex cover "covers" all edges by touching each one at a vertex.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsVertexCover : {V : Type u_1} -> (G : SimpleGraph V) -> (c : Set V) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsVertexCover : {V : Type u_1} -> (G : SimpleGraph V) -> (c : Set V) -> Prop`

The vertex type `V` is implicit and inferred from context. The first explicit argument `G` is the simple graph whose edges are to be covered. The second explicit argument `c` is the candidate set of vertices being tested as a cover.

### Conventions

The empty set is a vertex cover of a graph if and only if that graph has no edges (is the bottom/edgeless graph); there is no convention assigning a junk truth value to `IsVertexCover G ∅` when `G` is non-empty — it simply evaluates to `False` in that case. The full vertex set `Set.univ` is always a vertex cover of any graph, as every edge must be incident to some vertex. For the edgeless graph `⊥`, every set of vertices is trivially a vertex cover.

### Worked examples

- Claim: For any simple graph `G` on vertex type `V`, the full set `Set.univ` is a vertex cover of `G`.

- Claim: For the edgeless graph `(⊥ : SimpleGraph V)`, any set `c : Set V` satisfies `VTask.IsVertexCover ⊥ c`.

- Claim: If `c` is a vertex cover of `G` and `c ⊆ d`, then `d` is also a vertex cover of `G` (covers are closed under taking supersets).

- Claim: A set `c` is a vertex cover of `G` if and only if its complement is an independent set of `G` (no two adjacent vertices both lie outside `c`).

### Boundaries

- **Empty cover**: `VTask.IsVertexCover G ∅` holds exactly when `G` has no edges. For any graph with at least one edge `{v, w}`, neither `v` nor `w` is in `∅`, so the condition fails.
- **Full cover**: `VTask.IsVertexCover G Set.univ` is always true, since every vertex belongs to `Set.univ`.
- **Edgeless graph**: `VTask.IsVertexCover ⊥ c` holds for every set `c`, as the universal quantifier over edges ranges over an empty collection.
- **Monotonicity in the graph**: If `G ≤ G'` (i.e., `G` has a subset of `G'`'s edges) and `c` covers `G'`, then `c` also covers `G`. In particular, a vertex cover of a larger graph is a vertex cover of any subgraph.
- **Monotonicity in the cover**: If `c` covers `G` and `c ⊆ d`, then `d` covers `G`.
- **Graph isomorphisms**: Vertex covers are preserved and reflected by graph isomorphisms, and pulled back along graph homomorphisms.

### Not to be confused with

- **`SimpleGraph.IsIndepSet`**: An independent set is a set with *no* two adjacent vertices; a vertex cover is the complementary notion — its complement is an independent set.
- **`SimpleGraph.vertexCoverNum`**: This is the minimum cardinality (as an extended natural number) of a vertex cover of `G`, not the predicate asserting that a given set is a cover.
- **Edge cover**: An edge cover is a set of *edges* touching every *vertex*, which is a dual notion and is not the same as a vertex cover.