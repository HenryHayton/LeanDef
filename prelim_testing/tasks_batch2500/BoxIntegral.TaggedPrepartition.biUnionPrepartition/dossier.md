## VTask.biUnionPrepartition

### Object

Given a tagged prepartition `π` of a box `I` (a finite collection of non-overlapping sub-boxes of `I`, each carrying a distinguished tag point) and, for every box `J`, an (untagged) prepartition `πi J` of `J`, this construction produces a new tagged prepartition of `I` whose boxes are precisely the union of all boxes appearing in the individual `πi J` for `J ∈ π`. Each small box in the result inherits its tag from the tag that `π` assigned to the unique box of `π` that contains it. Boxes from `πi J` for `J ∉ π` are not included.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.biUnionPrepartition : {ι : Type u_1} -> {I : BoxIntegral.Box ι} -> (π : BoxIntegral.TaggedPrepartition I) -> (πi : (J : BoxIntegral.Box ι) → BoxIntegral.Prepartition J) -> BoxIntegral.TaggedPrepartition I
<!-- PINNED-SIGNATURE:END -->


The first argument `π` is the outer tagged prepartition of the ambient box `I`; it supplies both the coarse subdivision of `I` and the tag points. The second argument `πi` is a family of untagged prepartitions indexed by boxes: for each box `J` (anywhere, not just those in `π`), `πi J` is an untagged prepartition of `J`; only the values at boxes `J` that actually belong to `π` contribute to the result.

### Conventions

For a small box `B` that does not belong to any box of `π`, the tag-lookup function still returns a value (the tag of a canonical default box), but such boxes never appear in the result, so the tag value is irrelevant.

### Worked examples

- Claim: If `π` is a tagged prepartition of `I` and every `πi J` is empty (the trivial prepartition with no boxes), then `π.biUnionPrepartition πi` contains no boxes.

- Claim: If `π` consists of a single tagged box `J` with tag `t`, and `πi J` subdivides `J` into boxes `B₁, B₂`, then `π.biUnionPrepartition πi` contains exactly `B₁` and `B₂`, both carrying tag `t`.

- Claim: If `π` is a tagged partition of `I` (covers all of `I`) and each `πi J` is also a partition of `J`, then `π.biUnionPrepartition πi` is a tagged partition of `I`.

- Claim: The distortion of `π.biUnionPrepartition πi` equals the supremum over boxes `J ∈ π` of the distortion of `πi J`.

### Boundaries

- When `πi J` is empty for all `J`, the result is the empty tagged prepartition of `I` (no boxes).
- When `π` is itself empty (no boxes), the result is also empty regardless of `πi`.
- The construction does not guarantee a Henstock condition: even if `π` is a Henstock tagged partition, the result need not be Henstock, because the tags are inherited from the coarser partition and may lie outside the finer boxes.
- If `π` is a tagged partition and each `πi J` is a partition of `J`, then the result is a tagged partition of `I`.
- Subordination is preserved: if `π` is subordinate to a gauge `r`, so is the result.

### Not to be confused with

- `BoxIntegral.TaggedPrepartition.biUnion` (a variant that takes a family of *tagged* prepartitions and can carry distinct tags at the fine level, rather than inheriting tags from the coarse level).
- `BoxIntegral.Prepartition.biUnion` (the untagged version, which produces a plain prepartition with no tag data).
- `BoxIntegral.TaggedPrepartition.unionCompl` (extends a prepartition to cover all of `I` using a complementary piece, a different kind of union operation).