## VTask.graph

### Object

The graph of a function `f : α → β` is the binary relation (set of pairs) consisting of exactly those pairs `(a, b)` where `b = f a`. It is the standard set-theoretic encoding of a function as a relation: instead of viewing `f` as a rule, one views it as the collection of all input–output pairs it produces.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.graph : {α : Type u_1} -> {β : Type u_2} -> (f : α → β) -> SetRel α β
<!-- PINNED-SIGNATURE:END -->


`VTask.graph : {α : Type u_1} -> {β : Type u_2} -> (f : α → β) -> SetRel α β`

The two universe-polymorphic type arguments `α` and `β` are the domain and codomain types of the function, inferred implicitly. The explicit argument `f` is the function whose graph is being formed; it maps elements of `α` to elements of `β`. The result is a `SetRel α β`, i.e., a relation from `α` to `β` represented as a set of pairs.

### Conventions

No special junk-value or edge-case conventions are declared for this definition: the function `f` is arbitrary and total over its domain, so every element of `α` contributes exactly one pair to the graph, and no inputs are excluded or treated specially.

### Worked examples

- Claim: The pair `(3, 9)` belongs to `VTask.graph (fun n : ℕ => n * n)` because `3 * 3 = 9`.

- Claim: The pair `(3, 8)` does **not** belong to `VTask.graph (fun n : ℕ => n * n)` because `3 * 3 ≠ 8`.

- Claim: For the identity function `id : α → α`, `VTask.graph id` is the diagonal relation — it contains `(a, a)` for every `a : α`, and no pair `(a, b)` with `a ≠ b`.

- Claim: For a constant function `fun (_ : α) => c`, the graph `VTask.graph (fun (_ : α) => c)` contains every pair `(a, c)` for `a : α`, and no pair whose second component differs from `c`.

### Boundaries

- **Every function has a graph**: because `f` is a total Lean function, every element `a : α` contributes exactly one pair `(a, f a)`, so the graph is never empty (unless `α` is empty).
- **Empty domain**: if `α` is an empty type, the graph `VTask.graph f` is the empty relation (no pairs exist).
- **Uniqueness of right component**: for each fixed `a`, the pair `(a, b)` belongs to the graph for exactly one value of `b`, namely `b = f a`. This reflects the functional nature of `f`.
- **Surjectivity and the graph**: every element of `β` appears as a right component if and only if `f` is surjective; not every `b` need appear.

### Not to be confused with

- **`Set.range f`**: this is the image of `f` — the set `{b | ∃ a, f a = b}` — which records only the right components, discarding the pairing with their preimages.
- **`Relation.graph` or a preorder's Hasse diagram**: those relate to order-theoretic constructions and are distinct from the set-theoretic function graph.
- **An inverse relation**: the graph of `f` pairs `(a, f a)`; its relational converse pairs `(f a, a)`, which is the graph of a potential inverse and is generally different.
