## Object

`VTask.MonovaryOn f g s` is the proposition that `f` **monovaries with** `g` on the set `s`: whenever two indices `i` and `j` both lie in `s` and the value `g j` strictly exceeds `g i`, the value `f j` is at least `f i`. Informally, `g` increasing (strictly) from `i` to `j` forces `f` to be non-decreasing from `i` to `j`, but only for pairs of indices inside `s`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.MonovaryOn : {ι : Type u_1} -> {α : Type u_3} -> {β : Type u_4} -> [Preorder α] -> [Preorder β] -> (f : ι → α) -> (g : ι → β) -> (s : Set ι) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.MonovaryOn : {ι : Type u_1} -> {α : Type u_3} -> {β : Type u_4} -> [Preorder α] -> [Preorder β] -> (f : ι → α) -> (g : ι → β) -> (s : Set ι) -> Prop`

The index type `ι` is the common domain of both functions. The codomain `α` carries a preorder used to compare values of `f`, and `β` carries a preorder used to compare values of `g`. The argument `f` is the function whose non-decrease is being asserted; the argument `g` is the function that drives (or 'witnesses') the ordering. The argument `s` is the subset of the index type over which the covariation is required to hold.

## Conventions

There are no special junk-value or boundary conventions beyond the standard universal-quantifier behaviour: when `s` is empty the statement holds vacuously, since there are no pairs `i, j ∈ s` to check.

## Worked examples

- Claim: `VTask.MonovaryOn f g ∅` holds for any `f` and `g`, because the defining condition is vacuously satisfied over the empty set.

- Claim: For `f = id` and `g = id` on `Set.univ ⊆ ℕ`, `VTask.MonovaryOn id id Set.univ` holds, since `id i < id j` implies `id i ≤ id j` for natural numbers.

- Claim: If `h : VTask.MonovaryOn f g t` and `s ⊆ t`, then `VTask.MonovaryOn f g s` holds, because restricting to a smaller set cannot introduce new pairs that violate the condition.

- Claim: `VTask.MonovaryOn f g s` is symmetric in the sense that it implies `VTask.MonovaryOn g f s`; that is, a monovariance relation between `f` and `g` gives one between `g` and `f` on the same set.

## Boundaries

- **Empty set**: `VTask.MonovaryOn f g ∅` is always true; there are no indices to check.
- **Singleton set**: `VTask.MonovaryOn f g {i}` is always true; a single index yields only the pair `(i, i)`, but `g i < g i` is false in any preorder, so the implication holds vacuously.
- **Constant `g`**: If `g` is constant on `s`, then `g i < g j` is never satisfied for `i, j ∈ s`, so `VTask.MonovaryOn f g s` holds for any `f`.
- **Subset monotonicity**: If `VTask.MonovaryOn f g t` holds and `s ⊆ t`, then `VTask.MonovaryOn f g s` holds; the property is monotone in the downward direction with respect to set inclusion.

## Not to be confused with

- **`VTask.Monovary f g`** (the global, non-restricted version): requires the covariation condition to hold for *all* pairs of indices, not just those in a specified set `s`.
- **`VTask.AntivaryOn f g s`** (antivary on a set): asserts that `g i < g j` implies `f j ≤ f i`, i.e., `f` and `g` move in *opposite* directions.
- **`MonotoneOn f s`** (monotonicity on a set): concerns a single function `f : α → β` and requires `a ≤ b → f a ≤ f b` for `a, b ∈ s`, rather than a covariation condition between two separate index-to-preorder functions.