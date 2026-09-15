## Object

`VTask.concatRec` is a dependent eliminator (recursor) for walks in a simple graph, where induction proceeds by appending edges at the **end** of the walk rather than at the beginning. Given a walk `p : G.Walk u v`, it produces a term of type `motive u v p` by: (1) handling the empty walk at any vertex, and (2) extending any walk `p : G.Walk u v` by one additional edge `v —— w` to produce a result for the concatenated walk `p.concat h : G.Walk u w`. This is the "right-to-left" or "append at tail" induction principle for graph walks.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.concatRec : {V : Type u} -> {G : SimpleGraph V} -> {motive : (u v : V) → G.Walk u v → Sort u_1} -> (Hnil : {u : V} → motive u u SimpleGraph.Walk.nil) -> (Hconcat : {u v w : V} → (p : G.Walk u v) → (h : G.Adj v w) → motive u v p → motive u w (p.concat h)) -> {u v : V} -> (p : G.Walk u v) -> motive u v p
<!-- PINNED-SIGNATURE:END -->


`VTask.concatRec : {V : Type u} -> {G : SimpleGraph V} -> {motive : (u v : V) → G.Walk u v → Sort u_1} -> (Hnil : {u : V} → motive u u SimpleGraph.Walk.nil) -> (Hconcat : {u v w : V} → (p : G.Walk u v) → (h : G.Adj v w) → motive u v p → motive u w (p.concat h)) -> {u v : V} -> (p : G.Walk u v) -> motive u v p`

- `V` is the vertex type of the graph.
- `G` is the simple graph over `V`.
- `motive` is the type family (dependent return type) indexed by the two endpoints and the walk itself; it may live in any `Sort`.
- `Hnil` supplies the base-case value: a term of type `motive u u nil` for every vertex `u`, handling the empty walk.
- `Hconcat` is the inductive step: given any walk `p` from `u` to `v`, an adjacency proof `h : G.Adj v w` extending it by one edge, and a recursively-computed value for `p`, it produces a value for the concatenated walk `p.concat h`.
- The implicit arguments `u` and `v` are the start and end vertices of the walk.
- `p` is the walk being eliminated.

## Conventions

There are no junk-value or boundary conventions to declare: `VTask.concatRec` is a total function defined over all walks, all motives, and all vertex types without any side conditions.

## Worked examples

- Claim: Applying `VTask.concatRec` to the empty walk `nil` returns exactly `Hnil` — that is, `VTask.concatRec Hnil Hconcat nil = Hnil` (the `concatRec_nil` computation rule).

- Claim: Applying `VTask.concatRec` to a concatenated walk `p.concat h` returns `Hconcat p h (VTask.concatRec Hnil Hconcat p)` — the inductive step is evaluated by recursing on the prefix `p` first, then applying `Hconcat` (the `concatRec_concat` computation rule).

- Claim: For the length motive `motive u v p := Nat`, with `Hnil := 0` and `Hconcat _ _ n := n + 1`, applying `VTask.concatRec` to a walk of length `k` yields `k`, matching the definition of walk length.

- Claim: `VTask.concatRec` and `SimpleGraph.Walk.rec` (which inducts from the front via `cons`) produce equal results when the base cases and step cases are compatible, demonstrating that both recursors capture the same inductive structure from opposite ends.

## Boundaries

- On the empty walk `nil : G.Walk u u`, the recursor immediately returns `Hnil`, without invoking `Hconcat` at all.
- On a walk consisting of a single edge `nil.concat h`, the recursor calls `Hconcat nil h Hnil`, nesting exactly one level deep.
- The recursor is defined for walks of any finite length, including length 0 and length 1, with no restriction.
- Because `SimpleGraph` is a simple graph (no self-loops, edges are symmetric), the adjacency proofs `h` passed to `Hconcat` always connect distinct vertices.
- The universe level of `motive` is unconstrained (`Sort u_1`), so `VTask.concatRec` can be used both to compute values (functions) and to prove propositions (where `motive` lives in `Prop`).

## Not to be confused with

- `SimpleGraph.Walk.rec` — the standard recursor for walks, which inducts from the **front** using `cons` (prepending an edge) rather than from the back using `concat` (appending an edge).
- `SimpleGraph.Walk.concat` — the operation that appends one walk to another (or appends a single edge); this is what `VTask.concatRec`'s step case deconstructs, not a recursor itself.
- `SimpleGraph.Walk.reverse` — reverses a walk, swapping start and end; closely related in implementation but is a specific walk transformation, not a recursor.
