## Object

`VTask.comp` is the composition of two equivariant maps in the generalized ("twisted") sense. Given a map `f : X →ₑ[φ] Y` (which intertwines the scalar multiplications on `X` and `Y` via the monoid homomorphism `φ : M → N`) and a map `g : Y →ₑ[ψ] Z` (intertwining via `ψ : N → P`), their composite is the underlying set-theoretic composite `g ∘ f`, viewed as an equivariant map `X →ₑ[χ] Z`. The scalar homomorphism `χ : M → P` governing the composite is required to be compatible with `φ` and `ψ` in the sense recorded by the `CompTriple φ ψ χ` instance — typically `χ = ψ ∘ φ`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {M : Type u_2} -> {N : Type u_3} -> {P : Type u_4} -> {φ : M → N} -> {ψ : N → P} -> {χ : M → P} -> {X : Type u_5} -> [SMul M X] -> {Y : Type u_6} -> [SMul N Y] -> {Z : Type u_7} -> [SMul P Z] -> (g : Y →ₑ[ψ] Z) -> (f : X →ₑ[φ] Y) -> [κ : CompTriple φ ψ χ] -> X →ₑ[χ] Z
<!-- PINNED-SIGNATURE:END -->


VTask.comp : {M : Type u_2} -> {N : Type u_3} -> {P : Type u_4} -> {φ : M → N} -> {ψ : N → P} -> {χ : M → P} -> {X : Type u_5} -> [SMul M X] -> {Y : Type u_6} -> [SMul N Y] -> {Z : Type u_7} -> [SMul P Z] -> (g : Y →ₑ[ψ] Z) -> (f : X →ₑ[φ] Y) -> [κ : CompTriple φ ψ χ] -> X →ₑ[χ] Z

`M`, `N`, `P` are the monoids (or groups) acting on the three types. `φ : M → N` is the scalar homomorphism used by `f`; `ψ : N → P` is the scalar homomorphism used by `g`. `χ : M → P` is the composite scalar homomorphism that the result should respect. `X`, `Y`, `Z` are the types carrying the respective actions. The `SMul` instances supply the scalar-multiplication structure on each type. `g` is the outer (right-hand in application) equivariant map, going from `Y` to `Z` and twisting scalars by `ψ`. `f` is the inner (left-hand in application) equivariant map, going from `X` to `Y` and twisting scalars by `φ`. The `CompTriple φ ψ χ` instance `κ` is the proof obligation that `χ` correctly represents the composite `ψ ∘ φ`.

## Conventions

There are no junk-value or edge-case conventions: the definition is total and well-typed whenever valid arguments are supplied, and the `CompTriple` instance is the only constraint (supplied by the type system as an instance argument).

## Worked examples

- Claim: For any equivariant map `f : X →ₑ[φ] Y`, composing with the identity on the right gives back `f`; i.e., `(VTask.comp f (MulActionHom.id M)) = f`.

- Claim: For any equivariant map `g : Y →ₑ[ψ] Z`, composing with the identity on the left gives back `g`; i.e., `(VTask.comp (MulActionHom.id N) g) = g`.

- Claim: Composition is associative: for equivariant maps `f : X →ₑ[φ] Y`, `g : Y →ₑ[ψ] Z`, `h : Z →ₑ[η] T`, one has `VTask.comp h (VTask.comp g f) = VTask.comp (VTask.comp h g) f`.

- Claim: The pointwise value of `VTask.comp g f` at any `x : X` equals `g (f x)`; that is, `comp_apply g f x` confirms evaluation is the set-theoretic composite.

## Boundaries

- When `φ`, `ψ`, and `χ` are all identity maps (the non-twisted case, i.e., equivariant maps in the ordinary sense), `VTask.comp` specialises to ordinary composition of equivariant maps.
- The `CompTriple` instance is usually inferred automatically when `χ` is definitionally equal to `ψ ∘ φ`; if `χ` is some other equal-but-not-definitionally-identical map, the instance may need to be supplied manually.
- If either `f` or `g` is an identity map (`MulActionHom.id`), the composite equals the other map exactly (the left-identity and right-identity laws hold definitionally up to `id_comp` and `comp_id`).
- The composite of an equivariant inverse with the original map collapses to the identity, as witnessed by `comp_inverse'` and `inverse'_comp`.

## Not to be confused with

- `MulActionHom.id`: the identity equivariant map — a neutral element for `VTask.comp`, not a non-trivial composite.
- Function composition `Function.comp` (written `∘`): this forgets the equivariance structure entirely and produces a bare function, not a bundled equivariant map.
- `LinearMap.comp` or `AlgHom.comp`: analogous compositions in the linear or algebra-homomorphism setting; these require additional additive/ring structure beyond a mere scalar action.