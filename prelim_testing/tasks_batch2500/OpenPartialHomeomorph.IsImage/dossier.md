## VTask.IsImage

### Object

Given an open partial homeomorphism `e` from a topological space `X` to a topological space `Y`, a set `t ⊆ Y` is called an **image** of a set `s ⊆ X` under `e` if, at every point `x` in the domain of `e`, the image point `e x` lies in `t` if and only if `x` lies in `s`. Informally, `t` is the "shadow" of `s` under `e` as seen through the homeomorphism's domain: within that domain, membership in `s` and membership in `t` are perfectly interchangeable via the map.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsImage : {X : Type u_1} -> {Y : Type u_3} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> (e : OpenPartialHomeomorph X Y) -> (s : Set X) -> (t : Set Y) -> Prop
<!-- PINNED-SIGNATURE:END -->


The first implicit argument is the source topological space `X`; the second implicit argument is the target topological space `Y`, each equipped (via instance arguments) with their respective topologies. The explicit argument `e` is the open partial homeomorphism from `X` to `Y` through which the correspondence is measured. The argument `s` is the subset of `X` whose image relationship is being asserted, and `t` is the subset of `Y` that is claimed to be that image.

### Conventions

No junk-value or edge conventions have been declared for this definition. The predicate is a universally quantified proposition and is vacuously true whenever `e.source` is empty, since the quantifier over `e.source` then ranges over nothing.

### Worked examples

- Claim: For the identity open partial homeomorphism on ℝ (with full source), `VTask.IsImage e s s` holds — that is, any set is an image of itself under the identity map, since `e x = x` and so `e x ∈ s ↔ x ∈ s` is trivially true for all `x` in the source.

- Claim: If `e.source = ∅`, then `VTask.IsImage e s t` holds for any sets `s` and `t`, since the condition `∀ x ∈ e.source, e x ∈ t ↔ x ∈ s` is vacuously satisfied.

- Claim: The three characterisations stated in the docstring — (1) `e '' (e.source ∩ s) = e.target ∩ t`, (2) `e.source ∩ e ⁻¹' t = e.source ∩ s`, and (3) the pointwise biconditional — are all equivalent to `VTask.IsImage e s t`.

- Claim: If `VTask.IsImage e s t` and `x ∈ e.source`, then `x ∈ s ↔ e x ∈ t`.

### Boundaries

- **Empty source**: If `e.source = ∅`, the predicate holds for every pair `(s, t)`, because the universal quantification is vacuous.
- **Empty `s` and `t`**: `VTask.IsImage e ∅ ∅` holds whenever `e.source` is non-empty, but only if no point of the source maps into any set (which is consistent since both sides of the biconditional are `False` for all `x ∈ e.source`).
- **`t` outside `e.target`**: Points outside `e.target` are never in the range of `e` restricted to `e.source`, so `t` may contain arbitrary extra elements outside `e.target` without affecting the predicate; the condition only governs values `e x` for `x ∈ e.source`, which all lie in `e.target`.
- **Non-injectivity is not an issue**: The partial homeomorphism is a homeomorphism on its source/target, so injectivity is guaranteed there; the predicate is well-behaved throughout.

### Not to be confused with

- **`Set.image` (direct image)**: That is the set `e '' s`, the collection of actual output values, not a predicate asserting a correspondence between two given sets.
- **`PartialHomeomorph.IsImage`**: The analogous predicate for partial homeomorphisms (without the openness assumption on the image of open sets); `VTask.IsImage` specialises to open partial homeomorphisms.
- **`e.source ∩ s = e.symm '' (e.target ∩ t)`**: A re-arrangement that looks similar but conflates the direction of the correspondence; `VTask.IsImage` is symmetric in a precise sense given by the biconditional, not merely an image equality.