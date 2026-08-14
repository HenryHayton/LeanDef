## Object

`VTask.psub m n` is the *partial subtraction* of `n` from `m` on natural numbers. It returns `some k` when `m` is at least `n` and the difference is `k` (i.e., `k + n = m`), and `none` when `m < n` (i.e., when ordinary natural-number subtraction would silently truncate to 0). It is the "honest" version of natural-number subtraction that signals failure instead of clamping.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.psub : (m : ℕ) -> ℕ → Option ℕ
<!-- PINNED-SIGNATURE:END -->


`(m : ℕ) -> ℕ → Option ℕ`

The first argument `m` is the *minuend* — the number being subtracted from. The second argument (unnamed, introduced by the arrow) is the *subtrahend* `n` — the amount to subtract. The result is an `Option ℕ`: `some k` if the subtraction is exact (with quotient `k`), or `none` if the subtrahend exceeds the minuend.

## Conventions

When the subtrahend is 0 the result is always `some m`, since subtracting nothing leaves `m` intact. When `m < n` (the subtrahend strictly exceeds the minuend) the result is `none`; there is no junk-value fallback to 0 as in ordinary `Nat` subtraction.

## Worked examples

- Claim: `VTask.psub 5 3 = some 2` (5 − 3 = 2, within range).
- Claim: `VTask.psub 3 5 = none` (3 < 5, so subtraction is undefined).
- Claim: `VTask.psub 7 0 = some 7` (subtracting zero always succeeds and returns the minuend).
- Claim: `VTask.psub 4 4 = some 0` (exact equality: difference is 0).
- Claim: For any `m n : ℕ` with `n ≤ m`, `VTask.psub m n = some (m - n)` (the result agrees with ordinary truncating subtraction whenever no truncation is needed).
- Claim: `VTask.psub m n = none ↔ m < n` (the `none` branch is characterised exactly by the subtrahend being strictly larger).

## Boundaries

- **Subtrahend is 0**: always returns `some m`, regardless of `m`.
- **`m = n`**: returns `some 0`; the difference exists and equals zero.
- **`m < n`**: returns `none`; this is the precise boundary condition for failure.
- **`m > n`**: returns `some (m - n)`; agrees with ordinary `Nat` subtraction.
- **`m = 0, n = 0`**: returns `some 0`.
- **`m = 0, n > 0`**: returns `none` (since `0 < n`).

## Not to be confused with

- **`Nat.sub` (written `m - n`)**: ordinary truncating subtraction on `ℕ`; silently returns 0 when `n > m` instead of signalling failure.
- **`Nat.ppred`**: partial predecessor, the `n = 1` special case of partial subtraction (returns `none` for 0, `some k` for `k+1`).
- **`Nat.psub'`**: an alternative spelling of the same partial subtraction; provably equal to `VTask.psub`.