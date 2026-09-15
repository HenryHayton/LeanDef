## VTask.IsExtremal

### Object

A simple graph `G` on a finite vertex type `V` is *extremal* for a property `p` if two conditions hold simultaneously: `G` itself satisfies `p`, and no other simple graph on the same vertex set `V` satisfying `p` has strictly more edges than `G`. In other words, `G` is an edge-count maximiser among all graphs on `V` with property `p`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsExtremal : {V : Type u_1} -> [Fintype V] -> (G : SimpleGraph V) -> [DecidableRel G.Adj] -> (p : SimpleGraph V → Prop) -> Prop
<!-- PINNED-SIGNATURE:END -->


The implicit type argument `V` is the finite vertex type shared by all graphs under consideration; the `Fintype` instance makes `V` finite. `G` is the candidate simple graph being tested for extremality. The `DecidableRel G.Adj` instance enables computational reasoning about `G`'s adjacency relation. The argument `p` is the graph property — a predicate on simple graphs over `V` — with respect to which extremality is measured.

### Conventions

There are no special junk-value or edge conventions: the definition is a universally-quantified conjunction over a finite-type setting, and every input is fully constrained by the types involved.

### Worked examples

- Claim: If `G.IsExtremal p` holds, then `p G` holds — that is, every extremal graph satisfies its own property.

- Claim: If `G.IsExtremal p` and `H` also satisfies `p`, and `G ≤ H` (as graphs, i.e., every edge of `G` is an edge of `H`), then `G = H` — an extremal graph cannot be a proper subgraph of another graph satisfying the same property.

- Claim: For every non-empty graph `H` on a finite type `W`, there exists a simple graph on `V` that is extremal for the property of being `H`-free (i.e., containing no subgraph isomorphic to `H`).

- Claim: For a finite vertex type `α`, the Turán graph `turanGraph n (card α - 1)` is extremal for the property of being `(⊤ : SimpleGraph α)`-free, connecting extremality to the Turán-maximal notion.

### Boundaries

- If the property `p` is unsatisfiable (no simple graph on `V` satisfies `p`), then `VTask.IsExtremal G p` is false for every `G`, because the first conjunct `p G` fails.
- If `p` is satisfied by at least one graph, then by finiteness of `V` (and hence finiteness of the set of simple graphs on `V`), an extremal graph always exists.
- Extremality does not imply uniqueness: two distinct graphs can each be extremal for `p` if they both satisfy `p` and both achieve the maximum edge count. However, if one extremal graph is a subgraph of another graph satisfying `p`, they must be equal.
- The edge count comparison uses the cardinality of `edgeFinset`, so the maximality condition is purely combinatorial (number of edges), not structural.

### Not to be confused with

- `SimpleGraph.IsTuranMaximal r`: a graph that is `r`-partite and edge-maximal among `r`-partite graphs; related to extremality for the `(⊤ : SimpleGraph α).Free` property but defined independently.
- `SimpleGraph.extremalNumber n H`: a natural number giving the maximum edge count of any `H`-free graph on `n` vertices; a numerical invariant, not a predicate on graphs.
- `SimpleGraph.Free H G` (a.k.a. `H.Free G`): the property that `G` contains no subgraph isomorphic to `H`; this is an example of a predicate `p` one might plug into `VTask.IsExtremal`, not extremality itself.