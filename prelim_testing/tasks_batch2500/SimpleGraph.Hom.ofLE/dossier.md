## Object

Given two simple graphs `G₁` and `G₂` on the same vertex type `V` where `G₁` is a subgraph of `G₂` (i.e., every edge of `G₁` is also an edge of `G₂`), `VTask.ofLE h` is the canonical graph homomorphism from `G₁` into `G₂`. It acts as the identity on vertices: each vertex is sent to itself, and adjacency is preserved because any edge present in the smaller graph is also present in the larger one.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofLE : {V : Type u_1} -> {G₁ G₂ : SimpleGraph V} -> (h : G₁ ≤ G₂) -> G₁ →g G₂
<!-- PINNED-SIGNATURE:END -->


`VTask.ofLE : {V : Type u_1} -> {G₁ G₂ : SimpleGraph V} -> (h : G₁ ≤ G₂) -> G₁ →g G₂`

The vertex type `V` is an implicit universe-polymorphic type shared by both graphs. `G₁` and `G₂` are implicit simple graphs on `V`. The argument `h` is a proof that `G₁ ≤ G₂`, meaning `G₁` is a subgraph of `G₂` (its edge relation is contained in that of `G₂`). The result is a graph homomorphism from `G₁` to `G₂`.

## Conventions

There are no junk-value or edge conventions to declare: the definition is total and well-behaved for all inputs satisfying `G₁ ≤ G₂`, which is encoded directly in the type of `h`.

## Worked examples

- Claim: For any proof `h : G₁ ≤ G₂` and any vertex `v : V`, applying `VTask.ofLE h` to `v` returns `v` itself (the underlying map is the identity).

- Claim: For the inclusion of the empty graph into any graph `G` on `V`, `VTask.ofLE` yields a graph homomorphism from `⊥` to `G`.

- Claim: Composing the comap of a homomorphism `f : H →g G` with the canonical inclusion given by `VTask.ofLE f.le_comap` recovers `f`.

## Boundaries

- When `G₁ = G₂` and `h` is the reflexivity proof `le_refl G₁`, `VTask.ofLE h` is the identity homomorphism on `G₁`.
- When `G₁ = ⊥` (the empty graph with no edges), `VTask.ofLE h` still maps every vertex to itself; it is trivially a homomorphism since `⊥` has no edges to check.
- When `G₂ = ⊤` (the complete graph), any subgraph `G₁` satisfies `G₁ ≤ ⊤`, so `VTask.ofLE` always produces a valid homomorphism into the complete graph.
- The homomorphism is always injective on vertices (since it is the identity), but it need not be an embedding or isomorphism unless `G₁ = G₂`.

## Not to be confused with

- `SimpleGraph.Hom.comap`: pulls back a homomorphism to obtain a new graph on the domain; `VTask.ofLE` goes in the forward direction and only applies when one graph is a subgraph of another on the *same* vertex type.
- `SimpleGraph.Iso` (graph isomorphism): requires a bijection that preserves and reflects edges; `VTask.ofLE` only preserves edges and need not reflect them.
- `SimpleGraph.Embedding` (graph embedding): requires injectivity on vertices and reflection of edges; `VTask.ofLE` is weaker, providing only edge preservation.