## Object

`VTask.padicValuation p` is the *p-adic valuation* on the field of rational numbers ℚ, packaged as a Mathlib `Valuation` taking values in the multiplicative monoid `WithZero (Multiplicative ℤ)` (often written ℤᵐ⁰). Concretely, a nonzero rational number `x` is sent to `exp(−v_p(x))`, where `v_p(x)` is the usual p-adic valuation integer (the exponent of p in the factored form of x); the zero rational is sent to the absorbing zero element of ℤᵐ⁰. The map is a ring valuation: it is multiplicative, sends 0 to 0 and 1 to 1, and satisfies the ultrametric (non-Archimedean) triangle inequality `v(x + y) ≤ max(v(x), v(y))`.

In particular, p itself maps to `exp(−1)`, a generator of the value group; elements whose p-adic valuation is non-negative (i.e., p does not appear in the denominator) map to values ≤ 1; and the valuation equals 0 exactly when x = 0.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.padicValuation : (p : ℕ) -> [Fact (Nat.Prime p)] -> Valuation ℚ (WithZero (Multiplicative ℤ))
<!-- PINNED-SIGNATURE:END -->


`(p : ℕ) -> [Fact (Nat.Prime p)] -> Valuation ℚ (WithZero (Multiplicative ℤ))`

The first argument `p` is the prime that determines the valuation: the measure of divisibility by p. The instance argument `[Fact (Nat.Prime p)]` is the proof that p is indeed a prime number, supplied via Lean's `Fact` wrapper so it can be inferred from the local context; it ensures the construction is only available for primes.

## Conventions

The value at zero is the distinguished absorbing element `0` of `WithZero (Multiplicative ℤ)`, not an integer or `⊥`; this is the standard junk/edge convention for ring valuations in Mathlib. No other junk-value conventions are declared.

## Worked examples

- Claim: `VTask.padicValuation 5` sends `5 : ℚ` to `exp (-1)` in ℤᵐ⁰, i.e., the 5-adic valuation of 5 itself is the canonical generator.

- Claim: `VTask.padicValuation 2` sends `0 : ℚ` to `0` in ℤᵐ⁰ (the valuation of zero is zero, the absorbing element).

- Claim: `VTask.padicValuation 3` sends `1 : ℚ` to `1` in ℤᵐ⁰ (units map to the multiplicative identity).

- Claim: `VTask.padicValuation 2` is surjective onto ℤᵐ⁰, because every element of the value group is realised by some rational; formally `Function.Surjective (VTask.padicValuation 2)`.

## Boundaries

- **At zero:** `VTask.padicValuation p 0 = 0` (the zero element of ℤᵐ⁰), consistent with the general valuation axiom that the value of zero is the additive zero of the value monoid.
- **At p itself:** `VTask.padicValuation p (p : ℚ) = exp (-1)`, confirming p is mapped to a strict generator below 1 in the ordered monoid.
- **At units not divisible by p:** any rational whose numerator and denominator are both coprime to p maps to `1` (the multiplicative identity), i.e., the valuation is `≤ 1`; specifically `VTask.padicValuation p x ≤ 1 ↔ p ∤ x.den`.
- **Injectivity/surjectivity:** The valuation is surjective onto ℤᵐ⁰ (every value is achieved), but is far from injective — all rationals with the same p-adic exponent are in the same level set.
- **Non-primality:** The `Fact (Nat.Prime p)` hypothesis is mandatory; the definition does not apply to composite or zero n.

## Not to be confused with

- `padicValRat p x : ℤ` — the raw integer-valued p-adic valuation of a rational (the exponent in the factorisation), which is a plain function rather than a bundled `Valuation` structure and is undefined/junk at zero.
- `Int.padicValuation p` — the analogous bundled valuation on ℤ rather than ℚ; it agrees with `VTask.padicValuation p` after casting integers to rationals.
- `Padic.mulValuation` — the multiplicative valuation on the p-adic completion ℚ_p rather than on ℚ itself; its restriction (comap) along the canonical embedding equals `VTask.padicValuation p`.
