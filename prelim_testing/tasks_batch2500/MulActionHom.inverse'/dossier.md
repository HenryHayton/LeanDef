## Object

`VTask.inverse'` constructs a bundled equivariant map in the reverse direction from a bijective equivariant map. Concretely, given an equivariant map `f : X →ₑ[φ] Y` (where `φ : M → N` relates the two acting monoids) together with a bare set-theoretic inverse `g : Y → X`, evidence that `φ'` is a right-inverse of `φ`, and evidence that `g` is a two-sided inverse of `f`, it packages `g` into a fully bundled equivariant map `Y →ₑ[φ'] X` — verifying that `g` intertwines the scalar actions twisted by `φ'`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.inverse' : {M : Type u_2} -> {N : Type u_3} -> {φ : M → N} -> {X : Type u_5} -> [SMul M X] -> {Y : Type u_6} -> [SMul N Y] -> {φ' : N → M} -> (f : X →ₑ[φ] Y) -> (g : Y → X) -> (k : Function.RightInverse φ' φ) -> (h₁ : Function.LeftInverse g ⇑f) -> (h₂ : Function.RightInverse g ⇑f) -> Y →ₑ[φ'] X
<!-- PINNED-SIGNATURE:END -->


`VTask.inverse' : {M : Type u_2} -> {N : Type u_3} -> {φ : M → N} -> {X : Type u_5} -> [SMul M X] -> {Y : Type u_6} -> [SMul N Y] -> {φ' : N → M} -> (f : X →ₑ[φ] Y) -> (g : Y → X) -> (k : Function.RightInverse φ' φ) -> (h₁ : Function.LeftInverse g ⇑f) -> (h₂ : Function.RightInverse g ⇑f) -> Y →ₑ[φ'] X`

The implicit type arguments `M` and `N` are the two scalar-action monoids (or semigroups), and `φ : M → N` is the ring/monoid homomorphism twisting the action of `f`. `X` and `Y` are the two sets carrying the respective `M`- and `N`-actions. The implicit `φ' : N → M` is the monoid map that will twist the action of the inverse map. `f` is the forward equivariant map being inverted. `g` is the underlying set-theoretic inverse function. `k` is the proof that `φ'` is a right inverse of `φ` (i.e. `φ (φ' n) = n` for all `n`), which is needed to make the scalar-action intertwining work. `h₁` is the proof that `g` is a left inverse of `f` (i.e. `g (f x) = x`). `h₂` is the proof that `g` is a right inverse of `f` (i.e. `f (g y) = y`). The return value is the bundled equivariant map `Y →ₑ[φ'] X` whose underlying function is `g`.

## Conventions

No special junk-value or out-of-domain conventions are declared: the definition is total and well-defined for any arguments satisfying the stated hypotheses; there are no degenerate edge cases that produce a conventionally chosen filler value.

## Worked examples

- Claim: The underlying function of `VTask.inverse' f g k h₁ h₂` is `g` — that is, applying the resulting equivariant map to any `y : Y` gives `g y`.

- Claim: Composing `VTask.inverse' f g k h₁ h₂` on the right with `f` yields the identity equivariant map on `Y`; that is, `f.comp (VTask.inverse' f g k h₁ h₂) = MulActionHom.id N` (matching `inverse'_comp`).

- Claim: Taking the inverse of the inverse recovers the original map: `VTask.inverse' (VTask.inverse' f g k₂ h₁ h₂) f k₁ h₂ h₁ = f` (matching `inverse'_inverse'`).

## Boundaries

- Both `h₁` and `h₂` are required: left-inverse alone does not guarantee equivariance of `g`, because the proof of `map_smul'` for `g` needs `h₂` (to rewrite `x` as `f (g x)`) and `h₁` (to cancel the outer `f` after rewriting). Providing only one direction is insufficient.
- The hypothesis `k : Function.RightInverse φ' φ` (meaning `φ (φ' n) = n`) is strictly needed; the weaker condition of `φ'` being a left inverse of `φ` is not sufficient for the equivariance proof of the inverse map.
- When `φ` is the identity (the non-twisted case), `VTask.inverse'` with `φ' = id` and `k = congrFun rfl` agrees with the simpler `inverse` construction (as stated by `inverse_eq_inverse'`).
- There is no restriction on whether `M` and `N` are groups, monoids, or mere semigroups: the construction works in the general `SMul` setting.

## Not to be confused with

- `MulActionHom.inverse` — the non-twisted variant for `M`-equivariant maps `X →[M] Y` where the same monoid acts on both sides; `VTask.inverse'` handles the more general twisted (semilinear-style) setting.
- `Equiv.toMulActionHom` — builds an equivariant map from a full `Equiv` bundled with equivariance proofs; `VTask.inverse'` works from bare inverse-function evidence without requiring a pre-packaged `Equiv`.
- `MulActionHom.comp` — composes two equivariant maps; `VTask.inverse'` instead reverses a single equivariant map.
