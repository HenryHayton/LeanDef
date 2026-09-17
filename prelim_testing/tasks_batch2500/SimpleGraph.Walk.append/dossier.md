## VTask.append

### Object

Given a simple graph `G` on a vertex type `V`, `VTask.append` produces the **concatenation** of two walks in `G` that share a common intermediate vertex. Specifically, if `p` is a walk from vertex `u` to vertex `v`, and `q` is a walk from vertex `v` to vertex `w`, then `VTask.append p q` is the walk from `u` to `w` obtained by first traversing `p` and then traversing `q`. This is the graph-walk analogue of list concatenation.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.append : {V : Type u} -> {G : SimpleGraph V} -> {u v w : V} -> G.Walk u v → G.Walk v w → G.Walk u w
<!-- PINNED-SIGNATURE:END -->


`{V : Type u} -> {G : SimpleGraph V} -> {u v w : V} -> G.Walk u v → G.Walk v w → G.Walk u w`

The implicit type `V` is the vertex type of the graph. The implicit argument `G` is the simple graph whose walks are being combined. The implicit vertices `u`, `v`, and `w` are the start, shared intermediate, and end vertices, respectively. The first explicit argument is the walk from `u` to `v` (the left segment). The second explicit argument is the walk from `v` to `w` (the right segment). The result is a walk from `u` to `w`.

### Conventions

Appending any walk `q` (from `v` to `w`) onto a nil walk (the trivial walk at `v`) simply returns `q` unchanged — the nil walk acts as a left identity for append. Appending a nil walk onto any walk `p` (from `u` to `v`) returns `p` unchanged — the nil walk also acts as a right identity (following from the recursive structure). Append is associative: given walks `p : u → v`, `q : v → w`, `r : w → x`, the walks `p.append (q.append r)` and `(p.append q).append r` are definitionally equal.

### Worked examples

- Claim: Appending a nil walk on the right to a walk `p : G.Walk u v` returns the same walk `p`. That is, for any graph `G`, vertices `u v`, and walk `p : G.Walk u v`, one has `p.append Walk.nil = p`.

- Claim: Appending a nil walk on the left to any walk `q : G.Walk v w` returns `q`. That is, `(Walk.nil).append q = q`.

- Claim: Append is associative: for walks `p : G.Walk u v`, `q : G.Walk v w`, `r : G.Walk w x`, the equation `p.append (q.append r) = (p.append q).append r` holds.

- Claim: If `p : G.Walk u v` is a single-edge walk (`cons h Walk.nil`) and `q : G.Walk v w` is any walk, then `(cons h Walk.nil).append q = cons h q`.

### Boundaries

- If either walk is the trivial nil walk (at the shared endpoint), the result equals the other walk; no edges are added or removed.
- The length of `p.append q` equals the sum of the lengths of `p` and `q`.
- The support (vertex sequence) of `p.append q` is the concatenation of the support of `p` with the support of `q`, with the shared vertex `v` appearing at the junction (once as the last vertex of `p`'s support and once as the first vertex of `q`'s support).
- The edge set of `p.append q` is the union of the edge sets of `p` and `q`.
- If both `p` and `q` are paths (no repeated vertices), `p.append q` need not be a path — the shared vertex `v` might also appear elsewhere, or the two walks may visit a common vertex. Path status of the concatenation does not follow automatically.
- If `p.append q` is a path, then both `p` and `q` individually are paths (the path property is inherited by each segment).
- Similarly, if `p.append q` is a trail (no repeated edges), both `p` and `q` are individually trails.

### Not to be confused with

- `G.Walk.cons`: prepends a single edge to a walk, rather than joining two whole walks end-to-end.
- `G.Walk.concat`: appends a single edge at the end of a walk, rather than joining two whole walks.
- `G.Walk.reverse`: reverses the direction of a walk, which is a different kind of structural transformation.