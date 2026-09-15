## Object

Two graphs `G` and `H` (over the same vertex type `α` and edge type `β`) are **compatible** if, whenever an edge `e` belongs to both graphs, the two graphs agree completely on what vertices that edge connects. In other words, for every edge shared by both edge-sets, the "link" relation — specifying which ordered pair of vertices the edge joins, including whether it is a loop — is identical in `G` and in `H`. Edges that belong to only one of the two graphs place no constraint.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Compatible : {α : Type u_1} -> {β : Type u_2} -> (G H : Graph α β) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Compatible : {α : Type u_1} -> {β : Type u_2} -> (G H : Graph α β) -> Prop`

Both type parameters are implicit: `α` is the common vertex type and `β` is the common edge type. The first explicit argument `G` is the first graph; the second explicit argument `H` is the second graph. The proposition asserts that every edge in the intersection of their edge-sets has the same endpoints in `G` as in `H`.

## Conventions

The condition is stated only for edges appearing in **both** graphs; edges present in exactly one graph are unconstrained and do not affect compatibility. There are no junk-value conventions beyond this natural domain restriction inherent in the definition.

## Worked examples

- Claim: Every graph is compatible with itself — `VTask.Compatible G G` holds for any graph `G`.

- Claim: Compatibility is symmetric: if `VTask.Compatible G H` then `VTask.Compatible H G`.

- Claim: Any two graphs whose edge-sets are disjoint are compatible, since the universal quantification over shared edges is vacuously true.

- Claim: If `H₁` and `H₂` are both subgraphs of a common graph `G` (i.e., `H₁ ≤ G` and `H₂ ≤ G`), then `VTask.Compatible H₁ H₂` holds, because both inherit their edge-endpoint data from `G`.

- Claim: If `H ≤ G` (H is a subgraph of G), then `VTask.Compatible H G`.

## Boundaries

- When the two graphs have **disjoint** edge-sets, compatibility holds vacuously: there are no shared edges to check.
- A graph is always compatible with itself (`Compatible.rfl` / `Compatible.refl`).
- Compatibility is **not** transitive in general: `G` compatible with `H` and `H` compatible with `K` does not imply `G` compatible with `K`, since edges shared between `G` and `K` need not pass through `H`.
- Compatibility is **symmetric**: `Compatible G H ↔ Compatible H G`.
- Subgraph order implies compatibility: any subgraph is compatible with its host graph, and any two subgraphs of a common graph are compatible with each other.
- Compatibility is preserved downward under the subgraph order: if `G₁ ≤ G`, `H₁ ≤ H`, and `G` is compatible with `H`, then `G₁` is compatible with `H₁`.

## Not to be confused with

- **Graph isomorphism** — which requires a bijection between vertex/edge sets preserving structure globally, not merely consistency on shared edges.
- **Graph equality** — which demands identical vertex sets, edge sets, and link relations everywhere, while compatibility only constrains the intersection of edge-sets.
- **Subgraph (`H ≤ G`)** — which requires `H`'s edges and vertices to be contained in `G`'s with matching link data; compatibility is weaker and symmetric, requiring no containment.
