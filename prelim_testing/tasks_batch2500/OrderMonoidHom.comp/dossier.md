## Object

`VTask.comp` constructs the composite of two order-preserving monoid homomorphisms. Given maps `f : β →*o γ` and `g : α →*o β`, it produces the map `α →*o γ` that sends each element `a : α` to `f(g(a))`. The result respects both the monoid structure (it is a monoid homomorphism) and the order structure (it is order-preserving) because both of those properties are preserved by ordinary function composition.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {α : Type u_2} -> {β : Type u_3} -> {γ : Type u_4} -> [Preorder α] -> [Preorder β] -> [Preorder γ] -> [MulOneClass α] -> [MulOneClass β] -> [MulOneClass γ] -> (f : β →*o γ) -> (g : α →*o β) -> α →*o γ
<!-- PINNED-SIGNATURE:END -->


`VTask.comp : {α : Type u_2} -> {β : Type u_3} -> {γ : Type u_4} -> [Preorder α] -> [Preorder β] -> [Preorder γ] -> [MulOneClass α] -> [MulOneClass β] -> [MulOneClass γ] -> (f : β →*o γ) -> (g : α →*o β) -> α →*o γ`

The three universe-polymorphic types `α`, `β`, and `γ` are the domain, intermediate, and codomain types respectively. Each carries a `Preorder` instance (providing the order structure) and a `MulOneClass` instance (providing the monoid structure). The first explicit argument `f` is the outer order-preserving monoid homomorphism (from `β` to `γ`); the second explicit argument `g` is the inner order-preserving monoid homomorphism (from `α` to `β`). The result is the composite map from `α` to `γ`.

## Conventions

There are no special junk-value or edge conventions for this definition: it is a total construction well-defined for all valid inputs, and the order and monoid laws are always satisfied by composition.

## Worked examples

- Claim: Composing two identity maps (viewed as `OrderMonoidHom`s) yields an identity-like map, i.e., for any `a : α`, `VTask.comp (OrderMonoidHom.id α) (OrderMonoidHom.id α) a = a`.

- Claim: For `f : β →*o γ`, composing `f` on the right with the identity on `β` gives a map that agrees with `f` pointwise: `VTask.comp f (OrderMonoidHom.id β) b = f b` for every `b : β`.

- Claim: Composition is associative in the sense that for `f : γ →*o δ`, `g : β →*o γ`, `h : α →*o β`, and any `a : α`, `VTask.comp (VTask.comp f g) h a = VTask.comp f (VTask.comp g h) a`.

- Claim: If `f` and `g` both send the identity element `1` to `1`, then `VTask.comp f g` also sends `1` to `1` (inherited from the monoid homomorphism property).

## Boundaries

- When either `f` or `g` is the identity `OrderMonoidHom`, the composite is extensionally equal to the other map.
- When either type is a trivial one-element monoid, the composite is forced to be the unique map to/from that type.
- The composite of two order-preserving maps is automatically order-preserving, so there is no restriction on how the order interacts with multiplication.
- The definition is well-formed for any `Preorder` (not merely a partial order or total order), so reflexivity is the only order requirement.

## Not to be confused with

- `MonoidHom.comp`: Composition of plain monoid homomorphisms, which does not carry or enforce any order-preservation requirement.
- `OrderHom.comp`: Composition of order-preserving maps between preordered sets, which carries no monoid structure.
- `Function.comp`: Bare function composition, which neither preserves monoid structure nor order structure and returns a plain function rather than a bundled homomorphism.
