## VTask.orderedInsert

### Object

`VTask.orderedInsert r a l` inserts an element `a` into a list `l` at the unique position that preserves sorted order with respect to the binary relation `r`. Concretely, `a` is placed immediately before the first element `b` of `l` for which `r a b` holds; if no such element exists, `a` is appended at the end. The result is a permutation of `a :: l` and, provided `l` is sorted by `r`, the result is also sorted by `r`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.orderedInsert : {α : Type u_1} -> (r : α → α → Prop) -> [DecidableRel r] -> (a : α) -> List α → List α
<!-- PINNED-SIGNATURE:END -->


The implicit type argument `α` is the element type of the list. The explicit argument `r` is the ordering relation used to determine where to insert; it must be decidable (the `DecidableRel r` instance supplies the decision procedure). The argument `a` is the element to be inserted. The final argument is the target list into which `a` is inserted.

### Conventions

No junk-value or edge conventions beyond standard totality are declared: the function is total, with the empty-list case explicitly handled by returning the singleton `[a]`.

### Worked examples

- Claim: `VTask.orderedInsert (· ≤ ·) 3 [1, 2, 4, 5] = [1, 2, 3, 4, 5]`
  ```lean
  example : VTask.orderedInsert (· ≤ ·) 3 [1, 2, 4, 5] = [1, 2, 3, 4, 5] := by decide
  ```

- Claim: `VTask.orderedInsert (· ≤ ·) 0 [1, 2, 3] = [0, 1, 2, 3]` (element smaller than all: prepended)
  ```lean
  example : VTask.orderedInsert (· ≤ ·) 0 [1, 2, 3] = [0, 1, 2, 3] := by decide
  ```

- Claim: `VTask.orderedInsert (· ≤ ·) 7 [1, 4, 5] = [1, 4, 5, 7]` (element larger than all: appended)
  ```lean
  example : VTask.orderedInsert (· ≤ ·) 7 [1, 4, 5] = [1, 4, 5, 7] := by decide
  ```

- Claim: `VTask.orderedInsert (· ≤ ·) 42 [] = [42]` (inserting into the empty list yields the singleton)
  ```lean
  example : VTask.orderedInsert (· ≤ ·) 42 ([] : List Nat) = [42] := by decide
  ```

- Claim: The result always has length one greater than the original list.

- Claim: The result is always a permutation of `a` prepended to the original list, i.e., membership in the result is exactly membership in `a :: l`.

### Boundaries

- **Empty list**: inserting any element into `[]` returns the singleton list `[a]`.
- **Element smaller than all present**: if `r a b` holds for the very first element `b`, then `a` is placed at the head and the rest of the list is unchanged.
- **Element larger than all present** (under a total order): `a` is appended at the end, traversing the entire list.
- **Duplicate elements**: the function inserts `a` at the first valid position regardless of whether `a` already appears in the list; duplicates are allowed and `a` will appear at least twice in the result.
- **Input list not sorted**: the function still executes and terminates, but the result need not be sorted; the sortedness-preservation guarantee requires the input to be sorted.

### Not to be confused with

- `List.insertionSort r l` — uses `VTask.orderedInsert` repeatedly to sort an entire list; `VTask.orderedInsert` handles only a single insertion step.
- `List.insert a l` — inserts `a` only if it is not already a member of `l` (deduplicating), using decidable equality; `VTask.orderedInsert` always inserts and uses an ordering relation, not equality.
- `List.mergeSort` — a different sorting algorithm that does not expose a single-element insertion primitive.