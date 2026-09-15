## Object

The sequential composition of two non-unital ring homomorphisms. Given a homomorphism `f` from `α` to `β` and a homomorphism `g` from `β` to `γ`, `VTask.comp g f` is the non-unital ring homomorphism from `α` to `γ` that first applies `f` and then applies `g`. It preserves both addition and multiplication, as required of a non-unital ring homomorphism.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {α : Type u_2} -> {β : Type u_3} -> {γ : Type u_4} -> [NonUnitalNonAssocSemiring α] -> [NonUnitalNonAssocSemiring β] -> [NonUnitalNonAssocSemiring γ] -> (g : β →ₙ+* γ) -> (f : α →ₙ+* β) -> α →ₙ+* γ
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_2} -> {β : Type u_3} -> {γ : Type u_4} -> [NonUnitalNonAssocSemiring α] -> [NonUnitalNonAssocSemiring β] -> [NonUnitalNonAssocSemiring γ] -> (g : β →ₙ+* γ) -> (f : α →ₙ+* β) -> α →ₙ+* γ`

The type parameters `α`, `β`, and `γ` are the source, intermediate, and target types, each equipped with a `NonUnitalNonAssocSemiring` structure (addition and multiplication that are associative and distributive, but without a required multiplicative identity). The argument `g` is the non-unital ring homomorphism from `β` to `γ` applied second; the argument `f` is the non-unital ring homomorphism from `α` to `β` applied first. The result is a non-unital ring homomorphism from `α` to `γ`.

## Conventions

The argument order follows the standard mathematical convention for composition: `VTask.comp g f` means "g after f", i.e., the function that sends `x` to `g(f(x))`. This matches the usual notation `g ∘ f` for function composition.

## Worked examples

- Claim: For non-unital ring homomorphisms `f : α →ₙ+* β` and `g : β →ₙ+* γ`, applying `VTask.comp g f` to an element `x : α` yields the same result as applying `g` to `f x`.

- Claim: For non-unital ring homomorphisms `f : α →ₙ+* β`, `g : β →ₙ+* γ`, and `h : γ →ₙ+* δ`, the compositions `VTask.comp h (VTask.comp g f)` and `VTask.comp (VTask.comp h g) f` agree as functions (associativity of composition).

- Claim: For any non-unital ring homomorphism `f : α →ₙ+* β` and elements `x y : α`, `(VTask.comp g f) (x + y) = (VTask.comp g f) x + (VTask.comp g f) y`, since compositions of ring homomorphisms are again ring homomorphisms that preserve addition.

## Boundaries

- The definition is total: it works for any two non-unital ring homomorphisms whose types are composable, with no restrictions beyond the type-level compatibility.
- When `f` or `g` is an identity-like map, the composition reduces to the other map behaviorally.
- The result type `α →ₙ+* γ` carries bundled proofs that addition and multiplication are preserved; these proofs are derived automatically from the corresponding proofs on `f` and `g`.
- No multiplicative identity is assumed or required; this is strictly more general than composing unital ring homomorphisms.

## Not to be confused with

- `MulHom.comp`: Composition of bare multiplicative homomorphisms, which does not track additive structure.
- `AddMonoidHom.comp`: Composition of additive monoid homomorphisms, which does not track multiplicative structure.
- `RingHom.comp`: Composition of unital ring homomorphisms, which additionally requires and preserves a multiplicative identity `1`.