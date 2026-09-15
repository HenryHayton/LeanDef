## Object

`VTask.psigmaCongrRight` is an equivalence (a bijection with explicit inverse) between two dependent pair types `(a : α) ×' β₁ a` and `(a : α) ×' β₂ a` (propositional sigma types, written `Σ' a, β₁ a` and `Σ' a, β₂ a` in Mathlib notation). Given that each fibre `β₁ a` is equivalent to the corresponding fibre `β₂ a`, this construction lifts that fibrewise equivalence to an equivalence of the total spaces, leaving the base component `a` unchanged and applying the appropriate fibre equivalence to the second component.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.psigmaCongrRight : {α : Sort u} -> {β₁ : α → Sort u_1} -> {β₂ : α → Sort u_2} -> (F : (a : α) → β₁ a ≃ β₂ a) -> (a : α) ×' β₁ a ≃ (a : α) ×' β₂ a
<!-- PINNED-SIGNATURE:END -->


`VTask.psigmaCongrRight : {α : Sort u} -> {β₁ : α → Sort u_1} -> {β₂ : α → Sort u_2} -> (F : (a : α) → β₁ a ≃ β₂ a) -> (a : α) ×' β₁ a ≃ (a : α) ×' β₂ a`

The implicit argument `α` is the index type (the base of the dependent pair). The implicit arguments `β₁` and `β₂` are the two families of fibres over `α`, ranging over any sorts. The explicit argument `F` is a family of equivalences, one for each base element `a : α`, witnessing that the fibre `β₁ a` is equivalent to `β₂ a`.

## Conventions

No special junk-value or edge conventions are declared: the construction is total and well-behaved for all inputs, including the degenerate case where `α` is empty (in which case both sigma types are empty and the equivalence is trivially the identity on the empty type).

## Worked examples

- Claim: When `F` is the family of identity equivalences `fun a => Equiv.refl (β a)`, `VTask.psigmaCongrRight F` equals the identity equivalence on `Σ' a, β a`.

- Claim: The inverse of `VTask.psigmaCongrRight F` equals `VTask.psigmaCongrRight (fun a => (F a).symm)`, i.e., inverting fibrewise and then lifting commutes with inverting the total equivalence.

- Claim: For `α = Bool`, `β₁ = fun _ => Nat`, `β₂ = fun _ => Nat`, and `F = fun _ => Equiv.refl Nat`, the forward map of `VTask.psigmaCongrRight F` sends `⟨true, 3⟩` to `⟨true, 3⟩`.

- Claim: Composing `VTask.psigmaCongrRight F` with `VTask.psigmaCongrRight G` (via `.trans`) equals `VTask.psigmaCongrRight (fun a => (F a).trans (G a))`.

## Boundaries

- **Empty base**: When `α` is an empty type (e.g., `Empty` or `False`), both `Σ' a, β₁ a` and `Σ' a, β₂ a` are empty, and the equivalence is vacuously the unique equivalence between two empty types. The argument `F` is a function out of an empty type and does not need to produce any values.
- **Singleton fibre**: When every `β₁ a` and `β₂ a` is a `Prop` (or a subsingleton), the equivalence is again trivially well-defined, and the fibre equivalences `F a` are automatically unique.
- **Refl case**: Supplying `fun a => Equiv.refl (β a)` as the family recovers exactly the identity equivalence on `Σ' a, β a`.
- **Base component preserved**: In all cases the equivalence does not alter the first component of any pair; it only transforms the second component via the appropriate `F a`.

## Not to be confused with

- `Equiv.sigmaCongrRight`: The analogous construction for the *bundled* sigma type `Σ a, β a` (where the fibre is a `Type` rather than a `Sort`); `psigmaCongrRight` works for `Σ'` (propositional sigma / `PSigma`), which allows fibres in any `Sort`.
- `Equiv.psigmaCongrLeft`: Lifts an equivalence on the *base* `α` to an equivalence of the total space, rather than lifting fibrewise equivalences on the fibres.
- `Equiv.psigmaCongr`: The combination of both a base equivalence and fibrewise equivalences, of which `psigmaCongrRight` is the special case where the base equivalence is the identity.