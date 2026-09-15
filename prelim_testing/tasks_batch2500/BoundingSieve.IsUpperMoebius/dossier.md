## Object

A sequence of real-valued coefficients `muPlus : ℕ → ℝ` is called **upper Möbius** if, when convolved with the constant-1 function (the Dirichlet series analogue of the Riemann zeta function), the result dominates the convolution of the classical Möbius function `μ` with `ζ`. In elementary terms, the defining condition is that for every positive integer `n`, the sum of `muPlus` over all divisors of `n` is at least `1` when `n = 1` and at least `0` for every `n ≠ 1`. This mirrors the fact that the Möbius function satisfies `∑_{d | n} μ(d) = [n = 1]`, so an upper Möbius sequence is one whose divisor sums are everywhere at least as large as those of `μ`. Such sequences provide upper bounds for sifted sums via the Selberg sieve.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsUpperMoebius : (muPlus : ℕ → ℝ) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsUpperMoebius : (muPlus : ℕ → ℝ) -> Prop`

The sole argument `muPlus` is the candidate sequence of sieve coefficients, viewed as a real-valued arithmetic function on the natural numbers, whose upper Möbius property is being asserted.

## Conventions

The natural numbers here include `0`; the divisor sum `n.divisors` in Mathlib is the set of positive divisors of `n`, and for `n = 0` this set is empty, so the divisor sum is `0`. The condition at `n = 0` therefore requires `0 ≥ 0`, which is trivially satisfied, making `n = 0` a vacuous edge case.

## Worked examples

- Claim: The sequence `muPlus` defined by `muPlus 1 = 1` and `muPlus n = 0` for `n ≠ 1` is upper Möbius, since for every `n`, `∑_{d | n} muPlus d` equals `1` if `1 | n` (always true for `n ≥ 1`) and `0` otherwise, matching exactly the indicator `[n = 1]` when `n = 1` and giving `1 ≥ 0` for all `n > 1`.

- Claim: The Selberg `λ²` weights (the lambdaSquared construction) with `weights 1 = 1` satisfy `VTask.IsUpperMoebius (lambdaSquared weights)`, a non-trivial classical fact of sieve theory that gives a usable upper bound for sifted sums.

- Claim: If `muPlus` is upper Möbius, then for any sieve `s`, the sifted sum satisfies `s.siftedSum ≤ ∑ d ∈ divisors s.prodPrimes, muPlus d * s.multSum d`.

## Boundaries

- At `n = 0`: the divisors of `0` in Mathlib form the empty set, so the divisor sum is `0`; the right-hand side of the inequality is `0` (since `0 ≠ 1`), and the condition reduces to `0 ≤ 0`, which is trivially true. Every sequence automatically satisfies the `n = 0` instance.
- At `n = 1`: this is the critical case; the condition requires `∑_{d | 1} muPlus d = muPlus 1 ≥ 1`, so any upper Möbius sequence must satisfy `muPlus 1 ≥ 1`.
- For `n > 1`: the condition requires `∑_{d | n} muPlus d ≥ 0`; the divisor sum can be negative in principle, so this is a genuine constraint even for composite `n`.
- The sequence need not be supported on squarefree integers or satisfy any positivity condition beyond what is implied by the defining inequality.

## Not to be confused with

- **IsLowerMoebius** (if it exists): the analogous condition where the divisor sums are *at most* `[n = 1]`, yielding lower bounds for sifted sums rather than upper bounds.
- **The Möbius function `μ` itself**: `μ` is neither upper nor lower Möbius in this sense (its divisor sums equal `[n = 1]` exactly), but rather the reference point against which the inequality is measured.
- **Multiplicativity**: being upper Möbius does not imply that `muPlus` is a multiplicative arithmetic function; it is a weaker, one-sided condition on divisor sums.