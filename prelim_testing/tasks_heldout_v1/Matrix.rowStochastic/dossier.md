## Object

`VTask.rowStochastic R n` is the submonoid of all **row-stochastic matrices** over a square index type `n` with coefficients in an ordered semiring `R`. A matrix belongs to this collection if and only if every entry is nonnegative and every row sums to 1. The collection is closed under matrix multiplication and contains the identity matrix, making it a submonoid of the full matrix monoid under multiplication.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.rowStochastic : (R : Type u_3) -> (n : Type u_4) -> [Fintype n] -> [DecidableEq n] -> [Semiring R] -> [PartialOrder R] -> [IsOrderedRing R] -> Submonoid (Matrix n n R)
<!-- PINNED-SIGNATURE:END -->


`VTask.rowStochastic : (R : Type u_3) -> (n : Type u_4) -> [Fintype n] -> [DecidableEq n] -> [Semiring R] -> [PartialOrder R] -> [IsOrderedRing R] -> Submonoid (Matrix n n R)`

The first argument `R` is the coefficient ring (or semiring) in which matrix entries live; it must carry a compatible partial order so that nonnegativity of entries is meaningful. The second argument `n` is the (finite) index type that simultaneously parameterises rows and columns, so the matrices are square of size `|n|`. The typeclass arguments supply the required algebraic and order structure on `R` and the computability conditions on `n`.

## Conventions

The row-sum condition is stated as multiplication of the matrix on the right by the all-ones vector yielding the all-ones vector; equivalently, for every row index `i`, the sum over all column indices `j` of `M i j` equals 1. There are no junk-value conventions to declare for this definition, because membership is a purely logical predicate with no degenerate input regimes.

## Worked examples

- Claim: The 1×1 identity matrix over ℝ (with the single index `Fin 1`) is row-stochastic, since its only entry is 1 ≥ 0 and its unique row sums to 1.

- Claim: A 2×2 matrix over ℝ with all entries equal to 1/2 is row-stochastic: every entry satisfies 0 ≤ 1/2, and each row sums to 1/2 + 1/2 = 1.

- Claim: Any permutation matrix (the matrix `σ.permMatrix R` for a permutation `σ`) is a member of `VTask.rowStochastic R n`, because each row contains exactly one entry equal to 1 and all others 0.

- Claim: The set of row-stochastic matrices over a linear-ordered field forms a convex set.

## Boundaries

- When `n` is the empty type, the unique 0×0 matrix is vacuously row-stochastic (there are no entries to check and no rows to sum), so `VTask.rowStochastic R n` contains exactly that one element.
- When `n` has a single element (`Fin 1`), the only row-stochastic matrix is the 1×1 matrix `[[1]]`.
- Every entry `M i j` of a row-stochastic matrix satisfies both `0 ≤ M i j` and `M i j ≤ 1`, so entries are automatically bounded in [0, 1].
- The identity matrix is always a member, as it is the monoid's identity element.
- Row-stochastic matrices preserve nonneg vectors and stochastic vectors under both left (vecMul) and right (mulVec) multiplication.
- Transposing a row-stochastic matrix yields a column-stochastic matrix, and vice versa.
- Reindexing a row-stochastic matrix (via a pair of equivalences between index types) yields a row-stochastic matrix over the new index type.

## Not to be confused with

- `colStochastic R n`: The analogous submonoid of **column-stochastic** matrices, where every column (not every row) sums to 1; a row-stochastic matrix is column-stochastic if and only if its transpose is row-stochastic.
- `doublyStochastic R n`: Matrices that are simultaneously row- and column-stochastic, a strictly smaller collection.
- The plain carrier set `(VTask.rowStochastic R n : Set (Matrix n n R))`: This is the underlying set of row-stochastic matrices without the monoid structure; the submonoid additionally remembers closure under multiplication and the identity.