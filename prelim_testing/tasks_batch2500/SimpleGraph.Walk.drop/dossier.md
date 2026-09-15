## Object

`VTask.drop p n` is the walk obtained by discarding the first `n` darts (directed edges) of the walk `p`. The result starts at the `n`-th vertex of `p` (where vertices are numbered from 0) and ends at the same endpoint as `p`. If `n` is at least as large as the number of darts in `p`, the result is a trivial nil walk sitting at `p`'s terminal vertex.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.drop : {V : Type u} -> {G : SimpleGraph V} -> {u v : V} -> (p : G.Walk u v) -> (n : ℕ) -> G.Walk (p.getVert n) v
<!-- PINNED-SIGNATURE:END -->


`VTask.drop : {V : Type u} -> {G : SimpleGraph V} -> {u v : V} -> (p : G.Walk u v) -> (n : ℕ) -> G.Walk (p.getVert n) v`

The implicit type `V` is the vertex type; `G` is the simple graph on `V`; `u` and `v` are the start and end vertices of the walk. The explicit argument `p` is the walk to be truncated; `n` is the number of darts to remove from the front of `p`. The return type is a walk from the `n`-th vertex of `p` to `v`.

## Conventions

When `n` equals zero, the dropped walk is the entire original walk (starting at `p.getVert 0 = u`), so no darts are removed and the result is definitionally equal to `p` up to the identification `p.getVert 0 = u`. When `n` exceeds the length of `p`, `p.getVert n` is defined to be the final vertex `v`, so `VTask.drop p n` is a nil walk at `v`.

## Worked examples

- Claim: Dropping 0 darts from any walk returns a walk equal (up to vertex identification) to the original walk, starting at `p.getVert 0`.

- Claim: Dropping all `n` darts from a walk of length `n` yields a nil walk at the terminal vertex.

- Claim: If `p` is a path, then `VTask.drop p n` is also a path for every `n : ℕ`.

- Claim: For a cons walk `cons h q`, dropping `n+1` darts equals dropping `n` darts from the tail `q`, i.e., `(cons h q).drop (n+1) = q.drop n` (up to the appropriate vertex identification).

## Boundaries

- **`n = 0`**: No darts are removed; the result is the whole walk (with a type-cast adjusting the start vertex to `p.getVert 0`, which equals `u`).
- **`n ≥ length p`**: `p.getVert n` saturates to the final vertex `v`, and the drop produces a nil walk at `v`.
- **Nil walk, any `n`**: Dropping any number of darts from a nil walk yields a nil walk at the same vertex (since a nil walk has no darts and its `getVert n` is always `v`).
- **Path preservation**: If `p` is a path, then `VTask.drop p n` is a path for every `n`, and more generally if `VTask.drop p k` is a path and `k ≤ n`, then `VTask.drop p n` is also a path.

## Not to be confused with

- `SimpleGraph.Walk.dropLast`: removes the *last* dart of a walk (from the end), rather than the first `n` darts from the front.
- `SimpleGraph.Walk.dropUntil`: drops a prefix up to a specified *vertex* appearing in the support, not a specified count of darts.
- `SimpleGraph.Walk.take` / `SimpleGraph.Walk.takeUntil`: takes the *first* portion of a walk, which is the complement operation to `drop`.