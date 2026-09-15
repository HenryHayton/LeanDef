## Object

Given a graph homomorphism `f` from a simple graph `G` to a simple graph `G'`, and a subgraph `H` of `G'`, `VTask.comap f H` is the **pullback subgraph** of `H` along `f`: the subgraph of `G` whose vertex set is the preimage of `H`'s vertex set under `f`, and whose edges are exactly those edges of `G` that map into an edge of `H` under `f`. Informally, it is the largest subgraph of `G` that `f` carries into `H`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comap : {V : Type u} -> {W : Type v} -> {G : SimpleGraph V} -> {G' : SimpleGraph W} -> (f : G →g G') -> (H : G'.Subgraph) -> G.Subgraph
<!-- PINNED-SIGNATURE:END -->


`VTask.comap : {V : Type u} -> {W : Type v} -> {G : SimpleGraph V} -> {G' : SimpleGraph W} -> (f : G →g G') -> (H : G'.Subgraph) -> G.Subgraph`

The implicit arguments fix the vertex types and ambient simple graphs on both sides. The argument `f` is the graph homomorphism from `G` to `G'` along which the pullback is taken. The argument `H` is the subgraph of `G'` being pulled back. The result is the induced subgraph of `G`.

## Conventions

There are no junk-value conventions for this definition: it is a total construction defined for every graph homomorphism and every subgraph of the codomain graph, with no degenerate or boundary inputs requiring special treatment.

## Worked examples

- Claim: If `H` is the full subgraph of `G'` (all vertices and edges), then `VTask.comap f H` has the same vertices and adjacency as all of `G`, because the preimage of the full vertex set is all of `V` and every edge of `G` maps to some edge of `G'`.

- Claim: If `H` is the empty subgraph of `G'` (no vertices, no edges), then `VTask.comap f H` has an empty vertex set and no edges, because the preimage of the empty vertex set is empty.

- Claim: For vertices `u v : V`, the pair `(u, v)` is adjacent in `VTask.comap f H` if and only if `u` and `v` are adjacent in `G` **and** `f u` and `f v` are adjacent in `H`.

- Claim: The operation `VTask.comap f` is monotone in `H`: if `H₁ ≤ H₂` as subgraphs of `G'`, then `VTask.comap f H₁ ≤ VTask.comap f H₂` as subgraphs of `G`.

- Claim: `VTask.comap f` and the subgraph map operation along `f` form a Galois connection: for any subgraph `H` of `G` and subgraph `H'` of `G'`, the image of `H` under `f` is a subgraph of `H'` if and only if `H` is a subgraph of `VTask.comap f H'`.

## Boundaries

- When `H` is the empty subgraph of `G'` (no vertices), the pullback has empty vertex set and no edges.
- When `H` is the top subgraph (all vertices and edges of `G'`), the pullback contains all vertices and all edges of `G` that are sent to edges of `G'` by `f`; since `f` is a graph homomorphism it preserves adjacency, so in fact all edges of `G` appear.
- The vertex set of the pullback is determined by the vertices of `H` only (it is the preimage of `H.verts`), independently of which edges `H` contains.
- Adjacency in the pullback requires both that the edge exists in `G` **and** that its image under `f` is an edge of `H`; neither condition alone suffices.

## Not to be confused with

- `SimpleGraph.Subgraph.map f H`: the *forward* image of a subgraph of `G` along `f`, which sends `H` to a subgraph of `G'`; `comap` is its right adjoint.
- `SimpleGraph.comap f G'`: the pullback of an entire simple graph (not a subgraph) along a function `f`, yielding a new simple graph on the domain; this operates at the graph level, not the subgraph level.
- The preimage of a set `f ⁻¹' S`: while the vertex set of the pullback subgraph is indeed a preimage of sets, the full `comap` construction also incorporates the edge/adjacency condition and does not operate on vertex sets alone.