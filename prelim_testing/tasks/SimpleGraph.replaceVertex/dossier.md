## Object

Given a simple graph `G` on vertex type `V` and two vertices `s` and `t`, `VTask.replaceVertex G s t` is the simple graph on the same vertex type obtained by *replacing* `t`'s neighbourhood with a copy of `s`'s neighbourhood. More precisely, vertex `t` is now adjacent exactly to those vertices that `s` was adjacent to in `G` (excluding `t` itself, since simple graphs have no loops), while all other adjacencies among vertices different from `t` remain exactly as in `G`. In particular, the edge `s–t`, if it existed in `G`, is removed in the result.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.replaceVertex : {V : Type u_1} -> (G : SimpleGraph V) -> (s t : V) -> [DecidableEq V] -> SimpleGraph V
<!-- PINNED-SIGNATURE:END -->


`VTask.replaceVertex : {V : Type u_1} -> (G : SimpleGraph V) -> (s t : V) -> [DecidableEq V] -> SimpleGraph V`

- `V` is the (implicit) vertex type of the graph.
- `G` is the base simple graph whose adjacency structure is being modified.
- `s` is the *source* vertex whose neighbourhood is donated to `t`.
- `t` is the *target* vertex whose neighbourhood is completely replaced.
- The `DecidableEq V` instance is needed to decide equality of vertices in the adjacency predicate.

## Conventions

The result is a simple graph, so `t` is never adjacent to itself in `VTask.replaceVertex G s t`, even if one imagined "copying" a loop from `s` (there are no loops in simple graphs). The edge `s–t` is absent from the result regardless of whether it was present in `G`; this is a direct consequence of the no-loop and no-s–t-adjacency rules baked into the construction.

## Worked examples

- Claim: In the complete graph `K₃` on `{0,1,2}` (all pairs adjacent), replacing vertex `2`'s neighbours with vertex `0`'s neighbours yields a graph where `2` is adjacent to `1` but NOT to `0` (because the `s`–`t` = `0`–`2` edge is removed).

- Claim: If `G` is the path graph `0–1–2` (so `0` adj `1`, `1` adj `2`, `0` not adj `2`), then `VTask.replaceVertex G 0 2` has `2` adjacent to `1` (copying `0`'s neighbour `1` onto `2`) and NOT adjacent to `0` (the `s`–`t` edge is suppressed), giving a triangle minus the `0–2` edge, i.e., effectively the same path `0–1–2` but now also with `1–2`; vertices `0` and `1` retain their original adjacency.

- Claim: For any graph `G` and any vertices `s`, `t`, the vertex `t` is never adjacent to itself in `VTask.replaceVertex G s t`.

- Claim: For any graph `G` and any vertices `s`, `t`, `s` and `t` are not adjacent in `VTask.replaceVertex G s t`.

- Claim: If `v ≠ t` and `w ≠ t`, then `(VTask.replaceVertex G s t).Adj v w ↔ G.Adj v w`; edges not touching `t` are unchanged.

## Boundaries

- When `s = t`: the operation replaces `t`'s neighbourhood with `t`'s own neighbourhood, but then removes the `s–t = t–t` self-loop (which was already absent), effectively leaving the graph unchanged.
- When `t` is an isolated vertex in `G`: the result gives `t` exactly the same neighbours as `s`.
- When `s` is an isolated vertex in `G`: the result makes `t` isolated (it loses all its neighbours and gains none).
- The vertex set is unchanged; no vertices are added or removed.
- All edges not incident to `t` are preserved exactly.

## Not to be confused with

- `SimpleGraph.map` / `SimpleGraph.comap`: these reindex the vertex type by a function, rather than surgically modifying one vertex's neighbourhood.
- Vertex contraction: contracting `s` and `t` merges them into a single vertex and takes the union of neighbourhoods, whereas `VTask.replaceVertex` keeps both vertices but replaces `t`'s neighbourhood entirely with `s`'s.
- `SimpleGraph.deleteVerts`: this removes vertices from the graph entirely, whereas `VTask.replaceVertex` keeps all vertices.