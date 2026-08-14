## VTask.ofRowLens

### Object

Given a weakly-decreasing list of non-negative integers `w = [w₀, w₁, …, wₙ₋₁]`, this construction produces the Young diagram whose `i`-th row (0-indexed, from the top) has exactly `wᵢ` cells. The result is a finite subset of `ℕ × ℕ` that forms a lower set under the product order, i.e., a proper Young diagram in English convention: a cell `(i, j)` belongs to the diagram if and only if `i < w.length` and `j < w[i]`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofRowLens : (w : List ℕ) -> (hw : w.SortedGE) -> YoungDiagram
<!-- PINNED-SIGNATURE:END -->


The first argument `w` is the list of row lengths, listed from the topmost row downward; each entry is a natural number giving the width of that row. The second argument `hw` is a proof that `w` is sorted in weakly-decreasing (≥) order, which is the combinatorial condition ensuring the resulting shape is a genuine Young diagram (each row is at least as long as the one below it).

### Conventions

If an entry `wᵢ` equals zero, that row contributes no cells to the diagram; rows of length zero are tolerated by the construction, but the canonical `rowLens` of a Young diagram omits trailing zeros, so a round-trip through `rowLens` will strip any trailing zero entries from `w`.

### Worked examples

- Claim: The cell `(0, 2)` belongs to `VTask.ofRowLens [3, 2, 1] (by decide)` because row 0 has width 3 and `2 < 3`.

- Claim: The cell `(1, 2)` does NOT belong to `VTask.ofRowLens [3, 2, 1] (by decide)` because row 1 has width 2 and `2 < 2` is false.

- Claim: For `w = [4, 4, 2, 1]` (a valid weakly-decreasing list), the row length of row `⟨0, by decide⟩` in `VTask.ofRowLens w hw` is 4, matching `w[0]`.

- Claim: For `w = [2, 1]`, the resulting Young diagram has exactly `2 + 1 = 3` cells in rows 0 and 1 respectively, and `(1, 0)` is a member while `(2, 0)` is not (since `w.length = 2`).

### Boundaries

- **Empty list**: `VTask.ofRowLens [] (trivial proof)` produces the empty Young diagram (no cells at all), since there are no rows.
- **All-zero list**: A list like `[0, 0, 0]` satisfies `SortedGE` and produces the empty Young diagram; however, the canonical `rowLens` of that diagram is `[]`, not `[0, 0, 0]`, so the round-trip identity `rowLens ∘ ofRowLens = id` holds only when all entries are positive.
- **Singleton list**: `[k]` for any `k : ℕ` gives a one-row diagram with `k` cells in row 0.
- **Trailing zeros**: Allowed as input but stripped by the round-trip; if all entries are strictly positive, `rowLens (ofRowLens w hw) = w` holds.

### Not to be confused with

- `YoungDiagram.rowLens`: The *projection* from a Young diagram back to its list of row lengths; `ofRowLens` is its (partial) inverse constructor.
- `YoungDiagram.cellsOfRowLens`: The raw `Finset` of cells associated to the row-length list, without the `YoungDiagram` wrapper or the `isLowerSet` proof.
- A Young diagram specified by *column* lengths (i.e., the conjugate partition): `ofRowLens` always interprets `w` as row lengths, never column lengths.