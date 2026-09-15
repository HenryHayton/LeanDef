## Object

A *tagged prepartition* of a box `I` in `ℝ^ι` is a finite collection of non-overlapping sub-boxes of `I`, each equipped with a *tag* point that lies in the closed hull of `I`. `VTask.single I J hJ x h` is the tagged prepartition of `I` that contains exactly one sub-box, namely `J`, and assigns the tag `x` to that sub-box (and to every member of the collection, vacuously for all other positions).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.single : {ι : Type u_1} -> (I J : BoxIntegral.Box ι) -> (hJ : J ≤ I) -> (x : ι → ℝ) -> (h : x ∈ BoxIntegral.Box.Icc I) -> BoxIntegral.TaggedPrepartition I
<!-- PINNED-SIGNATURE:END -->


`VTask.single : {ι : Type u_1} -> (I J : BoxIntegral.Box ι) -> (hJ : J ≤ I) -> (x : ι → ℝ) -> (h : x ∈ BoxIntegral.Box.Icc I) -> BoxIntegral.TaggedPrepartition I`

- `ι` is the index type parameterising the coordinate directions (usually a finite type such as `Fin n`).
- `I` is the ambient box of which the result is a tagged prepartition.
- `J` is the single sub-box that will appear in the collection.
- `hJ` is the proof that `J` is indeed a sub-box of `I` (i.e. `J ≤ I` in the partial order on boxes).
- `x` is the tag point, a function `ι → ℝ` representing a point of `ℝ^ι`.
- `h` is the proof that `x` belongs to the closed box `[I]` (the closed hull of `I`), which is required for a valid tag.

## Conventions

Every member of the collection is assigned the same tag `x`; there is no per-box tag variation possible in this single-box construction. When `J = I` and `x ∈ [I]`, the result is a full tagged partition of `I` (not merely a prepartition). The Henstock condition holds precisely when the tag `x` also lies in the closed hull of the sub-box `J` itself, not merely in the larger `[I]`.

## Worked examples

- Claim: The only box in `VTask.single I J hJ x h` is `J`; for any box `J'`, `J' ∈ VTask.single I J hJ x h ↔ J' = J`.

- Claim: The union of the boxes in `VTask.single I J hJ x h` equals `J` (as a set in `ℝ^ι`).

- Claim: `VTask.single I J hJ x h` is a tagged partition of `I` if and only if `J = I`.

- Claim: When `J = I`, i.e. using `VTask.single I I le_rfl x h`, the result is a Henstock tagged partition whenever `x ∈ [I]`.

## Boundaries

- When `J = I` (the sub-box exhausts the ambient box) and `x ∈ [I]`, the single-element tagged prepartition is a full partition (`IsPartition`) and is automatically Henstock, since `x ∈ [I] = [J]`.
- When `J` is strictly smaller than `I`, the result is a proper prepartition (not a partition), and it is Henstock only if `x ∈ [J]`; having `x ∈ [I] \ [J]` is allowed by the type but violates the Henstock condition.
- The distortion of the tagged prepartition equals the distortion of `J` alone, regardless of the tag point.
- The index type `ι` is not required to be finite for the basic construction, though finiteness of `ι` is needed for certain properties such as subordinateness.

## Not to be confused with

- `BoxIntegral.Prepartition.single` — the untagged version; it carries no tag point and is not a `TaggedPrepartition`.
- `BoxIntegral.TaggedPrepartition` (the type itself) — the general structure containing many tagged boxes, of which `VTask.single` is the minimal one-box instance.
- A tagged *partition* (`IsPartition`) — `VTask.single I J hJ x h` is only a partition when `J = I`; otherwise it leaves uncovered area inside `I`.