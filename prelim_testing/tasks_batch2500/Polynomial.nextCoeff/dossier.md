## Object

`VTask.nextCoeff p` returns the coefficient of the second-highest degree term of the polynomial `p`, i.e., the coefficient of `X^(deg p − 1)`. For constant polynomials (including the zero polynomial), where there is no "second-highest" term in a meaningful sense, the value is defined to be `0`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.nextCoeff : {R : Type u} -> [Semiring R] -> (p : Polynomial R) -> R
<!-- PINNED-SIGNATURE:END -->


The single argument `p` is a polynomial over the semiring `R` whose second-highest coefficient is being extracted. The semiring instance is implicit and inferred from context.

## Conventions

When `p` has natural degree 0 (i.e., `p` is a constant polynomial or the zero polynomial), `VTask.nextCoeff p` is defined to be `0`, the additive identity of `R`, rather than raising an error or being left undefined.

## Worked examples

- Claim: For the polynomial `X^2 + 3*X + 5` over `ℤ`, `VTask.nextCoeff` returns `3`, the coefficient of `X`.

- Claim: For the constant polynomial `7` (natDegree = 0), `VTask.nextCoeff` returns `0`.

- Claim: For the zero polynomial (natDegree = 0), `VTask.nextCoeff` returns `0`.

- Claim: For a monic polynomial of degree `n ≥ 1`, `VTask.nextCoeff p` equals `p.coeff (n - 1)`, the actual penultimate coefficient.

## Boundaries

- **Zero polynomial**: `natDegree` of the zero polynomial is `0`, so `VTask.nextCoeff 0 = 0` (falls into the constant-branch case).
- **Constant non-zero polynomial**: `natDegree` is `0`, so `VTask.nextCoeff c = 0` for any constant `c`, even though `c` itself may be non-zero.
- **Linear polynomial** (degree 1): `VTask.nextCoeff p = p.coeff 0`, the constant term, since `natDegree - 1 = 0`.
- **Degree ≥ 2**: `VTask.nextCoeff p = p.coeff (natDegree p - 1)`, the genuine penultimate coefficient.

## Not to be confused with

- `Polynomial.leadingCoeff`: returns the leading (highest-degree) coefficient `p.coeff (p.natDegree)`, not the second-highest.
- `Polynomial.coeff p n`: returns the coefficient of `X^n` for an arbitrary index `n`; `VTask.nextCoeff` specifically targets index `natDegree p - 1` with a fallback of `0`.
- `Polynomial.nextCoeffUp`: not a standard object, but easy to confuse directionally — `VTask.nextCoeff` looks one step *below* the leading term, not above it.