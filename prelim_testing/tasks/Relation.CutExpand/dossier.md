## 1. Object

`VTask.CutExpand r s' s` is a binary relation on multisets that models one legal move in the Hercules-vs-Hydra game (or, equivalently, one reduction step in a multiset rewriting system). It holds when `s'` can be obtained from `s` by removing exactly one element `a` and replacing it with any finite collection `t` of elements that are each strictly smaller than `a` with respect to the relation `r`. In other words, one "head" of the hydra is cut off, and zero or more smaller heads may grow back in its place.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.CutExpand : {α : Type u_1} -> (r : α → α → Prop) -> (s' s : Multiset α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.CutExpand : {α : Type u_1} -> (r : α → α → Prop) -> (s' s : Multiset α) -> Prop`

The implicit type parameter `α` is the type of individual elements (hydra heads). The argument `r` is the "smaller-than" relation on elements: `r a' a` means `a'` is a valid replacement for `a` (i.e., strictly below it). The argument `s'` is the multiset *after* the move (the proposed successor state). The argument `s` is the multiset *before* the move (the current state). Thus `VTask.CutExpand r s' s` reads: "starting from `s`, one valid move produces `s'`."

## 3. Conventions

The relation is stated using the equivalent identity `s' + {a} = s + t` rather than the more explicit `s' = s.erase a + t`, in order to avoid requiring a `DecidableEq` instance on `α`. The membership condition `a ∈ s` is not stated explicitly, because the multiset-addition identity already forces `a` to appear in `s + t`; when `r` is irreflexive (in particular, when `r` is well-founded), `a` cannot belong to `t`, so `a` must come from `s`.

## 4. Worked examples

- Claim: `VTask.CutExpand (· < ·) {1, 2} {3}` holds, because we remove `3` from `{3}` and add back `{1, 2}` where `1 < 3` and `2 < 3`.

- Claim: `VTask.CutExpand (· < ·) (∅ : Multiset ℕ) {5}` holds, because we remove `5` from `{5}` and add back the empty multiset (no heads regrow).

- Claim: `VTask.CutExpand (· < ·) {4} {4}` does not hold when `<` is irreflexive, because removing `4` and adding back `{4}` would require `4 < 4`.

- Claim: For any `a b : α` and `r : α → α → Prop`, if `r a b` then `VTask.CutExpand r {a} {b}` holds (replacing a single head `b` by a single smaller head `a`).

## 5. Boundaries

- **Empty source multiset `s = ∅`:** No move is possible from the empty multiset when `r` is irreflexive; `VTask.CutExpand r s' ∅` is false for every `s'`. Intuitively, there is no head to cut.
- **Empty replacement `t = ∅`:** This is allowed. Cutting a head without regrowing any new ones is a valid (and terminating) move; `VTask.CutExpand r ∅ {a}` holds via the witness `t = ∅`.
- **Reflexive `r`:** If `r` is reflexive, the irreflexivity-based reasoning breaks down. An element `a` could then appear in `t`, and `a ∈ s` is no longer guaranteed; the correspondence with the direct-erase formulation (`cutExpand_iff`) requires irreflexivity.
- **Non-well-founded `r`:** The relation `VTask.CutExpand r` is well-founded precisely when `r` itself is well-founded; without that hypothesis the hydra game may go on forever.
- **Adding a common summand:** The relation is invariant under adding a common multiset summand to both sides: `VTask.CutExpand r (s + t) (s + u) ↔ VTask.CutExpand r t u`.

## 6. Not to be confused with

- **`Multiset.Rel`**: a pointwise lifting of a relation to multisets (matching elements pairwise), not a rewriting/game-move relation.
- **`Finsupp.Lex`**: the lexicographic order on finitely-supported functions, which is used internally to prove well-foundedness of `VTask.CutExpand` but is a total-order comparison, not a game-move predicate.
- **`Multiset.lt` / `Multiset.subset`**: standard sub-multiset or strict-sub-multiset relations on multisets, which do not involve a base relation `r` on elements and do not model cut-and-expand rewriting.