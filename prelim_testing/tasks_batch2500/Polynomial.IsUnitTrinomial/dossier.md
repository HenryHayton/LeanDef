## VTask.IsUnitTrinomial

### Object

A predicate on integer polynomials asserting that the polynomial is a *unit trinomial*: it has exactly three nonzero terms, and every nonzero coefficient is a unit of ℤ (i.e., either +1 or −1). Equivalently, such a polynomial can be written in the form ε₁·Xᵏ + ε₂·Xᵐ + ε₃·Xⁿ where k < m < n are natural numbers and ε₁, ε₂, ε₃ ∈ {+1, −1}.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsUnitTrinomial : (p : Polynomial ℤ) -> Prop
<!-- PINNED-SIGNATURE:END -->


The single argument `p` is the integer polynomial being tested for the unit-trinomial property.

### Conventions

The three exponents k, m, n are required to be strictly increasing (k < m < n), which forces the three terms to be genuinely distinct monomials. The coefficients are required to be units of ℤ, meaning each is exactly +1 or −1 (the only invertible integers). There is no convention assigning a junk value because the predicate is a `Prop`; it is simply false for polynomials that do not meet the structural requirement.

### Worked examples

- Claim: `VTask.IsUnitTrinomial (Polynomial.X ^ 2 - Polynomial.X + 1 : Polynomial ℤ)` holds, since this is X² + (−1)·X¹ + 1·X⁰, a trinomial with exponents 0 < 1 < 2 and all coefficients equal to ±1.

- Claim: `VTask.IsUnitTrinomial (Polynomial.X ^ 3 + Polynomial.X + 1 : Polynomial ℤ)` holds, since this is 1·X³ + 1·X¹ + 1·X⁰ with exponents 0 < 1 < 3 and all coefficients +1.

- Claim: `¬ VTask.IsUnitTrinomial (2 * Polynomial.X ^ 2 + Polynomial.X + 1 : Polynomial ℤ)` holds, because the leading coefficient 2 is not a unit of ℤ.

- Claim: `¬ VTask.IsUnitTrinomial (Polynomial.X ^ 2 + Polynomial.X : Polynomial ℤ)` holds, because this polynomial has only two nonzero terms, not three.

### Boundaries

- A polynomial with exactly three nonzero terms but at least one coefficient equal to 2 or any non-unit integer is **not** a unit trinomial.
- A polynomial with fewer than three or more than three nonzero terms is **not** a unit trinomial, even if the nonzero coefficients happen to all be ±1.
- The zero polynomial is **not** a unit trinomial (it has no nonzero terms).
- A monomial or binomial with all coefficients ±1 is **not** a unit trinomial, as term count must be exactly three.
- The characterization via support is equivalent: `VTask.IsUnitTrinomial p` if and only if `p` has a support of size 3 and every element of the support gives a unit coefficient.

### Not to be confused with

- `Polynomial.trinomial`: the constructor function that builds a specific three-term polynomial from given exponents and coefficients; `VTask.IsUnitTrinomial` is the predicate asserting a polynomial *is* of this form with unit coefficients.
- A *trinomial* with arbitrary integer coefficients: `VTask.IsUnitTrinomial` additionally demands each coefficient is ±1, not merely nonzero.
- `Polynomial.IsUnit`: a predicate asserting the polynomial itself is a unit in the polynomial ring, which is a much stronger (and almost always false for nonconstant polynomials) condition entirely unrelated to the coefficients being units.