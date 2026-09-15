## Object

`VTask.toSquareBlock M b k` is the **principal block submatrix** of a square matrix `M` corresponding to a given block label `k`. More precisely, given a function `b` that assigns a label in `β` to each index in `m`, the block labeled `k` consists of all rows and columns whose index maps to `k` under `b`. The result is a square matrix whose rows and columns are both indexed by the subtype `{ a : m // b a = k }` — the fiber of `b` over `k` — and whose `(i, j)` entry is the entry `M i j` of the original matrix (viewing the subtype elements as elements of `m` via the coercion).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toSquareBlock : {m : Type u_2} -> {α : Type u_12} -> {β : Type u_13} -> (M : Matrix m m α) -> (b : m → β) -> (k : β) -> Matrix { a // b a = k } { a // b a = k } α
<!-- PINNED-SIGNATURE:END -->


`VTask.toSquareBlock : {m : Type u_2} -> {α : Type u_12} -> {β : Type u_13} -> (M : Matrix m m α) -> (b : m → β) -> (k : β) -> Matrix { a // b a = k } { a // b a = k } α`

- `M` is the ambient square matrix, indexed by some type `m` on both rows and columns, with entries in `α`.
- `b` is the **block-labeling function**, assigning to each index in `m` a label in `β`; it partitions the index set into fibers (blocks).
- `k` is the **block label** selecting which block to extract; the resulting matrix is indexed by the fiber `{ a : m // b a = k }`.

## Conventions

No special junk-value or boundary conventions are declared: the definition is total, and whenever the fiber `{ a // b a = k }` is empty (i.e., no index maps to `k`), the result is the unique `0 × 0` matrix (a matrix over an empty index type), which is perfectly well-formed.

## Worked examples

- Claim: For the 3×3 identity matrix over ℕ with block function `b i = i % 2` and label `k = 0`, the block submatrix has rows/columns indexed by even-residue indices, and its `(⟨0, rfl⟩, ⟨0, rfl⟩)` entry equals the original `(0, 0)` entry.

- Claim: For a 2×2 matrix `M = !![a, b; c, d]` with block function `b = id` and label `k = 0`, `VTask.toSquareBlock M id 0` is a 1×1 matrix whose single entry is `M 0 0 = a`.

- Claim: When `b` is a constant function (all indices map to the same label `k`), `VTask.toSquareBlock M b k` is the whole matrix `M` (up to the canonical identification of `m` with `{ a // b a = k }`).

- Claim: When `b i = i` (the identity labeling on a `Fin n` type), `VTask.toSquareBlock M id i` is a 1×1 matrix with sole entry `M i i` — consistent with `Matrix.det_toSquareBlock_id`.

## Boundaries

- **Empty fiber**: If no index `a : m` satisfies `b a = k`, then `{ a // b a = k }` is empty, and the result is a `0×0` matrix — the unique matrix of that type. This is valid and causes no error.
- **Full fiber**: If every index satisfies `b a = k`, then `{ a // b a = k }` is isomorphic to `m`, and the block is essentially all of `M`.
- **Single-element fiber**: The block is a 1×1 matrix; its determinant equals the single diagonal entry `M i i` (as confirmed by `det_toSquareBlock_id` when `b = id`).
- **Type of labels `β`**: No ordering or decidability on `β` is required just to form the block; additional structure is only needed for theorems about determinant factorizations.

## Not to be confused with

- `Matrix.toSquareBlockProp M p`: the analogous construction using a *predicate* `p : m → Prop` rather than a labeling function and a specific label; `toSquareBlock M b k` is definitionally `toSquareBlockProp M (fun a => b a = k)`.
- `Matrix.toBlock M p q`: extracts a (potentially *non-square*) submatrix using separate row-predicate `p` and column-predicate `q`, which need not be equal.
- `Matrix.BlockTriangular M b`: a *property* of a matrix asserting that `M` is block-upper-triangular with respect to the labeling `b`; this is a proposition about `M`, not a submatrix extraction.
