## Object

A function `f : α → β` is **monotone on a set `s`** if it preserves the order relation when restricted to elements of `s`: whenever two elements `a` and `b` both belong to `s` and satisfy `a ≤ b`, their images satisfy `f a ≤ f b`. This is the localised or restricted version of global monotonicity, allowing `f` to behave arbitrarily outside `s`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.MonotoneOn : {α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> (s : Set α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.MonotoneOn : {α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> (s : Set α) -> Prop`

The type parameters `α` and `β` are the domain and codomain types; the two `Preorder` instances supply the ≤ relations on each. The argument `f` is the function whose monotonicity is being asserted. The argument `s` is the subset of `α` on which monotonicity is required.

## Conventions

There are no special junk-value or boundary-case conventions to declare: `VTask.MonotoneOn f s` is a universally quantified proposition and is vacuously true whenever `s` contains fewer than two elements (in particular when `s` is empty or a singleton), because the hypothesis `a ∈ s` and `b ∈ s` and `a ≤ b` can never be simultaneously satisfied with two distinct witnesses.

## Worked examples

- Claim: The function `f : ℝ → ℝ` given by `f x = x` satisfies `VTask.MonotoneOn f (Set.Icc 0 1)`, since the identity is globally monotone and restriction can only make the condition easier.

- Claim: The function `f : ℝ → ℝ` given by `f x = x^2` does **not** satisfy `VTask.MonotoneOn f (Set.Icc (-1) 1)`, as witnessed by `a = -1`, `b = 0` (both in `[-1,1]`), `a ≤ b`, yet `f a = 1 > 0 = f b`.

- Claim: For any types `α`, `β` with preorders, any function `f : α → β`, and the empty set `∅ : Set α`, `VTask.MonotoneOn f ∅` holds vacuously because no element belongs to `∅`.

- Claim: If `g : β → γ` is monotone on `t` and `f : α → β` is monotone on `s` with `f` mapping `s` into `t`, then `g ∘ f` is monotone on `s` (composition of monotone-on functions is monotone on the appropriate domain).

## Boundaries

- **Empty set**: `VTask.MonotoneOn f ∅` is always true because the universal quantifier has no witnesses to instantiate.
- **Singleton set**: `VTask.MonotoneOn f {a}` is always true; the only possible pair satisfying `a ∈ {a}` and `b ∈ {a}` has `a = b`, so `f a ≤ f a` holds by reflexivity.
- **Full set (`Set.univ`)**: `VTask.MonotoneOn f Set.univ` is equivalent to the global `Monotone f`.
- **Non-strict**: The condition uses `≤` (not `<`) on both sides, so a constant function is always monotone on any set.

## Not to be confused with

- **`Monotone f`** — global monotonicity, i.e., `∀ a b, a ≤ b → f a ≤ f b`; `VTask.MonotoneOn f Set.univ` is equivalent to it, but `VTask.MonotoneOn` is strictly weaker for proper subsets.
- **`StrictMonoOn f s`** — requires `a < b → f a < f b` for elements of `s`; strictly stronger than `VTask.MonotoneOn f s` in general.
- **`AntitoneOn f s`** — the reversed version: `a ≤ b → f b ≤ f a` for elements of `s`; not the same as `VTask.MonotoneOn f s` unless the order is trivial.