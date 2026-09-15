## Object

`VTask.sigmaCongrRight` constructs a type equivalence (a bijection with explicit inverse) between two dependent sum types (sigma types) `(a : α) × β₁ a` and `(a : α) × β₂ a` that share the same base type `α`, given a pointwise family of equivalences between their respective fibers.

Intuitively: if for every element `a : α` you can biject `β₁ a` with `β₂ a`, then you can biject the total spaces `Σ a, β₁ a` and `Σ a, β₂ a` by leaving the base component untouched and applying the appropriate fiber equivalence to the second component.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sigmaCongrRight : {α : Type u_3} -> {β₁ : α → Type u_1} -> {β₂ : α → Type u_2} -> (F : (a : α) → β₁ a ≃ β₂ a) -> (a : α) × β₁ a ≃ (a : α) × β₂ a
<!-- PINNED-SIGNATURE:END -->


VTask.sigmaCongrRight : {α : Type u_3} -> {β₁ : α → Type u_1} -> {β₂ : α → Type u_2} -> (F : (a : α) → β₁ a ≃ β₂ a) -> (a : α) × β₁ a ≃ (a : α) × β₂ a

- `α` is the shared base type whose elements index the fibers.
- `β₁` is the first family of fiber types, depending on `α`.
- `β₂` is the second family of fiber types, depending on `α`.
- `F` is the family of equivalences, one for each `a : α`, witnessing that the fiber `β₁ a` is in bijection with `β₂ a`.

The result is the induced equivalence between the two total sigma types.

## Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a fully total constructor of a bundled equivalence, valid for any type `α` and any fiber families `β₁`, `β₂` equipped with a pointwise equivalence family.

## Worked examples

- Claim: Applying `VTask.sigmaCongrRight` to the identity family of equivalences (each fiber mapped by `Equiv.refl`) yields the identity equivalence on the sigma type.

- Claim: For `α = Bool`, `β₁ = fun _ => Fin 2`, `β₂ = fun _ => ZMod 2`, and `F` the known equivalence `Fin 2 ≃ ZMod 2`, the forward map of `VTask.sigmaCongrRight F` sends `⟨b, v⟩` to `⟨b, F b v⟩`, preserving the base component `b`.

- Claim: The inverse (symmetry) of `VTask.sigmaCongrRight F` equals `VTask.sigmaCongrRight (fun a => (F a).symm)`, i.e., the inverse is obtained by inverting each fiber equivalence pointwise.

- Claim: Composing `VTask.sigmaCongrRight F` with `VTask.sigmaCongrRight G` (via `Equiv.trans`) gives the same result as `VTask.sigmaCongrRight (fun a => (F a).trans (G a))`, i.e., composition is pointwise.

## Boundaries

- When `α` is an empty type, the sigma types `Σ a, β₁ a` and `Σ a, β₂ a` are both empty, and the resulting equivalence is the unique bijection between two empty types. The family `F` is vacuously supplied and no fiber equivalences are ever applied.
- When `α` is a singleton type (e.g., `Unit`), the construction reduces to a single fiber equivalence: `Σ a, β₁ a ≃ β₁ ()` and `Σ a, β₂ a ≃ β₂ ()`, so `VTask.sigmaCongrRight F` essentially wraps `F ()`.
- When each `F a` is already `Equiv.refl (β a)` — the identity — the result is definitionally the identity equivalence on the sigma type (`sigmaCongrRight_refl`).
- The construction is strictly fiber-preserving: the first (base) component of every sigma pair is left unchanged by both the forward and inverse maps.

## Not to be confused with

- `Equiv.sigmaCongrLeft`: changes the base type `α` of the sigma type rather than the fiber types, using an equivalence of base types.
- `Equiv.sigmaCongr`: simultaneously changes both the base and the fibers; `VTask.sigmaCongrRight` is the special case where the base is held fixed.
- `Equiv.psigmaCongrRight`: the analogous construction for `PSigma` (which allows the fiber to live in any `Sort`), rather than `Sigma` (which requires `Type`).
