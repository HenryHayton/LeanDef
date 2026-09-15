## 1. Object

`VTask.valMinAbs` picks, from the residue class of `x` modulo `n`, the unique integer representative closest to zero. For a positive modulus `n`, this representative lies in the half-open interval `(-n/2, n/2]` (integers). For `n = 0`, the ring `ZMod 0` is identified with `ℤ` itself, so the function simply returns `x` unchanged.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.valMinAbs : {n : ℕ} -> ZMod n → ℤ
<!-- PINNED-SIGNATURE:END -->


```
VTask.valMinAbs : {n : ℕ} -> ZMod n → ℤ
```

The implicit argument `n` is the modulus; it is a natural number that determines the ring `ZMod n`. The explicit argument is an element of `ZMod n`, i.e., a residue class modulo `n`, whose canonical integer representative closest to zero is returned.

## 3. Conventions

When `n = 0`, the type `ZMod 0` is definitionally equal to `ℤ`, and `VTask.valMinAbs` acts as the identity, returning the integer `x` itself with no adjustment.

For a positive modulus `n`, the returned integer always satisfies `valMinAbs x * 2 ∈ Set.Ioc (-n : ℤ) n`, equivalently `valMinAbs x ∈ (-n/2, n/2]` (with division rounded down for odd `n`), so the "upper half" representative (value exactly `n/2` when `n` is even) is chosen over the "lower half" representative.

The map is injective: distinct residue classes receive distinct representatives, so `VTask.valMinAbs` can be used to distinguish elements of `ZMod n`.

The representative always casts back to the original element: `(x.valMinAbs : ZMod n) = x`.

## 4. Worked examples

- Claim: For `n = 7`, the element `3 : ZMod 7` has `valMinAbs` equal to `3` (since `3 ≤ 7/2 = 3`).
  ```lean
  example : (3 : ZMod 7).valMinAbs = 3 := by decide
  ```

- Claim: For `n = 7`, the element `5 : ZMod 7` has `valMinAbs` equal to `-2` (since `5 > 3 = 7/2`, so we subtract 7: `5 - 7 = -2`).
  ```lean
  example : (5 : ZMod 7).valMinAbs = -2 := by decide
  ```

- Claim: For `n = 6`, the element `3 : ZMod 6` has `valMinAbs` equal to `3` (since `3 ≤ 6/2 = 3`, the upper boundary is kept).
  ```lean
  example : (3 : ZMod 6).valMinAbs = 3 := by decide
  ```

- Claim: For `n = 6`, the element `4 : ZMod 6` has `valMinAbs` equal to `-2` (since `4 > 3`, so `4 - 6 = -2`).
  ```lean
  example : (4 : ZMod 6).valMinAbs = -2 := by decide
  ```

- Claim: For any `n`, `(0 : ZMod n).valMinAbs = 0`.

## 5. Boundaries

- **`n = 0`**: `ZMod 0 = ℤ`, and `VTask.valMinAbs` is the identity on integers; no adjustment occurs.
- **`n = 1`**: The only element is `0 : ZMod 1`, and its representative is `0`.
- **Even `n`, element `n/2`**: The element with natural value exactly `n/2` satisfies `val ≤ n/2`, so it receives the positive representative `n/2` (not `-(n/2)`). Thus the interval is half-open on the left.
- **`x = 0`**: Always gives `valMinAbs 0 = 0` for any `n`.
- **Negation**: For elements that are not the "half" element (i.e., `2 * x.val ≠ n`), negation commutes with `valMinAbs`: `(-x).valMinAbs = -(x.valMinAbs)`. For the half element (when it exists), both `x` and `-x` are the same element, so this is trivially satisfied.

## 6. Not to be confused with

- **`ZMod.val`**: Returns the canonical representative in `{0, 1, …, n-1}` (always non-negative), not the one closest to zero.
- **`Int.emod`**: Computes a remainder always in `[0, n)`, again without centering around zero.
- **`Int.natAbs`**: Returns the absolute value of an integer as a natural number, unrelated to residue classes.