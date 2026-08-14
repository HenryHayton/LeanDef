## Object

A binary relation `R : α → β → Prop` is **right unique** (also called *right-univalent* or *functional*) if whenever a single left-hand element `a` is related to two right-hand elements `b` and `c`, those two elements must be equal. In other words, each element of `α` is paired with **at most one** element of `β` — the relation behaves like a partial function from `α` to `β`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.RightUnique : {α : Sort u₁} -> {β : Sort u₂} -> (R : α → β → Prop) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.RightUnique : {α : Sort u₁} -> {β : Sort u₂} -> (R : α → β → Prop) -> Prop`

The two universe-polymorphic sort arguments `α` and `β` are the domain and codomain types of the relation, inferred implicitly. The explicit argument `R` is the binary relation whose right-uniqueness is being asserted.

## Conventions

No special junk-value or edge-case conventions are declared: `VTask.RightUnique` is a universally-quantified proposition that is total and well-defined for every relation, including the empty relation and the full relation.

## Worked examples

- Claim: The equality relation `(· = ·) : α → α → Prop` is right unique, because `a = b` and `a = c` together imply `b = c`.

- Claim: The membership relation `(· ∈ ·) : α → Part α → Prop` (for the `Part` monad) is right unique — a `Part α` value contains at most one element.

- Claim: The full relation `fun (_a : α) (_b : β) => True` is **not** right unique whenever `β` has at least two distinct elements, since every left element is related to all right elements.

- Claim: If `r : α → β → Prop` is left unique, then `flip r : β → α → Prop` is right unique.

## Boundaries

- **Empty relation**: `fun _ _ => False` is vacuously right unique, because the antecedents `R a b` and `R a c` are never satisfied.
- **Singleton codomain**: Any relation into a one-element type is trivially right unique.
- **Full relation on a type with two or more elements**: Not right unique.
- **Partial functions**: A relation that encodes a genuine partial function is exactly a right-unique relation; the two notions coincide.

## Not to be confused with

- `Relator.LeftUnique R` — the dual condition: each right-hand element is paired with at most one left-hand element (injectivity direction).
- `Function.Injective f` — injectivity of a total function, which implies left-uniqueness of the associated relation `R a b ↔ f a = b`, not right-uniqueness.
- `Function.bijective` / surjectivity — orthogonal to right-uniqueness; right-uniqueness says nothing about coverage of the codomain.