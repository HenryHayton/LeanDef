## VTask.IsBadSeq

### Object

A sequence `f : ℕ → α` is called a **bad sequence** for a binary relation `r` on a set `s ⊆ α` if two conditions both hold: every term of the sequence lies in `s`, and no term is related (by `r`) to any strictly later term. In the context of partial well-orderings, where `r` plays the role of "is dominated by" or "is less than", this means the sequence never goes up — it is perpetually non-increasing with respect to `r`. A bad sequence witnesses the failure of `s` to be partially well-ordered: `s` is partially well-ordered by `r` if and only if no bad sequence for `(r, s)` exists.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsBadSeq : {α : Type u_2} -> (r : α → α → Prop) -> (s : Set α) -> (f : ℕ → α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsBadSeq : {α : Type u_2} -> (r : α → α → Prop) -> (s : Set α) -> (f : ℕ → α) -> Prop`

The implicit argument `α` is the ambient type. The first explicit argument `r` is the binary relation on `α` that plays the role of the ordering (e.g., "is less than" or "is dominated by"). The second explicit argument `s` is the set whose partial well-orderedness is under examination; the sequence must be entirely contained in `s`. The third explicit argument `f` is the sequence in question — a function from the natural numbers into `α` — whose membership in `s` and non-increase with respect to `r` together constitute being a bad sequence.

### Conventions

There are no special junk-value or boundary conventions for this definition: it is a universally quantified conjunction that is straightforwardly false when its hypotheses fail, and no inputs are outside the definition's natural scope.

### Worked examples

- Claim: The constant sequence `f n = 0` on `ℕ` with `r = (<)` and `s = Set.univ` is a bad sequence, because no natural number is strictly less than itself (so `f m < f n` fails for all `m < n` since `f m = f n = 0`).

- Claim: If `r` is the usual strict order `(<)` on `ℕ` and `f n = n` (the identity sequence), then `f` is NOT a bad sequence for `s = Set.univ`, because `m < n` implies `f m = m < n = f n`, so `r (f m) (f n)` holds.

- Claim: The sequence `f n = 0` on any type with `r = (fun _ _ => False)` (the empty relation) is a bad sequence for any set `s` containing `0`, because `r (f m) (f n)` is always false.

- Claim: For `s.PartiallyWellOrderedOn r` to hold, it is necessary and sufficient that no `f` satisfies `VTask.IsBadSeq r s f`.

### Boundaries

- If `s` is the empty set, no sequence can have all its values in `s` (since `f 0` would need to be in `s`), so there is no bad sequence for `(r, ∅)` — consistently with the fact that the empty set is trivially partially well-ordered.
- If `r` is the everywhere-false relation, then the non-increase condition `¬ r (f m) (f n)` is satisfied by every sequence, so any sequence with range in `s` is a bad sequence; this reflects that no nonempty set is partially well-ordered by the empty relation.
- If `r` is the everywhere-true relation, the non-increase condition fails for every pair `m < n`, so no bad sequence exists; this reflects that every set is trivially partially well-ordered by the everywhere-true relation.
- The strict inequality `m < n` in the non-increase condition means only strictly later indices matter; reflexive behavior (m = n) is not considered.

### Not to be confused with

- `Set.IsMinBadSeq`: a refinement of `VTask.IsBadSeq` that additionally requires the sequence to be *minimal* bad in a rank-based sense — every bad sequence is a bad sequence, but not every bad sequence is a minimal bad sequence.
- `Set.PartiallyWellOrderedOn`: the property of a set that is *equivalent* to the non-existence of a bad sequence, rather than a witness to the failure of that property.
- A *decreasing* sequence in the usual sense: a bad sequence need not have `r (f n) (f m)` for `m < n`; it only needs to fail `r (f m) (f n)` for `m < n`, which is a weaker (one-directional) non-increase condition.