## Object

`VTask.SuccChain r s` is a **successor-chain operator**: given a relation `r` on a type `α` and a set `s ⊆ α`, it returns a chain with respect to `r` that is strictly larger than `s` whenever such a chain exists, and returns `s` itself otherwise. In other words, it is a choice function that, in the "non-maximal" case, picks one concrete witness to the fact that `s` is not a maximal chain; in the "maximal" (fixed-point) case it leaves `s` unchanged. This operator is the key ingredient in the transfinite construction used to prove Zorn's Lemma.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.SuccChain : {α : Type u_1} -> (r : α → α → Prop) -> (s : Set α) -> Set α
<!-- PINNED-SIGNATURE:END -->


`VTask.SuccChain : {α : Type u_1} -> (r : α → α → Prop) -> (s : Set α) -> Set α`

The implicit argument `α` is the ambient type whose subsets are being considered. The explicit argument `r` is the binary relation with respect to which "chain" is defined (e.g., a partial order). The explicit argument `s` is the set — typically already a chain — that is to be extended if possible.

## Conventions

When no strict superchain of `s` exists (i.e., `s` is already a maximal chain with respect to `r`, or is not itself a chain), `VTask.SuccChain r s` is defined to equal `s` exactly, so `s` is always a subset of `VTask.SuccChain r s` regardless of regime.

## Worked examples

- Claim: For any relation `r` and any set `s`, `s ⊆ VTask.SuccChain r s`. (The successor chain always contains the original set.)

- Claim: If `s` is a chain with respect to `r` and is not a maximal chain, then `VTask.SuccChain r s` is a chain that strictly includes `s` (i.e., `SuperChain r s (VTask.SuccChain r s)` holds).

- Claim: If `s` is a maximal chain with respect to `r`, then `VTask.SuccChain r s = s`. (The operator is a fixed point precisely at maximal chains.)

- Claim: If there exists some chain `t` with `SuperChain r s t`, then `VTask.SuccChain r s` is itself a superchain of `s` (not merely equal to `s`).

## Boundaries

- **Non-chain input**: If `s` is not a chain with respect to `r`, the condition for finding a superchain (`IsChain r s ∧ SuperChain r s t`) cannot be satisfied (the `IsChain r s` factor fails), so `VTask.SuccChain r s = s` in this case.
- **Maximal chain**: When `s` is a maximal chain (`IsMaxChain r s`), no strict superchain exists, so again `VTask.SuccChain r s = s`. This is the fixed-point condition: `VTask.SuccChain r s = s ↔ s` is the maximal chain (within the chain-closure framework).
- **Empty set**: The empty set is a chain (vacuously), and unless no larger chain exists, `VTask.SuccChain r ∅` will be a strictly larger set than `∅`.
- **Non-constructive choice**: The returned set is chosen via the axiom of choice when a superchain exists; nothing determines *which* superchain is selected, only that it is one.

## Not to be confused with

- `IsChain r s` — a `Prop` asserting that `s` is a chain; `VTask.SuccChain` is a `Set`-valued function, not a predicate.
- `SuperChain r s t` — a `Prop` asserting that `t` is a chain strictly extending `s`; `VTask.SuccChain r s` is the *chosen witness* `t` when such a `t` exists.
- `maxChain r` — the specific maximal chain selected in the proof of Zorn's Lemma; `VTask.SuccChain` is the one-step successor operator used to build toward it, not the chain itself.