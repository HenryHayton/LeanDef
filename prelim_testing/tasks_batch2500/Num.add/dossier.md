## Object

`VTask.add` computes the sum of two non-negative binary numerals of type `Num`. `Num` is a type that represents natural numbers in a binary (positional) format, with a distinguished zero constructor and a `pos` constructor wrapping a positive binary numeral (`PosNum`). The result is the unique `Num` value whose natural-number interpretation equals the sum of the natural-number interpretations of the two inputs.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.add : Num → Num → Num
<!-- PINNED-SIGNATURE:END -->


The first argument is the left addend, a non-negative binary numeral. The second argument is the right addend, also a non-negative binary numeral. Both arguments and the result inhabit the same `Num` type.

## Conventions

Zero is represented by the distinguished constructor `0 : Num` (not as `pos` of anything). When either addend is zero, the result is exactly the other addend with no structural change — `0 + a = a` and `b + 0 = b`. When both addends are positive (of the form `pos a` and `pos b`), the result is `pos` applied to the sum of the underlying `PosNum` values.

## Worked examples

- Claim: `VTask.add 0 0 = 0`
  ```lean
  example : VTask.add 0 0 = 0 := by decide
  ```

- Claim: `VTask.add 0 (pos 1) = pos 1` (zero plus a positive numeral is that numeral)
  ```lean
  example : VTask.add 0 (Num.pos 1) = Num.pos 1 := by decide
  ```

- Claim: `VTask.add (pos 1) 0 = pos 1` (a positive numeral plus zero is that numeral)
  ```lean
  example : VTask.add (Num.pos 1) 0 = Num.pos 1 := by decide
  ```

- Claim: The cast of `VTask.add m n` to `ℕ` equals the sum of the casts of `m` and `n` (the operation is a homomorphism to natural-number addition).

- Claim: `VTask.add` is commutative: for all `m n : Num`, `VTask.add m n = VTask.add n m`.

- Claim: `VTask.add` is associative: for all `m n k : Num`, `VTask.add (VTask.add m n) k = VTask.add m (VTask.add n k)`.

## Boundaries

- **Both arguments zero:** `VTask.add 0 0 = 0`. This is handled by the left-zero case, which returns the right argument (itself zero).
- **Left argument zero:** `VTask.add 0 a = a` for any `a`, including when `a = 0`.
- **Right argument zero:** `VTask.add b 0 = b` for any `b`, including when `b = 0`. This is a separate case from the left-zero case, so both identities hold definitionally.
- **Both positive:** The result wraps the `PosNum`-level addition inside `pos`; since a sum of two positive numbers is positive, the result is always `pos (...)` and never `0`.
- The function is total; there are no undefined or junk inputs.

## Not to be confused with

- `PosNum.add`: addition restricted to the strictly-positive binary numeral type `PosNum`; does not handle zero.
- `ZNum.add`: addition on the signed binary numeral type `ZNum`, which also covers negative numbers.
- `Nat.add`: the standard addition on `ℕ`; `Num` and `ℕ` are distinct types, though `VTask.add` is definitionally compatible with `Nat.add` under the canonical cast.