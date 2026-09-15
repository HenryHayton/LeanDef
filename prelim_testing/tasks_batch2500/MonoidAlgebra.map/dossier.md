## Object

`VTask.map` lifts an additive monoid homomorphism `f : R →+ S` to a function between monoid algebras `R[M] → S[M]` by applying `f` coefficient-wise. That is, given a formal finite linear combination `∑ aₘ · m` with coefficients in `R` and "monomials" in `M`, it returns `∑ f(aₘ) · m` with coefficients in `S`. The monomial structure (the elements of `M` that appear) is left unchanged; only the coefficients are transformed.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {R : Type u_3} -> {S : Type u_4} -> {M : Type u_6} -> [Semiring R] -> [Semiring S] -> (f : R →+ S) -> (x : MonoidAlgebra R M) -> MonoidAlgebra S M
<!-- PINNED-SIGNATURE:END -->


`VTask.map : {R : Type u_3} -> {S : Type u_4} -> {M : Type u_6} -> [Semiring R] -> [Semiring S] -> (f : R →+ S) -> (x : MonoidAlgebra R M) -> MonoidAlgebra S M`

The implicit type arguments `R` and `S` are the coefficient semirings of the source and target algebras respectively. `M` is the type of monomials (the "exponent" or "group element" type). The semiring instances on `R` and `S` are provided implicitly. The explicit argument `f` is the additive monoid homomorphism used to transform each coefficient. The argument `x` is the element of the monoid algebra `R[M]` to be mapped.

## Conventions

No special junk-value or edge conventions are declared: the function is total and well-defined on every element of `MonoidAlgebra R M`, including the zero element and elements with empty support, without any exceptional-case patching.

## Worked examples

- Claim: Applying `VTask.map` with the zero additive homomorphism `R →+ S` to any element sends every coefficient to zero, producing the zero element of `S[M]`.

- Claim: If `single m r` denotes the monoid algebra element with coefficient `r` at monomial `m` and zero elsewhere, then `VTask.map f (single m r) = single m (f r)`.

- Claim: `VTask.map` applied to the zero element of `R[M]` yields the zero element of `S[M]`, since `f 0 = 0` for any additive monoid homomorphism `f`.

- Claim: When `f = AddMonoidHom.id R` (the identity on `R`), `VTask.map f` acts as the identity on `MonoidAlgebra R M`.

## Boundaries

- **Zero element**: The zero of `R[M]` (the empty linear combination) maps to the zero of `S[M]`, because `f.map_zero` ensures `f 0 = 0` and thus every coefficient that was zero remains zero.
- **Single-monomial elements**: An element supported at a single monomial `m` with coefficient `r` maps to the element supported at the same `m` with coefficient `f r`.
- **Empty support**: If `x` has empty support (i.e., `x = 0`), the image also has empty support.
- **Support can only shrink**: If `f r = 0` for some nonzero `r ∈ R`, then monomials whose coefficient maps to zero will drop out of the support of the image. The support of `VTask.map f x` is a subset of the support of `x`.
- **Not a ring homomorphism in general**: `VTask.map f` is built from an *additive* monoid homomorphism, so it preserves the additive structure but is not guaranteed to respect multiplication unless `f` is also multiplicative.

## Not to be confused with

- `MonoidAlgebra.liftNCRingHom` / `MonoidAlgebra.lift`: lifts a pair of compatible semiring and monoid maps to a *ring* homomorphism `R[M] → A`, rather than just acting coefficient-wise on a fixed monomial set.
- `MonoidAlgebra.mapDomain`: transforms the *monomials* (keys) of a monoid algebra element using a function `M → N`, leaving coefficients in the same ring, as opposed to `VTask.map` which transforms the *coefficients* while fixing the monomials.
- `Finsupp.mapRange`: the underlying finitely-supported-function operation that applies a function to each value in the codomain; `VTask.map` is its structured counterpart living in the `MonoidAlgebra` API and carrying the algebraic bookkeeping.