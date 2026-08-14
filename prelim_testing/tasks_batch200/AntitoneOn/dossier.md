## Object

`VTask.AntitoneOn f s` is the proposition that the function `f` is order-reversing when its inputs are restricted to the set `s`. Concretely, it asserts: for every pair of elements `a, b` both belonging to `s`, if `a ≤ b` then `f b ≤ f a`. This is the set-restricted analogue of global antitonicity (order-reversing on the whole domain).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.AntitoneOn : {α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> (s : Set α) -> Prop
<!-- PINNED-SIGNATURE:END -->


The type parameters `α` and `β` are the domain and codomain types, each equipped with a preorder (the `[Preorder α]` and `[Preorder β]` instance arguments supply these orderings). The argument `f` is the function being tested: it maps elements of type `α` to elements of type `β`. The argument `s` is the subset of `α` to which the antitonicity condition is confined; only pairs `a, b ∈ s` are considered when checking whether `a ≤ b` implies `f b ≤ f a`.

## Conventions

There are no junk-value or edge conventions declared for this predicate: the universal quantification over an empty set `s` is vacuously true, so `VTask.AntitoneOn f ∅` holds for every `f`. No additional definitional conventions beyond the standard vacuous-universal reading are needed.

## Worked Examples

- Claim: The negation function `f(x) = -x` on `ℝ` is antitone on the closed interval `[0, 1]`, because `a ≤ b` implies `-b ≤ -a`.

- Claim: The constant function `f(x) = 0` is antitone on any set `s`, since `0 ≤ 0` is trivially satisfied whenever `f b ≤ f a` is required.

- Claim: `VTask.AntitoneOn (fun x : ℝ => -x) Set.univ` holds, as negation reverses the real order everywhere.

- Claim: `VTask.AntitoneOn (fun x : ℝ => x) (Set.Icc 0 1)` does **not** hold, because taking `a = 0, b = 1` gives `f b = 1 ≰ 0 = f a`.

## Boundaries

- **Empty set**: `VTask.AntitoneOn f ∅` is vacuously true for every `f` and every preorder, since no pair `a, b ∈ ∅` exists to violate the condition.
- **Singleton set**: `VTask.AntitoneOn f {c}` is vacuously true because the only pair `a = b = c` gives `f c ≤ f c` by reflexivity of the preorder on `β`.
- **Restriction to a smaller set**: if `VTask.AntitoneOn f s` holds and `t ⊆ s`, then `VTask.AntitoneOn f t` also holds, since any witness pair in `t` is also in `s`.
- **Composition**: composing two antitone-on functions (when the image of `f` on `s` lands in the domain set of `g`) yields a monotone-on function; composing a monotone-on and an antitone-on yields antitone-on.
- **Discontinuities**: an antitone-on function on a set may have at most countably many discontinuity points within that set.

## Not to be confused with

- `Antitone f` — the global version: `f` is order-reversing on its *entire* domain, not just on a subset `s`.
- `MonotoneOn f s` — the order-*preserving* analogue restricted to `s`; `a ≤ b` implies `f a ≤ f b`, the opposite direction.
- `StrictAntiOn f s` — the *strict* set-restricted version, requiring `a < b` to imply `f b < f a` (strict inequalities throughout).
