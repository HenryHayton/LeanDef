## Object

`VTask.prod f g` is the **Cartesian-product incidence algebra** on the product poset `α × β`. Given two incidence algebras `f` over `α` and `g` over `β` (both with coefficients in a ring `𝕜`), the product algebra evaluates at a pair of intervals componentwise: its value at pairs of elements `(a₁, b₁)` and `(a₂, b₂)` is the product (in `𝕜`) of `f a₁ a₂` and `g b₁ b₂`. The construction is well-defined as an incidence algebra because if `(a₁, b₁) ≰ (a₂, b₂)` in the product order, then either `a₁ ≰ a₂` or `b₁ ≰ b₂`, and the corresponding factor vanishes.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prod : {𝕜 : Type u_2} -> {α : Type u_5} -> {β : Type u_6} -> [Ring 𝕜] -> [Preorder α] -> [Preorder β] -> (f : IncidenceAlgebra 𝕜 α) -> (g : IncidenceAlgebra 𝕜 β) -> IncidenceAlgebra 𝕜 (α × β)
<!-- PINNED-SIGNATURE:END -->


`VTask.prod : {𝕜 : Type u_2} -> {α : Type u_5} -> {β : Type u_6} -> [Ring 𝕜] -> [Preorder α] -> [Preorder β] -> (f : IncidenceAlgebra 𝕜 α) -> (g : IncidenceAlgebra 𝕜 β) -> IncidenceAlgebra 𝕜 (α × β)`

The implicit type `𝕜` is the coefficient ring, equipped with a `Ring` instance. The implicit types `α` and `β` are the two posets (each carrying a `Preorder`). The argument `f` is an incidence algebra over `α` with coefficients in `𝕜`. The argument `g` is an incidence algebra over `β` with coefficients in `𝕜`. The result is an incidence algebra over the product poset `α × β`.

## Conventions

There are no junk-value or boundary conventions to declare: the construction is total and well-defined for all inputs in its domain — whenever `(a₁, b₁) ≰ (a₂, b₂)` the result is zero by the defining property of the factor incidence algebras, so no sentinel value is needed.

## Worked examples

- Claim: For the zeta algebra `ζ` on a poset, `VTask.prod ζ ζ` evaluated at `((a₁, b₁), (a₂, b₂))` equals `ζ a₁ a₂ * ζ b₁ b₂`.

- Claim: `VTask.prod f g` satisfies the multiplicativity identity: `VTask.prod f₁ g₁ * VTask.prod f₂ g₂ = VTask.prod (f₁ * f₂) (g₁ * g₂)`. This is the central structural fact — the product construction is a ring homomorphism in each factor simultaneously.

- Claim: When `f` and `g` are both the unit element `1` in their respective incidence algebras, `VTask.prod 1 1` equals `1` in `IncidenceAlgebra 𝕜 (α × β)` (assuming `DecidableEq` on both index types).

- Claim: The Möbius function on `α × β` equals `VTask.prod (μ 𝕜) (μ 𝕜)`, i.e., the product of the Möbius functions on each factor. This is the incidence-algebra analogue of the product formula for Möbius functions on product posets.

## Boundaries

- **Non-comparable pairs**: If `(a₁, b₁) ≰ (a₂, b₂)` in the product order — which means `a₁ ≰ a₂` or `b₁ ≰ b₂` — then `VTask.prod f g (a₁, b₁) (a₂, b₂) = 0`, because the respective factor (`f a₁ a₂` or `g b₁ b₂`) is zero, so the product is zero.
- **Diagonal elements**: At equal pairs `(a, b) = (a, b)`, the value is `f a a * g b b`, which for the zeta algebra is `1 * 1 = 1`.
- **Empty/trivial posets**: The construction is valid even when `α` or `β` has a single element; in that case the product algebra degenerates to essentially one copy of the other factor.

## Not to be confused with

- `IncidenceAlgebra.zeta_prod_zeta`: a *theorem* asserting that `VTask.prod ζ ζ = ζ` on the product type; not the construction itself.
- The direct product of rings `𝕜 × 𝕜`: `VTask.prod` forms a product of algebras over a *single* ring `𝕜`, not a product of the rings themselves.
- Pointwise multiplication of two incidence algebras on the *same* poset: `VTask.prod f g` lives on `α × β`, whereas `f * g` (convolution) lives on `α` alone.