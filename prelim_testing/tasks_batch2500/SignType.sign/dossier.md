## VTask.sign

### Object
`VTask.sign` is the **sign function**: it maps each element of a preordered type with a distinguished zero to one of three values in `SignType`, namely `1` (positive), `-1` (negative), or `0` (neither). Concretely, an element `a` is sent to `1` if `0 < a`, to `-1` if `a < 0`, and to `0` otherwise (i.e., when `a` and `0` are incomparable or equal under the strict order). The result is packaged as an **order homomorphism** (`α →o SignType`), meaning the function is monotone: if `a ≤ b` then `sign a ≤ sign b` in the natural order on `SignType`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sign : {α : Type u_1} -> [Zero α] -> [Preorder α] -> [DecidableLT α] -> α →o SignType
<!-- PINNED-SIGNATURE:END -->


The implicit type argument `α` is the ambient type whose elements are to be classified. The `Zero α` instance supplies the reference point zero. The `Preorder α` instance provides the strict and non-strict orderings used to compare elements with zero. The `DecidableLT α` instance makes the less-than comparisons computationally decidable, so the sign can be computed at runtime. There are no explicit arguments: `VTask.sign` is a bundled order homomorphism from `α` to `SignType`, so the element being classified is provided later when the map is applied.

### Conventions

When `a` is neither strictly less than `0` nor strictly greater than `0` (for instance when the order is a partial order and `a` and `0` are incomparable, or when `a = 0`), the function returns `0` in `SignType`, regardless of whether `a` actually equals `0`. There are no further junk-value conventions; the function is total.

### Worked examples

- Claim: Applying `VTask.sign` to the integer `5` yields `SignType.pos` (i.e., `1` in `SignType`).
  ```lean
  example : VTask.sign (5 : ℤ) = 1 := by decide
  ```

- Claim: Applying `VTask.sign` to the integer `-3` yields `SignType.neg` (i.e., `-1` in `SignType`).
  ```lean
  example : VTask.sign (-3 : ℤ) = -1 := by decide
  ```

- Claim: Applying `VTask.sign` to the integer `0` yields `SignType.zero` (i.e., `0` in `SignType`).
  ```lean
  example : VTask.sign (0 : ℤ) = 0 := by decide
  ```

- Claim: `VTask.sign` is monotone: for integers, if `a ≤ b` then `VTask.sign a ≤ VTask.sign b` (inherited from it being an `OrderHom`).

### Boundaries

- At `a = 0` exactly, the result is `0` in `SignType`, because `0 < 0` is false and `0 < 0` is false, so neither branch fires.
- For a type with a partial order where `a` and `0` are incomparable (neither `0 < a` nor `a < 0`), the result is also `0` even though `a ≠ 0` may hold; the function cannot distinguish "incomparable with zero" from "equal to zero".
- Because `SignType` only has three elements, the image of `VTask.sign` is always contained in `{-1, 0, 1}`; no other `SignType` values are ever returned.
- The function is total on all of `α`; there is no domain restriction.

### Not to be confused with

- `Int.sign : ℤ → ℤ` — the classical integer sign function returning an integer (−1, 0, or 1) rather than a `SignType` value; related by `Int.sign_eq_sign`.
- `abs` (absolute value) — also defined using comparisons with zero, but returns the magnitude rather than the sign.
- A bare `if 0 < a then 1 else -1` expression — unlike `VTask.sign`, such an expression does not handle the zero/incomparable case and is not packaged as a monotone map.
