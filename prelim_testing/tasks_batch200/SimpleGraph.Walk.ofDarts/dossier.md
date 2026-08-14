## Object

`VTask.ofDarts` constructs a graph walk from a nonempty, consecutively-compatible list of darts. A *dart* in a simple graph is an ordered pair of adjacent vertices together with a proof of adjacency. Given a list of darts in which each consecutive pair of darts is *dart-adjacent* (meaning the head of the second dart equals the tail of the first, so the walk can continue without a gap), the function assembles them into a single walk whose starting vertex is the tail of the first dart and whose ending vertex is the head of the last dart.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofDarts : {V : Type u} -> {G : SimpleGraph V} -> (l : List G.Dart) -> (hne : l ≠ []) -> (hchain : List.IsChain G.DartAdj l) -> G.Walk (l.head hne).toProd.1 (l.getLast hne).toProd.2
<!-- PINNED-SIGNATURE:END -->


`VTask.ofDarts : {V : Type u} -> {G : SimpleGraph V} -> (l : List G.Dart) -> (hne : l ≠ []) -> (hchain : List.IsChain G.DartAdj l) -> G.Walk (l.head hne).toProd.1 (l.getLast hne).toProd.2`

The implicit arguments `V` and `G` fix the vertex type and the simple graph in which all darts and the resulting walk live. The argument `l` is the ordered list of darts that will form the steps of the walk. The argument `hne` is a proof that `l` is nonempty, which is needed to extract the first and last dart for the walk's endpoints. The argument `hchain` is a proof that consecutive darts in `l` are dart-adjacent, ensuring the walk is well-formed (i.e., each step ends where the next step begins).

## Conventions

There are no junk-value conventions for this definition: the inputs are fully constrained (nonemptiness and the chain condition are explicit proof arguments), so every call to `VTask.ofDarts` with valid inputs yields a legitimate walk with no degenerate edge cases requiring special conventions.

## Worked examples

- Claim: For a single dart `d`, `VTask.ofDarts [d] _ _` is the one-step walk `Walk.cons d.adj Walk.nil`.

- Claim: The dart list of the walk produced by `VTask.ofDarts l hne hchain` equals `l` itself. That is, round-tripping through darts recovers the original list: `(VTask.ofDarts l hne hchain).darts = l`.

- Claim: The edge list of `VTask.ofDarts l hne hchain` equals `l.map Dart.edge`, i.e., each dart's underlying edge appears in order.

- Claim: The length of `VTask.ofDarts l hne hchain` equals the length of `l`.

- Claim: For a non-nil walk `p`, applying `VTask.ofDarts` to `p.darts` recovers a walk equal (up to vertex-equality) to `p`.

## Boundaries

- **Singleton list**: When `l` has exactly one dart `d`, the resulting walk is the single-step walk starting and ending at the tail and head of `d`, respectively. No chain condition is needed beyond the trivial one for a singleton.
- **Two or more darts**: The chain condition `hchain` must supply proofs that each consecutive pair of darts satisfies `DartAdj`, which means the source of the second dart equals the target of the first. Without this, the concatenation would not type-check.
- **Nonemptiness is required**: The empty list case is explicitly excluded by `hne`; attempting to call `VTask.ofDarts [] _ _` is impossible since `[] ≠ []` is unprovable.
- **Endpoints are determined by the list**: The start vertex `(l.head hne).toProd.1` and end vertex `(l.getLast hne).toProd.2` are not free parameters but are uniquely fixed by the first and last dart.

## Not to be confused with

- `SimpleGraph.Walk.cons`: builds a walk by prepending a single adjacency proof to an existing walk, rather than consuming an entire dart list at once.
- `SimpleGraph.Walk.darts`: the inverse direction, extracting the list of darts from a walk; `VTask.ofDarts` goes the other way.
- `SimpleGraph.Walk.copy`: adjusts the endpoint types of a walk by vertex equalities without changing its structure, which is used when round-tripping through `VTask.ofDarts` and back.