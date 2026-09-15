## Object

The `n`-th cyclotomic polynomial with coefficients in `R` is the unique monic polynomial whose roots are exactly the primitive `n`-th roots of unity. Over ℤ (or any ring via base change), the `n`-th cyclotomic polynomial Φₙ(X) is characterized by the factorization identity ∏_{d ∣ n} Φ_d(X) = Xⁿ − 1. For n ≥ 1 over ℤ, it has degree φ(n) (Euler's totient function), integer coefficients, and is irreducible over ℚ.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.cyclotomic : (n : ℕ) -> (R : Type u_1) -> [Ring R] -> Polynomial R
<!-- PINNED-SIGNATURE:END -->


`VTask.cyclotomic : (n : ℕ) -> (R : Type u_1) -> [Ring R] -> Polynomial R`

The first argument `n` is the index of the cyclotomic polynomial — it selects which Φₙ is produced. The second argument `R` is the coefficient ring in which the polynomial is expressed; it must carry a `Ring` structure (supplied by the instance argument). The result is a polynomial over `R`.

## Conventions

When `n = 0`, the 0th cyclotomic polynomial is defined to be the constant polynomial `1` (the multiplicative identity in `R[X]`). This is a junk value convention: there is no standard mathematical meaning for Φ₀, so the definition returns `1` as a convenient sentinel rather than leaving the function partial.

## Worked examples

- Claim: `VTask.cyclotomic 0 ℤ = 1` (the zero-index case yields the constant polynomial 1)
- Claim: `VTask.cyclotomic 1 ℤ = X - 1` (Φ₁ = X − 1, the minimal polynomial of the trivial root of unity 1)
- Claim: `VTask.cyclotomic 2 ℤ = X + 1` (Φ₂ = X + 1, the minimal polynomial of −1)
- Claim: `VTask.cyclotomic 4 ℤ = X^2 + 1` (Φ₄ = X² + 1, the minimal polynomial of i = √(−1))
- Claim: `VTask.cyclotomic 6 ℤ = X^2 - X + 1` (Φ₆ = X² − X + 1, degree φ(6) = 2)
- Claim: The degree of `VTask.cyclotomic n ℤ` equals `Nat.totient n` for every `n ≥ 1`.
- Claim: The product ∏_{d ∣ n} `VTask.cyclotomic d R` equals `X^n - 1` in `R[X]` for every `n ≥ 1` and any commutative ring `R`.

## Boundaries

- **n = 0**: Returns the constant polynomial `1` by convention (junk value; no standard mathematical definition exists here).
- **n = 1**: Returns `X − 1`, which is degree 1 with the single root 1 (the unique primitive 1st root of unity).
- **n = 2**: Returns `X + 1`, degree 1.
- **General n ≥ 1**: Returns a monic polynomial of degree φ(n) with integer coefficients (cast into R), whose complex roots are exactly the primitive n-th roots of unity e^(2πik/n) with gcd(k, n) = 1.
- **Coefficient ring R**: The polynomial is obtained by mapping the integer-coefficient cyclotomic polynomial along the unique ring homomorphism ℤ → R. Thus properties of the polynomial (e.g., irreducibility) may change depending on R, but the combinatorial/factorization structure is inherited from ℤ.

## Not to be confused with

- `Polynomial.X ^ n - 1` — this is Xⁿ − 1, the product of all cyclotomic polynomials Φ_d for d ∣ n, not a single cyclotomic factor.
- The minimal polynomial of a specific root of unity — while Φₙ is the minimal polynomial of a primitive n-th root of unity over ℚ, the construction here is ring-generic and not phrased in terms of minimal polynomials.
- `IsPrimitiveRoot` — this is the predicate asserting that a specific ring element is a primitive n-th root of unity; it is used internally in the construction but is distinct from the polynomial itself.