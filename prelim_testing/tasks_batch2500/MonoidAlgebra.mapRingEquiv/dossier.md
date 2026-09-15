## VTask.mapRingEquiv

### Object

Given a ring isomorphism between two semirings R and S, `VTask.mapRingEquiv` produces a corresponding ring isomorphism between the monoid algebras R[M] and S[M]. Concretely, it lifts a coefficient-level isomorphism to an isomorphism of the whole monoid algebra by applying the ring isomorphism to each coefficient, leaving the monoid elements (the "exponents") untouched. This formalises the intuition that isomorphic coefficient rings yield isomorphic monoid algebras.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mapRingEquiv : {R : Type u_3} -> {S : Type u_4} -> (M : Type u_6) -> [Semiring R] -> [Semiring S] -> [Monoid M] -> (e : R ≃+* S) -> MonoidAlgebra R M ≃+* MonoidAlgebra S M
<!-- PINNED-SIGNATURE:END -->


`VTask.mapRingEquiv : {R : Type u_3} -> {S : Type u_4} -> (M : Type u_6) -> [Semiring R] -> [Semiring S] -> [Monoid M] -> (e : R ≃+* S) -> MonoidAlgebra R M ≃+* MonoidAlgebra S M`

The explicit type argument `M` is the monoid whose elements index the basis; it is carried along unchanged by the construction. The implicit types `R` and `S` are the source and target semirings, inferred from the equivalence. The instance arguments `[Semiring R]`, `[Semiring S]`, and `[Monoid M]` supply the required algebraic structures. The explicit argument `e` is the ring isomorphism R ≃+* S whose action on coefficients is to be extended to the full monoid algebra.

### Conventions

The monoid `M` determines the indexing structure of both monoid algebras and is held fixed; there is no notion of a "junk value" here since the construction is total and well-defined for all valid inputs.

### Worked examples

- Claim: For the identity ring isomorphism `e = RingEquiv.refl R`, the induced equivalence `VTask.mapRingEquiv M e` acts as the identity on every element of `MonoidAlgebra R M`, since every coefficient is sent to itself.

- Claim: The coefficient of monoid element `m` in the image `VTask.mapRingEquiv M e x` equals `e` applied to the coefficient of `m` in `x`. That is, `(VTask.mapRingEquiv M e x).coeff m = e (x.coeff m)`.

- Claim: On a basis element `single m r`, the equivalence satisfies `VTask.mapRingEquiv M e (single m r) = single m (e r)` — the monoid component is unchanged and the coefficient is mapped by `e`.

- Claim: The inverse of `VTask.mapRingEquiv M e` is `VTask.mapRingEquiv M e.symm`. That is, `(VTask.mapRingEquiv M e).symm = VTask.mapRingEquiv M e.symm`.

- Claim: Composing two ring isomorphisms is compatible with the construction: `VTask.mapRingEquiv M (e₁.trans e₂) = (VTask.mapRingEquiv M e₁).trans (VTask.mapRingEquiv M e₂)`.

### Boundaries

- The construction is entirely determined by the coefficients: the underlying ring homomorphism of `VTask.mapRingEquiv M e` coincides with `mapRingHom M e`.
- When `e` is the identity isomorphism, the resulting equivalence is the identity on `MonoidAlgebra R M`.
- The definition is valid for semirings (not just rings), so it applies in a broad algebraic context.
- There is no restriction on the monoid `M`; it may be infinite, non-commutative, or trivial.

### Not to be confused with

- `MonoidAlgebra.mapRingHom`: the underlying ring homomorphism in one direction only, not a two-sided isomorphism.
- `MonoidAlgebra.mapDomain`: transports the monoid index set via a monoid homomorphism rather than transforming the coefficient ring.
- `AddMonoidAlgebra.mapRingEquiv`: the analogous construction for additive monoid algebras rather than multiplicative monoid algebras.