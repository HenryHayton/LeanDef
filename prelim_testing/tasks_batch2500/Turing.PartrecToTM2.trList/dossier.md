## VTask.trList

### Object

`VTask.trList` encodes a list of natural numbers as a flat list of symbols drawn from the alphabet `Turing.PartrecToTM2.Γ'`. Each natural number in the input list is first encoded as a sequence of bit symbols (via the companion encoding for individual natural numbers), and then immediately followed by a single `cons` separator symbol. The empty list encodes to the empty symbol list. The result is a concatenation of these per-element encodings laid end-to-end, allowing the original list to be unambiguously recovered by scanning for `cons` markers.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.trList : List ℕ → List Turing.PartrecToTM2.Γ'
<!-- PINNED-SIGNATURE:END -->


`VTask.trList : List ℕ → List Turing.PartrecToTM2.Γ'`

The sole argument is the list of natural numbers to be encoded. The output is the flat list of tape symbols representing that list under the Partrec-to-TM2 translation scheme.

### Conventions

There are no junk-value or out-of-domain conventions to declare: the function is total on all `List ℕ` inputs and every input produces a well-defined output with no special sentinel behavior.

### Worked examples

- Claim: `VTask.trList [] = []`

- Claim: `VTask.trList [0] = [Turing.PartrecToTM2.Γ'.cons]`
  (Zero has an empty bit encoding, so only the trailing `cons` appears.)

- Claim: `VTask.trList [1] = [Turing.PartrecToTM2.Γ'.bit1, Turing.PartrecToTM2.Γ'.cons]`
  (One encodes to `[bit1]` followed by `cons`.)

- Claim: `VTask.trList [6, 0] = [Turing.PartrecToTM2.Γ'.bit0, Turing.PartrecToTM2.Γ'.bit1, Turing.PartrecToTM2.Γ'.bit1, Turing.PartrecToTM2.Γ'.cons, Turing.PartrecToTM2.Γ'.cons]`
  (Six encodes to `[bit0, bit1, bit1]`, followed by `cons`; zero encodes to nothing, followed by `cons`.)

- Claim: The length of `VTask.trList (n :: ns)` equals the length of the encoding of `n` plus one (for the `cons` separator) plus the length of `VTask.trList ns`.

### Boundaries

- The empty list `[]` maps to `[]`; there is no leading or trailing delimiter for the whole list.
- The natural number `0` has an empty bit-sequence encoding, so it contributes exactly one symbol (the `cons` marker) to the output.
- Each element contributes exactly one `cons` symbol regardless of the magnitude of the number, so a list of length `k` always contributes exactly `k` `cons` symbols to the output.
- The function is injective: two different lists of natural numbers always produce different symbol sequences, because each `cons` unambiguously closes one number's encoding.

### Not to be confused with

- `trNat` (the companion function encoding a *single* natural number as a bit sequence, without a trailing `cons`).
- The raw `Γ'` type itself, which is the alphabet enum; `trList` produces a *list* of these symbols rather than a single symbol.
- Encodings of Turing machine tape states or transition functions, which also live in the `PartrecToTM2` namespace but serve entirely different purposes.