## Object

`VTask.StrictAnti f` is the proposition that the function `f` is *strictly antitone* (strictly order-reversing): whenever the input strictly increases, the output strictly decreases. Formally, `f` is strictly antitone when `a < b` implies `f b < f a` for every pair of elements `a`, `b` in the domain.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.StrictAnti : {α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.StrictAnti : {α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> Prop`

The implicit type arguments `α` and `β` are the domain and codomain types. The two instance arguments supply preorder structures on `α` and `β` respectively, providing the strict-less-than relations `<` used in the definition. The explicit argument `f` is the function being tested for strict antitonicity.

## Conventions

There are no junk-value or out-of-domain conventions to declare: `VTask.StrictAnti` is a universally quantified proposition over all pairs in the domain and is well-formed for any function between preordered types without restriction.

## Worked examples

- Claim: The negation function `Neg.neg : ℤ → ℤ` (i.e., `fun x => -x`) is strictly antitone on the integers with the natural order.

- Claim: The function `fun n : ℕ => 100 - n` (interpreted appropriately on a type with subtraction that respects order) is strictly antitone wherever it is order-reversing.

- Claim: `VTask.StrictAnti (fun x : ℤ => -x)` holds because for any integers `a < b` we have `-b < -a`.

- Claim: If `f : α → β` and `g : β → γ` are both strictly antitone (with appropriate preorder instances), then their composition `g ∘ f` is strictly monotone (not strictly antitone), illustrating that `VTask.StrictAnti` does not compose to `VTask.StrictAnti`.

- Claim: Every strictly antitone function is injective: if `VTask.StrictAnti f` then `Function.Injective f`.

## Boundaries

- On a type with no pairs satisfying `a < b` (e.g., a discrete preorder or a one-element type), every function vacuously satisfies `VTask.StrictAnti`, since the universal quantifier has no witnesses.
- `VTask.StrictAnti` requires strict inequalities on both sides; a function satisfying only the non-strict (`≤` implies `≥`) analogue is antitone but not necessarily strictly antitone.
- The codomain preorder matters: the same function `f` might be strictly antitone under one preorder on the codomain but fail under another.
- A strictly antitone function is automatically injective (no two distinct inputs can map to the same output) and in particular is not constant on any pair with a strict ordering between them.

## Not to be confused with

- `Antitone f`: the non-strict analogue requiring `a ≤ b → f b ≤ f a`; every strictly antitone function is antitone, but not conversely (e.g., a constant function is antitone but not strictly antitone on a nontrivial order).
- `StrictMono f`: strict monotonicity, the order-*preserving* version; `a < b → f a < f b` rather than `a < b → f b < f a`.
- `StrictAntiOn f s`: strict antitonicity restricted to a set `s`; `VTask.StrictAnti f` is the global (all-inputs) version, while `StrictAntiOn` is the pointwise restriction.