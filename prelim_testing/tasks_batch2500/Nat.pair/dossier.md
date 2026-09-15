## Object

`VTask.pair` is the Cantor-style pairing function on the natural numbers: a computable bijection that encodes any ordered pair of natural numbers `(a, b)` as a single natural number. The encoding depends on whether `a < b` or not, placing pairs along diagonals of the infinite grid ℕ × ℕ, and is left-inverse to the corresponding unpairing function.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pair : (a b : ℕ) -> ℕ
<!-- PINNED-SIGNATURE:END -->


`VTask.pair : (a b : ℕ) -> ℕ`

The first argument `a` is the left component of the pair to be encoded. The second argument `b` is the right component of the pair to be encoded. Both are arbitrary natural numbers with no restriction.

## Conventions

The function is total with no junk values: every natural number in the codomain is the encoding of exactly one pair, and every pair `(a, b)` is assigned a well-defined value. There are no special sentinel or edge-case conventions beyond the definition's natural casework.

## Worked examples

- Claim: VTask.pair 0 0 = 0
  ```lean
  example : VTask.pair 0 0 = 0 := by decide
  ```

- Claim: VTask.pair 2 5 = 27  (since 2 < 5, the result is 5 * 5 + 2 = 27)
  ```lean
  example : VTask.pair 2 5 = 27 := by decide
  ```

- Claim: VTask.pair 5 2 = 32  (since 5 ≥ 2, the result is 5 * 5 + 5 + 2 = 32)
  ```lean
  example : VTask.pair 5 2 = 32 := by decide
  ```

- Claim: VTask.pair 3 3 = 15  (since 3 is not < 3, the result is 3 * 3 + 3 + 3 = 15)
  ```lean
  example : VTask.pair 3 3 = 15 := by decide
  ```

- Claim: VTask.pair 0 1 = 1  (since 0 < 1, the result is 1 * 1 + 0 = 1)
  ```lean
  example : VTask.pair 0 1 = 1 := by decide
  ```

## Boundaries

- When `a = b`: the function uses the branch `a * a + a + b = a * a + 2 * a` (the non-strict branch), since `a < b` is false.
- When `a = 0, b = 0`: the result is 0, the minimum possible output.
- When `a < b`: the result is `b * b + a`, which is strictly less than `b * b + b = b * (b + 1)`, lying on the `b`-th anti-diagonal row.
- When `a ≥ b`: the result is `a * a + a + b`, which is at least `a * a + a`, lying on the `a`-th diagonal column segment.
- The function is injective: `VTask.pair a b = VTask.pair a' b'` implies `a = a'` and `b = b'`.
- The function is surjective (together with `Nat.unpair`): for every `n`, `VTask.pair (Nat.unpair n).1 (Nat.unpair n).2 = n`.

## Not to be confused with

- `Nat.unpair`: the inverse operation that decodes a single natural number back into a pair `(a, b)` — this is the left inverse of `VTask.pair`.
- `Nat.pairwise_coprime_pow_primeFactors_factorization`: a completely unrelated lemma about coprimality of prime power factors, which merely shares the word "pair" in its name.
- The Szudzik or Hopcroft–Ullman pairing functions: other bijections ℕ × ℕ → ℕ that use different formulas and produce different encodings for the same input pairs.