## Object

Given two composable equivariant non-unital semiring homomorphisms — one from `A` to `B` over a monoid homomorphism `φ : R →* S`, and one from `B` to `C` over a monoid homomorphism `ψ : S →* T` — `VTask.comp f g` is their composite, a single equivariant non-unital semiring homomorphism from `A` to `C` over the composed scalar-action monoid homomorphism `χ : R →* T`. In other words, it packages the usual set-theoretic composition of the two maps into a morphism in the appropriate category of equivariant non-unital non-associative semiring maps.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {R : Type u} -> {S : Type u₁} -> {T : Type u_1} -> [Monoid R] -> [Monoid S] -> [Monoid T] -> {φ : R →* S} -> {A : Type v} -> {B : Type w} -> {C : Type w₁} -> [NonUnitalNonAssocSemiring A] -> [DistribMulAction R A] -> [NonUnitalNonAssocSemiring B] -> [DistribMulAction S B] -> [NonUnitalNonAssocSemiring C] -> [DistribMulAction T C] -> {ψ : S →* T} -> {χ : R →* T} -> (f : B →ₛₙₐ[ψ] C) -> (g : A →ₛₙₐ[φ] B) -> [κ : φ.CompTriple ψ χ] -> A →ₛₙₐ[χ] C
<!-- PINNED-SIGNATURE:END -->


`VTask.comp : {R : Type u} -> {S : Type u₁} -> {T : Type u_1} -> [Monoid R] -> [Monoid S] -> [Monoid T] -> {φ : R →* S} -> {A : Type v} -> {B : Type w} -> {C : Type w₁} -> [NonUnitalNonAssocSemiring A] -> [DistribMulAction R A] -> [NonUnitalNonAssocSemiring B] -> [DistribMulAction S B] -> [NonUnitalNonAssocSemiring C] -> [DistribMulAction T C] -> {ψ : S →* T} -> {χ : R →* T} -> (f : B →ₛₙₐ[ψ] C) -> (g : A →ₛₙₐ[φ] B) -> [κ : φ.CompTriple ψ χ] -> A →ₛₙₐ[χ] C`

`R`, `S`, `T` are the scalar monoids acting on `A`, `B`, `C` respectively. `φ : R →* S` is the monoid homomorphism mediating the scalar actions between `A` and `B`; `ψ : S →* T` mediates those between `B` and `C`; `χ : R →* T` is the composite monoid homomorphism that the result will be equivariant over. The instance `κ` witnesses that `χ` is indeed the composite `ψ ∘ φ`. The argument `f` is the outer morphism (from `B` to `C`, equivariant over `ψ`) and `g` is the inner morphism (from `A` to `B`, equivariant over `φ`). The result is the composite map from `A` to `C`, equivariant over `χ`.

## Conventions

There are no junk-value or edge conventions declared for this definition: it is a total construction depending only on the given morphisms and the compatiblity witness, with no degenerate inputs producing special output.

## Worked examples

- Claim: For any `a : A`, `VTask.comp f g` applied to `a` equals `f (g a)` — that is, the composite acts by first applying `g` then `f`.

- Claim: When `φ`, `ψ`, and `χ` are all the identity monoid homomorphism on a single monoid `R`, and `f : B →ₛₙₐ[id] C` and `g : A →ₛₙₐ[id] B`, then `VTask.comp f g` is the standard function-composition `f ∘ g` viewed as an equivariant non-unital semiring map.

- Claim: `VTask.comp f (VTask.comp g h)` and `VTask.comp (VTask.comp f g) h` represent the same underlying function (associativity of composition), whenever the scalar-action compatibility witnesses are consistent.

## Boundaries

- The construction requires the `CompTriple` witness `κ` asserting that `χ = ψ ∘ φ` as monoid homomorphisms; without it the equivariance condition for the composite cannot be established.
- There is no restriction on the rings or monoids involved beyond the stated typeclasses; in particular, the rings need not be unital or associative.
- If either `f` or `g` is the identity morphism on its respective type, the composite reduces to the other morphism (up to the appropriate `CompTriple` instance).
- The definition is total: it is defined for all valid inputs satisfying the typeclass assumptions.

## Not to be confused with

- The composition of plain ring homomorphisms (unital, associative) — `VTask.comp` operates in the strictly weaker non-unital, non-associative setting.
- The composition of `DistribMulAction` maps alone (without semiring structure) — `VTask.comp` simultaneously respects both the additive semiring and the multiplicative equivariance structure.
- The composition of monoid homomorphisms `φ`, `ψ` into `χ` — that is the scalar-side data consumed by `VTask.comp`, not the output it produces.
