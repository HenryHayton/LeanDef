## VTask.revAt

### Object

`VTask.revAt N` is an injective embedding of the natural numbers into themselves that "reflects" the initial segment `{0, 1, …, N}` around its midpoint. Concretely, for a natural number `i`, the embedding sends `i` to `N − i` when `i ≤ N`, and leaves `i` fixed (returns `i` unchanged) when `i > N`. The embedding is constructed so that it is an involution on `{0, …, N}`: applying it twice recovers the original value.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.revAt : (N : ℕ) -> ℕ ↪ ℕ
<!-- PINNED-SIGNATURE:END -->


`(N : ℕ) -> ℕ ↪ ℕ`

The first argument `N` is the "ceiling" or "reflection point": it is the largest index that gets remapped. The result is a bundled injective function (an `Embedding`) from `ℕ` to `ℕ`.

### Conventions

For indices `i` strictly greater than `N`, the embedding returns `i` unchanged. This is a junk-value convention: the embedding is really only meaningful on the domain `{0, …, N}`, but it must be total on `ℕ`. Returning `i` for `i > N` (rather than, say, `0`) is the choice that makes the whole function injective.

### Worked examples

- Claim: `VTask.revAt 5 3 = 2` (since `3 ≤ 5`, the result is `5 − 3 = 2`)
  ```lean
  example : (VTask.revAt 5).toFun 3 = 2 := by decide
  ```

- Claim: `VTask.revAt 5 0 = 5` (since `0 ≤ 5`, the result is `5 − 0 = 5`)
  ```lean
  example : (VTask.revAt 5).toFun 0 = 5 := by decide
  ```

- Claim: `VTask.revAt 5 5 = 0` (since `5 ≤ 5`, the result is `5 − 5 = 0`)
  ```lean
  example : (VTask.revAt 5).toFun 5 = 0 := by decide
  ```

- Claim: `VTask.revAt 5 7 = 7` (since `7 > 5`, the result is `7` unchanged)
  ```lean
  example : (VTask.revAt 5).toFun 7 = 7 := by decide
  ```

- Claim: Applying `VTask.revAt N` twice to any `i ≤ N` returns `i` (involutivity on the relevant domain). For example, `(VTask.revAt 5).toFun ((VTask.revAt 5).toFun 3) = 3`.
  ```lean
  example : (VTask.revAt 5).toFun ((VTask.revAt 5).toFun 3) = 3 := by decide
  ```

### Boundaries

- At `i = 0` with any `N`: `VTask.revAt N 0 = N`, since `0 ≤ N` always holds for natural numbers.
- At `i = N`: `VTask.revAt N N = 0`, since `N ≤ N` holds and `N − N = 0`.
- At `N = 0`: `VTask.revAt 0 0 = 0`, and for all `i > 0`, `VTask.revAt 0 i = i` (the identity on all positive naturals).
- For `i = N + 1` (first index above the reflection range): `VTask.revAt N (N + 1) = N + 1`, the fixed-point regime begins immediately.
- The function is injective on all of `ℕ`: points in the range `{0, …, N}` map bijectively among themselves, and points above `N` are fixed, so no two distinct inputs produce the same output.

### Not to be confused with

- Truncated subtraction `N - i : ℕ`: This is not injective (e.g., `N - (N+1) = N - (N+2) = 0`) and is not an embedding; `VTask.revAt` fixes values above `N` precisely to avoid this collapse.
- `Function.Involutive` instances on `Fin N`: `VTask.revAt` works on all of `ℕ`, not on a finite type, though its restriction to `{0, …, N}` behaves like reversal on `Fin (N+1)`.
- `OrderIso.symm` for natural number order: `VTask.revAt` reverses the order on `{0, …, N}` but is not an order isomorphism on `ℕ` as a whole.
