## VTask.aevalTower

### Object

`VTask.aevalTower f X` is the unique algebra homomorphism from `MvPolynomial σ R` to `A` that is `S`-linear, sends each variable `i : σ` to the element `X i ∈ A`, and extends the `S`-algebra map `f : R →ₐ[S] A` on coefficients. It is the "tower" variant of multivariate polynomial evaluation: instead of requiring `A` to be an `R`-algebra directly, it only requires a common base `S` together with an explicit `S`-algebra map `f` from `R` to `A`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.aevalTower : {R : Type u} -> {σ : Type u_1} -> [CommSemiring R] -> {S : Type u_2} -> {A : Type u_3} -> [CommSemiring S] -> [CommSemiring A] -> [Algebra S R] -> [Algebra S A] -> (f : R →ₐ[S] A) -> (X : σ → A) -> MvPolynomial σ R →ₐ[S] A
<!-- PINNED-SIGNATURE:END -->


VTask.aevalTower : {R : Type u} -> {σ : Type u_1} -> [CommSemiring R] -> {S : Type u_2} -> {A : Type u_3} -> [CommSemiring S] -> [CommSemiring A] -> [Algebra S R] -> [Algebra S A] -> (f : R →ₐ[S] A) -> (X : σ → A) -> MvPolynomial σ R →ₐ[S] A

`R` is the coefficient ring of the multivariate polynomials. `σ` is the index type for the indeterminates. `S` is the smaller base ring that sits below both `R` and `A` via algebra structures. `A` is the target algebra. The argument `f` is an `S`-algebra homomorphism from `R` to `A`, specifying how coefficients are mapped. The argument `X` is a function assigning to each indeterminate `i : σ` a chosen evaluation point `X i` in `A`. The result is the induced `S`-algebra homomorphism from `MvPolynomial σ R` to `A`.

### Conventions

There are no junk-value or edge conventions to declare: the construction is total and well-defined for any valid inputs satisfying the typeclass constraints, including the degenerate cases noted in Boundaries.

### Worked examples

- Claim: Evaluating the polynomial `X 0 + C 1` via `aevalTower id (fun _ => 2)` over `ℤ` (with `S = R = A = ℤ`, `f = id`, single variable mapped to `2`) yields `3`.

- Claim: When `σ` is empty (no variables), `VTask.aevalTower f X` applied to a constant polynomial `C r` equals `f r`.

- Claim: When `f` is the identity map on `R` and `X` maps each variable to itself (the canonical inclusion into `MvPolynomial σ R`), `VTask.aevalTower (AlgHom.id S R) (fun i => MvPolynomial.X i)` is the identity algebra homomorphism on `MvPolynomial σ R`.

- Claim: `VTask.aevalTower f X` composed appropriately with the constant-polynomial embedding `C` recovers `f`; that is, for any `r : R`, `(VTask.aevalTower f X) (MvPolynomial.C r) = f r`.

### Boundaries

- If `σ` is the empty type, there are no variables and every polynomial is a constant; the homomorphism reduces to composition with `f` through the coefficient map.
- If `f` is the zero map (when the target algebra admits one), all coefficients are sent to zero, so every polynomial evaluates to `0` regardless of `X`.
- If `A = R` and `f = AlgHom.id S R` (the identity), the result recovers the standard multivariate polynomial evaluation map where only the variable substitution `X` matters.
- The definition is valid even when `σ` is an infinite type; the polynomial ring `MvPolynomial σ R` consists of finitely-supported monomials, so the infinite image of `X` causes no convergence issues.

### Not to be confused with

- `MvPolynomial.aeval`: the standard evaluation map `MvPolynomial σ R →ₐ[R] A`, which requires `A` to be an `R`-algebra directly and does not accept a separate coefficient map `f`.
- `MvPolynomial.eval₂`: a ring homomorphism (not an algebra homomorphism) version of two-argument evaluation, lacking the `S`-algebra structure on the result.
- `Polynomial.aevalTower`: the single-variable analogue for `Polynomial R` rather than `MvPolynomial σ R`.
