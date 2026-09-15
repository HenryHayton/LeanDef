## Object

`VTask.map` transports a walk in one simple graph to a walk in another simple graph along a graph homomorphism. Concretely, given a graph homomorphism `f : G →g G'` (a vertex map that preserves adjacency) and a walk `w` from vertex `u` to vertex `v` in `G`, it produces a walk from `f u` to `f v` in `G'` by applying `f` to every vertex visited and every edge traversed.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {V : Type u} -> {V' : Type v} -> {G : SimpleGraph V} -> {G' : SimpleGraph V'} -> (f : G →g G') -> {u v : V} -> G.Walk u v → G'.Walk (f u) (f v)
<!-- PINNED-SIGNATURE:END -->


`VTask.map : {V : Type u} -> {V' : Type v} -> {G : SimpleGraph V} -> {G' : SimpleGraph V'} -> (f : G →g G') -> {u v : V} -> G.Walk u v → G'.Walk (f u) (f v)`

The implicit type arguments `V` and `V'` are the vertex types of the source and target graphs respectively. `G` is the source simple graph on `V` and `G'` is the target simple graph on `V'`. The explicit argument `f` is the graph homomorphism from `G` to `G'`; it provides both the vertex map and the proof that adjacency is preserved. The implicit arguments `u` and `v` are the endpoints of the input walk in `G`. The final explicit argument is the walk itself, a path of edges in `G` from `u` to `v`.

## Conventions

This operation is total: it is defined for every graph homomorphism and every walk, including the trivial (nil) walk at any vertex and walks of any finite length. No special junk values or out-of-domain conventions apply.

## Worked examples

- Claim: Mapping the trivial (nil) walk at any vertex `u` along any homomorphism `f` yields the trivial walk at `f u` in `G'`.

- Claim: Mapping a single-edge walk `cons h nil` along `f` yields a single-edge walk `cons (f.map_adj h) nil` in `G'`, whose sole edge connects `f u` to `f v`.

- Claim: The length of `VTask.map f w` equals the length of `w` for any walk `w` — the homomorphism preserves the number of steps.

- Claim: For the identity homomorphism `Hom.id`, `VTask.map Hom.id w = w` for any walk `w` (the walk is unchanged).

- Claim: Mapping commutes with concatenation: for walks `p : G.Walk u v` and `q : G.Walk v w`, `(p.append q).map f = (p.map f).append (q.map f)`.

## Boundaries

- **Nil walk**: The nil walk at vertex `u` maps to the nil walk at vertex `f u`. The walk has length zero before and after.
- **Single step**: A walk consisting of one edge between adjacent vertices `u` and `v` maps to a single-edge walk between `f u` and `f v`; the adjacency of the image is guaranteed by the homomorphism condition.
- **Non-injective homomorphism**: If `f` identifies distinct vertices, the image walk may revisit vertices or even collapse multiple steps into a trivial segment (e.g., if `f u = f v` the walk's image starts and ends at the same vertex). The operation is still well-defined, but the image walk may not be a path even if the source walk was.
- **Injectivity and path preservation**: If `f` is injective and the source walk is a path (no repeated vertices), then the image walk is also a path. More precisely, if the image walk is a path, then `f` must be injective on the support of the original walk.

## Not to be confused with

- **`SimpleGraph.Walk.mapToSubgraph`**: lifts a walk to a walk in its own induced subgraph rather than transporting it along an external homomorphism.
- **`SimpleGraph.Walk.transfer`**: transfers a walk to a different graph on the *same* vertex type when the edge relation is (locally) compatible, rather than applying a vertex-level map.
- **`SimpleGraph.Hom.mapWalk` / walk operations on darts**: functions that map the list of *darts* or *edges* of a walk via `List.map`, which produce lists rather than typed `Walk` values.