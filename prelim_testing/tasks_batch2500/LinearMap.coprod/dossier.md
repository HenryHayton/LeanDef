## Object

`VTask.coprod f g` is the **copairing** (or coproduct map) of two linear maps that share a common codomain. Given linear maps `f : M →ₗ[R] M₃` and `g : M₂ →ₗ[R] M₃`, it produces the linear map `M × M₂ →ₗ[R] M₃` that sends a pair `(x, y)` to `f x + g y`. This is the canonical map out of a direct product (viewed as a biproduct) induced by two maps into the same target module.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.coprod : {R : Type u} -> {M : Type v} -> {M₂ : Type w} -> {M₃ : Type y} -> [Semiring R] -> [AddCommMonoid M] -> [AddCommMonoid M₂] -> [AddCommMonoid M₃] -> [Module R M] -> [Module R M₂] -> [Module R M₃] -> (f : M →ₗ[R] M₃) -> (g : M₂ →ₗ[R] M₃) -> M × M₂ →ₗ[R] M₃
<!-- PINNED-SIGNATURE:END -->


VTask.coprod : {R : Type u} -> {M : Type v} -> {M₂ : Type w} -> {M₃ : Type y} -> [Semiring R] -> [AddCommMonoid M] -> [AddCommMonoid M₂] -> [AddCommMonoid M₃] -> [Module R M] -> [Module R M₂] -> [Module R M₃] -> (f : M →ₗ[R] M₃) -> (g : M₂ →ₗ[R] M₃) -> M × M₂ →ₗ[R] M₃

The scalar semiring `R` governs the module structures throughout. `M` and `M₂` are the two source modules forming the product domain; `M₃` is the shared target module. The first explicit argument `f` is the linear map applied to the left component of the pair; the second explicit argument `g` is the linear map applied to the right component. The result is a single linear map on the product whose value at `(x, y)` is `f x + g y`.

## Conventions

No junk-value or edge conventions are declared for this definition: it is a totally defined constructor of a linear map, with no special treatment required at boundary inputs.

## Worked examples

- Claim: Applying `VTask.coprod f g` to a pair `(x, y)` yields `f x + g y`, so in particular if `f` and `g` are both the identity on a module `M = M₂ = M₃`, then `VTask.coprod LinearMap.id LinearMap.id` sends `(x, y)` to `x + y`.

- Claim: If `f` is the zero map and `g` is the zero map, then `VTask.coprod (0 : M →ₗ[R] M₃) (0 : M₂ →ₗ[R] M₃)` is the zero map on `M × M₂`, because `0 x + 0 y = 0` for all `(x, y)`.

- Claim: `VTask.coprod f g` is linear in `f`: for linear maps `f₁ f₂ : M →ₗ[R] M₃` and `g : M₂ →ₗ[R] M₃`, `VTask.coprod (f₁ + f₂) g = VTask.coprod f₁ g + VTask.coprod f₂ g` as linear maps `M × M₂ →ₗ[R] M₃`, since `(f₁ + f₂) x + g y = f₁ x + f₂ x + g y`.

- Claim: `VTask.coprod f g` applied to `(x, 0)` equals `f x`, since `f x + g 0 = f x + 0 = f x`.

## Boundaries

- When either `f` or `g` is the zero linear map, the result reduces to the composition of the other map with the appropriate projection: `VTask.coprod 0 g` maps `(x, y)` to `g y`, and `VTask.coprod f 0` maps `(x, y)` to `f x`.
- The definition is valid over any semiring `R` (not only rings or fields), since addition in `M₃` is all that is needed beyond the module axioms.
- There is no restriction on the relationship between `M`, `M₂`, and `M₃`; they may all be distinct or coincide.

## Not to be confused with

- `LinearMap.prod` (or `VTask.prod`): constructs a map *into* a product `M₃ × M₄` from two maps with the same domain, i.e., the dual pairing `x ↦ (f x, g x)` — the direction is reversed compared to `coprod`.
- `LinearMap.inl` / `LinearMap.inr`: the canonical injections into a product module `M × M₂`, which are the adjoints/co-units; `coprod` is the universal map *out* of a product induced by these.
- `LinearMap.comp`: plain composition of two linear maps in sequence, not the sum-of-components construction that `coprod` performs.