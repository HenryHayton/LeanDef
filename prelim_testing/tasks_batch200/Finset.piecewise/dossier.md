## 1. Object

Given a finite set `s` of indices and two dependent functions `f` and `g` over those indices, `VTask.piecewise s f g` is the dependent function that agrees with `f` at every index belonging to `s` and agrees with `g` at every index outside `s`. In classical terms, it is the "gluing" or "splicing" of `f` and `g` along the indicator of the finite set `s`.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.piecewise : {ι : Type u_1} -> {π : ι → Sort u_2} -> (s : Finset ι) -> (f g : (i : ι) → π i) -> [(j : ι) → Decidable (j ∈ s)] -> (i : ι) -> π i
<!-- PINNED-SIGNATURE:END -->


`VTask.piecewise : {ι : Type u_1} -> {π : ι → Sort u_2} -> (s : Finset ι) -> (f g : (i : ι) → π i) -> [(j : ι) → Decidable (j ∈ s)] -> (i : ι) -> π i`

The implicit argument `ι` is the index type. The implicit argument `π` is the dependent sort family over `ι`, determining the type of the value at each index. The explicit argument `s` is the finite set that serves as the "domain of `f`": the piecewise function uses `f` on `s` and `g` off `s`. The arguments `f` and `g` are the two dependent functions being spliced: `f` supplies values on `s` and `g` supplies values on the complement of `s`. The instance argument `[∀ j, Decidable (j ∈ s)]` provides the decidability of membership in `s` needed to evaluate the branching condition at each index. The final argument `i` is the index at which to evaluate the resulting piecewise function.

## 3. Conventions

When both functions coincide (`f = g`), the piecewise construction returns `f` regardless of the set `s`. When `s = ∅`, the piecewise function equals `g` everywhere, since no index belongs to the empty set. When `s = {i}` (a singleton), the piecewise function equals `g` updated at `i` to the value `f i`.

## 4. Worked examples

- Claim: For any `i ∈ s`, `VTask.piecewise s f g i = f i`.
  (At an index that belongs to `s`, the piecewise function yields the value of `f`.)

- Claim: For any `i ∉ s`, `VTask.piecewise s f g i = g i`.
  (At an index outside `s`, the piecewise function yields the value of `g`.)

- Claim: `VTask.piecewise (∅ : Finset ι) f g = g`.
  (On the empty finset, the piecewise function is everywhere equal to `g`.)

- Claim: `VTask.piecewise s f f = f`.
  (When both branch functions agree, the result is simply that common function, regardless of the set.)

- Claim: If `f ≤ g`, then `VTask.piecewise s f g` lies in the interval `Set.Icc f g`.
  (The splice of a pointwise-smaller `f` with a pointwise-larger `g` stays between the two.)

## 5. Boundaries

- When `s = ∅`: every index is outside `s`, so the piecewise function equals `g` everywhere.
- When `s = Finset.univ`: every index is inside `s`, so the piecewise function equals `f` everywhere.
- When `s = {i}` for a single index `i`: the result equals `g` with the single point `i` updated to `f i`.
- When `f = g`: the choice of `s` is irrelevant; the result is `f` (equivalently `g`).
- The function is well-typed even when `π` is a sort (not just a type), covering both value and proof splicing.

## 6. Not to be confused with

- `Set.piecewise`: the analogous construction for arbitrary (possibly infinite) *sets* of indices rather than finite sets; `VTask.piecewise` is the finset-indexed specialisation, and a coherence lemma states they agree when the finset is coerced to a set.
- `Function.update`: replaces a function's value at a *single* index, whereas `VTask.piecewise` handles an entire finite set of indices at once; `VTask.piecewise` on a singleton recovers `Function.update`.
- `Finset.indicator`: maps a function to zero outside a set (requires a zero), which is a scalar-valued specialisation; `VTask.piecewise` does not require a zero and instead explicitly provides a second function `g` for the complement.