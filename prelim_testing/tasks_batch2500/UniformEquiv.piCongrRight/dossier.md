## Object

`VTask.piCongrRight` constructs a uniform isomorphism between two dependent product spaces (pi types) `(i : ι) → β₁ i` and `(i : ι) → β₂ i`, given a family of uniform isomorphisms `F i : β₁ i ≃ᵤ β₂ i` between the fibers at each index `i`. Concretely, a function `f : (i : ι) → β₁ i` is sent to the function `i ↦ (F i) (f i)`, and uniform continuity is preserved in both directions because the uniform structure on a pi type is generated fiberwise. This is the uniform-space analogue of the purely set-theoretic "congr right" operation on pi types.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.piCongrRight : {ι : Type u_4} -> {β₁ : ι → Type u_5} -> {β₂ : ι → Type u_6} -> [(i : ι) → UniformSpace (β₁ i)] -> [(i : ι) → UniformSpace (β₂ i)] -> (F : (i : ι) → β₁ i ≃ᵤ β₂ i) -> ((i : ι) → β₁ i) ≃ᵤ ((i : ι) → β₂ i)
<!-- PINNED-SIGNATURE:END -->


`VTask.piCongrRight : {ι : Type u_4} -> {β₁ : ι → Type u_5} -> {β₂ : ι → Type u_6} -> [(i : ι) → UniformSpace (β₁ i)] -> [(i : ι) → UniformSpace (β₂ i)] -> (F : (i : ι) → β₁ i ≃ᵤ β₂ i) -> ((i : ι) → β₁ i) ≃ᵤ ((i : ι) → β₂ i)`

- `ι` is the index type parametrizing the family.
- `β₁` and `β₂` are the two families of types indexed by `ι`, whose fiber-wise types are being compared.
- The two instance arguments supply a uniform space structure on every fiber of `β₁` and `β₂` respectively, endowing both pi types with their product uniform structures.
- `F` is the family of uniform isomorphisms: for each index `i`, `F i` is a uniform isomorphism from `β₁ i` to `β₂ i`.
- The result is the induced uniform isomorphism between the two pi types, acting pointwise via `F`.

## Conventions

No special junk-value or edge conventions are declared: the definition is total and well-defined for any choice of `ι`, families `β₁`, `β₂`, and fiber isomorphisms `F`. When `ι` is the empty type the pi types are both singleton (unit-like), and `VTask.piCongrRight` is still well-typed, yielding the unique isomorphism between two singletons.

## Worked examples

- Claim: When every fiber isomorphism is the identity, `VTask.piCongrRight (fun i => UniformEquiv.refl (X i))` equals `UniformEquiv.refl (∀ i, X i)` — the overall isomorphism is itself the identity on the pi type.

- Claim: The inverse (symmetry) of `VTask.piCongrRight F` equals `VTask.piCongrRight (fun i => (F i).symm)` — taking the inverse of the whole isomorphism is the same as inverting each fiber isomorphism pointwise.

- Claim: For a family of uniform spaces `X i` and `Y i` indexed by a two-element type, if `f : (i : ι) → X i` is a function and `F i : X i ≃ᵤ Y i`, then `VTask.piCongrRight F` applied to `f` gives the function `i ↦ (F i) (f i)` — it acts pointwise on elements.

## Boundaries

- When `ι` is empty, the pi types `(i : ι) → β₁ i` and `(i : ι) → β₂ i` each contain exactly one element (the empty function). The isomorphism exists and is the unique map between two singletons.
- When `ι` is a singleton `{i₀}`, the isomorphism reduces to essentially `F i₀` on the single relevant fiber.
- The construction is entirely insensitive to whether `ι` is finite or infinite; the pi uniform structure and the pointwise action of `F` make sense in all cases.
- If all fiber isomorphisms `F i` are the identity (`UniformEquiv.refl`), the result is the identity isomorphism on the pi type (`UniformEquiv.refl (∀ i, X i)`).

## Not to be confused with

- `Equiv.piCongrRight`: the purely set-theoretic (no uniform structure) version that merely gives an equivalence of types, without the uniform continuity data carried by `VTask.piCongrRight`.
- `UniformEquiv.piCongrLeft`: a related construction that re-indexes the domain `ι` of the pi type via an equivalence on the index type, rather than changing the fiber types.
- `HomeomorphPiCongrRight` (the topological analogue): similar construction yielding a homeomorphism of pi spaces with respect to the product topology, rather than a uniform isomorphism with respect to the product uniform structure.