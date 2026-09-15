## Object

`VTask.comp` is the composition of two isometries of bilinear forms. Given a commutative semiring `R`, three `R`-modules `M₁`, `M₂`, `M₃` equipped with bilinear forms `B₁`, `B₂`, `B₃` respectively, and two isometries `f : B₁ →bᵢ B₂` and `g : B₂ →bᵢ B₃`, their composition is an isometry `B₁ →bᵢ B₃` whose underlying map sends each element `x` of `M₁` first through `f` and then through `g`, and which preserves the bilinear form values end-to-end: for all `x, y ∈ M₁`, one has `B₃(g(f(x)), g(f(y))) = B₁(x, y)`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {R : Type u_1} -> {M₁ : Type u_3} -> {M₂ : Type u_4} -> {M₃ : Type u_5} -> [CommSemiring R] -> [AddCommMonoid M₁] -> [AddCommMonoid M₂] -> [AddCommMonoid M₃] -> [Module R M₁] -> [Module R M₂] -> [Module R M₃] -> {B₁ : LinearMap.BilinForm R M₁} -> {B₂ : LinearMap.BilinForm R M₂} -> {B₃ : LinearMap.BilinForm R M₃} -> (g : B₂ →bᵢ B₃) -> (f : B₁ →bᵢ B₂) -> B₁ →bᵢ B₃
<!-- PINNED-SIGNATURE:END -->


VTask.comp : {R : Type u_1} -> {M₁ : Type u_3} -> {M₂ : Type u_4} -> {M₃ : Type u_5} -> [CommSemiring R] -> [AddCommMonoid M₁] -> [AddCommMonoid M₂] -> [AddCommMonoid M₃] -> [Module R M₁] -> [Module R M₂] -> [Module R M₃] -> {B₁ : LinearMap.BilinForm R M₁} -> {B₂ : LinearMap.BilinForm R M₂} -> {B₃ : LinearMap.BilinForm R M₃} -> (g : B₂ →bᵢ B₃) -> (f : B₁ →bᵢ B₂) -> B₁ →bᵢ B₃

The scalar ring `R` and the three carrier types `M₁`, `M₂`, `M₃` are implicit type arguments; their algebraic structures (commutative semiring, additive-commutative monoids, and module structures over `R`) are provided as typeclass instances. The bilinear forms `B₁`, `B₂`, `B₃` are implicit arguments inhabiting the respective `BilinForm` types. The first explicit argument `g` is the outer (second-applied) isometry from `B₂` to `B₃`. The second explicit argument `f` is the inner (first-applied) isometry from `B₁` to `B₂`.

## Conventions

Arguments are in right-to-left (categorical/function-composition) order: `g` is written first and `f` second, so `VTask.comp g f` means "first apply `f`, then apply `g`", matching the usual convention for composition of functions and linear maps.

## Worked examples

- Claim: Composing any isometry `f : B₁ →bᵢ B₂` with the identity isometry on `B₂` on the left yields a map that acts the same as `f` pointwise.

- Claim: Composing the identity isometry on `B₁` on the right of any isometry `f : B₁ →bᵢ B₂` yields a map that acts the same as `f` pointwise.

- Claim: For three isometries `f : B₁ →bᵢ B₂`, `g : B₂ →bᵢ B₃`, `h : B₃ →bᵢ B₄`, the compositions `VTask.comp (VTask.comp h g) f` and `VTask.comp h (VTask.comp g f)` send every `x : M₁` to the same element of `M₄`.

- Claim: The underlying linear map of `VTask.comp g f` sends `x : M₁` to `g (f x) : M₃`.

## Boundaries

- The definition is total: it is valid for any two composable isometries of bilinear forms over any commutative semiring, with no restrictions beyond the typeclass assumptions.
- When `M₁ = M₂ = M₃` and `B₁ = B₂ = B₃`, repeated composition gives a monoid structure on self-isometries; `VTask.comp` is the monoid multiplication in that setting.
- The composition inherits `R`-linearity from both constituent isometries, since the underlying map is the composition of two `R`-linear maps.
- The form-preservation property `B₃(g(f(x)), g(f(y))) = B₁(x, y)` follows by applying `f`'s preservation property and then `g`'s.

## Not to be confused with

- `LinearMap.comp`: composition of bare `R`-linear maps without any bilinear-form structure; `VTask.comp` additionally tracks and preserves bilinear form data.
- `LinearEquiv.trans`: composition of linear *isomorphisms* (invertible linear maps); `VTask.comp` composes isometries of bilinear forms, which need not be invertible as linear maps in general.
- Applying two isometries in sequence without packaging the result: `g (f x)` gives a single element, whereas `VTask.comp g f` gives a new isometry morphism object.