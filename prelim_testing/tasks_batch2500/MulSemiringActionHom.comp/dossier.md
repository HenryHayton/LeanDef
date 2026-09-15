## Object

`VTask.comp` is the composition of two equivariant additive ring homomorphisms. Given rings `R`, `S`, `T` acted upon by monoids `M`, `N`, `P` respectively, a map `f : R →ₑ+*[φ] S` that is a ring homomorphism equivariant with respect to the monoid homomorphism `φ : M →* N`, and a map `g : S →ₑ+*[ψ] T` that is a ring homomorphism equivariant with respect to `ψ : N →* P`, their composition is the ring homomorphism `R → T` that is equivariant with respect to the composite monoid homomorphism `χ : M →* P` (where `χ = ψ ∘ φ` in the sense witnessed by the `CompTriple` instance).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {M : Type u_1} -> [Monoid M] -> {N : Type u_2} -> [Monoid N] -> {P : Type u_3} -> [Monoid P] -> {φ : M →* N} -> {ψ : N →* P} -> {χ : M →* P} -> {R : Type u_10} -> [Semiring R] -> [MulSemiringAction M R] -> {S : Type u_12} -> [Semiring S] -> [MulSemiringAction N S] -> {T : Type u_14} -> [Semiring T] -> [MulSemiringAction P T] -> (g : S →ₑ+*[ψ] T) -> (f : R →ₑ+*[φ] S) -> [κ : φ.CompTriple ψ χ] -> R →ₑ+*[χ] T
<!-- PINNED-SIGNATURE:END -->


VTask.comp : {M : Type u_1} -> [Monoid M] -> {N : Type u_2} -> [Monoid N] -> {P : Type u_3} -> [Monoid P] -> {φ : M →* N} -> {ψ : N →* P} -> {χ : M →* P} -> {R : Type u_10} -> [Semiring R] -> [MulSemiringAction M R] -> {S : Type u_12} -> [Semiring S] -> [MulSemiringAction N S] -> {T : Type u_14} -> [Semiring T] -> [MulSemiringAction P T] -> (g : S →ₑ+*[ψ] T) -> (f : R →ₑ+*[φ] S) -> [κ : φ.CompTriple ψ χ] -> R →ₑ+*[χ] T

`M`, `N`, `P` are the acting monoids; `φ : M →* N` and `ψ : N →* P` are the monoid homomorphisms governing equivariance of `f` and `g` respectively; `χ : M →* P` is the composite monoid homomorphism (implicitly determined by the `CompTriple` instance `κ`). `R`, `S`, `T` are the semirings being acted upon by `M`, `N`, `P` respectively. The argument `g` is the outer equivariant ring homomorphism from `S` to `T`, and `f` is the inner equivariant ring homomorphism from `R` to `S`. The instance `κ` witnesses that `χ` is the composite of `φ` and `ψ`.

## Conventions

No junk-value or edge conventions are declared for this definition: the operation is a total constructor on well-typed inputs and the `CompTriple` instance is inferred automatically in the vast majority of cases; there is no distinguished behavior at any boundary that requires documentation.

## Worked examples

- Claim: For the identity equivariant ring homomorphism `id` (with all monoids and rings trivial), composing `id` with itself yields a map that acts as the identity on every element.

- Claim: If `f : R →ₑ+*[φ] S` and `g : S →ₑ+*[ψ] T`, then for any `r : R`, applying `VTask.comp g f` to `r` equals `g (f r)` as elements of `T`.

- Claim: If `f : R →ₑ+*[φ] S`, `g : S →ₑ+*[ψ] T`, `h : T →ₑ+*[ρ] U`, then `VTask.comp h (VTask.comp g f)` and `VTask.comp (VTask.comp h g) f` agree pointwise on all elements of `R` (associativity of composition).

- Claim: The result of `VTask.comp g f` preserves addition: for all `r₁ r₂ : R`, `VTask.comp g f (r₁ + r₂) = VTask.comp g f r₁ + VTask.comp g f r₂`.

- Claim: The result of `VTask.comp g f` preserves multiplication: for all `r₁ r₂ : R`, `VTask.comp g f (r₁ * r₂) = VTask.comp g f r₁ * VTask.comp g f r₂`.

## Boundaries

- When `φ`, `ψ`, or `χ` are identity monoid homomorphisms, composition reduces to ordinary (non-twisted) equivariant ring homomorphism composition.
- When `R = S = T` and `f` and `g` are both the identity equivariant ring homomorphism, the composite is again the identity.
- The `CompTriple` instance `κ` is typically synthesized automatically by typeclass inference; if no such instance exists (i.e., `χ` is not definitionally the composite of `φ` and `ψ`), the composition cannot be formed.
- The definition is total on all well-typed inputs satisfying the typeclass constraints.

## Not to be confused with

- `RingHom.comp`: composition of plain (non-equivariant) ring homomorphisms, which carries no monoid-action equivariance data.
- `DistribMulActionHom.comp`: composition of equivariant additive group homomorphisms respecting a distributive mul-action, which does not require multiplicativity (ring homomorphism property).
- `MonoidHom.comp`: composition of monoid homomorphisms between the acting monoids `M`, `N`, `P`, which operates on the symmetry side rather than the ring side.