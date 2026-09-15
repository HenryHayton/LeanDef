## Object

Given a continuous linear map `g : N →L[R] N'` and a continuous alternating map `f : M [⋀^ι]→L[R] N`, their composition `g ∘ f` is again a continuous alternating map `M [⋀^ι]→L[R] N'`. Concretely, this is the map sending an `ι`-indexed family of vectors in `M` to the image under `g` of the value that `f` assigns to that family. The result inherits multilinearity, the alternating property (vanishing whenever two inputs coincide), and joint continuity from its constituents.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.compContinuousAlternatingMap : {R : Type u_1} -> {M : Type u_2} -> {N : Type u_4} -> {N' : Type u_5} -> {ι : Type u_6} -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> [TopologicalSpace M] -> [AddCommMonoid N] -> [Module R N] -> [TopologicalSpace N] -> [AddCommMonoid N'] -> [Module R N'] -> [TopologicalSpace N'] -> (g : N →L[R] N') -> (f : M [⋀^ι]→L[R] N) -> M [⋀^ι]→L[R] N'
<!-- PINNED-SIGNATURE:END -->


`VTask.compContinuousAlternatingMap : {R : Type u_1} -> {M : Type u_2} -> {N : Type u_4} -> {N' : Type u_5} -> {ι : Type u_6} -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> [TopologicalSpace M] -> [AddCommMonoid N] -> [Module R N] -> [TopologicalSpace N] -> [AddCommMonoid N'] -> [Module R N'] -> [TopologicalSpace N'] -> (g : N →L[R] N') -> (f : M [⋀^ι]→L[R] N) -> M [⋀^ι]→L[R] N'`

The scalar semiring `R`, the domain module `M`, the intermediate module `N`, the codomain module `N'`, and the index type `ι` are implicit parameters. The instance arguments provide the necessary algebraic and topological structure on each type. The explicit argument `g` is the continuous linear map applied after evaluation; the explicit argument `f` is the continuous alternating map being post-composed with `g`.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total construction well-defined for any continuous linear map and any continuous alternating map over a common semiring, and the result is always a well-formed continuous alternating map.

## Worked examples

- Claim: For any continuous alternating map `f : M [⋀^ι]→L[R] N` and the identity continuous linear map `id : N →L[R] N`, the composition `VTask.compContinuousAlternatingMap id f` equals `f` as a continuous alternating map.

- Claim: For composable continuous linear maps `g : N →L[R] N'` and `h : N' →L[R] N''`, and a continuous alternating map `f : M [⋀^ι]→L[R] N`, the composition `VTask.compContinuousAlternatingMap (h.comp g) f` equals `VTask.compContinuousAlternatingMap h (VTask.compContinuousAlternatingMap g f)`.

- Claim: Applying `VTask.compContinuousAlternatingMap g f` to a family of vectors `v : ι → M` gives the same value as first applying `f` to `v` and then applying `g`.

## Boundaries

- When `ι` is the empty type, the alternating map `f` is constant (returning a fixed element of `N`), and the composition simply applies `g` to that constant; the alternating and multilinearity conditions hold vacuously.
- When `g` is the zero continuous linear map, the resulting continuous alternating map is identically zero regardless of `f`.
- When `f` is the zero continuous alternating map, the resulting map is also identically zero regardless of `g`.
- The construction is associative in the sense that composing with further linear maps on the outside respects the usual composition of linear maps.

## Not to be confused with

- `ContinuousLinearMap.compContinuousMultilinearMap`: composes a continuous linear map with a continuous *multilinear* map, without requiring the alternating (antisymmetry/vanishing) property.
- `AlternatingMap.compLinearMap`: post-composes an algebraic (non-topological) alternating map with an algebraic linear map, ignoring continuity.
- `ContinuousMultilinearMap.compContinuousLinearMap`: *pre*-composes a continuous multilinear map with continuous linear maps on each argument slot, rather than post-composing with a single linear map on the output.