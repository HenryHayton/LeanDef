## Object

`VTask.IsInduced G'` is the predicate asserting that a subgraph `G'` of a simple graph `G` is an *induced subgraph*: whenever two vertices both belong to `G'`'s vertex set and are adjacent in the ambient graph `G`, they are also adjacent in `G'` itself. In other words, `G'` inherits every edge of `G` that runs between its own vertices — it does not "forget" any such edge.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsInduced : {V : Type u} -> {G : SimpleGraph V} -> (G' : G.Subgraph) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.IsInduced : {V : Type u} -> {G : SimpleGraph V} -> (G' : G.Subgraph) -> Prop
```

The implicit argument `V` is the type of vertices. The implicit argument `G` is the ambient simple graph on `V`. The explicit argument `G'` is the subgraph of `G` whose induced-ness is being tested.

## Conventions

There are no declared junk-value or boundary conventions for this definition: it is a universally-quantified predicate that is meaningful for every subgraph, including those with empty vertex sets, and it imposes no restriction that would require a special default value.

## Worked examples

- Claim: The top subgraph of any simple graph (containing all vertices and all edges of `G`) is an induced subgraph, because every edge between vertices of `G` is already present.

- Claim: If `G'` is an induced subgraph and `G'.verts = s`, then `G'` equals the subgraph obtained by inducing the top graph on `s` (i.e., `VTask.IsInduced G' ↔ ∃ s, G' = SimpleGraph.Subgraph.induce ⊤ s`).

- Claim: A subgraph `G'` fails `VTask.IsInduced` precisely when there exist two vertices `v w ∈ G'.verts` that are adjacent in `G` but not adjacent in `G'`.

## Boundaries

- **Empty vertex set**: If `G'.verts = ∅`, the predicate holds vacuously — there are no vertices to check, so `VTask.IsInduced G'` is true.
- **Single-vertex subgraph**: A subgraph with exactly one vertex has no adjacent pairs among its vertices, so it is trivially induced regardless of the ambient graph's edges.
- **Spanning subgraphs**: A subgraph that has `G`.vertex set as its vertex set is induced if and only if it is equal (as a subgraph) to `G` itself, since every edge of `G` must be present.
- **Already-complete edge sets**: If `G'` already contains every edge of `G` restricted to its vertex set, then it is induced by definition.

## Not to be confused with

- `SimpleGraph.Subgraph.induce`: This is the *constructor* that builds an induced subgraph from a vertex set; `VTask.IsInduced` is the *predicate* that tests whether a given subgraph is induced.
- `SimpleGraph.Subgraph.spanning`: A spanning subgraph retains all vertices but may omit edges; an induced subgraph retains all edges between its (possibly restricted) vertex set but may omit vertices.
- `SimpleGraph.Subgraph.Adj`: The adjacency relation of a subgraph, which is weaker than ambient adjacency; `VTask.IsInduced` exactly closes the gap between subgraph adjacency and ambient adjacency on the vertex set.
