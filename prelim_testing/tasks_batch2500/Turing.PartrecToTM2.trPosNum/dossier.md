## Object

`VTask.trPosNum` converts a strictly-positive binary numeral (`PosNum`) into a little-endian list of Turing-machine tape symbols from the alphabet `Turing.PartrecToTM2.Γ'`. The least-significant bit comes first. The symbol `Γ'.bit1` encodes a 1-bit and `Γ'.bit0` encodes a 0-bit. Because `PosNum` never has a most-significant 0, the resulting list never ends in `Γ'.bit0`; every list produced is a valid canonical little-endian binary representation.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.trPosNum : PosNum → List Turing.PartrecToTM2.Γ'
<!-- PINNED-SIGNATURE:END -->


The sole argument is a `PosNum` — a structurally-defined positive binary numeral whose constructors are `PosNum.one` (the numeral 1), `PosNum.bit0 n` (append a 0-bit to `n`, i.e. double it), and `PosNum.bit1 n` (append a 1-bit to `n`, i.e. double it and add one).

## Conventions

The bit ordering is little-endian: the least-significant bit occupies the head of the list and the most-significant bit occupies the tail. Because `PosNum` structurally forbids a leading (most-significant) zero, the last element of every output list is always `Γ'.bit1`, guaranteeing a canonical representation with no trailing `Γ'.bit0` symbols.

## Worked examples

- Claim: `VTask.trPosNum PosNum.one = [Γ'.bit1]` (the numeral 1 maps to the single-element list `[bit1]`)

- Claim: `VTask.trPosNum (PosNum.bit0 PosNum.one) = [Γ'.bit0, Γ'.bit1]` (the numeral 2 = 0b10 maps to `[bit0, bit1]` in little-endian order)

- Claim: `VTask.trPosNum (PosNum.bit1 PosNum.one) = [Γ'.bit1, Γ'.bit1]` (the numeral 3 = 0b11 maps to `[bit1, bit1]`)

- Claim: `VTask.trPosNum (PosNum.bit0 (PosNum.bit0 PosNum.one)) = [Γ'.bit0, Γ'.bit0, Γ'.bit1]` (the numeral 4 = 0b100 maps to `[bit0, bit0, bit1]`)

- Claim: Every element `x` in `VTask.trPosNum n` satisfies `natEnd x = false`, i.e., no tape symbol in the encoding acts as a natural-number terminator.

## Boundaries

- The smallest input is `PosNum.one`, which produces the shortest possible output `[Γ'.bit1]` (length 1). There is no zero case: `PosNum` is strictly positive, so `VTask.trPosNum` is defined for all inputs without a zero or empty-list edge case.
- The last element of any output list is always `Γ'.bit1` (never `Γ'.bit0`), because every `PosNum` ultimately bottoms out at `PosNum.one`.
- The length of the output equals the number of bits in the binary representation of the input, i.e., `⌊log₂ n⌋ + 1`.

## Not to be confused with

- `trNum` — the companion function for `Num` (which includes zero); `VTask.trPosNum` handles only the positive case and is called by `trNum` for its `Num.pos` branch.
- A big-endian encoding — `VTask.trPosNum` is little-endian (LSB first), the opposite of the usual written convention for binary numbers.
- `Γ'.bit0` and `Γ'.bit1` as Boolean values — these are tape alphabet symbols, not Lean `Bool` or `Bit` values, and their roles are determined by position in the list, not by some inherent numeric field.