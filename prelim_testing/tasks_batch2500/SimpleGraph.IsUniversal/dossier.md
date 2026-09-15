## VTask.IsUniversal

### Object

A vertex `v` in a simple graph `G` is called **universal** if it is adjacent to every other vertex in the graph. Equivalently, `v` is universal when its closed neighbourhood (excluding itself, since simple graphs have no self-loops) covers the entire vertex set.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsUniversal : {V : Type u} -> (G : SimpleGraph V) -> (v : V) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsUniversal : {V : Type u} -> (G : SimpleGraph V) -> (v : V) -> Prop`

The implicit type argument `V` is the vertex type of the graph. The first explicit argument `G` is the simple graph under consideration. The second explicit argument `v` is the vertex whose universality is being tested.

### Conventions

Because simple graphs are irreflexive (no vertex is adjacent to itself), the adjacency condition is stated only for vertices `w` distinct from `v`; the exclusion of `v = w` is not an extra restriction but the standard form of the predicate given the irreflexivity of simple-graph adjacency. When the vertex type `V` is a subsingleton (has at most one element), the condition is vacuously true: every vertex is universal, since there is no other vertex to be adjacent to.

### Worked examples

**Membership regime**

- Claim: In the complete graph `⊤` on any vertex type, every vertex is universal.

- Claim: In the complete graph `⊤` on two or more vertices, the universal vertex `v` is not isolated.

- Claim: A vertex that is universal in `G` cannot be isolated in `G` (when the vertex type is nontrivial, i.e., has at least two elements).

- Claim: The center vertex of a star graph is universal in that star graph.

**Global regime**

- Claim: In a finite graph, a vertex `v` is universal if and only if its degree equals `|V| - 1`.

- Claim: If `v` is universal in `G`, then `G` is connected.

- Claim: A vertex `v` is universal in `G` if and only if `v` is isolated in the complement graph `Gᶜ`.

- Claim: `G` equals the complete graph `⊤` if and only if every vertex of `G` is universal.

### Boundaries

- **Subsingleton vertex type**: When `V` has at most one element, the universal quantifier `∀ w, v ≠ w → G.Adj v w` is vacuously satisfied (there is no `w ≠ v`), so every vertex is universal regardless of what edges `G` contains (including the empty graph).
- **Two-vertex graph**: With exactly two vertices `v` and `w`, `v` is universal if and only if `G.Adj v w`, which is the single possible edge.
- **Empty graph (no edges)**: On a nontrivial vertex type, no vertex is universal in the empty graph, since universality requires adjacency to every other vertex.
- **Complete graph `⊤`**: Every vertex is universal in `⊤` by definition of the complete graph.
- **Isolated vertex**: An isolated vertex (adjacent to no other vertex) is never universal on a nontrivial vertex type; universality and isolation are mutually exclusive when `|V| ≥ 2`.
- **Complement duality**: `v` is universal in `G` if and only if `v` is isolated in `Gᶜ`, providing a clean duality between the two extremes.

### Not to be confused with

- **`SimpleGraph.IsIsolated`**: The opposite extreme — a vertex adjacent to *no* other vertex; universality and isolation are mutually exclusive for nontrivial graphs.
- **`SimpleGraph.IsDominating`**: A *set* of vertices such that every vertex outside the set has a neighbour inside it; universality is a single-vertex property, not a set property.
- **`SimpleGraph.IsConnected`**: A global property of the whole graph; a universal vertex *implies* connectivity, but connectivity does not imply the existence of a universal vertex.