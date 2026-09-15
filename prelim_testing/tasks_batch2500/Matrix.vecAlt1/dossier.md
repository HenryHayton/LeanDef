## VTask.vecAlt1

### Object

`VTask.vecAlt1` selects the odd-indexed elements from a finite vector of even length, returning a new vector of half the length. Concretely, given a vector `v` of length `m = 2n`, the output vector has length `n`, and its `k`-th entry (for `k : Fin n`) is `v[2k + 1]` — that is, the element at position `2k + 1` in the original vector (0-indexed). Equivalently, it picks out the elements at positions 1, 3, 5, … from the original vector.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.vecAlt1 : {α : Type u} -> {m n : ℕ} -> (hm : m = n + n) -> (v : Fin m → α) -> (k : Fin n) -> α
<!-- PINNED-SIGNATURE:END -->


The implicit argument `α` is the element type of the vector. The implicit natural numbers `m` and `n` represent the length of the input vector and the length of the output vector, respectively. The argument `hm` is a proof that `m = n + n`, witnessing that the input length is exactly twice the output length (this is required to guarantee that `2k + 1 < m` for every valid index `k`). The argument `v` is the input vector, represented as a function from `Fin m` to `α`. The argument `k` is the index into the output vector, a value in `Fin n`.

### Conventions

The proof argument `hm : m = n + n` is mathematically inert — it is used only to establish the well-typedness of the index arithmetic, and does not affect the computed value. Any two proofs of `m = n + n` yield definitionally equal results.

### Worked examples

- Claim: For the vector `![a, b, c, d]` (length 4, so n = 2), `VTask.vecAlt1 rfl ![a, b, c, d] 0 = b` (the element at position 2·0 + 1 = 1).

- Claim: For the vector `![a, b, c, d]` (length 4, so n = 2), `VTask.vecAlt1 rfl ![a, b, c, d] 1 = d` (the element at position 2·1 + 1 = 3).

- Claim: For the vector `![p, q, r, s, t, u]` (length 6, so n = 3), `VTask.vecAlt1 rfl ![p, q, r, s, t, u] 2 = u` (the element at position 2·2 + 1 = 5).

- Claim: Applying `VTask.vecAlt1` to the empty vector of length 0 yields the empty vector: `VTask.vecAlt1 rfl (![] : Fin 0 → α) = ![]`.

### Boundaries

- When `n = 0`, the output vector is empty (there are no valid `k : Fin 0`), and the function produces the unique function from `Fin 0 → α`, regardless of `v`.
- The index `2k + 1` always lies strictly within `[0, m)` for any `k : Fin n` when `m = 2n`, so no out-of-bounds access can occur; this is enforced by the proof `hm`.
- The proof `hm` must satisfy `m = n + n` (not `n + n = m`); swapping the equality would require `hm.symm` at the call site.
- The function picks **odd** positions (1, 3, 5, …), not even positions (0, 2, 4, …). The companion `vecAlt0` handles even positions.

### Not to be confused with

- `vecAlt0`: the analogous function selecting **even-indexed** elements (positions 0, 2, 4, …) rather than odd-indexed ones.
- `vecHead`: extracts only the very first element of a vector, not every other element.
- `Matrix.submatrix` or row/column selection: those operate on 2D matrices, whereas `VTask.vecAlt1` operates on 1D vectors (functions from `Fin n`).