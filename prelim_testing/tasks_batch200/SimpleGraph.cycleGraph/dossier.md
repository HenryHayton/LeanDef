## Object

The **cycle graph** on `n` vertices is the simple graph whose vertex set is `{0, 1, …, n-1}` (represented as `Fin n`) and whose edges connect every pair of vertices that are *cyclically adjacent*, i.e., consecutive modulo `n`. Concretely, two distinct vertices `a` and `b` are adjacent when one of them immediately follows the other in the cyclic order on `Fin n` (with vertex `0` considered a neighbour of vertex `n-1`). For `n ≥ 3` this produces the familiar polygon graph Cₙ; the degenerate cases `n = 0` and `n = 1` yield empty graphs (no edges possible), and `n = 2` yields the unique graph on two mutually adjacent vertices.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.cycleGraph : (n : ℕ) -> SimpleGraph (Fin n)
<!-- PINNED-SIGNATURE:END -->


The single argument `n` is a natural number specifying how many vertices the cycle graph has; the vertex set of the resulting `SimpleGraph` is `Fin n`.

## Conventions

For `n = 0` the graph is the empty (bottom) graph on the empty vertex type `Fin 0`, since there are no vertices and hence no edges. For `n = 1` the graph is likewise the empty (bottom) graph on the one-element type `Fin 1`, since a simple graph forbids self-loops. For `n = 2` the graph equals the complete graph (top graph) on `Fin 2`, connecting the two vertices by an edge; this is consistent with the adjacency rule but is topologically a multi-edge in the non-simple sense — Mathlib records it as the unique simple graph on two vertices with an edge. Arithmetic on vertices in `Fin n` is modular (subtraction and addition wrap around), so the adjacency relation is genuinely cyclic.

## Worked examples

- Claim: `VTask.cycleGraph 0` has no edges, i.e., it equals the bottom graph `⊥` on `Fin 0`.

- Claim: `VTask.cycleGraph 1` has no edges, i.e., it equals the bottom graph `⊥` on `Fin 1`.

- Claim: For `n = 5` each vertex has exactly two neighbours — the vertex immediately before it and the vertex immediately after it in the cyclic order.

- Claim: `VTask.cycleGraph 3 = ⊤` — on three vertices the cycle graph is the complete graph K₃, since every pair of the three vertices is cyclically adjacent.

- Claim: For `n ≥ 3` a simple graph `G` contains `VTask.cycleGraph n` as a subgraph if and only if `G` has a closed walk of length `n` that is a cycle.

## Boundaries

- **`n = 0`**: The vertex type is empty; the graph has no vertices and no edges. It coincides with `⊥`.
- **`n = 1`**: There is one vertex but no edges (a simple graph has no self-loops). The graph coincides with `⊥`.
- **`n = 2`**: There are two vertices, and the modular subtraction condition makes them adjacent; the graph is the complete graph `⊤` on `Fin 2`, which is also `K₂`.
- **`n = 3`**: Every pair among the three vertices satisfies the adjacency condition, so the graph equals `⊤` on `Fin 3`, i.e., K₃.
- **`n ≥ 3` in general**: Each vertex has degree exactly 2, and the graph is the standard polygon graph Cₙ, which contains exactly one Hamiltonian cycle.
- The path graph on `n` vertices is a subgraph of `VTask.cycleGraph n` for all `n`.

## Not to be confused with

- **`pathGraph n`**: The path graph Pₙ on `n` vertices, which is a subgraph of the cycle graph but lacks the closing edge between vertex `0` and vertex `n-1`.
- **`completeGraph n`** (`⊤`): The complete graph on `Fin n`; equals `VTask.cycleGraph n` only for `n ∈ {2, 3}`, not in general.
- **`completeBipartiteGraph`**: A bipartite complete graph; unrelated to the cycle structure, though even cycles are bipartite.
