## VTask.SameCycle

### Object

`VTask.SameCycle f x y` is the proposition asserting that the two points `x` and `y` lie in the same cycle of the permutation `f`. Concretely, this means there exists an integer `i` such that applying `f` exactly `i` times (with negative integers corresponding to iterates of the inverse) to `x` yields `y`. It defines an equivalence relation on the underlying type whose equivalence classes are precisely the orbits (cycles) of `f`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.SameCycle : {α : Type u_2} -> (f : Equiv.Perm α) -> (x y : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_2} -> (f : Equiv.Perm α) -> (x y : α) -> Prop`

The implicit argument `α` is the type on which the permutation acts. The explicit argument `f` is the permutation whose cycle structure is under consideration. The arguments `x` and `y` are the two points of `α` whose membership in a common cycle is being asserted.

### Conventions

There are no junk-value or boundary conventions for this definition: it is a universally-quantified proposition over all permutations and all pairs of points, with no degenerate or out-of-domain inputs to handle.

### Worked Examples

- Claim: For any permutation `f` and any point `x`, `VTask.SameCycle f x x` holds (reflexivity), witnessed by `i = 0`.

- Claim: For the transposition swapping `0` and `1` in `Fin 3`, `VTask.SameCycle f 0 1` holds, witnessed by `i = 1` (one application of the transposition sends `0` to `1`).

- Claim: If `f` is the identity permutation on any type `α`, then `VTask.SameCycle f x y` holds if and only if `x = y`, since all cycles of the identity are fixed points and the only integer power sending `x` to `y` is `i = 0` when `x = y`.

- Claim: For a 3-cycle `f` permuting `{0, 1, 2}` in `Fin 3` via `0 ↦ 1 ↦ 2 ↦ 0`, all three pairs `(0,1)`, `(1,2)`, `(0,2)` satisfy `VTask.SameCycle f`, since appropriate integer powers of `f` connect each pair.

### Boundaries

- When `f` is the identity permutation, every point is its own cycle. Thus `VTask.SameCycle f x y` holds precisely when `x = y`.
- The relation is defined for all integers `i`, not merely non-negative ones, so iterates of the inverse permutation are included. This ensures symmetry: if `VTask.SameCycle f x y` then `VTask.SameCycle f y x`.
- On a finite type, every orbit is finite and every integer power eventually repeats, so the existential is witnessed within a bounded range; on an infinite type with an infinite-order permutation the same formulation is still valid but the orbit may be infinite.
- The relation `VTask.SameCycle f` is an equivalence relation (reflexive, symmetric, transitive) for every permutation `f` on any type.

### Not to be confused with

- `Equiv.Perm.IsCycle`: a predicate on a permutation itself, asserting it acts as a single cycle, rather than a relation between two points.
- `Equiv.Perm.cycleOf`: a function that extracts the cycle of `f` containing a given point as a permutation, rather than a proposition about two points sharing a cycle.
- `Equiv.Perm.orbit`: the set of all points reachable from a given point under a group action, which is the underlying set-theoretic object whose membership is captured by `VTask.SameCycle` but expressed as a `Set` rather than a `Prop`.
