## Object

A pair of sets `(s, t)` satisfies this predicate when `t` is a chain with respect to a given binary relation `r` and `t` strictly contains `s` (i.e., every element of `s` belongs to `t`, but `t` has at least one element not in `s`).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.SuperChain : {α : Type u_1} -> (r : α → α → Prop) -> (s t : Set α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.SuperChain : {α : Type u_1} -> (r : α → α → Prop) -> (s t : Set α) -> Prop`

The implicit type parameter `α` is the carrier type of all sets involved. The argument `r` is the binary relation that determines what it means for a collection of elements to form a chain — two elements are "comparable" when at least one direction of `r` holds between them. The argument `s` is the reference set being strictly extended. The argument `t` is the candidate set that must simultaneously be a chain under `r` and a strict superset of `s`.

## Conventions

No special junk-value or edge-case conventions have been declared for this definition: it is a straightforward conjunction of two well-defined conditions (`IsChain r t` and `s ⊂ t`), both of which behave normally on all inputs including empty sets.

## Worked examples

- Claim: For the usual `≤` relation on `ℕ`, the pair `(s, t)` with `s = {1, 2}` and `t = {1, 2, 3}` satisfies `VTask.SuperChain (· ≤ ·) s t`, because `{1, 2, 3}` is a chain under `≤` and strictly contains `{1, 2}`.

- Claim: For any relation `r` and any set `s`, `VTask.SuperChain r s s` does **not** hold, because `s ⊂ s` is false (a set is never a strict subset of itself).

- Claim: A maximal chain `s` (i.e., `IsMaxChain r s`) satisfies `¬ VTask.SuperChain r s t` for every set `t`, because no chain strictly extends a maximal chain.

- Claim: If `s` is a chain under `r` and `s` is not a maximal chain, then `VTask.SuperChain r s (SuccChain r s)` holds.

## Boundaries

- When `s = ∅`: any non-empty chain `t` qualifies as a strict extension, so the predicate can hold. An empty `t` does not satisfy `∅ ⊂ ∅`.
- When `s` is already a maximal chain: the predicate is false for every `t`, as guaranteed by `IsMaxChain.not_superChain`.
- The predicate requires **both** conditions simultaneously: `t` being a strict superset of `s` is not enough — `t` must also be a chain under `r`.
- The relation `r` need not be a partial order; it can be any binary relation, and `IsChain` still makes sense.

## Not to be confused with

- `IsChain r t` alone — that only checks that `t` is a chain; it says nothing about any relationship to another set `s`.
- `s ⊂ t` (strict subset) alone — that only checks containment; it does not require `t` to be a chain.
- `IsMaxChain r s` — that asserts `s` is a chain with **no** strict chain extension, essentially the negation of the scenario where `VTask.SuperChain r s t` could hold for any `t`.