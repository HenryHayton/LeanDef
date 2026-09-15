## VTask.Adj

### Object

Given a hypergraph `H` over a vertex type `α`, `VTask.Adj H x y` is the proposition that vertices `x` and `y` are **adjacent** in `H`: there exists at least one hyperedge `e` belonging to the edge set of `H` such that both `x` and `y` are members of `e`. This is the hypergraph generalisation of ordinary graph adjacency — rather than a single edge connecting exactly two vertices, a hyperedge may contain arbitrarily many vertices, and two vertices are adjacent whenever some common hyperedge contains them both.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Adj : {α : Type u_1} -> (H : Hypergraph α) -> (x y : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> (H : Hypergraph α) -> (x y : α) -> Prop`

The implicit type parameter `α` is the carrier type whose elements serve as vertices. The argument `H` is the hypergraph whose edge set is searched for a common hyperedge. The arguments `x` and `y` are the two vertices whose adjacency is being tested.

### Conventions

There are no declared junk-value conventions for this predicate: it is a well-defined existential proposition for every choice of `H`, `x`, and `y`. In particular, if either `x` or `y` does not belong to the vertex set of `H`, then neither can be incident to any edge of `H`, so the predicate is simply `False` — no special convention is needed to handle out-of-vertex-set inputs.

### Worked examples

- Claim: `VTask.Adj H x y` is symmetric — if `x` and `y` are adjacent in `H`, then `y` and `x` are adjacent in `H`.

- Claim: `VTask.Adj H x y ↔ VTask.Adj H y x` holds for all hypergraphs `H` and all vertices `x`, `y` of type `α`.

- Claim: If a hyperedge `e` belongs to `H` and both `x ∈ e` and `y ∈ e`, then `VTask.Adj H x y` holds.

- Claim: If `x` is not a member of any edge in `H`, then `VTask.Adj H x y` is `False` for every `y`.

### Boundaries

- **Reflexivity**: `VTask.Adj H x x` holds precisely when there is some hyperedge `e ∈ E(H)` with `x ∈ e`. Adjacency is not guaranteed to be reflexive in general (a vertex with no incident edge is not self-adjacent), nor is it guaranteed to be irreflexive.
- **Empty edge set**: If `H` has no edges at all, then `VTask.Adj H x y` is `False` for every pair `x`, `y`.
- **Vertices outside the vertex set**: A vertex that does not appear in the vertex set of `H` cannot be incident to any edge of `H`, so the predicate evaluates to `False` for any such vertex paired with any other vertex — without any explicit guard.
- **Symmetry**: The predicate is symmetric: `VTask.Adj H x y ↔ VTask.Adj H y x`, since both conditions `x ∈ e` and `y ∈ e` appear in a conjunction and can be swapped.

### Not to be confused with

- **`Hypergraph.EAdj`**: adjacency of two *edges* (hyperedges) in `H`, defined by the existence of a vertex belonging to both edges — the dual notion to vertex adjacency.
- **`Hypergraph.Incident`** (or membership of a vertex in an edge): incidence relates a single vertex to a single edge, whereas `VTask.Adj` relates two vertices via a shared edge.
- **Simple graph adjacency (`SimpleGraph.Adj`)**: in a simple graph every edge is a two-element set and adjacency implies the two vertices are distinct; hypergraph adjacency imposes neither a size constraint on edges nor irreflexivity.