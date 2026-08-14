## Object

`VTask.EAdj H e f` is the predicate asserting that two sets `e` and `f` are **edge-adjacent** in the hypergraph `H`. Two edges are edge-adjacent when both belong to the edge set of `H` and they share at least one common vertex (i.e., their intersection is nonempty as subsets of the vertex type).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.EAdj : {α : Type u_1} -> (H : Hypergraph α) -> (e f : Set α) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.EAdj : {α : Type u_1} -> (H : Hypergraph α) -> (e f : Set α) -> Prop
```

The implicit type argument `α` is the type of vertices. The argument `H` is the hypergraph whose edge set and vertex set provide the ambient structure. The arguments `e` and `f` are the two sets (candidate edges) being tested for adjacency.

## Conventions

Edge adjacency is defined to require that **both** `e` and `f` are genuine members of the edge set `E(H)`; a set that is not in `E(H)` cannot be adjacent to anything, even if it shares vertices with a real edge. A common vertex witnessing adjacency need not be explicitly a member of `V(H)` in the existential condition — only membership of `e` and `f` in `E(H)` is required directly, though a stronger lemma (`EAdj.exists_vertex`) does produce a witness in `V(H)`.

## Worked Examples

- Claim: If `H.EAdj e f` holds, then `H.EAdj f e` also holds (edge adjacency is symmetric).

- Claim: If `H.EAdj e f` holds, then `e ∩ f` is nonempty.

- Claim: `H.EAdj e f ↔ H.EAdj f e` (commutativity as a biconditional).

- Claim: If `e ∉ E(H)`, then `H.EAdj e f` is false for every `f`.

## Boundaries

- **Both edges must be in `E(H)`**: If either `e` or `f` is not a member of `E(H)`, the predicate is `False` regardless of any vertex overlap.
- **Self-adjacency**: An edge `e` is adjacent to itself (`H.EAdj e e`) if and only if `e ∈ E(H)` and `e` is nonempty (since `e ∩ e = e`).
- **Empty edges**: If `e ∈ E(H)` but `e` is the empty set, then `H.EAdj e f` is `False` for all `f` because no common vertex can exist.
- **Symmetry**: The relation is symmetric; `H.EAdj e f ↔ H.EAdj f e` always holds.

## Not to be confused with

- `Hypergraph.Adj` (vertex adjacency): that predicate asks whether two *vertices* are adjacent (i.e., both belong to some common edge), whereas `VTask.EAdj` asks whether two *edges* share a common vertex.
- Set intersection nonemptiness alone: `(e ∩ f).Nonempty` is a weaker statement; `VTask.EAdj H e f` additionally requires both sets to be edges of `H`.
- Incidence: incidence relates a single vertex to a single edge, while `VTask.EAdj` is a binary relation on pairs of edges mediated by a shared vertex.