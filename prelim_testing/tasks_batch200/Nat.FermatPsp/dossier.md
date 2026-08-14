## 1. Object

`VTask.FermatPsp n b` is the proposition that `n` is a **Fermat pseudoprime to base `b`**: a composite natural number that nevertheless passes the Fermat primality test for the base `b`. Concretely, `n` must (1) be a *probable prime* to base `b` (meaning `b^(n-1) ≡ 1 (mod n)` in the classical sense, or the appropriate variant adopted by Mathlib), (2) fail to be a prime, and (3) satisfy `n > 1`. Real primes satisfy condition (1) by Fermat's little theorem, so the requirement that `n` be composite is what makes it a *pseudo*prime — a composite impostor.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.FermatPsp : (n b : ℕ) -> Prop
<!-- PINNED-SIGNATURE:END -->


The first argument `n` is the number being tested — the candidate pseudoprime. The second argument `b` is the base with respect to which the Fermat test is applied.

## 3. Conventions

All composite natural numbers greater than 1 are Fermat pseudoprimes to base 0 and to base 1, because the probable-prime condition degenerates in those cases. The definition does **not** require `n ≥ b`; for instance, 4 qualifies as a pseudoprime to base 5. The lower bound `1 < n` is built into the definition, so 0 and 1 are never pseudoprimes regardless of the base.

## 4. Worked Examples

- Claim: `VTask.FermatPsp 4 1` holds — 4 is composite, greater than 1, and every composite number is a probable prime to base 1.
  ```lean
  example : VTask.FermatPsp 4 1 := by decide
  ```

- Claim: `VTask.FermatPsp 9 1` holds — 9 is composite and greater than 1, so it is a pseudoprime to base 1.
  ```lean
  example : VTask.FermatPsp 9 1 := by decide
  ```

- Claim: `¬VTask.FermatPsp 7 2` holds — 7 is prime, so it cannot be a Fermat pseudoprime.
  ```lean
  example : ¬VTask.FermatPsp 7 2 := by decide
  ```

- Claim: `¬VTask.FermatPsp 4 2` — 4 is composite but is not a probable prime to base 2 (since 2^3 = 8 ≡ 0 mod 4, not 1), so it fails.
  ```lean
  example : ¬VTask.FermatPsp 4 2 := by decide
  ```

## 5. Boundaries

- **n = 0 or n = 1**: Never a pseudoprime, because the condition `1 < n` is required.
- **n prime**: Never a pseudoprime regardless of base, because non-primality is required.
- **b = 0**: Every composite `n > 1` satisfies the probable-prime condition (the congruence degenerates), so every composite number greater than 1 is a pseudoprime to base 0.
- **b = 1**: Similarly, every composite number greater than 1 is a pseudoprime to base 1.
- **n < b**: Permitted; for example, 4 is a pseudoprime to base 5.
- **Infinitude**: For every base `b ≥ 1`, there are infinitely many Fermat pseudoprimes to base `b`.

## 6. Not to be confused with

- **`Nat.ProbablePrime n b`**: The weaker condition that `n` merely *passes* the Fermat test for base `b`; it includes actual primes and does not require compositeness.
- **Strong pseudoprimes / Miller–Rabin witnesses**: A stronger compositeness test; `VTask.FermatPsp` uses only the basic Fermat congruence, not the additional square-root checks of the strong version.
- **Carmichael numbers**: Composite numbers that are Fermat pseudoprimes to *every* coprime base; `VTask.FermatPsp` refers to a single fixed base `b`, not all bases simultaneously.