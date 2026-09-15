## 1. Object

A matrix `A` over a commutative ring `R` is **totally unimodular** if every square submatrix obtained by selecting any subset of rows and any subset of columns (each selection given as an injective map from a finite index set) has determinant equal to `0`, `1`, or `-1`. Equivalently, the determinant of every such square submatrix lies in the image of the canonical sign-type embedding into `R`.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsTotallyUnimodular : {m : Type u_1} -> {n : Type u_3} -> {R : Type u_5} -> [CommRing R] -> (A : Matrix m n R) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.IsTotallyUnimodular : {m : Type u_1} -> {n : Type u_3} -> {R : Type u_5} -> [CommRing R] -> (A : Matrix m n R) -> Prop
```

The implicit type `m` is the row-index type of the matrix; `n` is the column-index type; `R` is the coefficient ring, which must be a commutative ring. The single explicit argument `A` is the matrix being tested for total unimodularity.

## 3. Conventions

The submatrices considered are those formed by choosing `k` distinct rows (via an injective function `Fin k → m`) and `k` distinct columns (via an injective function `Fin k → n`) for any natural number `k`, including `k = 0`. The empty (`0 × 0`) submatrix has determinant `1` by convention (the empty product), which lies in the range of `SignType.cast`, so the `k = 0` case imposes no constraint. There is no restriction that `m` or `n` be finite types; the property quantifies over all finite selections.

## 4. Worked examples

- Claim: The `2 × 2` identity matrix over `ℤ` is totally unimodular, because every square submatrix has determinant in `{-1, 0, 1}`.

- Claim: The `1 × 1` matrix `[[2]]` over `ℤ` is **not** totally unimodular, because selecting its single row and single column yields a `1 × 1` submatrix with determinant `2`, which is not in the range of `SignType.cast`.

- Claim: Any matrix with an empty row-index type satisfies `VTask.IsTotallyUnimodular`, since there are no rows to select and every submatrix selection either has `k = 0` (trivially satisfied) or cannot inject into the empty row set.

- Claim: If `A` is totally unimodular, then its transpose `Aᵀ` is also totally unimodular.

- Claim: If `A` is totally unimodular and `f : m' → m`, `g : n' → n` are arbitrary functions, then the submatrix `A.submatrix f g` is also totally unimodular.

## 5. Boundaries

- **`k = 0` (empty submatrix):** The determinant of the `0 × 0` matrix is `1` by convention, which is `SignType.cast SignType.pos`, so this case is always satisfied and imposes no constraint on `A`.
- **All-zero matrix:** The all-zeros matrix is totally unimodular because every square submatrix has determinant `0 = SignType.cast SignType.zero`.
- **Non-injectivity not considered:** If the row or column selection functions are not injective, the resulting submatrix is not required to have determinant in `{-1, 0, 1}` as part of the definition; only injective selections matter. (However, a related lemma shows the injectivity requirement is actually redundant: the condition without injectivity implies the condition with it.)
- **Single entries:** As a special case (`k = 1`), each individual entry of `A` must lie in the range of `SignType.cast`, i.e., must be `0`, `1`, or `-1`.
- **Empty column type:** A matrix whose column-index type is empty is trivially totally unimodular.

## 6. Not to be confused with

- **`Matrix.det`**: The determinant of the full matrix `A` itself — total unimodularity is a condition on *all* square submatrices, not just the determinant of `A`.
- **Unimodular matrix** (a square matrix with determinant `±1`): A unimodular matrix need not be totally unimodular; total unimodularity is a strictly stronger, global condition applying to all submatrices.
- **`Matrix.submatrix`**: This is the operation that selects rows and columns; `VTask.IsTotallyUnimodular` is the *property* that all such selections yield determinants in `{-1, 0, 1}`, not the submatrix construction itself.