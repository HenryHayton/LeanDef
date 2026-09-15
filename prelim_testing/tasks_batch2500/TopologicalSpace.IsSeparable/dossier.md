## VTask.IsSeparable

### Object

A set `s` in a topological space is *separable* (in the sense of `VTask.IsSeparable`) if there exists a countable set `c` — anywhere in the ambient space — whose closure contains all of `s`. Informally, `s` can be "approximated" by a countable collection of points in the sense that every point of `s` is a limit point (or member) of some countable set. This is the ambient-space version of separability: the witnessing countable set `c` need not itself lie inside `s`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsSeparable : {α : Type u} -> [t : TopologicalSpace α] -> (s : Set α) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.IsSeparable : {α : Type u} -> [t : TopologicalSpace α] -> (s : Set α) -> Prop
```

The implicit type argument `α` is the ambient topological space. The instance `t` is the topology on `α`, supplied automatically by typeclass inference. The explicit argument `s` is the subset of `α` whose separability is being asserted.

### Conventions

The witnessing countable set `c` in the definition is not required to be a subset of `s`. Consequently `VTask.IsSeparable s` does **not** say that `s` itself has a countable dense subset *within* `s`; for the intrinsic notion (dense subset contained in `s`), one should use the `SeparableSpace` instance on the subtype `s` or the statement `VTask.IsSeparable (Set.univ : Set s)`. In pseudo-metrizable spaces the two notions coincide, but in general topology they can differ.

### Worked examples

- Claim: Every finite set satisfies `VTask.IsSeparable`.

- Claim: Every countable set satisfies `VTask.IsSeparable` (take `c := s` itself; then `s ⊆ closure s`).

- Claim: In a `SeparableSpace α`, every subset `s : Set α` satisfies `VTask.IsSeparable s`.

- Claim: If `VTask.IsSeparable s` and `u ⊆ s`, then `VTask.IsSeparable u` (monotonicity: the same witnessing countable set works for `u`).

- Claim: A countable union of separable sets is separable: if `∀ i, VTask.IsSeparable (s i)` for a countably-indexed family, then `VTask.IsSeparable (⋃ i, s i)`.

### Boundaries

- The empty set is separable: take `c = ∅`, which is countable, and `∅ ⊆ closure ∅`.
- The full space `Set.univ` is separable if and only if `α` is a `SeparableSpace` (via the `Dense.isSeparable_iff` equivalence when `s` is dense).
- A set that is totally bounded in a uniform space is separable.
- Separability is preserved under countable unions but not arbitrary ones.
- The closure of a separable set is again separable (take the same witnessing `c`; `closure (closure c) = closure c`).

### Not to be confused with

- `TopologicalSpace.SeparableSpace s` (or `SeparableSpace s`): the intrinsic notion, requiring a countable dense subset *of* `s` viewed as a topological space in its own right; this is stronger than `VTask.IsSeparable s` in general topology.
- `SecondCountableTopology`: a strictly stronger property (countable base for the topology) that implies separability but is not equivalent in non-metrizable spaces.
- `Set.Countable s`: mere countability of `s` as a set, which implies `VTask.IsSeparable s` but is much stronger than it.
