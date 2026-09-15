## VTask.insertIdx

### Object

Given an element `a` of type `α`, a position index `i`, and a length-`n` vector `v`, `VTask.insertIdx a i v` produces a new length-`(n+1)` vector formed by inserting `a` at position `i` inside `v`. All elements of `v` that originally appeared at positions `i, i+1, …, n-1` are shifted one step to the right to make room for `a`; elements before position `i` are unchanged.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.insertIdx : {α : Type u_1} -> {n : ℕ} -> (a : α) -> (i : Fin (n + 1)) -> (v : List.Vector α n) -> List.Vector α (n + 1)
<!-- PINNED-SIGNATURE:END -->


The first argument `a` is the element to be inserted. The second argument `i` is the position (as a `Fin (n + 1)` index, so it ranges from `0` to `n` inclusive) at which `a` will be placed in the resulting vector. The third argument `v` is the source vector of length `n` into which the element is inserted.

### Conventions

When `i = 0` (the smallest valid index), `a` is prepended to the front of `v` and all original elements shift right by one. When `i = n` (the largest valid index, i.e., `Fin.last n`), `a` is appended after all elements of `v`, leaving the original elements in their original positions.

### Worked examples

- Claim: Inserting `5` at position `0` into the vector `[1, 2, 3]` yields `[5, 1, 2, 3]`.
  ```lean
  example : (VTask.insertIdx 5 ⟨0, by omega⟩ ⟨[1, 2, 3], rfl⟩ : List.Vector ℕ 4) =
            ⟨[5, 1, 2, 3], rfl⟩ := by decide
  ```

- Claim: Inserting `99` at position `2` (the last valid position) into the vector `[7, 8]` yields `[7, 8, 99]`.
  ```lean
  example : (VTask.insertIdx 99 ⟨2, by omega⟩ ⟨[7, 8], rfl⟩ : List.Vector ℕ 3) =
            ⟨[7, 8, 99], rfl⟩ := by decide
  ```

- Claim: Inserting `0` at position `1` into `[10, 20, 30]` yields `[10, 0, 20, 30]`.
  ```lean
  example : (VTask.insertIdx 0 ⟨1, by omega⟩ ⟨[10, 20, 30], rfl⟩ : List.Vector ℕ 4) =
            ⟨[10, 0, 20, 30], rfl⟩ := by decide
  ```

### Boundaries

- The index type `Fin (n + 1)` guarantees that `i` is always a valid insertion point; there is no out-of-bounds case.
- Inserting into a length-`0` vector is valid: the only choice is `i = ⟨0, …⟩`, and the result is the singleton vector `[a]`.
- The result always has length exactly `n + 1`, enforced by the type; the length invariant is maintained regardless of `i`.
- Inserting at `i = 0` is semantically equivalent to `cons a v`; inserting at `i = n` is semantically equivalent to appending `a` at the end.

### Not to be confused with

- `List.Vector.set` — replaces the element at a given index rather than inserting a new one (the length is unchanged).
- `List.Vector.cons` — always prepends an element at position `0`; `VTask.insertIdx` generalises this to any valid position.
- `List.insertIdx` — the analogous operation on plain lists, without the compile-time length guarantee that `VTask.insertIdx` carries in its type.