## Object

`VTask.BiTotal R` is a proposition asserting that the relation `R : α → β → Prop` is **bi-total**: every element of `α` is related to at least one element of `β` (left totality), **and** every element of `β` is related to at least one element of `α` (right totality). In other words, `R` has no "gaps" on either side — neither type can have an element that is entirely ignored by the relation.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.BiTotal : {α : Sort u₁} -> {β : Sort u₂} -> (R : α → β → Prop) -> Prop
<!-- PINNED-SIGNATURE:END -->


`{α : Sort u₁} -> {β : Sort u₂} -> (R : α → β → Prop) -> Prop`

The two universe-polymorphic sort arguments `α` and `β` are the domain and codomain types of the relation, respectively; they are implicit and inferred from context. The explicit argument `R` is the binary relation whose bi-totality is being asserted.

## Conventions

No special junk-value or boundary conventions are declared for this predicate: it is a straightforward conjunction of two totality conditions and is defined for any binary relation on any two sorts.

## Worked examples

- Claim: The equality relation `@Eq α` on any type `α` is bi-total, because every element equals itself.

- Claim: If `R : α → β → Prop` is bi-total, then the lifted quantifier transfer `((R ⇒ Iff) ⇒ Iff) (fun p => ∀ i, p i) (fun q => ∀ i, q i)` holds — universal quantification is preserved in both directions across `R`.

- Claim: The empty relation on `ℕ` (sending every pair to `False`) is **not** bi-total, since no element of `ℕ` is related to anything.

- Claim: If `f : α → β` is a surjective function, then the graph relation `R a b ↔ f a = b` is bi-total.

## Boundaries

- When `α` or `β` is an empty type (`Sort 0` with no inhabitants), left totality and right totality are vacuously true for those empty sides, so `VTask.BiTotal R` holds trivially for any `R` when either type is empty.
- When `α` and `β` are both nonempty, `VTask.BiTotal R` is a substantive requirement: the relation must cover every element on both sides.
- `VTask.BiTotal R` is a `Prop`; it carries no computational data, only a logical certificate.

## Not to be confused with

- `LeftTotal R`: only requires that every element of `α` is related to some element of `β`; the condition on `β` is absent.
- `RightTotal R`: only requires that every element of `β` is related back to some element of `α`; the condition on `α` is absent.
- `BiUnique R` (or `Relator.BiUnique`): requires that `R` is both left-unique and right-unique (i.e., functional and injective), which is an orthogonal concept to totality.