## Object

`VTask.copy` constructs a new order-preserving monoid homomorphism (of type `α →*o β`) from an existing order-preserving monoid-with-zero homomorphism `f : α →*₀o β`, by replacing its underlying function with a definitionally different but propositionally equal function `f'`. The resulting morphism carries exactly the same algebraic and order data as `f`, but its "to-function" component is literally `f'` rather than the coercion of `f`. This is a standard Mathlib bookkeeping device: when you have a function `f'` that you know equals `⇑f`, you can produce a morphism whose `toFun` is definitionally `f'`, which can resolve definitional-equality goals that the original `f` would not satisfy.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [Preorder α] -> [Preorder β] -> [MulZeroOneClass α] -> [MulZeroOneClass β] -> (f : α →*₀o β) -> (f' : α → β) -> (h : f' = ⇑f) -> α →*o β
<!-- PINNED-SIGNATURE:END -->


`VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [Preorder α] -> [Preorder β] -> [MulZeroOneClass α] -> [MulZeroOneClass β] -> (f : α →*₀o β) -> (f' : α → β) -> (h : f' = ⇑f) -> α →*o β`

The implicit type arguments `α` and `β` are the source and target types, respectively. The four instance arguments supply the preorder structures on `α` and `β` and the `MulZeroOneClass` (multiplicative monoid-with-zero) structures on each. The explicit argument `f` is the original order-preserving monoid-with-zero homomorphism being copied. The argument `f'` is the new underlying function to use in place of `⇑f`. The argument `h` is a proof that `f'` equals the coercion `⇑f`, ensuring the replacement is propositionally sound.

## Conventions

There are no junk-value or out-of-domain conventions to declare: every combination of inputs satisfying `h : f' = ⇑f` yields a well-defined result, and the definition is total over its stated domain.

## Worked examples

- Claim: For any `f : α →*₀o β`, calling `VTask.copy f (⇑f) rfl` yields a morphism whose underlying function is `⇑f`.

- Claim: The morphism produced by `VTask.copy f f' h` is propositionally equal to `f` as an order-preserving monoid-with-zero homomorphism when viewed through the `copy_eq` theorem; that is, `VTask.copy f f' h` and `f` agree on all inputs.

- Claim: The coercion of `VTask.copy f f' h` to a function is exactly `f'`; that is, `⇑(VTask.copy f f' h) = f'` holds by `coe_copy`.

## Boundaries

- The proof `h` must establish `f' = ⇑f` (not merely extensional equality); any function propositionally equal to `⇑f` is accepted.
- The output type is `α →*o β` (an order-preserving monoid homomorphism), not the stronger `α →*₀o β`; the zero-preservation data is used internally but the returned bundled morphism type is the weaker one.
- When `f'` is literally `⇑f` and `h` is `rfl`, the construction is a no-op up to definitional equality.
- There are no restrictions on the types `α` and `β` beyond the stated typeclass assumptions.

## Not to be confused with

- `OrderMonoidWithZeroHom` (`α →*₀o β`) itself: this is the source type of `f`, which carries the full zero-preserving data; `VTask.copy` returns only `α →*o β`.
- `MonoidWithZeroHom.copy` (`α →*₀ β` version): that operation copies a monoid-with-zero homomorphism without the order structure, whereas `VTask.copy` also threads through the order-monoid structure.
- `OrderMonoidHom.copy` (`α →*o β` version): that copies an order-monoid homomorphism without zero-preservation, whereas `VTask.copy` takes an `α →*₀o β` as input and uses both the order and zero data during construction.