## Object

Given two monoid-with-zero homomorphisms — one from `α` to `β` and one from `β` to `γ` — `VTask.comp` produces their composite, which is itself a monoid-with-zero homomorphism from `α` to `γ`. It is the standard composition of structure-preserving maps in the category of monoids-with-zero.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {α : Type u_2} -> {β : Type u_3} -> {γ : Type u_4} -> [MulZeroOneClass α] -> [MulZeroOneClass β] -> [MulZeroOneClass γ] -> (hnp : β →*₀ γ) -> (hmn : α →*₀ β) -> α →*₀ γ
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_2} -> {β : Type u_3} -> {γ : Type u_4} -> [MulZeroOneClass α] -> [MulZeroOneClass β] -> [MulZeroOneClass γ] -> (hnp : β →*₀ γ) -> (hmn : α →*₀ β) -> α →*₀ γ`

The three type arguments `α`, `β`, `γ` are the source, intermediate, and target types, inferred implicitly. The three typeclass arguments supply the monoid-with-zero structure on each type, also inferred automatically. The explicit argument `hnp` is the outer homomorphism from `β` to `γ` (applied second). The explicit argument `hmn` is the inner homomorphism from `α` to `β` (applied first). The result is the composite homomorphism from `α` to `γ`.

## Conventions

No junk-value or edge conventions are declared: the definition is total and well-behaved on all inputs without any degenerate cases requiring special treatment.

## Worked examples

- Claim: Applying `VTask.comp hnp hmn` at a point `a : α` gives the same value as first applying `hmn` then `hnp`, i.e., `VTask.comp hnp hmn a = hnp (hmn a)` for any concrete morphisms and element.

- Claim: For monoid-with-zero homomorphisms `f : ℤ →*₀ ℤ` and `g : ℤ →*₀ ℤ`, the underlying function of `VTask.comp f g` equals the function composition `⇑f ∘ ⇑g`.

- Claim: For any monoid-with-zero homomorphism `f : α →*₀ β`, composing with the identity homomorphism on the left or right recovers `f`; specifically `VTask.comp (MonoidWithZeroHom.id β) f` and `VTask.comp f (MonoidWithZeroHom.id α)` both act the same as `f`.

- Claim: Composition is associative: for homomorphisms `f : α →*₀ β`, `g : β →*₀ γ`, `h : γ →*₀ δ`, the composites `VTask.comp h (VTask.comp g f)` and `VTask.comp (VTask.comp h g) f` agree as functions on every element of `α`.

## Boundaries

- If either argument is the zero homomorphism (sending everything to zero), the composite is also the zero homomorphism, since both `map_zero` and the constant-zero property are preserved.
- If both arguments are identity homomorphisms, the composite is the identity.
- The types `α`, `β`, `γ` may all coincide, in which case composition of endomorphisms is an endomorphism on the same type.
- There is no restriction on the types; in particular trivial or one-element monoids-with-zero are handled without special cases.

## Not to be confused with

- `MonoidHom.comp`: composition of plain monoid homomorphisms (`α →* β`), which does not track the zero-preservation property.
- `RingHom.comp`: composition of ring homomorphisms; requires more structure (additive group, distributivity) than a monoid-with-zero.
- Plain function composition `Function.comp` (written `∘`): produces a bare function, not a bundled homomorphism carrying proof obligations.