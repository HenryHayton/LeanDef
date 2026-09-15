## VTask.algEquivOfCompEqX

### Object

Given two polynomials `p` and `q` over a commutative semiring `R` that are composition-inverses of each other (i.e., `p(q(X)) = X` and `q(p(X)) = X`), this construction produces an algebra automorphism of the polynomial ring `R[X]` over `R`. The forward direction sends a polynomial `f` to `f(p)` (substituting `p` for the variable), and the inverse sends `f` to `f(q)`. The two conditions ensure these substitution maps are mutually inverse, giving a genuine isomorphism of `R`-algebras.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.algEquivOfCompEqX : {R : Type u} -> [CommSemiring R] -> (p q : Polynomial R) -> (hpq : p.comp q = Polynomial.X) -> (hqp : q.comp p = Polynomial.X) -> Polynomial R ≃ₐ[R] Polynomial R
<!-- PINNED-SIGNATURE:END -->


`VTask.algEquivOfCompEqX : {R : Type u} -> [CommSemiring R] -> (p q : Polynomial R) -> (hpq : p.comp q = Polynomial.X) -> (hqp : q.comp p = Polynomial.X) -> Polynomial R ≃ₐ[R] Polynomial R`

The implicit type `R` is the coefficient ring, equipped with a commutative semiring structure via the typeclass argument. The argument `p` is the polynomial used for substitution in the forward direction of the automorphism. The argument `q` is its composition-inverse, used for substitution in the reverse direction. The proof `hpq` witnesses that composing `p` after `q` yields the identity polynomial `X`. The proof `hqp` witnesses that composing `q` after `p` also yields `X`. Together these conditions guarantee the two substitution maps are inverse `R`-algebra homomorphisms.

### Conventions

No junk-value or edge conventions are declared for this definition: it is a proof-relevant construction whose inputs are constrained by explicit hypotheses (`hpq` and `hqp`), so there are no "out-of-domain" inputs to assign conventional values to.

### Worked examples

- Claim: The pair `p = X + C r` and `q = X - C r` (translation and its inverse) satisfies the composition conditions and yields an automorphism whose forward map sends any polynomial `f` to `f(X + r)`.

- Claim: The symmetry theorem holds: the inverse of `VTask.algEquivOfCompEqX p q hpq hqp` equals `VTask.algEquivOfCompEqX q p hqp hpq`.

- Claim: Two such automorphisms `VTask.algEquivOfCompEqX p q hpq hqp` and `VTask.algEquivOfCompEqX p' q' hpq' hqp'` are equal if and only if `p = p'`.

- Claim: For the identity polynomial `p = q = X` (which satisfies `X.comp X = X` on both sides), `VTask.algEquivOfCompEqX X X rfl rfl` is the identity automorphism of `R[X]`.

### Boundaries

- The construction requires both `hpq : p.comp q = X` and `hqp : q.comp p = X` to be provided; neither condition alone suffices to determine the other in general over a commutative semiring (without additional hypotheses such as being over a field or having degree conditions). Both proofs must be supplied explicitly.
- Over a commutative semiring (not necessarily a ring or field), translation polynomials of the form `X + C r` have composition-inverse `X - C r` only when subtraction makes sense; the hypotheses gate entry into the construction.
- The two composition conditions force `p` and `q` each to have degree exactly 1 when `R` is an integral domain, but the construction itself does not restrict to degree-1 polynomials — any pair satisfying the composition conditions is accepted.
- The automorphism is an `R`-algebra map, meaning it fixes all constant polynomials `C r` for `r : R`.

### Not to be confused with

- `Polynomial.aeval`: the plain `R`-algebra homomorphism `R[X] →ₐ[R] A` given by evaluation at a point; `VTask.algEquivOfCompEqX` bundles two such maps into a full equivalence.
- `AlgEquiv.ofAlgHom`: the generic constructor that builds an `AlgEquiv` from two mutually inverse algebra homomorphisms; `VTask.algEquivOfCompEqX` is the polynomial-specific wrapper that derives the inverses from the composition-equals-`X` conditions.
- `Polynomial.mapAlgEquiv` (or ring homomorphism-induced equivalences on polynomial rings): those lift a base-ring automorphism to `R[X]`, whereas `VTask.algEquivOfCompEqX` acts on the variable by substitution, fixing the base ring `R` pointwise.
