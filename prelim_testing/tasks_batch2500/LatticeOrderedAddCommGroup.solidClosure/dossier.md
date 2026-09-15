## VTask.solidClosure

### Object

Given a subset `s` of a lattice-ordered additive commutative group, the **solid closure** of `s` is the smallest superset of `s` that is *solid*. A set is solid if whenever an element `x` belongs to it and `|y| ≤ |x|` (in the lattice sense), then `y` belongs to it as well. Equivalently, the solid closure of `s` is the collection of all elements `y` for which there exists some `x ∈ s` with `|y| ≤ |x|`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.solidClosure : {α : Type u_1} -> [Lattice α] -> [AddCommGroup α] -> (s : Set α) -> Set α
<!-- PINNED-SIGNATURE:END -->


The ambient type `α` carries both a lattice structure and the structure of an additive commutative group, so that absolute values (lattice-theoretic, i.e., `|x| = x ⊔ (-x)`) and comparisons are available. The argument `s` is the input subset of `α` whose solid closure is to be formed.

### Conventions

No special junk-value or edge-case conventions have been declared for this definition: it is a total function on all subsets, including the empty set and the full set, with no exceptional inputs requiring separate treatment.

### Worked examples

- Claim: For the set `s = {(3 : ℤ)}`, any integer `y` with `|y| ≤ 3` belongs to `VTask.solidClosure s`.

- Claim: For `s = ∅ ⊆ ℤ`, the solid closure `VTask.solidClosure ∅` is also `∅`, since there is no element `x ∈ ∅` witnessing the existential.

- Claim: `s ⊆ VTask.solidClosure s` for any `s`, because each `x ∈ s` witnesses `|x| ≤ |x|`.

- Claim: For `s = {(0 : ℤ)}`, the solid closure `VTask.solidClosure s = {0}`, since `|y| ≤ |0| = 0` implies `y = 0`.

### Boundaries

- **Empty set**: `VTask.solidClosure ∅ = ∅`. There is no witness `x ∈ ∅`, so no element `y` can satisfy the existential condition.
- **Singleton `{0}`**: The solid closure is `{0}` because `|y| ≤ 0` forces `y = 0` in a lattice-ordered group.
- **Full set**: If `s` is all of `α`, then `VTask.solidClosure s = α` as well, since every element is dominated by itself.
- **Already solid sets**: If `s` is itself solid, then `VTask.solidClosure s = s` — the operation is idempotent on solid sets.
- **Monotonicity**: If `s ⊆ t`, then `VTask.solidClosure s ⊆ VTask.solidClosure t`.

### Not to be confused with

- **Convex cone closure / order-ideal closure**: These are related notions of generating a set closed under certain order conditions, but they do not use the absolute-value condition that defines solidity.
- **`Set.closure` or topological closure**: A topological or algebraic closure operator; solidity is a purely order-theoretic/lattice-group condition, not a topological one.
- **Solid sets (the predicate)**: A set `s` is solid if it equals its own solid closure; `VTask.solidClosure` is the operation producing the smallest solid superset, not the predicate testing solidity.