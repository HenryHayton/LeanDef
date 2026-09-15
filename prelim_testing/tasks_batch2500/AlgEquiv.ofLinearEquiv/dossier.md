## Object

An algebra equivalence between two `R`-algebras `A₁` and `A₂`, produced by promoting a linear equivalence (a bijective `R`-linear map) to a full algebra isomorphism once one supplies proofs that it also preserves multiplication and the multiplicative identity. Concretely, an algebra equivalence is an invertible map that is simultaneously a ring isomorphism and an `R`-module isomorphism, and is compatible with the `R`-algebra structure on both sides.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofLinearEquiv : {R : Type uR} -> {A₁ : Type uA₁} -> {A₂ : Type uA₂} -> [CommSemiring R] -> [Semiring A₁] -> [Semiring A₂] -> [Algebra R A₁] -> [Algebra R A₂] -> (l : A₁ ≃ₗ[R] A₂) -> (map_one : l 1 = 1) -> (map_mul : ∀ (x y : A₁), l (x * y) = l x * l y) -> A₁ ≃ₐ[R] A₂
<!-- PINNED-SIGNATURE:END -->


VTask.ofLinearEquiv : {R : Type uR} -> {A₁ : Type uA₁} -> {A₂ : Type uA₂} -> [CommSemiring R] -> [Semiring A₁] -> [Semiring A₂] -> [Algebra R A₁] -> [Algebra R A₂] -> (l : A₁ ≃ₗ[R] A₂) -> (map_one : l 1 = 1) -> (map_mul : ∀ (x y : A₁), l (x * y) = l x * l y) -> A₁ ≃ₐ[R] A₂

`R` is the commutative semiring of scalars shared by both algebras. `A₁` is the source `R`-algebra and `A₂` is the target `R`-algebra. The argument `l` is the underlying `R`-linear equivalence (a bijective `R`-module map from `A₁` to `A₂`) that one wishes to upgrade. The argument `map_one` is a proof that `l` sends the multiplicative identity of `A₁` to the multiplicative identity of `A₂`. The argument `map_mul` is a proof that `l` distributes over multiplication, i.e., that it is a ring homomorphism with respect to the multiplicative structure.

## Conventions

No junk-value or out-of-domain conventions apply: the construction is total over all valid inputs and every field of the resulting algebra equivalence is determined directly by the supplied data. NONE_DECLARED: this is a total constructor with no edge cases requiring a junk-value convention.

## Worked examples

- Claim: Applying `VTask.ofLinearEquiv` to the identity linear equivalence `LinearEquiv.refl R A` with proofs that it maps `1` to `1` and respects multiplication yields an algebra equivalence whose underlying forward function is the identity on `A`.

- Claim: If `φ : A₁ ≃ₐ[R] A₂` is any algebra equivalence, then applying `VTask.ofLinearEquiv` to its underlying linear equivalence `φ.toLinearEquiv`, together with the proofs `φ.map_one` and `φ.map_mul`, recovers an algebra equivalence that agrees with `φ` on all elements of `A₁`.

- Claim: The algebra equivalence produced by `VTask.ofLinearEquiv l h₁ h_mul` has its inverse given by `l.symm`, equipped with the corresponding inverse properties inherited from the linear equivalence structure of `l`.

## Boundaries

- The construction requires `map_one` and `map_mul` as explicit proof arguments; if either condition fails for a given linear equivalence, no algebra equivalence can be constructed by this route.
- The `commutes'` field — which asserts compatibility with scalar multiplication by `R` via the algebra maps — is derived automatically from the linear equivalence `l` itself (linearity over `R` and `map_one` together imply this), so the caller need not supply it.
- The function is well-defined for all semiring-based algebras (not just rings or fields); the base `R` need only be a commutative semiring and `A₁`, `A₂` need only be semirings with an `R`-algebra structure.
- The resulting equivalence's carrier function is definitionally equal to `l` as a bare function, so rewriting with it in proofs that need the linear map or the algebra map is straightforward.

## Not to be confused with

- `AlgHom.ofLinearMap` — this constructs a one-directional algebra *homomorphism* from a linear map plus the same two side conditions; it does not produce an invertible equivalence.
- `AlgEquiv.ofRingEquiv` — promotes a *ring* equivalence (rather than a linear equivalence) to an algebra equivalence, requiring a different compatibility hypothesis.
- `LinearEquiv.toAlgEquiv` — a variant that may require the linear equivalence to already carry more structure, rather than accepting separate `map_one` and `map_mul` proofs.