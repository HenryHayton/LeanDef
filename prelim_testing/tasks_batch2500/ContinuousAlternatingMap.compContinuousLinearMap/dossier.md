## Object

Given a continuous alternating multilinear map `g : M [⋀^ι]→L[R] N` and a continuous linear map `f : M' →L[R] M`, `VTask.compContinuousLinearMap g f` is the continuous alternating map `M' [⋀^ι]→L[R] N` obtained by pre-composing each argument of `g` with `f`. Concretely, if `m₁, …, mₙ` are elements of `M'`, the new map sends them to `g(f(m₁), …, f(mₙ))`. The result is again alternating (swapping any two equal inputs still yields zero) and continuous.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.compContinuousLinearMap : {R : Type u_1} -> {M : Type u_2} -> {M' : Type u_3} -> {N : Type u_4} -> {ι : Type u_6} -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> [TopologicalSpace M] -> [AddCommMonoid M'] -> [Module R M'] -> [TopologicalSpace M'] -> [AddCommMonoid N] -> [Module R N] -> [TopologicalSpace N] -> (g : M [⋀^ι]→L[R] N) -> (f : M' →L[R] M) -> M' [⋀^ι]→L[R] N
<!-- PINNED-SIGNATURE:END -->


`VTask.compContinuousLinearMap : {R : Type u_1} -> {M : Type u_2} -> {M' : Type u_3} -> {N : Type u_4} -> {ι : Type u_6} -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> [TopologicalSpace M] -> [AddCommMonoid M'] -> [Module R M'] -> [TopologicalSpace M'] -> [AddCommMonoid N] -> [Module R N] -> [TopologicalSpace N] -> (g : M [⋀^ι]→L[R] N) -> (f : M' →L[R] M) -> M' [⋀^ι]→L[R] N`

The scalar semiring `R` controls the module structure throughout. The types `M`, `M'`, and `N` are the source domain, the new source domain, and the codomain respectively, each equipped with compatible module and topological structures. The index type `ι` parametrises the finite list of arguments. The argument `g` is the continuous alternating map being pre-composed; it accepts tuples indexed by `ι` in `M` and produces values in `N`. The argument `f` is the continuous linear map that transforms each input from `M'` into `M` before `g` is evaluated.

## Conventions

There are no declared junk-value or edge conventions for this definition: the construction is total and well-defined for all valid inputs, including the degenerate case where `ι` is empty (yielding a continuous alternating map of zero arguments) and where `f` is the zero map.

## Worked examples

- Claim: When `f` is the identity continuous linear map on `M`, `VTask.compContinuousLinearMap g (ContinuousLinearMap.id R M)` equals `g` as a continuous alternating map.

- Claim: When `ι = Fin 2`, `R = ℝ`, and `g` is the determinant-style alternating map on `ℝ²`, pre-composing with any continuous linear map `f : ℝ² →L[ℝ] ℝ²` yields the alternating map that computes the determinant of the matrix whose columns are the images under `f` of the two input vectors.

- Claim: Pre-composing any `g : M [⋀^ι]→L[R] N` with the zero continuous linear map `(0 : M' →L[R] M)` yields the zero continuous alternating map, because every input gets sent to `0` in `M` and the resulting value is `g(0, …, 0) = 0` by multilinearity.

## Boundaries

- If `ι` is empty, the result is a continuous alternating map with no arguments; it behaves as a continuous map from the empty product to `N`, and pre-composing with `f` does not change its (unique) value.
- If `f` is the zero map `0 : M' →L[R] M`, then `VTask.compContinuousLinearMap g 0` is the zero element of `M' [⋀^ι]→L[R] N`, since `g` evaluated at all-zero inputs returns `0`.
- If `f` is the identity on `M` (with `M' = M`), the composition recovers `g` itself.
- Composition is associative: pre-composing `g` with `f₂ ∘ f₁` (a composite of two continuous linear maps) yields the same result as first pre-composing with `f₂` and then with `f₁`.

## Not to be confused with

- `ContinuousMultilinearMap.compContinuousLinearMap`: the analogous composition for continuous *multilinear* maps that need not be alternating; it does not enforce the alternating condition.
- `AlternatingMap.compLinearMap`: the purely algebraic (non-topological) version that pre-composes an algebraic alternating map with a plain linear map, carrying no continuity data.
- Pre-composing on the *codomain*: `VTask.compContinuousLinearMap` inserts `f` on the *inputs*, not on the output; a continuous linear post-composition would be a different operation.