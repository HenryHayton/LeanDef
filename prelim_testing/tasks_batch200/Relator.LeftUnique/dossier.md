## Object

A relation `R : α → β → Prop` is *left unique* if it behaves like a partial function from `β` to `α`: whenever two left-hand-side elements `a` and `b` are both related to the same right-hand-side element `c`, they must be equal. Equivalently, each element on the right is paired with **at most one** element on the left.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.LeftUnique : {α : Sort u₁} -> {β : Sort u₂} -> (R : α → β → Prop) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.LeftUnique` takes two implicit universe-polymorphic types `α` and `β`, together with an explicit binary relation `R : α → β → Prop`. It produces the proposition asserting that `R` is left unique. The type `α` is the "left-hand" or source type; `β` is the "right-hand" or target type; `R` is the relation whose left uniqueness is being asserted.

## Conventions

No special junk-value or edge conventions are declared for this definition: it is a universally quantified `Prop` that is vacuously true whenever `α` or `β` is empty, and this is not an assigned convention but simply the usual behaviour of universal quantification over an empty domain.

## Worked examples

- Claim: The membership relation `(· ∈ ·) : α → Option α → Prop` satisfies `VTask.LeftUnique`, because each `Option α` value contains at most one `α`.

- Claim: The equality relation `(· = ·) : α → α → Prop` satisfies `VTask.LeftUnique`, since if `a = c` and `b = c` then `a = b` by transitivity and symmetry.

- Claim: The relation `R : ℕ → ℕ → Prop` defined by `R a b ↔ a = 0 ∧ b = 0` does **not** satisfy `VTask.LeftUnique` in general once we replace `0` with a non-injective condition — but the constant-false relation `R a b := False` trivially satisfies `VTask.LeftUnique` because the hypothesis `R a c` is never fulfilled.

- Claim: If `R : α → β → Prop` satisfies `VTask.LeftUnique R`, then the flipped relation `flip R : β → α → Prop` satisfies `RightUnique (flip R)`, reflecting the symmetric dual property.

## Boundaries

- **Empty types**: If `α` is empty, `VTask.LeftUnique R` holds vacuously regardless of `R`, because the universal quantifier over `a` and `b` in `α` ranges over nothing.
- **Empty relation**: The relation that is `False` everywhere satisfies `VTask.LeftUnique` vacuously, since there are no witnesses to the hypothesis.
- **Total functional relations**: A relation induced by a function `f : α → β` via `R a b ↔ f a = b` is **not** in general left unique unless `f` is injective; left uniqueness of `R` here would require `f` to be injective.
- **List membership via Forall₂**: Left uniqueness lifts through `Forall₂`: if `R` is left unique, then `Forall₂ R` (pointwise lifting to lists) is also left unique.

## Not to be confused with

- `Relator.RightUnique`: The dual property — each left-hand element is paired with at most one right-hand element; this corresponds to `R` being a partial function from `α` to `β`, not from `β` to `α`.
- `Function.Injective`: Injectivity of a function `f : α → β` is the special case of left uniqueness for the functional relation `R a b ↔ f a = b`, but `VTask.LeftUnique` applies to arbitrary relations, not just those arising from functions.
- `Relator.BiUnique`: The conjunction of left uniqueness and right uniqueness; a strictly stronger property than `VTask.LeftUnique` alone.