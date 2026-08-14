## VTask.sum

### Object

The *disjoint sum* (also called disjoint union) of two simple graphs $G$ on vertex set $V$ and $H$ on vertex set $W$ is the simple graph whose vertex set is the disjoint union $V \sqcup W$ (the type-theoretic sum $V \oplus W$) and whose edges are exactly the edges of $G$ (between left-tagged vertices) and the edges of $H$ (between right-tagged vertices). No edge connects a left-tagged vertex to a right-tagged vertex. The two original graphs sit inside the sum as induced subgraphs on complementary parts, with no edges between the parts.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sum : {V : Type u_3} -> {W : Type u_5} -> (G : SimpleGraph V) -> (H : SimpleGraph W) -> SimpleGraph (V ⊕ W)
<!-- PINNED-SIGNATURE:END -->


`VTask.sum : {V : Type u_3} -> {W : Type u_5} -> (G : SimpleGraph V) -> (H : SimpleGraph W) -> SimpleGraph (V ⊕ W)`

The implicit arguments `V` and `W` are the vertex types of the two constituent graphs. The first explicit argument `G` is the simple graph on `V` that will occupy the left summand. The second explicit argument `H` is the simple graph on `W` that will occupy the right summand. The result is a simple graph whose vertex type is `V ⊕ W`, the type-theoretic disjoint union.

### Conventions

No junk-value or boundary conventions are declared for this definition: the construction is defined for all simple graphs and all vertex types without restriction, and every vertex-pair case is handled cleanly by the Sum.inl / Sum.inr casework.

### Worked Examples

- Claim: Two left-injected vertices are adjacent in `VTask.sum G H` if and only if they are adjacent in `G`.

- Claim: Two right-injected vertices are adjacent in `VTask.sum G H` if and only if they are adjacent in `H`.

- Claim: A left-injected vertex and a right-injected vertex are never adjacent in `VTask.sum G H`, regardless of the graphs.

- Claim: If `G` is `n`-colorable and `H` is `m`-colorable, then `VTask.sum G H` is `max n m`-colorable.

- Claim: If `G` and `H` are both connected, then adding a single edge between a left vertex and a right vertex to `VTask.sum G H` yields a connected graph.

### Boundaries

- When both `G` and `H` are the empty graph (no edges), `VTask.sum G H` is also the empty graph on `V ⊕ W`.
- When `G` is the complete graph on a single vertex and `H` is the complete graph on a single vertex, `VTask.sum G H` is the empty graph on a two-element type (since each graph has no self-loops, and the only cross-pair gets no edge).
- The disjoint sum is NOT connected in general: the left and right summands form two disconnected components unless an external edge is added.
- The chromatic number of the sum equals the maximum of the chromatic numbers of `G` and `H`, since the two parts can be colored independently using the same color palette.
- The sum is symmetric up to isomorphism: `VTask.sum G H` is isomorphic to `VTask.sum H G` via the canonical swap `V ⊕ W ≅ W ⊕ V`.

### Not to be confused with

- `SimpleGraph.sup G H` (lattice join): this requires both graphs to live on the **same** vertex type and produces a graph on that same type; `VTask.sum` combines graphs on **different** vertex types into a graph on their disjoint union.
- `SimpleGraph.disjointUnion` or categorical coproduct constructions in other formalizations: the present definition is specifically the type-theoretic `⊕` disjoint union, with no identification of vertices.
- The *join* of two graphs (sometimes written $G + H$ in combinatorics): unlike the disjoint sum, the join also adds all edges between the two parts, making it connected.