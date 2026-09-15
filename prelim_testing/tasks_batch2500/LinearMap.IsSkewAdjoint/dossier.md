## Object

Let `M` be a module over a commutative ring `R`, and let `B : M × M → M₂` be a bilinear map (presented as a linear map into linear maps). An `R`-linear endomorphism `f : M → M` is called **skew-adjoint** with respect to `B` if `B(f(x), y) = -B(x, f(y))` for all `x, y : M`. Equivalently, the negation `-f` acts as a (self-)adjoint of `f` under `B`.

This generalises the classical notion of a skew-adjoint (skew-symmetric, or anti-self-adjoint) operator: for a bilinear form `B` playing the role of an inner product, the condition says that transposing `f` to the other argument flips the sign.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsSkewAdjoint : {R : Type u_1} -> {M : Type u_5} -> {M₂ : Type u_7} -> [CommRing R] -> [AddCommGroup M] -> [Module R M] -> [AddCommGroup M₂] -> [Module R M₂] -> (B : M →ₗ[R] M →ₗ[R] M₂) -> (f : M → M) -> Prop
<!-- PINNED-SIGNATURE:END -->


The type string is inserted automatically above.

- `R` is the commutative ring of scalars.
- `M` is the module whose endomorphisms are under consideration.
- `M₂` is the target module in which the bilinear form takes values.
- The instances `[CommRing R]`, `[AddCommGroup M]`, `[Module R M]`, `[AddCommGroup M₂]`, `[Module R M₂]` equip these types with their algebraic structures.
- `B : M →ₗ[R] M →ₗ[R] M₂` is the bilinear map (the "form") with respect to which adjointness is measured.
- `f : M → M` is the endomorphism being tested for skew-adjointness.

## Conventions

No junk-value or edge-case conventions are declared for this predicate: it is a `Prop` that is simply true or false for any given `B` and `f`, with no special conventions for degenerate inputs.

## Worked examples

- Claim: For the zero bilinear map `B = 0`, every endomorphism `f` satisfies `VTask.IsSkewAdjoint 0 f`, because `B(f(x), y) = 0 = -0 = -B(x, f(y))` for all `x, y`.

- Claim: For a non-degenerate symmetric bilinear form `B` (e.g., the standard dot product on `ℝⁿ`), the identity map `id` is NOT skew-adjoint unless `B` is identically zero, since `B(x, y) = -B(x, y)` would force `2B(x,y) = 0` for all `x, y`.

- Claim: For an alternating bilinear form `B` (satisfying `B(x, x) = 0` for all `x`), a map `f` is skew-adjoint with respect to `B` if and only if `B(f(x), y) + B(x, f(y)) = 0` for all `x, y`.

- Claim: If `f` is skew-adjoint with respect to `B`, then `f + f` (i.e., the scalar-two multiple of `f`) satisfies `B((f+f)(x), y) = -B(x, (f+f)(y))` for all `x, y`, so scalar multiples of a skew-adjoint endomorphism remain skew-adjoint.

## Boundaries

- When `B` is the zero bilinear map, every endomorphism is trivially skew-adjoint.
- When `M` is the zero module, the condition is vacuously satisfied for any `B` and `f`.
- The predicate does not require `f` to be `R`-linear; it is stated for `f : M → M` (an arbitrary set-map). In practice, meaningful examples arise when `f` is linear.
- Skew-adjointness is a stronger condition than mere adjointness (self-adjointness): a map that is both self-adjoint and skew-adjoint satisfies `B(f(x),y) = B(x,f(y))` and `B(f(x),y) = -B(x,f(y))`, forcing `2B(x,f(y)) = 0` for all `x, y`.

## Not to be confused with

- **`IsAdjointPair B B f f`** (self-adjointness): requires `B(f(x),y) = B(x,f(y))`; skew-adjointness instead requires the negated version.
- **`IsAdjointPair B₁ B₂ f g`** (general adjoint pair): the general notion where two possibly different bilinear forms and two possibly different maps are involved; `VTask.IsSkewAdjoint B f` is the specialisation to `B₁ = B₂ = B` and `g = -f`.
- **Skew-symmetry of `B`** (the form, not the endomorphism): the property `B(x,y) = -B(y,x)`; this is a condition on `B` itself, not on an endomorphism relative to `B`.