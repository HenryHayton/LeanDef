## VTask.linearMapOfLE

### Object

Given a family of normed modules `E` indexed by a type `α` and an exponent comparison `p ≤ q` (where `p` and `q` are extended non-negative reals), `VTask.linearMapOfLE` is the canonical inclusion of the `lp` space with exponent `p` into the `lp` space with exponent `q`, viewed as a `𝕜`-linear map. Concretely, every sequence (or function) that is `p`-summable is also `q`-summable when `p ≤ q`, and this map packages that inclusion as a linear map, preserving the underlying function pointwise.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.linearMapOfLE : (𝕜 : Type u_1) -> {α : Type u_3} -> (E : α → Type u_4) -> [(i : α) → NormedAddCommGroup (E i)] -> [NormedRing 𝕜] -> [(i : α) → Module 𝕜 (E i)] -> [∀ (i : α), IsBoundedSMul 𝕜 (E i)] -> {p q : ENNReal} -> (h : p ≤ q) -> ↥(lp E p) →ₗ[𝕜] ↥(lp E q)
<!-- PINNED-SIGNATURE:END -->


`VTask.linearMapOfLE : (𝕜 : Type u_1) -> {α : Type u_3} -> (E : α → Type u_4) -> [(i : α) → NormedAddCommGroup (E i)] -> [NormedRing 𝕜] -> [(i : α) → Module 𝕜 (E i)] -> [∀ (i : α), IsBoundedSMul 𝕜 (E i)] -> {p q : ENNReal} -> (h : p ≤ q) -> ↥(lp E p) →ₗ[𝕜] ↥(lp E q)`

- `𝕜` is the scalar field (a normed ring with a bounded scalar multiplication action on each fibre).
- `α` is the index type over which the family is defined.
- `E` is the family of normed modules, one for each index in `α`.
- The bracketed arguments are typeclass instances: normed additive commutative group structures on each `E i`, a normed ring structure on `𝕜`, module structures for the scalar action, and bounded scalar multiplication assumptions.
- `p` and `q` are extended non-negative real exponents (elements of `ℝ≥0∞`).
- `h` is the proof that `p ≤ q`, which witnesses that `lp E p` embeds into `lp E q`.

The result is a `𝕜`-linear map from the `lp` space at exponent `p` to the `lp` space at exponent `q`.

### Conventions

The map acts as the identity on the underlying functions: applying `VTask.linearMapOfLE` to an element `f : lp E p` and then coercing to a function yields the same function as coercing `f` directly. This means the inclusion is purely at the level of membership/subtype structure, with no modification of values.

### Worked examples

- Claim: For any `f : lp E p` and a proof `h : p ≤ q`, the underlying function of `VTask.linearMapOfLE 𝕜 E h f` equals the underlying function of `f`; that is, `⇑(VTask.linearMapOfLE 𝕜 E h f) = ⇑f`.

- Claim: Composing two such inclusion maps is the same as the single inclusion for the composed inequality: `(VTask.linearMapOfLE 𝕜 E hqr).comp (VTask.linearMapOfLE 𝕜 E hpq) = VTask.linearMapOfLE 𝕜 E (hpq.trans hqr)` for `p ≤ q ≤ r`.

- Claim: The underlying `AddMonoidHom` of `VTask.linearMapOfLE 𝕜 E h` coincides with the `AddSubgroup.inclusion` map determined by the monotonicity of `lp` in its exponent.

### Boundaries

- When `p = q`, the map `VTask.linearMapOfLE 𝕜 E (le_refl p)` is the identity linear map on `lp E p` (pointwise the same element).
- The exponent `p` may be `0`, `∞`, or any finite positive value in `ℝ≥0∞`; the definition is stated for all valid `ENNReal` exponents without restriction.
- The scalar field `𝕜` need only be a normed ring with bounded scalar multiplication; full field structure is not required.
- The map is injective (since it is the identity on underlying functions), but it need not be surjective unless `p = q`.

### Not to be confused with

- `AddSubgroup.inclusion` for `lp` spaces: that is the corresponding additive subgroup map; `VTask.linearMapOfLE` lifts this to a `𝕜`-linear map.
- The norm-preserving or isometric embedding between `lp` spaces: `VTask.linearMapOfLE` is merely a linear map and does not assert any norm inequality or isometry.
- `lp.monotone`: that is the statement that `lp E p ≤ lp E q` as `AddSubgroup`s; `VTask.linearMapOfLE` uses this fact but is itself a linear map, not a subgroup inclusion proof.