## Object

`VTask.ofEq` constructs a canonical affine equivalence (an invertible affine map) between two affine subspaces of the same ambient affine space, given a proof that those two subspaces are equal as sets-with-structure. It is the affine-geometry analogue of the canonical linear isomorphism between two definitionally or propositionally equal submodules.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofEq : {k : Type u_1} -> {V₁ : Type u_2} -> {P₁ : Type u_3} -> [Ring k] -> [AddCommGroup V₁] -> [Module k V₁] -> [AddTorsor V₁ P₁] -> (S₁ S₂ : AffineSubspace k P₁) -> [Nonempty ↥S₁] -> [Nonempty ↥S₂] -> (h : S₁ = S₂) -> ↥S₁ ≃ᵃ[k] ↥S₂
<!-- PINNED-SIGNATURE:END -->


`VTask.ofEq : {k : Type u_1} -> {V₁ : Type u_2} -> {P₁ : Type u_3} -> [Ring k] -> [AddCommGroup V₁] -> [Module k V₁] -> [AddTorsor V₁ P₁] -> (S₁ S₂ : AffineSubspace k P₁) -> [Nonempty ↥S₁] -> [Nonempty ↥S₂] -> (h : S₁ = S₂) -> ↥S₁ ≃ᵃ[k] ↥S₂`

- `k` is the scalar ring over which the affine geometry is defined.
- `V₁` is the direction vector space (the underlying `k`-module that acts on the affine space).
- `P₁` is the ambient affine space (a torsor for `V₁`).
- The `Ring`, `AddCommGroup`, `Module`, and `AddTorsor` instances supply the required algebraic structure on `k`, `V₁`, and `P₁`.
- `S₁` and `S₂` are the two affine subspaces of `P₁` being compared.
- The two `Nonempty` instances assert that `S₁` and `S₂` each contain at least one point (required so that their subtypes are non-empty, enabling the affine-equivalence structure).
- `h` is the proof of equality `S₁ = S₂`; it is the sole datum driving the construction.

## Conventions

There are no junk-value or boundary conventions to declare for this definition: the construction is total under its stated hypotheses, and the output is always the canonical "identity-like" affine equivalence induced by the equality proof.

## Worked examples

- Claim: When `h = rfl`, `VTask.ofEq S₁ S₁ rfl` equals the identity affine equivalence `AffineEquiv.refl k S₁`.

- Claim: For any `h : S₁ = S₂` and any point `x : S₁`, the image of `x` under `VTask.ofEq S₁ S₂ h`, when coerced back to the ambient space `P₁`, equals the coercion of `x` itself — that is, `VTask.ofEq` acts as the identity on underlying points.

- Claim: The inverse of `VTask.ofEq S₁ S₂ h` is `VTask.ofEq S₂ S₁ h.symm` — symmetry of the equality proof yields the inverse affine equivalence.

## Boundaries

- When `S₁ = S₂ = ⊥` (the empty affine subspace, if considered), the `Nonempty` hypothesis would not be satisfied; the definition is not applicable to empty subspaces.
- When `h = rfl` (reflexivity), the resulting equivalence is definitionally the identity (`AffineEquiv.refl`), confirming there is no spurious data introduced.
- The definition is entirely proof-irrelevant with respect to `h`: any two proofs of `S₁ = S₂` yield the same affine equivalence, because equality of affine subspaces is a proposition.

## Not to be confused with

- `LinearEquiv.ofEq`: the purely linear (module) version of this construction, acting on submodules rather than affine subspaces.
- `AffineEquiv.refl`: the identity affine equivalence on a single fixed affine subspace, a special case of `VTask.ofEq` when `h = rfl`.
- `AffineSubspace.equivOfEq` (if it existed as a set-level equivalence): `VTask.ofEq` is specifically an *affine* equivalence, respecting the full affine structure, not merely a bijection of underlying sets.