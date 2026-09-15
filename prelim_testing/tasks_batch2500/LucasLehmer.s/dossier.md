## VTask.s

### Object

`VTask.s` is the integer sequence defined by the initial value `s(0) = 4` and the recurrence `s(i+1) = s(i)² − 2`. This is the **Lucas–Lehmer sequence** (over ℤ), whose iterates starting from 4 are the standard test values used in the Lucas–Lehmer primality test for Mersenne numbers. The sequence grows doubly-exponentially: 4, 14, 194, 37634, …

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.s : ℕ → ℤ
<!-- PINNED-SIGNATURE:END -->


`VTask.s : ℕ → ℤ`

The single argument is the (zero-based) index into the sequence. Supplying `0` returns the seed value 4; supplying `i + 1` returns the square of the previous term minus 2.

### Conventions

The sequence is defined for all natural numbers without restriction; there are no junk-value conventions because the function is total on ℕ → ℤ.

### Worked examples

- Claim: VTask.s 0 = 4
  ```lean
  example : VTask.s 0 = 4 := by decide
  ```

- Claim: VTask.s 1 = 14
  ```lean
  example : VTask.s 1 = 14 := by decide
  ```

- Claim: VTask.s 2 = 194
  ```lean
  example : VTask.s 2 = 194 := by decide
  ```

- Claim: VTask.s 3 = 37634
  ```lean
  example : VTask.s 3 = 37634 := by decide
  ```

- Claim: For all i : ℕ, VTask.s i ≥ 4 (the sequence never drops below its seed).

- Claim: The reduction of VTask.s (p − 2) modulo the Mersenne number 2^p − 1 (for prime p ≥ 2) equals 0 if and only if 2^p − 1 is prime (Lucas–Lehmer criterion).

### Boundaries

- At index 0, the sequence returns the seed value 4 exactly, not 0 or 2 (common alternative seeds in similar recurrences).
- The sequence is strictly increasing for all i ≥ 0: each term is at least as large as the previous term squared minus 2, so the sequence diverges to +∞.
- There are no negative values: s(0) = 4 > 2, and if s(i) ≥ 2 then s(i)² − 2 ≥ 2, so positivity is preserved by induction.
- The function is total; it is defined for every natural number index.

### Not to be confused with

- **`LucasLehmer.sMod p`**: the same recurrence taken modulo the Mersenne number 2^p − 1 at each step, yielding bounded non-negative integers rather than the unbounded sequence over ℤ.
- **`LucasLehmer.sZMod p`**: the recurrence computed inside the ring `ZMod (2^p − 1)`, i.e., already reduced mod the Mersenne number, used directly in the primality criterion.
- **Lucas sequences in general**: the broader family of integer linear recurrence sequences parametrised by two integers P and Q; `VTask.s` is the specific instance P = 0, Q = −1 with seed 4 (equivalently, iterating z ↦ z² − 2 from z = 4).