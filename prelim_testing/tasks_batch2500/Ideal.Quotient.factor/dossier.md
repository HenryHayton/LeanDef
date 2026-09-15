## Object

Given a ring `R` and two two-sided ideals `S ⊆ T` of `R`, `VTask.factor H` is the canonical ring homomorphism from the quotient ring `R ⧸ S` to the quotient ring `R ⧸ T`. It sends the coset `r + S` to the coset `r + T`. This is well-defined precisely because `S ≤ T`: any two representatives that agree mod `S` also agree mod `T`. The map is always surjective (every coset of `T` is the image of the corresponding coset of `S`) and its kernel is the image of `T` under the quotient map `R → R ⧸ S`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.factor : {R : Type u} -> [Ring R] -> {S T : Ideal R} -> [S.IsTwoSided] -> [T.IsTwoSided] -> (H : S ≤ T) -> R ⧸ S →+* R ⧸ T
<!-- PINNED-SIGNATURE:END -->


VTask.factor : {R : Type u} -> [Ring R] -> {S T : Ideal R} -> [S.IsTwoSided] -> [T.IsTwoSided] -> (H : S ≤ T) -> R ⧸ S →+* R ⧸ T

`R` is the ambient ring. The instance `[Ring R]` equips it with ring structure. `S` is the smaller ideal (the one being quotiented out in the domain) and `T` is the larger ideal (quotiented out in the codomain); both must be two-sided, as required for forming quotient rings. `H` is the inclusion proof `S ≤ T`, which is the essential datum licensing the construction.

## Conventions

When `H` is `le_refl S` (i.e., `S = T`), `VTask.factor H` equals the identity ring homomorphism on `R ⧸ S`. There are no junk-value conventions in the traditional sense, as the definition is total over its stated domain.

## Worked examples

- Claim: For any ring `R` and two-sided ideal `S`, `VTask.factor (le_refl S)` is the identity map on `R ⧸ S`.

- Claim: If `S ≤ T ≤ U` are three two-sided ideals of `R`, then composing `VTask.factor (H₁ : S ≤ T)` with `VTask.factor (H₂ : T ≤ U)` yields `VTask.factor (H₁.trans H₂ : S ≤ U)`.

- Claim: For ideals `I ⊓ J ≤ I`, the component map from `R ⧸ (I ⊓ J)` to `R ⧸ I` obtained by projecting a CRT-style isomorphism equals `VTask.factor inf_le_left`.

- Claim: The kernel of `VTask.factor H` (where `H : S ≤ T`) is the image of `T` under the quotient map `Ideal.Quotient.mk S : R →+* R ⧸ S`.

## Boundaries

- When `S = T` (witnessed by `le_refl`), the map is an isomorphism; it equals the identity ring homomorphism.
- When `S` is the zero ideal and `T = R` (the whole ring), the map is the zero ring homomorphism from `R ⧸ S ≅ R` to the zero ring `R ⧸ R`.
- The map is always surjective regardless of how much larger `T` is than `S`.
- The kernel is always the image of `T` in `R ⧸ S`, so by the first isomorphism theorem `(R ⧸ S) ⧸ (T / S) ≅ R ⧸ T`.
- The construction composes transitively: chaining two factor maps along `S ≤ T ≤ U` gives the factor map along `S ≤ U`.

## Not to be confused with

- `Ideal.Quotient.factorPow`: the specialised version for ideals of the form `I^m` and `I^n` with `n ≤ m`; use that when working with power-of-ideal filtrations.
- `Ideal.quotEquivOfEq`: a ring *isomorphism* constructed when the two ideals are *equal*, not merely comparable; `VTask.factor` for equal ideals recovers this map but does not produce an `RingEquiv`.
- `Submodule.factor`: an analogous construction for submodules (as `ℤ`-modules), which agrees with `VTask.factor` on the underlying additive group maps but lives in the `Submodule` rather than `Ideal` API.