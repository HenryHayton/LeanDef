## VTask.Specializes

### Object

`VTask.Specializes x y`, written `x ⤳ y`, is the *specialization preorder* relation on a topological space. It asserts that the point `x` *specializes to* the point `y`: intuitively, `y` is "more general" or "further from being closed" than `x`, in the sense that every neighbourhood of `y` already contains `x`. Equivalently, `y` lies in the closure of the singleton `{x}`, or every closed set containing `x` also contains `y`, or every open set containing `y` also contains `x`. This relation is a preorder on any topological space, a partial order when the space is T₀, and degenerates to equality when the space is T₁.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Specializes : {X : Type u_1} -> [TopologicalSpace X] -> (x y : X) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Specializes : {X : Type u_1} -> [TopologicalSpace X] -> (x y : X) -> Prop`

The implicit type argument `X` is the carrier type of the topological space. The instance argument `[TopologicalSpace X]` supplies the topology on `X`. The first explicit argument `x` is the *specializing* point — the "more special," more concrete point. The second explicit argument `y` is the *specialized-to* point — the "more general" point whose neighbourhood filter is coarser.

### Conventions

No junk-value or boundary conventions are declared for this definition: it is a total Prop-valued relation defined for all pairs of points in any topological space, with no inputs treated as degenerate or out-of-domain.

### Worked examples

- Claim: In any topological space, every point specializes to itself, i.e., `VTask.Specializes x x` holds for all `x` (reflexivity of the specialization preorder).

- Claim: In a T₁ topological space (e.g., a metric space or any Hausdorff space), `VTask.Specializes x y` holds if and only if `x = y`; in particular, two distinct points never stand in the specialization relation.

- Claim: In the Sierpiński space on `{0, 1}` where `{1}` is open and `{0}` is not, the generic point `0` specializes to `1`, i.e., `VTask.Specializes 0 1` holds, because every open neighbourhood of `1` (namely `{1}` and the whole space) contains… actually `0` does not belong to `{1}`, so instead: `1` is in the closure of `{0}` (since every open set containing `1` that is `{0, 1}` meets `{0}`), hence `VTask.Specializes 0 1`.

- Claim: Specialization is transitive: if `VTask.Specializes x y` and `VTask.Specializes y z` then `VTask.Specializes x z`.

### Boundaries

- **Reflexivity**: `VTask.Specializes x x` always holds, since the neighbourhood filter is always less than or equal to itself.
- **Antisymmetry vs. T₀**: Without the T₀ axiom, two distinct points can satisfy both `x ⤳ y` and `y ⤳ x` (they are topologically indistinguishable). The relation is only a partial order in T₀ spaces.
- **Trivial in T₁**: In any T₁ space every singleton is closed, so `y ∈ closure {x}` forces `y = x`. Thus specialization collapses to equality.
- **Indiscrete topology**: In the indiscrete topology every pair satisfies `x ⤳ y` (and `y ⤳ x`), giving the most degenerate preorder.
- **Discrete topology**: In the discrete topology every singleton is both open and closed, so `x ⤳ y` forces `x = y`, recovering the diagonal relation.

### Not to be confused with

- **`Inseparable`**: the symmetric version, asserting `𝓝 x = 𝓝 y`; it is the kernel equivalence of the specialization preorder, not the preorder itself.
- **`nhds` / neighbourhood filter ordering**: `𝓝 x ≤ 𝓝 y` is precisely the definition, but the *filter* ordering goes the opposite intuitive direction — a *smaller* filter means *fewer* open sets, not more; keep track that `x ⤳ y` means `x` has the finer neighbourhood filter.
- **`closure` membership**: `y ∈ closure {x}` is equivalent to `x ⤳ y`, but it is easy to accidentally swap the roles of `x` and `y` when translating between the two characterizations.