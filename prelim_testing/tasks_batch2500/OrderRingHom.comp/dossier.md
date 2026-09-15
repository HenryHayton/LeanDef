## Object

`VTask.comp` is the composition of two order-preserving ring homomorphisms. Given a map `f : β →+*o γ` and a map `g : α →+*o β`, it produces the composite map `α →+*o γ` that first applies `g` (from `α` to `β`) and then applies `f` (from `β` to `γ`). The result is again simultaneously a ring homomorphism and an order-preserving map.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {α : Type u_2} -> {β : Type u_3} -> {γ : Type u_4} -> [NonAssocSemiring α] -> [Preorder α] -> [NonAssocSemiring β] -> [Preorder β] -> [NonAssocSemiring γ] -> [Preorder γ] -> (f : β →+*o γ) -> (g : α →+*o β) -> α →+*o γ
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_2} -> {β : Type u_3} -> {γ : Type u_4} -> [NonAssocSemiring α] -> [Preorder α] -> [NonAssocSemiring β] -> [Preorder β] -> [NonAssocSemiring γ] -> [Preorder γ] -> (f : β →+*o γ) -> (g : α →+*o β) -> α →+*o γ`

The three implicit type arguments `α`, `β`, `γ` are the source, intermediate, and target types respectively; each must carry both a `NonAssocSemiring` structure and a `Preorder`. The instance arguments supply these algebraic and order structures automatically. The first explicit argument `f` is the outer ("later") order-ring homomorphism, mapping from `β` to `γ`. The second explicit argument `g` is the inner ("earlier") order-ring homomorphism, mapping from `α` to `β`. Composition is applied in the standard mathematical order: `g` is applied first, then `f`.

## Conventions

No junk-value or edge-case conventions are declared: the definition is total and has no distinguished degenerate inputs requiring special semantic notes.

## Worked examples

- Claim: For any order-ring homomorphisms `f : β →+*o γ` and `g : α →+*o β`, and any element `x : α`, evaluating `VTask.comp f g` at `x` gives the same result as `f (g x)`.

- Claim: `VTask.comp` preserves the ring homomorphism property: if `f` and `g` each send `1` to `1`, then so does `VTask.comp f g`, since `(VTask.comp f g) 1 = f (g 1) = f 1 = 1`.

- Claim: `VTask.comp` preserves the order-preserving property: if `x ≤ y` in `α`, then `g x ≤ g y` in `β` (since `g` is order-preserving), and then `f (g x) ≤ f (g y)` in `γ` (since `f` is order-preserving), so the composite is also order-preserving.

- Claim: Composition is associative: for order-ring homomorphisms `f : γ →+*o δ`, `g : β →+*o γ`, `h : α →+*o β`, we have `VTask.comp f (VTask.comp g h) = VTask.comp (VTask.comp f g) h` as functions on elements.

## Boundaries

- The definition is total: it is defined for any two composable order-ring homomorphisms without restriction.
- When either `f` or `g` is the identity order-ring homomorphism on its respective type, `VTask.comp` with it is the identity on the resulting composite (up to definitional equality on underlying functions).
- The intermediate type `β` must match exactly: the codomain of `g` and the domain of `f` must be the same type with the same semiring and preorder structures.
- The order component is preserved strictly in the sense of the underlying preorder (not necessarily a partial order or total order); the definition works for any `Preorder`.

## Not to be confused with

- `RingHom.comp`: the composition of plain ring homomorphisms, which ignores any order structure entirely.
- `OrderHom.comp`: the composition of order-preserving maps on preordered types, which carries no ring structure.
- `OrderRingIso.trans`: composition of order-ring *isomorphisms* (invertible maps), a strictly stronger notion than mere homomorphisms.
