## Object

`VTask.D n` is the Cartan matrix of Dynkin type Dₙ — a symmetric integer square matrix of size n×n whose combinatorial structure encodes the root system of the simple Lie algebra **so**(2n) (the special orthogonal Lie algebra in even dimension 2n). Concretely, it is the matrix with 2 on the diagonal and entries −1 exactly at the pairs of simple roots that are adjacent in the Dₙ Dynkin diagram, including the characteristic forked tail at the end of that diagram.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.D : (n : ℕ) -> Matrix (Fin n) (Fin n) ℤ
<!-- PINNED-SIGNATURE:END -->


`VTask.D : (n : ℕ) -> Matrix (Fin n) (Fin n) ℤ`

The sole argument `n` is the *rank* of the root system, i.e., the size of the square matrix returned. The matrix rows and columns are both indexed by `Fin n`.

## Conventions

For small or degenerate values of `n` the definition still returns a well-typed matrix, but the result may not correspond to an irreducible rank-n root system of type D. Specifically, for `n ≤ 2` the off-diagonal entries are all 0, so `VTask.D 0` and `VTask.D 1` and `VTask.D 2` are simply scaled identity matrices (or the empty matrix for n = 0). There is a known coincidence `VTask.D 1 = VTask.A 1` and `VTask.D 3 ≅ VTask.A 3` (up to reindexing), reflecting classical isomorphisms of small-rank Lie algebras. These small cases are junk values from the Lie-algebra perspective but are assigned definite values by the definition.

## Worked examples

- Claim: Every diagonal entry of `VTask.D n` equals 2, i.e., `VTask.D n i i = 2` for all `i : Fin n`.

- Claim: Every off-diagonal entry of `VTask.D n` is ≤ 0 (the matrix is a valid Cartan matrix in terms of signs).

- Claim: `VTask.D 4` equals the 4×4 matrix with rows `[2,−1,0,0]`, `[−1,2,−1,−1]`, `[0,−1,2,0]`, `[0,−1,0,2]`, encoding the forked Dynkin diagram D₄.

- Claim: `VTask.D 2` is the 2×2 diagonal matrix `[[2,0],[0,2]]`, reflecting the fact that D₂ is a degenerate (disconnected) diagram.

- Claim: `VTask.D 3` equals `[[2,−1,−1],[−1,2,0],[−1,0,2]]`, which after reindexing agrees with the Cartan matrix of type A₃.

## Boundaries

- **n = 0**: Returns the unique 0×0 empty matrix over ℤ. Vacuously well-defined; no root system interpretation.
- **n = 1**: Returns the 1×1 matrix `[[2]]`. Coincides with `VTask.A 1`.
- **n = 2**: Returns the 2×2 matrix `[[2,0],[0,2]]` — a disconnected diagram, not a simple Lie algebra. All off-diagonal entries are 0 because the condition `n ≤ 2` forces them to be.
- **n = 3**: Returns the 3×3 matrix with the forked structure, which happens to be isomorphic to A₃ under a relabelling of simple roots.
- **n ≥ 4**: Returns the standard irreducible Dₙ Cartan matrix, symmetric with 2 on the diagonal, −1 for adjacent nodes in the chain, and the characteristic fork at position n−1 connecting to both n−2 and n−3.
- The matrix is always symmetric (no off-diagonal asymmetry, unlike type B/C Cartan matrices).
- Off-diagonal entries are always ≤ 0.

## Not to be confused with

- **`VTask.A n`** — the Cartan matrix of type Aₙ, a simple tridiagonal matrix corresponding to **sl**(n+1); coincides with `VTask.D n` only in degenerate cases (n=1, n=3 up to reindexing).
- **The adjacency matrix of the Dₙ Dynkin diagram** — that would be a 0/1 matrix; `VTask.D n` has 2 on the diagonal and −1 for adjacent pairs, not 1.
- **`VTask.B n` or `VTask.C n`** — the Cartan matrices of types B and C, which are *not* symmetric (they have asymmetric off-diagonal entries −1 and −2), unlike the simply-laced `VTask.D n`.