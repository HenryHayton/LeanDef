## Object

`VTask.IsMinBadSeq r rk s n f` is a predicate asserting that the sequence `f` is *rank-minimal at position `n`* among bad sequences agreeing with `f` on its first `n` terms. Concretely, it says: no bad sequence for the relation `r` on the set `s` can agree with `f` on all indices strictly less than `n` while having strictly smaller rank (as measured by `rk`) at index `n`. In other words, `f` cannot be improved at position `n`—keeping the earlier terms fixed—by substituting a term of lower rank.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsMinBadSeq : {α : Type u_2} -> (r : α → α → Prop) -> (rk : α → ℕ) -> (s : Set α) -> (n : ℕ) -> (f : ℕ → α) -> Prop
<!-- PINNED-SIGNATURE:END -->


VTask.IsMinBadSeq : {α : Type u_2} -> (r : α → α → Prop) -> (rk : α → ℕ) -> (s : Set α) -> (n : ℕ) -> (f : ℕ → α) -> Prop

`r` is the binary relation on the type `α` with respect to which "bad sequence" is defined. `rk` is a rank function assigning a natural-number rank to each element of `α`; it is used to measure minimality. `s` is the set from which the sequences draw their values. `n` is the position at which minimality is being asserted: the first `n` terms are treated as fixed, and rank-minimality is checked at index `n`. `f` is the sequence being tested for this minimality property.

## Conventions

The predicate is vacuously true if no bad sequence agrees with `f` on the first `n` terms and has smaller rank at position `n`—in particular, any non-bad sequence satisfies `VTask.IsMinBadSeq` trivially for any `n`. The rank function `rk` is required to map into `ℕ` but is otherwise unrestricted; no assumption is made that it is injective, surjective, or monotone.

## Worked examples

- Claim: If `f` is a bad sequence for `r` on `s` and `∀ n, VTask.IsMinBadSeq r rk s n f` holds, then there is no bad sequence `g` that agrees with `f` on all initial segments and strictly improves the rank at any position.

- Claim: For any relation `r`, rank function `rk`, set `s`, natural number `n`, and sequence `f`, if there exists no bad sequence for `r` on `s` that agrees with `f` on the first `n` terms with strictly smaller rank at `n`, then `VTask.IsMinBadSeq r rk s n f` holds.

- Claim: A set `s` is partially well-ordered with respect to `r` if and only if there is no sequence that is simultaneously a bad sequence for `r` on `s` and satisfies `VTask.IsMinBadSeq r rk s n f` for all `n`.

## Boundaries

- When `n = 0`, the condition on the first `n` terms is vacuous (no terms need to match), so `VTask.IsMinBadSeq r rk s 0 f` says that no bad sequence for `r` on `s` has strictly smaller rank than `f` at index `0`. This is the strongest form of the condition at the "start" of the sequence.
- The predicate does not require `f` itself to be a bad sequence; it is a purely comparative statement about what bad sequences can do at position `n`.
- If `rk` is the constant function `fun _ => 0`, then `rk (g n) < rk (f n)` is always false, making `VTask.IsMinBadSeq r rk s n f` hold trivially for every `f`, `n`, `s`, and `r`.

## Not to be confused with

- `IsBadSeq r s f`: asserts that `f` is itself a bad sequence (all values in `s`, and no pair of indices is related by `r`); `VTask.IsMinBadSeq` is a *minimality* condition on a sequence, not a membership condition.
- `Set.PartiallyWellOrderedOn`: a global property of a set stating it has no bad sequences at all; `VTask.IsMinBadSeq` is an index-by-index minimality condition used to build the proof of that property.
- A globally minimal bad sequence (one satisfying `∀ n, VTask.IsMinBadSeq r rk s n f`): `VTask.IsMinBadSeq r rk s n f` for a single fixed `n` is only a local/positional minimality condition, not global minimality across all positions.
