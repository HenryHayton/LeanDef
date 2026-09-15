## VTask.take

### Object

`VTask.take p n` is the prefix walk obtained by following the first `n` darts (directed edges) of the walk `p`. It starts at the same vertex as `p` and ends at the `n`-th vertex along `p` (as given by `getVert n`). If `n` is zero the result is the trivial (nil) walk at the starting vertex; if `n` is at least as large as the length of `p` the result is `p` itself.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.take : {V : Type u} -> {G : SimpleGraph V} -> {u v : V} -> (p : G.Walk u v) -> (n : ℕ) -> G.Walk u (p.getVert n)
<!-- PINNED-SIGNATURE:END -->


`VTask.take : {V : Type u} -> {G : SimpleGraph V} -> {u v : V} -> (p : G.Walk u v) -> (n : ℕ) -> G.Walk u (p.getVert n)`

The implicit argument `V` is the vertex type; `G` is the simple graph; `u` and `v` are the start and end vertices of the input walk. The first explicit argument `p` is the walk from which the prefix is extracted. The second explicit argument `n` is the number of darts (edges) to keep from the beginning of `p`.

### Conventions

When `n = 0` the result is the nil walk at vertex `u`, encoded as a walk of length zero; no darts are traversed. When `n` is strictly greater than the length of `p`, taking `n` steps from `p` still yields exactly `p` (since there are no further darts to take), so the result equals `p` and ends at `v`.

### Worked examples

- Claim: For any walk `p`, `(VTask.take p 0)` has length 0.

- Claim: For a walk `p` of length `L`, `(VTask.take p n).length = min n L`.

- Claim: The dart list of `VTask.take p n` equals the first `n` elements of the dart list of `p`.

- Claim: If `p : G.Walk u v` is a path and `n : ℕ`, then `VTask.take p n` is also a path.

- Claim: `VTask.take p n` is a sub-walk of `p` for every `n`.

### Boundaries

- **`n = 0`**: The result is the nil walk at `u`; it has no darts, no edges, and its support is the singleton `[u]`.
- **`n ≥ p.length`**: Taking more darts than `p` has simply returns `p` (length-saturates at `p.length`); the end vertex is `v`, the same as `p`'s end vertex.
- **`p` is nil**: Regardless of `n`, the result is the nil walk at `u` (there are no darts to take).
- **Length formula**: `(VTask.take p n).length = min n p.length` — the length is exactly the smaller of `n` and the walk's length.
- **Path preservation**: Taking a prefix of a path yields a path; taking a prefix of a prefix of a path still yields a path.

### Not to be confused with

- `SimpleGraph.Walk.takeUntil`: stops at the first occurrence of a *specified vertex* in the walk's support, rather than after a fixed number of darts.
- `SimpleGraph.Walk.dropUntil`: the complementary operation that *discards* the prefix up to a vertex, returning the suffix.
- `List.take`: the analogous operation on plain lists; `VTask.take` on a walk corresponds to `List.take` on the walk's dart list, but operates at the level of typed graph walks.