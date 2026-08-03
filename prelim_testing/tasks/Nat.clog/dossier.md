## VTask.clog

### 1. Object

`VTask.clog b n` is the **ceiling logarithm** (upper logarithm) of a natural number `n` in base `b`. It returns the smallest natural number `k` such that `n ≤ b^k`. In other words, it is ⌈log_b n⌉ lifted to ℕ, with junk values of 0 assigned whenever the logarithm is not well-defined (base ≤ 1, or n ≤ 1).

### 2. Signature

```
VTask.clog : (b n : ℕ) -> ℕ
```

- `b : ℕ` — the base of the logarithm.
- `n : ℕ` — the argument whose ceiling logarithm is computed.
- Returns the smallest `k : ℕ` with `n ≤ b^k`.

### 3. Conventions

When the base `b` is 0 or 1, the logarithm is not mathematically meaningful; `VTask.clog b n` returns 0 for any `n`. When the argument `n` is 0 or 1 (and the base is valid), `n ≤ b^0 = 1` already holds, so the function returns 0. These assignments are junk/convention values ensuring the function is total on all of ℕ × ℕ.

### 4. Worked Examples

- Claim: `VTask.clog 2 8 = 3` (since 2^3 = 8 ≥ 8, and 2^2 = 4 < 8)
- Claim: `VTask.clog 2 9 = 4` (since 2^4 = 16 ≥ 9, and 2^3 = 8 < 9)
- Claim: `VTask.clog 3 27 = 3` (since 3^3 = 27, a perfect power, returns exactly 3)
- Claim: `VTask.clog 2 1 = 0` (since 1 ≤ 2^0 = 1, the smallest such k is 0)
- Claim: `VTask.clog 1 100 = 0` (base 1: junk value, returns 0)
- Claim: `VTask.clog 2 0 = 0` (n = 0 ≤ 1 = 2^0, so k = 0)

### 5. Boundaries

- **b = 0**: Returns 0 for all `n` (base 0 ≤ 1, junk value).
- **b = 1**: Returns 0 for all `n` (base 1 is degenerate, junk value).
- **n = 0**: Returns 0 (0 ≤ 1 = b^0 for any b, so k = 0 suffices; also covered by the n ≤ 1 branch).
- **n = 1**: Returns 0 (1 ≤ b^0 = 1, so the smallest k is 0).
- **n = b^k exactly**: Returns exactly `k` (perfect power case).
- **Monotonicity in n**: For fixed base `b > 1`, `VTask.clog b` is monotone in `n`.
- **Antitonicity in b**: For fixed `n`, `VTask.clog b n` is antitone in `b` (larger base ⟹ smaller or equal ceiling log).
- **Relation to floor log**: `Nat.log b n ≤ VTask.clog b n` always holds.

### 6. Not to be confused with

- **`Nat.log b n`** (floor logarithm): returns the *largest* `k` with `b^k ≤ n`, rounding *down*, whereas `VTask.clog` rounds *up*.
- **`Int.clog b r`**: a version of ceiling logarithm for real (or ordered field) inputs that can return negative integers; `VTask.clog` is ℕ-valued and always ≥ 0.
- **`Real.logb b x`**: the real-valued logarithm base `b`; `VTask.clog` is its ⌈·⌉₊ (natural ceiling) specialisation to natural number inputs.
