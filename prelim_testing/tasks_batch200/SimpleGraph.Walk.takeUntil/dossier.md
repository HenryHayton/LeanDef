## VTask.takeUntil

### Object

Given a walk in a simple graph from vertex `v` to vertex `w`, and a vertex `u` that appears somewhere on that walk's support (the ordered list of vertices visited), `takeUntil` extracts the initial segment of the walk that starts at `v` and ends exactly at the *first* occurrence of `u`. The result is a walk from `v` to `u` whose edges and vertices are a prefix of those of the original walk.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.takeUntil : {V : Type u} -> {G : SimpleGraph V} -> [DecidableEq V] -> {v w : V} -> (p : G.Walk v w) -> (u : V) -> u ∈ p.support → G.Walk v u
<!-- PINNED-SIGNATURE:END -->


```
VTask.takeUntil : {V : Type u} -> {G : SimpleGraph V} -> [DecidableEq V] -> {v w : V} -> (p : G.Walk v w) -> (u : V) -> u ∈ p.support → G.Walk v u
```

The implicit type `V` is the vertex type of the graph, and `G` is the ambient simple graph. The `DecidableEq V` instance is needed to compare vertices for equality during traversal. The implicit vertices `v` and `w` are the start and end of the given walk. The argument `p` is the walk from `v` to `w` from which the prefix is extracted. The argument `u` is the target vertex at which to stop. The final argument is a proof that `u` appears in the support of `p`, ensuring the operation is well-defined.

### Conventions

When `u` equals the starting vertex `v` of the walk, `takeUntil` returns the trivial (nil) walk at `v`, because the walk reaches `u` immediately without traversing any edges. There are no junk-value conventions because the membership proof ensures `u` is always present in the support.

### Worked examples

- Claim: Taking until the start vertex of any walk yields the nil walk. For a walk `p : G.Walk v w`, `p.takeUntil v p.start_mem_support` equals `Walk.nil`.

- Claim: For a path of the form `cons h₁ (cons h₂ nil)` going `v → v₁ → w`, taking until `v₁` (the middle vertex) yields a single-edge walk `cons h₁ nil` from `v` to `v₁`.

- Claim: Taking until the end vertex `w` of a walk `p : G.Walk v w` (when `w ∈ p.support`) yields a walk with the same length as `p` and the same edges.

- Claim: If `p` is a path (no repeated vertices) and `u ∈ p.support`, then `p.takeUntil u h` is also a path.

- Claim: If `p` is a trail (no repeated edges) and `u ∈ p.support`, then `p.takeUntil u h` is also a trail.

- Claim: The darts of `p.takeUntil u h` form a prefix of the dart list of `p`.

### Boundaries

- **Start vertex (`u = v`):** `takeUntil` returns `Walk.nil`, a walk of length 0 with no edges and support `[v]`.
- **End vertex (`u = w`):** `takeUntil` returns the full walk unchanged (up to definitional equality), since the first occurrence of `w` in the support is precisely at the end of the walk when no vertex is repeated before it.
- **Repeated occurrences of `u`:** If `u` appears multiple times in the support, `takeUntil` stops at the *first* occurrence, giving the shortest prefix ending at `u`.
- **Nil walk:** The nil walk `Walk.nil` at vertex `v` has support `[v]`, so the only valid `u` is `v` itself, and the result is `Walk.nil`.
- **The membership proof is required:** The function is not defined for vertices outside the walk's support; the proof argument enforces this at the type level.

### Not to be confused with

- `Walk.dropUntil`: the complementary operation that returns the *suffix* of the walk starting at `u` and continuing to `w`; together with `takeUntil` it decomposes the walk at `u`.
- `Walk.take`: if such a function existed taking an index rather than a vertex, it would truncate by position; `takeUntil` instead stops at a named vertex.
- `Walk.IsSubwalk`: a predicate asserting one walk is a subwalk of another; `takeUntil` *produces* such a subwalk, which `isSubwalk_takeUntil` confirms is indeed a subwalk of `p`.