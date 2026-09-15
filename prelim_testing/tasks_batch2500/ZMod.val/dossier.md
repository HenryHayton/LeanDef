## Object

`VTask.val` extracts a canonical natural-number representative from an element of `ZMod n`. For `ZMod 0`, which is identified with the integers, the result is the absolute value of the integer. For `ZMod n` with `n > 0`, the result is the unique natural number in `{0, 1, …, n-1}` that lies in the same residue class — i.e., the least non-negative representative modulo `n`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.val : {n : ℕ} -> ZMod n → ℕ
<!-- PINNED-SIGNATURE:END -->


`VTask.val : {n : ℕ} → ZMod n → ℕ`

The implicit argument `n` is the modulus determining which ring `ZMod n` we are working in. The explicit argument is the element of `ZMod n` whose canonical representative we want.

## Conventions

When `n = 0`, `ZMod 0` is the integers and `VTask.val` returns the absolute value (i.e., `Int.natAbs`), not a residue. When `n > 0`, the output always satisfies `0 ≤ VTask.val a < n`, so the least non-negative residue is returned.

## Worked examples

- Claim: For `a : ZMod 7` equal to `3`, `VTask.val a = 3`.
  ```lean
  example : VTask.val (3 : ZMod 7) = 3 := by decide
  ```

- Claim: For `a : ZMod 7` equal to `6`, `VTask.val a = 6`.
  ```lean
  example : VTask.val (6 : ZMod 7) = 6 := by decide
  ```

- Claim: For `a : ZMod 5` equal to `0`, `VTask.val a = 0`.
  ```lean
  example : VTask.val (0 : ZMod 5) = 0 := by decide
  ```

- Claim: For `a : ZMod 0` equal to the integer `-3`, `VTask.val a = 3` (absolute value).

- Claim: `VTask.val (1 : ZMod 0) = 1` (absolute value of integer 1 is 1).
  ```lean
  example : VTask.val (1 : ZMod 0) = 1 := by decide
  ```

## Boundaries

- When `n = 1`, `ZMod 1` is the trivial ring with a single element `0`, so `VTask.val (0 : ZMod 1) = 0` and this is the only possible output.
- When `n = 0`, the output is unbounded (it is `Int.natAbs` of the underlying integer) and can be any natural number.
- For `n > 0`, the output is always in `{0, 1, …, n-1}`; in particular `VTask.val a < n` for all `a : ZMod n`.
- `VTask.val a = 0` if and only if `a = 0` (for all `n`).
- When `n > 0`, the map `VTask.val : ZMod n → ℕ` is injective (it is a bijection onto `{0, …, n-1}`).

## Not to be confused with

- `ZMod.valMinAbs`: a variant that maps `ZMod n` to `ℤ` choosing the representative with smallest absolute value (i.e., in the symmetric range around 0), rather than the least non-negative one.
- Casting `ZMod n` to `ℕ` or `ℤ` via coercion (`↑a`): for `n > 0` this coincides with `VTask.val` via `Fin`'s coercion, but for `n = 0` the coercion is the identity on `ℤ` (preserving sign), whereas `VTask.val` takes absolute value.
- `Fin.val`: the underlying natural-number value of a `Fin n` element; for `n > 0`, `VTask.val` on `ZMod n` reduces to exactly `Fin.val` after the identification `ZMod (n+1) = Fin (n+1)`.