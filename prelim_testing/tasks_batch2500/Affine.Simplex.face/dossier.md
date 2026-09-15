## Object

A *face* of an affine simplex is a lower-dimensional affine simplex whose vertices are exactly the points of the original simplex indexed by a chosen finite subset of vertex indices. Concretely, given an $n$-simplex (a collection of $n+1$ affinely independent points in an affine space) and a subset $fs$ of size $m+1$ of the index set $\{0, 1, \ldots, n\}$, the face is the $m$-simplex formed by those $m+1$ selected vertices, listed in their natural (order-embedding) order.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.face : {k : Type u_1} -> {V : Type u_2} -> {P : Type u_5} -> [Ring k] -> [AddCommGroup V] -> [Module k V] -> [AddTorsor V P] -> {n : ℕ} -> (s : Affine.Simplex k P n) -> {fs : Finset (Fin (n + 1))} -> {m : ℕ} -> (h : fs.card = m + 1) -> Affine.Simplex k P m
<!-- PINNED-SIGNATURE:END -->


`VTask.face : {k : Type u_1} -> {V : Type u_2} -> {P : Type u_5} -> [Ring k] -> [AddCommGroup V] -> [Module k V] -> [AddTorsor V P] -> {n : ℕ} -> (s : Affine.Simplex k P n) -> {fs : Finset (Fin (n + 1))} -> {m : ℕ} -> (h : fs.card = m + 1) -> Affine.Simplex k P m`

The implicit type arguments `k`, `V`, and `P` are the scalar field, the underlying vector space, and the ambient affine space, respectively; the typeclass arguments equip these with the required algebraic structures. The argument `s` is the ambient $n$-simplex whose face is being taken. The implicit argument `fs` is a `Finset` of indices drawn from $\{0, 1, \ldots, n\}$ specifying which vertices of `s` are to be selected. The implicit `m` is the dimension of the resulting face. The proof `h` witnesses that `fs` has exactly $m+1$ elements, connecting the cardinality of the index subset to the dimension of the resulting simplex.

## Conventions

The vertices of the face are ordered according to the canonical order embedding of `fs` into `Fin (n+1)`, meaning the $i$-th vertex of the face corresponds to the $i$-th smallest element of `fs` (in the natural ordering on `Fin (n+1)`). Affine independence of the face is inherited from that of the ambient simplex, so no additional independence check is needed.

## Worked examples

- Claim: For the standard 2-simplex with vertices indexed 0, 1, 2, taking the face corresponding to the subset `{0, 1}` (with cardinality proof `2 = 1 + 1`) yields a 1-simplex whose first vertex is the vertex at index 0 of the original simplex, and second vertex is the vertex at index 1.

- Claim: Taking the face of an $n$-simplex `s` with `fs = Finset.univ` (all $n+1$ indices) and the trivial cardinality proof `h : Finset.univ.card = n + 1` returns an $n$-simplex with the same set of vertices as `s` (in the same order given by the canonical order embedding of the full index set).

- Claim: For a 2-simplex `s` and a singleton subset `{i}` with cardinality proof `h : ({i} : Finset (Fin 3)).card = 0 + 1`, `VTask.face s h` is a 0-simplex (a single point) whose unique vertex is `s.points i`.

## Boundaries

- **Minimum face dimension**: The cardinality constraint `fs.card = m + 1` forces `fs` to be nonempty (since $m+1 \geq 1$), so the face always has at least one vertex (dimension $\geq 0$). There is no "empty face" or face of dimension $-1$.
- **Maximum face dimension**: When `fs = Finset.univ`, the face has the same dimension as the original simplex; in this case the result is a simplex with identical vertex multiset (in order-embedding order).
- **Vertex ordering**: Vertices in the face are always enumerated in the strictly increasing order of the corresponding original indices; any reordering of `fs` would yield the same result because `Finset` is unordered and the order embedding is canonical.
- **Affine independence is automatic**: The face is automatically affinely independent by virtue of being a subset of an affinely independent collection; the definition handles this internally without additional hypotheses.

## Not to be confused with

- `Affine.Simplex` itself — the ambient simplex type, not the operation of selecting a face from it.
- A combinatorial face of a simplicial complex — in Mathlib the `face` function operates on a concrete affine simplex and returns an affine simplex, not a combinatorial object.
- The `Finset.orderEmbOfFin` order embedding — a tool used internally to enumerate the selected vertices in order, not the face operation itself.