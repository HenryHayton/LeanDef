## Object

A function `f : α → β` between two preordered types is *order-preserving* (or *non-decreasing*) if whenever an element `a` of `α` is at most another element `b` of `α` in the order on `α`, the image `f a` is at most `f b` in the order on `β`. In classical mathematics this property is called monotonicity or being an order-homomorphism.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Monotone : {α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Monotone : {α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> Prop`

The universe-polymorphic type parameters `α` and `β` are the domain and codomain types; they are inferred implicitly. The two `Preorder` instances supply the `≤` relations used on `α` and on `β`. The explicit argument `f` is the function whose order-preserving behaviour is being asserted.

## Conventions

Because the property is stated with respect to the `≤` relation of a `Preorder`, it applies to any preorder, including partial orders, linear orders, and discrete orders. Every constant function on any preorder is considered to satisfy this property (since `a ≤ b` implies `c ≤ c` for any fixed `c`). On a type carrying the discrete order (where `a ≤ b` iff `a = b`), every function satisfies this property vacuously at distinct pairs.

## Worked examples

- Claim: The identity function on the natural numbers satisfies `VTask.Monotone id`.

- Claim: Any constant function `fun _ => c : ℕ → ℕ` satisfies `VTask.Monotone (fun _ => c)` because `c ≤ c` always holds.

- Claim: The function `fun n : ℕ => 2 * n` satisfies `VTask.Monotone (fun n => 2 * n)` because multiplying both sides of `a ≤ b` by 2 preserves the inequality.

- Claim: The function `fun n : ℕ => 0` satisfies `VTask.Monotone (fun _ : ℕ => 0)` since it is a constant.

- Claim: The negation function `fun b : Bool => !b` does *not* satisfy `VTask.Monotone (fun b : Bool => !b)` under the standard order on `Bool` (where `false < true`), because `false ≤ true` but `!false = true` and `!true = false`, so `true ≰ false`.

## Boundaries

- **Reflexive pairs**: For any `a`, we have `a ≤ a` (reflexivity of a preorder), so the condition requires `f a ≤ f a`, which holds automatically. There is no special boundary behaviour here.
- **Preorder vs partial order**: The property only uses `≤`, not strict inequality `<`. A function that maps two equivalent (but not equal) elements to values where the order is reversed would still fail, but equal elements trivially satisfy the condition.
- **Empty domain**: If `α` is an empty type, the universal quantification is vacuously true, so every function from an empty type satisfies the property.
- **Single-element domain**: Any function from a one-element preorder is vacuously order-preserving.
- **The `Prop`-valued nature**: `VTask.Monotone f` is itself a proposition; it is neither a number nor a set, so there is no "value" to speak of at boundary inputs.

## Not to be confused with

- **`MonotoneOn`**: The same order-preserving condition but restricted to a specified subset of the domain, rather than holding universally.
- **`StrictMono`**: Requires `a < b → f a < f b` (strict inequality on both sides), which is a stronger condition than `VTask.Monotone`.
- **`Antitone`**: The opposite condition, requiring `a ≤ b → f b ≤ f a`; order-*reversing* rather than order-preserving.