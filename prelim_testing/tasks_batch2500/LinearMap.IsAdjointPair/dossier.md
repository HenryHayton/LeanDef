## Object

`VTask.IsAdjointPair B B' f g` is the proposition that the maps `f : M → M₁` and `g : M₁ → M` are *mutually adjoint* with respect to the sesquilinear forms `B` on `M` and `B'` on `M₁`. Concretely, this means that for every element `x` of `M` and every element `y` of `M₁`, applying `f` on the left argument of `B'` is the same as applying `g` on the right argument of `B`:

> B'(f(x), y) = B(x, g(y))  for all x ∈ M, y ∈ M₁.

This is the natural generalization of the classical notion of adjoint linear maps familiar from linear algebra and functional analysis: if one thinks of a bilinear (or sesquilinear) form as an inner product, then `f` and `g` are adjoints of each other in exactly the sense that ⟨f(x), y⟩ = ⟨x, g(y)⟩.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsAdjointPair : {R : Type u_1} -> {M : Type u_5} -> {M₁ : Type u_6} -> {M₃ : Type u_8} -> [CommSemiring R] -> [AddCommMonoid M] -> [Module R M] -> [AddCommMonoid M₁] -> [Module R M₁] -> [AddCommMonoid M₃] -> [Module R M₃] -> {I : R →+* R} -> (B : M →ₗ[R] M →ₛₗ[I] M₃) -> (B' : M₁ →ₗ[R] M₁ →ₛₗ[I] M₃) -> (f : M → M₁) -> (g : M₁ → M) -> Prop
<!-- PINNED-SIGNATURE:END -->


VTask.IsAdjointPair : {R : Type u_1} -> {M : Type u_5} -> {M₁ : Type u_6} -> {M₃ : Type u_8} -> [CommSemiring R] -> [AddCommMonoid M] -> [Module R M] -> [AddCommMonoid M₁] -> [Module R M₁] -> [AddCommMonoid M₃] -> [Module R M₃] -> {I : R →+* R} -> (B : M →ₗ[R] M →ₛₗ[I] M₃) -> (B' : M₁ →ₗ[R] M₁ →ₛₗ[I] M₃) -> (f : M → M₁) -> (g : M₁ → M) -> Prop

`R` is the commutative semiring of scalars, `M` and `M₁` are the source and target modules, and `M₃` is the codomain module in which the forms take their values. The ring homomorphism `I : R →+* R` is the twist (semi-linearity) used in both bilinear forms. `B` is the sesquilinear form on `M` (bilinear in the first argument over `R`, semi-linear in the second with respect to `I`). `B'` is the sesquilinear form on `M₁` of the same type. `f` is the forward map from `M` to `M₁` and `g` is the reverse map from `M₁` to `M`; together they form the proposed adjoint pair.

## Conventions

No junk-value or boundary conventions are declared for this definition: it is a universally quantified proposition with no undefined or degenerate inputs — every choice of `B`, `B'`, `f`, `g` yields a well-formed `Prop`, even when the maps are zero, the identity, or the forms are degenerate.

## Worked examples

- Claim: The zero map and the zero map form an adjoint pair with respect to any two sesquilinear forms `B` and `B'` (since both sides of the defining equation become 0).

- Claim: The identity map on `M` and itself form an adjoint pair with respect to any sesquilinear form `B` on `M` (i.e., `VTask.IsAdjointPair B B id id`), because `B(id(x), y) = B(x, y) = B(x, id(y))`.

- Claim: If `f` and `g` are adjoint with respect to `B` and `B'`, and `f'` and `g'` are adjoint with respect to `B'` and `B''`, then `f' ∘ f` and `g ∘ g'` are adjoint with respect to `B` and `B''` (adjoint pairs compose).

- Claim: For inner product spaces `E` and `F` over `𝕜`, and a continuous linear map `A : E →L[𝕜] F`, the pair `(A, A†)` satisfies `VTask.IsAdjointPair` for the inner-product-derived sesquilinear forms, recovering the classical Hilbert-space adjoint.

## Boundaries

- When both `f` and `g` are the zero map, the condition holds trivially for any `B`, `B'`, because both sides equal zero.
- When `B` or `B'` is the zero form, the condition again holds for any `f`, `g`.
- The condition is not symmetric in `f` and `g` in general: `VTask.IsAdjointPair B B' f g` and `VTask.IsAdjointPair B' B g f` are different propositions (though they are equivalent when `B = B'` and the forms are symmetric).
- When `M = M₁` and `f = g`, the condition specialises to self-adjointness of `f` with respect to `B`.
- The proposition is well-formed even when `f` or `g` are not linear; linearity is not required by the type, though in practice the interesting cases have `f` and `g` linear.

## Not to be confused with

- `Matrix.IsAdjointPair`: the matrix-level version of the same concept, asserting `Jᵀ A' = Aᵀ J` for matrices; related by the `isAdjointPair_toLinearMap₂` equivalence.
- `LinearMap.BilinForm.IsSymm` / symmetry of a single form: asks whether `B(x, y) = B(y, x)`, not whether two maps intertwine two forms.
- `LinearMap.IsSkewAdjoint`: the condition `B(f(x), y) = -B(x, f(y))`, i.e., adjointness with a sign flip, equivalent to `VTask.IsAdjointPair (-B) B f f`.