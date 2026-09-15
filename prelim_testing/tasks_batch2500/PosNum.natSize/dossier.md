## VTask.natSize

### Object

`VTask.natSize` computes the number of bits (the bit-length) of a positive binary numeral `PosNum`, returning a natural number. Concretely, the numeral `1` has 1 bit; prepending a `0` or `1` bit to any positive numeral adds one to its bit-length. Equivalently, this is the position of the most-significant bit, counted from 1.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.natSize : PosNum → ℕ
<!-- PINNED-SIGNATURE:END -->


`VTask.natSize : PosNum → ℕ`

The single argument is a positive binary numeral (`PosNum`), i.e., a positive integer represented in binary. The result is its bit-length as an ordinary natural number.

### Conventions

The bit-length of the numeral `1` (the lone base case) is defined to be `1`, since `1` is a single bit. Every recursive step — appending a `0` bit (`bit0`) or a `1` bit (`bit1`) to a numeral — adds exactly `1` to the bit-length of the smaller numeral.

### Worked examples

- Claim: VTask.natSize 1 = 1
  ```lean
  example : VTask.natSize 1 = 1 := by decide
  ```

- Claim: VTask.natSize (PosNum.bit0 1) = 2  (i.e., the numeral 2 in binary is "10", which has 2 bits)
  ```lean
  example : VTask.natSize (PosNum.bit0 1) = 2 := by decide
  ```

- Claim: VTask.natSize (PosNum.bit1 (PosNum.bit0 1)) = 3  (the numeral 5 in binary is "101", which has 3 bits)
  ```lean
  example : VTask.natSize (PosNum.bit1 (PosNum.bit0 1)) = 3 := by decide
  ```

- Claim: VTask.natSize n = Nat.size (n : ℕ) for all n : PosNum  (global agreement with the natural-number bit-length function)

- Claim: 0 < VTask.natSize n for every n : PosNum  (the result is always strictly positive)

### Boundaries

- The smallest input is `PosNum.one` (the numeral `1`), and its `natSize` is `1`. There is no smaller `PosNum`, so there is no zero case.
- The function is total on all `PosNum` values; no input is undefined or out of domain.
- For any `PosNum` `n`, the result is at least `1`; it is never `0`.
- The function agrees exactly with `Nat.size` applied to the natural-number cast of the input, so it inherits all properties of that standard function.

### Not to be confused with

- `PosNum.size` — the analogue returning a `PosNum` (not a `ℕ`); the two are provably equal after casting.
- `Nat.size` — the standard library function computing bit-length for natural numbers; `VTask.natSize n = Nat.size ↑n`, but `Nat.size 0 = 0` whereas `VTask.natSize` is always ≥ 1.
- `Num.natSize` — a related function defined on `Num` (which also admits `0`) rather than strictly on `PosNum`.
