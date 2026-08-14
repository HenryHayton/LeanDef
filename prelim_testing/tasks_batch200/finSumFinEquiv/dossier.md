## VTask.finSumFinEquiv

### Object

A canonical bijection (in fact, an equivalence of types) between the disjoint union `Fin m ⊕ Fin n` and `Fin (m + n)`. Concretely, the left summand `Fin m` is identified with the first `m` elements of `Fin (m + n)` (indices `0` through `m - 1`), and the right summand `Fin n` is identified with the last `n` elements (indices `m` through `m + n - 1`). The inverse map splits an element of `Fin (m + n)` back into the appropriate summand according to whether its value is less than `m`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.finSumFinEquiv : {m n : ℕ} -> Fin m ⊕ Fin n ≃ Fin (m + n)
<!-- PINNED-SIGNATURE:END -->


`{m n : ℕ} -> Fin m ⊕ Fin n ≃ Fin (m + n)`

The implicit argument `m` is the size of the left finite type; the implicit argument `n` is the size of the right finite type. No explicit value argument is required: the result is the equivalence itself, a bundled record carrying both the forward and inverse functions together with proofs that they are mutual inverses.

### Conventions

There are no junk-value or edge conventions for this definition: it is a total, unconditional equivalence defined for all natural numbers `m` and `n`, including the degenerate cases `m = 0` and `n = 0`.

### Worked examples

- Claim: Applying `VTask.finSumFinEquiv` to `Sum.inl i` (for `i : Fin m`) yields `Fin.castAdd n i`, i.e., the element of `Fin (m + n)` with the same numeric value as `i`.

- Claim: Applying `VTask.finSumFinEquiv` to `Sum.inr i` (for `i : Fin n`) yields `Fin.natAdd m i`, i.e., the element of `Fin (m + n)` with numeric value `m + i`.

- Claim: The inverse `VTask.finSumFinEquiv.symm` applied to `Fin.castAdd n x` returns `Sum.inl x`, recovering the original left-summand element.

- Claim: The inverse `VTask.finSumFinEquiv.symm` applied to `Fin.natAdd m x` returns `Sum.inr x`, recovering the original right-summand element.

- Claim: When `m = 2` and `n = 3`, the forward map sends `Sum.inl ⟨1, by omega⟩ : Fin 2 ⊕ Fin 3` to the element `⟨1, by omega⟩ : Fin 5`, and `Sum.inr ⟨0, by omega⟩` to `⟨2, by omega⟩ : Fin 5`.

### Boundaries

- **`m = 0`**: `Fin 0` is empty, so the left summand contributes no elements. The equivalence restricts to an isomorphism between `Fin 0 ⊕ Fin n ≅ Fin n`, and it behaves correctly: only `Sum.inr` inputs are possible, and they map via `Fin.natAdd 0`, which is the identity (since adding 0 does not shift indices).
- **`n = 0`**: Symmetrically, the right summand `Fin 0` is empty. The equivalence becomes `Fin m ⊕ Fin 0 ≅ Fin m`; only `Sum.inl` inputs are possible, and they map via `Fin.castAdd 0`.
- **`m = 0, n = 0`**: Both summands are empty, and `Fin 0 ⊕ Fin 0 ≅ Fin 0` is the unique equivalence between empty types.
- The ordering convention is **left-then-right**: elements from `Fin m` occupy the lower block of indices, and elements from `Fin n` occupy the upper block.

### Not to be confused with

- `Fin.castAdd` / `Fin.natAdd`: These are the individual injections used to construct the forward map; `VTask.finSumFinEquiv` packages both into a single invertible equivalence.
- `Equiv.sumComm`: Swaps the two summands `α ⊕ β ≃ β ⊕ α`; composing this with `VTask.finSumFinEquiv` gives an equivalence that places the right block first, which corresponds to `Fin (n + m)` rather than `Fin (m + n)`.
- `finCongr`: An equivalence `Fin m ≃ Fin n` arising purely from a proof that `m = n`, with no sum structure involved.