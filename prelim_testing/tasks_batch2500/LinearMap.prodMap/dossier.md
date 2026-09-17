## Object

Given two linear maps `f : M →ₗ[R] M₃` and `g : M₂ →ₗ[R] M₄` over a common semiring `R`, `VTask.prodMap f g` is the linear map from the product module `M × M₂` to the product module `M₃ × M₄` that applies `f` to the first component and `g` to the second component. Concretely, it sends a pair `(m, m₂)` to the pair `(f m, g m₂)`. This is the direct-product (or categorical product) of linear maps.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prodMap : {R : Type u} -> {M : Type v} -> {M₂ : Type w} -> {M₃ : Type y} -> {M₄ : Type z} -> [Semiring R] -> [AddCommMonoid M] -> [AddCommMonoid M₂] -> [AddCommMonoid M₃] -> [AddCommMonoid M₄] -> [Module R M] -> [Module R M₂] -> [Module R M₃] -> [Module R M₄] -> (f : M →ₗ[R] M₃) -> (g : M₂ →ₗ[R] M₄) -> M × M₂ →ₗ[R] M₃ × M₄
<!-- PINNED-SIGNATURE:END -->


VTask.prodMap : {R : Type u} -> {M : Type v} -> {M₂ : Type w} -> {M₃ : Type y} -> {M₄ : Type z} -> [Semiring R] -> [AddCommMonoid M] -> [AddCommMonoid M₂] -> [AddCommMonoid M₃] -> [AddCommMonoid M₄] -> [Module R M] -> [Module R M₂] -> [Module R M₃] -> [Module R M₄] -> (f : M →ₗ[R] M₃) -> (g : M₂ →ₗ[R] M₄) -> M × M₂ →ₗ[R] M₃ × M₄

The first explicit argument `f` is a linear map from the first factor `M` to the first target factor `M₃`. The second explicit argument `g` is a linear map from the second factor `M₂` to the second target factor `M₄`. All type-class arguments supply the algebraic structure (a semiring `R` acting on each of the four modules via the `Module` and `AddCommMonoid` instances).

## Conventions

No junk-value or edge conventions are declared: the function is total and well-behaved for all valid inputs, including identity maps and zero maps.

## Worked examples

- Claim: `VTask.prodMap` applied to a pair `(m, m₂)` returns `(f m, g m₂)` — that is, the output first component equals `f` applied to the input first component.
  (For any semiring `R`, modules `M M₂ M₃ M₄`, linear maps `f : M →ₗ[R] M₃` and `g : M₂ →ₗ[R] M₄`, and any `m : M`, `m₂ : M₂`, we have `(VTask.prodMap f g) (m, m₂) = (f m, g m₂)`.)

- Claim: `VTask.prodMap` of two identity maps is the identity on the product — for modules `M` and `M₂` over `R`, `VTask.prodMap (LinearMap.id) (LinearMap.id) = LinearMap.id`.

- Claim: `VTask.prodMap` of two zero maps is the zero map — for any `f = 0` and `g = 0`, `VTask.prodMap 0 0 = 0` as a linear map `M × M₂ →ₗ[R] M₃ × M₄`.

- Claim: Composing `VTask.prodMap f g` with `VTask.prodMap f' g'` (where the codomains match the domains) equals `VTask.prodMap (f' ∘ₗ f) (g' ∘ₗ g)`.

## Boundaries

- The function is total over all four module types and both linear maps; there are no domain restrictions.
- When either `f` or `g` is the zero linear map, the corresponding output component is always zero.
- When `M` or `M₂` is the trivial module `{0}`, the map still type-checks and behaves as expected (collapsing that component to zero).
- The construction works over any semiring `R`, not just rings or fields, so it applies in the setting of modules over ℕ or semirings like `Bool` as well.

## Not to be confused with

- `LinearMap.prod` (or `VTask.prod`): takes two linear maps `f : M →ₗ[R] M₂` and `g : M →ₗ[R] M₃` sharing the *same domain* and produces a map `M →ₗ[R] M₂ × M₃` by pairing their outputs — a fan-out, not a parallel application.
- `LinearMap.coprod`: takes two linear maps sharing the *same codomain* and produces a map out of a direct sum/product — a fan-in, the dual construction.
- `Prod.map` (the plain function-level version): maps a pair of ordinary functions over a product type, without any linearity structure.