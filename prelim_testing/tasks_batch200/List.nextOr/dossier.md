## Object

`VTask.nextOr xs x default` scans the list `xs` from left to right looking for the first occurrence of the element `x` such that `x` is immediately followed by some element `z` in `xs` (i.e., the pair `x, z` appears as consecutive elements). When such a `z` exists, it returns `z`; otherwise it returns `default`. Informally: "find the element immediately after the first occurrence of `x` in the list, or fall back to `default` if no such successor exists."

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.nextOr : {α : Type u_1} -> [DecidableEq α] -> List α → α → α → α
<!-- PINNED-SIGNATURE:END -->


VTask.nextOr : {α : Type u_1} -> [DecidableEq α] -> List α → α → α → α

The implicit type parameter `α` is the element type of the list. The `DecidableEq` instance is required to test elements for equality. The first explicit argument is the list `xs` being searched. The second explicit argument `x` is the element whose immediate successor in `xs` is sought. The third explicit argument is the `default` value returned when no immediate successor of `x` is found.

## Conventions

When `xs` is empty, the function returns `default` regardless of `x`. When `xs` has exactly one element, the function returns `default` regardless of `x`, because a single-element list has no room for a successor. When `x` does not appear in `xs` at a position that has a following element (i.e., `x` either does not appear at all, or appears only as the last element), the function returns `default`.

## Worked examples

- Claim: `VTask.nextOr [] 5 0 = 0` — searching the empty list always returns the default.

- Claim: `VTask.nextOr [3] 3 0 = 0` — a singleton list has no successor for any element, so the default is returned.

- Claim: `VTask.nextOr [1, 2, 3] 1 0 = 2` — the element immediately after the first occurrence of `1` in the list `[1, 2, 3]` is `2`.

- Claim: `VTask.nextOr [1, 2, 3] 2 0 = 3` — the element immediately after `2` in `[1, 2, 3]` is `3`.

- Claim: `VTask.nextOr [1, 2, 3] 3 0 = 0` — `3` is the last element of `[1, 2, 3]`, so it has no successor and `default` is returned.

- Claim: `VTask.nextOr [1, 2, 1, 4] 1 0 = 2` — only the *first* occurrence of `1` is used; its successor is `2`.

- Claim: If `d ∈ xs` then `VTask.nextOr xs x d ∈ xs` — the result always belongs to the list whenever the default value itself belongs to the list.

## Boundaries

- **Empty list**: returns `default` unconditionally.
- **Singleton list**: returns `default` unconditionally; there can be no consecutive pair.
- **`x` not in `xs`**: returns `default`; `x` must equal the head of a sublist that still has a next element.
- **`x` is the last element of `xs`**: returns `default`, since there is no element following it.
- **Duplicate occurrences of `x`**: only the first occurrence is used; the element immediately after that first occurrence is returned.
- **`default` equals an element of `xs`**: the result type `α` is unrestricted, so `default` may coincide with list members; there is no conflict.
- **`x = default`**: the function handles this uniformly; the return value is still the element following the first occurrence of `x`, or `default` if none exists.

## Not to be confused with

- **`List.next?`** (or a hypothetical cycle-aware next): `VTask.nextOr` does **not** wrap around; the last element of the list has no successor, and `default` is returned rather than the first element.
- **`List.indexOf` / `List.idxOf`**: those return the *index* of `x`, not the element following it.
- **`List.get?`**: retrieves an element by numeric index, not by searching for a predecessor element.
