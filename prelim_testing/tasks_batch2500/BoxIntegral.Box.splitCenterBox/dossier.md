## Object

Given an axis-aligned box `I` in `ι`-dimensional space (where `ι` indexes the coordinate directions), the hyperplanes through the center of `I`—one perpendicular to each axis—slice `I` into `2^(card ι)` sub-boxes of equal volume. `VTask.splitCenterBox I s` selects one of these `2^(card ι)` sub-boxes, determined by the subset `s ⊆ ι`: for each coordinate `i`, the sub-box occupies the **upper** half-interval `[(lower i + upper i)/2, upper i]` if `i ∈ s`, and the **lower** half-interval `[lower i, (lower i + upper i)/2]` if `i ∉ s`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.splitCenterBox : {ι : Type u_1} -> (I : BoxIntegral.Box ι) -> (s : Set ι) -> BoxIntegral.Box ι
<!-- PINNED-SIGNATURE:END -->


`VTask.splitCenterBox : {ι : Type u_1} -> (I : BoxIntegral.Box ι) -> (s : Set ι) -> BoxIntegral.Box ι`

The implicit type `ι` is the index type whose elements label the coordinate axes. `I` is the ambient box being subdivided. `s` is the subset of coordinate indices that selects which half-interval to use in each dimension: coordinates in `s` contribute the upper half, coordinates outside `s` contribute the lower half.

## Conventions

Every valid subset `s` of `ι` (including the empty set and all of `ι`) yields a valid box, so the construction is total with no junk values; there are no special sentinel or degenerate-input conventions declared for this definition.

## Worked examples

- Claim: For a 1-dimensional box `I` with lower bound `0` and upper bound `1`, `VTask.splitCenterBox I ∅` has lower bound `0` and upper bound `1/2` (the lower half-box, since no index belongs to `∅`).

- Claim: For a 1-dimensional box `I` with lower bound `0` and upper bound `1`, `VTask.splitCenterBox I Set.univ` has lower bound `1/2` and upper bound `1` (the upper half-box, since every index belongs to `Set.univ`).

- Claim: For a 2-dimensional box with lower `(0, 0)` and upper `(2, 2)`, choosing `s = {0}` (first coordinate only) gives a sub-box whose lower corner is `(1, 0)` and upper corner is `(2, 1)` — the first coordinate takes its upper half and the second takes its lower half.

- Claim: `VTask.splitCenterBox I s` is always a sub-box of `I`, meaning its lower bounds are at least those of `I` and its upper bounds are at most those of `I`.

## Boundaries

- When `s = ∅`, every coordinate contributes its lower half, yielding the sub-box `[lower, center]` in all dimensions.
- When `s = Set.univ`, every coordinate contributes its upper half, yielding the sub-box `[center, upper]` in all dimensions.
- The center `(lower i + upper i) / 2` is strictly between `lower i` and `upper i` for every `i` (guaranteed by the box invariant `lower_lt_upper`), so every sub-box is itself a valid, non-degenerate box regardless of `s`.
- The `2^(card ι)` choices of `s` (as distinct subsets) yield pairwise essentially disjoint sub-boxes that together tile `I`; this tiling is captured by `BoxIntegral.Partition.splitCenter`.

## Not to be confused with

- `BoxIntegral.Partition.splitCenter`: the entire collection of all `2^(card ι)` sub-boxes packaged as a `Partition` of `I`, rather than a single selected sub-box.
- `BoxIntegral.Box.splitLower` / `BoxIntegral.Box.splitUpper`: hypothetical single-axis bisection operations, whereas `VTask.splitCenterBox` bisects simultaneously along all axes.
- `BoxIntegral.Box.face` or similar restriction operations: those fix a value in one dimension rather than selecting a half-interval in every dimension.