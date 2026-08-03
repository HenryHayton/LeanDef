## Object

`VTask.banana u v edgeSet` is a graph with vertex set `{u, v}` (exactly two, possibly equal, vertices) and a prescribed edge set, where every edge in `edgeSet` connects `u` to `v` (in either direction) and there are no other edges. When `u ≠ v` this produces a multigraph on two distinct vertices (a "banana graph" or "multi-edge" between two vertices); when `u = v` every edge is a loop at that single vertex.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.banana : {α : Type u_1} -> {β : Type u_2} -> (u v : α) -> (edgeSet : Set β) -> Graph α β
<!-- PINNED-SIGNATURE:END -->


`VTask.banana : {α : Type u_1} -> {β : Type u_2} -> (u v : α) -> (edgeSet : Set β) -> Graph α β`

The implicit type arguments `α` and `β` are the vertex type and edge type, respectively. The first explicit argument `u` is one endpoint of every edge. The second explicit argument `v` is the other endpoint of every edge. The third explicit argument `edgeSet` is the set of edges (elements of type `β`) that are present in the graph; every element of this set is a link between `u` and `v`.

## Conventions

There is no junk value in the usual sense, but two edge-case conventions govern degenerate inputs. When `edgeSet = ∅`, the resulting graph has the vertex set `{u, v}` but no edges, and is equal to the no-edge graph on `{u, v}`. When `u = v`, all edges in `edgeSet` become loops at the single vertex `u`, rather than non-loop edges between two distinct vertices.

## Worked examples

- Claim: For any `u`, `v`, and `edgeSet`, the vertex set of `VTask.banana u v edgeSet` equals `{u, v}`.

- Claim: For any `u`, `v`, and `edgeSet`, the two-vertex banana graph is symmetric in its vertex arguments: `VTask.banana u v edgeSet = VTask.banana v u edgeSet`.

- Claim: An edge `e` is incident to a vertex `x` in `VTask.banana u v edgeSet` if and only if `e ∈ edgeSet` and (`x = u` or `x = v`).

- Claim: Two vertices `x` and `y` are adjacent in `VTask.banana u v edgeSet` if and only if `edgeSet` is nonempty and the unordered pair `{x, y}` equals `{u, v}`.

- Claim: When `edgeSet = ∅`, `VTask.banana u v ∅` has no edges and equals the no-edge graph on `{u, v}`.

## Boundaries

- **Empty edge set**: `VTask.banana u v ∅` is a valid graph with vertex set `{u, v}` and no edges; it coincides with the no-edge graph on `{u, v}`.
- **Equal vertices (`u = v`)**: The graph is still well-formed; `{u, v}` collapses to a singleton, and every edge in `edgeSet` is a loop at `u`. In particular, `IsNonloopAt` fails for every edge, while `IsLoopAt` holds for every edge.
- **Distinct vertices (`u ≠ v`)**: Every edge in `edgeSet` is a non-loop edge between two distinct vertices; `IsLoopAt` fails for every edge.
- **Large or infinite `edgeSet`**: The construction is valid for any `Set β`; there is no finiteness requirement on either the vertex type or the edge type.

## Not to be confused with

- **`Graph.noEdge`**: A graph on a given vertex set with no edges at all; `VTask.banana u v ∅` reduces to this, but `noEdge` does not carry an edge set or enforce exactly two vertices.
- **A simple graph on two vertices**: A simple graph has at most one edge between any pair of vertices, whereas `VTask.banana` allows an arbitrary (possibly infinite) set of parallel edges between `u` and `v`.
- **A path graph on two vertices**: A path or complete graph `K₂` is a specific combinatorial object with exactly one edge; `VTask.banana` is a constructor parametrised by an arbitrary edge set, not a fixed graph.