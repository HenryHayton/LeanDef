## 1. Object

Given a family of matrices `M`, one matrix `M i` of size `m'(i) × n'(i)` for each index `i` in some type `o`, `VTask.blockDiagonal' M` assembles them into a single large matrix whose rows are indexed by the dependent sum `Σ i, m' i` and whose columns are indexed by `Σ i, n' i`. The entry at row `⟨k, r⟩` and column `⟨k', c⟩` equals `M k r c` when `k = k'`, and `0` otherwise. In other words, the constituent matrices appear as non-overlapping diagonal blocks, with every off-block entry set to zero.

This is the dependently-typed generalisation of the ordinary block-diagonal construction: while the non-dependent version requires every block to share the same row-index type and the same column-index type, here each block `M i` may have its own distinct row-index type `m' i` and column-index type `n' i`.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.blockDiagonal' : {o : Type u_4} -> {m' : o → Type u_7} -> {n' : o → Type u_8} -> {α : Type u_12} -> [DecidableEq o] -> [Zero α] -> (M : (i : o) → Matrix (m' i) (n' i) α) -> Matrix ((i : o) × m' i) ((i : o) × n' i) α
<!-- PINNED-SIGNATURE:END -->


`VTask.blockDiagonal' : {o : Type u_4} -> {m' : o → Type u_7} -> {n' : o → Type u_8} -> {α : Type u_12} -> [DecidableEq o] -> [Zero α] -> (M : (i : o) → Matrix (m' i) (n' i) α) -> Matrix ((i : o) × m' i) ((i : o) × n' i) α`

- `o` is the type that indexes the family of blocks; each value of `o` identifies one diagonal block.
- `m'` is a function assigning to each block index its row-index type; `m' i` is the type whose elements label the rows of the `i`-th block.
- `n'` is the analogous function for column-index types.
- `α` is the scalar type of the matrix entries.
- The `DecidableEq o` instance is needed to decide, for any two block indices `k` and `k'`, whether they are equal; this equality check determines whether an entry is inside a diagonal block or in an off-block position.
- The `Zero α` instance supplies the zero value used to fill all off-block positions.
- `M` is the family of matrices being assembled: for each `i : o` it provides a matrix with rows in `m' i` and columns in `n' i`.

The result is a matrix with rows indexed by dependent pairs `⟨i, r⟩` (block index together with a row within that block) and columns indexed by dependent pairs `⟨i, c⟩`.

## 3. Conventions

When the row block-index `k` equals the column block-index `k'`, the entry at `⟨k, i⟩`, `⟨k', j⟩` is exactly the entry `M k i j` of the corresponding diagonal block. When `k ≠ k'`, the entry is unconditionally `0`, regardless of the values of `i` and `j`.

## 4. Worked Examples

- Claim: For any family `M` of matrices over an index type with `DecidableEq`, the entry `VTask.blockDiagonal' M ⟨k, i⟩ ⟨k, j⟩` equals `M k i j` (on-diagonal block entry).

- Claim: For any family `M` and distinct block indices `k ≠ k'`, the entry `VTask.blockDiagonal' M ⟨k, i⟩ ⟨k', j⟩` equals `0` (off-diagonal block entry).

- Claim: `VTask.blockDiagonal' (0 : ∀ i, Matrix (m' i) (n' i) α) = 0` — assembling a family of zero matrices yields the zero matrix.

- Claim: For a family of identity matrices (when `m' = n'` and `α` has a `One` with compatible `DecidableEq`), `VTask.blockDiagonal' (1 : ∀ i, Matrix (m' i) (m' i) α) = 1` — the block-diagonal of identity blocks is the identity.

- Claim: `VTask.blockDiagonal'` is injective: if `VTask.blockDiagonal' M = VTask.blockDiagonal' N` then `M = N`.

## 5. Boundaries

- **Empty index type**: If `o` is the empty type, the resulting matrix is the unique `(Σ i, m' i) × (Σ i, n' i)` matrix, which is itself empty (no rows and no columns), and is vacuously zero.
- **Single-element index type**: With `|o| = 1`, the result is simply the single block `M` (up to the isomorphism between `Σ i, m' i` and `m' (the unique element)`).
- **Off-diagonal entries are always `0`**: The zero-fill is strict; there is no optional or partial fill — every position `⟨k, i⟩`, `⟨k', j⟩` with `k ≠ k'` is `0` by definition.
- **Dependent types**: Because each block may have a different index type, the equality check on block indices must be handled with care, in particular when types `m' k` and `m' k'` differ; the off-diagonal case avoids any type mismatch by returning `0` directly.

## 6. Not to be confused with

- `Matrix.blockDiagonal` — the non-dependent version where all blocks share the same row-index type `m` and column-index type `n`; `VTask.blockDiagonal'` strictly generalises this.
- `Matrix.blockDiag'` — the *inverse* operation that extracts the family of diagonal blocks from a block-structured matrix; `blockDiag' ∘ blockDiagonal' = id`.
- `Matrix.fromBlocks` — assembles exactly four explicitly named blocks (top-left, top-right, bottom-left, bottom-right) into a 2×2 block matrix; not a general block-diagonal construction.