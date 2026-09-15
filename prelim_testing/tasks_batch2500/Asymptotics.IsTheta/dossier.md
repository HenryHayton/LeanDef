## 1. Object

`VTask.IsTheta l f g` asserts that `f` and `g` have the same asymptotic order of growth along the filter `l`. Concretely, this means there exist positive constants `c₁` and `c₂` such that, along `l`, the norm of `f` is bounded above by `c₁` times the norm of `g`, and simultaneously the norm of `g` is bounded above by `c₂` times the norm of `f`. This is the standard "big-Theta" relation from asymptotic analysis, written `f =Θ[l] g` in Mathlib notation.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsTheta : {α : Type u_1} -> {E : Type u_3} -> {F : Type u_4} -> [Norm E] -> [Norm F] -> (l : Filter α) -> (f : α → E) -> (g : α → F) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.IsTheta : {α : Type u_1} -> {E : Type u_3} -> {F : Type u_4} -> [Norm E] -> [Norm F] -> (l : Filter α) -> (f : α → E) -> (g : α → F) -> Prop
```

The implicit type `α` is the domain of the functions; `E` and `F` are the codomains of `f` and `g` respectively, each equipped with a norm via the `Norm` instances. The argument `l` is the filter along which the asymptotic comparison is made (for example, a neighbourhood filter at a point, or the filter of large natural numbers). The argument `f` is the function being compared, and `g` is the reference function.

## 3. Conventions

There are no special junk-value or edge-case conventions declared for this definition: it is simply a conjunction of two `IsBigO` statements, both of which are propositions defined for all inputs without restriction or special casing.

## 4. Worked Examples

- Claim: If `f =Θ[l] g` then `f =O[l] g` (the forward big-O component can always be extracted).

- Claim: If `f =Θ[l] g` then `g =O[l] f` (the reverse big-O component can always be extracted).

- Claim: `VTask.IsTheta l f g` implies `VTask.IsTheta l g f` (the relation is symmetric: swapping the two functions yields another valid `IsTheta` because the two `IsBigO` components simply trade roles).

- Claim: For any filter `l' ≤ l`, if `VTask.IsTheta l f g` then `VTask.IsTheta l' f g` (the relation is monotone: a coarser filter gives a weaker condition, so the Theta relation is inherited by finer comparisons).

- Claim: If `f =Θ[l] g` and `g =Θ[l] h` then `f =Θ[l] h` (transitivity holds, since big-O is transitive and both components compose).

## 5. Boundaries

- When `l` is the `⊥` filter (the filter containing every set), every `IsBigO` relation holds trivially, so `VTask.IsTheta ⊥ f g` is always true regardless of `f` and `g`.
- When the codomain norms are trivially zero (e.g., if `g` is identically zero and `f` is not), the reverse `IsBigO` condition `g =O[l] f` may fail, so `IsTheta` is not symmetric unless both norms are comparable.
- The relation makes sense for functions into different normed types `E` and `F`; the norms of the two codomains are compared independently.
- There is no requirement that `f` or `g` be nonzero, continuous, or measurable; the definition is purely analytic/order-theoretic via filters.

## 6. Not to be confused with

- `IsBigO l f g` (`f =O[l] g`): only the one-sided bound — `f` is at most `g` in growth — without the matching lower bound that `IsTheta` also requires.
- `IsLittleO l f g` (`f =o[l] g`): a strictly stronger (quantitative) one-sided relation asserting `‖f‖ / ‖g‖ → 0` along `l`, incompatible with `IsTheta` unless both functions vanish.
- `IsThetaTVS` (the TVS variant, notation `f =Θ[𝕜; l] g`): a related but distinct notion for topological vector spaces that does not require a norm and uses scalar multiples in a different sense.