## Object

`VTask.pred'` computes the predecessor of a strictly-positive binary numeral (`PosNum`), returning the result as a possibly-zero binary numeral (`Num`). Because `PosNum` represents numbers ≥ 1, the predecessor of 1 is 0, which lives in `Num` but not in `PosNum`; hence the return type must be the wider type `Num`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pred' : PosNum → Num
<!-- PINNED-SIGNATURE:END -->


`VTask.pred' : PosNum → Num`

The sole argument is the strictly-positive binary numeral whose predecessor is to be computed.

## Conventions

The function is total: every `PosNum` has a well-defined predecessor in `Num`. There are no junk values or out-of-domain inputs.

## Worked examples

- Claim: `VTask.pred' 1 = 0` — the predecessor of 1 (the smallest `PosNum`) is `Num.zero`.
- Claim: `VTask.pred' (PosNum.bit1 1) = Num.pos (PosNum.bit0 1)` — the predecessor of 3 (binary `11`) is 2 (binary `10`).
- Claim: `VTask.pred' (PosNum.bit0 1) = Num.pos 1` — the predecessor of 2 (binary `10`) is 1.
- Claim: For any `PosNum` `n`, casting `VTask.pred' n` to `ℕ` gives `Nat.pred (n : ℕ)`, i.e., `(VTask.pred' n : ℕ) = (n : ℕ) - 1`.
- Claim: For any `PosNum` `n`, `(n : ℕ) = (VTask.pred' n : ℕ) + 1`, reflecting the identity `n = pred(n) + 1`.

## Boundaries

- At `1` (the least element of `PosNum`): the result is `Num.zero` (`0 : Num`), the only case where a `Num` value outside `Num.pos _` is returned.
- For any `bit1 n` (an odd number ≥ 3): the predecessor is even, represented as `Num.pos (bit0 n)`.
- For any `bit0 n` (an even number ≥ 2): the predecessor is odd; the computation recurses on the predecessor of `n` to build the correct odd binary representation, and the result is always in `Num.pos _`.

## Not to be confused with

- `Num.pred`: the predecessor function on the wider type `Num`; inputs `0 : Num` and returns `0`, whereas `VTask.pred'` never receives `0`.
- `Num.ppred`: a partial predecessor returning `Option Num`, used when one needs to distinguish the `0` predecessor case explicitly.
- `PosNum.succ'`: the successor map `Num → PosNum`, the left inverse of `VTask.pred'` (i.e., `succ' (pred' n) = n`).