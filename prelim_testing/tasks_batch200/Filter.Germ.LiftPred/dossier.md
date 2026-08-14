## Object

`VTask.LiftPred p f` is the proposition that the germ `f` (an equivalence class of functions from a filtered space into `β`, modulo eventual equality along the filter `l`) satisfies the predicate `p` in an eventual sense: it holds if and only if the underlying function eventually takes values satisfying `p`, i.e., the set of points where `p` holds belongs to the filter `l`. The definition is well-posed because eventual satisfaction is invariant under replacing a function by one that agrees with it eventually.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.LiftPred : {α : Type u_1} -> {β : Type u_2} -> {l : Filter α} -> (p : β → Prop) -> (f : l.Germ β) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.LiftPred : {α : Type u_1} -> {β : Type u_2} -> {l : Filter α} -> (p : β → Prop) -> (f : l.Germ β) -> Prop`

The implicit type `α` is the index type over which the filter `l` lives; `β` is the target type whose elements the predicate talks about; `l` is the filter on `α` that determines what "eventually" means; `p` is the predicate on `β` being lifted; and `f` is the germ, i.e., the equivalence class of functions `α → β` under eventual equality along `l`, to which the predicate is being applied.

## Conventions

There are no special junk-value or out-of-domain conventions for this definition: it is a total predicate defined for all filters `l`, all types `α` and `β`, all predicates `p : β → Prop`, and all germs `f : l.Germ β`.

## Worked examples

- Claim: For a constant function coerced to a germ, `VTask.LiftPred p (↑x : Filter.Germ l β)` holds whenever `p x` holds.

- Claim: `VTask.LiftPred p (f : Filter.Germ l β) ↔ ∀ᶠ x in l, p (f x)` — lifting a predicate to the germ of a concrete function `f : α → β` is equivalent to saying `p (f x)` holds for eventually all `x` in `l`.

- Claim: When `l` is a non-bot filter, `VTask.LiftPred p (↑x : Filter.Germ l β) ↔ p x` — for constant germs over a non-trivial filter, the lifted predicate reduces to the original predicate at the constant value.

- Claim: If `l = ⊥` (the bottom filter, where every set is a member), then `VTask.LiftPred p f` holds for any `f` and any `p`, because every statement holds eventually along `⊥`.

## Boundaries

- When `l = ⊥`, every set belongs to `l`, so `∀ᶠ x in l, p (f x)` is vacuously true regardless of `p` or `f`. Thus `VTask.LiftPred p f` holds for all `p` and `f` when `l = ⊥`.
- When `l` is a `NeBot` filter, a constant germ `↑x` satisfies `VTask.LiftPred p` if and only if `p x`; the filter non-triviality is needed to ensure the constant germ uniquely determines the value.
- The predicate `p` need not be decidable; `VTask.LiftPred` is purely propositional.
- The definition is well-defined on equivalence classes: if two functions `f` and `g` are eventually equal along `l`, then `∀ᶠ x in l, p (f x) ↔ ∀ᶠ x in l, p (g x)`, so the lifted predicate does not depend on the choice of representative.

## Not to be confused with

- `Filter.Germ.LiftRel`: lifts a *binary relation* between two germs rather than a unary predicate on one germ.
- `Filter.eventually`: a statement about an ordinary function `f : α → β`, not about its equivalence class; `VTask.LiftPred` packages this into a germ-level predicate.
- `Filter.Germ.map`: transports a *function* `β → γ` across a germ, rather than lifting a predicate to a proposition about the germ.