## VTask.IsLoop

### Object

A predicate on a hypergraph `H` and a set `e` of vertices that holds precisely when `e` is an edge of `H` whose vertex set consists of exactly one vertex — that is, `e` is a singleton set and also belongs to the edge collection of `H`. Such an edge is called a *loop*.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsLoop : {α : Type u_1} -> (H : Hypergraph α) -> (e : Set α) -> Prop
<!-- PINNED-SIGNATURE:END -->


The first argument is the hypergraph under consideration, supplying both the vertex type and the edge set. The second argument is the candidate edge (a set of vertices of `H`) being tested for being a loop.

### Conventions

No special junk-value or boundary conventions are declared: the predicate is defined for every hypergraph and every set of vertices of the appropriate type, and it simply returns `False` whenever `e` is not a member of `H`'s edge set or is not a singleton.

### Worked examples

- Claim: For any hypergraph `H` over a type `α` and any vertex `x`, if the singleton set `{x}` belongs to the edge set of `H`, then `H.IsLoop {x}` holds.

- Claim: `H.IsLoop e` implies `Set.ncard e = 1`; equivalently, `IsLoop` forces the edge to contain exactly one vertex.

- Claim: `H.IsLoop e` is equivalent to the conjunction `e ∈ E(H) ∧ ∃ x, e = {x}`, matching the characterization given by `isLoop_iff_mem_edgeSet_and_singleton`.

- Claim: An edge that is the empty set can never satisfy `H.IsLoop`, regardless of whether it belongs to the edge set, because the empty set has cardinality 0, not 1.

### Boundaries

- The empty set is never a loop: it is not a singleton, so the existential witness fails.
- A two-element (or larger) edge is never a loop, even if it belongs to `H`.
- A singleton set `{x}` that does *not* belong to `E(H)` is not a loop: the membership condition fails.
- The predicate is well-defined for any `Set α`, not just for sets that are already known to be vertices or edges of `H`.

### Not to be confused with

- **A simple edge (link/hyperedge with ≥ 2 vertices):** an edge belonging to `H` that contains two or more vertices; this is distinct from a loop, which requires exactly one vertex.
- **An isolated vertex:** a vertex that appears in no edge of `H`; a loop, by contrast, is an *edge* (which happens to contain only one vertex) and does not assert anything about edge-absence.
- **`Set.ncard e = 1` alone:** having cardinality one is necessary but not sufficient for `IsLoop`; the edge must also be a member of `E(H)`.
