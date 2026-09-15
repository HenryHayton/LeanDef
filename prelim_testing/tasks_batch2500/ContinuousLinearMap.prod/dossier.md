## Object

`VTask.prod f₁ f₂` is the **Cartesian product** of two continuous (bounded) linear maps sharing the same domain and scalar ring. Given maps `f₁ : M₁ →L[R] M₂` and `f₂ : M₁ →L[R] M₃`, the result is a single continuous linear map `M₁ →L[R] M₂ × M₃` that sends every vector `x : M₁` to the pair `(f₁ x, f₂ x)` in the product module `M₂ × M₃`. Continuity and linearity of the result follow from those of each component.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prod : {R : Type u_1} -> [Semiring R] -> {M₁ : Type u_2} -> [TopologicalSpace M₁] -> [AddCommMonoid M₁] -> [Module R M₁] -> {M₂ : Type u_3} -> [TopologicalSpace M₂] -> [AddCommMonoid M₂] -> [Module R M₂] -> {M₃ : Type u_4} -> [TopologicalSpace M₃] -> [AddCommMonoid M₃] -> [Module R M₃] -> (f₁ : M₁ →L[R] M₂) -> (f₂ : M₁ →L[R] M₃) -> M₁ →L[R] M₂ × M₃
<!-- PINNED-SIGNATURE:END -->


VTask.prod : {R : Type u_1} -> [Semiring R] -> {M₁ : Type u_2} -> [TopologicalSpace M₁] -> [AddCommMonoid M₁] -> [Module R M₁] -> {M₂ : Type u_3} -> [TopologicalSpace M₂] -> [AddCommMonoid M₂] -> [Module R M₂] -> {M₃ : Type u_4} -> [TopologicalSpace M₃] -> [AddCommMonoid M₃] -> [Module R M₃] -> (f₁ : M₁ →L[R] M₂) -> (f₂ : M₁ →L[R] M₃) -> M₁ →L[R] M₂ × M₃

The scalar type `R` must be a semiring. `M₁` is the shared domain module equipped with a topology; `M₂` and `M₃` are the two target modules, each also carrying a topology and an `R`-module structure. The explicit argument `f₁` is the first component map (landing in `M₂`), and `f₂` is the second component map (landing in `M₃`). The result packages both into a single bounded linear map whose codomain is the product `M₂ × M₃`.

## Conventions

No special junk-value or edge conventions are declared for this definition: it is a total constructor on well-typed inputs and there are no degenerate or boundary inputs requiring a conventional choice.

## Worked examples

- Claim: For any `x : M₁`, applying `VTask.prod f₁ f₂` to `x` yields `(f₁ x, f₂ x)` — the pair of the two component values.

- Claim: Composing `VTask.prod f₁ f₂` on the left with the continuous linear projection `ContinuousLinearMap.fst R M₂ M₃` recovers `f₁`.

- Claim: Composing `VTask.prod f₁ f₂` on the left with the continuous linear projection `ContinuousLinearMap.snd R M₂ M₃` recovers `f₂`.

- Claim: `VTask.prod` respects scalar multiplication: `VTask.prod (c • f₁) (c • f₂) = c • VTask.prod f₁ f₂` for any scalar `c : R` (when the scalar action is compatible).

## Boundaries

- When either `f₁` or `f₂` is the zero map, `VTask.prod 0 f₂` sends every `x` to `(0, f₂ x)`, and `VTask.prod f₁ 0` sends every `x` to `(f₁ x, 0)`; the result is still a valid continuous linear map.
- When both maps are equal (`f₁ = f₂`), the product is the diagonal embedding `x ↦ (f₁ x, f₁ x)`.
- When `M₂` or `M₃` is the trivial module (e.g., `{0}`), the product collapses to an essentially one-dimensional output, but the type and construction remain well-formed.

## Not to be confused with

- `ContinuousLinearMap.prodMap`: takes two maps `f : M₁ →L[R] M₂` and `g : N₁ →L[R] N₂` with *different* domains and forms `M₁ × N₁ →L[R] M₂ × N₂`; here the domain is a product, not a shared single space.
- `LinearMap.prod`: the analogous construction for plain (not necessarily continuous) linear maps; `VTask.prod` additionally guarantees continuity/boundedness.
- `ContinuousLinearMap.coprod` (or `prod` on morphisms into a coproduct): pairs maps *from* two domains into a single codomain, the dual construction to `VTask.prod`.