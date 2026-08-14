## Object

`VTask.StrictAntiOn f s` is the proposition that the function `f` is **strictly antitone on the set `s`**: for every pair of elements `a, b` belonging to `s`, if `a` is strictly less than `b` (in the preorder on `α`), then `f b` is strictly less than `f a` (in the preorder on `β`). In other words, `f` strictly reverses order among elements of `s`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.StrictAntiOn : {α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> (s : Set α) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.StrictAntiOn : {α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> (s : Set α) -> Prop
```

The type arguments `α` and `β` are the domain and codomain types, each equipped with a preorder (supplied as instance arguments). The explicit argument `f` is the function whose order-reversing behaviour is being asserted. The explicit argument `s` is the subset of `α` on which the strict antitone condition is required to hold; points outside `s` are entirely unconstrained.

## Conventions

No special junk-value or boundary conventions are declared for this predicate. It is a universally quantified proposition and is vacuously true whenever `s` contains fewer than two comparable elements (e.g., when `s` is empty or a singleton, or more generally when `s` is a subsingleton).

## Worked examples

- Claim: The negation function `fun x : ℤ => -x` is strictly antitone on the entire set of integers (`Set.univ`).

- Claim: Any strictly antitone function on a set `s` is injective on `s` (i.e., `VTask.StrictAntiOn f s → s.InjOn f`).

- Claim: The function `fun x : ℝ => x⁻¹` is strictly antitone on `Set.Ioi 0` (the positive reals).

- Claim: If `g` is strictly monotone on `t` and `f` is strictly antitone on `s` with `f` mapping `s` into `t`, then `g ∘ f` is strictly antitone on `s`.

## Boundaries

- **Empty set**: `VTask.StrictAntiOn f ∅` holds vacuously for every `f`, since there are no elements `a, b ∈ ∅` to consider.
- **Singleton set**: `VTask.StrictAntiOn f {a}` holds vacuously: there is no pair of distinct elements, so the hypothesis `a < b` with both in the singleton can never be satisfied.
- **Subsingleton set**: More generally, if `s` is a subsingleton (has at most one element), `VTask.StrictAntiOn f s` is vacuously true.
- **Universal set**: On `Set.univ`, `VTask.StrictAntiOn f Set.univ` is exactly the global strict antitonicity of `f` (i.e., `StrictAnti f`).
- **Constant function**: A constant function on a set with two or more comparable elements fails `VTask.StrictAntiOn`, since `f b < f a` cannot hold when `f a = f b`.

## Not to be confused with

- **`AntitoneOn f s`**: the non-strict version; requires only `a ≤ b → f b ≤ f a`, which permits `f a = f b`.
- **`StrictMonoOn f s`**: the order-*preserving* analogue; requires `a < b → f a < f b`, the opposite direction.
- **`StrictAnti f`**: the global (set-unrestricted) version of the same condition, applying to all elements of `α` rather than just those in a specified subset `s`.