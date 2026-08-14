## Object

`VTask.Monovary f g` is the proposition that the function `f` *monovaries* with the function `g`: whenever `g` strictly increases between two indices (i.e., `g i < g j`), `f` must weakly increase between those same indices (i.e., `f i ≤ f j`). Informally, `g` going up forces `f` to not go down. This is a one-sided, asymmetric notion of "co-monotonicity" between two functions defined on a common index type.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Monovary : {ι : Type u_1} -> {α : Type u_3} -> {β : Type u_4} -> [Preorder α] -> [Preorder β] -> (f : ι → α) -> (g : ι → β) -> Prop
<!-- PINNED-SIGNATURE:END -->


VTask.Monovary : {ι : Type u_1} -> {α : Type u_3} -> {β : Type u_4} -> [Preorder α] -> [Preorder β] -> (f : ι → α) -> (g : ι → β) -> Prop

- `ι` is the shared index type ranging over both functions.
- `α` is the codomain of `f`, equipped with a preorder that provides the `≤` relation used in the conclusion.
- `β` is the codomain of `g`, equipped with a preorder that provides the `<` relation used in the hypothesis.
- The two `Preorder` instances supply the ordering structure on `α` and `β` respectively.
- `f : ι → α` is the function whose weak monotone increase is being guaranteed.
- `g : ι → β` is the function whose strict increase triggers the condition.

## Conventions

No special junk-value or boundary conventions are declared: the predicate is universally quantified over all indices in `ι` with no domain restriction, and its meaning is uniform across all inputs.

## Worked examples

- Claim: `VTask.Monovary (fun n : ℕ => n) (fun n : ℕ => n)` holds — the identity function monovaries with itself, since `j < i` implies `j ≤ i`.

- Claim: `VTask.Monovary (fun _ : Fin 3 => (0 : ℕ)) (fun n : Fin 3 => (n : ℕ))` holds — a constant function `f` monovaries with any `g`, because `g i < g j` requires `f i ≤ f j`, but `f` is constant so `f i = f j ≤ f j`.

- Claim: `¬ VTask.Monovary (fun n : Fin 2 => (1 - n : ℤ)) (fun n : Fin 2 => (n : ℤ))` holds — here `g 0 < g 1` but `f 0 = 1 > 0 = f 1`, so `f` strictly decreases where `g` strictly increases, violating the condition.

- Claim: If `VTask.Monovary f g` holds then `VTask.Monovary g f` also holds (the relation is symmetric between the two functions when both directions are considered).

## Boundaries

- When `ι` is empty there are no indices at all, so the universal quantification is vacuously true: every pair of functions on an empty type satisfies `VTask.Monovary`.
- When `g` is a constant function, the strict inequality `g i < g j` is never satisfied, so the hypothesis is always false and `VTask.Monovary f g` holds vacuously for any `f`.
- The condition is one-directional: `VTask.Monovary f g` does **not** in general imply `VTask.Monovary g f`. However, there is a theorem establishing that it does imply `VTask.Monovary g f` when both directions are present, and the symmetry theorem `VTask.Monovary.symm` states that `VTask.Monovary f g → VTask.Monovary g f`.
- The conclusion uses weak inequality (`≤`) while the hypothesis uses strict inequality (`<`); this asymmetry is deliberate and means that ties in `g` impose no constraint on `f`.

## Not to be confused with

- `Antivary f g`: the opposite relationship, where `g i < g j` implies `f j ≤ f i` — `f` weakly *decreases* when `g` strictly increases.
- `MonovaryOn f g s`: the same condition restricted to indices `i, j` belonging to a specified set `s`, rather than all of `ι`.
- `Monotone f`: a single-function condition asserting `a ≤ b → f a ≤ f b`; `VTask.Monovary f g` is a two-function generalisation where the ordering on the domain is replaced by the ordering induced by a separate function `g`.