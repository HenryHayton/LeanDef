## VTask.compAlternatingMap

### Object

Given a linear map `g : N →ₗ[R] N₂` and an alternating multilinear map `f : M [⋀^ι]→ₗ[R] N`, their composition `g ∘ f` is again an alternating multilinear map from `M` (indexed by `ι`) to `N₂`. Concretely, the composed map sends a family of vectors `(v i)_{i : ι}` to `g(f(v))`, and this composition inherits both the multilinearity and the alternating property (the output is zero whenever two inputs coincide) from `f`, while the linearity of `g` preserves those properties.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.compAlternatingMap : {R : Type u_1} -> [Semiring R] -> {M : Type u_2} -> [AddCommMonoid M] -> [Module R M] -> {N : Type u_3} -> [AddCommMonoid N] -> [Module R N] -> {ι : Type u_7} -> {N₂ : Type u_11} -> [AddCommMonoid N₂] -> [Module R N₂] -> (g : N →ₗ[R] N₂) -> (f : M [⋀^ι]→ₗ[R] N) -> M [⋀^ι]→ₗ[R] N₂
<!-- PINNED-SIGNATURE:END -->


VTask.compAlternatingMap : {R : Type u_1} -> [Semiring R] -> {M : Type u_2} -> [AddCommMonoid M] -> [Module R M] -> {N : Type u_3} -> [AddCommMonoid N] -> [Module R N] -> {ι : Type u_7} -> {N₂ : Type u_11} -> [AddCommMonoid N₂] -> [Module R N₂] -> (g : N →ₗ[R] N₂) -> (f : M [⋀^ι]→ₗ[R] N) -> M [⋀^ι]→ₗ[R] N₂

`R` is the commutative semiring of scalars. `M` is the common domain module (indexed by `ι`) for the alternating map. `N` is the codomain module of the alternating map `f` and the domain of the linear map `g`. `N₂` is the final codomain module. `ι` is the index type governing the number of arguments. The argument `g` is the linear map applied on the left (after `f`). The argument `f` is the alternating multilinear map applied first to the family of vectors.

### Conventions

No special junk-value or boundary conventions are declared: the definition is total, every valid combination of `g` and `f` produces a well-formed alternating map, and no inputs are treated as "out of domain."

### Worked examples

- Claim: When `g` is the identity linear map `LinearMap.id`, `VTask.compAlternatingMap LinearMap.id f` equals `f` as an alternating map (composing with the identity on the left leaves `f` unchanged).

- Claim: For any alternating map `f : M [⋀^ι]→ₗ[R] N`, linear map `g : N →ₗ[R] N₂`, and a family of vectors `v : ι → M` in which `v i = v j` for some `i ≠ j`, evaluating `VTask.compAlternatingMap g f` at `v` yields zero, since `f v = 0` (alternating property) and `g 0 = 0` (linearity).

- Claim: For composable linear maps `g₁ : N →ₗ[R] N₂` and `g₂ : N₂ →ₗ[R] N₃`, composing in succession satisfies `VTask.compAlternatingMap (g₂.comp g₁) f = VTask.compAlternatingMap g₂ (VTask.compAlternatingMap g₁ f)` as alternating maps (associativity of composition).

### Boundaries

- If `ι` is the empty type, the alternating map `f` is a constant map (it takes no vector arguments), and `VTask.compAlternatingMap g f` simply applies `g` to that constant value.
- If `g` is the zero linear map, then `VTask.compAlternatingMap g f` is the zero alternating map regardless of `f`.
- If `f` is the zero alternating map, then `VTask.compAlternatingMap g f` is the zero alternating map regardless of `g`.
- The definition requires only a `Semiring` on `R` (not a full `CommSemiring` or `Ring`), so it applies in somewhat general algebraic settings.

### Not to be confused with

- `MultilinearMap.compLinearMap` / `LinearMap.compMultilinearMap`: composes a linear map on the left of a *multilinear* (but not necessarily alternating) map; `VTask.compAlternatingMap` specifically preserves and asserts the alternating property.
- Composing an alternating map with a linear map *on the right* (i.e., precomposing each argument slot with a linear map), which changes the domain rather than the codomain.
- `AlternatingMap.compLinearEquiv`: a variant using a linear *equivalence* instead of a mere linear map, which additionally provides invertibility.