## Object

`VTask.toSubgraph` converts a `SimpleGraph V` that is known to be a subgraph of a fixed ambient graph `G` (in the sense of having a smaller or equal edge relation) into a value of type `G.Subgraph` — the bundled subgraph type that records both a vertex set and an adjacency relation, together with the coherence conditions required by Mathlib's subgraph API. The resulting subgraph has *all* vertices of `V` as its vertex set, and uses the adjacency relation of `H` exactly.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toSubgraph : {V : Type u} -> {G : SimpleGraph V} -> (H : SimpleGraph V) -> (h : H ≤ G) -> G.Subgraph
<!-- PINNED-SIGNATURE:END -->


`VTask.toSubgraph : {V : Type u} -> {G : SimpleGraph V} -> (H : SimpleGraph V) -> (h : H ≤ G) -> G.Subgraph`

The implicit argument `V` is the common vertex type shared by `H` and `G`. The implicit argument `G` is the ambient "parent" simple graph, the one whose subgraph type is being targeted. The explicit argument `H` is the simple graph on the same vertex type that is to be packaged as a subgraph. The explicit argument `h` is a proof that `H` is indeed a subgraph of `G`, i.e., that whenever two vertices are adjacent in `H` they are also adjacent in `G`.

## Conventions

The vertex set of the resulting `G.Subgraph` is taken to be all of `Set.univ`, meaning every vertex of `V` is considered to belong to the subgraph regardless of whether it has any edges in `H`. This is a Mathlib convention: `toSubgraph` does not restrict the vertex set to only the endpoints of edges of `H`.

## Worked examples

- Claim: For any simple graph `H ≤ G` and any vertex `v : V`, the vertex `v` belongs to `(VTask.toSubgraph H h).verts`.

- Claim: For any simple graph `H ≤ G` and vertices `u v : V`, `(VTask.toSubgraph H h).Adj u v` holds if and only if `H.Adj u v`.

- Claim: The adjacency relation of the subgraph `VTask.toSubgraph H h` is exactly the adjacency relation of `H`, not some larger relation.

- Claim: If `H = ⊥` (the edgeless graph) and `G` is any simple graph, then `VTask.toSubgraph ⊥ (bot_le)` produces a spanning subgraph of `G` with no edges but containing every vertex.

## Boundaries

- When `H = G` and `h` is the identity proof (reflexivity of `≤`), `VTask.toSubgraph G (le_refl G)` yields a subgraph whose adjacency is exactly `G.Adj` and whose vertex set is all of `V` — essentially the top element of the subgraph lattice of `G`.
- When `H = ⊥` (the empty graph), the result is a spanning subgraph with no edges at all; every vertex is still present because `verts = Set.univ`.
- Because `verts` is always `Set.univ`, the resulting subgraph is always a *spanning* subgraph (every vertex of the ambient graph is included), even if `H` has isolated vertices or no edges.
- The function is total: it is defined for any `H` and any proof `h : H ≤ G`; there are no cases where it is undefined.

## Not to be confused with

- `SimpleGraph.Subgraph.coe`: Converts a `G.Subgraph` back to a `SimpleGraph` on the induced vertex subtype, going in the opposite direction from `VTask.toSubgraph`.
- `SimpleGraph.Subgraph.induce`: Produces a subgraph induced by a chosen vertex subset, which may have a restricted vertex set rather than `Set.univ`.
- `SimpleGraph.subgraphOfAdj`: Creates a subgraph from a single edge, a much more restricted constructor than `VTask.toSubgraph`.