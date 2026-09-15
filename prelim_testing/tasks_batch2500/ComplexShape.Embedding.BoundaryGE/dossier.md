## VTask.BoundaryGE

### Object

Given an embedding `e` of one complex shape into another, `VTask.BoundaryGE e j` is a proposition asserting that the index `j` (in the source shape) sits at the **lower boundary** of the embedding. Concretely, it means two things simultaneously: (1) the predecessor of `e.f j` in the target shape actually exists and is related to `e.f j` by the target relation, and (2) that predecessor is **not** in the image of the embedding — no source index maps to it. In other words, `j` is an entry point of the embedded subcomplex: something in the target sits directly below it, but that something lies outside the embedded region.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.BoundaryGE : {ι : Type u_1} -> {ι' : Type u_2} -> {c : ComplexShape ι} -> {c' : ComplexShape ι'} -> (e : c.Embedding c') -> (j : ι) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.BoundaryGE : {ι : Type u_1} -> {ι' : Type u_2} -> {c : ComplexShape ι} -> {c' : ComplexShape ι'} -> (e : c.Embedding c') -> (j : ι) -> Prop`

The implicit arguments `ι` and `ι'` are the index types for the source and target complex shapes respectively. The implicit arguments `c` and `c'` are the source and target complex shapes (each specifying a grading and a relation between consecutive indices). The explicit argument `e` is the embedding of `c` into `c'`, providing in particular an injective map `e.f : ι → ι'` compatible with the relations. The explicit argument `j` is the source index being tested for lower-boundary membership.

### Conventions

No junk-value or edge conventions are declared for this definition: it is a `Prop`-valued predicate whose truth value is fully determined by the mathematical data, and there is no out-of-domain input to assign a default to.

### Worked examples

- Claim: If `e.IsTruncLE` holds (the embedding is a truncation from above), then no index `j` satisfies `VTask.BoundaryGE e j`; i.e., the lower boundary is empty under this hypothesis.

- Claim: If `c.Rel j k` holds (j immediately precedes k in the source shape) and `e` satisfies `IsRelIff`, then `VTask.BoundaryGE e k` is false — an index that has a predecessor inside the embedded region cannot be at the lower boundary.

- Claim: If `i'` is an index in the target shape satisfying `c'.Rel i' (e.f j)`, and no source index maps to `i'` (i.e., `∀ i, e.f i ≠ i'`), then `VTask.BoundaryGE e j` holds.

- Claim: If `VTask.BoundaryGE e j` holds and `i'` satisfies `c'.Rel i' (e.f j)`, then for every source index `a`, `e.f a ≠ i'` — the predecessor of `e.f j` in the target is confirmed to lie outside the image.

### Boundaries

- If the complex shape embedding has no predecessor of `e.f j` in the target shape (the target's predecessor relation does not hold for any `i'` relative to `e.f j`), then `VTask.BoundaryGE e j` is false, since the first conjunct fails.
- If every predecessor of `e.f j` in the target is itself in the image of `e.f`, then `VTask.BoundaryGE e j` is false, since the second conjunct fails.
- When the embedding is a truncation from above (`IsTruncLE`), `VTask.BoundaryGE e j` is always false for every `j`.
- The predicate is stable in the sense that once `VTask.BoundaryGE e j` fails and `IsRelIff` holds, the next index (and any further successor) also fails to satisfy `VTask.BoundaryGE`.

### Not to be confused with

- `ComplexShape.Embedding.BoundaryLE`: the **upper** boundary predicate, which instead looks at successors of `e.f j` lying outside the image, rather than predecessors.
- `ComplexShape.Embedding.IsRelIff`: a condition on the embedding relating source and target relations bidirectionally; it is a hypothesis often needed to reason about `VTask.BoundaryGE`, not the predicate itself.
- `ComplexShape.prev`: the function computing the predecessor index in a complex shape; `VTask.BoundaryGE` uses it as part of its definition, but the two are distinct concepts.
