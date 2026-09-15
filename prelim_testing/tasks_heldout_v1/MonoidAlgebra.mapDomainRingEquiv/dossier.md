## VTask.mapDomainRingEquiv

### Object

Given a monoid isomorphism `e : M ≃* N`, this is the induced ring isomorphism between the monoid algebras `R[M]` and `R[N]`. Concretely, an element of `R[M]` is a finitely-supported function from `M` to `R` (thought of as a formal `R`-linear combination of elements of `M`); the isomorphism transports each basis element `m ∈ M` to `e(m) ∈ N` while leaving the coefficients in `R` untouched. The result is a ring equivalence — a bijective ring homomorphism with a specified two-sided inverse — reflecting the principle that isomorphic monoids give rise to isomorphic monoid algebras.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mapDomainRingEquiv : (R : Type u_3) -> {M : Type u_6} -> {N : Type u_7} -> [Semiring R] -> [Monoid M] -> [Monoid N] -> (e : M ≃* N) -> MonoidAlgebra R M ≃+* MonoidAlgebra R N
<!-- PINNED-SIGNATURE:END -->


`(R : Type u_3) -> {M : Type u_6} -> {N : Type u_7} -> [Semiring R] -> [Monoid M] -> [Monoid N] -> (e : M ≃* N) -> MonoidAlgebra R M ≃+* MonoidAlgebra R N`

The first argument `R` is the coefficient semiring, supplied explicitly. `M` and `N` are the source and target monoids, inferred from context. The semiring instance on `R` and monoid instances on `M` and `N` are filled in automatically. The argument `e` is the monoid isomorphism that determines how basis elements are renamed.

### Conventions

The inverse of the resulting ring equivalence is the ring equivalence induced by the inverse monoid isomorphism `e.symm`; there is no junk value convention because the construction is total.

### Worked examples

- Claim: For the identity monoid isomorphism `e : M ≃* M` (i.e., `MulEquiv.refl M`), applying `VTask.mapDomainRingEquiv R e` to the single-term element `single m r` yields `single m r` unchanged.

- Claim: `VTask.mapDomainRingEquiv R e (single m r) = single (e m) r` — the isomorphism sends the basis element `single m r` (the formal monomial `r · m`) to `single (e m) r`, renaming the monoid element via `e` and keeping the coefficient `r`.

- Claim: Applying `VTask.mapDomainRingEquiv R e` followed by `VTask.mapDomainRingEquiv R f` (for `e : M ≃* N`, `f : N ≃* O`) is the same as applying `VTask.mapDomainRingEquiv R (e.trans f)` — the construction is functorial with respect to composition of monoid isomorphisms.

- Claim: The symmetric ring equivalence `(VTask.mapDomainRingEquiv R e).symm` equals `VTask.mapDomainRingEquiv R e.symm`, so the inverse is obtained by inverting the underlying monoid isomorphism.

### Boundaries

- When `M = N` and `e` is the identity isomorphism `MulEquiv.refl M`, the resulting ring equivalence is the identity on `R[M]`.
- The construction is defined for any semiring `R` (not merely a commutative ring or field) and any monoids `M`, `N` (not merely abelian or finite ones).
- The underlying ring homomorphism of the equivalence coincides exactly with `mapDomainRingHom R e`.
- The coefficient function of the image `VTask.mapDomainRingEquiv R e x` is obtained by pre-composing the coefficient function of `x` with `e⁻¹`, i.e., it equals `equivMapDomain e x.coeff`.

### Not to be confused with

- `MonoidAlgebra.mapDomainRingHom R e` — this is merely a ring homomorphism `R[M] →+* R[N]`, not bundled with its inverse as a full equivalence.
- `AddMonoidAlgebra.mapDomainRingEquiv` — the analogous construction for additive monoid algebras (where the group operation on the index type is written additively), not multiplicative monoid algebras.
- `MonoidAlgebra.domCongr` or `Finsupp.equivMapDomain` — these operate at the level of the underlying finitely-supported functions and do not carry the ring structure.
