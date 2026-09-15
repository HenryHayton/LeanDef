## Object

`VTask.order φ` is the **order** (also called the *valuation*) of a formal power series `φ` over a semiring `R`. It is the largest extended natural number `n : ℕ∞` such that `X^n` divides `φ` in the ring of formal power series — equivalently, the index of the first nonzero coefficient of `φ`. When `φ` is the zero series (all coefficients zero), no finite such bound exists and the order is defined to be `⊤` (infinity in `ℕ∞`).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.order : {R : Type u_1} -> [Semiring R] -> (φ : PowerSeries R) -> ℕ∞
<!-- PINNED-SIGNATURE:END -->


`VTask.order : {R : Type u_1} -> [Semiring R] -> (φ : PowerSeries R) -> ℕ∞`

The implicit argument `R` is the coefficient ring; it is inferred automatically. The instance argument supplies the semiring structure on `R`. The explicit argument `φ` is the formal power series whose order is being computed. The result lives in `ℕ∞`, the extended natural numbers, to accommodate the special value `⊤` for the zero series.

## Conventions

The order of the zero formal power series is `⊤` (the top element of `ℕ∞`), not any finite natural number; this is the unique junk/edge convention. For every nonzero series, the order is a finite element `(n : ℕ)` embedded in `ℕ∞`, equal to the smallest index `n` for which the `n`-th coefficient is nonzero.

## Worked examples

- Claim: The order of the zero power series over `ℤ` is `⊤`.

- Claim: The order of the constant series `1` (i.e., the series with constant term 1 and all other coefficients 0) is `0`, since the 0th coefficient is nonzero.

- Claim: The order of `X` (the series with coefficient 1 in degree 1 and 0 elsewhere) is `1`, since the first nonzero coefficient appears at index 1.

- Claim: The order of `X^3` as a power series over `ℤ` is `3`.

- Claim: For two nonzero power series `φ` and `ψ` over an integral domain, `VTask.order (φ * ψ) = VTask.order φ + VTask.order ψ`.

## Boundaries

- **Zero series**: `VTask.order 0 = ⊤`. This is the defining edge case; the order is not a finite natural number.
- **Nonzero constant series**: If `c ≠ 0` in `R`, then `VTask.order (C c) = 0` because the 0th coefficient is nonzero.
- **Powers of X**: `VTask.order (X^n) = n` for any `n : ℕ`, since the only nonzero coefficient is at index `n`.
- **Addition**: In general, `VTask.order (φ + ψ) ≥ min (VTask.order φ) (VTask.order ψ)`, with equality when the orders differ; if the orders are equal, cancellation of leading terms can raise the order.
- **The result type is `ℕ∞`**: arithmetic on `ℕ∞` uses the conventions that `n + ⊤ = ⊤` and `⊤ + ⊤ = ⊤`, consistent with the order of the zero series being `⊤`.

## Not to be confused with

- **`multiplicity`**: a more general notion of `p`-adic valuation for elements of a monoid; `VTask.order` is the special case for formal power series where the "prime" is `X`.
- **`PowerSeries.coeff R n φ`**: this extracts the individual coefficient of degree `n` in `φ`, rather than finding the smallest nonzero index.
- **`Polynomial.natDegree`**: the degree of a polynomial, which is the *largest* nonzero coefficient index, not the smallest; and it lives in `ℕ` rather than `ℕ∞`.