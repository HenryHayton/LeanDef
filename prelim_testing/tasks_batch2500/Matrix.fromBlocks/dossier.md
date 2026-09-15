## Object

Given four matrices `A`, `B`, `C`, `D` of compatible dimensions,
`VTask.fromBlocks A B C D` assembles them into a single block matrix arranged as a 2×2 grid of blocks:

```
[ A  B ]
[ C  D ]
```

The rows of the result are indexed by the disjoint union `n ⊕ o` (rows from `A`/`B` come first via `Sum.inl`, rows from `C`/`D` come second via `Sum.inr`), and the columns are indexed by `l ⊕ m` (columns from `A`/`C` come first via `Sum.inl`, columns from `B`/`D` come second via `Sum.inr`). Each entry of the large matrix is the corresponding entry from whichever sub-block it falls into.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.fromBlocks : {l : Type u_1} -> {m : Type u_2} -> {n : Type u_3} -> {o : Type u_4} -> {α : Type u_12} -> (A : Matrix n l α) -> (B : Matrix n m α) -> (C : Matrix o l α) -> (D : Matrix o m α) -> Matrix (n ⊕ o) (l ⊕ m) α
<!-- PINNED-SIGNATURE:END -->


`VTask.fromBlocks : {l : Type u_1} -> {m : Type u_2} -> {n : Type u_3} -> {o : Type u_4} -> {α : Type u_12} -> (A : Matrix n l α) -> (B : Matrix n m α) -> (C : Matrix o l α) -> (D : Matrix o m α) -> Matrix (n ⊕ o) (l ⊕ m) α`

The implicit type arguments `l`, `m`, `n`, `o` are the index types for the four blocks, and `α` is the entry type. `A` is the upper-left block, with row-index type `n` and column-index type `l`. `B` is the upper-right block, with row-index type `n` and column-index type `m`. `C` is the lower-left block, with row-index type `o` and column-index type `l`. `D` is the lower-right block, with row-index type `o` and column-index type `m`. The result has row-index type `n ⊕ o` and column-index type `l ⊕ m`.

## Conventions

No special junk-value or out-of-domain conventions are declared: the function is total and well-defined for all matrices of the given types.

## Worked examples

- Claim: The upper-left entry (i.e., at `(Sum.inl i, Sum.inl j)`) of `VTask.fromBlocks A B C D` equals `A i j`.
  ```lean
  example {n l m o α : Type*} (A : Matrix n l α) (B : Matrix n m α)
      (C : Matrix o l α) (D : Matrix o m α) (i : n) (j : l) :
      VTask.fromBlocks A B C D (Sum.inl i) (Sum.inl j) = A i j := rfl
  ```

- Claim: The upper-right entry (i.e., at `(Sum.inl i, Sum.inr j)`) of `VTask.fromBlocks A B C D` equals `B i j`.
  ```lean
  example {n l m o α : Type*} (A : Matrix n l α) (B : Matrix n m α)
      (C : Matrix o l α) (D : Matrix o m α) (i : n) (j : m) :
      VTask.fromBlocks A B C D (Sum.inl i) (Sum.inr j) = B i j := rfl
  ```

- Claim: The lower-left entry (i.e., at `(Sum.inr i, Sum.inl j)`) of `VTask.fromBlocks A B C D` equals `C i j`.
  ```lean
  example {n l m o α : Type*} (A : Matrix n l α) (B : Matrix n m α)
      (C : Matrix o l α) (D : Matrix o m α) (i : o) (j : l) :
      VTask.fromBlocks A B C D (Sum.inr i) (Sum.inl j) = C i j := rfl
  ```

- Claim: The lower-right entry (i.e., at `(Sum.inr i, Sum.inr j)`) of `VTask.fromBlocks A B C D` equals `D i j`.
  ```lean
  example {n l m o α : Type*} (A : Matrix n l α) (B : Matrix n m α)
      (C : Matrix o l α) (D : Matrix o m α) (i : o) (j : m) :
      VTask.fromBlocks A B C D (Sum.inr i) (Sum.inr j) = D i j := rfl
  ```

## Boundaries

- The function is total: it is defined for any four matrices whose row and column types satisfy the indicated pairing constraints (the two upper blocks share row-index type `n`, the two lower blocks share `o`, the two left blocks share `l`, and the two right blocks share `m`).
- There is no restriction on the entry type `α`; it need not have any algebraic structure.
- When any of the index types is empty (e.g., `o = Empty`), the corresponding rows/columns simply do not appear in the result; the construction still type-checks and is well-defined.
- The ordering within each block is preserved: rows from `A`/`B` are accessed via `Sum.inl`, and rows from `C`/`D` via `Sum.inr`.

## Not to be confused with

- `Matrix.blockDiagonal`: builds a block-diagonal matrix from a family of matrices indexed by a type, rather than a fixed 2×2 grid of four blocks.
- `Matrix.reindex`: reindexes rows and columns of a matrix via equivalences, without combining separate matrices into a larger one.
- Direct matrix concatenation along a single axis (e.g., stacking just rows or just columns): `VTask.fromBlocks` always combines four sub-blocks arranged in a 2×2 pattern.
