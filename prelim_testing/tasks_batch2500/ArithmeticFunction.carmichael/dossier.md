## VTask.carmichael

### Object

The Carmichael function (also called the reduced totient function or Korselt's lambda function) is the arithmetic function λ : ℕ → ℕ that assigns to each positive integer n the **exponent** of the multiplicative group of integers modulo n — that is, the smallest positive integer m such that a^m ≡ 1 (mod n) for every integer a coprime to n. It is the analogue of Euler's totient function φ(n), but where φ(n) is the *order* of the unit group (ZMod n)ˣ, λ(n) is the *exponent* of that group (the lcm of all element orders rather than their count). By convention λ(0) = 0.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.carmichael : ArithmeticFunction ℕ
<!-- PINNED-SIGNATURE:END -->


`VTask.carmichael : ArithmeticFunction ℕ`

This is a nullary constant — a single arithmetic function ℕ → ℕ with the extra structure of an `ArithmeticFunction` (which requires the value at 0 to be 0). There are no arguments to describe beyond the implicit natural-number index at which the function is evaluated when written `VTask.carmichael n`.

### Conventions

The value at 0 is defined to be 0 by convention, even though 0 has no multiplicative group of integers in the usual sense; this is the standard junk value required by the `ArithmeticFunction` typeclass.

### Worked examples

- Claim: VTask.carmichael 0 = 0 (the conventional junk value).

- Claim: VTask.carmichael 1 = 1, because the unit group of ZMod 1 is trivial and the exponent of the trivial group is 1.

- Claim: VTask.carmichael 6 = 2, because the units of ZMod 6 are {1, 5} ≅ ℤ/2ℤ, so every unit squares to 1.

- Claim: VTask.carmichael 12 = 2, because the unit group of ZMod 12 is (ℤ/2ℤ)², whose exponent is 2, while φ(12) = 4.

- Claim: VTask.carmichael 5 = 4, because ZMod 5 is a field with cyclic unit group of order 4, whose exponent equals its order.

- Claim: For every prime p, VTask.carmichael p = p - 1, since (ZMod p)ˣ is cyclic of order p − 1, so its exponent equals its order (which also equals the totient).

- Claim: VTask.carmichael (2^3) = 2, because 2^(3-2) = 2; for powers of 2 that are ≥ 8 the unit group is ℤ/2ℤ × ℤ/2^(n−2)ℤ whose exponent is 2^(n−2), exactly half the totient.

### Boundaries

- **n = 0**: Returns 0 by the `ArithmeticFunction` convention; this is a junk value with no number-theoretic meaning.
- **n = 1**: The unit group of ZMod 1 is trivial, so the exponent is 1; `VTask.carmichael 1 = 1`.
- **n = 2**: (ZMod 2)ˣ is trivial, so `VTask.carmichael 2 = 1`.
- **Powers of 2**: The behaviour splits at n = 1, 2 (where λ(2^n) = φ(2^n)) versus n ≥ 3 (where λ(2^n) = 2^(n−2) = φ(2^n)/2).
- **Prime powers p^k (p odd prime)**: λ(p^k) = φ(p^k) = p^(k−1)(p−1), since the unit group is cyclic.
- **General n**: λ(n) divides φ(n), and the two are equal exactly when the unit group of ZMod n is cyclic (i.e., n = 1, 2, 4, p^k, or 2p^k for odd prime p).
- **Multiplicativity**: For coprime a, b, λ(ab) = lcm(λ(a), λ(b)); more generally λ(lcm(a,b)) = lcm(λ(a), λ(b)).

### Not to be confused with

- **`Nat.totient` (Euler's φ function)**: φ(n) counts units mod n (order of the group), while λ(n) is their universal exponent; λ(n) always divides φ(n) but can be strictly smaller.
- **The Charmichael numbers (Carmichael numbers)**: These are composite integers n satisfying a^(n−1) ≡ 1 mod n for all a coprime to n; they are defined in terms of the Carmichael *function* (λ(n) | n−1) but are a different object.
- **`ArithmeticFunction.sigma` or other standard multiplicative functions**: Those are fully multiplicative or multiplicative with respect to products, not the lcm-multiplicativity that the Carmichael function satisfies.
