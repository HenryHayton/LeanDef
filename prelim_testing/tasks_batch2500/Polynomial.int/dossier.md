## VTask.int

### Object

Given a field `K`, a subring `R ⊆ K`, and a polynomial `P ∈ K[X]` all of whose coefficients happen to lie in `R`, `VTask.int` produces the corresponding polynomial in `R[X]` — that is, the same formal polynomial reinterpreted as living over the smaller ring `R`. No coefficient is changed; every coefficient is merely re-tagged with the proof that it belongs to `R`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.int : {K : Type u_1} -> [Field K] -> (R : Subring K) -> (P : Polynomial K) -> (hP : ∀ (n : ℕ), P.coeff n ∈ R) -> Polynomial ↥R
<!-- PINNED-SIGNATURE:END -->


The first argument `R` is the subring of `K` that will serve as the coefficient ring of the output polynomial. The second argument `P` is the input polynomial over the field `K`. The third argument `hP` is a proof that for every natural number `n`, the `n`-th coefficient of `P` belongs to `R`; this is the evidence that the reinterpretation is valid.

### Conventions

No special junk-value or edge conventions are declared for this definition: the construction is total and well-behaved for all valid inputs, including the zero polynomial (where every coefficient is zero, which lies in any subring) and constant polynomials.

### Worked examples

- Claim: If `P` is the zero polynomial over `K`, then `VTask.int R P hP` is the zero polynomial over `R`.

- Claim: If `P = C r + X` where `r ∈ R` and `1 ∈ R` (so all coefficients are in `R`), then the polynomial `VTask.int R P hP` has the same support as `P` and its `n`-th coefficient, coerced back to `K`, equals the `n`-th coefficient of `P`.

- Claim: For any `P : K[X]` with `hP : ∀ n, P.coeff n ∈ R`, the degree of `VTask.int R P hP` equals the degree of `P`.

- Claim: For any `P : K[X]` with `hP : ∀ n, P.coeff n ∈ R` and any `n : ℕ`, the coercion of the `n`-th coefficient of `VTask.int R P hP` back into `K` equals `P.coeff n`.

### Boundaries

- **Zero polynomial**: When `P = 0`, every coefficient is `0`, which belongs to any subring. The output is the zero polynomial of `R[X]`.
- **Constant polynomial**: When `P` is a nonzero constant with value in `R`, the output is the corresponding constant polynomial over `R`.
- **Support preservation**: The support (the finite set of indices with nonzero coefficients) is exactly the same for the output as for the input; no coefficients are zeroed out or introduced.
- **Coefficient coercion**: Coercing any coefficient of the output back to `K` via the subring inclusion recovers the original coefficient of `P`.

### Not to be confused with

- `Polynomial.map`: applies a ring homomorphism to the coefficients, potentially changing their values; `VTask.int` only repackages them with a subring membership proof, leaving values unchanged.
- `Polynomial.restriction` or related subtype coercions: those may refer to restricting the variable or the domain in a different sense, not specifically to packaging subring membership for all coefficients simultaneously.
- The canonical inclusion `R →+* K` applied to a polynomial in `R[X]` (which goes the other direction, embedding `R[X]` into `K[X]`): `VTask.int` goes from `K[X]` down to `R[X]`, the reverse direction.
