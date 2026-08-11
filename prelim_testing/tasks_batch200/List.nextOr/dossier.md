## VTask.nextOr

### Object

`VTask.nextOr xs x default` searches the list `xs` for an occurrence of the element `x` that is immediately followed by another element, and returns that successor element. If `x` does not appear in `xs` at a position that has a successor (i.e., `x` is absent, or it only appears as the last element), the function returns `default`. In other words, it finds the unique `z` such that the consecutive pair `x, z` appears somewhere in `xs`, and returns `z`; if no such `z` exists, it returns `default`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.nextOr : {α : Type u_1} -> [DecidableEq α] -> List α → α → α → α
<!-- PINNED-SIGNATURE:END -->


`VTask.nextOr : {α : Type u_1} -> [DecidableEq α] -> List α → α → α → α`

The implicit type parameter `α` is the element type of the list. The `DecidableEq α` instance is required to compare elements for equality. The first explicit argument is the list `xs` being searched. The second explicit argument `x` is the element whose immediate successor in the list is sought. The third explicit argument is the default value returned when no successor of `x` is found.

### Conventions

When the list is empty, the function returns `default` regardless of the query element. When `x` appears only as the last element of `xs` (including the case of a singleton list whose sole element is `x`), `default` is returned, since there is no successor. When `x` does not appear in `xs` at all, `default` is likewise returned. The function finds only the *first* occurrence of `x` in `xs` that has a successor; if `x` appears multiple times, the result is determined by the earliest such occurrence.

### Worked examples

- Claim: `VTask.nextOr [] 1 0 = 0` — searching an empty list returns the default.

- Claim: `VTask.nextOr [3] 3 0 = 0` — `3` is the sole (last) element, so no successor exists and the default is returned.

- Claim: `VTask.nextOr [1, 2, 3] 1 0 = 2` — `1` is immediately followed by `2` in the list.

- Claim: `VTask.nextOr [1, 2, 3] 2 0 = 3` — `2` is immediately followed by `3`.

- Claim: `VTask.nextOr [1, 2, 3] 3 0 = 0` — `3` is the last element, no successor, returns default `0`.

- Claim: `VTask.nextOr [1, 2, 3] 5 0 = 0` — `5` is not in the list at all, returns default `0`.

- Claim: `VTask.nextOr [1, 2, 1, 3] 1 0 = 2` — the first occurrence of `1` has successor `2`; later occurrence is not reached first.

- Claim: If `x` appears in `dropLast xs` and `d ∈ xs`, then `VTask.nextOr xs x d ∈ xs` — the result is always a member of the list when the default is also a member.

### Boundaries

- **Empty list**: Always returns `default`.
- **Singleton list**: Always returns `default` (there can be no successor to any element).
- **`x` is the last element**: Returns `default` even if `x` appears elsewhere earlier; if the earlier occurrence has a successor, that successor is returned instead. Only the *last* element without a successor (when it is the first match found) yields `default`.
- **`x` not in list**: Returns `default`.
- **Duplicate elements**: Only the first occurrence of `x` that has an immediate successor in the list influences the result.
- **`default` value is arbitrary**: Its type must match `α`, but no constraint is placed on it; the caller chooses it freely.
- **`x = z` (self-loop)**: If `x` is immediately followed by `x` itself, the result is `x`, which may equal the default; the two coinciding does not indicate "not found".

### Not to be confused with

- **`List.getLast`**: Returns the final element of a list, not the successor of a specified element.
- **`List.get?` / `List.getElem?`**: Index-based element access; retrieves an element by numeric position rather than by finding a predecessor element.
- **`List.Cycle.next`**: A related concept for cyclic lists where the successor of the last element wraps around to the first; `VTask.nextOr` does *not* wrap around and returns `default` for the last element.
