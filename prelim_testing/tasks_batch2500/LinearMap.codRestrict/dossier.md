## Object

`VTask.codRestrict` takes a semilinear map `f : M →ₛₗ[σ₁₂] M₂` whose images all land inside a submodule `p ≤ M₂`, and produces a semilinear map `M →ₛₗ[σ₁₂] ↥p` — that is, the same underlying function but now regarded as mapping into `p` rather than all of `M₂`. The resulting map is definitionally equal to `f` when composed with the inclusion `p.subtype : ↥p →ₛₗ[…] M₂`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.codRestrict : {R : Type u_1} -> {R₂ : Type u_3} -> {M : Type u_5} -> {M₂ : Type u_7} -> [Semiring R] -> [Semiring R₂] -> [AddCommMonoid M] -> [AddCommMonoid M₂] -> [Module R M] -> [Module R₂ M₂] -> {σ₁₂ : R →+* R₂} -> (p : Submodule R₂ M₂) -> (f : M →ₛₗ[σ₁₂] M₂) -> (h : ∀ (c : M), f c ∈ p) -> M →ₛₗ[σ₁₂] ↥p
<!-- PINNED-SIGNATURE:END -->


`VTask.codRestrict : {R : Type u_1} -> {R₂ : Type u_3} -> {M : Type u_5} -> {M₂ : Type u_7} -> [Semiring R] -> [Semiring R₂] -> [AddCommMonoid M] -> [AddCommMonoid M₂] -> [Module R M] -> [Module R₂ M₂] -> {σ₁₂ : R →+* R₂} -> (p : Submodule R₂ M₂) -> (f : M →ₛₗ[σ₁₂] M₂) -> (h : ∀ (c : M), f c ∈ p) -> M →ₛₗ[σ₁₂] ↥p`

- `p` is the target submodule of `M₂` into which the restricted map will land.
- `f` is the semilinear map being restricted; its codomain is `M₂` and it is twisted by the ring homomorphism `σ₁₂ : R →+* R₂`.
- `h` is the proof obligation that every value `f c` for `c : M` lies in `p`; this is what makes the codomain restriction valid.

## Conventions

No special junk-value or out-of-domain conventions are declared: the definition is total and requires an explicit membership proof `h`, so there is no regime in which the output is undefined or silently defaulted.

## Worked examples

- Claim: Applying `VTask.codRestrict p f h` at a point `x : M` and then coercing back to `M₂` via `p.subtype` recovers `f x`.

- Claim: The composition of the submodule inclusion `p.subtype` with `VTask.codRestrict p f h` equals `f` as a semilinear map `M →ₛₗ[σ₁₂] M₂`.

- Claim: The kernel of `VTask.codRestrict p f h` equals the kernel of `f`; restricting the codomain does not change which inputs map to zero.

- Claim: If `f : M →ₛₗ[σ₁₂] M₂` is injective, then `VTask.codRestrict p f h` is also injective, and conversely.

## Boundaries

- When `p` is the top submodule `⊤` of `M₂`, the restricted map is essentially the same as `f` up to a canonical isomorphism `↥⊤ ≃ M₂`.
- When `p` is the zero submodule and `f` is the zero map, the proof `h` is satisfied and the result is the zero map into the trivial submodule.
- The domain `M` is unrestricted; the definition works for any `M` satisfying the module axioms, including the zero module.
- The ring homomorphism `σ₁₂` is arbitrary (no surjectivity or bijectivity assumed), so the construction is valid for non-bijective scalings.

## Not to be confused with

- `LinearMap.domRestrict`: restricts the *domain* of a linear map to a submodule, rather than the codomain.
- `LinearMap.codLift` (mentioned in the docstring): a related construction that goes in the other direction — lifting a map through a quotient — rather than restricting into a submodule.
- `Submodule.subtype` (the inclusion `↥p →ₛₗ M₂`): this is the *inclusion* map out of a submodule, which is the right inverse of codRestrict in the sense that composing subtype after codRestrict recovers `f`.