## Object

Given a composition `c` of a natural number `n` (i.e., an ordered list of positive parts that sum to `n`), `VTask.boundary c` is a strictly-monotone order embedding that maps each index `i` in `{0, 1, …, c.length}` to the cumulative sum of the first `i` block sizes, viewed as an element of `{0, 1, …, n}`. Concretely, index `i` maps to the left endpoint of the `i`-th block when the blocks are laid out consecutively on `{0, …, n-1}`, with the extra virtual index `c.length` mapping to `n` itself (one past the last block), representing the right boundary of the whole composition.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.boundary : {n : ℕ} -> (c : Composition n) -> Fin (c.length + 1) ↪o Fin (n + 1)
<!-- PINNED-SIGNATURE:END -->


VTask.boundary : {n : ℕ} -> (c : Composition n) -> Fin (c.length + 1) ↪o Fin (n + 1)

The implicit argument `n` is the integer being composed. The explicit argument `c` is a composition of `n`, specifying the ordered sequence of positive block sizes that sum to `n`. The result is a strictly-monotone order embedding from the `(c.length + 1)`-element index set — ranging over all block boundaries including a virtual right endpoint — into the `(n + 1)`-element set `{0, 1, …, n}` of positions in the composition.

## Conventions

The domain includes a virtual extra index beyond the last block: index `c.length` (i.e., `Fin.last c.length`) maps to `n` (i.e., `Fin.last n`), representing the right end of the entire composition rather than the start of any actual block. Index `0` always maps to `0`, representing the left end of the first block.

## Worked examples

- Claim: For the composition [2, 3] of 5, `VTask.boundary c 0 = 0` (the 0th boundary is the leftmost point).

- Claim: For the composition [2, 3] of 5, `VTask.boundary c (Fin.last 2) = Fin.last 5` (the last boundary is `n`).

- Claim: For any composition `c` of `n`, `VTask.boundary c 0 = 0`, i.e., `boundary_zero` holds: the 0th cumulative sum is 0.

- Claim: For a composition `c` of `n` with two blocks of sizes 1 and 2, the boundary at index 1 equals 1 (the sum of the first block alone).

## Boundaries

- At `i = 0`: the result is always `0 : Fin (n + 1)`, since the cumulative sum of zero blocks is 0.
- At `i = c.length` (the virtual last index): the result is always `n : Fin (n + 1)`, since all block sizes sum to `n`.
- The mapping is strictly monotone and injective (it is an order embedding), so no two distinct indices share the same boundary value.
- For a composition with a single block of size `n`, there are exactly two boundaries: `0` and `n`.
- The composition must have positive block sizes, so the boundary strictly increases at every step; no two consecutive boundaries coincide.

## Not to be confused with

- `Composition.sizeUpTo`: the raw natural-number function computing cumulative sums; `boundary` packages this into a verified order embedding into `Fin (n + 1)`.
- `Composition.boundaries`: the finset of all boundary values as a subset of `Finset (Fin (n + 1))`; `boundary` is the order embedding parametrising that finset by index.
- `Composition.blocksFun`: maps a `Fin c.length` index to the *size* of that block, not to its left endpoint position.