## Object

Given two submodules `p` and `q` of a module `M` over a semiring `R` that are literally equal (as submodules), `VTask.ofEq p q h` is the canonical linear equivalence (i.e., a bijective linear map together with a linear inverse) between the coerced types `↥p` and `↥q`. Because `p` and `q` are the same submodule, this equivalence is essentially the identity map re-typed along the proof of equality.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofEq : {R : Type u_1} -> {M : Type u_5} -> [Semiring R] -> [AddCommMonoid M] -> {module_M : Module R M} -> (p q : Submodule R M) -> (h : p = q) -> ↥p ≃ₗ[R] ↥q
<!-- PINNED-SIGNATURE:END -->


`VTask.ofEq : {R : Type u_1} -> {M : Type u_5} -> [Semiring R] -> [AddCommMonoid M] -> {module_M : Module R M} -> (p q : Submodule R M) -> (h : p = q) -> ↥p ≃ₗ[R] ↥q`

`R` is the scalar semiring. `M` is the ambient additive commutative monoid carrying an `R`-module structure. `p` and `q` are the two submodules of `M` between which the equivalence is built. `h` is the proof that `p` and `q` are definitionally equal as submodules; this is what makes the construction possible and determines the equivalence entirely.

## Conventions

No junk-value or edge conventions are declared for this definition: it is a total construction parametrised by a proof of equality, and every input combination that type-checks yields a well-defined linear equivalence with no special degenerate cases requiring separate treatment.

## Worked examples

- Claim: For any submodule `p`, `VTask.ofEq p p rfl` sends every element of `p` to itself (as an element of `p`).

- Claim: For submodules `p` and `q` with a proof `h : p = q` and any `x : ↥p`, the image `(VTask.ofEq p q h) x` has the same underlying element of `M` as `x`.

- Claim: The inverse of `VTask.ofEq p q h` is `VTask.ofEq q p h.symm`, in the sense that composing the two linear equivalences yields the identity on either side.

## Boundaries

- The only input that matters for the map's behaviour is the proof `h : p = q`; since `p = q` as submodules, the underlying sets are identical and the map acts as the identity on elements of `M`.
- When `h` is `rfl` (i.e., `p` and `q` are definitionally the same), `VTask.ofEq p p rfl` is the identity linear equivalence on `↥p`.
- The construction is valid even when `p` is the zero submodule or the whole module `M`; no special casing occurs at these extremes.
- Because the equivalence is determined entirely by `h`, two calls with proofs `h₁ h₂ : p = q` yield the same map on underlying elements (submodule equality proofs are proof-irrelevant in the relevant sense).

## Not to be confused with

- `Submodule.inclusion`: a linear map (not necessarily an equivalence) from a submodule into a larger submodule given a containment `p ≤ q`, not an equality.
- `LinearEquiv.refl R M`: the identity linear equivalence on the whole module `M`, not on a submodule coercion.
- `Equiv.setCongr`: a bare (non-linear) type equivalence between sets given a set equality, which `VTask.ofEq` extends with linearity.