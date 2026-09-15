## VTask.labelGraph

### Object

Given an edge-labeling of a simple graph `G` (an assignment of a label from a type `K` to each edge of `G`) and a chosen label `k`, `VTask.labelGraph C k` is the simple graph on the same vertex type `V` whose edges are precisely the edges of `G` that `C` labels `k`. In other words, it is the "color-`k` subgraph" of `G` induced by the labeling.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.labelGraph : {V : Type u_1} -> {G : SimpleGraph V} -> {K : Type u_3} -> (C : G.EdgeLabeling K) -> (k : K) -> SimpleGraph V
<!-- PINNED-SIGNATURE:END -->


The implicit arguments fix the vertex type `V`, the base graph `G`, and the label type `K`. The first explicit argument `C` is the edge labeling: a function assigning to every edge of `G` a label in `K`. The second explicit argument `k` is the particular label whose corresponding subgraph is to be extracted.

### Conventions

There are no special junk-value or boundary conventions for this construction: it is defined for all simple graphs, all edge labelings, and all choices of label, with no degenerate or undefined cases.

### Worked examples

- Claim: For a complete graph on a two-element type with a constant labeling, `VTask.labelGraph C k` equals the complete graph itself when `k` is the unique label value used.

- Claim: For any edge labeling `C` on a graph `G`, two distinct label subgraphs `VTask.labelGraph C k` and `VTask.labelGraph C l` (with `k ≠ l`) are disjoint as simple graphs, meaning they share no edges.

- Claim: The supremum (union) over all labels `k` of `VTask.labelGraph C k` equals the original graph `G`; every edge of `G` belongs to exactly one label subgraph.

- Claim: `VTask.labelGraph C k` is always a subgraph of (i.e., its edge set is contained in that of) `G`, regardless of the labeling or label choice.

### Boundaries

- If no edge of `G` receives label `k` under `C`, then `VTask.labelGraph C k` is the empty graph (no edges) on `V`.
- If every edge of `G` receives label `k`, then `VTask.labelGraph C k` equals `G` itself.
- The construction is defined even when `K` is an empty type, in which case no label can be chosen, and the function vacuously produces a graph for any (impossible) `k`.
- Vertices are never removed: the vertex type of `VTask.labelGraph C k` is always `V`, the same as that of `G`, regardless of whether any vertex has an incident edge labeled `k`.

### Not to be confused with

- `SimpleGraph.induce`: restricts a graph to a vertex subset, not an edge subset determined by a labeling.
- `SimpleGraph.fromEdgeSet` (the underlying constructor): builds a graph from an arbitrary set of unordered pairs, without the structure of an edge labeling or the parent graph `G`.
- An edge coloring (proper edge coloring): `VTask.labelGraph` does not require that the labeling be proper (adjacent edges may share labels); it only extracts the subgraph for one label value.