## Object

`VTask.StrictMono f` is the predicate asserting that the function `f : α → β` is **strictly monotone**: whenever `a < b` holds in `α`, it follows that `f a < f b` holds in `β`. In other words, `f` preserves the strict order exactly — it never collapses a strict inequality and never reverses one.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.StrictMono : {α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.StrictMono : {α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> Prop`

The universe-polymorphic type parameters `α` and `β` are the domain and codomain of `f`, supplied implicitly. The two `Preorder` instances supply the strict-order relations `<` on `α` and on `β` respectively; they too are inferred automatically. The explicit argument `f` is the function whose strict monotonicity is being asserted.

## Conventions

There are no junk-value or out-of-domain conventions to declare: `VTask.StrictMono` is a universally-quantified `Prop` that is well-formed and meaningful for any function between any two preorders, with no edge inputs that receive a distinguished default treatment.

## Worked examples

- Claim: The natural-number successor function `Nat.succ` satisfies `VTask.StrictMono Nat.succ`, because `n < m` implies `n + 1 < m + 1`.

- Claim: The identity function on any preorder satisfies `VTask.StrictMono id`, since `a < b` trivially gives `id a < id b`.

- Claim: A constant function `fun _ : ℕ => 0` does **not** satisfy `VTask.StrictMono (fun _ : ℕ => 0)`, because `0 < 1` but `0` is not strictly less than `0`.

- Claim: The function `fun n : ℕ => 2 * n` satisfies `VTask.StrictMono (fun n : ℕ => 2 * n)`, because doubling preserves strict inequality on natural numbers.

## Boundaries

- On a **single-element type** (or any preorder with no pair satisfying `a < b`), the universal statement is vacuously true, so every function out of such a type is trivially strictly monotone.
- On **discrete preorders** where `<` is empty (e.g., `Prop` with the trivial order), strict monotonicity is again vacuous.
- The predicate applies to functions between **preorders**, not just partial or linear orders; in a preorder `a < b` means `a ≤ b ∧ ¬(b ≤ a)`, so strict monotonicity is meaningful even when the order is not antisymmetric.
- A strictly monotone function between linear orders is automatically **injective**; this is a derived fact, not part of the definition.
- `VTask.StrictMono f` implies the weaker `Monotone f` (i.e., `a ≤ b → f a ≤ f b`), but not vice versa.

## Not to be confused with

- `Monotone f` — the non-strict version: `a ≤ b → f a ≤ f b`; every strictly monotone function is monotone, but a monotone function need not be strictly monotone (e.g., constant functions).
- `StrictMonoOn f s` — strict monotonicity restricted to a subset `s` of the domain; `VTask.StrictMono f` is the global (whole-domain) version.
- `StrictAnti f` (strict antitonicity) — the reversed predicate: `a < b → f b < f a`; this describes order-reversing functions, not order-preserving ones.
