## 1. Object

A germ `P` of functions `α → β` along a filter `l` is **constant** (with respect to `l`) if there exists some value `b : β` such that the underlying function agrees with the constant function `fun _ ↦ b` on a set belonging to the filter `l`. In other words, the function is eventually equal to a single fixed value.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsConstant : {α : Type u_1} -> {β : Type u_2} -> {l : Filter α} -> (P : l.Germ β) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.IsConstant : {α : Type u_1} -> {β : Type u_2} -> {l : Filter α} -> (P : l.Germ β) -> Prop
```

The implicit type arguments `α` and `β` are the domain and codomain types of the functions forming the germ. The implicit argument `l` is the filter on `α` with respect to which the germ and the notion of "eventually" are defined. The explicit argument `P` is the germ — an equivalence class of functions `α → β` under the relation of eventual equality along `l` — whose constancy is being asserted.

## 3. Conventions

The predicate is well-defined on germs: if two functions represent the same germ (i.e., they are eventually equal along `l`), then one is eventually constant if and only if the other is. There are no junk-value conventions to declare since `IsConstant` is a well-posed predicate on all germs without restriction.

## 4. Worked Examples

- Claim: The germ of the literal constant function `fun _ : α ↦ b` along any filter `l` satisfies `VTask.IsConstant`.

- Claim: If `f : α → β` satisfies `∀ x, f x = b` for some fixed `b`, then the germ `(↑f : Filter.Germ l β)` satisfies `VTask.IsConstant`.

- Claim: If `(↑f : Filter.Germ l β).IsConstant` and `g : β → γ` is any function, then `(↑(g ∘ f) : Filter.Germ l γ).IsConstant`.

- Claim: If `f : α → β` is eventually equal to two different constants `b₁` and `b₂` along a non-empty filter `l`, then `b₁ = b₂` (the eventual constant value is unique when the filter is non-trivial).

## 5. Boundaries

- When `l = ⊥` (the bottom filter, which contains every set), every germ along `⊥` trivially satisfies `IsConstant`, because the "eventually equal" condition is vacuous.
- When `β` has a single element, every germ is constant regardless of the filter.
- A germ along `l = Filter.principal s` for a set `s` is constant if and only if the function takes a single value on all of `s`.
- The predicate depends only on the equivalence class (the germ), not on any particular representative function.

## 6. Not to be confused with

- `Filter.Germ` itself: that is the type of germs; `VTask.IsConstant` is a predicate on germs, not the germ type.
- Pointwise constancy of a function: `VTask.IsConstant` requires only *eventual* constancy (constancy on a filter-large set), not global constancy everywhere.
- `Filter.EventuallyEq`: that is the relation of two functions or germs being eventually equal to *each other*; `VTask.IsConstant` asserts eventual equality to some *constant* function, which is a special case.