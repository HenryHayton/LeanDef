## Object

`VTask.splitMul 𝕜 A` is the canonical unital `𝕜`-algebra homomorphism from the unitization `Unitization 𝕜 A` into the product algebra `𝕜 × (A →L[𝕜] A)`. Given an element `(k, a) : Unitization 𝕜 A` (a scalar part `k : 𝕜` and a non-unital part `a : A`), the map sends it to the pair consisting of:
- **First component**: the scalar `k : 𝕜` itself.
- **Second component**: the continuous linear map on `A` given by left multiplication by `(k, a)` inside the unitization, i.e., the map `b ↦ k • b + a * b` for `b : A`, viewed as an element of `A →L[𝕜] A`.

This construction realises the unitization as an algebra of "scalar-plus-left-multiplication" operators on `A`, and is the standard way to embed `Unitization 𝕜 A` faithfully into a product of simpler algebras.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.splitMul : (𝕜 : Type u_1) -> (A : Type u_2) -> [NontriviallyNormedField 𝕜] -> [NonUnitalNormedRing A] -> [NormedSpace 𝕜 A] -> [IsScalarTower 𝕜 A A] -> [SMulCommClass 𝕜 A A] -> Unitization 𝕜 A →ₐ[𝕜] 𝕜 × (A →L[𝕜] A)
<!-- PINNED-SIGNATURE:END -->


VTask.splitMul : (𝕜 : Type u_1) -> (A : Type u_2) -> [NontriviallyNormedField 𝕜] -> [NonUnitalNormedRing A] -> [NormedSpace 𝕜 A] -> [IsScalarTower 𝕜 A A] -> [SMulCommClass 𝕜 A A] -> Unitization 𝕜 A →ₐ[𝕜] 𝕜 × (A →L[𝕜] A)

`𝕜` is the scalar field, which must be a nontrivially normed field. `A` is the non-unital normed ring being unitized, which must also be a normed `𝕜`-module with compatible scalar tower and commutativity conditions (`IsScalarTower 𝕜 A A` and `SMulCommClass 𝕜 A A`). The typeclass instances supply the norm and algebraic structure required for continuity of the operators involved.

## Conventions

There are no junk-value or edge conventions declared for this definition: it is a total algebra homomorphism defined on all of `Unitization 𝕜 A`, with no undefined or degenerate inputs.

## Worked examples

- Claim: For `(k, a) : Unitization 𝕜 A`, the first component of `VTask.splitMul 𝕜 A (k, a)` equals `k`.

- Claim: For `(k, a) : Unitization 𝕜 A`, the second component of `VTask.splitMul 𝕜 A (k, a)` applied to `b : A` equals `k • b + a * b`, reflecting the left-multiplication action of the unitization element on `A`.

- Claim: `VTask.splitMul 𝕜 A` is a `𝕜`-algebra homomorphism, so it preserves addition, multiplication, scalar multiplication, and the unit: `VTask.splitMul 𝕜 A 1 = (1, ContinuousLinearMap.id 𝕜 A)` (the identity element maps to `(1, id)`).

- Claim: `VTask.splitMul 𝕜 A` maps the sum of two unitization elements to the sum of their images, i.e., it is additive: `VTask.splitMul 𝕜 A (x + y) = VTask.splitMul 𝕜 A x + VTask.splitMul 𝕜 A y`.

## Boundaries

- When `A = 0` (the trivial non-unital ring), the second component of the map is always the zero operator, and the map collapses to the projection onto the scalar field `𝕜`.
- The first component always extracts the scalar part `k` exactly; it does not depend on `a`.
- The second component is **not** simply `NonUnitalAlgHom.Lmul` applied to `A` on itself, because: (a) `a` alone would miss the scalar shift `k • (-)`, and (b) `NonUnitalAlgHom.Lmul` only produces a non-unital hom, whereas here a unital `AlgHom` is needed.
- The codomain is a product of a field and an operator algebra; the map is a unital `𝕜`-algebra homomorphism into this product, so it respects all ring and `𝕜`-module operations.
- The map is injective when the left-multiplication representation of `Unitization 𝕜 A` on `A` is faithful (which holds in the typical normed-algebra setting).

## Not to be confused with

- `NonUnitalAlgHom.Lmul 𝕜 A`: the left-multiplication map of the non-unital ring `A` acting on itself; this is only a non-unital hom and does not include the scalar-shift component.
- The projection `Unitization.fst`: merely extracts the scalar part `k`, with no information about the `A`-component or the operator it defines.
- `Unitization.lift`: a general construction that lifts a non-unital hom out of `A` to a unital hom out of `Unitization 𝕜 A`; `VTask.splitMul` is built from two applications of `lift` combined into a product, and is a specific instance rather than the general lifting device.