## VTask.InjOn

### Object

`VTask.InjOn f s` is the proposition that the function `f` is *injective when restricted to the set `s`*: distinct elements of `s` are mapped to distinct values. Concretely, whenever `x₁` and `x₂` both belong to `s` and `f x₁ = f x₂`, one can conclude `x₁ = x₂`. This is strictly weaker than global injectivity — `f` may identify points outside `s` arbitrarily.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.InjOn : {α : Type u} -> {β : Type v} -> (f : α → β) -> (s : Set α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.InjOn : {α : Type u} -> {β : Type v} -> (f : α → β) -> (s : Set α) -> Prop`

The universe levels `u` and `v` are implicit and inferred automatically. The first explicit argument `f` is the function whose behaviour on the set is being examined. The second explicit argument `s` is the domain set over which injectivity is required; only pairs of points drawn from `s` are constrained.

### Conventions

There are no junk-value conventions for this definition: it is a universally quantified proposition and is well-defined for every function and every set, including the empty set and the full type. No special defaults or sentinel values are needed.

### Worked examples

- Claim: `VTask.InjOn (fun n : ℕ => n * 2) Set.univ` holds — doubling is injective on all natural numbers.

- Claim: `VTask.InjOn (fun _ : ℕ => (0 : ℕ)) ∅` holds — every function is vacuously injective on the empty set, since there are no pairs of distinct points to violate injectivity.

- Claim: `VTask.InjOn (fun _ : ℕ => (0 : ℕ)) {0, 1}` does *not* hold — the constant-zero function identifies `0` and `1`, both members of `{0, 1}`, so injectivity fails on this two-element set.

- Claim: If `VTask.InjOn f s` and `t ⊆ s`, then `VTask.InjOn f t` — injectivity on a set is inherited by any subset.

### Boundaries

- **Empty set**: `VTask.InjOn f ∅` is always true for any `f`, since the universal quantification over members of `∅` has no witnesses.
- **Singleton sets**: `VTask.InjOn f {a}` is always true; a single point cannot produce two distinct inputs that map to the same output.
- **Full type (`Set.univ`)**: `VTask.InjOn f Set.univ` is equivalent to global injectivity (`Function.Injective f`).
- **Constant functions**: A constant function satisfies `VTask.InjOn f s` if and only if `s` has at most one element.
- **Set enlargement**: `VTask.InjOn f s` does *not* imply `VTask.InjOn f t` for `t ⊇ s`; the injectivity condition may fail on the added points.

### Not to be confused with

- `Function.Injective f` — global injectivity; requires `f x₁ = f x₂ → x₁ = x₂` for *all* `x₁ x₂ : α`, not just those in a specified set.
- `Set.SurjOn f s t` — surjectivity of `f` from `s` onto `t`; a dual notion about coverage rather than distinctness.
- `Set.BijOn f s t` — bijectivity of `f` from `s` to `t`; combines `InjOn`, `MapsTo`, and `SurjOn` simultaneously.