## VTask.toLoop

### Object

Given a generalized loop `p : Ω^N X x` — a continuous map from the unit $N$-cube $I^N$ to $X$ that sends every boundary point to the base point $x$ — and a chosen coordinate direction `i : N`, `toLoop i p` produces a loop in the loop space $\Omega(\Omega^{N\setminus\{i\}} X, x)$. Concretely, it curries the map $I^N \to X$ into a path $I \to (I^{N\setminus\{i\}} \to X)$ by inserting the time parameter into coordinate $i$, and verifies that this path starts and ends at the constant map (the base point of the inner loop space). The result is an element of the loop space whose base point is the constant generalized loop `const`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toLoop : {N : Type u_1} -> {X : Type u_2} -> [TopologicalSpace X] -> {x : X} -> [DecidableEq N] -> (i : N) -> (p : ↑(GenLoop N X x)) -> LoopSpace (↑(GenLoop { j // j ≠ i } X x)) GenLoop.const
<!-- PINNED-SIGNATURE:END -->


`N` is the index type labelling the coordinate directions of the cube; `X` is the ambient topological space; `x` is the base point of `X`; instances provide the topology on `X` and decidable equality on `N`. The argument `i : N` is the coordinate direction to be "singled out" as the loop parameter. The argument `p` is the generalized $N$-loop to be curried.

### Conventions

No junk-value or edge-case conventions are declared for this definition: it is a total construction whose output is determined entirely by the mathematical content of the inputs, with no degenerate regime requiring special treatment.

### Worked examples

- Claim: For the trivial index type `N = Unit`, applying `toLoop` to the constant generalized loop yields the constant loop in the resulting loop space.

- Claim: The source of `toLoop i p` (i.e., its value at time 0) is the constant generalized loop `GenLoop.const`, because inserting 0 into coordinate `i` puts the argument on the boundary of the $N$-cube, where `p` is required to evaluate to `x`.

- Claim: The target of `toLoop i p` (i.e., its value at time 1) is again `GenLoop.const`, because inserting 1 into coordinate `i` likewise places the argument on the boundary of the $N$-cube.

- Claim: For any point `t` in $I$ and any `y` on the boundary of $I^{N\setminus\{i\}}$, the value `(toLoop i p).toFun t` evaluated at `y` equals `x`, since `(t, y)` inserted into coordinate `i` lands on the boundary of $I^N$.

### Boundaries

- When `N` is empty (or has a single element so that $N\setminus\{i\}$ is empty), the construction still type-checks; the inner loop space degenerates to a loop space of maps from the 0-cube (a point) to `X`, which is essentially just the loop space $\Omega X$ itself.
- When `p` is the constant generalized loop `const`, `toLoop i p` is the constant loop at `const`.
- The boundary conditions are enforced strictly: the produced loop lives in the correct loop space with base point `GenLoop.const` regardless of which coordinate `i` is chosen.

### Not to be confused with

- `GenLoop` itself — that is the type of generalized $N$-loops (maps $I^N \to X$ vanishing on the boundary), of which `toLoop i p` is an element of the loop space, not a generalized loop itself.
- `Cube.insertAt i` — the auxiliary function that inserts a single time value into coordinate `i` of the cube; `toLoop` uses this internally but is a higher-level looping/currying operation.
- The inverse operation (uncurrying a loop in a loop space back to a generalized loop), which would go in the opposite direction and is a distinct construction.