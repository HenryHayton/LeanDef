## VTask.IsSubordinate

### Object

Given a bump covering — a collection of continuous functions `f i : X → ℝ` indexed by `ι`, each taking values in `[0, 1]` and forming a covering of a set `s` in a topological space `X` — the predicate `VTask.IsSubordinate f U` asserts that this bump covering is **subordinate** to the open family `U : ι → Set X`. Subordination means that for every index `i`, the closure of the support of `f i` (the topological support, i.e., the closure of the set of points where `f i` is non-zero) is entirely contained in `U i`. Informally: each bump function "lives inside" the corresponding member of the covering family.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsSubordinate : {ι : Type u} -> {X : Type v} -> [TopologicalSpace X] -> {s : Set X} -> (f : BumpCovering ι X s) -> (U : ι → Set X) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsSubordinate : {ι : Type u} -> {X : Type v} -> [TopologicalSpace X] -> {s : Set X} -> (f : BumpCovering ι X s) -> (U : ι → Set X) -> Prop`

The implicit type `ι` is the index type shared by the bump covering and the target family. The implicit type `X` is the topological space in which everything lives; it carries the implicit `TopologicalSpace` instance. The implicit set `s` is the subset of `X` that the bump covering covers. The explicit argument `f` is the bump covering under consideration. The explicit argument `U` is the family of sets indexed by `ι` to which the bump covering is required to be subordinate.

### Conventions

There are no special junk-value or boundary conventions to declare: the predicate is a universally quantified inclusion and is simply false (not vacuously meaningful in any special way) when the topological support of some `f i` is not contained in `U i`; when `ι` is an empty type the predicate holds vacuously for any `f` and `U`.

### Worked examples

- Claim: If `f` is subordinate to `U` and each `U i` is contained in `V i`, then `f` is subordinate to `V`. (Monotonicity: `VTask.IsSubordinate.mono` states that `f.IsSubordinate U` and `∀ i, U i ⊆ V i` together imply `f.IsSubordinate V`.)

- Claim: On a normal paracompact space, for any closed set `s`, any open cover `U` of `s` indexed by `ι`, there exists a bump covering of `s` that is subordinate to `U`. (Existence: `VTask.exists_isSubordinate` guarantees `∃ f : BumpCovering ι X s, f.IsSubordinate U` under those hypotheses.)

- Claim: If `f` is a bump covering subordinate to `U`, then the induced partition of unity `f.toPartitionOfUnity` is also subordinate to `U`. (Transfer: `VTask.IsSubordinate.toPartitionOfUnity` asserts that subordination is preserved under the canonical map from bump coverings to partitions of unity.)

- Claim: If `f` is a bump covering subordinate to `U` and each `f i` is smooth of class `C^∞`, then the smooth partition of unity built from `f` is also subordinate to `U`. (Smooth transfer: `VTask.IsSubordinate.toSmoothPartitionOfUnity` asserts this.)

### Boundaries

- **Empty index type:** When `ι` is empty, the universal quantification `∀ i, tsupport (f i) ⊆ U i` holds vacuously, so every bump covering over an empty index type is subordinate to every family `U`.
- **Trivially large `U`:** If `U i = X` for all `i`, then `VTask.IsSubordinate f U` holds for every bump covering `f`, since any set is a subset of the whole space.
- **Disjoint support and wrong set:** If even a single index `i₀` has a point in `tsupport (f i₀)` that lies outside `U i₀`, the whole predicate is false, regardless of how well-behaved all other indices are.
- **Closed versus open target sets:** The definition places no openness requirement on the sets `U i`; subordination is purely a topological-support containment condition. The open-cover hypotheses appear only in the existence theorems, not in the definition itself.

### Not to be confused with

- **`PartitionOfUnity.IsSubordinate`**: The analogous subordination predicate for a partition of unity (where the functions sum to 1 on `s`), rather than merely a bump covering. A bump covering subordinate to `U` induces a partition of unity also subordinate to `U`, but the two predicates live on different types.
- **`SmoothBumpCovering.IsSubordinate`**: The subordination notion for smooth bump coverings on manifolds, which tracks subordination to a family indexed by the base points of the covering rather than directly by `ι`.
- **Support containment without closure (`support (f i) ⊆ U i`)**: Subordination uses the *topological* support (closure of the support), a strictly stronger requirement than mere support containment. A function can have support inside `U i` while its closure escapes `U i`.