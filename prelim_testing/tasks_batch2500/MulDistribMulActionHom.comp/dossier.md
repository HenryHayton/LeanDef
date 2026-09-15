## Object

`VTask.comp` constructs the composition of two equivariant multiplicative monoid homomorphisms. Given a map `f : A →ₑ*[φ] B` (a multiplicative monoid homomorphism from `A` to `B` that is equivariant with respect to the group-action morphism `φ : M →* N`) and a map `g : B →ₑ*[ψ] C` (a multiplicative monoid homomorphism from `B` to `C` equivariant with respect to `ψ : N →* P`), together with a witness that `φ` and `ψ` compose to give `χ : M →* P`, the result is a multiplicative monoid homomorphism `A →ₑ*[χ] C` that is equivariant with respect to `χ`.

Intuitively, if `f` intertwines the `M`-action on `A` with the `N`-action on `B` (via `φ`), and `g` intertwines the `N`-action on `B` with the `P`-action on `C` (via `ψ`), then `g ∘ f` intertwines the `M`-action on `A` with the `P`-action on `C` via the composite scalar morphism `χ = ψ ∘ φ`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {M : Type u_1} -> [Monoid M] -> {N : Type u_2} -> [Monoid N] -> {P : Type u_3} -> [Monoid P] -> {φ : M →* N} -> {ψ : N →* P} -> {χ : M →* P} -> {A : Type u_4} -> [Monoid A] -> [MulDistribMulAction M A] -> {B : Type u_5} -> [Monoid B] -> [MulDistribMulAction N B] -> {C : Type u_7} -> [Monoid C] -> [MulDistribMulAction P C] -> [κ : φ.CompTriple ψ χ] -> (g : B →ₑ*[ψ] C) -> (f : A →ₑ*[φ] B) -> A →ₑ*[χ] C
<!-- PINNED-SIGNATURE:END -->


VTask.comp : {M : Type u_1} -> [Monoid M] -> {N : Type u_2} -> [Monoid N] -> {P : Type u_3} -> [Monoid P] -> {φ : M →* N} -> {ψ : N →* P} -> {χ : M →* P} -> {A : Type u_4} -> [Monoid A] -> [MulDistribMulAction M A] -> {B : Type u_5} -> [Monoid B] -> [MulDistribMulAction N B] -> {C : Type u_7} -> [Monoid C] -> [MulDistribMulAction P C] -> [κ : φ.CompTriple ψ χ] -> (g : B →ₑ*[ψ] C) -> (f : A →ₑ*[φ] B) -> A →ₑ*[χ] C

`M`, `N`, `P` are the monoids acting on the source, intermediate, and target types respectively. `φ : M →* N` is the monoid homomorphism relating the source and intermediate scalar monoids; `ψ : N →* P` relates the intermediate and target scalar monoids; `χ : M →* P` is the composite scalar morphism. `A`, `B`, `C` are the multiplicative monoids being acted upon (source, intermediate, and target carrier types). The instance `κ` is a proof that `χ` is the composition of `φ` followed by `ψ` (i.e., `χ = ψ ∘ φ` as monoid homomorphisms). The argument `g` is the equivariant monoid homomorphism from `B` to `C` intertwining the `N`- and `P`-actions via `ψ`. The argument `f` is the equivariant monoid homomorphism from `A` to `B` intertwining the `M`- and `N`-actions via `φ`. The result is their pointwise composite as a function, carrying both the monoid homomorphism structure and the equivariance structure with respect to `χ`.

## Conventions

There are no declared junk-value or edge-case conventions for this definition: it is a total construction on well-typed inputs and every combination of valid arguments produces a meaningful equivariant monoid homomorphism.

## Worked examples

- Claim: If `f` and `g` are equivariant monoid homomorphisms with compatible scalar morphisms, then `VTask.comp g f` applied to an element `a : A` equals `g (f a)` as underlying functions.

- Claim: `VTask.comp g f` preserves the monoid identity: `VTask.comp g f 1 = 1`, since both `f` and `g` individually preserve `1`.

- Claim: For scalar `m : M` and `a : A`, the composite satisfies `VTask.comp g f (m • a) = χ(m) • VTask.comp g f a`, reflecting the chained equivariance through the `CompTriple` witness.

## Boundaries

- When `φ`, `ψ`, and `χ` are all identity morphisms and `M = N = P`, the construction reduces to ordinary composition of equivariant monoid endomorphisms.
- When `A = B = C` and `f` or `g` is the identity equivariant map, the composition is the other map (up to definitional equality).
- The `CompTriple` instance `κ` is the key coherence datum; without it, the types of `g ∘ f` and the claimed scalar morphism `χ` would not be compatible. The definition does not apply unless this witness is present.
- Because the underlying carrier types and monoid structures are fully general, there is no restriction on the sizes of `A`, `B`, or `C`.

## Not to be confused with

- `MulActionHom.comp`: composes equivariant maps for `MulAction` (without the monoid homomorphism requirement on the carrier maps); `VTask.comp` additionally requires and preserves the monoid multiplication structure.
- `MonoidHom.comp`: composes plain monoid homomorphisms with no equivariance/action data; `VTask.comp` tracks and requires the compatibility between scalar monoid morphisms.
- `VTask.comp` for additive equivariant maps (`AddMonoidHom`-based equivariant composition): the additive analogue has the same shape but for additive monoids and uses `+` rather than `*` throughout.