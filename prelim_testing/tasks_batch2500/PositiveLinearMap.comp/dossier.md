## Object

`VTask.comp g f` is the composite positive linear map obtained by first applying `f` and then `g`. Both maps are required to be linear and order-preserving (positive), and the result is again a linear, order-preserving map between the outer spaces. In other words, it is the usual composition of functions, packaged together with the proof that the composite of two monotone linear maps is again monotone and linear.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {R : Type u_1} -> {E₁ : Type u_2} -> {E₂ : Type u_3} -> {E₃ : Type u_4} -> [Semiring R] -> [AddCommMonoid E₁] -> [PartialOrder E₁] -> [AddCommMonoid E₂] -> [PartialOrder E₂] -> [AddCommMonoid E₃] -> [PartialOrder E₃] -> [Module R E₁] -> [Module R E₂] -> [Module R E₃] -> (g : E₂ →ₚ[R] E₃) -> (f : E₁ →ₚ[R] E₂) -> E₁ →ₚ[R] E₃
<!-- PINNED-SIGNATURE:END -->


The implicit arguments `R`, `E₁`, `E₂`, `E₃` are, respectively, the scalar semiring and the three ordered modules (source, intermediate, and target). The instance arguments supply the necessary algebraic and order structure. The explicit argument `g : E₂ →ₚ[R] E₃` is the outer (second-applied) positive linear map, and `f : E₁ →ₚ[R] E₂` is the inner (first-applied) positive linear map.

## Conventions

There are no junk-value conventions declared for this definition: it is a total constructor whose inputs are well-typed positive linear maps, and every well-typed input yields a meaningful output.

## Worked examples

- Claim: The underlying linear map of `VTask.comp g f` equals the composition of the underlying linear maps of `g` and `f`, i.e., `(VTask.comp g f).toLinearMap = g.toLinearMap.comp f.toLinearMap`.

- Claim: For any elements `x ≤ y` in `E₁`, applying `VTask.comp g f` satisfies `VTask.comp g f x ≤ VTask.comp g f y`, since monotonicity is preserved under composition.

- Claim: If `g` and `f` are both the identity positive linear map on the same module `E`, then `VTask.comp g f` acts as the identity on `E`.

- Claim: Composition is associative: for positive linear maps `h : E₃ →ₚ[R] E₄`, `g : E₂ →ₚ[R] E₃`, `f : E₁ →ₚ[R] E₂`, the maps `VTask.comp (VTask.comp h g) f` and `VTask.comp h (VTask.comp g f)` agree pointwise on all inputs.

## Boundaries

- The definition is total on well-typed inputs: any two composable positive linear maps (where the codomain of `f` matches the domain of `g`) yield a valid result.
- There are no degenerate or edge cases introduced by the composition itself; the ordering of arguments follows the standard convention that `g` is written on the left (applied second), matching the usual mathematical notation for function composition.
- The scalar semiring `R` need not be commutative or have a unit beyond what is required for a `Semiring`; the construction works in this generality.

## Not to be confused with

- `LinearMap.comp`: the analogous composition for plain linear maps, with no positivity/monotonicity constraint or packaging.
- `OrderHom.comp`: composition of order-homomorphisms (monotone maps) without the linear structure.
- `VTask.comp f g` (arguments swapped): swapping `f` and `g` produces a different map (or a type error if the types are not symmetric), since composition is not commutative.