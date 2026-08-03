## VTask.ModEq

### 1. Object

`VTask.ModEq n a b` is the proposition that the natural numbers `a` and `b` are **congruent modulo `n`**: they leave the same remainder when divided by `n`. This is the standard elementary number-theory notion of modular equality, restricted here to natural numbers.

### 2. Signature

```
VTask.ModEq : (n a b : ℕ) -> Prop
```

- `n : ℕ` — the modulus.
- `a : ℕ` — the first natural number.
- `b : ℕ` — the second natural number.

Returns the proposition `a % n = b % n`.

The conventional infix notation is `a ≡ b [MOD n]`.

### 3. Conventions

**Modulus zero:** When `n = 0`, the remainder operation `a % 0` equals `a` for all natural numbers `a` (since division by zero yields zero in Lean's `Nat`). Therefore `VTask.ModEq 0 a b` holds if and only if `a = b`.

**Modulus one:** When `n = 1`, every natural number has remainder `0` modulo `1`, so `VTask.ModEq 1 a b` holds for all `a` and `b`.

**Reflexivity:** `VTask.ModEq n a a` holds for every `n` and `a`.

### 4. Worked examples

- Claim: `VTask.ModEq 5 7 12` holds (both 7 and 12 leave remainder 2 modulo 5).
  ```lean
  example : VTask.ModEq 5 7 12 := by decide
  ```

- Claim: `VTask.ModEq 3 0 9` holds (both 0 and 9 leave remainder 0 modulo 3).
  ```lean
  example : VTask.ModEq 3 0 9 := by decide
  ```

- Claim: `VTask.ModEq 0 5 5` holds (modulus zero forces equality, and 5 = 5).
  ```lean
  example : VTask.ModEq 0 5 5 := by decide
  ```

- Claim: `¬ VTask.ModEq 0 5 6` holds (modulus zero requires equality, and 5 ≠ 6).
  ```lean
  example : ¬ VTask.ModEq 0 5 6 := by decide
  ```

- Claim: `VTask.ModEq 1 42 99` holds (every pair of naturals is congruent mod 1).
  ```lean
  example : VTask.ModEq 1 42 99 := by decide
  ```

### 5. Boundaries

- **`n = 0`:** `VTask.ModEq 0 a b` is equivalent to `a = b`, because `a % 0 = a` in `ℕ`.
- **`n = 1`:** `VTask.ModEq 1 a b` is always true, since every natural number is congruent to every other modulo 1.
- **`a = b`:** `VTask.ModEq n a a` is always true (reflexivity).
- **`a < n` and `b < n`:** `VTask.ModEq n a b` reduces to the literal equality `a = b`.
- The relation is symmetric and transitive, forming an equivalence relation on `ℕ` for each fixed `n`.

### 6. Not to be confused with

- **`Int.ModEq n a b`** — the integer analogue, where the modulus and arguments are integers and `n ∣ b - a`; differs from `VTask.ModEq` in type (uses `ℤ` instead of `ℕ`) and definition.
- **`a % n`** (`Nat.mod`) — the remainder function itself, which is a `ℕ`-valued term, not a proposition; `VTask.ModEq` is the *equality of two such remainders*.
- **`n ∣ b - a`** (divisibility) — for integers this is equivalent to modular congruence, but for natural-number subtraction it diverges when `b < a` due to truncated subtraction.
