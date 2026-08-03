## Object

`VTask.prev l x h` returns the *cyclic predecessor* of an element `x` in a list `l`, treating the list as a cycle where the element before the head is the last element. The search proceeds from left to right and stops at the first occurrence of `x`, so duplicate entries later in the list are ignored.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prev : {α : Type u_1} -> [DecidableEq α] -> (l : List α) -> (x : α) -> x ∈ l → α
<!-- PINNED-SIGNATURE:END -->


`VTask.prev : {α : Type u_1} -> [DecidableEq α] -> (l : List α) -> (x : α) -> x ∈ l → α`

The implicit type parameter `α` is the element type. The `DecidableEq α` instance is needed to compare list elements for equality during the search. `l` is the list viewed as a cycle. `x` is the element whose predecessor is sought. The final argument is a proof that `x` actually belongs to `l`, which guarantees the function always returns a value.

## Conventions

When the list has exactly one element `[y]`, the predecessor of any member is `y` itself (the sole element is its own predecessor in a length-1 cycle). When `x` is the first (head) element of the list, its predecessor is the last element of the list (`getLast`). The function matches the *first* occurrence of `x` when the list contains duplicates, so later occurrences do not affect the result.

## Worked examples

- Claim: `VTask.prev [1, 2, 3] 2 (by simp) = 1` — the element before 2 in the cycle 1→2→3→(back to 1) is 1.
- Claim: `VTask.prev [1, 2, 3] 1 (by simp) = 3` — 1 is the head, so its predecessor wraps around to the last element 3.
- Claim: `VTask.prev [1, 1, 2] 1 (by simp) = 2` — the first occurrence of 1 is the head; its predecessor is the last element, which is 2.
- Claim: `VTask.prev [1, 2, 3, 2, 4] 2 (by simp) = 1` — only the first occurrence of 2 (at index 1) is considered; its predecessor is 1.
- Claim: `VTask.prev [5] 5 (by simp) = 5` — a singleton list: every element is its own predecessor.

## Boundaries

- **Empty list**: impossible by construction — the membership proof `x ∈ []` is `False`, so the empty-list case is vacuously handled and never actually produces a value.
- **Singleton list `[y]`**: returns `y` regardless of what element (necessarily `y`) is queried.
- **Head element**: when `x` equals the head of a list of length ≥ 2, the predecessor is `getLast` of the tail (equivalently, the last element of the whole list).
- **Duplicates**: only the first occurrence of `x` is considered; any later copies of `x` are ignored entirely.
- **Result is always a member**: `VTask.prev l x h ∈ l` holds for all valid inputs.

## Not to be confused with

- `List.next`: the cyclic *successor* of an element; `prev` and `next` are mutual inverses on duplicate-free lists.
- `List.getLast`: returns the physically last element of a list, not a cyclic predecessor relative to a given element.
- `List.get` / `List.getElem`: accesses a list element by numeric index rather than by value with a membership witness.