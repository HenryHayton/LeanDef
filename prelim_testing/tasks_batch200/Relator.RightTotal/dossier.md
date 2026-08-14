## Object

`VTask.RightTotal R` asserts that the relation `R : α → β → Prop` is *right total*: every element `b : β` is "covered" in the sense that there exists at least one `a : α` with `R a b`. In other words, the right-hand projection of `R` is surjective onto `β`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.RightTotal : {α : Sort u₁} -> {β : Sort u₂} -> (R : α → β → Prop) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.RightTotal : {α : Sort u₁} -> {β : Sort u₂} -> (R : α → β → Prop) -> Prop`

The two universe-polymorphic type arguments `α` and `β` are the domain and codomain sorts of the relation, inferred implicitly. The explicit argument `R` is the binary relation whose right totality is being asserted.

## Conventions

No special junk-value or out-of-domain conventions are declared for this definition: it is a straightforward universally-quantified proposition and is meaningful for every binary relation between any two sorts.

## Worked examples

- Claim: The relation `fun (n : ℕ) (m : ℕ) => n = m` is right total, because for every `m` we can choose `a = m`.

- Claim: The relation `fun (n : ℕ) (b : Bool) => (n = 0 ↔ b = true)` is right total over `ℕ → Bool`, since for `b = true` we pick `n = 0` and for `b = false` we pick `n = 1`.

- Claim: A well-founded strict order `r` on a nonempty type `α` is *not* right total, because the minimal element has no predecessor — formally `¬ VTask.RightTotal r`.

- Claim: If `R : α → β → Prop` is right total, then the lifted predicate transformer `(R ⇒ (· → ·)) ⇒ (· → ·)` preserves universal quantification: `(fun p => ∀ i, p i)` and `(fun q => ∀ i, q i)` are related by it.

## Boundaries

- When `β` is empty (`IsEmpty β`), the condition `∀ b, ∃ a, R a b` holds vacuously, so every relation is right total over an empty codomain type.
- When `α` is empty but `β` is nonempty, no relation can be right total, since there is no witness `a : α` to supply.
- Right totality makes no claim about uniqueness: multiple `a` values may satisfy `R a b` for a given `b`, and that is perfectly fine.
- The property is one-sided: right totality does not imply left totality (surjectivity onto `α`), nor any form of functionality.

## Not to be confused with

- `Relator.LeftTotal R` — the symmetric condition requiring every `a : α` to appear on the *left*, i.e., `∀ a, ∃ b, R a b`.
- `Function.Surjective f` — the special case of right totality when `R` is the graph of a function `f`; `VTask.RightTotal` generalises this to arbitrary relations.
- `Relator.BiTotal R` — the conjunction of left totality and right totality, requiring coverage on both sides simultaneously.