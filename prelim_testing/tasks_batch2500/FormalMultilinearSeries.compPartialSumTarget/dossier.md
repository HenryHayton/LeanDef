## Object

`VTask.compPartialSumTarget m M N` is a finite set (packaged as a `Finset`) of dependent pairs `⟨n, c⟩` where `n` is a natural number and `c` is a composition of `n`. It serves as the target index set in the change-of-variables formula used to compute the composition of two formal power series truncated to partial sums. Concretely, a pair `⟨n, c⟩` belongs to this set when the composition `c` of the integer `n` is "compatible" with the truncation parameters: the number of blocks of `c` lies in the range `[m, M)` and every block size is at most `N`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.compPartialSumTarget : (m M N : ℕ) -> Finset ((n : ℕ) × Composition n)
<!-- PINNED-SIGNATURE:END -->


`VTask.compPartialSumTarget : (m M N : ℕ) -> Finset ((n : ℕ) × Composition n)`

The first argument `m` is the lower bound (inclusive) on the number of parts of the composition. The second argument `M` is the upper bound (exclusive) on the number of parts of the composition. The third argument `N` is the upper bound (exclusive) on each individual part size: every block of the composition must be strictly less than `N`.

## Conventions

There are no declared junk-value or edge conventions beyond the natural set-theoretic behaviour: when the parameter constraints are contradictory or yield an empty collection (e.g., `m ≥ M`, or `N = 0` preventing any block sizes), the resulting `Finset` is simply empty.

## Worked examples

- Claim: The pair `⟨2, Composition.mk [1, 1] (by decide)⟩` belongs to `VTask.compPartialSumTarget 2 3 2`, since the composition `[1,1]` of `2` has exactly `2` parts (in `[2,3)`) and every part equals `1 < 2`.

- Claim: `VTask.compPartialSumTarget 0 1 1` is empty, because if `M = 1` then the only eligible compositions would have `0` parts (an empty composition of `0`), but every block must be strictly less than `N = 1`, i.e., less than `1`, which is impossible for any non-empty block; the single zero-part composition has `n = 0` and vacuously passes, so the set contains exactly `⟨0, (empty composition of 0)⟩`.

- Claim: For any `m M N`, if `M ≤ m` then `VTask.compPartialSumTarget m M N` is empty, since there is no natural number in the half-open interval `[m, M)` when `M ≤ m`.

- Claim: The pair `⟨3, c⟩` for the composition `c = [1, 2]` of `3` belongs to `VTask.compPartialSumTarget 2 3 3`, as it has `2` parts (in `[2,3)`) and all parts are less than `3`.

## Boundaries

- When `N = 0`: no composition can have all parts strictly less than `0`, so the finset is empty regardless of `m` and `M`.
- When `M = 0` or `M ≤ m`: the number-of-parts constraint `[m, M)` is empty, so the finset is empty.
- When `m = 0` and `M = 1`: only the empty composition of `0` (zero parts) qualifies, provided `N ≥ 1` (the vacuous block-size condition is satisfied), giving a singleton finset.
- Large values of `M` and `N` cause the finset to grow as more compositions are included.

## Not to be confused with

- `compPartialSumSource` (or its `Finset` version): the *source* index set in the same change-of-variables, consisting of tuples `(k, blocks)` rather than `(n, Composition n)`.
- `Composition n`: the type of a single composition of a fixed integer `n`, not a finset of compositions.
- `Finset.sigma`: the generic construction of a dependent-pair finset from a base finset and fibre finsets, which is a general tool and does not encode the partial-sum truncation conditions.