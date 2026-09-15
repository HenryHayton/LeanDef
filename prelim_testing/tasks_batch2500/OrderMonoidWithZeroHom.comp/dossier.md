## Object

Given two composable order-preserving monoid-with-zero homomorphisms — maps that simultaneously preserve the multiplication, the multiplicative identity, zero, and the partial order — `VTask.comp f g` is their composite, the map that first applies `g` and then applies `f`. The result is again an order-preserving monoid-with-zero homomorphism.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {α : Type u_2} -> {β : Type u_3} -> {γ : Type u_4} -> [Preorder α] -> [Preorder β] -> [Preorder γ] -> [MulZeroOneClass α] -> [MulZeroOneClass β] -> [MulZeroOneClass γ] -> (f : β →*₀o γ) -> (g : α →*₀o β) -> α →*₀o γ
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_2} -> {β : Type u_3} -> {γ : Type u_4} -> [Preorder α] -> [Preorder β] -> [Preorder γ] -> [MulZeroOneClass α] -> [MulZeroOneClass β] -> [MulZeroOneClass γ] -> (f : β →*₀o γ) -> (g : α →*₀o β) -> α →*₀o γ`

The implicit type arguments `α`, `β`, `γ` are the source, intermediate, and target types. The preorder and `MulZeroOneClass` instances on each type supply the order and the algebraic structure (multiplication, one, and zero). The explicit argument `f` is the outer morphism from `β` to `γ`; it is applied second. The explicit argument `g` is the inner morphism from `α` to `β`; it is applied first.

## Conventions

No junk-value or edge conventions are declared for this definition: it is a total construction on well-typed inputs and every valid pair `(f, g)` produces a meaningful composite morphism with no degenerate cases.

## Worked examples

- Claim: For the identity-like morphisms on a preordered monoid-with-zero `α`, composing any morphism `f : α →*₀o α` with the identity (viewed as a morphism) recovers `f` pointwise.

- Claim: If `f : β →*₀o γ` and `g : α →*₀o β`, then `VTask.comp f g` maps `1 : α` to `1 : γ`, because both `f` and `g` preserve the multiplicative identity.

- Claim: If `f : β →*₀o γ` and `g : α →*₀o β`, then `VTask.comp f g` maps `0 : α` to `0 : γ`, because both `f` and `g` preserve zero.

- Claim: If `f : β →*₀o γ` and `g : α →*₀o β`, and `a ≤ b` in `α`, then `VTask.comp f g a ≤ VTask.comp f g b` in `γ`, because both morphisms are order-preserving.

## Boundaries

- The composition is defined for any two morphisms with matching intermediate type; there are no restrictions beyond well-typedness.
- When either `f` or `g` is the identity morphism (if one exists for the relevant type), the composite coincides with the other morphism.
- The operation is associative: composing three morphisms in either bracketing order yields the same composite map.
- The underlying function of `VTask.comp f g` is exactly the set-theoretic composition `fun a => f (g a)`.

## Not to be confused with

- `OrderMonoidHom.comp`: composition of order-preserving monoid homomorphisms that do *not* necessarily preserve zero; `VTask.comp` additionally requires and preserves the zero element.
- `MonoidWithZeroHom.comp`: composition of monoid-with-zero homomorphisms that are *not* required to be order-preserving; `VTask.comp` adds the order-monotonicity condition.
- `Function.comp`: plain function composition with no algebraic or order structure; `VTask.comp` bundles the proof that the composite preserves multiplication, one, zero, and the order.