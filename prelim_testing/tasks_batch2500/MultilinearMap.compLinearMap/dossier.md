## Object

`VTask.compLinearMap g f` is the multilinear map obtained by precomposing a multilinear map `g : M₁'₁ × … × M₁'ₙ → M₂` with a family of linear maps `fᵢ : M₁ᵢ → M₁'ᵢ`, one for each index `i`. Concretely, the resulting map sends a tuple `(m₁, …, mₙ)` to `g(f₁(m₁), …, fₙ(mₙ))`. Multilinearity of `g` together with linearity of each `fᵢ` guarantees that the composition is again multilinear.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.compLinearMap : {R : Type uR} -> {ι : Type uι} -> {M₁ : ι → Type v₁} -> {M₁' : ι → Type v₁'} -> {M₂ : Type v₂} -> [Semiring R] -> [(i : ι) → AddCommMonoid (M₁ i)] -> [AddCommMonoid M₂] -> [(i : ι) → Module R (M₁ i)] -> [Module R M₂] -> [(i : ι) → AddCommMonoid (M₁' i)] -> [(i : ι) → Module R (M₁' i)] -> (g : MultilinearMap R M₁' M₂) -> (f : (i : ι) → M₁ i →ₗ[R] M₁' i) -> MultilinearMap R M₁ M₂
<!-- PINNED-SIGNATURE:END -->


`VTask.compLinearMap : {R : Type uR} -> {ι : Type uι} -> {M₁ : ι → Type v₁} -> {M₁' : ι → Type v₁'} -> {M₂ : Type v₂} -> [Semiring R] -> [(i : ι) → AddCommMonoid (M₁ i)] -> [AddCommMonoid M₂] -> [(i : ι) → Module R (M₁ i)] -> [Module R M₂] -> [(i : ι) → AddCommMonoid (M₁' i)] -> [(i : ι) → Module R (M₁' i)] -> (g : MultilinearMap R M₁' M₂) -> (f : (i : ι) → M₁ i →ₗ[R] M₁' i) -> MultilinearMap R M₁ M₂`

The scalar semiring `R` parameterises all module structures. The index type `ι` ranges over the slots of the multilinear map. The families `M₁` and `M₁'` assign an `R`-module to each index in the domain and intermediate layer respectively, and `M₂` is the common codomain module. The argument `g` is the outer multilinear map, consuming one element of each `M₁' i` and producing a value in `M₂`. The argument `f` is the family of linear maps threading through the composition: for each index `i`, `f i` is an `R`-linear map from `M₁ i` to `M₁' i`.

## Conventions

No special junk-value or boundary conventions are declared for this construction: the definition is total and well-behaved for any valid inputs.

## Worked examples

- Claim: Evaluating `g.compLinearMap f` at a tuple `m` yields the same result as applying `g` to the tuple obtained by applying each `fᵢ` to `mᵢ`.
  This is the defining evaluation rule: `(g.compLinearMap f) m = g (fun i => f i (m i))`.

- Claim: Composing any multilinear map with the family of identity linear maps returns the original multilinear map unchanged, i.e., `g.compLinearMap (fun _ => LinearMap.id) = g`.
  This is the identity law for the construction.

- Claim: The zero multilinear map composed with any family of linear maps is again the zero multilinear map: `(0 : MultilinearMap R M₁' M₂).compLinearMap f = 0`.

- Claim: If each `fᵢ` is surjective, then the map `g ↦ g.compLinearMap f` is injective on `MultilinearMap R M₁' M₂`.

## Boundaries

- When `ι` is empty the result is a multilinear map on zero arguments, which is simply a constant; the construction still works correctly because the universal quantification over `i` is vacuous.
- When any `fᵢ` is the zero linear map, the entire output of `g.compLinearMap f` at any input is `g` evaluated at the tuple that has `0` in position `i` (and `fⱼ(mⱼ)` elsewhere), which need not be zero unless `g` itself vanishes on such tuples.
- If each `fᵢ` is a linear equivalence, the composition is invertible (the zero-iff criterion applies: `g.compLinearMap f = 0 ↔ g = 0`).
- The construction is defined over a general semiring `R`, so it does not require commutativity or the existence of additive inverses.

## Not to be confused with

- `MultilinearMap.compMultilinearMap`: this composes a *linear* map on the *outside* (postcomposition with a linear map into a third module), rather than precomposing each slot with a linear map.
- `MultilinearMap.domDomCongr` / reindexing maps: those permute or reindex the domain slots rather than transforming the module values in each slot.
- `LinearMap.comp`: ordinary composition of two linear maps between modules; unlike `VTask.compLinearMap`, it operates on single-slot (linear) maps, not multilinear ones.