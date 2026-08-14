## Object

Given a walk in a simple graph from vertex `u` to vertex `v`, `VTask.getVert` returns the vertex visited at position `n` along that walk. The walk visits vertices at positions `0, 1, 2, …, p.length`, where position `0` is the starting vertex `u` and position `p.length` is the ending vertex `v`. If `n` exceeds the walk's length, the function returns the walk's endpoint `v` (clamping at the end).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.getVert : {V : Type u} -> {G : SimpleGraph V} -> {u v : V} -> G.Walk u v → ℕ → V
<!-- PINNED-SIGNATURE:END -->


`VTask.getVert : {V : Type u} -> {G : SimpleGraph V} -> {u v : V} -> G.Walk u v → ℕ → V`

The implicit argument `V` is the type of vertices. The implicit argument `G` is the simple graph in question. The implicit arguments `u` and `v` are the start and end vertices of the walk, respectively. The first explicit argument is the walk itself, a path of edges in `G` from `u` to `v`. The second explicit argument `n : ℕ` is the position index along the walk whose corresponding vertex is to be retrieved.

## Conventions

When the index `n` is greater than or equal to the length of the walk, the function returns the walk's endpoint `v` (the terminal vertex), rather than producing an error or a default value.

## Worked examples

- Claim: For the trivial (nil) walk at a vertex `u`, `VTask.getVert nil n = u` for every `n`.

- Claim: For a single-edge walk `cons h nil` of length 1, `VTask.getVert (cons h nil) 0 = u` (the starting vertex).

- Claim: For a single-edge walk `cons h nil` of length 1, `VTask.getVert (cons h nil) 1 = v` (the ending vertex).

- Claim: For a single-edge walk `cons h nil` of length 1, `VTask.getVert (cons h nil) 5 = v` (out-of-range index clamps to endpoint).

- Claim: For any walk `p : G.Walk u v` with `i < p.length`, the vertices `VTask.getVert p i` and `VTask.getVert p (i + 1)` are adjacent in `G`.

## Boundaries

- At `n = 0`, the result is always the starting vertex `u`, regardless of the walk.
- At `n = p.length`, the result is the ending vertex `v`.
- For any `n ≥ p.length`, the result is the ending vertex `v` (clamped).
- The nil walk (of length 0) always returns `u` for every `n`.
- Consecutive vertices in the walk (positions `i` and `i+1` for `i < p.length`) are guaranteed to be adjacent in `G`.
- On a path (walk with no repeated vertices), `VTask.getVert` is injective on the index set `{i | i ≤ p.length}`.
- On a cycle, `VTask.getVert` is injective on `{i | 1 ≤ i ∧ i ≤ p.length}` and on `{i | i ≤ p.length - 1}`.

## Not to be confused with

- `G.Walk.support`: the full list of vertices visited by the walk (of length `p.length + 1`), rather than indexed vertex lookup.
- `G.Walk.length`: returns the number of edges in the walk, not a vertex at a position.
- `List.get` on the support list: equivalent in content but accessed via a `Fin` index with proof, rather than a natural number with out-of-bounds clamping.