## Object

`VTask.colStochastic R n` is the submonoid of all *column-stochastic* square matrices with entries in `R` and row/column index type `n`. A matrix belongs to this submonoid if and only if (1) every entry is nonnegative, and (2) the entries in each column sum to 1. It is a submonoid of the monoid of `n × n` matrices under multiplication, meaning it contains the identity matrix and is closed under matrix multiplication.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.colStochastic : (R : Type u_3) -> (n : Type u_4) -> [Fintype n] -> [DecidableEq n] -> [Semiring R] -> [PartialOrder R] -> [IsOrderedRing R] -> Submonoid (Matrix n n R)
<!-- PINNED-SIGNATURE:END -->


`VTask.colStochastic : (R : Type u_3) -> (n : Type u_4) -> [Fintype n] -> [DecidableEq n] -> [Semiring R] -> [PartialOrder R] -> [IsOrderedRing R] -> Submonoid (Matrix n n R)`

The first argument `R` is the scalar ring over which the matrices are defined; it must be an ordered semiring (with `PartialOrder` and `IsOrderedRing`) so that nonnegativity of entries is meaningful. The second argument `n` is the (finite, decidable-equality) index type that simultaneously parameterises rows and columns, so the matrices are square of size `|n| × |n|`.

## Conventions

There are no junk-value or degenerate-input conventions to declare: the definition is total over all valid type-class combinations, and the submonoid structure is well-formed for every valid instantiation.

## Worked examples

- Claim: The identity matrix over `ℝ` with index type `Fin 2` is column stochastic, since its column sums are all 1 and all entries are nonnegative.

- Claim: Any permutation matrix (the matrix of a permutation σ acting on `n`) is column stochastic, because each column has exactly one entry equal to 1 and all others 0, so column sums are 1 and all entries are nonneg.

- Claim: The product of two column-stochastic matrices over an ordered ring is again column stochastic — this follows from the submonoid closure property baked into `VTask.colStochastic`.

- Claim: For a matrix `M` in `VTask.colStochastic R n` and a nonneg vector `x`, the matrix-vector product `M *ᵥ x` is again nonneg — the column-stochastic property preserves nonnegativity of vectors under left multiplication.

- Claim: The set underlying `VTask.colStochastic R n` (when `R` is a linear-ordered field like `ℝ`) is a convex set in the vector space of matrices.

## Boundaries

- When `n` is the empty type (`Fin 0`), every matrix is vacuously column stochastic (there are no columns whose sums could fail to equal 1, and no entries that could be negative), so the submonoid equals the full matrix monoid in that case.
- When `n` has a single element (`Fin 1`), the only column-stochastic matrix is the `1 × 1` matrix with entry `1`.
- The scalar type `R` must be an ordered semiring satisfying `IsOrderedRing`; in particular `ℝ`, `ℚ`, and `ℤ` are valid, but a field with no ordering (like `ℂ` with its standard lack of total order) would not instantiate the required type classes.
- Each entry of a column-stochastic matrix is automatically between 0 and 1 (inclusive), since individual entries are nonneg and they sum to 1 per column.

## Not to be confused with

- `Matrix.rowStochastic R n`: the analogous submonoid of *row*-stochastic matrices, where every *row* sums to 1; a matrix is column stochastic if and only if its transpose is row stochastic.
- `Matrix.doublyStochastic R n`: matrices that are simultaneously row- and column-stochastic (all row sums and all column sums equal 1).
- `Matrix.substochastic` or sub-stochastic matrices: matrices where column (or row) sums are at most 1 rather than exactly 1, which is a strictly weaker condition.