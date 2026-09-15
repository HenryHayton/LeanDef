## VTask.IsSolid

### Object

A set `s` in a lattice-ordered additive commutative group is called **solid** if it is closed under domination in absolute value: whenever an element `x` belongs to `s` and another element `y` satisfies `|y| ≤ |x|`, then `y` must also belong to `s`. Intuitively, solid sets are "symmetric balls" in the order-theoretic sense — if a set contains an element of a certain absolute size, it contains everything of smaller or equal absolute size.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsSolid : {α : Type u_1} -> [Lattice α] -> [AddCommGroup α] -> (s : Set α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsSolid : {α : Type u_1} -> [Lattice α] -> [AddCommGroup α] -> (s : Set α) -> Prop`

The implicit type argument `α` is the carrier type of the lattice-ordered group. The `Lattice` instance supplies the lattice structure (in particular, the meet and join, from which the absolute value `|·|` is derived as `x ⊔ (-x)`). The `AddCommGroup` instance supplies the additive group structure. The explicit argument `s` is the set whose solidity is being asserted.

### Conventions

There are no declared junk-value or edge-case conventions for this definition: `IsSolid` is a universally quantified `Prop` that is well-formed for every set `s` in any lattice-ordered additive commutative group, including the empty set and the whole type.

### Worked examples

- Claim: The whole set `Set.univ` is solid in any lattice-ordered additive commutative group, because every element trivially belongs to it.

- Claim: The singleton `{0}` is solid in any lattice-ordered additive commutative group, because `|y| ≤ |0| = 0` forces `|y| = 0`, which in a lattice-ordered group means `y = 0`.

- Claim: In `ℝ`, the open ball `Metric.ball (0 : ℝ) r` is solid for any radius `r`, since `|y| ≤ |x|` and `|x| < r` together imply `|y| < r`.

- Claim: The solid closure of any set `s` is itself solid, i.e., `VTask.IsSolid (solidClosure s)` holds.

- Claim: The empty set `∅` is solid vacuously, because there are no elements `x ∈ ∅` to begin with.

### Boundaries

- **Empty set**: `IsSolid ∅` holds vacuously — the universal quantifier ranges over members of `∅`, so there are no obligations to discharge.
- **Whole type**: `IsSolid Set.univ` holds trivially — the conclusion `y ∈ Set.univ` is always true.
- **Singletons**: `{0}` is solid (since `|y| ≤ 0` implies `y = 0` in a lattice-ordered group), but `{x}` for `x ≠ 0` is not solid in general, because `-x` satisfies `|-x| = |x|` yet `-x` may differ from `x`.
- **Absolute-value symmetry**: Solidity forces sets to be symmetric with respect to the absolute value: if `x ∈ s` then `-x ∈ s`, since `|-x| = |x|`.
- **Intersection**: The intersection of two solid sets is again solid.

### Not to be confused with

- **`solidClosure`**: The smallest solid set containing a given set `s`; it is the constructor dual to `IsSolid`, which is the predicate testing whether a set already is solid.
- **Convexity**: A convex set in an ordered group need not be solid, and a solid set need not be convex in the topological sense; solidity is an order-theoretic, not a metric/linear, notion.
- **Ideal (order theory)**: A downward-closed set (order ideal) is closed under `y ≤ x`, not under `|y| ≤ |x|`; solidity is a two-sided, absolute-value–based condition rather than a one-sided order condition.