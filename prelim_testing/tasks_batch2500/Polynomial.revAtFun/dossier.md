## Object

`VTask.revAtFun N i` is the "reflection about the midpoint" map on natural numbers. Given an upper bound `N` and a position `i`, it returns `N - i` when `i ≤ N` (reflecting `i` across the centre of the interval `[0, N]`), and returns `i` unchanged when `i > N`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.revAtFun : (N i : ℕ) -> ℕ
<!-- PINNED-SIGNATURE:END -->


`VTask.revAtFun : (N i : ℕ) -> ℕ`

The first argument `N` is the upper bound (or "ceiling") of the interval being reflected over; the second argument `i` is the position to be mapped.

## Conventions

When `i > N`, the function returns `i` itself rather than being undefined or signalling an error. This is a junk-value convention: inputs outside the intended domain `[0, N]` are handled by the identity.

## Worked examples

- Claim: `VTask.revAtFun 10 3 = 7` (reflecting 3 over [0, 10] gives 10 − 3 = 7)
  ```lean
  example : VTask.revAtFun 10 3 = 7 := by decide
  ```

- Claim: `VTask.revAtFun 10 10 = 0` (reflecting the endpoint 10 over [0, 10] gives 0)
  ```lean
  example : VTask.revAtFun 10 10 = 0 := by decide
  ```

- Claim: `VTask.revAtFun 5 8 = 8` (since 8 > 5, the out-of-range input is returned unchanged)
  ```lean
  example : VTask.revAtFun 5 8 = 8 := by decide
  ```

- Claim: `VTask.revAtFun N (VTask.revAtFun N i) = i` when `i ≤ N` (the map is an involution on `[0, N]`)

## Boundaries

- At `i = 0`: returns `N - 0 = N` (0 is always ≤ N, so reflection always applies).
- At `i = N`: returns `N - N = 0` (the top endpoint maps to the bottom).
- At `i = N + 1` and beyond: the condition `i ≤ N` fails, so the function returns `i` unchanged. In particular `VTask.revAtFun N (N + 1) = N + 1`.
- At `N = 0`: returns `0 - i = 0` for `i = 0`, and returns `i` for all `i > 0`.

## Not to be confused with

- The embedding `revAt` built from this function: `revAt` is an order-embedding version of the same reflection, whereas `VTask.revAtFun` is the raw ℕ → ℕ function.
- Natural-number subtraction `N - i` alone: `N - i` in Lean saturates at 0 for all `i > N`, which differs from `VTask.revAtFun`'s behaviour of returning `i` itself when `i > N`.
- A modular-arithmetic reflection: `VTask.revAtFun` does not wrap around modulo any number; it simply fixes points outside `[0, N]`.