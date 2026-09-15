## VTask.copy

### Object

Given a continuous linear map `f : M₁ →SL[σ₁₂] M₂` and an ordinary function `f' : M₁ → M₂` that is propositionally equal to the underlying function of `f`, `VTask.copy` produces a new continuous linear map whose underlying function is definitionally `f'` (rather than the coercion of `f`). The resulting map is equal to `f` as a continuous linear map, but its `toFun` field is literally `f'`. This construction is useful when a proof or definition requires a specific function to appear definitionally in the `toFun` slot, avoiding the need for cast or transport steps elsewhere.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {R₁ : Type u_1} -> {R₂ : Type u_2} -> [Semiring R₁] -> [Semiring R₂] -> {σ₁₂ : R₁ →+* R₂} -> {M₁ : Type u_4} -> [TopologicalSpace M₁] -> [AddCommMonoid M₁] -> {M₂ : Type u_6} -> [TopologicalSpace M₂] -> [AddCommMonoid M₂] -> [Module R₁ M₁] -> [Module R₂ M₂] -> (f : M₁ →SL[σ₁₂] M₂) -> (f' : M₁ → M₂) -> (h : f' = ⇑f) -> M₁ →SL[σ₁₂] M₂
<!-- PINNED-SIGNATURE:END -->


VTask.copy : {R₁ : Type u_1} -> {R₂ : Type u_2} -> [Semiring R₁] -> [Semiring R₂] -> {σ₁₂ : R₁ →+* R₂} -> {M₁ : Type u_4} -> [TopologicalSpace M₁] -> [AddCommMonoid M₁] -> {M₂ : Type u_6} -> [TopologicalSpace M₂] -> [AddCommMonoid M₂] -> [Module R₁ M₁] -> [Module R₂ M₂] -> (f : M₁ →SL[σ₁₂] M₂) -> (f' : M₁ → M₂) -> (h : f' = ⇑f) -> M₁ →SL[σ₁₂] M₂

`f` is the original continuous linear map being copied. `f'` is the new bare function that will serve as the `toFun` of the copy; it must be propositionally equal to the coercion of `f`. `h` is the proof that `f'` equals the coercion `⇑f`, which guarantees the copy retains all linearity and continuity properties. The remaining arguments (`R₁`, `R₂`, `σ₁₂`, `M₁`, `M₂`, and their typeclass instances) supply the algebraic and topological structure in which `f` lives.

### Conventions

There are no junk-value or boundary conventions for this definition: it is a total construction requiring an explicit proof `h` that the supplied function equals the original, so there are no edge inputs producing degenerate or undefined output.

### Worked examples

- Claim: For any continuous linear map `f`, the coercion of `VTask.copy f (⇑f) rfl` is definitionally `⇑f`.

- Claim: For any continuous linear map `f`, `VTask.copy f (⇑f) rfl = f` as continuous linear maps (by `copy_eq`).

- Claim: If `f' = ⇑f` and we form `g = VTask.copy f f' h`, then `⇑g = f'` (by `coe_copy`).

### Boundaries

- The proof `h : f' = ⇑f` must go in the direction `f' = ⇑f` (not `⇑f = f'`); the types enforce this convention.
- The copy is propositionally equal to the original (`copy_eq`), so it carries all the same mathematical content — the only difference is definitional in the `toFun` field.
- When `f'` is literally `⇑f` and `h` is `rfl`, the copy is the canonical self-copy and is trivially equal to `f`.
- No structural information about `f` is lost or changed: linearity, continuity, and the ring homomorphism `σ₁₂` all carry over unchanged.

### Not to be confused with

- `LinearMap.copy`: The analogous construction for bare linear maps (without topology/continuity), which replaces `toFun` without requiring continuity.
- Direct coercion `⇑f`: Simply extracts the underlying function of `f` without creating a new `ContinuousLinearMap` object.
- `ContinuousLinearMap.mk`: Constructs a continuous linear map from scratch with explicit data, rather than wrapping an existing one with a definitional alias for its function.