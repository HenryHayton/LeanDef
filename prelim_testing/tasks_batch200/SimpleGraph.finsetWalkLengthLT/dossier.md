## Object

Given a locally finite simple graph `G` on a vertex type `V`, `VTask.finsetWalkLengthLT G n u v` is the finite set of all walks in `G` that start at vertex `u`, end at vertex `v`, and whose length (number of edges) is strictly less than `n`. It packages exactly those walks `p : G.Walk u v` satisfying `p.length < n` into a `Finset`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.finsetWalkLengthLT : {V : Type u} -> (G : SimpleGraph V) -> [DecidableEq V] -> [G.LocallyFinite] -> (n : ℕ) -> (u v : V) -> Finset (G.Walk u v)
<!-- PINNED-SIGNATURE:END -->


`VTask.finsetWalkLengthLT : {V : Type u} -> (G : SimpleGraph V) -> [DecidableEq V] -> [G.LocallyFinite] -> (n : ℕ) -> (u v : V) -> Finset (G.Walk u v)`

The implicit type `V` is the vertex type of the graph. `G` is the simple graph on `V`. The `DecidableEq V` instance enables equality comparisons between vertices. The `G.LocallyFinite` instance guarantees that each vertex has only finitely many neighbours, which is what makes it possible to enumerate walks up to a given length as a genuine finite set. `n` is the strict upper bound on walk length. `u` is the starting vertex and `v` is the ending vertex of all walks collected.

## Conventions

When `n = 0`, there are no walks of length strictly less than `0`, so the resulting `Finset` is empty for every choice of `u` and `v`.

## Worked examples

- Claim: A walk `p` from `u` to `v` belongs to `VTask.finsetWalkLengthLT G n u v` if and only if its length is strictly less than `n`.

- Claim: For any graph `G`, vertices `u` and `v`, and any `n`, `VTask.finsetWalkLengthLT G n u v` when coerced to a set equals `{p : G.Walk u v | p.length < n}`.

- Claim: For `n = 0`, `VTask.finsetWalkLengthLT G 0 u v = ∅` for all `u v`, since no natural number is less than `0`.

- Claim: For `n = 1`, `VTask.finsetWalkLengthLT G 1 u v` contains exactly the walks of length `0`, which exist only when `u = v` (the single nil walk).

## Boundaries

- When `n = 0`: the range over which the disjoint union is taken is empty, so the result is the empty `Finset` regardless of `u` and `v`.
- When `n = 1`: only walks of length exactly `0` qualify. A walk of length `0` from `u` to `v` exists precisely when `u = v`; if `u ≠ v`, the set is empty.
- The bound `n` is a strict upper bound, not an inclusive one; walks of length exactly `n` are excluded.
- The definition is valid (produces a genuine `Finset`) only under the `LocallyFinite` hypothesis; without it, the set of walks up to a given length need not be finite.

## Not to be confused with

- `SimpleGraph.finsetWalkLength`: collects walks of length *exactly* `n`, not strictly less than `n`.
- `SimpleGraph.Walk`: the type of individual walks; `VTask.finsetWalkLengthLT` produces a `Finset` of such walks, not a single walk.
- A set of paths (non-repeating walks): `VTask.finsetWalkLengthLT` collects all walks, including those that revisit vertices or edges.