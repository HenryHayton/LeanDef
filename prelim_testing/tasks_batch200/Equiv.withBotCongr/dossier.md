## Object

`VTask.withBotCongr` lifts an equivalence (bijection) `e : α ≃ β` between two types to an equivalence `WithBot α ≃ WithBot β` between their respective "type with a bottom element added" versions. Concretely, the new equivalence sends the added bottom element `⊥` to `⊥`, and sends every lifted element `↑a` to `↑(e a)`. The inverse does the same with `e⁻¹`. This construction is functorial: it respects identity, reversal, and composition of equivalences.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.withBotCongr : {α : Type u_1} -> {β : Type u_2} -> (e : α ≃ β) -> WithBot α ≃ WithBot β
<!-- PINNED-SIGNATURE:END -->


`VTask.withBotCongr : {α : Type u_1} -> {β : Type u_2} -> (e : α ≃ β) -> WithBot α ≃ WithBot β`

The implicit arguments `α` and `β` are the source and target types of the underlying equivalence. The explicit argument `e` is the equivalence between `α` and `β` that is to be lifted to an equivalence between `WithBot α` and `WithBot β`.

## Conventions

There are no junk-value or out-of-domain conventions: the function is total, defined for every equivalence `e : α ≃ β` without restriction.

## Worked examples

- Claim: Applying `VTask.withBotCongr e` to the bottom element `⊥ : WithBot α` always returns `⊥ : WithBot β`, regardless of `e`.

- Claim: Applying `VTask.withBotCongr e` to a lifted element `(↑a : WithBot α)` returns `↑(e a) : WithBot β`.

- Claim: `VTask.withBotCongr (Equiv.refl α) = Equiv.refl (WithBot α)` — lifting the identity equivalence yields the identity equivalence on `WithBot α`.

- Claim: For equivalences `e₁ : α ≃ β` and `e₂ : β ≃ γ`, `VTask.withBotCongr (e₁.trans e₂) = (VTask.withBotCongr e₁).trans (VTask.withBotCongr e₂)` — the construction respects composition.

- Claim: For an equivalence `e : α ≃ β`, `VTask.withBotCongr e.symm = (VTask.withBotCongr e).symm` — lifting the inverse gives the inverse of the lifting.

## Boundaries

- The bottom element `⊥` is fixed by the equivalence: both the forward and backward maps send `⊥` to `⊥`.
- For every non-bottom element `↑a`, the forward map applies `e` and the backward map applies `e.symm`; there is no exceptional behaviour.
- The construction is defined for all universe levels `u_1` and `u_2`, making it universe-polymorphic.
- When `α = β` and `e = Equiv.refl α`, the resulting equivalence is the identity on `WithBot α`.

## Not to be confused with

- `Equiv.withTopCongr`: the analogous construction for `WithTop` (adding a top element) rather than `WithBot`.
- `WithBot.map`: the bare function `WithBot α → WithBot β` obtained by applying a function on the non-bottom elements; `VTask.withBotCongr` packages both directions into a full equivalence.
- `EquivFunctor.mapEquiv WithBot e`: a typeclass-driven version of the same construction, less universe-polymorphic and requiring a `Functor`/`EquivFunctor` instance.