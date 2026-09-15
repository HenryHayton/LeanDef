## Object

The **orthogonal complement** of a submodule $K$ of an inner-product space $E$ over a scalar field $\mathbb{k}$ (which is either $\mathbb{R}$ or $\mathbb{C}$). It is the collection of all vectors $v \in E$ such that $\langle u, v \rangle = 0$ for every $u \in K$. This set is itself a submodule of $E$, often written $K^{\perp}$.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.orthogonal : {𝕜 : Type u_1} -> {E : Type u_2} -> [RCLike 𝕜] -> [NormedAddCommGroup E] -> [InnerProductSpace 𝕜 E] -> (K : Submodule 𝕜 E) -> Submodule 𝕜 E
<!-- PINNED-SIGNATURE:END -->


`VTask.orthogonal : {𝕜 : Type u_1} -> {E : Type u_2} -> [RCLike 𝕜] -> [NormedAddCommGroup E] -> [InnerProductSpace 𝕜 E] -> (K : Submodule 𝕜 E) -> Submodule 𝕜 E`

The implicit type `𝕜` is the scalar field, which must satisfy the `RCLike` typeclass (covering $\mathbb{R}$ and $\mathbb{C}$). The implicit type `E` is the ambient vector space, which must carry both a norm (`NormedAddCommGroup`) and a compatible inner product (`InnerProductSpace 𝕜 E`). The explicit argument `K` is the submodule whose orthogonal complement is to be formed. The result is a new submodule of `E` over the same scalars `𝕜`.

## Conventions

The inner product used to define membership is $\langle u, v \rangle$ where $u$ ranges over $K$ and $v$ is the candidate vector — i.e., the submodule element appears in the **first** slot and the candidate in the **second** slot of the inner product, following the convention that the inner product is conjugate-linear in the first argument (the physicist / Mathlib convention).

## Worked examples

- Claim: The zero vector belongs to `VTask.orthogonal K` for any submodule `K`, since $\langle u, 0 \rangle = 0$ for all $u$.

- Claim: If $v \in K$ and $v \in \text{VTask.orthogonal}\, K$, then $\langle v, v \rangle = 0$, which in a (semi-)definite inner product space forces $v = 0$. In particular, $K \cap K^{\perp} = \{0\}$ when the inner product is definite.

- Claim: For the whole space `⊤ : Submodule 𝕜 E`, its orthogonal complement `VTask.orthogonal ⊤` equals `⊥` (only the zero vector satisfies $\langle u, v \rangle = 0$ for all $u$ when the inner product is non-degenerate).

- Claim: For the zero submodule `⊥ : Submodule 𝕜 E`, its orthogonal complement `VTask.orthogonal ⊥` equals `⊤` (every vector is orthogonal to the zero vector, so every vector lies in $(\{0\})^{\perp}$).

## Boundaries

- The construction is defined for **any** submodule `K`, including `⊤` and `⊥`, with no domain restriction.
- The result is always a submodule (not merely a subset), closed under addition and scalar multiplication.
- The zero vector always lies in `VTask.orthogonal K`, so the result is never empty.
- For infinite-dimensional spaces the double orthogonal complement $K^{\perp\perp}$ may properly contain $K$ (it equals the closure of $K$ in the norm topology), so $K^{\perp\perp} = K$ holds in general only when $K$ is closed.
- The orthogonality condition is checked against the **closed** linear span of $K$ in the sense that a vector orthogonal to every generator of $K$ is automatically in $K^{\perp}$.

## Not to be confused with

- **`Submodule.orthogonalComplement`** or the notation `Kᗮ` for the same object — these are just notation/aliases for this same construction.
- **`LinearMap.ker` of the adjoint** — while related by the rank–nullity / Fredholm alternative, the orthogonal complement as defined here is purely in terms of inner product, not in terms of linear maps.
- **`compl` of a submodule** — the lattice complement `K` in the submodule lattice is a purely algebraic notion and does not coincide with the orthogonal complement except in special cases.