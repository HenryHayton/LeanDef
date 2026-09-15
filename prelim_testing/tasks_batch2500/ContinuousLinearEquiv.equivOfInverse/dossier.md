## Object

`VTask.equivOfInverse` constructs a **continuous linear equivalence** (a bicontinuous linear isomorphism) between two topological modules from a pair of continuous linear maps that are mutual inverses of each other. Given maps `f₁ : M₁ → M₂` and `f₂ : M₂ → M₁` that are each other's left and right inverse as functions, it packages them together into a single invertible object of type `M₁ ≃SL[σ₁₂] M₂`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.equivOfInverse : {R₁ : Type u_1} -> {R₂ : Type u_2} -> [Semiring R₁] -> [Semiring R₂] -> {σ₁₂ : R₁ →+* R₂} -> {σ₂₁ : R₂ →+* R₁} -> [RingHomInvPair σ₁₂ σ₂₁] -> [RingHomInvPair σ₂₁ σ₁₂] -> {M₁ : Type u_4} -> [TopologicalSpace M₁] -> [AddCommMonoid M₁] -> {M₂ : Type u_5} -> [TopologicalSpace M₂] -> [AddCommMonoid M₂] -> [Module R₁ M₁] -> [Module R₂ M₂] -> (f₁ : M₁ →SL[σ₁₂] M₂) -> (f₂ : M₂ →SL[σ₂₁] M₁) -> (h₁ : Function.LeftInverse ⇑f₂ ⇑f₁) -> (h₂ : Function.RightInverse ⇑f₂ ⇑f₁) -> M₁ ≃SL[σ₁₂] M₂
<!-- PINNED-SIGNATURE:END -->


VTask.equivOfInverse : {R₁ : Type u_1} -> {R₂ : Type u_2} -> [Semiring R₁] -> [Semiring R₂] -> {σ₁₂ : R₁ →+* R₂} -> {σ₂₁ : R₂ →+* R₁} -> [RingHomInvPair σ₁₂ σ₂₁] -> [RingHomInvPair σ₂₁ σ₁₂] -> {M₁ : Type u_4} -> [TopologicalSpace M₁] -> [AddCommMonoid M₁] -> {M₂ : Type u_5} -> [TopologicalSpace M₂] -> [AddCommMonoid M₂] -> [Module R₁ M₁] -> [Module R₂ M₂] -> (f₁ : M₁ →SL[σ₁₂] M₂) -> (f₂ : M₂ →SL[σ₂₁] M₁) -> (h₁ : Function.LeftInverse ⇑f₂ ⇑f₁) -> (h₂ : Function.RightInverse ⇑f₂ ⇑f₁) -> M₁ ≃SL[σ₁₂] M₂

The semirings `R₁` and `R₂` are the scalar rings acting on the two modules; `σ₁₂` is the ring homomorphism from `R₁` to `R₂` giving the semilinear structure of `f₁`, and `σ₂₁` is its inverse ring homomorphism in the other direction, used by `f₂`. The `RingHomInvPair` instances assert that `σ₁₂` and `σ₂₁` are genuinely inverse ring homomorphisms. The types `M₁` and `M₂` are the underlying topological modules. The argument `f₁` is the forward continuous linear map from `M₁` to `M₂`. The argument `f₂` is the backward continuous linear map from `M₂` to `M₁`, intended to be the inverse of `f₁`. The proof `h₁` asserts that `f₂` is a left inverse of `f₁` as functions (i.e., `f₂(f₁(x)) = x` for all `x : M₁`). The proof `h₂` asserts that `f₂` is a right inverse of `f₁` as functions (i.e., `f₁(f₂(y)) = y` for all `y : M₂`).

## Conventions

There are no junk-value or out-of-domain conventions for this definition: all inputs are either types, algebraic structures, or total proofs, and the construction is total whenever the supplied maps genuinely satisfy the inverse conditions.

## Worked examples

- Claim: If `e := VTask.equivOfInverse f₁ f₂ h₁ h₂`, then `e` applied to an element `x : M₁` equals `f₁ x`.

- Claim: If `e := VTask.equivOfInverse f₁ f₂ h₁ h₂`, then the symm of `e` applied to `y : M₂` equals `f₂ y`.

- Claim: For the identity map `id` (as a continuous linear map), `VTask.equivOfInverse id id (fun x => rfl) (fun y => rfl)` is a continuous linear equivalence whose forward and backward maps are both the identity.

## Boundaries

- The function does not verify bijectivity on its own; it trusts the caller-supplied proofs `h₁` and `h₂`. If those proofs are bogus (inconsistent hypotheses), the resulting equivalence would be mathematically unsound, but that is the caller's responsibility.
- Both `f₁` and `f₂` must be continuous linear maps (in the appropriate semilinear sense), not merely set-theoretic functions. Continuity of the inverse is encoded in the type of `f₂`, not separately checked.
- The ring homomorphisms `σ₁₂` and `σ₂₁` must form an inverse pair via the `RingHomInvPair` typeclass; this is a prerequisite for the semilinear structure to be consistent.
- When `R₁ = R₂` and `σ₁₂ = σ₂₁ = RingHom.id`, this specialises to an ordinary (not twisted) continuous linear equivalence.

## Not to be confused with

- `ContinuousLinearEquiv.symm`: extracts the inverse equivalence from an already-existing `ContinuousLinearEquiv`; it does not construct one from scratch from two maps.
- `LinearEquiv.ofLinear` (the linear-algebra analogue without topology): constructs a `LinearEquiv` from two linear maps that are mutual inverses, but ignores continuity.
- `equivOfInverse'` (mentioned in the docstring): a variant constructor for the same type, likely with a different argument order or slightly different hypotheses.