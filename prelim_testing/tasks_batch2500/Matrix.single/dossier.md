## VTask.single

### Object
`VTask.single i j a` is the matrix over index types `m` (rows) and `n` (columns) with the scalar `a` placed at position `(i, j)` and the zero element `0` of the coefficient type `α` placed at every other position. It is the matrix analogue of a "standard basis vector" or "indicator" construction, but for a single matrix entry.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.single : {m : Type u_2} -> {n : Type u_3} -> {α : Type u_7} -> [DecidableEq m] -> [DecidableEq n] -> [Zero α] -> (i : m) -> (j : n) -> (a : α) -> Matrix m n α
<!-- PINNED-SIGNATURE:END -->


The implicit type arguments fix the row-index type `m`, the column-index type `n`, and the entry type `α`, together with decidable-equality instances for `m` and `n` (needed to compare row and column indices) and a `Zero` instance for `α` (supplying the fill value). The explicit argument `i : m` is the row index at which `a` is placed; `j : n` is the column index at which `a` is placed; `a : α` is the entry value placed at position `(i, j)`.

### Conventions

When the value `a` equals the zero element of `α`, `VTask.single i j 0` is still well-defined and equals the all-zeros matrix; there is no special case or junk value. The construction requires only a `Zero` instance on `α`, not any ring or semiring structure, so it applies in very general settings.

### Worked examples

- Claim: The entry of `VTask.single i j a` at position `(i, j)` equals `a`.
- Claim: The entry of `VTask.single i j a` at any position `(i', j')` with `(i', j') ≠ (i, j)` equals `0`.
- Claim: For `m = n = Fin 2` and `α = ℤ`, `VTask.single 0 1 (5 : ℤ)` is the 2×2 integer matrix with `5` at row 0, column 1 and `0` elsewhere; in particular its `(0,0)` entry is `0`, its `(0,1)` entry is `5`, and its `(1,0)` and `(1,1)` entries are `0`.
- Claim: `VTask.single i j a` is related to `Pi.single`: the matrix is equal to `Matrix.of (Pi.single i (Pi.single j a))`.
- Claim: The transpose of `VTask.single i j a` is `VTask.single j i a` (with rows and columns swapped).

### Boundaries

- If `m` or `n` is an empty type, the resulting matrix has no entries; `VTask.single` still type-checks and produces the unique matrix over those index types.
- If `m` is a singleton type so that there is only one possible row index, then `i` is forced and the matrix collapses to a single row.
- Setting `a = 0` produces the zero matrix; the construction does not distinguish this case.
- The types `m` and `n` need not be finite; however, operations like matrix multiplication that use `VTask.single` may additionally require `Fintype` hypotheses on the index types.

### Not to be confused with

- `Pi.single i a` — a function `m → α` that equals `a` at `i` and `0` elsewhere; this is a one-dimensional analogue, not a matrix.
- `Matrix.diagonal d` — places entries along the diagonal of a *square* matrix; `VTask.single` can place an entry anywhere, including off-diagonal, and works for rectangular matrices.
- `Matrix.stdBasisMatrix` (if present under another name) — some libraries use a similar name for the same concept; make sure you are working with the version from `Data/Matrix/Basis.lean`.
