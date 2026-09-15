## Object

`VTask.splitAtPred p L` partitions a list `L` around the first element satisfying the Boolean predicate `p`. If such an element exists — say `L = l₁ ++ [a] ++ l₂` where `p a = true` and no element of `l₁` satisfies `p` — the function returns the triple `(l₁, some a, l₂)`. If no element of `L` satisfies `p`, the function returns `(L, none, [])`, i.e. the whole list as the prefix, no pivot, and an empty suffix.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.splitAtPred : {α : Type u_1} -> (p : α → Bool) -> List α → List α × Option α × List α
<!-- PINNED-SIGNATURE:END -->


`VTask.splitAtPred : {α : Type u_1} -> (p : α → Bool) -> List α → List α × Option α × List α`

The implicit type argument `α` is the element type of the list being searched. The argument `p` is the Boolean predicate used to identify the pivot element: the search stops at the first element for which `p` returns `true`. The final argument is the list to be split.

## Conventions

When the list contains no element satisfying `p`, the function returns the whole input list as the first component, `none` as the middle component, and the empty list as the third component. In particular the third component is always `[]` in the "not found" case — there is no symmetric or arbitrary convention; the empty suffix is canonical.

## Worked examples

- Claim: `VTask.splitAtPred (· == 3) [1, 2, 3, 4, 5] = ([1, 2], some 3, [4, 5])`
  ```lean
  example : VTask.splitAtPred (· == 3) [1, 2, 3, 4, 5] = ([1, 2], some 3, [4, 5]) := by decide
  ```

- Claim: `VTask.splitAtPred (· == 3) [1, 2, 4, 5] = ([1, 2, 4, 5], none, [])`
  ```lean
  example : VTask.splitAtPred (· == 3) [1, 2, 4, 5] = ([1, 2, 4, 5], none, []) := by decide
  ```

- Claim: `VTask.splitAtPred (fun _ => true) [1, 2, 3] = ([], some 1, [2, 3])` — when `p` holds immediately, the prefix is empty and the very first element becomes the pivot.
  ```lean
  example : VTask.splitAtPred (fun _ => true) [1, 2, 3] = ([], some 1, [2, 3]) := by decide
  ```

- Claim: `VTask.splitAtPred (fun _ => false) [1, 2, 3] = ([1, 2, 3], none, [])` — when `p` never holds, the result is the whole list, `none`, and `[]`.
  ```lean
  example : VTask.splitAtPred (fun _ => false) [1, 2, 3] = ([1, 2, 3], none, []) := by decide
  ```

## Boundaries

- **Empty list**: `VTask.splitAtPred p [] = ([], none, [])`. Both the prefix and suffix are empty and no pivot is found.
- **Pivot at the very beginning** (first element satisfies `p`): the prefix `l₁` is `[]`, the pivot is `some` of that first element, and the suffix is the rest of the list.
- **Pivot at the very end** (only the last element satisfies `p`): the prefix `l₁` contains all elements but the last, the pivot is `some` of that last element, and the suffix `l₂` is `[]`.
- **No element satisfies `p`**: returns `(L, none, [])` — the third component is always `[]` in this case (not some arbitrary list).
- **Multiple elements satisfy `p`**: only the *first* such element becomes the pivot; all subsequent satisfying elements end up in the suffix `l₂` unchanged.

## Not to be confused with

- `List.span` / `List.splitAt`: these split a list at a position or by a prefix predicate, but do not isolate a pivot element as the middle component of a triple.
- `List.partition`: separates *all* elements satisfying `p` from those that do not, rather than locating the first satisfying element as a pivot.
- `List.find?`: returns only the first element satisfying a predicate (as an `Option`), without also returning the surrounding prefix and suffix.
