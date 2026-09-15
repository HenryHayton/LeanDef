## Object

`VTask.IsThetaTVS 𝕜 l f g` asserts that the functions `f` and `g` are *mutually big-O of each other* with respect to the scalar field `𝕜`, along the filter `l`. Concretely, this means there exist scalar-controlled absorbing bounds: `f` is eventually bounded (in the TVS sense) by a scalar multiple of `g`, and `g` is eventually bounded by a scalar multiple of `f`. This is the topological-vector-space analogue of the classical Theta (Θ) asymptotic equivalence notion, and it forms an equivalence relation on pairs of functions into topological `𝕜`-modules.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsThetaTVS : (𝕜 : Type u_1) -> {α : Type u_2} -> {E : Type u_3} -> {F : Type u_4} -> [ENorm 𝕜] -> [TopologicalSpace E] -> [TopologicalSpace F] -> [Zero E] -> [Zero F] -> [SMul 𝕜 E] -> [SMul 𝕜 F] -> (l : Filter α) -> (f : α → E) -> (g : α → F) -> Prop
<!-- PINNED-SIGNATURE:END -->


VTask.IsThetaTVS : (𝕜 : Type u_1) -> {α : Type u_2} -> {E : Type u_3} -> {F : Type u_4} -> [ENorm 𝕜] -> [TopologicalSpace E] -> [TopologicalSpace F] -> [Zero E] -> [Zero F] -> [SMul 𝕜 E] -> [SMul 𝕜 F] -> (l : Filter α) -> (f : α → E) -> (g : α → F) -> Prop

The explicit type argument `𝕜` is the scalar field (or ring), equipped with an extended norm used to measure scalar size. The implicit type `α` is the index type over which both functions are defined. The implicit types `E` and `F` are the target topological spaces, each a `𝕜`-module with a zero and a scalar multiplication. The argument `l` is the filter on `α` encoding the asymptotic regime of interest (e.g., a neighbourhood filter at a point, or the cofinite filter for sequences). The argument `f : α → E` is the first function being compared. The argument `g : α → F` is the second function; crucially, `f` and `g` may land in *different* topological `𝕜`-modules.

## Conventions

There are no declared junk-value or boundary conventions for this definition: it is a `Prop`-valued predicate that is simply true or false for any inputs, and no special out-of-domain inputs arise. The filter `l` may be any filter including `⊥` (the inconsistent filter), and the definition remains well-formed.

## Worked examples

- Claim: Every function `f : α → E` satisfies `VTask.IsThetaTVS 𝕜 l f f` (reflexivity).

- Claim: If `VTask.IsThetaTVS 𝕜 l f g` holds, then so does `VTask.IsThetaTVS 𝕜 l g f` (symmetry).

- Claim: If `VTask.IsThetaTVS 𝕜 l f g` and `VTask.IsThetaTVS 𝕜 l g h` both hold, then `VTask.IsThetaTVS 𝕜 l f h` holds (transitivity).

- Claim: If `VTask.IsThetaTVS 𝕜 l f g` holds, then the one-sided bound `f =O[𝕜; l] g` (i.e., `IsBigOTVS 𝕜 l f g`) also holds.

## Boundaries

- When `l = ⊥` (the bottom filter, which contains every set), every `Filter`-quantified statement is vacuously true, so `VTask.IsThetaTVS 𝕜 ⊥ f g` holds for all `f` and `g`.
- When `f` or `g` is the constant zero function, the condition `g =O[𝕜; l] f` requires `g` to be eventually zero along `l` as well (since zero cannot absorb a nonzero value via scalar multiplication in a faithful module), so `VTask.IsThetaTVS 𝕜 l 0 g` is not automatically trivial unless `g` is also eventually zero.
- The two functions `f` and `g` are allowed to take values in *different* `𝕜`-modules `E` and `F`; the definition is not restricted to a single target space.

## Not to be confused with

- `Asymptotics.IsTheta` (the classical `f =Θ[l] g`): the normed-space version that uses real-valued norms on `E` and `F` directly, rather than the TVS big-O defined via scalar absorbing sets.
- `Asymptotics.IsBigOTVS` (`f =O[𝕜; l] g`): only the *one-sided* bound; `IsThetaTVS` is the conjunction of this with the reverse direction.
- `Asymptotics.IsLittleOTVS` (`f =o[𝕜; l] g`): a *strictly stronger* (small-o) condition requiring the ratio to vanish, rather than remain bounded in both directions.