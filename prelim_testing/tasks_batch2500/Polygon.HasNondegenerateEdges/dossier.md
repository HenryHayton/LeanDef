## VTask.HasNondegenerateEdges

### Object

A predicate on a polygon asserting that every edge is **nondegenerate**: no two adjacent vertices of the polygon coincide. In other words, for every index `i`, the vertex at position `i` is distinct from the vertex at the next position in cyclic order. A polygon satisfying this condition has no collapsed (zero-length) edges.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.HasNondegenerateEdges : {P : Type u_3} -> {n : ℕ} -> (poly : Polygon P n) -> Prop
<!-- PINNED-SIGNATURE:END -->


The type parameter `P` is the type of points in which the polygon lives. The natural number `n` is the number of vertices (and edges) of the polygon. The argument `poly` is the polygon itself, viewed as a map from vertex indices to points.

### Conventions

No edge-case conventions are declared for this predicate: it is a straightforward universal quantification over all vertex indices and carries no special junk-value behaviour.

### Worked examples

- Claim: A triangle whose three vertices are all equal does **not** have nondegenerate edges (the predicate is false).

- Claim: For a polygon `poly` of type `Polygon P n`, `VTask.HasNondegenerateEdges poly` holds if and only if for every `i : Fin n`, `poly i ≠ poly (finRotate n i)`.

- Claim: If `n = 0`, the predicate `VTask.HasNondegenerateEdges poly` holds vacuously, since there are no indices `i : Fin 0` over which to quantify.

- Claim: A regular triangle in the Euclidean plane with three mutually distinct vertices satisfies `VTask.HasNondegenerateEdges`.

### Boundaries

- When `n = 0`, the polygon has no vertices and no edges; the universal quantification is over an empty type, so `VTask.HasNondegenerateEdges` holds vacuously for every polygon of size 0.
- When `n = 1`, there is a single vertex and a single edge whose two endpoints are both that vertex; the unique edge is always degenerate, so no 1-gon satisfies `VTask.HasNondegenerateEdges`.
- When `n = 2`, there are two vertices and two edges (each connecting the two vertices in opposite directions); nondegeneracy requires that the two vertices be distinct.
- The predicate is stated for any type `P` of points with a notion of equality (`DecidableEq` or `BEq` is not required; it uses propositional inequality `≠`), so it applies to abstract as well as metric settings.

### Not to be confused with

- **Injectivity of the vertex map** (`Function.Injective poly`): that stronger condition requires *all* vertices to be mutually distinct, whereas `HasNondegenerateEdges` only requires *adjacent* (cyclically consecutive) vertices to be distinct.
- **Simple polygon / non-self-intersecting polygon**: that condition forbids edge crossings globally and is strictly stronger and geometrically different from mere nondegeneracy of individual edges.
- **`HasNondegenerateEdges` for a path or open polygon**: the cyclic wraparound (the last vertex is compared with the first) is specific to the closed-polygon interpretation here; an open version would omit that last comparison.