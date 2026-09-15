## Object

Given a walk in a simple graph — a finite sequence of vertices where consecutive vertices are adjacent — `VTask.support` returns the ordered list of all vertices visited by that walk, from the starting vertex to the ending vertex, including repetitions if the walk revisits a vertex.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.support : {V : Type u} -> {G : SimpleGraph V} -> {u v : V} -> G.Walk u v → List V
<!-- PINNED-SIGNATURE:END -->


`VTask.support : {V : Type u} -> {G : SimpleGraph V} -> {u v : V} -> G.Walk u v → List V`

The implicit type `V` is the vertex type of the graph. The implicit argument `G` is the simple graph in which the walk lives. The implicit vertices `u` and `v` are the start and end of the walk, respectively. The explicit argument is the walk itself, whose support is to be computed.

## Conventions

There are no special junk-value or default-value conventions for this definition: it is a structurally recursive function whose output is fully determined by the walk on every input, including the base case of a trivial (nil) walk.

## Worked examples

- Claim: For any graph `G` and vertex `u`, the support of the nil (empty) walk at `u` is the singleton list `[u]`.
  ```lean
  example {V : Type*} {G : SimpleGraph V} {u : V} : (SimpleGraph.Walk.nil (G := G) (u := u)).support = [u] := by rfl
  ```

- Claim: For any graph `G`, adjacent vertices `u v w`, and edge proofs `h : G.Adj u v` and `h' : G.Adj v w`, the support of the walk `cons h (cons h' nil)` is `[u, v, w]`.
  ```lean
  example {V : Type*} {G : SimpleGraph V} {u v w : V} (h : G.Adj u v) (h' : G.Adj v w) :
      (SimpleGraph.Walk.cons h (SimpleGraph.Walk.cons h' SimpleGraph.Walk.nil)).support = [u, v, w] := by rfl
  ```

- Claim: The support of any walk from `u` to `v` is nonempty.

- Claim: The first element of the support of any walk from `u` to `v` is `u`.

- Claim: The last element of the support of any walk from `u` to `v` is `v`.

- Claim: The length of the support of a walk equals the number of edges in the walk plus one.

## Boundaries

- **Nil walk**: The support of `Walk.nil` at vertex `u` is exactly `[u]`. This is the base case: a walk that goes nowhere still visits its single vertex.
- **Single-step walk**: The support of a one-edge walk from `u` to `v` is `[u, v]`, a list of length 2.
- **Repeated vertices**: If a walk visits the same vertex multiple times (a non-path walk), that vertex appears multiple times in the support list. The support is not deduplicated.
- **Length relationship**: For any walk, `support.length = walk.length + 1`, where `walk.length` counts edges.
- **Membership**: Both the start vertex `u` and the end vertex `v` always appear in the support.

## Not to be confused with

- `G.Walk.edges`: Returns the list of edges traversed, not vertices visited; has length one less than `support`.
- `G.Walk.darts`: Returns the list of directed edge darts (pairs of adjacent vertices with adjacency proofs) rather than bare vertices.
- `G.Walk.getVert`: A function mapping an index to the vertex at that position in the walk, rather than returning the full list at once.