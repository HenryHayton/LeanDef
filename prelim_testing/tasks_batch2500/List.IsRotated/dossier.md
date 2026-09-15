## 1. Object

`VTask.IsRotated l l'` is the proposition that two lists `l` and `l'` are **cyclic rotations** of one another: one can be obtained from the other by detaching some prefix and reattaching it at the end. Concretely, this means there exists a natural number `n` such that rotating `l` by `n` positions (moving the first `n` elements to the back) yields `l'`. This captures exactly the notion of "same circular sequence" familiar from cyclic arrangements, necklaces, or round-robin schedules.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsRotated : {α : Type u} -> (l l' : List α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsRotated : {α : Type u} -> (l l' : List α) -> Prop`

The implicit argument `α` is the type of elements stored in both lists. The first explicit argument `l` is the reference list; the second explicit argument `l'` is the candidate list being compared. The proposition asserts that `l'` is reachable from `l` by some cyclic rotation.

## 3. Conventions

Rotating a list by `0` returns it unchanged, so every list is a rotation of itself (`VTask.IsRotated` is reflexive). Rotating by any `n ≥ length l` wraps around modulo the length, so the quantification over all natural numbers `n` introduces no junk: values of `n` beyond the length simply revisit earlier rotations. In particular, rotating the empty list by any amount yields the empty list, making `VTask.IsRotated [] []` true (trivially witnessed by `n = 0`).

## 4. Worked Examples

- Claim: `VTask.IsRotated [1, 2, 3] [2, 3, 1]` holds, witnessed by rotating by 1.

- Claim: `VTask.IsRotated [1, 2, 3] [3, 1, 2]` holds, witnessed by rotating by 2.

- Claim: `VTask.IsRotated ([] : List ℕ) []` holds, since the empty list rotated by 0 is itself.

- Claim: `VTask.IsRotated [1, 2, 3] [1, 3, 2]` does **not** hold; a mere swap of adjacent elements is not a cyclic rotation of a 3-element list.

- Claim: `VTask.IsRotated [a] [a]` holds for any element `a`, since a single-element list has only one rotation.

## 5. Boundaries

- **Empty lists**: `VTask.IsRotated [] []` is true. `VTask.IsRotated [] (a :: t)` is false for any non-empty list, and vice versa, since rotating an empty list always yields the empty list and rotating a non-empty list always yields a non-empty list.
- **Length mismatch**: If `l` and `l'` have different lengths, `VTask.IsRotated l l'` is false, because rotation preserves the length of a list.
- **Single-element lists**: `VTask.IsRotated [a] [a]` is always true; `VTask.IsRotated [a] [b]` is true if and only if `a = b`.
- **Large `n`**: Rotating by `n ≥ length l` (for a non-empty list) wraps around; the witness `n` is not required to be reduced modulo the length.
- **Symmetry**: `VTask.IsRotated` is symmetric — if `l ~r l'` then `l' ~r l` — so the roles of the two arguments are interchangeable for the purpose of deciding the proposition.

## 6. Not to be confused with

- **`List.Perm`** (`l ~ l'`): asserts that `l'` is any permutation of `l`, not necessarily a cyclic one; every rotation is a permutation but most permutations are not rotations.
- **`List.rotate`**: this is a *function* producing a specific rotation of a list by a given count, whereas `VTask.IsRotated` is the *relation* asserting the existence of some such rotation.
- **`List.cyclicPermutations`**: returns the *list of all* rotations of a given list as a list-of-lists; it is a function on lists, not a binary relation between two lists.