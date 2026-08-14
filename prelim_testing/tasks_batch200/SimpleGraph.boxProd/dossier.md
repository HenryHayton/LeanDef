## Object

The **box product** (also called the **Cartesian product**) of two simple graphs `G` on vertex set `α` and `H` on vertex set `β` is the simple graph whose vertices are ordered pairs `(a, b) ∈ α × β`, where two vertices are adjacent if and only if they agree in one coordinate and the graphs relate them in the other. Concretely, `(a₁, b)` and `(a₂, b)` are adjacent when `G` has an edge between `a₁` and `a₂`, and `(a, b₁)` and `(a, b₂)` are adjacent when `H` has an edge between `b₁` and `b₂`. Two vertices that differ in both coordinates are never adjacent.

The box product is a fundamental construction in graph theory; for instance, the `n`-dimensional hypercube graph `Qₙ` is the `n`-fold box product of `K₂` with itself.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.boxProd : {α : Type u_1} -> {β : Type u_2} -> (G : SimpleGraph α) -> (H : SimpleGraph β) -> SimpleGraph (α × β)
<!-- PINNED-SIGNATURE:END -->


`VTask.boxProd : {α : Type u_1} -> {β : Type u_2} -> (G : SimpleGraph α) -> (H : SimpleGraph β) -> SimpleGraph (α × β)`

The first explicit argument `G` is the simple graph on the first coordinate type `α`; the second explicit argument `H` is the simple graph on the second coordinate type `β`. The universe-polymorphic vertex types `α` and `β` are inferred implicitly from `G` and `H`, respectively.

## Conventions

The box product is symmetric by construction: the adjacency relation is declared `symm`, so there is no distinguished "left" or "right" orientation. In particular, if `(a₁, b) ~ (a₂, b)` then also `(a₂, b) ~ (a₁, b)`, and similarly for the second coordinate.

No junk-value convention is needed for out-of-domain inputs, because the construction is total for all simple graphs `G` and `H`.

## Worked examples

- Claim: In `VTask.boxProd G H`, two pairs sharing their second coordinate are adjacent precisely when `G` relates their first coordinates (`boxProd_adj_left`).

- Claim: In `VTask.boxProd G H`, two pairs sharing their first coordinate are adjacent precisely when `H` relates their second coordinates (`boxProd_adj_right`).

- Claim: The degree of a vertex `x` in `VTask.boxProd G H` equals the degree of `x.1` in `G` plus the degree of `x.2` in `H`. That is, each G-neighbour of the first component and each H-neighbour of the second component contributes exactly one edge.

- Claim: `VTask.boxProd G H` is connected if and only if both `G` and `H` are connected.

- Claim: The graph-theoretic distance in `VTask.boxProd G H` between vertices `x` and `y` equals the distance from `x.1` to `y.1` in `G` plus the distance from `x.2` to `y.2` in `H`.

## Boundaries

- If either `G` or `H` is the empty graph (no edges), then `VTask.boxProd G H` also has no edges (since both disjuncts of the adjacency condition require an edge in one of the factor graphs).
- If either `G` or `H` has a single vertex (trivially, any single-vertex graph), the box product is isomorphic to the other factor graph.
- Vertices `(a₁, b₁)` and `(a₂, b₂)` with `a₁ ≠ a₂` and `b₁ ≠ b₂` are **never** adjacent, regardless of whether `G` or `H` has edges between the respective components.
- The construction is total: it is defined for all simple graphs on any (possibly infinite) vertex types.
- Because `G` and `H` are simple graphs (irreflexive, symmetric adjacency), `VTask.boxProd G H` is automatically a simple graph: no loops arise (since `G.Adj a₁ a₂` implies `a₁ ≠ a₂`, and the second coordinates match, so `(a₁, b) ≠ (a₂, b)`), and symmetry is built in.

## Not to be confused with

- **Categorical (tensor/direct) product of graphs**: Two vertices `(a₁, b₁)` and `(a₂, b₂)` are adjacent when `G` relates `a₁, a₂` AND `H` relates `b₁, b₂` simultaneously (both coordinates change); in the box product, exactly one coordinate changes.
- **Strong product of graphs**: Combines both the box product edges and the tensor product edges, so vertices may be adjacent when one *or* both coordinates change.
- **Lexicographic product of graphs**: An asymmetric construction where adjacency depends on a priority ordering of the factor graphs, not a symmetric split by coordinate.