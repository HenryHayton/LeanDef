## Object

`VTask.finSigmaFinEquiv` is a canonical bijection (an equivalence of types) between the dependent pair type `(i : Fin m) × Fin (n i)` — whose elements are pairs of a "row index" `i` in `{0, …, m−1}` together with a "column index" in `{0, …, n(i)−1}` — and the single finite type `Fin (∑ i, n i)`, whose size is the total count of all entries across all rows. Concretely, it linearises a variable-width 2-D table into a single flat index, respecting the natural row-major ordering.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.finSigmaFinEquiv : {m : ℕ} -> {n : Fin m → ℕ} -> (i : Fin m) × Fin (n i) ≃ Fin (∑ i, n i)
<!-- PINNED-SIGNATURE:END -->


`{m : ℕ} -> {n : Fin m → ℕ} -> (i : Fin m) × Fin (n i) ≃ Fin (∑ i, n i)`

The implicit argument `m` is the number of "rows" (the outer index range). The implicit argument `n` is the function assigning to each row index `i : Fin m` the width `n i` of that row (the inner index range). The equivalence itself takes no explicit arguments; it is a proof-carrying bijection between the two types just described.

## Conventions

No special junk-value or out-of-range conventions are declared for this definition: as an `Equiv` it is a total bijection on the types as stated, and all cases (including `m = 0` and rows of width 0) are handled without any padding or undefined behaviour.

## Worked examples

- Claim: For `m = 2` with `n = ![2, 3]`, the total size is `Fin 5`, and the sigma pair `⟨0, 1⟩` (row 0, column 1) maps to the flat index `1`.

- Claim: For `m = 2` with `n = ![2, 3]`, the sigma pair `⟨1, 0⟩` (row 1, column 0) maps to flat index `2` (= width of row 0).

- Claim: For `m = 0` (no rows), the source type `(i : Fin 0) × Fin (n i)` is empty, and the target `Fin 0` is also empty; `VTask.finSigmaFinEquiv` is the unique equivalence between two empty types.

- Claim: The underlying natural-number value of `VTask.finSigmaFinEquiv ⟨i, j⟩` equals `(∑ k : Fin i, n (Fin.castLE i.2.le k)) + j.val`, i.e., it is the sum of all earlier row widths plus the column index within the current row.

## Boundaries

- When `m = 0`: both sides are empty types (`Fin 0` on the right, an uninhabited sigma on the left). The equivalence is valid and unique.
- When some `n i = 0`: the row `i` contributes no elements to the sigma type. Those rows are simply skipped in the flat enumeration.
- When all `n i = 0`: the sum is 0, the sigma type is empty, and the target is `Fin 0`; the equivalence is again between two empty types.
- The flat index assigned to `⟨i, j⟩` is exactly `(∑ k < i, n k) + j`, which stays strictly less than `∑ i, n i` as required for membership in the target `Fin`.

## Not to be confused with

- `Fin.sigma_equiv_sigma`: a different re-indexing that changes the dependent index rather than flattening to a single `Fin`.
- `finProdFinEquiv` (or `Fin.prod_univ`): the special case where `n` is a constant function, giving `Fin m × Fin k ≃ Fin (m * k)`; `VTask.finSigmaFinEquiv` generalises this to variable row widths.
- `Equiv.sigmaEquivProd`: an equivalence between a sigma type and a product type in a different, non-`Fin`-specific context.