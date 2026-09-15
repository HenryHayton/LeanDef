## Object

`VTask.IsEquivalent l u v` expresses that two functions `u` and `v` into a seminormed abelian group are *asymptotically equivalent* along a filter `l`. Concretely, this means that the difference `u x - v x` is negligible compared with `v x` as `x` travels along `l`; that is, `(u - v)(x) / ‖v(x)‖ → 0` along `l` (in the sense of Landau's little-o). Informally: `u(x)` and `v(x)` have the same leading-order behaviour as `x` moves in the direction captured by the filter.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsEquivalent : {α : Type u_1} -> {E' : Type u_6} -> [SeminormedAddCommGroup E'] -> (l : Filter α) -> (u v : α → E') -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsEquivalent : {α : Type u_1} -> {E' : Type u_6} -> [SeminormedAddCommGroup E'] -> (l : Filter α) -> (u v : α → E') -> Prop`

The implicit type `α` is the domain of the functions (the "index" or "variable" space). The implicit type `E'` is the codomain, which must carry a seminormed additive commutative group structure (the instance supplies the notion of norm needed to measure relative smallness). The argument `l` is the filter along which the asymptotic comparison is made; typical choices include `Filter.atTop` (for sequences tending to infinity) or the neighbourhood filter of a point. The arguments `u` and `v` are the two functions being compared; the relation is stated with `v` as the *reference* function against whose size the difference is measured.

## Conventions

The relation is not symmetric by definition (the reference function is always `v`), yet it is in fact symmetric as a mathematical relation (proved as a theorem), so the asymmetry of the definition does not restrict which pairs are equivalent. When `v` is eventually zero along `l`, the little-o condition `(u - v) =o[l] v` degenerates (any function is little-o of the zero function in the trivial sense used in Mathlib's `IsLittleO`), so the condition becomes vacuous in that regime; in particular `VTask.IsEquivalent l u v` holds trivially if `v` is eventually zero.

## Worked examples

- Claim: Every function `u : ℕ → ℝ` satisfies `VTask.IsEquivalent Filter.atTop u u` (reflexivity).

- Claim: If `f n = n + 1` and `g n = n` (as functions `ℕ → ℝ`), then `VTask.IsEquivalent Filter.atTop f g`, because `(f - g)(n) = 1 = o(n)` as `n → ∞`.

- Claim: If `VTask.IsEquivalent l u v` then `VTask.IsEquivalent l v u` (symmetry), so asymptotic equivalence is a symmetric relation.

- Claim: If `VTask.IsEquivalent l u v` and `VTask.IsEquivalent l v w` then `VTask.IsEquivalent l u w` (transitivity), so it is also a transitive relation, forming an equivalence relation on functions.

## Boundaries

- If `v` is eventually zero along `l`, the condition `(u - v) =o[l] v` holds vacuously (little-o of the zero function is trivially satisfied), so any `u` is asymptotically equivalent to such a `v`. This is a degenerate case and does not reflect the usual intuition of "same leading order".
- The definition does not require `u` or `v` to be nonzero, bounded, or tending to any particular limit; the filter `l` encodes all directional information.
- For `l = ⊥` (the bottom filter, which contains every set), all statements about eventual behaviour hold trivially, so `VTask.IsEquivalent ⊥ u v` is always true.
- The relation is reflexive (`u ~[l] u` for all `u` and `l`) and symmetric and transitive, making it a genuine equivalence relation.

## Not to be confused with

- `Asymptotics.IsLittleO l u v` (`u =o[l] v`): this says `u` is *strictly smaller* in order than `v`, not that they have the same order; `IsEquivalent` is the condition `u - v = o(v)`, not `u = o(v)`.
- `Asymptotics.IsTheta l u v` (`u =Θ[l] v`): this says `u` and `v` have the *same order of magnitude* up to constant factors, a strictly weaker condition than asymptotic equivalence (which also pins the leading constant to 1).
- `Filter.Tendsto (fun x => u x / v x) l (nhds 1)`: while equivalent to `IsEquivalent` in many normed-field settings, this formulation requires division to make sense and does not directly generalise to seminormed groups.