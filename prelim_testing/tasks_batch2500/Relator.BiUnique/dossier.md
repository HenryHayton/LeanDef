## Object

`VTask.BiUnique R` asserts that the relation `R : α → β → Prop` is *bi-unique*: every element on the left side is related to **at most one** element on the right side, and every element on the right side is related to **at most one** element on the left side. In other words, `R` behaves like a partial injective function in both directions simultaneously — it is both a partial function from `α` to `β` and a partial function from `β` to `α`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.BiUnique : {α : Sort u₁} -> {β : Sort u₂} -> (R : α → β → Prop) -> Prop
<!-- PINNED-SIGNATURE:END -->


VTask.BiUnique : {α : Sort u₁} -> {β : Sort u₂} -> (R : α → β → Prop) -> Prop

The two universe-polymorphic type arguments `α` and `β` are the domain and codomain sorts of the relation. The explicit argument `R` is the binary relation being tested: it maps an element of `α` and an element of `β` to a proposition.

## Conventions

There are no declared junk-value or edge-case conventions for this definition: it is a straightforward propositional conjunction over the two uniqueness conditions, and it is defined for any relation regardless of the sizes or structures of `α` and `β`.

## Worked examples

- Claim: The equality relation `(· = ·) : α → α → Prop` is bi-unique, because each element is equal to exactly one thing — itself.

- Claim: The relation `R a b ↔ (a = 0 ∧ b = 0)` on `ℕ` is bi-unique: the only pair in the relation is `(0, 0)`, so both left and right uniqueness hold trivially.

- Claim: If `R` is bi-unique, then `R` preserves equality in the sense that `R a b → R a b' → b = b'` (right uniqueness) and `R a b → R a' b → a = a'` (left uniqueness).

- Claim: If `R : α → β → Prop` is bi-unique and `Forall₂ R xs ys` and `Forall₂ R xs zs`, then `ys = zs`, because `Forall₂ R` inherits bi-uniqueness from `R`.

## Boundaries

- The **empty relation** (which never holds) is trivially bi-unique, since the uniqueness conditions are vacuously satisfied.
- A relation that maps **every** element of `α` to **every** element of `β` fails bi-uniqueness as soon as `|α| > 1` or `|β| > 1`, because a single element on one side would be related to multiple elements on the other.
- Bi-uniqueness does **not** require `R` to be total or surjective; elements may be unrelated to anything.
- When `α = β` and `R` is the identity relation, bi-uniqueness holds.

## Not to be confused with

- `Relator.LeftUnique R` — only the half of bi-uniqueness stating that distinct left elements cannot share a right image; bi-uniqueness additionally requires right uniqueness.
- `Relator.RightUnique R` — only the half of bi-uniqueness stating that a single left element has at most one right partner; bi-uniqueness additionally requires left uniqueness.
- `Function.Injective f` — injectivity of a *total* function implies left uniqueness of its graph, but injectivity says nothing about right uniqueness and requires the function to be defined everywhere, whereas bi-uniqueness applies to arbitrary partial relations.