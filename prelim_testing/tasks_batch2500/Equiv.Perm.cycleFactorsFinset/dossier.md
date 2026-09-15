## VTask.cycleFactorsFinset

### Object

Given a permutation `f` of a finite type `α`, `VTask.cycleFactorsFinset f` is the finite set of all disjoint cycles whose product equals `f`. More precisely, it is the unique `Finset` of permutations of `α` satisfying three properties simultaneously: every element of the set is a cycle (a non-trivial permutation that acts on its support as a single orbit), the elements are pairwise disjoint (their supports are disjoint), and their product (in some—hence any—order, since disjoint cycles commute) equals `f`. This set is the canonical cycle decomposition of `f` viewed as a set rather than a list.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.cycleFactorsFinset : {α : Type u_2} -> [DecidableEq α] -> [Fintype α] -> (f : Equiv.Perm α) -> Finset (Equiv.Perm α)
<!-- PINNED-SIGNATURE:END -->


The implicit type argument `α` is the finite type being permuted. The `DecidableEq` and `Fintype` instances make equality testing and enumeration of `α` possible. The explicit argument `f` is the permutation of `α` whose cycle decomposition is to be computed.

### Conventions

The identity permutation has an empty cycle factorization: `VTask.cycleFactorsFinset 1 = ∅`, since no cycle is needed and there are no cycles to include. Every element of the returned `Finset` is a cycle (satisfies `IsCycle`), so fixed points of `f` do not appear as singleton-support "cycles"—they are simply absent from the set.

### Worked examples

- Claim: For a single transposition `f = Equiv.swap a b` with `a ≠ b`, the cycle factorization set is the singleton `{Equiv.swap a b}`, since a transposition is itself a cycle.

- Claim: If `f` is a cycle (satisfies `IsCycle f`), then `VTask.cycleFactorsFinset f = {f}`.

- Claim: If `f` and `g` are disjoint permutations, then `VTask.cycleFactorsFinset (f * g)` equals the disjoint union of `VTask.cycleFactorsFinset f` and `VTask.cycleFactorsFinset g`.

- Claim: The product of all elements of `VTask.cycleFactorsFinset f` (in any order, since they commute) equals `f`.

- Claim: The function `f ↦ VTask.cycleFactorsFinset f` is injective: two permutations with the same cycle factorization set are equal.

### Boundaries

- **Identity permutation**: `VTask.cycleFactorsFinset 1 = ∅`. The identity has no non-trivial cycles, so the factorization set is empty.
- **Single cycle**: If `f` is already a cycle, the factorization set is `{f}` (a singleton).
- **Transpositions**: A transposition is a 2-cycle, so its factorization set is a singleton containing itself.
- **Fixed points**: Elements of `α` that are fixed by `f` do not contribute any cycle to the set; no length-1 "trivial cycles" appear.
- **Product reconstruction**: The product of the elements of the returned set always equals `f`, regardless of the order chosen (disjointness implies commutativity).
- **Uniqueness**: The cycle factorization into disjoint cycles is unique, so `VTask.cycleFactorsFinset` is well-defined and injective as a function of `f`.

### Not to be confused with

- **`Equiv.Perm.cycleOf f x`**: This gives the single cycle of `f` containing the point `x`, not the full set of all cycles; it returns the identity when `x` is a fixed point.
- **`Equiv.Perm.cycleType f`**: This is the multiset of support sizes of the cycles in the factorization, not the cycles themselves; it discards the actual cycle permutations.
- **`Equiv.Perm.support f`**: This is the set of points that `f` moves, not the set of cycle permutations that factor `f`.
