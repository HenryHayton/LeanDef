## VTask.darts

### Object

Given a walk in a simple graph, `VTask.darts` returns the ordered list of *darts* (directed edges) traversed by that walk. Each dart records both the oriented edge (an ordered pair of adjacent vertices) and the adjacency proof. The list is in the same order as the walk itself: the first dart corresponds to the first step taken, and so on.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.darts : {V : Type u} -> {G : SimpleGraph V} -> {u v : V} -> G.Walk u v → List G.Dart
<!-- PINNED-SIGNATURE:END -->


```
VTask.darts : {V : Type u} -> {G : SimpleGraph V} -> {u v : V} -> G.Walk u v → List G.Dart
```

The implicit argument `V` is the vertex type of the graph. The implicit argument `G` is the simple graph over `V`. The implicit arguments `u` and `v` are the start and end vertices of the walk, respectively. The explicit argument is the walk itself, whose darts are to be extracted.

### Conventions

The `darts` of a nil (empty, length-zero) walk at any vertex is the empty list — there are no steps, hence no darts.

### Worked examples

- Claim: The darts of a nil walk is the empty list.

- Claim: If `p` is a walk from `v` to `w` and `h : G.Adj u v`, then `VTask.darts (Walk.cons h p) = ⟨(u, v), h⟩ :: VTask.darts p`.

- Claim: For any walk `p` from `u` to `v` and extension walk `p'` from `v` to `w`, `VTask.darts (p.append p') = VTask.darts p ++ VTask.darts p'`.

- Claim: The dart list of a walk uniquely determines the walk — `VTask.darts` is injective on walks with the same start and end vertices.

- Claim: For any walk `p`, the dart list `VTask.darts p` forms a chain under dart-adjacency: consecutive darts in the list share a vertex (the head of one equals the tail of the previous).

### Boundaries

- A nil walk (a walk of length zero, staying at a single vertex) produces an empty dart list.
- A walk of length one (a single edge from `u` to `v`) produces a dart list with exactly one element, the dart `⟨(u, v), h⟩`.
- The length of the dart list equals the number of edges in the walk (the walk's length).
- The dart list of a reversed walk consists of the element-wise symmetric darts of the original list, themselves reversed.
- A dart `d` belongs to `VTask.darts p` if and only if the two-element list `[d.fst, d.snd]` appears as a contiguous sublist (infix) of the walk's support (vertex list).
- If a walk `p₁` is a subwalk of `p₂`, then `VTask.darts p₁` is a subset of `VTask.darts p₂`; moreover, `VTask.darts p₁` is an infix (contiguous sublist) of `VTask.darts p₂`.

### Not to be confused with

- `Walk.edges`: returns the list of undirected edges (pairs of vertices without orientation or adjacency proof), not directed darts.
- `Walk.support`: returns the list of *vertices* visited by the walk, not the directed edges between them.
- `G.Dart`: the type of a single directed edge with adjacency proof; `VTask.darts` produces a *list* of such darts from a whole walk.