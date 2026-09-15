## Object

Given a polynomial `p` over a semiring `R`, `VTask.nextCoeffUp p` returns the coefficient of the monomial one degree above the trailing (lowest-degree nonzero) term of `p`. If `p` is a constant polynomial (including the zero polynomial), the result is `0`. Informally, if the lowest nonzero term of `p` has degree `d > 0`, then `VTask.nextCoeffUp p` is the coefficient of degree `d + 1`; if `p` has no nonzero term below degree 1 (i.e., `p` is a constant), the result is `0`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.nextCoeffUp : {R : Type u} -> [Semiring R] -> (p : Polynomial R) -> R
<!-- PINNED-SIGNATURE:END -->


`VTask.nextCoeffUp : {R : Type u} -> [Semiring R] -> (p : Polynomial R) -> R`

The implicit type argument `R` is the coefficient semiring. The typeclass argument `[Semiring R]` supplies the semiring structure (in particular the zero element used as the fallback value). The explicit argument `p` is the polynomial whose second-lowest coefficient is being extracted.

## Conventions

For constant polynomials — including the zero polynomial — where the natural trailing degree is 0, the function returns `0` (the zero of `R`), regardless of whether any nonzero constant term is present. This is a junk-value convention: constants do not have a "second-lowest" coefficient in the intended sense, so `0` is returned.

## Worked examples

- Claim: For the zero polynomial (over ℕ), `VTask.nextCoeffUp 0 = 0`, since the zero polynomial is treated as a constant.

- Claim: For the constant polynomial `3` (over ℕ), `VTask.nextCoeffUp (Polynomial.C 3) = 0`, because the natural trailing degree is 0 and the constant-branch applies.

- Claim: For the polynomial `X^2 + 5*X + 7` over ℕ, the trailing degree is 0 (the constant term `7` is nonzero), so `VTask.nextCoeffUp` returns `0`.

- Claim: For the polynomial `2*X^3 + 9*X^2` over ℕ, the trailing degree is 2 (the `X^2` term is the lowest nonzero term), so `VTask.nextCoeffUp` returns the coefficient of `X^3`, which is `2`.

- Claim: For the monomial `X` (i.e., the polynomial `X^1`) over ℕ, the trailing degree is 1, so `VTask.nextCoeffUp` returns the coefficient of `X^2`, which is `0`.

## Boundaries

- **Zero polynomial**: `natTrailingDegree` of the zero polynomial is `0`, so the function returns `0` via the constant branch.
- **Nonzero constant**: A nonzero constant `C c` also has `natTrailingDegree = 0`, so the function returns `0`, not `c` itself.
- **Monomial**: A pure monomial `a * X^n` with `n ≥ 1` has trailing degree `n`, so the function returns the coefficient of `X^{n+1}`, which is `0` if there is no `X^{n+1}` term.
- **Linear polynomial `a*X + b` with `b ≠ 0`**: Trailing degree is `0`, so the function returns `0` (not `a`).
- **Linear polynomial `a*X` with `a ≠ 0`**: Trailing degree is `1`, so the function returns the coefficient of `X^2`, which is `0`.

## Not to be confused with

- `Polynomial.nextCoeff`: Returns the coefficient one above the *leading* (highest-degree) term, not the trailing term.
- `Polynomial.coeff p (p.natTrailingDegree)`: Returns the *trailing* (lowest-degree nonzero) coefficient itself, not the one above it.
- `Polynomial.trailingCoeff`: Also returns the trailing coefficient (the leading coefficient of the reversed polynomial), not the second-lowest.