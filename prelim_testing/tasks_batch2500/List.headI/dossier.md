## Object

`VTask.headI` returns the first element of a list. If the list is non-empty, it returns its first element. If the list is empty, it returns the canonical default value supplied by the `Inhabited` type-class instance for the element type.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.headI : {α : Type u_1} -> [Inhabited α] -> List α → α
<!-- PINNED-SIGNATURE:END -->


`VTask.headI : {α : Type u_1} -> [Inhabited α] -> List α → α`

The implicit type argument `α` is the element type of the list. The instance argument `[Inhabited α]` supplies the default value of type `α` that is returned when the list is empty. The explicit argument is the list whose first element is to be retrieved.

## Conventions

When the input list is empty (`[]`), the function returns `default`, i.e. the distinguished inhabitant provided by the `Inhabited α` instance, rather than raising an error or returning an `Option`.

## Worked examples

- Claim: `VTask.headI ([] : List Nat) = 0` (since `default : Nat = 0`)
  ```lean
  example : VTask.headI ([] : List Nat) = 0 := by decide
  ```

- Claim: `VTask.headI [3, 1, 4] = 3`
  ```lean
  example : VTask.headI [3, 1, 4] = 3 := by decide
  ```

- Claim: `VTask.headI [true, false] = true`
  ```lean
  example : VTask.headI [true, false] = true := by decide
  ```

- Claim: For a single-element list `[42]`, `VTask.headI [42] = 42`.
  ```lean
  example : VTask.headI [42] = 42 := by decide
  ```

## Boundaries

- **Empty list**: The function is total; on `[]` it returns `default` (the `Inhabited` instance's designated element). For `Nat` this is `0`, for `Bool` it is `false`, for `String` it is `""`.
- **Single-element list**: Returns that unique element.
- **Multi-element list**: Returns only the first element; the tail is completely ignored.

## Not to be confused with

- `List.head?` — returns `Option α`, yielding `none` on the empty list rather than a default value.
- `List.head` — a version that requires a proof that the list is non-empty as an argument, avoiding the need for an `Inhabited` instance.
- `List.getLast!` / `List.lastI` — retrieves the *last* element of the list, not the first.