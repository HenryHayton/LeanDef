## Object

`VTask.cycleBypass` takes a closed walk (a walk from a vertex `v` back to itself) in a simple graph and returns a shorter or equal closed walk from `v` to `v` that has no repeated vertices **except** for the shared start/end vertex `v`. It is the analogue of `Walk.bypass` (which eliminates all repeated vertices, potentially collapsing a closed walk to the empty walk) but adapted for closed walks: the first edge of the walk is always retained, and `Walk.bypass` is applied only to the tail, so the result is still a non-trivial closed walk whenever the input is.

Intuitively, given any closed walk that visits some vertices more than once, `VTask.cycleBypass` finds a cycle (or the empty walk, if the input is already empty) embedded within it by removing detours.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.cycleBypass : {V : Type u} -> {G : SimpleGraph V} -> {v : V} -> [DecidableEq V] -> G.Walk v v → G.Walk v v
<!-- PINNED-SIGNATURE:END -->


VTask.cycleBypass : {V : Type u} -> {G : SimpleGraph V} -> {v : V} -> [DecidableEq V] -> G.Walk v v → G.Walk v v

- `V` is the type of vertices of the graph (implicit).
- `G` is the simple graph over `V` (implicit).
- `v` is the base vertex: both the start and end of the input closed walk (implicit).
- The `DecidableEq V` instance (synthesised automatically) is needed to decide vertex equality when removing repeated vertices.
- The explicit argument is the closed walk from `v` to `v` that is to be simplified.

## Conventions

The empty walk (`Walk.nil`) is mapped to itself: `VTask.cycleBypass` of the empty closed walk at `v` is again the empty closed walk at `v`. There is no junk value convention beyond this; the function is total on all closed walks.

## Worked examples

- Claim: For the empty closed walk at any vertex `v`, `VTask.cycleBypass Walk.nil = Walk.nil`.

- Claim: If `w : G.Walk v v` is a non-empty circuit (closed trail), then `w.cycleBypass` is a cycle — that is, a closed walk whose support has no repeated vertices except the base vertex.

- Claim: For any closed walk `w : G.Walk v v`, the edges of `VTask.cycleBypass w` form a sublist of the edges of `w`.

- Claim: For any closed walk `w : G.Walk v v`, the length of `VTask.cycleBypass w` is at most the length of `w`.

## Boundaries

- **Empty walk**: `VTask.cycleBypass Walk.nil = Walk.nil`. The function returns the empty walk unchanged; it does not raise an error or produce an unexpected result.
- **Single-edge loop walk** (a walk `cons h nil` traversing one edge from `v` back to `v`): the tail after removing the first edge is `nil`, and `Walk.bypass nil = nil`, so the result is `cons h nil` — identical to the input.
- **Already-a-cycle input**: if `w` is already a cycle (no repeated interior vertices), `VTask.cycleBypass w = w`, because `Walk.bypass` is the identity on paths.
- **Circuits** (closed trails, not necessarily cycle-shaped): a circuit that is not the empty walk is guaranteed to produce a cycle under `VTask.cycleBypass`.
- **Non-trail closed walks** (edges repeated): the output is still a valid closed walk but may not be a cycle if the input is not a trail.

## Not to be confused with

- `Walk.bypass`: the plain bypass for general walks; applied to a closed walk it may return the empty walk, losing the closed structure entirely.
- `Walk.IsCycle`: a *predicate* asserting that a closed walk is a cycle; `VTask.cycleBypass` *produces* a walk that satisfies this predicate (when the input is a non-empty circuit or non-nil trail).
- `Walk.toPath`: projects a walk to a simple path between two (possibly different) endpoints, which does not preserve the closed structure needed for cycles.
