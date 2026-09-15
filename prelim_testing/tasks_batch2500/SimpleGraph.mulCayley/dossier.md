## Object

The **multiplication Cayley graph** of a type `M` equipped with a binary operation, with respect to a set of generators `s ⊆ M`. This is the simple graph whose vertex set is `M` and in which two distinct vertices `x` and `y` are adjacent if and only if there exists some generator `g ∈ s` such that multiplying one of the vertices on the right by `g` yields the other — that is, `x * g = y` or `y * g = x` (the relation is symmetrised to make the graph undirected, and the self-loop at each vertex is removed to keep it simple).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mulCayley : {M : Type u_1} -> (s : Set M) -> [Mul M] -> SimpleGraph M
<!-- PINNED-SIGNATURE:END -->


`VTask.mulCayley : {M : Type u_1} -> (s : Set M) -> [Mul M] -> SimpleGraph M`

The implicit type argument `M` is the carrier type whose elements serve as the vertices of the graph. The explicit argument `s` is the generating set: the collection of elements of `M` whose right-multiplication action determines the edges. The instance argument `[Mul M]` provides the binary multiplication on `M` used to define adjacency.

## Conventions

The resulting graph is a `SimpleGraph`, which by definition has no self-loops; even if `s` contains an element `g` such that `x * g = x` for some vertex `x`, the pair `(x, x)` is not an edge. The underlying relation is symmetrised automatically: if `x` is adjacent to `y` via a generator in `s`, then `y` is also adjacent to `x`, regardless of whether the structure of `M` is commutative or whether `s` is closed under inversion.

## Worked examples

- Claim: In the integers mod 4 with addition written as multiplication, taking `s = {1}`, the vertex `0` is adjacent to `1` (since `0 * 1 = 1`, i.e., `0 + 1 = 1`), but `0` is not adjacent to `2` (no single step of `+1` connects them directly).

- Claim: For any type `M` with a `Mul` instance and any generating set `s`, the graph `VTask.mulCayley s` is a `SimpleGraph M`, meaning its adjacency relation is irreflexive and symmetric.

- Claim: If `s` is the empty set, then `VTask.mulCayley s` has no edges — every pair of vertices is non-adjacent, yielding a totally disconnected graph.

- Claim: If `M` is the integers (or any group) and `s = {1, -1}`, the Cayley graph `VTask.mulCayley s` connects each integer `n` to `n+1` and `n-1`, producing the infinite path (bi-infinite line) graph.

## Boundaries

- **Empty generating set**: When `s = ∅`, no two vertices can be adjacent (there is no generator to witness the relation), so the graph has vertex set `M` and no edges.
- **Self-loops excluded**: Even when a generator `g` satisfies `x * g = x` (i.e., `g` is a right identity for `x`), the pair `(x, x)` is excluded by the `SimpleGraph` contract.
- **Non-injective multiplication**: If right-multiplication by some `g ∈ s` is not injective, multiple edges may share a generator, but `SimpleGraph` collapses parallel edges — adjacency is a `Prop`.
- **Non-invertible elements**: Unlike the classical group-theoretic Cayley graph, `M` need not be a group. There is no requirement that generators be invertible or that `s` be closed under inverses; symmetry of adjacency is imposed externally.
- **Infinite types**: The construction is well-defined for infinite `M`; the result is an infinite simple graph.

## Not to be confused with

- **`addCayley`** (the additive analogue): uses `[Add M]` and additive structure (`x + g = y`) rather than multiplication; the two coincide when additive and multiplicative notations agree but are otherwise distinct.
- **`SimpleGraph.fromRel`**: the lower-level constructor that symmetrises any binary relation into a `SimpleGraph`; `VTask.mulCayley` is a specific instance of it, not the general tool.
- **The classical Cayley graph of a group**: the standard definition in combinatorics typically requires `M` to be a group and `s` to be closed under inverses (or at least inverse-symmetric); `VTask.mulCayley` imposes neither restriction.