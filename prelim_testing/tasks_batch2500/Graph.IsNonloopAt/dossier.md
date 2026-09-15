## VTask.IsNonloopAt

### Object

`VTask.IsNonloopAt G e x` is the proposition asserting that the vertex `x` is an endpoint of the edge `e` in the graph `G`, but `e` is **not** a loop at `x`. Concretely, this means there exists some other vertex `y`, distinct from `x`, such that `e` links `x` to `y` in `G`. Equivalently, `e` is incident with `x`, but the two endpoints of `e` are distinct (so `x` accounts for exactly one of the two ends).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsNonloopAt : {α : Type u_1} -> {β : Type u_2} -> (G : Graph α β) -> (e : β) -> (x : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`(G : Graph α β) -> (e : β) -> (x : α) -> Prop`

The first argument `G` is the graph in which incidence is being assessed. The second argument `e` is the edge under consideration (an element of the edge type `β`). The third argument `x` is the vertex (an element of the vertex type `α`) that is claimed to be a non-loop endpoint of `e`.

### Conventions

There are no declared junk-value or out-of-domain conventions for this predicate: when `e` is not an edge of `G`, or when `x` is not a vertex of `G`, the proposition is simply `False` (no witness `y ≠ x` with `G.IsLink e x y` can exist), so the predicate is well-defined and total with no special sentinel behavior.

### Worked examples

- Claim: In a banana graph `banana u v {e}` with `u ≠ v`, the edge `e` satisfies `IsNonloopAt` at both `u` and `v`.

- Claim: In a banana graph `banana u v {e}` with `u ≠ v`, `VTask.IsNonloopAt (banana u v {e}) e u` holds because there exists `v ≠ u` with `(banana u v {e}).IsLink e u v`.

- Claim: A loop edge `e` in a bouquet graph `bouquet v {e}` does **not** satisfy `IsNonloopAt` at any vertex, since a loop has both ends equal, leaving no distinct witness `y ≠ x`.

- Claim: If `G.IsNonloopAt e x` holds, then `G.Inc e x` holds (x is incident with e in G) and `¬ G.IsLoopAt e x` holds (e is not a loop at x). These two conditions are in fact equivalent to `IsNonloopAt`.

### Boundaries

- If `e` is not in the edge set of `G`, then `VTask.IsNonloopAt G e x` is `False` for all `x`, since no valid link exists.
- If `x` is not in the vertex set of `G`, then `VTask.IsNonloopAt G e x` is `False`.
- A loop edge (both endpoints equal) can never satisfy `IsNonloopAt` at **any** vertex: `G.IsLoopAt e x` implies `¬ VTask.IsNonloopAt G e y` for every `y`.
- `IsNonloopAt` is monotone in the graph: if `H ≤ G` and `H.IsNonloopAt e x`, then `G.IsNonloopAt e x`.
- For edges present in a subgraph, `IsNonloopAt` agrees between the subgraph and the ambient graph.

### Not to be confused with

- `Graph.IsLoopAt G e x`: the complementary predicate asserting that `e` **is** a loop at `x` (both endpoints equal `x`); `IsNonloopAt` and `IsLoopAt` partition the edges incident at `x`.
- `Graph.Inc G e x`: the weaker incidence predicate asserting merely that `x` is **some** endpoint of `e`, without requiring the two endpoints to differ; `IsNonloopAt` implies `Inc` but not vice versa.
- `Graph.IsLink G e x y`: the two-endpoint relation asserting `e` links `x` to `y`; `IsNonloopAt G e x` is the existential shadow of `IsLink` asking only for some distinct other endpoint `y`.
