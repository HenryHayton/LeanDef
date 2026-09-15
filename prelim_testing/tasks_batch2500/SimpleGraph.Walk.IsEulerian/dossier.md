## VTask.IsEulerian

### Object

`VTask.IsEulerian p` is the predicate asserting that the walk `p` in a simple graph is an **Eulerian trail** (also called an Eulerian path): a walk that traverses every edge of the graph exactly once. Such a walk is automatically a trail (no edge is repeated), and when its start and end vertices coincide it becomes an Eulerian circuit.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsEulerian : {V : Type u_1} -> {G : SimpleGraph V} -> [DecidableEq V] -> {u v : V} -> (p : G.Walk u v) -> Prop
<!-- PINNED-SIGNATURE:END -->


The vertex type `V` and simple graph `G` are implicit; `DecidableEq V` is a required typeclass instance enabling edge counting. The endpoints `u` and `v` are implicit vertices of `G`; the explicit argument `p` is the walk from `u` to `v` whose Eulerian property is being asserted.

### Conventions

No special junk-value or edge conventions are declared for this predicate: it is a universally quantified statement over all edges of the graph, and it is vacuously true on the empty-edge graph (where the nil walk trivially satisfies the condition since there are no edges to check).

### Worked examples

- Claim: Any walk satisfying `VTask.IsEulerian p` is a trail (no edge repeated), i.e., `VTask.IsEulerian p → p.IsTrail`.

- Claim: For a graph on finitely many vertices with a decidable adjacency relation, if `p : G.Walk u v` satisfies `VTask.IsEulerian p` and `u ≠ v`, then both `u` and `v` have odd degree in `G` and every other vertex has even degree.

- Claim: If `p : G.Walk u v` is an Eulerian trail, then the set of edges appearing in `p` equals the entire edge set of `G`, i.e., `p.edgeSet = G.edgeSet`.

- Claim: A trail `p : G.Walk u v` is Eulerian if and only if it passes through every edge of the graph at least once (given it already visits no edge more than once).

### Boundaries

- **Empty graph**: If `G` has no edges, any nil walk (of length zero from a vertex to itself) is trivially Eulerian, since the universal quantification over edges is vacuously satisfied.
- **Single edge**: A walk that traverses a single edge `{u, v}` once is Eulerian for the graph consisting of exactly that edge.
- **Not a trail**: A walk that repeats any edge fails `VTask.IsEulerian` because that edge's count in `p.edges` would be ≥ 2, not 1.
- **Missing an edge**: A trail that skips any edge of the graph fails `VTask.IsEulerian` because that edge's count would be 0, not 1.
- **Eulerian circuit**: Combining `VTask.IsEulerian p` with `p.IsCircuit` (which requires `u = v` and non-trivial length) gives the notion of an Eulerian circuit/cycle.
- **Degree parity**: In a finite graph, at most two vertices can have odd degree (exactly the endpoints when `u ≠ v`, and zero when `u = v` and the walk is a circuit).

### Not to be confused with

- `SimpleGraph.Walk.IsTrail`: a weaker condition requiring only that no edge is repeated; an Eulerian trail must additionally cover every edge of the graph.
- `SimpleGraph.Walk.IsCircuit`: concerns start/end coincidence and non-triviality; combine with `VTask.IsEulerian` for Eulerian circuits, but `IsCircuit` alone says nothing about edge coverage.
- `SimpleGraph.Walk.IsHamiltonian` (or path variants): a Hamiltonian path/cycle visits every *vertex* exactly once, whereas an Eulerian trail visits every *edge* exactly once.
