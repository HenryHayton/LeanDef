## VTask.StrictMonoOn

### Object

`VTask.StrictMonoOn f s` is the proposition asserting that the function `f` is *strictly monotone on the set `s`*: whenever `a` and `b` are both elements of `s` and `a` is strictly less than `b` (in the preorder on `α`), it follows that `f a` is strictly less than `f b` (in the preorder on `β`). Informally, restricted to `s`, the function `f` preserves strict inequalities.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.StrictMonoOn : {α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> (s : Set α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`{α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> (s : Set α) -> Prop`

The two universe-polymorphic type arguments `α` and `β` are the domain and codomain types, respectively; they are inferred implicitly. The two `Preorder` instance arguments supply the strict-order structure on `α` and on `β` needed to make sense of `<` on each side. The explicit argument `f` is the function whose monotonicity is being asserted. The explicit argument `s` is the subset of `α` on which the assertion is restricted: only pairs of elements from `s` are considered.

### Conventions

When `s` is the empty set or a singleton, the condition is vacuously satisfied by any function, since there are no pairs `a < b` with both in `s`. No special junk values are assigned; the definition is a universally quantified proposition and is simply `True` in those degenerate cases by vacuity.

### Worked examples

- Claim: The squaring function `fun n : ℕ => n * n` is strictly monotone on the full set of natural numbers (viewed as `Set.univ`).

- Claim: The constant function `fun _ : ℕ => 0` is **not** `VTask.StrictMonoOn` on any set containing two distinct elements, since `0 < 1` in `ℕ` but the image of any two elements is the same.

- Claim: `VTask.StrictMonoOn id s` holds for every set `s : Set α` in any preorder `α` where `<` is the strict part of the order — because `id a = a < b = id b` whenever `a < b`.

- Claim: `VTask.StrictMonoOn (fun x : ℝ => x ^ 3) Set.univ` holds, reflecting that the cube function is strictly increasing on all of ℝ.

- Claim: If `VTask.StrictMonoOn f s` holds and `t ⊆ s`, then `VTask.StrictMonoOn f t` holds, because any pair in `t` is also a pair in `s`.

### Boundaries

- **Empty set**: `VTask.StrictMonoOn f ∅` is vacuously true for any `f`, since the universal quantifier over elements of `∅` has no witnesses.
- **Singleton**: `VTask.StrictMonoOn f {a}` is vacuously true for any `f` and `a`, since there is no pair with `a < b` when both must equal `a`.
- **Full set (`Set.univ`)**: `VTask.StrictMonoOn f Set.univ` is equivalent to the global `StrictMono f`, since every element of `α` belongs to `Set.univ`.
- **Non-strict (`a ≤ b`)**: The definition uses strict inequality `a < b → f a < f b`; it does not require anything about equal elements, so a strictly monotone function on `s` may still fail to be injective if the underlying order has incomparable elements (though in a linear order, strict monotonicity implies injectivity on `s`).

### Not to be confused with

- **`StrictMono f`**: the global version asserting `∀ a b, a < b → f a < f b`, with no subset restriction; equivalent to `VTask.StrictMonoOn f Set.univ`.
- **`MonotonOn f s`** (also written `VTask.MonoOn`): the *non-strict* version, requiring only `a ≤ b → f a ≤ f b` for `a, b ∈ s`; strictly weaker than `VTask.StrictMonoOn f s`.
- **`StrictAntiOn f s`**: the analogous predicate for *strict anti-monotonicity*, requiring `a < b → f b < f a` for `a, b ∈ s`; same shape but opposite direction.
