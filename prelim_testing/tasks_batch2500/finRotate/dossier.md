## Object

For a natural number `n`, `VTask.finRotate n` is the permutation of the set `{0, 1, …, n−1}` (represented as `Fin n`) that shifts every element one step to the right cyclically: element `i` moves to `i + 1` for `i < n − 1`, and the last element `n − 1` wraps around to `0`. It is an element of the symmetric group on `Fin n`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.finRotate : (n : ℕ) -> Equiv.Perm (Fin n)
<!-- PINNED-SIGNATURE:END -->


`VTask.finRotate : (n : ℕ) -> Equiv.Perm (Fin n)`

The single argument `n` is the size of the finite set being permuted; the result is the one-step right-rotation permutation on `Fin n`.

## Conventions

When `n = 0`, the domain `Fin 0` is empty, so `VTask.finRotate 0` is necessarily the identity (the unique permutation of the empty set). When `n = 1`, the domain is a singleton, so `VTask.finRotate 1` is again the identity permutation. For `n ≥ 2`, `VTask.finRotate n` is a genuine cyclic permutation of order `n` whose support is all of `Fin n`.

## Worked examples

- Claim: `VTask.finRotate 3` maps `⟨0, by omega⟩` to `⟨1, by omega⟩`.

- Claim: `VTask.finRotate 4` maps `⟨3, by omega⟩` (the last element) to `⟨0, by omega⟩` (zero), wrapping around.

- Claim: The sign of `VTask.finRotate 5` equals `(-1) ^ (5 - 1) = 1`, so the rotation is an even permutation.

- Claim: For `n ≥ 2`, the support of `VTask.finRotate n` is all of `Fin n` (every element is moved).

## Boundaries

- **`n = 0`**: `Fin 0` is empty; `VTask.finRotate 0` is the identity equivalence on the empty type.
- **`n = 1`**: `Fin 1` is a singleton; the only element maps to itself, so `VTask.finRotate 1` is the identity.
- **`n = 2`**: The permutation swaps `0` and `1`; it has order 2 and its support is `{0, 1}`.
- **Last element**: For any `n + 1`, the last element `⟨n, …⟩` is mapped to `⟨0, …⟩`, the only wrap-around case.
- **All other elements**: For `i < n` in `Fin (n + 1)`, the image has underlying natural number `i + 1`.

## Not to be confused with

- **`Equiv.Perm.cycleOf`**: extracts the cycle containing a particular element from an arbitrary permutation, rather than constructing the canonical rotation permutation on `Fin n`.
- **`Fin.cycleRange`**: a related but distinct permutation that generates a cycle among a contiguous range of `Fin n`, not necessarily the full one-step right rotation.
- **`finAddFlip`**: the building block that swaps the two halves of `Fin (n + 1)`, used internally to construct the rotation but not itself a cyclic rotation.
