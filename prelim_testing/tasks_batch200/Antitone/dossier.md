## Object

A function between two preordered sets is called **antitone** (or order-reversing) if it sends smaller inputs to larger outputs: whenever `a ≤ b` in the domain, we have `f b ≤ f a` in the codomain. In classical analysis this is also called a *decreasing* function (in the non-strict sense).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Antitone : {α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Antitone : {α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> Prop`

The type variables `α` and `β` are the domain and codomain types, respectively. The two `Preorder` instances supply the notions of `≤` on each type. The explicit argument `f` is the function whose order-reversing behaviour is being asserted.

## Conventions

No special junk-value or boundary conventions are declared for this predicate: it is a universally-quantified proposition that is simply true or false for any given function and pair of preorders, with no distinguished edge inputs requiring special treatment.

## Worked examples

- Claim: The negation function `fun (n : ℤ) => -n` satisfies `VTask.Antitone` with respect to the standard order on `ℤ`, because `a ≤ b` implies `-b ≤ -a`.

- Claim: Any constant function `fun (_ : α) => c` satisfies `VTask.Antitone`, since `c ≤ c` holds regardless of how the inputs compare.

- Claim: The composition of two antitone functions is monotone (not antitone), so `VTask.Antitone (g ∘ f)` does **not** follow from `VTask.Antitone f` and `VTask.Antitone g` alone; instead their composition is order-preserving.

- Claim: If `f : α → β` and `g : β → γ` with `g` monotone and `f` antitone, then `g ∘ f` is antitone.

## Boundaries

- On a type where every pair of elements is incomparable (e.g. a discrete preorder), every function trivially satisfies `VTask.Antitone` because the hypothesis `a ≤ b` is never satisfied for distinct `a` and `b`.
- On a type with only one element, every function is trivially antitone.
- The predicate uses non-strict `≤` throughout; it does not require strict order-reversal, so constant functions always qualify.
- The definition makes no continuity or measurability requirement; it is a purely order-theoretic condition.

## Not to be confused with

- **`Monotone`**: the order-*preserving* counterpart; `a ≤ b` implies `f a ≤ f b`.
- **`StrictAnti`**: the *strict* version requiring `a < b → f b < f a`; antitone does not imply strict antitone.
- **`AntitoneOn`**: the *set-restricted* variant asserting the order-reversing property only for pairs drawn from a specified subset of the domain.