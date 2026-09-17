## Object

A **prepartition** of a box `I` in `ℝⁿ` is a finite collection of pairwise non-overlapping sub-boxes of `I`. `VTask.single I J h` is the simplest possible prepartition of `I`: the singleton collection containing exactly one box, namely `J`, where `J ≤ I` (i.e., `J` is a sub-box of `I`).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.single : {ι : Type u_1} -> (I J : BoxIntegral.Box ι) -> (h : J ≤ I) -> BoxIntegral.Prepartition I
<!-- PINNED-SIGNATURE:END -->


`VTask.single : {ι : Type u_1} -> (I J : BoxIntegral.Box ι) -> (h : J ≤ I) -> BoxIntegral.Prepartition I`

The implicit argument `ι` is the index type parametrising the coordinate directions (e.g., `Fin n` for an `n`-dimensional ambient space). The first explicit argument `I` is the ambient box being partitioned. The second explicit argument `J` is the single sub-box that forms the entire prepartition. The proof argument `h` is the evidence that `J` is indeed a sub-box of `I` (i.e., `J ≤ I` in the partial order on boxes).

## Conventions

There are no junk-value conventions: the definition is total and well-defined for any `J ≤ I`; the proof `h` is required and ensures that the single-element collection is a valid prepartition.

## Worked examples

- Claim: For any index type `ι` and boxes `I J : BoxIntegral.Box ι` with `h : J ≤ I`, the box `J` is a member of `VTask.single I J h`.

- Claim: For any index type `ι` and boxes `I J K : BoxIntegral.Box ι` with `h : J ≤ I` and `hKJ : K ≠ J`, the box `K` is not a member of `VTask.single I J h`.

- Claim: For any `ι` and boxes `I J` with `h : J ≤ I`, the underlying finite set of `VTask.single I J h` has cardinality 1.

- Claim: The prepartition `VTask.single I I (le_refl I)` consists of `I` itself, which is the maximal sub-box of `I`.

## Boundaries

- When `J = I` (with `h` being `le_refl I`), the singleton prepartition covers `I` completely, making it a full partition (not merely a prepartition) of `I`.
- When `J` is a proper sub-box of `I` (`J < I`), the prepartition does not cover all of `I`; it is a genuine prepartition rather than a partition.
- The collection always has exactly one element; it is never empty.
- The non-overlapping condition (required of any prepartition) is trivially satisfied by a singleton.

## Not to be confused with

- `BoxIntegral.Prepartition.top I`: the "full" or "trivial" prepartition of `I` by `I` itself — this is the same as `VTask.single I I (le_refl I)`, but `top` is reached via a different construction path.
- `BoxIntegral.Box.le`: the sub-box ordering used in `h`; it is a relation between boxes, not itself a prepartition.
- `BoxIntegral.Partition I`: a prepartition that additionally covers `I` entirely; `VTask.single I J h` is a `Partition` only when `J = I`.