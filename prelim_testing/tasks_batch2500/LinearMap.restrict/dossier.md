## Object

`VTask.restrict` takes a semilinear map `f : M →ₛₗ[σ₁₂] M₂` together with submodules `p ⊆ M` and `q ⊆ M₂` and a proof that `f` carries `p` into `q`, and produces the induced semilinear map `p →ₛₗ[σ₁₂] q` obtained by simultaneously restricting the domain to `p` and the codomain to `q`. The resulting map acts on elements of `p` exactly as `f` does on their underlying elements of `M`, but the codomain type is recorded as `q` rather than `M₂`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.restrict : {R : Type u_1} -> {R₂ : Type u_3} -> {M : Type u_5} -> {M₂ : Type u_7} -> [Semiring R] -> [Semiring R₂] -> [AddCommMonoid M] -> [AddCommMonoid M₂] -> [Module R M] -> [Module R₂ M₂] -> {σ₁₂ : R →+* R₂} -> (f : M →ₛₗ[σ₁₂] M₂) -> {p : Submodule R M} -> {q : Submodule R₂ M₂} -> (hf : ∀ x ∈ p, f x ∈ q) -> ↥p →ₛₗ[σ₁₂] ↥q
<!-- PINNED-SIGNATURE:END -->


VTask.restrict : {R : Type u_1} -> {R₂ : Type u_3} -> {M : Type u_5} -> {M₂ : Type u_7} -> [Semiring R] -> [Semiring R₂] -> [AddCommMonoid M] -> [AddCommMonoid M₂] -> [Module R M] -> [Module R₂ M₂] -> {σ₁₂ : R →+* R₂} -> (f : M →ₛₗ[σ₁₂] M₂) -> {p : Submodule R M} -> {q : Submodule R₂ M₂} -> (hf : ∀ x ∈ p, f x ∈ q) -> ↥p →ₛₗ[σ₁₂] ↥q

`f` is the ambient semilinear map whose domain and codomain are to be restricted. `p` is the submodule of `M` that serves as the new domain. `q` is the submodule of `M₂` that serves as the new codomain. `hf` is the proof obligation that `f` maps every element of `p` into `q`, ensuring the restriction is well-typed.

## Conventions

The ring homomorphism `σ₁₂ : R →+* R₂` governing the semilinearity is inherited unchanged from `f`; restricting to submodules does not alter the scalar action structure. When `p` and `q` are both the whole module (i.e., `⊤`), `VTask.restrict` recovers a map that is canonically equivalent to `f` itself.

## Worked examples

- Claim: For a linear map `f : M →ₗ[R] M₂` and submodules `p`, `q` with `hf : ∀ x ∈ p, f x ∈ q`, the underlying function of `VTask.restrict f hf` on an element `⟨x, hx⟩ : p` equals `⟨f x, hf x hx⟩ : q` as elements of `M₂`.

- Claim: If `f : M →ₗ[R] M` is an endomorphism and `p` is an `f`-invariant submodule (meaning `∀ x ∈ p, f x ∈ p`), then `VTask.restrict f h` is a well-defined linear endomorphism of `p`, and its value on any `⟨v, hv⟩ : p` coerces back to `f v` in `M`.

- Claim: `VTask.restrict` is compatible with composition: if `g : M₂ →ₛₗ[σ₂₃] M₃` maps `q` into a submodule `r`, and `f` maps `p` into `q`, then composing the two restricted maps yields the same semilinear map on `p` as restricting `g ∘ₗ f` to `p` and `r` directly.

## Boundaries

- If `p = ⊥` (the zero submodule), `VTask.restrict f hf` is the zero map from the trivial module to `q`; the proof obligation `hf` is vacuously satisfied by any `f`.
- If `q = ⊤` (the whole module `M₂`), then `hf` is trivially satisfied for any `f` and any `p`, and the result is the domain restriction of `f` to `p` with codomain `M₂` (up to the subtype coercion to `⊤`).
- If `p = ⊤` and `q = ⊤`, the restriction is canonically equivalent to `f` itself.
- The map is only required to send `p` into `q`, not onto `q`; no surjectivity is assumed or guaranteed.
- Injectivity of the restriction follows from injectivity of `f`, since the underlying function is unchanged.

## Not to be confused with

- `LinearMap.domRestrict`: restricts only the domain of a linear map to a submodule, leaving the codomain as the full module `M₂`.
- `LinearMap.codRestrict`: restricts only the codomain of a linear map to a submodule, leaving the domain as the full module `M`.
- `LinearMap.restrictScalars`: changes the ring of scalars acting on modules, rather than restricting the domain or codomain to submodules.