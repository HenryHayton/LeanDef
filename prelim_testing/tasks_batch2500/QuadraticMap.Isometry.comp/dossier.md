## Object

Given two isometries of quadratic maps — one from `Q₁` to `Q₂` and one from `Q₂` to `Q₃` — `VTask.comp` produces their composite isometry from `Q₁` to `Q₃`. An isometry of quadratic maps is a linear bijection between the underlying modules that preserves the quadratic form values. The composition is the usual function composition on the underlying maps, and it inherits both linearity and the quadratic-form-preservation property from the two factors.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {R : Type u_1} -> {M₁ : Type u_3} -> {M₂ : Type u_4} -> {M₃ : Type u_5} -> {N : Type u_7} -> [CommSemiring R] -> [AddCommMonoid M₁] -> [AddCommMonoid M₂] -> [AddCommMonoid M₃] -> [AddCommMonoid N] -> [Module R M₁] -> [Module R M₂] -> [Module R M₃] -> [Module R N] -> {Q₁ : QuadraticMap R M₁ N} -> {Q₂ : QuadraticMap R M₂ N} -> {Q₃ : QuadraticMap R M₃ N} -> (g : Q₂ →qᵢ Q₃) -> (f : Q₁ →qᵢ Q₂) -> Q₁ →qᵢ Q₃
<!-- PINNED-SIGNATURE:END -->


VTask.comp : {R : Type u_1} -> {M₁ : Type u_3} -> {M₂ : Type u_4} -> {M₃ : Type u_5} -> {N : Type u_7} -> [CommSemiring R] -> [AddCommMonoid M₁] -> [AddCommMonoid M₂] -> [AddCommMonoid M₃] -> [AddCommMonoid N] -> [Module R M₁] -> [Module R M₂] -> [Module R M₃] -> [Module R N] -> {Q₁ : QuadraticMap R M₁ N} -> {Q₂ : QuadraticMap R M₂ N} -> {Q₃ : QuadraticMap R M₃ N} -> (g : Q₂ →qᵢ Q₃) -> (f : Q₁ →qᵢ Q₂) -> Q₁ →qᵢ Q₃

The scalar ring `R` acts on all modules; `M₁`, `M₂`, `M₃` are the domain modules of the three quadratic maps, and `N` is the common codomain module in which the quadratic form values live. The implicit arguments `Q₁`, `Q₂`, `Q₃` are the three quadratic maps involved. The first explicit argument `g` is the outer isometry from `Q₂` to `Q₃`; the second explicit argument `f` is the inner isometry from `Q₁` to `Q₂`. The result is the composite isometry from `Q₁` to `Q₃`, which applies `f` first and then `g`.

## Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a total construction on well-typed inputs, and every combination of valid isometries produces a valid composite isometry with no degenerate cases.

## Worked examples

- Claim: For any quadratic map isometry `f : Q₁ →qᵢ Q₂` and `g : Q₂ →qᵢ Q₃`, the underlying function of `VTask.comp g f` maps a point `x` in `M₁` to `g (f x)` in `M₃`.

- Claim: `VTask.comp g f` preserves the quadratic form, meaning `Q₃ (VTask.comp g f x) = Q₁ x` for all `x`, since `f` satisfies `Q₂ (f x) = Q₁ x` and `g` satisfies `Q₃ (g y) = Q₂ y`, so chaining gives `Q₃ ((VTask.comp g f) x) = Q₃ (g (f x)) = Q₂ (f x) = Q₁ x`.

- Claim: The composition of isometries is associative: for isometries `f : Q₁ →qᵢ Q₂`, `g : Q₂ →qᵢ Q₃`, `h : Q₃ →qᵢ Q₄`, the isometries `VTask.comp (VTask.comp h g) f` and `VTask.comp h (VTask.comp g f)` have the same underlying function.

- Claim: Composing any isometry `f : Q₁ →qᵢ Q₂` with the identity isometry on `Q₂` on the left yields an isometry with the same underlying function as `f`.

## Boundaries

- The definition is entirely well-behaved on all valid inputs: there are no domain restrictions or exceptional inputs. The composition of two isometries is always an isometry.
- If either `g` or `f` is the identity isometry (identity linear map that fixes the quadratic form trivially), the composition reduces to the other factor as a function, modulo definitional equality of the bundled structure.
- The construction works over any `CommSemiring`, not just fields, so no invertibility or characteristic assumptions on `R` are needed.
- The modules `M₁`, `M₂`, `M₃` need not be finite-dimensional.

## Not to be confused with

- `QuadraticMap.IsometryEquiv.trans`: the analogue for quadratic-map *equivalences* (invertible isometries), which additionally tracks the inverse map.
- Composition of `LinearMap`s (`LinearMap.comp`): that composes the underlying linear maps but does not carry the quadratic-form-preservation property.
- `QuadraticMap.comp`: this composes a quadratic map with a linear map to produce a new *quadratic map*, not an isometry between quadratic maps.