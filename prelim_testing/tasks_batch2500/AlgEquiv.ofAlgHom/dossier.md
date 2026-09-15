## Object

`VTask.ofAlgHom` constructs an algebra isomorphism (an `R`-algebra equivalence `A₁ ≃ₐ[R] A₂`) from a pair of `R`-algebra homomorphisms that are mutual inverses. In classical terms: if `f : A₁ → A₂` and `g : A₂ → A₁` are `R`-algebra maps satisfying `f ∘ g = id` and `g ∘ f = id`, then `f` is in fact an algebra isomorphism, and this definition packages that isomorphism as a single bundled object.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofAlgHom : {R : Type uR} -> {A₁ : Type uA₁} -> {A₂ : Type uA₂} -> [CommSemiring R] -> [Semiring A₁] -> [Semiring A₂] -> [Algebra R A₁] -> [Algebra R A₂] -> (f : A₁ →ₐ[R] A₂) -> (g : A₂ →ₐ[R] A₁) -> (h₁ : f.comp g = AlgHom.id R A₂) -> (h₂ : g.comp f = AlgHom.id R A₁) -> A₁ ≃ₐ[R] A₂
<!-- PINNED-SIGNATURE:END -->


`VTask.ofAlgHom : {R : Type uR} -> {A₁ : Type uA₁} -> {A₂ : Type uA₂} -> [CommSemiring R] -> [Semiring A₁] -> [Semiring A₂] -> [Algebra R A₁] -> [Algebra R A₂] -> (f : A₁ →ₐ[R] A₂) -> (g : A₂ →ₐ[R] A₁) -> (h₁ : f.comp g = AlgHom.id R A₂) -> (h₂ : g.comp f = AlgHom.id R A₁) -> A₁ ≃ₐ[R] A₂`

The implicit type arguments `R`, `A₁`, and `A₂` are, respectively, the commutative semiring of scalars and the two `R`-algebras being identified. The instance arguments supply the semiring and algebra structures. The argument `f` is the forward algebra homomorphism from `A₁` to `A₂`. The argument `g` is the proposed inverse algebra homomorphism from `A₂` back to `A₁`. The proof `h₁` witnesses that `f` followed by `g` equals the identity on `A₂` (i.e., `f` is a right inverse of `g`). The proof `h₂` witnesses that `g` followed by `f` equals the identity on `A₁` (i.e., `f` is a left inverse of `g`). Together `h₁` and `h₂` confirm that `f` and `g` are mutual inverses.

## Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a total constructor whose output is fully determined whenever the four arguments `f`, `g`, `h₁`, `h₂` are supplied, and there are no degenerate inputs requiring special treatment.

## Worked examples

- Claim: The underlying algebra homomorphism of `VTask.ofAlgHom f g h₁ h₂` (viewed as an `AlgHom`) equals `f`.

- Claim: The symmetry of `VTask.ofAlgHom f g h₁ h₂` equals `VTask.ofAlgHom g f h₂ h₁`; that is, swapping `f` and `g` and swapping the two proofs gives the inverse isomorphism.

- Claim: The `toLinearMap` of `VTask.ofAlgHom f g h₁ h₂` equals the `toLinearMap` of `f`; the linear-map content of the equivalence is exactly `f`.

- Claim: If `e : A₁ ≃ₐ[R] A₂` is an existing algebra equivalence and `g` is a left/right inverse to `↑e` (its coercion to an `AlgHom`), then `VTask.ofAlgHom (↑e) g h₁ h₂ = e`.

## Boundaries

- The function is total: it requires no injectivity or surjectivity hypothesis beyond the two inverse-composition equalities `h₁` and `h₂`, because those already imply bijectivity.
- If `A₁ = A₂` and both `f` and `g` are chosen to be `AlgHom.id R A₁`, then both `h₁` and `h₂` are trivially `rfl`, and `VTask.ofAlgHom` returns the identity equivalence.
- The definition works for semirings (it does not require ring or field structure), so it applies in the broad generality of `CommSemiring R` and `Semiring A₁`, `Semiring A₂`.
- The hypotheses `h₁` and `h₂` must both be supplied; providing only one would not suffice (a one-sided inverse for algebra maps between, say, non-finitely-generated algebras need not be a two-sided inverse in general).

## Not to be confused with

- `AlgEquiv.symm`: reverses an *already-constructed* algebra equivalence; `VTask.ofAlgHom` instead *constructs* an equivalence from raw morphism data.
- `AlgEquiv.ofBijective`: constructs an algebra isomorphism from a single algebra homomorphism that is proven bijective, without needing an explicit inverse map.
- `AlgHom.comp`: merely composes two algebra homomorphisms without upgrading them to an equivalence.