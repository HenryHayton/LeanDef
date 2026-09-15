## 1. Object

Given a continuous multilinear map `g : M₁'₁ × … × M₁'ₙ → M₄` and, for each index `i`, a continuous linear map `fᵢ : M₁ᵢ → M₁'ᵢ`, the object `VTask.compContinuousLinearMap g f` is the continuous multilinear map that sends a tuple `(m₁, …, mₙ)` to `g(f₁(m₁), …, fₙ(mₙ))`. In other words, it is the precomposition of a continuous multilinear map with a family of continuous linear maps, one on each argument slot.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.compContinuousLinearMap : {R : Type u} -> {ι : Type v} -> {M₁ : ι → Type w₁} -> {M₁' : ι → Type w₁'} -> {M₄ : Type w₄} -> [Semiring R] -> [(i : ι) → AddCommMonoid (M₁ i)] -> [(i : ι) → AddCommMonoid (M₁' i)] -> [AddCommMonoid M₄] -> [(i : ι) → Module R (M₁ i)] -> [(i : ι) → Module R (M₁' i)] -> [Module R M₄] -> [(i : ι) → TopologicalSpace (M₁ i)] -> [(i : ι) → TopologicalSpace (M₁' i)] -> [TopologicalSpace M₄] -> (g : ContinuousMultilinearMap R M₁' M₄) -> (f : (i : ι) → M₁ i →L[R] M₁' i) -> ContinuousMultilinearMap R M₁ M₄
<!-- PINNED-SIGNATURE:END -->


The implicit universe and type arguments fix the index type `ι`, the family of source modules `M₁ i`, the family of intermediate modules `M₁' i`, the target module `M₄`, a commutative semiring `R` acting on all of them, additive-commutative-monoid and module structures on every module in the picture, and topological spaces on every module. The explicit arguments are: `g`, the continuous multilinear map from the intermediate family `M₁'` to the target `M₄`; and `f`, the family of continuous linear maps, where `f i` maps from the `i`-th source module `M₁ i` to the `i`-th intermediate module `M₁' i`. The result is a continuous multilinear map from the source family `M₁` to the target `M₄`.

## 3. Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total construction whose output is fully determined by the given algebraic and topological data, with no degenerate edge cases requiring special treatment.

## 4. Worked examples

- Claim: For any continuous multilinear map `g` and family of continuous linear maps `f`, evaluating `VTask.compContinuousLinearMap g f` at a tuple `m` yields the same value as evaluating `g` at the tuple obtained by applying each `f i` to `m i`, i.e., `(VTask.compContinuousLinearMap g f) m = g (fun i => f i (m i))`.

- Claim: If `g` is a continuous multilinear map on a single-variable family and `f` is a single continuous linear map (i.e., `ι` is a one-element type), then `VTask.compContinuousLinearMap g f` applies `f` to the sole argument before passing it to `g`.

- Claim: When every `f i` is the identity continuous linear map on `M₁' i` (so `M₁ i = M₁' i`), the result `VTask.compContinuousLinearMap g (fun i => ContinuousLinearMap.id R (M₁' i))` equals `g`.

## 5. Boundaries

- When `ι` is the empty type, both `g` and the result are continuous multilinear maps on an empty product; the composition is still well-defined and simply equals `g` (with no linear maps applied).
- When some `f i` is the zero map, the corresponding argument slot of the result is always fed the zero element of `M₁' i`, so the composition reflects the multilinearity of `g` in that slot (in particular, the result is the zero map if `g` is zero on inputs with a zero component).
- The construction is defined for any semiring `R` and does not require a field or normed structure; norm estimates (`‖g.compContinuousLinearMap f‖ ≤ ‖g‖ · ∏ᵢ ‖f i‖`) apply additionally when normed module structures are present.

## 6. Not to be confused with

- `ContinuousMultilinearMap.compLinearMap`: the purely algebraic (non-topological) analogue that composes a multilinear map with linear maps without requiring or verifying continuity.
- `ContinuousMultilinearMap.compContinuousLinearMapL`: the continuous-linear-map-valued (curried, operator-norm-continuous) version of the same construction, used when one wants to vary `f` or `g` continuously in a normed setting.
- `ContinuousLinearMap.comp`: ordinary composition of two continuous linear maps (single-argument case), which should not be confused with composing a multilinear map with a family of linear maps.