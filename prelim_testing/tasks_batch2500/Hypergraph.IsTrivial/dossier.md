## Object

A hypergraph is **trivial** if it has at least one vertex and no edges at all. Informally, a trivial hypergraph is one that contains vertices but carries no hyperedge structure whatsoever — the simplest non-empty hypergraph possible.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsTrivial : {α : Type u_1} -> (H : Hypergraph α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsTrivial : {α : Type u_1} -> (H : Hypergraph α) -> Prop`

The implicit type parameter `α` is the type of vertices. The explicit argument `H` is the hypergraph being tested for triviality.

## Conventions

No junk-value or out-of-domain conventions are declared for this definition: it is a total predicate on all hypergraphs, including the empty hypergraph (which has no vertices and therefore does **not** satisfy `IsTrivial`).

## Worked examples

- Claim: For any hypergraph `H`, if `H.IsTrivial` holds then no edge `e` belongs to `E(H)`.

- Claim: For any nonempty set `f : Set α`, the hypergraph `trivialOn f` satisfies `IsTrivial`.

- Claim: If `H` is a complete hypergraph (i.e., `H.IsComplete`) then `H.IsTrivial` is false, because a complete hypergraph on at least one vertex contains edges.

- Claim: Any trivial hypergraph satisfies `IsNonempty` (the vertex set is non-empty by definition of triviality).

## Boundaries

- The **empty hypergraph** (no vertices, no edges) is **not** trivial, because `IsTrivial` requires the vertex set to be nonempty. The condition is specifically "at least one vertex AND no edges."
- A hypergraph with at least one vertex **and** at least one edge is **not** trivial; the edge set must be exactly empty.
- A complete hypergraph is never trivial (assuming it has at least one vertex), since by definition a complete hypergraph on a nonempty vertex set contains edges.
- The predicate is meaningful for any carrier type `α`; if `α` itself is empty then no hypergraph on `α` can be trivial.

## Not to be confused with

- `Hypergraph.IsNonempty`: only requires the vertex set to be nonempty, with no restriction on the edge set; `IsTrivial` additionally demands the edge set be empty.
- `Hypergraph.IsComplete`: the opposite extreme — a complete hypergraph contains every possible hyperedge, while a trivial hypergraph contains none.
- `trivialOn f`: a **construction** that builds a specific trivial hypergraph from a set `f`, not a predicate testing whether a given hypergraph is trivial.