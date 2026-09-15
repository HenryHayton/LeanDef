## VTask.weightedHomogeneousSubmodule

### Object

Given a commutative semiring `R`, a type of variables `σ`, an additive commutative monoid `M`, a weight function `w : σ → M`, and a target degree `m : M`, this object is the **submodule of `MvPolynomial σ R`** consisting exactly of those multivariate polynomials that are *weighted homogeneous of weighted degree `m`*. A polynomial is weighted homogeneous of degree `m` (with respect to `w`) if every monomial appearing with a nonzero coefficient has weighted total degree equal to `m`, where the weighted degree of a monomial `∏ xᵢ^{eᵢ}` is `∑ᵢ eᵢ · w(xᵢ)` computed in `M`. As `m` varies, these submodules form a graded structure on `MvPolynomial σ R`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.weightedHomogeneousSubmodule : (R : Type u_1) -> {M : Type u_2} -> [CommSemiring R] -> {σ : Type u_3} -> [AddCommMonoid M] -> (w : σ → M) -> (m : M) -> Submodule R (MvPolynomial σ R)
<!-- PINNED-SIGNATURE:END -->


The type string is inserted automatically above.

- `R` is the coefficient ring (a commutative semiring).
- `M` is the grading monoid, i.e., the additive commutative monoid in which weighted degrees are measured.
- `σ` is the type indexing the variables of the polynomial ring.
- `w` is the weight function assigning to each variable `x : σ` its weight `w x ∈ M`; it determines how the degree of a monomial is computed.
- `m` is the target weighted degree; the submodule consists of all polynomials whose every nonzero monomial has weighted degree exactly `m`.

### Conventions

The zero polynomial is considered weighted homogeneous of every degree, so it belongs to every `VTask.weightedHomogeneousSubmodule R w m`. This is the standard junk-value convention needed to make the set closed under addition.

### Worked examples

- Claim: A polynomial `p : MvPolynomial σ R` belongs to `VTask.weightedHomogeneousSubmodule R w m` if and only if `p.IsWeightedHomogeneous w m`.

- Claim: The product of an element of `VTask.weightedHomogeneousSubmodule R w m` and an element of `VTask.weightedHomogeneousSubmodule R w n` lies in `VTask.weightedHomogeneousSubmodule R w (m + n)`, i.e., the family of these submodules is sub-multiplicative with respect to degree addition.

- Claim: When `w` is the constant weight function `1 : σ → ℕ` (assigning weight 1 to every variable), `VTask.weightedHomogeneousSubmodule R 1 n` coincides with the ordinary homogeneous submodule of total degree `n`.

- Claim: When `σ` is finite and `w : σ → ℕ` assigns a nonzero weight to every variable, the submodule `VTask.weightedHomogeneousSubmodule R w n` is finitely generated as an `R`-module.

### Boundaries

- The zero polynomial is in every `VTask.weightedHomogeneousSubmodule R w m`, for all choices of `w` and `m`, because the zero polynomial has no nonzero monomials and the condition is vacuously satisfied.
- When `m` and `m'` are distinct elements of `M`, the submodules `VTask.weightedHomogeneousSubmodule R w m` and `VTask.weightedHomogeneousSubmodule R w m'` can overlap only in the zero polynomial.
- If the weight function `w` is the zero map (sending every variable to `0 ∈ M`), then the only graded piece that is nontrivial is at degree `0`, and it contains all polynomials (since every monomial then has weighted degree `0`).
- The sum of two polynomials of different weighted homogeneous degrees is generally not in any single `VTask.weightedHomogeneousSubmodule R w m`; the submodule is not closed under addition across different degrees.

### Not to be confused with

- `homogeneousSubmodule σ R n`: the special case where `w` is the constant weight `1` and `M = ℕ`; this is exactly ordinary total-degree homogeneity.
- `IsWeightedHomogeneous w m`: the *predicate* on individual polynomials asserting weighted homogeneity; the submodule here is the carrier set of that predicate packaged as an `R`-submodule.
- `weightedHomogeneousComponent w m`: the *linear projection* from `MvPolynomial σ R` onto `VTask.weightedHomogeneousSubmodule R w m`, not the submodule itself.
