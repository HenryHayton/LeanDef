## Object

`VTask.liouville` is the Liouville lambda function λ : ℕ → ℤ, a classical number-theoretic arithmetic function that assigns to each positive integer `n` the value `(−1)^Ω(n)`, where Ω(n) is the number of prime factors of `n` counted with multiplicity. Concretely, λ(n) = 1 when `n` has an even total number of prime factors (including repetitions), and λ(n) = −1 when `n` has an odd total number. By convention the value at 0 is defined to be 0.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.liouville : ArithmeticFunction ℤ
<!-- PINNED-SIGNATURE:END -->


`VTask.liouville : ArithmeticFunction ℤ`

This is a nullary declaration — it takes no arguments. It is a complete arithmetic function from the natural numbers to the integers, packaged as a member of the type `ArithmeticFunction ℤ` (which bundles the underlying function together with the requirement that it maps 0 to 0).

## Conventions

The value at 0 is defined to be 0. This is a junk value: 0 is not a positive integer and does not participate in multiplicative number theory; the convention exists solely to satisfy the `ArithmeticFunction` interface, which requires `map_zero' : f 0 = 0`.

## Worked examples

- Claim: `VTask.liouville 1 = 1`, because 1 has zero prime factors (an even count), so (−1)^0 = 1.

- Claim: `VTask.liouville 2 = -1`, because 2 is prime (one prime factor), so (−1)^1 = −1.

- Claim: `VTask.liouville 4 = 1`, because 4 = 2² has two prime factors counted with multiplicity, so (−1)^2 = 1.

- Claim: `VTask.liouville 12 = 1`, because 12 = 2² · 3 has three prime factors counted with multiplicity, giving (−1)^3 = −1... wait: Ω(12) = 3, so λ(12) = −1. Corrected: `VTask.liouville 12 = -1`.

- Claim: `VTask.liouville 0 = 0`, the junk value at zero.

- Claim: `VTask.liouville` is multiplicative, meaning `VTask.liouville (m * n) = VTask.liouville m * VTask.liouville n` for all natural numbers `m` and `n` (even when `m` or `n` is 0).

## Boundaries

- **At n = 0**: the function returns 0. This is a junk value introduced to satisfy the `ArithmeticFunction` interface and has no number-theoretic meaning.
- **At n = 1**: Ω(1) = 0 (no prime factors), so λ(1) = (−1)^0 = 1. This is consistent with multiplicativity (the empty product).
- **At prime p**: Ω(p) = 1, so λ(p) = −1 for every prime.
- **At prime powers p^k**: Ω(p^k) = k, so λ(p^k) = (−1)^k.
- **Non-vanishing**: for every positive integer `n ≠ 0`, λ(n) ≠ 0; in fact λ(n) ∈ {1, −1}.
- **Complete multiplicativity**: λ(mn) = λ(m)λ(n) for all natural numbers m, n (not only coprime ones), which is stronger than ordinary multiplicativity.

## Not to be confused with

- **Möbius function `μ`**: also takes values in {−1, 0, 1}, but equals 0 on non-squarefree integers and counts prime factors without multiplicity for squarefree inputs; not completely multiplicative.
- **`ArithmeticFunction.cardFactors` (Ω)**: the raw count Ω(n) of prime factors with multiplicity; `VTask.liouville n = (−1)^(cardFactors n)` for n ≠ 0, so cardFactors is the exponent, not the Liouville function itself.
- **Von Mangoldt function `Λ`**: another arithmetic function used in prime counting, taking real (or complex) values; completely unrelated to the ±1 Liouville function despite sharing initial-letter notation in some texts.
