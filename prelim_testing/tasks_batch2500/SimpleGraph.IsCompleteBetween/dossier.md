## VTask.IsCompleteBetween

### Object

Given a simple graph `G` on a vertex type `V`, and two sets of vertices `s` and `t`, `VTask.IsCompleteBetween G s t` is the proposition asserting that the bipartite "slice" of `G` between `s` and `t` is complete: every vertex in `s` is adjacent (in `G`) to every vertex in `t`. Because adjacency in a simple graph is symmetric and irreflexive, this forces `s` and `t` to be disjoint (no vertex can be adjacent to itself), and the condition is symmetric in `s` and `t`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsCompleteBetween : {V : Type u} -> (G : SimpleGraph V) -> (s t : Set V) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsCompleteBetween : {V : Type u} -> (G : SimpleGraph V) -> (s t : Set V) -> Prop`

The implicit argument `V` is the type of vertices of the graph. The first explicit argument `G` is the simple graph under consideration. The second and third explicit arguments `s` and `t` are the two sets of vertices whose cross-adjacency is being tested — every vertex in `s` must be adjacent (in `G`) to every vertex in `t`.

### Conventions

No edge-case or junk-value conventions are declared for this definition: it is a universally quantified proposition over all `v₁ ∈ s` and `v₂ ∈ t`, so when `s` or `t` is empty the quantifier is vacuously true, which is the standard mathematical convention and requires no special note.

### Worked examples

- Claim: For the complete bipartite graph `completeBipartiteGraph (Fin 2) (Fin 3)`, the predicate holds between the "left" copy `{Sum.inl 0, Sum.inl 1}` and the "right" copy `{Sum.inr 0, Sum.inr 1, Sum.inr 2}` in any graph that contains it.

- Claim: If `s = ∅` (the empty set) and `t` is any set of vertices, then `VTask.IsCompleteBetween G ∅ t` holds for any graph `G`, because the defining universal quantification over `s` is vacuously satisfied.

- Claim: If `G` is the empty graph (no edges) and `s` and `t` are both nonempty, then `VTask.IsCompleteBetween G s t` is false, since there are vertices in `s` and `t` that are not adjacent.

- Claim: The predicate is symmetric: `VTask.IsCompleteBetween G s t ↔ VTask.IsCompleteBetween G t s`.

- Claim: Whenever `VTask.IsCompleteBetween G s t` holds, the sets `s` and `t` must be disjoint (as subsets of `V`), since a simple graph has no self-loops.

### Boundaries

- **Empty sets**: If either `s` or `t` is empty, the proposition holds vacuously for any graph `G`.
- **Singleton sets**: `VTask.IsCompleteBetween G {u} {v}` reduces to the single adjacency `G.Adj u v`.
- **Disjointness forced**: Because `G` is a simple graph (irreflexive adjacency), `VTask.IsCompleteBetween G s t` implies `s ∩ t = ∅`; in particular, `VTask.IsCompleteBetween G s s` can only hold if `s` is empty.
- **Symmetry**: The condition `VTask.IsCompleteBetween G s t` is logically equivalent to `VTask.IsCompleteBetween G t s`.
- **Subgraph monotonicity**: If `H ≤ G` (as simple graphs) and `VTask.IsCompleteBetween H s t`, then `VTask.IsCompleteBetween G s t`; but the converse need not hold.

### Not to be confused with

- **`SimpleGraph.IsComplete`** (or the complete graph `⊤`): That predicate asserts every two *distinct* vertices of the whole graph are adjacent, not just vertices across two specified sets.
- **`SimpleGraph.IsBipartite`**: That predicate says the vertex set can be 2-coloured with no monochromatic edges; it does *not* require all cross-edges to exist.
- **`SimpleGraph.Adj`**: A binary predicate on two individual vertices, not on two sets; `VTask.IsCompleteBetween G s t` is the universal lifting of `G.Adj` across the Cartesian product `s × t`.
