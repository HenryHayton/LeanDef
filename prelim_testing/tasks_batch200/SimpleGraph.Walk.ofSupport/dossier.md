## VTask.ofSupport

### Object

Given a nonempty list of vertices of a simple graph such that every pair of consecutive vertices in the list are adjacent in the graph, `VTask.ofSupport` produces a walk in the graph whose vertex sequence (support) is exactly that list. The walk starts at the list's first element and ends at its last element.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofSupport : {V : Type u} -> {G : SimpleGraph V} -> (l : List V) -> (hne : l ≠ []) -> (hchain : List.IsChain G.Adj l) -> G.Walk (l.head hne) (l.getLast hne)
<!-- PINNED-SIGNATURE:END -->


The implicit argument `V` is the type of vertices and `G` is the simple graph on those vertices. The argument `l` is the nonempty list of vertices that is to become the support of the constructed walk. The argument `hne` is the proof that `l` is not the empty list (required to make the head and last elements well-defined). The argument `hchain` is the proof that consecutive entries in `l` are adjacent in `G` (i.e., `l` forms a chain under the adjacency relation of `G`).

### Conventions

When the list `l` has exactly one element, the constructed walk is the trivial (nil) walk at that single vertex — it has length zero and its support is the singleton list. There are no junk-value conventions beyond this base case; the function is well-defined and total on all nonempty lists satisfying the chain condition.

### Worked examples

- Claim: For a singleton list `[v]`, `VTask.ofSupport [v] _ _` equals the nil walk at `v`, which has length 0.

- Claim: For a two-element list `[u, v]` where `u` and `v` are adjacent in `G`, `VTask.ofSupport [u, v] _ _` is a walk of length 1 from `u` to `v`.

- Claim: The support of `VTask.ofSupport l hne hchain` is exactly `l` (as stated by `support_ofSupport`).

- Claim: The length of `VTask.ofSupport l hne hchain` equals `l.length - 1`; for a list of `n` vertices the walk traverses `n - 1` edges.

- Claim: Applying `VTask.ofSupport` to the support of an existing walk `p` recovers (a copy of) `p` itself; that is, the construction is a right inverse to extracting the support.

### Boundaries

- **Singleton list**: The list `[v]` with one vertex produces the nil walk `Walk.nil` at `v`. No edge is traversed.
- **Two-element list**: The list `[u, v]` (with `u` adjacent to `v`) produces a single-edge walk `Walk.cons h Walk.nil`.
- **Minimum chain condition**: If the list has two or more elements, every adjacent pair must be adjacent in the graph. If the chain condition `hchain` were violated the construction would not type-check (the proof is a required argument).
- **Length**: The walk has exactly `l.length - 1` edges, consistent with the fact that `n` vertices connected in a chain span `n - 1` edges.

### Not to be confused with

- `SimpleGraph.Walk.support`: Goes in the opposite direction — extracts the list of vertices from an already-given walk, rather than constructing a walk from a list.
- `SimpleGraph.Walk.copy`: Reindexes the endpoints of an existing walk using proofs of equality, but does not construct a walk from a vertex list.
- `List.IsChain`: The purely list-theoretic predicate asserting that consecutive elements satisfy a relation; `VTask.ofSupport` consumes this predicate but is not the same object.