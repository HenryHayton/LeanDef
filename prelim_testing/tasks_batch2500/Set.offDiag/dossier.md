## VTask.offDiag

### Object

Given a set `s` of elements of some type `α`, the *off-diagonal* of `s` is the set of all ordered pairs `(a, b)` such that both `a` and `b` belong to `s` and `a` is not equal to `b`. Equivalently, it is the Cartesian product `s × s` with the diagonal `{(a, a) | a ∈ s}` removed.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.offDiag : {α : Type u} -> (s : Set α) -> Set (α × α)
<!-- PINNED-SIGNATURE:END -->


The single explicit argument `s` is the ambient set whose off-diagonal is being formed. The universe-polymorphic type `α` is inferred from `s`.

### Conventions

No special junk-value or boundary conventions are declared for this definition: it is a genuinely total operation whose behaviour on every input (including the empty set, singletons, and infinite sets) is determined directly by the membership condition.

### Worked examples

- Claim: The pair `(1, 2)` belongs to `VTask.offDiag {1, 2, 3}` because both `1` and `2` are in `{1, 2, 3}` and `1 ≠ 2`.

- Claim: The pair `(1, 1)` does not belong to `VTask.offDiag {1, 2}` because its two components are equal.

- Claim: `VTask.offDiag (∅ : Set ℕ) = ∅`, since there are no elements at all to form pairs from.

- Claim: `VTask.offDiag {a}` (a singleton set) equals `∅` for any element `a`, because any pair `(x, y)` drawn from a singleton must have `x = y`.

- Claim: `VTask.offDiag s ⊆ s ×ˢ s` for every set `s`, since every pair in the off-diagonal has both components in `s`.

### Boundaries

- **Empty set**: `VTask.offDiag ∅ = ∅`. There are no pairs to form.
- **Singleton**: `VTask.offDiag {a} = ∅`. The only candidate pair `(a, a)` is excluded by the inequality condition.
- **Subsingleton sets**: More generally, `VTask.offDiag s = ∅` if and only if `s` is a subsingleton (has at most one element).
- **Nontrivial sets**: `VTask.offDiag s` is nonempty if and only if `s` is nontrivial (contains at least two distinct elements).
- **Finite sets**: If `s` is finite, then `VTask.offDiag s` is also finite.
- **Relation to product**: `VTask.offDiag s` is always a subset of the Cartesian product `s ×ˢ s`.

### Not to be confused with

- `Set.diagonal s`: the *diagonal* of `s`, i.e., `{(a, a) | a ∈ s}` — the complement within `s ×ˢ s` of the off-diagonal.
- `Finset.offDiag`: the finset analogue of the same construction, defined for `Finset α` rather than `Set α`.
- `s ×ˢ s` (the full Cartesian product of `s` with itself): this includes the diagonal pairs `(a, a)`, which are excluded from the off-diagonal.