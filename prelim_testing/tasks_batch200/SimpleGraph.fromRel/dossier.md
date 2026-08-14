## Object

`VTask.fromRel r` is the simple graph on vertex type `V` whose edges connect two distinct vertices `a` and `b` whenever `r a b` or `r b a` holds (or both). It is the simple graph that arises from the binary relation `r` by simultaneously symmetrizing it (treating `r a b` and `r b a` as equivalent) and making it irreflexive (forbidding loops).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.fromRel : {V : Type u} -> (r : V → V → Prop) -> SimpleGraph V
<!-- PINNED-SIGNATURE:END -->


`VTask.fromRel : {V : Type u} -> (r : V → V → Prop) -> SimpleGraph V`

The implicit argument `V` is the type of vertices of the resulting graph. The explicit argument `r` is any binary relation on `V`; it need not be symmetric or irreflexive — the construction enforces both automatically.

## Conventions

There are no declared junk-value or edge-case conventions for this definition: the construction is total and well-defined for every binary relation on every type, with no degenerate inputs that require special treatment.

## Worked examples

- Claim: For the relation `r a b ↔ a < b` on `Fin 3`, the vertices `0` and `1` are adjacent in `VTask.fromRel r`.

- Claim: For the discrete relation `r a b := False`, `VTask.fromRel r` has no edges (is the empty graph), since `r a b ∨ r b a` is always false.

- Claim: For the relation `r a b := True` on a type `V`, two vertices `a ≠ b` are always adjacent in `VTask.fromRel r`, since `r a b` holds for all pairs.

- Claim: A vertex `a` is never adjacent to itself in `VTask.fromRel r` regardless of whether `r a a` holds, because adjacency requires `a ≠ b`.

## Boundaries

- **Self-loops are always absent**: even if `r a a` holds, `a` is not adjacent to itself, because the construction explicitly requires the two endpoints to be distinct.
- **Symmetric relations**: if `r` is already symmetric, the symmetrization `r a b ∨ r b a` is equivalent to `r a b`, so the graph's adjacency reduces to `a ≠ b ∧ r a b`.
- **Asymmetric (directed) relations**: an asymmetric relation `r` (e.g., a strict order) is symmetrized, so if `r a b` holds but not `r b a`, the undirected edge `{a, b}` is still present.
- **Empty relation** (`r a b := False` for all `a b`): produces the graph with no edges (the empty simple graph).
- **Universal relation** (`r a b := True` for all `a b`): produces the complete graph, where every pair of distinct vertices is adjacent.

## Not to be confused with

- `SimpleGraph.fromEdgeSet`: constructs a simple graph from a set of unordered pairs (`Sym2 V`), rather than from a directed binary relation; the symmetrization is done at the `Sym2` level rather than by `∨`.
- `SimpleGraph.Adj`: the adjacency predicate of an *already-constructed* simple graph, not a constructor.
- `Relation.ReflTransGen r` / reachability: the reflexive–transitive closure of `r`, which describes multi-step connectivity; `VTask.fromRel r` only captures direct (one-step) symmetric adjacency.
