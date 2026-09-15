## Object

Given topological spaces $X$ and $Y$, and continuous maps $f_0, f_1, f_2 : X \to Y$, `VTask.trans F G` constructs a homotopy from $f_0$ to $f_2$ by concatenating two homotopies: $F$ (a homotopy from $f_0$ to $f_1$) and $G$ (a homotopy from $f_1$ to $f_2$). The resulting homotopy runs $F$ on the first half of the time interval $[0, 1/2]$ and $G$ on the second half $[1/2, 1]$, with both halves rescaled to fill the full unit interval $[0,1]$.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.trans : {X : Type u} -> {Y : Type v} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> {f₀ f₁ f₂ : C(X, Y)} -> (F : f₀.Homotopy f₁) -> (G : f₁.Homotopy f₂) -> f₀.Homotopy f₂
<!-- PINNED-SIGNATURE:END -->


VTask.trans : {X : Type u} -> {Y : Type v} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> {f₀ f₁ f₂ : C(X, Y)} -> (F : f₀.Homotopy f₁) -> (G : f₁.Homotopy f₂) -> f₀.Homotopy f₂

The type parameters `X` and `Y` are the domain and codomain topological spaces, provided implicitly. The topological space structures on `X` and `Y` are instance arguments. The maps `f₀`, `f₁`, `f₂` are continuous maps from `X` to `Y`, provided implicitly. The argument `F` is a homotopy connecting $f_0$ to $f_1$ — a continuous deformation of $f_0$ into $f_1$ parametrised by the unit interval. The argument `G` is a homotopy connecting $f_1$ to $f_2$ — a continuous deformation of $f_1$ into $f_2$ parametrised by the unit interval. Both homotopies share the intermediate map $f_1$ as their meeting point.

## Conventions

The concatenation uses the rescaling convention: for parameter $t \in [0, 1/2]$, the output is $F(2t, x)$, and for $t \in [1/2, 1]$, the output is $G(2t - 1, x)$. At the junction point $t = 1/2$, both pieces agree because $F(1, x) = f_1(x) = G(0, x)$, ensuring continuity. The boundary conditions are inherited: at $t = 0$ the concatenated homotopy equals $f_0$, and at $t = 1$ it equals $f_2$.

## Worked examples

- Claim: For any homotopy `F : f₀.Homotopy f₁` and `G : f₁.Homotopy f₂`, evaluating `VTask.trans F G` at time parameter $0$ (i.e., the left endpoint) at any point $x$ yields $f_0(x)$.

- Claim: For any homotopy `F : f₀.Homotopy f₁` and `G : f₁.Homotopy f₂`, evaluating `VTask.trans F G` at time parameter $1$ (i.e., the right endpoint) at any point $x$ yields $f_2(x)$.

- Claim: For any homotopy `F : f₀.Homotopy f₁` and `G : f₁.Homotopy f₂`, evaluating `VTask.trans F G` at time parameter $1/4$ at any point $x$ equals $F(1/2, x)$, since $1/4 \leq 1/2$ so the first branch applies with rescaled time $2 \cdot 1/4 = 1/2$.

- Claim: For any homotopy `F : f₀.Homotopy f₁` and `G : f₁.Homotopy f₂`, evaluating `VTask.trans F G` at time parameter $3/4$ at any point $x$ equals $G(1/2, x)$, since $3/4 > 1/2$ so the second branch applies with rescaled time $2 \cdot 3/4 - 1 = 1/2$.

## Boundaries

- At $t = 0$: the homotopy evaluates to $f_0(x)$ for all $x$, matching the required left boundary condition.
- At $t = 1$: the homotopy evaluates to $f_2(x)$ for all $x$, matching the required right boundary condition.
- At $t = 1/2$ (the junction): both halves agree, since $F(1, x) = f_1(x) = G(0, x)$. This agreement is what guarantees continuity of the concatenated homotopy at the seam.
- The construction is defined for all $t \in [0, 1]$ without exception; there are no points excluded from the domain.
- The resulting object is genuinely a homotopy (satisfies continuity and the boundary conditions at $0$ and $1$), not merely a set-theoretic combination.

## Not to be confused with

- `ContinuousMap.HomotopyRel.trans`: the relative version of homotopy concatenation, where the homotopy is required to fix a specified subset of $X$ pointwise throughout.
- `ContinuousMap.Homotopy.symm`: reverses a single homotopy from $f_0$ to $f_1$ into one from $f_1$ to $f_0$, rather than concatenating two homotopies.
- Path concatenation (`Path.trans`): concatenation of paths (continuous maps from $[0,1]$ to a space with fixed endpoints), which is the special case $X = \{*\}$ of homotopy concatenation but lives in a different type.
