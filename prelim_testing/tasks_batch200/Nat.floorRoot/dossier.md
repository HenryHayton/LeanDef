## Object

`VTask.floorRoot n a` computes the **floor n-th root** of a natural number `a` in the sense of divisibility: it returns the largest natural number `r` (up to divisibility) such that `r ^ n` divides `a`. Concretely, if `a` has prime factorization `p₁^k₁ · p₂^k₂ · …`, then `VTask.floorRoot n a = p₁^⌊k₁/n⌋ · p₂^⌊k₂/n⌋ · …` — each prime's exponent is floored by dividing by `n`. This is the upper (right) adjoint of the power map `a ↦ a ^ n` on `ℕ` ordered by divisibility.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.floorRoot : (n a : ℕ) -> ℕ
<!-- PINNED-SIGNATURE:END -->


VTask.floorRoot : (n a : ℕ) -> ℕ

The first argument `n` is the **degree** of the root being taken (e.g., `n = 2` for a square root, `n = 3` for a cube root). The second argument `a` is the **natural number** whose floor n-th root (in the divisibility sense) is being computed.

## Conventions

When the degree `n` is zero, the result is defined to be `0` (a junk value ensuring the adjunction `a ^ n ∣ b ↔ a ∣ VTask.floorRoot n b` holds as broadly as possible). When the input `a` is zero, the result is also defined to be `0` (again a junk/edge-case convention ensuring the adjunction is not violated at zero).

## Worked examples

- Claim: `VTask.floorRoot 2 (2^3 * 3^2 * 5) = 2 * 3` — taking the floor square root of `2³·3²·5` gives `2^⌊3/2⌋ · 3^⌊2/2⌋ · 5^⌊1/2⌋ = 2¹ · 3¹ · 5⁰ = 6`.
  ```lean
  example : VTask.floorRoot 2 (2^3 * 3^2 * 5) = 2 * 3 := by native_decide
  ```

- Claim: `VTask.floorRoot 3 (2^6 * 5^4) = 2^2 * 5` — taking the floor cube root of `2⁶·5⁴` gives `2^⌊6/3⌋ · 5^⌊4/3⌋ = 4 · 5 = 20`.
  ```lean
  example : VTask.floorRoot 3 (2^6 * 5^4) = 2^2 * 5 := by native_decide
  ```

- Claim: `VTask.floorRoot 2 36 = 6` — the floor square root of 36 = 2²·3² is 2·3 = 6, since ⌊2/2⌋ = 1 for each prime.
  ```lean
  example : VTask.floorRoot 2 36 = 6 := by native_decide
  ```

- Claim: `VTask.floorRoot 2 12 = 2` — the floor square root of 12 = 2²·3 is 2^⌊2/2⌋ · 3^⌊1/2⌋ = 2·1 = 2.
  ```lean
  example : VTask.floorRoot 2 12 = 2 := by native_decide
  ```

- Claim: `VTask.floorRoot 0 a = 0` for any `a` — degree-zero convention.
  ```lean
  example (a : ℕ) : VTask.floorRoot 0 a = 0 := by simp [VTask.floorRoot]
  ```

- Claim: `VTask.floorRoot n 0 = 0` for any `n` — zero-input convention.
  ```lean
  example (n : ℕ) : VTask.floorRoot n 0 = 0 := by simp [VTask.floorRoot]
  ```

## Boundaries

- **`n = 0`**: Returns `0` regardless of `a`. This is a deliberately chosen junk value to maintain the adjunction identity.
- **`a = 0`**: Returns `0` regardless of `n`, again for adjunction coherence.
- **`n = 1`**: Returns `a` itself for any positive `a`, since `⌊k/1⌋ = k` for every exponent `k`, so the factorization is unchanged.
- **`a = 1`**: Returns `1` for any `n ≥ 1`, since `1` has an empty prime factorization and the empty product is `1`.
- **Perfect n-th powers**: When `a` is an exact n-th power, `VTask.floorRoot n a` equals the exact n-th root of `a`, and `(VTask.floorRoot n a) ^ n = a`.
- **Non-perfect powers**: The result satisfies `(VTask.floorRoot n a) ^ n ∣ a` but `(VTask.floorRoot n a) ^ n` need not equal `a`.
- **Adjunction**: For positive `n` and `b`, `a ^ n ∣ b ↔ a ∣ VTask.floorRoot n b`.

## Not to be confused with

- **`Nat.sqrt`**: The ordinary integer square root of `a` (i.e., `⌊√a⌋` in the usual metric sense), which minimizes the gap `|r² - a|` and differs from the divisibility floor root.
- **`VTask.ceilRoot`** (if it exists): The analogous *ceiling* n-th root in the divisibility order, which would round each prime exponent *up* rather than down.
- **`Nat.Coprime.pow_dvd_of_pow_dvd`**: A divisibility lemma about powers that looks related but is a theorem, not the floor-root construction itself.