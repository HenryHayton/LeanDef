## VTask.disjUnion

### Object

Given a box `I` in `ι`-indexed Euclidean space and two prepartitions `π₁`, `π₂` of `I` whose covered regions are disjoint (as subsets of `ι → ℝ`), `VTask.disjUnion π₁ π₂ h` is the prepartition of `I` obtained by taking all the boxes from both `π₁` and `π₂` together. The result is again a valid prepartition: every box still lies inside `I`, and all pairs of distinct boxes remain mutually disjoint (guaranteed either by disjointness within each original prepartition, or by the cross-disjointness hypothesis `h`).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.disjUnion : {ι : Type u_1} -> {I : BoxIntegral.Box ι} -> (π₁ π₂ : BoxIntegral.Prepartition I) -> (h : Disjoint π₁.iUnion π₂.iUnion) -> BoxIntegral.Prepartition I
<!-- PINNED-SIGNATURE:END -->


The index type `ι` determines the ambient dimension. `I` is the ambient box that both prepartitions subdivide. `π₁` and `π₂` are the two prepartitions being combined. `h` is a proof that the region covered by `π₁` and the region covered by `π₂` are disjoint sets in `ι → ℝ`; this hypothesis is essential to ensure the combined collection is still a valid (pairwise-disjoint) prepartition.

### Conventions

No special junk-value or edge conventions are declared: the operation is only defined when the disjointness hypothesis `h` is satisfied, and the result is always a fully valid prepartition of `I`.

### Worked examples

- Claim: A box `J` belongs to `VTask.disjUnion π₁ π₂ h` if and only if it belongs to `π₁` or to `π₂`.

- Claim: The union of regions covered by `VTask.disjUnion π₁ π₂ h` equals the union of the two individual covered regions, i.e., `(VTask.disjUnion π₁ π₂ h).iUnion = π₁.iUnion ∪ π₂.iUnion`.

- Claim: The distortion of `VTask.disjUnion π₁ π₂ h` is the maximum of the distortions of `π₁` and `π₂`.

- Claim: If `π₂.iUnion = ↑I \ π₁.iUnion`, then `VTask.disjUnion π₁ π₂ h` is a partition of `I` (i.e., covers all of `I`).

### Boundaries

- If either `π₁` or `π₂` is the empty prepartition (containing no boxes), `VTask.disjUnion` reduces to the other prepartition; the disjointness hypothesis is trivially satisfied in that case.
- The hypothesis `h` must be a proof of disjointness of the *covered regions* (the geometric unions), not merely disjointness of the box collections as finsets. Two prepartitions could share the same box yet have the same geometric covered region only if that box appears in both, which would violate pairwise disjointness — so in practice the box sets will also be disjoint.
- When both prepartitions have the same ambient box `I`, the combined prepartition still has ambient box `I` unchanged.

### Not to be confused with

- `BoxIntegral.Prepartition.iUnion`: this is merely the *set-valued union* of a single prepartition's boxes, not a constructor combining two prepartitions.
- `BoxIntegral.Partition`: a partition is a prepartition that additionally covers all of `I`; `VTask.disjUnion` produces a prepartition (not necessarily a partition) unless the two pieces together tile `I`.
- Set-union of finsets of boxes without the prepartition structure: the raw union `π₁.boxes ∪ π₂.boxes` as a finset does not carry the validity proof that all boxes are sub-boxes of `I` and pairwise disjoint; `VTask.disjUnion` packages those proofs together.
