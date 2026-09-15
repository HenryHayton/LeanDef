## VTask.addBottom

### Object

Given a `ListBlank` of stacks (each cell is a tuple assigning to every tape-head index `k` an optional symbol from alphabet `Γ k`), `addBottom` produces a `ListBlank` over the product type `Γ' K Γ` that is identical in content but decorates exactly the **first** (leftmost / head) position with a Boolean flag `true` — the "bottom marker" — while every subsequent position carries the flag `false`. This encoding allows a multi-tape Turing machine simulation to identify the absolute bottom of all stacks simultaneously, embedded in a single-tape representation.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.addBottom : {K : Type u_1} -> {Γ : K → Type u_2} -> (L : Turing.ListBlank ((k : K) → Option (Γ k))) -> Turing.ListBlank (Turing.TM2to1.Γ' K Γ)
<!-- PINNED-SIGNATURE:END -->


`VTask.addBottom : {K : Type u_1} -> {Γ : K → Type u_2} -> (L : Turing.ListBlank ((k : K) → Option (Γ k))) -> Turing.ListBlank (Turing.TM2to1.Γ' K Γ)`

- `K` is the implicit finite index type enumerating the tapes (tape-head indices).
- `Γ` is the implicit family of tape alphabets, assigning to each tape index `k` its symbol type `Γ k`.
- `L` is the input `ListBlank`, representing the combined stack contents across all tapes: each entry maps every tape index to an optional alphabet symbol.

The return value is a `ListBlank` over `Γ' K Γ`, the product type pairing a Boolean bottom-marker with the stack content, ready for single-tape simulation.

### Conventions

The Boolean bottom-marker component of the very first cell is `true`; all subsequent cells carry `false` as their marker. This convention is the sole distinguishing feature introduced by `addBottom` relative to the plain stack data.

### Worked examples

- Claim: After applying `VTask.addBottom` to any `ListBlank L`, the head of the result has its Boolean component equal to `true` and its data component equal to `L.head`.

- Claim: For every index `i ≥ 1` into the resulting `ListBlank`, the Boolean component of the entry at position `i` is `false`, reflecting that only the bottom position carries the marker.

- Claim: The content projection of each cell in `VTask.addBottom L` (ignoring the Boolean flag) equals the corresponding cell of `L`; i.e., `addBottom` is a lossless decoration that does not alter the stack data.

### Boundaries

- A `ListBlank` is a semi-infinite sequence that is eventually the blank/default value; `addBottom` respects this: the output is also eventually the default element of `Γ' K Γ`, which pairs `false` with the default stack row.
- Since `ListBlank` is defined up to trailing blanks, `addBottom` is well-defined on equivalence classes: feeding in two representatives of the same `ListBlank` produces the same output `ListBlank`.
- The `true` marker appears at exactly one logical position (the head); there is no notion of "empty" input that would omit the marker — even if `L` represents all-blank stacks, the output still has `true` at position 0.

### Not to be confused with

- `Turing.ListBlank.map`: a general-purpose covariant map on `ListBlank` that applies a function uniformly to every cell, without singling out the head for special treatment.
- `Turing.TM2to1.Γ'`: the *type* of cells in the single-tape encoding (a pair of a Boolean and a stack row); `addBottom` produces a `ListBlank` *of* this type but is not the type itself.
- The `bottom` element of a `ListBlank` in the sense of the default/blank value: here "bottom marker" refers to the positional marker indicating the base of the stacks, not the blank symbol of the tape alphabet.