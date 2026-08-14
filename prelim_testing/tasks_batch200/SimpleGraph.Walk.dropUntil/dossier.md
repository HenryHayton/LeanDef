## VTask.dropUntil

### Object

`VTask.dropUntil` extracts the **suffix** of a walk in a simple graph starting at a specified vertex. Given a walk `p` from vertex `v` to vertex `w`, and a vertex `u` that appears somewhere in the support (vertex sequence) of `p`, the function returns the sub-walk that begins at `u` and continues to `w`, discarding all edges and vertices that appear strictly before the first occurrence of `u`. The result is a walk in the same graph whose starting vertex is exactly `u` and whose ending vertex is `w`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.dropUntil : {V : Type u} -> {G : SimpleGraph V} -> [DecidableEq V] -> {v w : V} -> (p : G.Walk v w) -> (u : V) -> u ∈ p.support → G.Walk u w
<!-- PINNED-SIGNATURE:END -->


`VTask.dropUntil : {V : Type u} -> {G : SimpleGraph V} -> [DecidableEq V] -> {v w : V} -> (p : G.Walk v w) -> (u : V) -> u ∈ p.support → G.Walk u w`

- `V` is the type of vertices of the graph (implicit).
- `G` is the simple graph over `V` (implicit).
- The `DecidableEq V` instance is needed to compare vertices for equality during traversal (implicit instance).
- `v` and `w` are the start and end vertices of the original walk (implicit).
- `p` is the walk from `v` to `w` whose prefix is to be dropped.
- `u` is the vertex at which the returned walk should begin.
- The final argument is a proof that `u` appears in the support of `p`, ensuring the operation is well-defined.

### Conventions

When `u` is the very first vertex of the walk (i.e., `u = v`), no edges are dropped and `VTask.dropUntil p u h` returns the entire original walk `p`. This is the degenerate suffix case, not a junk value.

### Worked examples

- Claim: For the trivial (nil) walk at vertex `v`, the only vertex in its support is `v` itself, and `VTask.dropUntil (Walk.nil) v h` equals `Walk.nil` (the same walk).

- Claim: If `p` is a walk `v → a → b → w` and `u = a`, then `VTask.dropUntil p a h` is the walk `a → b → w`, containing all edges from `a` onward.

- Claim: Appending the result of `takeUntil p u h` with `dropUntil p u h` reconstructs the original walk `p` exactly (the `take_spec` identity).

- Claim: The support of `VTask.dropUntil p u h` is a suffix of the support of `p`.

- Claim: The length of `VTask.dropUntil p u h` is at most the length of `p`.

- Claim: If `p` is a path (no repeated vertices), then `VTask.dropUntil p u h` is also a path.

### Boundaries

- **`u = v` (drop nothing):** When the target vertex `u` equals the walk's starting vertex `v`, the entire walk is returned unchanged. No edges are removed.
- **`u = w` (drop everything but the end):** When `u` is the terminal vertex `w`, the result is a nil walk at `w`.
- **First occurrence:** If `u` appears multiple times in the support of `p` (possible in a non-simple walk), `dropUntil` uses the **first** occurrence of `u` and returns the suffix from that point.
- **Length:** The result has length strictly less than `p` when `u ≠ v`, and equal length when `u = v`.
- **Edge/dart sets:** The edges and darts of the result form a suffix of those of `p` and are a subset of `p`'s edges and darts.
- **Trails and paths:** If `p` is a trail or a path, the sub-walk returned by `dropUntil` inherits that property.

### Not to be confused with

- `Walk.takeUntil`: The complementary operation that retains the **prefix** of the walk up to and including `u`, discarding everything after; together with `dropUntil` it decomposes `p` at `u`.
- `Walk.support`: The list of all vertices visited by a walk; `dropUntil` uses membership in this list as its precondition but is not itself a support operation.
- `List.dropWhile` / `List.drop`: Generic list operations on the vertex sequence alone; `dropUntil` operates on the walk structure, preserving graph-adjacency data, not merely the list of vertices.