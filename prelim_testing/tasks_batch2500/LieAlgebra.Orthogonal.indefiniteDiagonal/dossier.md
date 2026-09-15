## Object

The indefinite diagonal matrix is a square matrix indexed by a disjoint-union type `p ⊕ q`, whose diagonal entries are `1` for indices coming from `p` (via `Sum.inl`) and `-1` for indices coming from `q` (via `Sum.inr`), with all off-diagonal entries equal to `0`. This is the canonical representative of an indefinite quadratic form with `|p|` positive directions and `|q|` negative directions, used for instance to encode Minkowski-type metrics.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.indefiniteDiagonal : (p : Type u_2) -> (q : Type u_3) -> (R : Type u₂) -> [DecidableEq p] -> [DecidableEq q] -> [CommRing R] -> Matrix (p ⊕ q) (p ⊕ q) R
<!-- PINNED-SIGNATURE:END -->


VTask.indefiniteDiagonal : (p : Type u_2) -> (q : Type u_3) -> (R : Type u₂) -> [DecidableEq p] -> [DecidableEq q] -> [CommRing R] -> Matrix (p ⊕ q) (p ⊕ q) R

The first argument `p` is the index type for the positive (value `1`) diagonal block. The second argument `q` is the index type for the negative (value `-1`) diagonal block. The third argument `R` is the commutative ring in which the matrix entries live. The implicit `DecidableEq` instances on `p` and `q` are required to define diagonal matrices (equality of indices must be decidable). The `CommRing` instance on `R` provides the ring structure needed for the constants `1` and `-1`.

## Conventions

All off-diagonal entries — regardless of whether the row and column indices are in the same summand or different summands — are `0`; only same-index pairs on the diagonal are nonzero.

## Worked examples

- Claim: The `(Sum.inl 0, Sum.inl 0)` diagonal entry of `VTask.indefiniteDiagonal (Fin 2) (Fin 3) ℤ` equals `1`.
  ```lean
  example : VTask.indefiniteDiagonal (Fin 2) (Fin 3) ℤ (Sum.inl 0) (Sum.inl 0) = 1 := by decide
  ```

- Claim: The `(Sum.inr 0, Sum.inr 0)` diagonal entry of `VTask.indefiniteDiagonal (Fin 2) (Fin 3) ℤ` equals `-1`.
  ```lean
  example : VTask.indefiniteDiagonal (Fin 2) (Fin 3) ℤ (Sum.inr 0) (Sum.inr 0) = -1 := by decide
  ```

- Claim: The off-diagonal entry `(Sum.inl 0, Sum.inl 1)` of `VTask.indefiniteDiagonal (Fin 2) (Fin 3) ℤ` equals `0`.
  ```lean
  example : VTask.indefiniteDiagonal (Fin 2) (Fin 3) ℤ (Sum.inl 0) (Sum.inl 1) = 0 := by decide
  ```

- Claim: The mixed entry `(Sum.inl 0, Sum.inr 0)` of `VTask.indefiniteDiagonal (Fin 2) (Fin 3) ℤ` equals `0`.
  ```lean
  example : VTask.indefiniteDiagonal (Fin 2) (Fin 3) ℤ (Sum.inl 0) (Sum.inr 0) = 0 := by decide
  ```

## Boundaries

- If `p` is an empty type (e.g., `Fin 0`), the matrix is purely a `(-1)`-diagonal block over `q`, equivalent to the negation of the identity on `q`.
- If `q` is an empty type, the matrix is purely a `1`-diagonal block over `p`, i.e., the identity matrix on `p`.
- If both `p` and `q` are empty, the matrix is the unique `0 × 0` matrix.
- The matrix is symmetric (it equals its own transpose) because all off-diagonal entries are `0`.
- The matrix squares to the identity matrix (`M * M = 1`) when `2` is invertible in `R`, since each diagonal entry is `±1` and `(±1)² = 1`.

## Not to be confused with

- `Matrix.diagonal`: a general diagonal matrix from an arbitrary function `p → R`; the indefinite diagonal is the special case where the index set is `p ⊕ q` and the function is `Sum.elim (const 1) (const -1)`.
- `Matrix.one` (identity matrix): that matrix has all diagonal entries equal to `1`; the indefinite diagonal replaces the `q`-block diagonal entries with `-1`.
- A block-diagonal matrix built from two blocks: the indefinite diagonal is diagonal (not merely block-diagonal), so there are no off-block-diagonal entries either.