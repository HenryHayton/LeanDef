## Object

`VTask.getLastI` returns the last element of a list. When the list is non-empty it yields whatever element sits at the end; when the list is empty it yields the `default` value supplied by the `Inhabited` type-class instance for the element type.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.getLastI : {α : Type u_1} -> [Inhabited α] -> List α → α
<!-- PINNED-SIGNATURE:END -->


`VTask.getLastI : {α : Type u_1} -> [Inhabited α] -> List α → α`

The implicit type parameter `α` is the type of the list elements. The instance argument `[Inhabited α]` provides the default value used when the list is empty. The explicit argument is the list whose last element is sought.

## Conventions

When applied to the empty list, `VTask.getLastI` returns `default` (the canonical inhabitant of `α` furnished by the `Inhabited` instance), rather than raising an error or returning an `Option`. This is the standard "junk value" convention for total functions on lists in Mathlib.

## Worked examples

- Claim: `VTask.getLastI ([] : List Nat) = 0` (the `Inhabited Nat` default is 0)
  ```lean
  example : VTask.getLastI ([] : List Nat) = 0 := by decide
  ```

- Claim: `VTask.getLastI [1, 2, 3] = 3`
  ```lean
  example : VTask.getLastI [1, 2, 3] = 3 := by decide
  ```

- Claim: `VTask.getLastI [42] = 42`
  ```lean
  example : VTask.getLastI [42] = 42 := by decide
  ```

- Claim: `VTask.getLastI [10, 20] = 20`
  ```lean
  example : VTask.getLastI [10, 20] = 20 := by decide
  ```

- Claim: For any non-empty list `l : List α`, `VTask.getLastI l` is equal to the value wrapped by `l.getLast?` (with `default` as fallback), i.e. `VTask.getLastI l = l.getLast?.getD default`.

## Boundaries

- **Empty list**: returns `default` (the `Inhabited` instance's default value), not a partial function or `none`.
- **Singleton list `[a]`**: returns `a` directly.
- **Two-element list `[_, b]`**: returns `b`, the second element.
- **General list**: recurses by dropping the first two elements, eventually hitting one of the above base cases; the result is always the final element of the original list.
- The function is defined for every list regardless of length; it is total.

## Not to be confused with

- `List.getLast?` — returns `Option α`, giving `none` on the empty list instead of a default value; `VTask.getLastI` is the "defaulted" variant.
- `List.getLast` — takes an explicit proof that the list is non-empty, rather than falling back to a default; not callable on an arbitrary list without the proof.
- `List.head` / `List.headI` — retrieves the *first* element of a list, not the last.