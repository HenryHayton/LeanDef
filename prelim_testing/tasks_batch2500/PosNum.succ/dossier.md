## Object

`VTask.succ` computes the successor of a positive binary numeral, i.e., it returns the unique `PosNum` whose value (as a positive integer) is exactly one greater than its input. It is the analogue of `n ↦ n + 1` restricted to the type of strictly positive binary numbers.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.succ : PosNum → PosNum
<!-- PINNED-SIGNATURE:END -->


`VTask.succ : PosNum → PosNum`

The single argument is a positive binary numeral (a member of the inductive type `PosNum`, whose constructors represent 1, and numbers whose binary representations end in a 0-bit or a 1-bit). The function returns its successor as another `PosNum`.

## Conventions

No junk-value or out-of-domain conventions are declared: `VTask.succ` is a total function on all `PosNum` values, with no undefined or sentinel cases.

## Worked examples

- Claim: The successor of `1` (the numeral 1) is `bit0 one`, which represents 2. Casting to ℕ: `(VTask.succ 1 : ℕ) = 2`.
- Claim: The successor of `bit1 1` (binary `11`, i.e. 3) is `bit0 (VTask.succ 1)` = `bit0 (bit0 one)`, which represents 4. Casting to ℕ: `(VTask.succ (PosNum.bit1 1) : ℕ) = 4`.
- Claim: The successor of `bit0 1` (binary `10`, i.e. 2) is `bit1 1`, which represents 3. Casting to ℕ: `(VTask.succ (PosNum.bit0 1) : ℕ) = 3`.
- Claim: For every `n : PosNum`, `(VTask.succ n : ℕ) = (n : ℕ) + 1` (the cast of the successor equals the successor of the cast).

## Boundaries

- The minimum input is `1` (= `PosNum.one`), since `PosNum` contains no zero. Its successor is `bit0 one`, representing 2; there is no underflow or special-case issue.
- There is no maximum input: `PosNum` is an unbounded inductive type, and `VTask.succ` is defined for all of them.
- A `bit0 n` input (an even positive number) yields `bit1 n` (the odd number one greater), without recursing.
- A `bit1 n` input (an odd positive number ≥ 3) yields `bit0 (VTask.succ n)`, which may carry recursively through multiple high bits (e.g., `bit1 (bit1 n)` → `bit0 (bit0 (VTask.succ n))`), correctly implementing binary carry propagation.

## Not to be confused with

- `PosNum.succ'` (`Num.succ'`): the successor function that maps `Num` (which includes zero) to `PosNum`, rather than `PosNum` to `PosNum`.
- `Nat.succ`: the successor on natural numbers; `VTask.succ` is its analogue on `PosNum`, and they agree under the canonical cast, but they are distinct functions on distinct types.
- `PosNum.pred'`: the partial predecessor on `PosNum` (returning a `Num` to accommodate the predecessor of 1 being 0); it is the left inverse of `VTask.succ` but not the same function.