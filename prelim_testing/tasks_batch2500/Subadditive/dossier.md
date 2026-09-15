## VTask.Subadditive

### Object

A predicate on real-valued sequences indexed by the natural numbers. A sequence `u : ℕ → ℝ` is called **subadditive** if, for every pair of non-negative integers `m` and `n`, the value of `u` at their sum is no greater than the sum of the individual values: `u(m + n) ≤ u(m) + u(n)`. This is the standard notion of subadditivity for sequences, appearing prominently in ergodic theory, combinatorics, and the study of growth rates.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Subadditive : (u : ℕ → ℝ) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Subadditive : (u : ℕ → ℝ) -> Prop`

The single argument `u` is the real-valued sequence being tested for subadditivity; it maps each natural number index to a real number.

### Conventions

No special junk-value or boundary conventions are declared: the predicate is a universally quantified statement over all pairs `m, n : ℕ`, so it is well-defined for every function `u : ℕ → ℝ` with no edge-case treatment required.

### Worked examples

- Claim: The zero sequence `u n = 0` is subadditive, since `0 ≤ 0 + 0` for all `m, n`.

- Claim: The sequence `u n = -n` (i.e., `u n = -(n : ℝ)`) is subadditive, because `-(m + n) = -m + (-n)` so equality holds, satisfying `≤`.

- Claim: The constant sequence `u n = 1` is **not** subadditive in general, since `u(1 + 1) = 1` but `u 1 + u 1 = 2`, and `1 ≤ 2` holds — actually it is subadditive whenever the constant `c` satisfies `c ≤ 2c`, i.e. `0 ≤ c`; the constant sequence `u n = -1` fails because `u(1+1) = -1` while `u 1 + u 1 = -2`, giving `-1 ≤ -2` which is false.

- Claim: The sequence `u n = (n : ℝ)` is subadditive (in fact additive), since `m + n ≤ m + n` holds with equality.

### Boundaries

- The quantifier ranges over **all** `m n : ℕ`, including `m = 0` or `n = 0`. In particular, `u 0 ≤ u 0 + u 0` (taking `m = n = 0`) implies `u 0 ≥ 0` when `VTask.Subadditive u` holds (i.e., `0 ≤ u 0`); more precisely, from `m = n = 0` we get `u 0 ≤ 2 · u 0`, which forces `u 0 ≥ 0`.
- The definition places no restriction on the sign or growth rate of `u` beyond the subadditivity inequality itself.
- Because the domain is `ℕ` (not `ℤ`), negative indices do not arise and the predicate is total.

### Not to be confused with

- **Superadditivity**: the reversed inequality `u m + u n ≤ u (m + n)`; a sequence satisfying both would be additive.
- **`IsSigmaSubadditive` (measure-theoretic)**: a sigma-subadditivity condition for set functions over countable unions, which is an entirely different (measure-theoretic) notion despite the similar name.
- **Subadditivity for functions on a monoid or group**: the same inequality concept but stated for domains other than `ℕ`; `VTask.Subadditive` is specifically for sequences indexed by natural numbers.