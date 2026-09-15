## Object

`VTask.sumLexCongr` constructs an order isomorphism between two lexicographic sum types. Given order isomorphisms between corresponding component types, it assembles them into a single order isomorphism between the two lexicographic sums, respecting the lex ordering throughout.

The *lexicographic sum* (written `α ⊕ₗ β`) is the disjoint union of two ordered types where all elements from `α` are considered smaller than all elements from `β`, and elements within each summand are compared by their own order.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sumLexCongr : {α₁ : Type u_4} -> {α₂ : Type u_5} -> {β₁ : Type u_6} -> {β₂ : Type u_7} -> [LE α₁] -> [LE α₂] -> [LE β₁] -> [LE β₂] -> (ea : α₁ ≃o α₂) -> (eb : β₁ ≃o β₂) -> α₁ ⊕ₗ β₁ ≃o α₂ ⊕ₗ β₂
<!-- PINNED-SIGNATURE:END -->


`VTask.sumLexCongr : {α₁ : Type u_4} -> {α₂ : Type u_5} -> {β₁ : Type u_6} -> {β₂ : Type u_7} -> [LE α₁] -> [LE α₂] -> [LE β₁] -> [LE β₂] -> (ea : α₁ ≃o α₂) -> (eb : β₁ ≃o β₂) -> α₁ ⊕ₗ β₁ ≃o α₂ ⊕ₗ β₂`

The four implicit type arguments are the four types being related; the four `LE` instances supply the orderings on each type. The argument `ea` is an order isomorphism between the two "left" component types, and `eb` is an order isomorphism between the two "right" component types.

## Conventions

No special junk-value or edge-case conventions are declared: the construction is total and well-defined for any pair of order isomorphisms on types equipped with a `≤` relation.

## Worked examples

- Claim: Applying `VTask.sumLexCongr` with both components being the identity isomorphism yields the identity isomorphism on the lexicographic sum.

- Claim: For order isomorphisms `ea : α₁ ≃o α₂` and `eb : β₁ ≃o β₂`, the inverse of `VTask.sumLexCongr ea eb` equals `VTask.sumLexCongr ea.symm eb.symm`.

- Claim: Composing `VTask.sumLexCongr e₁ e₂` with `VTask.sumLexCongr f₁ f₂` (via `trans`) equals `VTask.sumLexCongr (e₁.trans f₁) (e₂.trans f₂)`, so the construction is functorial in both arguments.

## Boundaries

- When both `ea` and `eb` are identity isomorphisms (`OrderIso.refl`), the result is the identity isomorphism on `α ⊕ₗ β`.
- The construction handles the cross-summand case correctly: a `Sum.inl` element is always mapped to a `Sum.inl` element (via `ea`) and a `Sum.inr` element is always mapped to a `Sum.inr` element (via `eb`), so the lex boundary between the left and right components is preserved.
- Elements that compare across the lex boundary (an `inl` vs. an `inr`) retain their relative order under the isomorphism, since both original and image types use the same lex convention.

## Not to be confused with

- `Equiv.sumCongr`: the underlying plain equivalence (bijection) between sum types, with no order structure preserved.
- A product-order isomorphism on `α × β`: that operates on products with the product order, not disjoint unions with the lex order.
- `VTask.sumLexCongr ea eb` composed in the wrong order: functoriality requires `(e₁.sumLexCongr e₂).trans (f₁.sumLexCongr f₂) = (e₁.trans f₁).sumLexCongr (e₂.trans f₂)`, so component isomorphisms must be composed before or after lifting, not mixed.