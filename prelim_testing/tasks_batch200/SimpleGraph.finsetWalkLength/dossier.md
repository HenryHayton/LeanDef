## Object

`VTask.finsetWalkLength G n u v` is the finite set (a `Finset`) of all walks of exactly length `n` from vertex `u` to vertex `v` in the simple graph `G`. A walk of length `n` is a sequence of `n` edges traversed one after another, possibly revisiting vertices or edges. The result collects every such walk as an explicit, enumerable finite collection.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.finsetWalkLength : {V : Type u} -> (G : SimpleGraph V) -> [DecidableEq V] -> [G.LocallyFinite] -> (n : ℕ) -> (u v : V) -> Finset (G.Walk u v)
<!-- PINNED-SIGNATURE:END -->


`VTask.finsetWalkLength : {V : Type u} -> (G : SimpleGraph V) -> [DecidableEq V] -> [G.LocallyFinite] -> (n : ℕ) -> (u v : V) -> Finset (G.Walk u v)`

`G` is the simple graph whose walks are being enumerated. The `DecidableEq V` instance provides decidable equality on the vertex type, needed to compare vertices. The `G.LocallyFinite` instance asserts that every vertex of `G` has only finitely many neighbours, which is necessary to enumerate walks recursively. `n` is the required length (number of edges) of every walk in the resulting set. `u` is the starting vertex and `v` is the ending vertex of all walks collected.

## Conventions

When `n = 0` and `u ≠ v`, no walk of length zero can connect distinct vertices, so the returned finset is empty. When `n = 0` and `u = v`, the only length-zero walk is the trivial (nil) walk staying at `u`, so the finset contains exactly that one walk.

## Worked examples

- Claim: A walk `p` belongs to `VTask.finsetWalkLength G n u v` if and only if its length equals `n`.

- Claim: For any locally finite simple graph `G` and vertices `u`, `v`, the coercion of `VTask.finsetWalkLength G n u v` to a `Set` equals `{p : G.Walk u v | p.length = n}`.

- Claim: When `u = v`, `VTask.finsetWalkLength G 0 u u` contains exactly the nil walk (so it has cardinality 1).

- Claim: When `u ≠ v`, `VTask.finsetWalkLength G 0 u v` is empty.

- Claim: The cardinality of `{p : G.Walk u v | p.length = n}` as a `Fintype` equals the size of `VTask.finsetWalkLength G n u v`.

## Boundaries

- At `n = 0` with `u = v`: the finset contains exactly one element, the nil walk `Walk.nil` at `u`.
- At `n = 0` with `u ≠ v`: the finset is empty, since a walk of length zero cannot change vertices.
- At `n = 1`: the finset contains one walk for each edge between `u` and `v`; for a simple graph this is either empty (if `u` and `v` are not adjacent) or a singleton (if they are adjacent, since there is only one edge between any two vertices in a simple graph).
- The `LocallyFinite` hypothesis is essential: without it the neighbour sets at each step would be infinite and the finset could not be formed.
- Walks in this finset may revisit vertices and edges; no simplicity or path condition is imposed.

## Not to be confused with

- `SimpleGraph.Walk` itself: that is the type of a single walk (of any length) in a graph, not a collection of walks of a fixed length.
- `VTask.finsetWalkLengthLT G n u v`: the analogous finset collecting all walks of length *strictly less than* `n`, rather than exactly `n`.
- `SimpleGraph.Path`: a walk with no repeated vertices; `VTask.finsetWalkLength` imposes no such restriction and may include walks that revisit vertices.
