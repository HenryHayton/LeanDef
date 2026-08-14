## Object

`VTask.permutations'` takes a list and returns the list of all its permutations — every rearrangement of its elements, each as a separate list — collecting them into a single list. Concretely, a list `s` appears in the output if and only if `s` is a permutation (in the mathematical sense: same elements with the same multiplicities, possibly reordered) of the input list.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.permutations' : {α : Type u_1} -> List α → List (List α)
<!-- PINNED-SIGNATURE:END -->


`VTask.permutations' : {α : Type u_1} -> List α → List (List α)`

The implicit type argument `α` is the element type of the list. The single explicit argument is the list whose permutations are to be enumerated.

## Conventions

The empty list has exactly one permutation — itself — so `VTask.permutations' []` returns `[[]]`, a one-element list containing the empty list. The ordering of permutations in the output differs from the ordering produced by the alternative `permutations` function, but both produce the same collection up to permutation of the outer list.

## Worked examples

- Claim: `VTask.permutations' ([] : List Nat) = [[]]`
  ```lean
  example : VTask.permutations' ([] : List Nat) = [[]] := by decide
  ```

- Claim: `VTask.permutations' [1]` is `[[1]]`, a single-element list containing the singleton.
  ```lean
  example : VTask.permutations' [1] = [[1]] := by decide
  ```

- Claim: `VTask.permutations' [1, 2, 3]` has length 6 and contains exactly those lists that are permutations of `[1, 2, 3]`.
  ```lean
  example : (VTask.permutations' [1, 2, 3]).length = 6 := by decide
  ```

- Claim: `VTask.permutations' [1, 2, 3]` equals `[[1,2,3],[2,1,3],[2,3,1],[1,3,2],[3,1,2],[3,2,1]]` (the specific ordering given by this variant).
  ```lean
  example : VTask.permutations' [1, 2, 3] =
      [[1,2,3],[2,1,3],[2,3,1],[1,3,2],[3,1,2],[3,2,1]] := by decide
  ```

- Claim: For any lists `s` and `t`, `s ∈ VTask.permutations' t` if and only if `s` is a permutation of `t`.

- Claim: Applying a function elementwise to every permutation is the same as enumerating the permutations of the mapped list: `map (map f) (VTask.permutations' ts) = VTask.permutations' (map f ts)`.

## Boundaries

- **Empty list**: `VTask.permutations' [] = [[]]`. The output contains the empty list itself; the outer list has length 1.
- **Singleton list**: `VTask.permutations' [x] = [[x]]`. There is exactly one permutation of a one-element list.
- **Lists with repeated elements**: The function does not deduplicate. If the input has repeated elements, some output permutations may be equal as lists (equal as sequences), and the output list will contain them as separate entries.
- **Length of output**: For a list of length `n` with all distinct elements, the output has length `n!`. With repeats the output still has length `n!` (one entry per positional arrangement), but some entries may coincide.

## Not to be confused with

- `List.permutations`: The standard (more efficient) Mathlib permutation enumerator; produces the same set of permutations but in a different order. `VTask.permutations'` has simpler definitional equations.
- `List.Perm` (the `~` relation): A *proposition* asserting that two lists are permutations of each other, not a function enumerating them. `s ∈ VTask.permutations' t ↔ s ~ t` connects the two.
- `List.permutations'Aux`: The auxiliary helper that inserts a single element into every position of a given list, used internally to build `VTask.permutations'` but not the full permutation enumerator itself.