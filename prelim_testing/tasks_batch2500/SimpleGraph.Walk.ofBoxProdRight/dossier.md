## Object

Given a walk on the box product (categorical square product) `G □ H` of two simple graphs, `VTask.ofBoxProdRight` projects that walk down to a walk on the second factor graph `H`. At each step of the original walk, either the first coordinate changes (a "G-move") or the second coordinate changes (an "H-move"). The projection retains only the H-moves, discarding all G-moves, thereby producing a walk on `H` between the second coordinates of the start and end vertices.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofBoxProdRight : {α : Type u_1} -> {β : Type u_2} -> {G : SimpleGraph α} -> {H : SimpleGraph β} -> [DecidableEq α] -> [DecidableRel H.Adj] -> {x y : α × β} -> (G □ H).Walk x y → H.Walk x.2 y.2
<!-- PINNED-SIGNATURE:END -->


`VTask.ofBoxProdRight : {α : Type u_1} -> {β : Type u_2} -> {G : SimpleGraph α} -> {H : SimpleGraph β} -> [DecidableEq α] -> [DecidableRel H.Adj] -> {x y : α × β} -> (G □ H).Walk x y → H.Walk x.2 y.2`

- `α` and `β` are the vertex types of the two factor graphs.
- `G` is the simple graph on `α` forming the left (first) factor of the box product.
- `H` is the simple graph on `β` forming the right (second) factor of the box product.
- The `DecidableEq α` instance is required to determine, at each step, whether a given edge of the box product moves in the G-direction or the H-direction.
- The `DecidableRel H.Adj` instance is needed to construct adjacency evidence in `H` for the retained H-moves.
- `x` and `y` are vertices of `α × β`, the starting and ending points of the walk in the box product.
- The final argument is the walk in `G □ H` from `x` to `y` to be projected.

The result is a walk in `H` from `x.2` (the second coordinate of the start) to `y.2` (the second coordinate of the end).

## Conventions

When a step in the box product walk moves only in the G-direction (i.e., the second coordinate is unchanged), that step contributes nothing to the projected walk — it is silently dropped, and the walk in `H` continues from the same vertex. This means the length of the projected walk may be strictly less than the original walk's length.

## Worked examples

- Claim: Projecting the empty (nil) walk on `G □ H` at a vertex `(a, b)` yields the empty walk on `H` at `b`.

- Claim: For any walk `w` on `H` and a vertex `a : α`, the projection `(w.boxProdRight G a).ofBoxProdRight` recovers exactly `w` — the round-trip through the box product and back is the identity on `H`-walks.

- Claim: For a walk `w` on `G □ H` with endpoints `(a₁, b₁)` and `(a₂, b₂)`, the total length of `w` equals the length of its left projection plus the length of its right projection: `w.length = w.ofBoxProdLeft.length + w.ofBoxProdRight.length`.

## Boundaries

- **Nil walk:** The projection of the nil walk (a walk of length zero at a single vertex) is the nil walk at the second coordinate. No adjacency decisions need to be made.
- **All G-moves:** If every step of the walk in `G □ H` moves only the first coordinate, the projected walk has length zero (a nil walk at the single second coordinate, which must therefore be the same throughout).
- **All H-moves:** If every step moves only the second coordinate, the projected walk has the same length as the original and retains all edges.
- **Mixed walks:** The projected walk's length is the number of H-direction steps in the original walk.
- The second coordinates of the endpoints are correctly tracked: the result always ends at `y.2`, even after discarding G-moves, because G-moves do not change the second coordinate.

## Not to be confused with

- `SimpleGraph.Walk.ofBoxProdLeft`: the analogous projection to the *first* factor graph `G`, which discards H-moves instead of G-moves.
- `SimpleGraph.Walk.boxProdRight`: the *embedding* of a walk on `H` into the box product (the reverse direction — lifting, not projecting).
- `SimpleGraph.Walk.map`: a general graph homomorphism applied to a walk, which does not selectively drop steps but transforms every step via a fixed map.