## Object

Given a (non-tagged) prepartition `π` of a box `I` in `ι`-dimensional space, and for each box `J` a tagged prepartition `πi J` of that box `J`, `VTask.biUnionTagged π πi` is the tagged prepartition of `I` obtained by taking all the small boxes appearing in every `πi J` (for `J ∈ π`) together, and equipping each small box with the tag assigned to it by the appropriate `πi J`. In other words, it is the "hierarchical join": first subdivide `I` via `π`, then subdivide each piece `J` via `πi J`, and carry along the tags from those sub-partitions.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.biUnionTagged : {ι : Type u_1} -> {I : BoxIntegral.Box ι} -> (π : BoxIntegral.Prepartition I) -> (πi : (J : BoxIntegral.Box ι) → BoxIntegral.TaggedPrepartition J) -> BoxIntegral.TaggedPrepartition I
<!-- PINNED-SIGNATURE:END -->


`VTask.biUnionTagged : {ι : Type u_1} -> {I : BoxIntegral.Box ι} -> (π : BoxIntegral.Prepartition I) -> (πi : (J : BoxIntegral.Box ι) → BoxIntegral.TaggedPrepartition J) -> BoxIntegral.TaggedPrepartition I`

The implicit argument `ι` is the index type parameterising the dimension of the ambient space. The implicit argument `I` is the ambient box being partitioned. The argument `π` is the coarse prepartition of `I` (without tags) whose boxes will each be further subdivided. The argument `πi` is a family of tagged prepartitions, one for each box of the same type; in practice the relevant ones are those indexed by the boxes `J` that appear in `π`. The result is a tagged prepartition of the original box `I`.

## Conventions

The function `πi` is defined on **all** boxes of type `BoxIntegral.Box ι`, not merely on those that appear in `π`; values of `πi` at boxes outside `π` are ignored and do not affect the result. Each small box in the output inherits its tag from the tagged prepartition `πi J` of the unique `J ∈ π` that contains it, as determined by the internal index function; this means the tag of a small box always lies inside the corresponding `J ∈ π`, hence inside `I`.

## Worked examples

- Claim: If `π` is the trivial single-box prepartition of `I` (containing only `I` itself) and `πi I` is a tagged prepartition `τ` of `I`, then `VTask.biUnionTagged π πi` has the same boxes and tags as `τ`.

- Claim: If every `πi J` for `J ∈ π` is the single-box tagged prepartition of `J` (tagging `J` with some point in `J`), then the boxes of `VTask.biUnionTagged π πi` are exactly the boxes of `π`, each tagged by the point chosen in its own `πi J`.

- Claim: A box `K` belongs to `VTask.biUnionTagged π πi` if and only if there exists some `J` belonging to `π` such that `K` belongs to `πi J`.

- Claim: The underlying (non-tagged) prepartition of `VTask.biUnionTagged π πi` equals the binary union `π.biUnion (fun J => (πi J).toPrepartition)`.

## Boundaries

- If `π` is the empty prepartition (containing no boxes), the result is the empty tagged prepartition of `I`, regardless of `πi`.
- If some `πi J` for `J ∈ π` is empty, the boxes of `J` contribute nothing to the result; the overall result can still be non-empty if other boxes in `π` have non-empty tagged prepartitions.
- Values of `πi` at boxes `J` that do **not** belong to `π` are entirely ignored.
- The tag of each box `K` in the result is always guaranteed to lie in the closed interval (the `Icc`) of `I`, because each tag lies in the `Icc` of its own sub-box `J ∈ π`, and each such `J` is contained in `I`.

## Not to be confused with

- `BoxIntegral.Prepartition.biUnion`: the non-tagged version, which produces a `Prepartition` (no tag data) by the same hierarchical union construction.
- `BoxIntegral.TaggedPrepartition.biUnionPrepartition`: a variant where the coarse partition itself is tagged and the fine sub-partitions may be untagged.
- `BoxIntegral.TaggedPrepartition.unionComplTagged`: combines a tagged prepartition with a tagged prepartition of the complement, rather than subdividing each piece separately.