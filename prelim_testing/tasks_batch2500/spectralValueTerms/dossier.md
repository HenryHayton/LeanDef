## Object

For a polynomial `p` over a seminormed ring, `VTask.spectralValueTerms p` is the function `ℕ → ℝ` that assigns to each natural number `n` the value `‖p.coeff n‖^(1/(d − n))` when `n < d` (where `d` is the natural degree of `p`), and the value `0` for every `n ≥ d`. These terms appear as the candidates whose supremum defines the spectral value (also called the spectral radius of a polynomial), a non-Archimedean analogue of the classical Cauchy–Hadamard formula.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.spectralValueTerms : {R : Type u_1} -> [SeminormedRing R] -> (p : Polynomial R) -> ℕ → ℝ
<!-- PINNED-SIGNATURE:END -->


`VTask.spectralValueTerms : {R : Type u_1} -> [SeminormedRing R] -> (p : Polynomial R) -> ℕ → ℝ`

The implicit type argument `R` is the coefficient ring; the instance argument provides the seminorm structure on `R`. The explicit argument `p` is the polynomial whose spectral value terms are being computed. The result is a function on natural numbers, where the input `n` selects the index of the coefficient of `p` to evaluate.

## Conventions

For every index `n` that is at least `p.natDegree`, the term is defined to be `0`. This includes the leading-coefficient index itself (`n = p.natDegree`) and all larger indices, even though `p.coeff n` might formally be nonzero for indices beyond `p.natDegree` in degenerate cases. This zero convention ensures the range is finite and bounded above.

## Worked examples

- Claim: For any polynomial `p` and any `n ≥ p.natDegree`, `VTask.spectralValueTerms p n = 0`.

- Claim: If `p` is a polynomial of natural degree 3 over ℝ with `p.coeff 1 = 8`, then `VTask.spectralValueTerms p 1 = 8^(1/2 : ℝ)`, since `1 < 3` and the exponent is `1/(3 − 1) = 1/2`.

- Claim: For the zero polynomial (which has `natDegree = 0`), `VTask.spectralValueTerms 0 n = 0` for all `n : ℕ`, because `n < 0` is never satisfied.

- Claim: The range of `VTask.spectralValueTerms p` is always a finite set of nonneg reals, for any polynomial `p`.

## Boundaries

- **`n = p.natDegree`**: Returns `0`, not `‖p.coeff d‖^(1/0)`. The condition is strict (`n < p.natDegree`), so the leading term index itself falls in the zero branch. This avoids any division-by-zero issue with the exponent `1/(d − n)` at `n = d`.
- **Zero polynomial**: `p.natDegree = 0`, so the condition `n < 0` is never true; the function is identically `0`.
- **Constant polynomial (nonzero, degree 0)**: Same as the zero polynomial case — all terms are `0`.
- **`n > p.natDegree`**: Also returns `0` by the same branch.
- All values are nonneg reals (norms raised to positive real exponents are nonneg; the zero branch is also nonneg).
- The range is always finite and bounded above.

## Not to be confused with

- **`spectralValue p`**: The supremum of the range of `VTask.spectralValueTerms p`; this is the scalar, not the function producing the terms.
- **`Polynomial.coeff p n`**: The raw coefficient at index `n`, before applying the norm and the fractional power; used as an ingredient but not the same object.
- **Mahler measure terms**: Superficially similar exponential-normed coefficient expressions but arising from a different (Archimedean) theory and with different exponents.
