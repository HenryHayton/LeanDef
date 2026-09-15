## VTask.InductiveLimit

### Object

Given a sequence of metric spaces $(X_n)_{n \in \mathbb{N}}$ connected by isometric embeddings $f_n : X_n \to X_{n+1}$, the **inductive limit** (also called the **direct limit** or **colimit**) is a metric space that is, informally, the "union" of all the $X_n$ after identifying each $x \in X_n$ with its image $f_n(x) \in X_{n+1}$.  Concretely, one first equips the disjoint union $\bigsqcup_n X_n$ with a premetric (a symmetric, reflexive distance function that satisfies the triangle inequality but may assign distance $0$ to distinct points), then passes to the Hausdorff quotient that collapses all pairs at premetric distance $0$ to single points.  The result is a genuine metric space into which each $X_n$ maps isometrically, and it enjoys the universal property that any compatible family of isometric maps out of the $X_n$ factors through it.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.InductiveLimit : {X : ℕ → Type u} -> [(n : ℕ) → MetricSpace (X n)] -> {f : (n : ℕ) → X n → X (n + 1)} -> (I : ∀ (n : ℕ), Isometry (f n)) -> Type u
<!-- PINNED-SIGNATURE:END -->


The implicit argument `X` is the sequence of types, one for each natural number, that form the links of the inductive system.  The instance argument `[MetricSpace (X n)]` supplies, for every $n$, the metric-space structure on the $n$-th term.  The implicit argument `f` is the transition family: for each $n$, a function $f_n : X_n \to X_{n+1}$ connecting consecutive terms.  The explicit argument `I` is the proof that every transition map $f_n$ is an isometry, i.e., preserves all pairwise distances; this hypothesis is essential for the premetric on the disjoint union to be well-defined and consistent.

### Conventions

No junk-value or edge conventions are declared for this construction: it is a genuinely total type-valued operation and is well-defined for any isometric inductive system, including degenerate ones such as a constant sequence or a single-term system.

### Worked examples

- Claim: When every $X_n$ is the real line $\mathbb{R}$ and every $f_n$ is the identity, `VTask.InductiveLimit I` is a well-typed `Type u` (it exists and is inhabited by the equivalence class of any real number).

- Claim: When $X_n = \{0\}$ (a one-point metric space) for all $n$ and every $f_n$ is the unique map, `VTask.InductiveLimit I` is a one-element type, because all points in every $X_n$ are identified and there is a single equivalence class.

- Claim: For an isometric inductive system in which each $f_n$ is a strict isometric embedding (so the spaces are genuinely growing), `VTask.InductiveLimit I` is a `Type u` that contains isometric copies of every $X_n$ as a subspace.

### Boundaries

- **Single-term / trivial system**: If each $X_n$ is a one-point space, the inductive limit is itself a one-point metric space.
- **Constant system**: If $X_n = X$ for all $n$ and every $f_n$ is the identity, the inductive limit is isometric to $X$ itself.
- **Non-surjective embeddings**: The construction is still valid; the inductive limit may be strictly larger than any individual $X_n$.
- **Completeness**: The inductive limit of a sequence of complete metric spaces need not itself be complete; its completion is the metric completion of this construction.
- **Hausdorff quotient step**: Points that are at premetric distance $0$ but are formally distinct (arising from different levels) are identified, so the output is a genuine metric space (with $d(x,y) = 0 \Rightarrow x = y$), not merely a premetric space.

### Not to be confused with

- **`Metric.Completion`** — the metric completion of a metric space, which adds limit points of Cauchy sequences; distinct from the inductive limit even when applied to the same underlying space.
- **`TopologicalSpace.inductive_limit` (topological colimit)** — a colimit construction in the category of topological spaces without the metric structure; the present definition carries full metric-space data.
- **`DirectSum` / `Finset`-indexed coproducts** — algebraic direct sums index over all of $\mathbb{N}$ with finite support; the inductive limit here is a quotient of the full disjoint union, not a direct sum of modules.