## VTask.piCongrRight

### Object

`VTask.piCongrRight` constructs a type equivalence (a bijection that is itself structured as a bundled pair of mutually inverse functions) between two dependent function types `(a : α) → β₁ a` and `(a : α) → β₂ a`, given that each fibre `β₁ a` and `β₂ a` is individually equivalent via a supplied family of equivalences. In other words, if you can convert each value type pointwise, you can convert entire dependent functions pointwise — the construction is simply function composition at each argument.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.piCongrRight : {α : Sort u_1} -> {β₁ : α → Sort u_9} -> {β₂ : α → Sort u_10} -> (F : (a : α) → β₁ a ≃ β₂ a) -> ((a : α) → β₁ a) ≃ ((a : α) → β₂ a)
<!-- PINNED-SIGNATURE:END -->


`VTask.piCongrRight : {α : Sort u_1} -> {β₁ : α → Sort u_9} -> {β₂ : α → Sort u_10} -> (F : (a : α) → β₁ a ≃ β₂ a) -> ((a : α) → β₁ a) ≃ ((a : α) → β₂ a)`

The implicit argument `α` is the index type over which both function spaces are parameterised. The implicit argument `β₁` is the first fibre family, assigning to each `a : α` a sort that serves as the codomain of the left-hand dependent function type. The implicit argument `β₂` is the second fibre family, analogously serving as the codomain of the right-hand dependent function type. The explicit argument `F` is a family of equivalences, one for each index `a : α`, providing the fibre-wise bijection between `β₁ a` and `β₂ a` that drives the construction.

### Conventions

There are no junk-value or special-input conventions for this definition: it is a total construction on all inputs in its domain, and every input is meaningful (there are no degenerate or vacuous edge cases that produce arbitrary or conventionally-chosen output).

### Worked examples

- Claim: When `F` is the family of identity equivalences (`fun a => Equiv.refl (β a)`), `VTask.piCongrRight F` equals the identity equivalence on `(a : α) → β a`.

- Claim: For `α := Fin 2`, `β₁ := fun _ => Bool`, `β₂ := fun _ => Bool`, and `F := fun _ => Equiv.refl Bool`, the forward function of `VTask.piCongrRight F` sends any `f : Fin 2 → Bool` to itself.

- Claim: Composing `VTask.piCongrRight F` with `VTask.piCongrRight G` (where `G : ∀ a, β₂ a ≃ β₃ a`) yields an equivalence whose forward map coincides with the forward map of `VTask.piCongrRight (fun a => (F a).trans (G a))`.

### Boundaries

- When `α` is the empty type, both dependent function types `(a : α) → β₁ a` and `(a : α) → β₂ a` are each inhabited by exactly one function (the empty function), and `VTask.piCongrRight F` is the trivial equivalence between two one-element types regardless of `F`.
- When `α` is `Unit` (or any single-element type), the construction reduces to a simple non-dependent equivalence between the unique fibre types `β₁ ⟨⟩` and `β₂ ⟨⟩`, and `F` only needs to supply one equivalence.
- When `F` is the family of reflexivity equivalences, the result is the identity equivalence on the function type (as captured by `piCongrRight_refl`).
- The construction works uniformly for any universe levels for `α`, `β₁`, and `β₂`, including propositional sorts (`Prop`), so it generalises beyond set-like types.

### Not to be confused with

- `Equiv.piCongrLeft`: lifts an equivalence on the *index* type `α` to an equivalence of dependent function types, rather than acting fibre-wise on the codomains.
- `Equiv.piCongr`: simultaneously applies both a reindexing of the domain and fibre-wise equivalences on the codomains, combining the roles of `piCongrLeft` and `VTask.piCongrRight`.
- `LinearEquiv.piCongrRight`: the linear-algebra analogue that upgrades the output from a bare type equivalence to a linear equivalence, requiring the fibre equivalences to be linear.