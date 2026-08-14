## VTask.map

### Object

Given a function `f : V → W` and a simple graph `G` on vertex type `V`, together with a proof that `f` separates adjacent vertices (i.e., whenever two vertices are adjacent in `G` their images under `f` are distinct), `VTask.map` packages `f` as a graph homomorphism from `G` to the image graph `SimpleGraph.map f G`. Informally, if `f` is a proper coloring of `G` with colors drawn from `W`, then `f` is also a structure-preserving map from `G` into the graph on `W` whose edges are exactly the images of edges of `G` under `f`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {V : Type u_1} -> {W : Type u_2} -> (f : V → W) -> (G : SimpleGraph V) -> (h : ∀ {u v : V}, G.Adj u v → f u ≠ f v) -> G →g SimpleGraph.map f G
<!-- PINNED-SIGNATURE:END -->


`{V : Type u_1} -> {W : Type u_2} -> (f : V → W) -> (G : SimpleGraph V) -> (h : ∀ {u v : V}, G.Adj u v → f u ≠ f v) -> G →g SimpleGraph.map f G`

The implicit arguments `V` and `W` are the source and target vertex types. The argument `f` is the vertex map from `V` to `W`. The argument `G` is the simple graph whose vertex set is `V`. The argument `h` is the key hypothesis: a proof that whenever `u` and `v` are adjacent in `G`, their images `f u` and `f v` are distinct in `W`. The return type is a bundled graph homomorphism from `G` to the graph on `W` obtained by pushing `G` forward along `f`.

### Conventions

No special junk-value or edge conventions are declared for this definition: the construction is total and well-defined for any `f`, `G`, and `h` satisfying the stated types, and no degenerate inputs produce conventionally-defined but mathematically arbitrary output.

### Worked examples

- Claim: For the 2-vertex complete graph `K₂` and the identity function on `Fin 2`, the hypothesis that adjacent vertices map to distinct values is exactly the adjacency condition, and `VTask.map id K₂ h` is a homomorphism from `K₂` to `SimpleGraph.map id K₂`.

- Claim: For a graph `G : SimpleGraph V` and any proper coloring `c : V → Fin n` (satisfying `G.Adj u v → c u ≠ c v`), the result `VTask.map c G h` is a graph homomorphism from `G` to `SimpleGraph.map c G`, and its underlying function `(VTask.map c G h).toFun` equals `c`.

- Claim: For any simple graph `G` and injective function `f`, the condition `∀ {u v}, G.Adj u v → f u ≠ f v` holds automatically (since `G` is a simple graph with `Adj u v → u ≠ v`), so `VTask.map f G h` is always constructible when `f` is injective.

### Boundaries

- If `f` is the constant function (mapping all vertices to the same element of `W`), the hypothesis `h` cannot be satisfied for any graph with at least one edge, so `VTask.map` cannot be applied. For edgeless graphs, the constant function trivially satisfies `h` (vacuously), and `VTask.map` produces a valid homomorphism to the discrete graph on `W`.
- For injective `f`, the hypothesis `h` follows from irreflexivity of adjacency (`G.Adj u v → u ≠ v`) combined with injectivity, so the construction always applies.
- The target graph `SimpleGraph.map f G` is the graph on `W` whose edges are precisely the images of edges of `G` under `f`; the homomorphism lands in this subgraph, not in the complete graph on `W`.
- When `G` has no edges, the hypothesis `h` is vacuously true for any `f`, and the resulting homomorphism simply sends every vertex to its image in the (also edgeless) mapped graph.

### Not to be confused with

- `SimpleGraph.map f G` (the *graph* obtained by pushing `G` forward along `f`) — that is the codomain of `VTask.map`, not a homomorphism itself.
- `SimpleGraph.comap f G` — the *pullback* of a graph along `f`, which goes in the opposite direction; `G ≤ comap ⊤ f` is an equivalent way to state the hypothesis `h`, but `comap` itself is not a homomorphism constructor.
- `SimpleGraph.Hom.comp` — composition of two already-existing graph homomorphisms, not the construction of one from a raw vertex function and a separation hypothesis.